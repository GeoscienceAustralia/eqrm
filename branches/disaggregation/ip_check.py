"""

Title: 
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2008-03-11 

  Description:Audit the directories flagged for released

This module forms an easy way to audit data files in the repository.

The benefit is that license files can be tested before being checked in.

Note: This script will work on all data whether it is part of the
repository or not. Before creating a license file for a data file it
is a good idea to see if it is part of the repository or not (in which
case there is no need). This can be done using svn status or by
deleting the offending area and do a fresh svn update.
  

  Version: $Revision: 444 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2008-01-29 17:14:38 +1100 (Tue, 29 Jan 2008) $


"""
import sys
from os import sep, listdir, path #, remove, walk


from eqrm_code.eqrm_audit_wrapper import eqrm_audit_wrapper
from distribution import distro_dirs, distro_files

def main():
    #root_eqrm = '.' # So this has to run in the root eqrm dir
    root_eqrm, tail = path.split( __file__)
    if root_eqrm == '':root_eqrm ='.'

    # Check all the dirs that are distributed
    for dir in distro_dirs:
        eqrm_audit_wrapper(root_eqrm + sep + dir)

    # Check the root files that are distributed
    eqrm_audit_wrapper(root_eqrm,directories_to_ignore=listdir(root_eqrm))

if __name__ == "__main__":
    if not sys.platform == 'win32':  #Windows
        print 'Ip_check.py only works in windows'
        import sys; sys.exit() 
    
    if len(sys.argv) > 1:
        eqrm_audit_wrapper(sys.argv[1])
    else:
        main()
