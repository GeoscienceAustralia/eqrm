#!/bin/env python

"""Testlet to check that packages required are importable"""


# packages we are testing
Package_Imports = ('from Scientific.IO.NetCDF import NetCDFFile',
                   'import numpy',
                   'import Numeric',
                   'import RandomArray',
                   'import pypar',
                   'import scipy',
                   'import matplotlib',
                   'import pylab',
                   'import wxPython',
                   'import sqlalchemy',
                  )


Package_Imports = (
                   'import numpy',
                   'import Numeric',
                   'import RandomArray',
                   'import scipy',
                   'import matplotlib',
                   'import Shapely',
                   'import pypar',
                   'from Scientific.IO.NetCDF import NetCDFFile'
                  )


name = 'Test if python packages are importable'

def python_packages():
    result = True
    
    # test each import
    num_errors = 0
    error_packages = []
    
    for pkg in Package_Imports:
        try:

            exec pkg

        except ImportError, e:
            error_packages.append(pkg)
            num_errors += 1
            result = False
        except:
            error_packages.append(pkg)
            num_errors += 1
            result = False

    # report errors
    if num_errors == 0:
        print 'All OK.'
    else:
        print 'Failed'
        print error_packages
    
    return result

def versions():
    import scipy
    import numpy
    print "scipy.__version__", scipy.__version__
    print "numpy.__version__", numpy.__version__
if __name__ == '__main__':
    
    python_packages()
    versions()
