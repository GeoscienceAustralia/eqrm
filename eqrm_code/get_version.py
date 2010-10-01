"""Obtain the latest revision number and date from Subversion. 

Using the tool SubWCRev.exe on the download page on the SVN website or
in the TortoiseSVN Folder under bin.

To create run 

#SubWCRev.exe path\to\working\copy version.in version.h
SubWCRev.exe . ver.txt ver.py

"""
import os
import sys
import commands
from os.path import join
import tempfile

template = 'version.txt'
version = 'version.py'

#Write out template
txt = """version = $WCREV$
status = '$WCMODS?Modified:Not modified$'
date = '$WCDATE$'
"""

asc  = """$WCREV$
'$WCMODS?Modified:Not modified$'
'$WCDATE$'
"""


def get_version():
    """
    To be used for sandpit and distribution versions.
    """
    try:
        # The stored_version_info.py file is created during the distribution
        # process.
        import stored_version_info
        version = stored_version_info.version
        date = None
        modified = None
    except:
        if sys.platform == 'win32':  # Windows
            version, date, modified = get_version_sandpit_windows()
        else:
            version, date, modified = get_version_sandpit_linux()
    return version, date, modified

def get_version_sandpit_linux():
    """
    #FIXME: This only gives the most recent version info in the current dir
    """
    output = commands.getoutput('svnversion')
    print "*******" + str(output) + "**********"
    splitoutput = output.split(":")
    #print "splitoutput", splitoutput
    #if splitoutput[0][-1:] == "M":
    #    splitoutput[0] = splitoutput[0][:-1]
    version = splitoutput[0]
    
    
    date = None
    modified = None
    return version, date, modified
    
    

def get_version_sandpit_windows():
    """
    return SVN information on windows systems

    returns version, last check in date, modified

    version - commited at? updated to?  Maybe these are only diff if
              the sandpit is rolled back.
    Last committed at revision 439
    Updated to revision 439
    Local modifications found

    This function outputs to screen.

    It will only work if TortoiseSVN has been installed and
    SubWCRev.exe can be executed.
    """
    handle, file_in = tempfile.mkstemp('.asc','eqrm_get_version_')
    os.close(handle)
    
    handle, file_out = tempfile.mkstemp('.asc','eqrm_get_version_')
    os.close(handle)
        
    # create  template file
    fid = open(file_in, 'w')
    fid.write(asc)
    fid.close()

    #Run conversion
    cmd = 'SubWCRev.exe . %s %s' %(file_in, file_out)
    err = os.system(cmd)
    if err != 0:
        #msg = 'Command %s could not execute.'
        #msg += 'Make sure the program SubWCRev.exe is available on your path'
        #raise msg
        
        # Delete files
        os.remove(file_out)
        os.remove(file_in)
        version = 0
        modified = 'Not known'
        date = 'Not known'
        return version, date, modified
    
    fid = open(file_out, 'r')
    lines = fid.read().splitlines()
    lines = [L.strip("'") for L in lines]
    fid.close()

    # Delete files
    os.remove(file_out)
    os.remove(file_in)
    
    version = int(lines[0])
    modified = lines[1]
    date = lines[2]
    return version, date, modified

def broken_get_version(destination_path):
    """
    cmd = 'from %s import version, status, date' %version[:-3]
    might import an old copy of version.py, depending which dir the
    contoling program is.

    read the file in and parse, rather than making a python file.
    """
    
    # create  template file
    fid = open(template, 'w')
    fid.write(txt)
    fid.close()

    #
    version_path = join(destination_path, version)
    
    #Run conversion
    cmd = 'SubWCRev.exe . %s %s' %(template, version)
    err = os.system(cmd)
    if err != 0:
        msg = 'Command %s could not execute.'
        msg += 'Make sure the program SubWCRev.exe is available on your path'
        raise msg



    #Obtain version
    cmd = 'from %s import version, status, date' %version[:-3]
    #print cmd
    exec(cmd)

    return version

#-------------------------------------------------------------
if __name__ == "__main__":
    version, date, modified =  get_version()
    print "version", version
    print "date", date
    print "modified", modified