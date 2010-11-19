"""

Title: set_current_to_standard - move the current scenario result
  files to the standard dir.  You do this when the standard needs to
  be updated.
 
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2007-10-9 

  Description:
  
   This script moves the current scenario result files to the standard
  dir.

   The results in 'standard' dir represent the correct results.

  Version: $Revision: 1626 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-21 17:28:13 +1000 (Wed, 21 Apr 2010) $


"""

from os import listdir, path
from eqrm_code.check_scenarios import STANDARD_DIR, CURRENT_DIR, \
     MINI_STANDARD_DIR, MINI_CURRENT_DIR
from shutil import copyfile

def main():
    current2standard(CURRENT_DIR, STANDARD_DIR)
    current2standard(MINI_CURRENT_DIR, MINI_STANDARD_DIR)
    
def current2standard(current_dir, standard_dir):
    current_dirs = listdir(current_dir)
    try:
        current_dirs.remove('.svn')
    except:
        pass
    
    print 'moving from;'
    for dir in current_dirs:
        print dir
        cur_files = listdir(path.join(current_dir, dir))
        
        try:
            cur_files.remove('.svn')
        except:
            pass
        try:
            cur_files.remove('log.txt')
        except:
            pass
        for file in cur_files:
            move_file = path.join(current_dir, dir, file)
            move_to_here = path.join(standard_dir, dir, file)
            copyfile(move_file,move_to_here)


#-------------------------------------------------------------
if __name__ == "__main__":
     main()
#     if sys.platform == 'linux2':  #Windows
#         main()
#     else:
#         print 'Run set current to standard in Linux.'
#         print 'To avoid checking in EOL system differences.'
