"""Remove computer generated garbage such as

   *.py~
   *.pyc
   *.o   
   *.so
   *.dll

Note: Recompile ANUGA after running this script
"""

import os
import tempfile

from eqrm_code import util

def files_to_delete(filenames_to_delete, extensions_to_delete, dir="."):
    for dirpath, dirnames, filenames in os.walk(dir):

        #print 'Searching dir', dirpath
        if '.svn' in dirnames:
            dirnames.remove('.svn')  # don't visit SVN directories

        for filename in filenames:
            for ext in extensions_to_delete:
                if filename.endswith(ext):
                    absname = os.path.join(dirpath, filename)
                    filenames_to_delete.append(absname)


def find_files():
    extensions_to_delete = ['~',
                            '.pyc','.pyo',       # Python
                            '.o', '.so', '.dll', '.pyd', # C
                            '.aux', '.ps']        # LaTeX 

    filenames_to_delete = []
    files_to_delete(filenames_to_delete, extensions_to_delete)

    # remove the compiled weave code.
    weave_path = util.get_weave_dir()
    extensions_to_delete.append('.cpp')
    extensions_to_delete.append('_catalog')
    files_to_delete(filenames_to_delete, extensions_to_delete, dir=weave_path)


    #FIXME remove the scenario test current files.

    return filenames_to_delete

def clean_all_main(verbose=True, prompt=True):
    filenames_to_delete = find_files()
    if verbose is True:
        for file in filenames_to_delete:
            print '  Flagged for deletion', file            
        print
    if prompt is True:    
        N = len(filenames_to_delete)             
        if N > 0:
            msg = '%d files flagged for deletion. Proceed? (Y/N)[N]' %N
            answer = raw_input(msg)

            if answer.lower() == 'y':
                for filename in filenames_to_delete:
                    if verbose is True:
                        print 'Deleting', filename
                    os.remove(filename)
            else:
                print 'Nothing deleted'
        else:
            print 'No files flagged for deletion'
    else:
        for filename in filenames_to_delete:
            if verbose is True:
                print 'Deleting', filename
            os.remove(filename)
        


#-------------------------------------------------------------
if __name__ == "__main__":
    clean_all_main(verbose=True, prompt=True)
