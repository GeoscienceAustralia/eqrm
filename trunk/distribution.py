"""

Create the distribution zip file.

General paradigm is files and dir's are chosen to be distributed,
rather than having everything automatically distributed.  This stops
getting junky files/dir's getting into the distribution.

"""
import sys
import tempfile
import re
import os
from shutil import copyfile, copytree, rmtree
from os import system, remove, sep, getcwd, chdir, rmdir, mkdir, popen, \
     listdir
from os.path import join, isfile

from for_all_verification import do_tests_checks_demos_audits

# directories to include in the distro, at the root level
distro_dirs = [
    'demo',
    'Documentation',
    'eqrm_code',
    'implementation_tests',
    'Matlab_utils',
    'postprocessing',
    'preprocessing',
    'resources',
    'test_resources'
    ]

# files to include at the root level
# Note copyright.pdf is created from copyright.tex
distro_files = [
    'check_scenarios.py',
    'clean_all.py',
    'copyright.tex',
    'eqrm_analysis.py',
    'README.txt',
    'README-getting-started.txt',
    'README-getting-started.txt',
    'README-install.txt',
    'README-tests.txt',
    'test_all.py'
    ]
    
def main():
    create_distribution_zip('eqrm_version2.0.',distro_dirs=distro_dirs,
                                   distro_files=distro_files)
    
def create_distribution_zip(vername, distro_dirs=None,
                                   distro_files=None):
    """
    Create a zip file that can be posted to source forge.

    vername - part of the distribution file;
              vername+'svn'+version+'.zip'

    distro_dirs - directories in python_eqrm to be included in the zip file.

    distro_files - files in python_eqrm to be included in the zip file.

    return:
      Return False if create_distribution_zip fails
    """
    
    # Exporting the eqrm root repository to the temp file
    expo_dir = tempfile.mkdtemp(prefix='EQRM_distribution_expo_dir')
    print "expo_dir", expo_dir

    # When using this, make sure the expo_dir is not deleted in 2 places.
    
    if False: 
        s = 'svn --force export http://65.61.168.30/svn/eqrm_core/trunk '\
            + expo_dir
    
        print s
        
        print "This will take a while..."
        
        fid = popen(s)
    
        version_info = fid.read()
        for line in version_info.split('\n'):
            # print "line", line
            if line.startswith('Exported'):
                
                version = re.findall(re.compile(r'[0-9]+'),line)
                if len(version)==1:
                    version = version[0]
                    print "Got a version number:" , version
                else:
                    print "Could not get version number.  Got this instead",  \
                          version
                    print "WARNING: Using incorrect version number."
                    version ='999'
        fid.close()
    else:
        expo_dir = join("C:","WINNT","Profiles","gray duncan",
                        "Local Settings","Temp",
                        "EQRM_distribution_expo_dir-uphuz")
        expo_dir = join("c:\\","winnt","Profiles","graydu~1",
                        "locals~1","temp",
                        "EQRM_distribution_expo_dir-uphuz")
        version = '999'
        
        
    # create another temp dir to move things into
    temp_dir = tempfile.mkdtemp(prefix='EQRM_distribution_temp_dir')
    eqrm_dir_name = 'python_eqrm'
    # zip_dir is the directory where files to be distributed are placed
    zip_dir = join(temp_dir, eqrm_dir_name)
    mkdir(zip_dir)
    print "zip_dir", zip_dir

    # Copy the dir's we want to distribute
    for dir in distro_dirs:
        # Fail silently if I can't copy a dir.
        src = join(expo_dir, dir) 
        dst = join(zip_dir, dir)
        copytree(src, dst)
    
    # Copy the file's we want to distribute
    for file in distro_files:
        # Fail silently if I can't copy a file.
        src = join(expo_dir, file)
        dst = join(zip_dir, file)
        try:
            copyfile(src, dst)
        except:
            pass
        
    # I tried doing the compile stuff before moving files.
    # It didn't work for me.
    
    # compile the copyright document
    current_dir = getcwd()
    chdir(zip_dir)
    print '       '
    print 'compiling the copyright document'
    s = 'latex copyright.tex'
    print s
    system(s)
    s = 'dvipdfm copyright.dvi'
    print s
    system(s)
    remove('copyright.tex')
    remove('copyright.log')
    remove('copyright.aux')
    remove('copyright.dvi')
    try:    
        remove('copyright.tex.bak')
    except:
        pass

    # Move the EQRM inputs pdf to the Documentation directory. 
    src = join(expo_dir, 'latex_sourcefiles', 'manual_tech', 'EQRM_inputs.pdf')
    dst = join(zip_dir, 'Documentation', 'EQRM_inputs.pdf')
    try:
        copyfile(src, dst)
    except:
        print "***************************************"
        print "***  Could not move EQRM_inputs.pdf ***"
        print "***************************************"

    if False:
        chdir('latex_sourcefiles')
        chdir('manual_tech')
        file_base = 'EQRM_inputs'
        print '       '
        print 'compiling the new parameter list'
        s = 'latex ' + file_base + '.tex'
        print s
        system(s)
        s = 'dvipdfm ' + file_base + '.dvi'
        print s
        system(s)
        if False:
            for ext in ['.tex', '.log', '.aux', '.dvi']:  
                try:    
                    remove(file_base + ext)
                except:
                    pass
            try:    
                remove(file_base + '.bak')
            except:
                pass
            chdir('..')
            chdir('..')

    chdir('Documentation')
    # Remove, this dir is not our IP, we shouldn't distribute.
    rmtree('coding_standards')
    
    # Add the stored_version_info.py file to eqrm_code
    chdir('..')
    chdir('eqrm_code')
    fid = open('stored_version_info.py', 'w')
    fid.write('version = '+version+'\n')
    fid.close()
    remove('test_cadell_damage.py')
    rmtree('plotting')
    
    
    #eqrm_code_dir = join(zip_dir,'eqrm_code')
    #store_version_info(eqrm_code_dir)
    
    
    # Create the zip file before running tests which create .pyc
    zip_file = vername+'svn'+version+'.zip'
    repos_distro_file = join(current_dir,'distribution', zip_file)
    
    chdir(temp_dir)
    print '   '
    print 'zipping application into  ', repos_distro_file
    system('zip -r -q '+zip_file+' '+eqrm_dir_name)

    # Haven't tried
   #  # List all files in the current directory
