"""Obtain the latest revision number and date from Subversion. 

Using the tool SubWCRev.exe on the download page on the SVN website or
in the TortoiseSVN Folder under bin.

To create run 

#SubWCRev.exe path\to\working\copy version.in version.h
SubWCRev.exe . ver.txt ver.py

"""
import os
import re
import sys
import subprocess
from os.path import join
import tempfile
from xml.dom import minidom

from eqrm_code.eqrm_filesystem import eqrm_path

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
    version, date, _ = get_svn_revision_sandpit_linux()
    print "*******" + str(version) + "**********"
    
    modified = None
    return version, date, modified

def get_svn_revision_sandpit_linux(path=None):
    """
    Returns the SVN revision and other data - does not comform to the get_version()
    return format so leaving separate for now.
    Based on method used in django 
    (https://code.djangoproject.com/browser/django/trunk/django/utils/version.py)
    """
    commit = "exported"
    date = None
    url = None
    
    if path is None:
        path = eqrm_path
    
    # Determine whether the path has svn info, then read from the info xml 
    entries_path = '%s/.svn/entries' % path
    if os.path.exists(entries_path):
        try:
            info_xml = os.popen('svn info --xml %s' % path)
            dom = minidom.parse(info_xml)
            url = dom.getElementsByTagName('url')[0].firstChild.toxml()
            commit = dom.getElementsByTagName('commit')[0].getAttribute('revision')
            date = dom.getElementsByTagName('date')[0].firstChild.toxml()
        except:
            # for NCI - nodes higher than 8 do not appear to return output 
            pass
        
    return commit, date, url

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

    # Run conversion
    cmd = ['SubWCRev.exe', '.', file_in, file_out]
    fnull = open(os.devnull, 'w') 
    try:
        # Suppress stdout and stderr by piping to devnull
        subprocess.check_call(cmd, stdout=fnull, stderr=fnull)
        fnull.close()
    except:
        fnull.close()
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
    
    print "*******" + str(version) + "**********"
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
