"""

Title: eqrm_audit_wrapper.py
  
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2008-03-11 

  Description:
  
  Call the IP auditor. Add the standard extersions, directories and
  files to ignore. This script has nothing to do with earthquakes.
  

  Version: $Revision: 1713 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-06-17 16:22:06 +1000 (Thu, 17 Jun 2010) $


"""

from eqrm_code.ANUGA_utilities.data_audit import IP_verified

# Ignore source code files
standard_extensions_to_ignore = ['.py','.c', '.h', '.cpp', '.f', '.bat', '.m',
                        '.sh','.awk','.dll', '.pyd', '.for']

# Ignore LaTeX documents
standard_extensions_to_ignore += ['.tex', '.sty', '.cls', '.bib', '.def',
                                  '.dvi']

# Ignore pdf and doc documents
standard_extensions_to_ignore += ['.pdf', '.doc']

# Ignore images
standard_extensions_to_ignore += ['.png', '.gif', '.sun', '.eps']

# Ignore EQRM par setup files 
standard_extensions_to_ignore += ['.par']

# Misc'
standard_extensions_to_ignore += ['.asc', '.py,cover', '.zargo']

# html files
standard_extensions_to_ignore += ['.htm', 'css']

# Ignore generated stuff 
standard_extensions_to_ignore += ['.pyc', '.o', '.so', '~']
standard_extensions_to_ignore += ['.aux', '.log', '.idx', 'ilg', '.ind',
                         '.bbl', '.blg', '.syn', '.toc']

# Ignore license files themselves
standard_extensions_to_ignore += ['.lic']    


# Ignore certain other files,
standard_files_to_ignore = ['README-documentation.txt',
                            '.project',
                            'README',
                            'README.txt',
                            'README-getting-started.txt',
                            'README-getting-started.txt',
                            'README-install.txt',
                            'README-tests.txt',
                            'README-demo-risk.txt',
                            'README-GA.txt',
                            'README_plot_routines.txt',
                            'README_plotting_overview.txt',
                            'README_imp_unit_test_coverage.txt',
                            'README_notes.txt',
                            'README_system_coverage.txt',
                            'RcPerWrtBuildCFCBusageEdwards.xls'  # CRC changes
                            ]


# Ignore directories
standard_directories_to_ignore = ['.svn']

# Avoid the data output files for demos and the imp tests.
standard_directories_to_ignore += ['output', 'current', 'mini_current',
                                   'mini_standard', 'standard',
                                   'risk_seperated',
                                   'hazard_seperated']

def eqrm_audit_wrapper(directory,
                       extensions_to_ignore=None,
                       directories_to_ignore=None,
                       files_to_ignore=None,
                       verbose=True):
    #global standard_extensions_to_ignore
    #global standard_files_to_ignore
    #global standard_directories_to_ignore
    
    if extensions_to_ignore == None:
        extensions_to_ignore = []
    extensions_to_ignore += standard_extensions_to_ignore

    if directories_to_ignore == None:
        directories_to_ignore = []
    directories_to_ignore += standard_directories_to_ignore  

    if files_to_ignore == None:
        files_to_ignore = []
    files_to_ignore += standard_files_to_ignore   
    
    result = IP_verified(directory,
                       extensions_to_ignore,
                       directories_to_ignore,
                       files_to_ignore,
                       verbose=verbose)    
    return result

if __name__ == '__main__':
    eqrm_audit_wrapper('..\\')