# allFileNames = os.listdir( os.curdir )

# # Open the zip file for writing, and write some files to it
# myZipFile = zipfile.ZipFile( "spam_skit.zip", "w" )

# # Write each file present into the new zip archive, except the python script
# for fileName in allFileNames:
#     (name, ext) = os.path.splitext( fileName )
#     if ext != ".py":
#         print "Writing... " + fileName
#         myZipFile.write( fileName, os.path.basename(fileName), zipfile.ZIP_DEFLATED )

# myZipFile.close()

    # Run all the tests
    results_passed = do_tests_checks_demos_audits(
        eqrm_root_dir=zip_dir,
        ip_audit=True,
        test_all=True,
        check_scenarios=True,
        mini_check_scenarios=False,
        check_risk=False,
        demo_batchrun=True,
        verbose=True)
    if results_passed is False:
        os.remove(zip_file) # delete the zip file.  It is a fail
        clean_up(current_dir, temp_dir, expo_dir)
        return False
    
    chdir(temp_dir)
    # Move the zip file to the repository distro dir
    copyfile(zip_file,repos_distro_file)

    clean_up(current_dir, temp_dir, expo_dir)

def clean_up(current_dir, temp_dir, expo_dir):
    chdir(current_dir)
    rmtree(temp_dir)
    #rmtree(expo_dir)

if __name__ == '__main__':
    if sys.platform == 'win32':  #Windows
        main()
    else:
        print 'Distribution.py only works in windows'
