
Introduction
	
The EQRM builds on existing open source packages and it uses multiple
languages (C and Python) to obtain an optimal trade-off between
useability and speed. For these two reasons the installation process
contains multiple steps.

Currently EQRM can be installed on the Windows and Linux operating
system. Installation on the Mac has not been tested.

For any help, please post to eqrm-user@lists.sourceforge.net
(https://sourceforge.net/mail/?group_id=198293). Also, to
keep up to date with EQRM, join the list.

We would also like to hear from you if you
are not able to install the software. 

EQRM is currently dependant on; 
python
numpy
scipy
Shapely
gcc

The above requirements are for the 'core' of EQRM. The plotting functions
require one or more of the following:
matplotlib
GMT

Note: when *\eqrm_core\eqrm_code is used below you need to replace
the * with the actual place you have installed EQRM on your computer.

WINDOWS INSTALL INSTRUCTIONS:
1. Delete any old versions of EQRM from your system.

2. Unzip the eqrm_install file (e.g.eqrm_versionX.X.svn_X.zip)
 
3. Install python from
   http://www.python.org/download/
   - We recommend python2.5 although python2.4 is also acceptable.
   Note the python packages you install must be for your version of
   python.

4. Install numpy from
   http://numpy.scipy.org/
    (if you are installing to python 2.4, the version must be no later than 
   http://prdownloads.sourceforge.net/numpy/numpy-1.0.2.win32-py2.4.exe?download)

5. Install scipy from 
   http://scipy.org 
   (if you are installing to python 2.4, the version must be no later than 
   http://prdownloads.sourceforge.net/scipy/scipy-0.5.2.1.win32-py2.4.exe?download)

6. If you are updating an existing copy of numpy, delete the "python24_compiled" folder:
On WINNT "C:\WINNT\Profiles\YOUR USERNAME\Local Settings\Temp\YOUR
USERNAME\python24_compiled". 
ON XP "C:\Documents and Settings\YOUR USERNAME\Local Settings\Temp\\YOUR
USERNAME\python24_compiled"
(this is where your inline c code is
compiled - it is not compatible between numpy versions - deleting it
now forces weave to re-compile the required components)

7. Install Shapely 1.X.X (python GIS kit) from
   http://pypi.python.org/pypi/Shapely/.   
   (If you are using Python 2.4, you will have to install ctypes as well)

    
8. Install the full package of MinGW. (TICK THE G++ COMPILER)
   When installing using mingw-5.X.X.exe, you are asked to choose
   components.  Tick the g++ compiler and do not untick any components.
   http://www.mingw.org/

9. Add C:\MinGW\bin (so you can compile c extensions to python) and
   C:\Python25 (so you can call Python from a DOS prompt) to your path
   and *\eqrm_core\ to your pythonpath:

   a) right click My Computer - go to properties - Advanced -
   Environment Variables 
   
   b) If a variable called "path" already exists in User Variables:
          select path then 'press Edit..."
          otherwise press "New..."
	  
   c) Variable Name = PATH, add "C:\MinGW\bin;C:\Python25;" 
   (or python24) to
   Variable Value (use ";" to separate values).
   
   d) Variable Name = PYTHONPATH, add "*\python_core\;" to
   Variable Value (use ";" to separate values).

10. Optional: install gzip working with compressed
   output. http://gnuwin32.sourceforge.net/downlinks/gzip.php
  
11. At the dos prompt:
    cd *\eqrm_core\eqrm_code
    python test_all.py	
    cd ..
    python check_scenarios.py
    
If you get a Could not locate executable g++ error, it means MinGW is
not working.  Check steps 9 and 10. 

To install the components required for any plotting you may require, do:
1. Install matplotlib from [http://sourceforge.net/projects/matplotlib/].
   You must choose the file to install that matches your operating system
   'type' and python version. For example, the matplotlib install file
   [matplotlib-0.98.5.2.win32-py2.5.exe] is meant for a Win32 system running
   python 2.5.

2. If you require any visualisation with a map in it, install GMT from
   [http://gmt.soest.hawaii.edu/gmt/gmt_windows.html].  You will need the
   [Basic GMT distribution] and the [High and Full resolution GSHHS coastlines]
   installs.
    
 _________________________________
 For developers running using the SVN repository
 
 If you want to run the coverage scrips(coverage_of_tests.py) the python
 coverage module needs to be installed.  To do this go to;
   http://www.nedbatchelder.com/code/modules/coverage.html
 and follow the install instructions. Note, if the file is
 downloaded as coverage-2.77.tar.tar, change it to
 coverage-2.77.tar.gz.

 
-----------------------------------------------------------------------------


GENERAL LINUX INSTALL INSTRUCTIONS:
There are a variety of Linux distributions.  The best instructions for
installing each of the necessary packages is found at the website of
each package, so only general instructions are given here.

Install;
* python 2.4 + (http://www.python.org/download/)
* python-dev
* python package numpy (http://numpy.scipy.org/)
* python package scipy , (http://www.scipy.org/)
* python package libgeos_c (for shapely)
* python package python-setuptolls (for installing shapely using easy_install)
* python package shapely  (see notes below) (http://pypi.python.org/pypi/Shapely/)
* python-numeric
(http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=1351)
* gcc also needs to be installed. Using versions higher than 4.2 have
caused problems with weave.
 
 Unzip the eqrm_install file (e.g.eqrm_versionX.X.svn_X.zip) to where
 ever you want it.
 
Set the environment variable PYTHONPATH to *\eqrm_core (where the
EQRM software was installed.)
    
in the *\eqrm_core\ directory;
    python test_all.py     - to test that individual parts of the code work
    python check_scenarios.py - to run some scenarios and check the
    output
    
    6/03/09 - I installed EQRM on a debian system.  Test_all failed
    due to the inline compiler (weave) failing.  To fix I get g++ to
    work with g++_4.2, instead of g++_4.3.  Weave will also fail if
    python-dev is not installed.

To install the components required for any plotting you may require, install:
* python-matplotlib
* gmt

When you install GMT you will need to install the high and full resolution
coastlines.  Get these from http://gmt.soest.hawaii.edu/ by clicking on the 
'DOWNLOAD' link and then clicking on the 'INSTALL FORM' link.  You choose
many options on the form - if you do not understand a choice it is usually
safe to leave the default choice, with the exception of the NetCDF question.
Unless you are sure you already have NetCDF 3.6.x installed, always ask for
NetCDF to be installed.  You should also select the high-resolution and
full-resolution coastline data installs.

Note that in question 8 you can install GMT anywhere you wish, though you
may choose to use the suggested directories (such as /usr/local, for example).
Note that if you do choose a 'system' place you will need to do it via 'sudo'.
_________________________________________________
Notes for installing Shapely on a Linux system
**please note that shapely is not produced by us so the install process
  may vary over time. 

  a)  download and install ez_setup.py - need to be root
      (http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install)
  b)  If using Python2.4 install ctypes - (easy_install ctypes)
	(http://pypi.python.org/pypi/ctypes/)
  c)  download and install the GIS library (i.e. libgeos_c)

	To install on debian
		apt-get install libgeos-c1

	To install on Suse (need to be root)
		dowload geos (e.g. geos-3.0.0.tar.bz2)
		from http://trac.osgeo.org/geos/

		tar xvfj geos-3.0.0.tar.bz2
		cd geos-3.0.0
		./configure
		./make
		./make install
		ldconfig

  d) install shapely (http://pypi.python.org/pypi/Shapely) 
  (sudo easy_install Shapely)
_________________________________________________  

----------------------------------------------------------------

NOTES:

*** Python libraries for python 2.4.x are not compatible with python
    2.3.x or python 2.5.x

*** Scipy is dependent on numpy, so numpy must be installed before
    scipy, and the two versions must be compatible.

*** If you use numpy version < 1 (NOT RECOMENDED), you will need to
    search and replace newaxis with NewAxis throughout the code.
    
*** To find out the version of numpy, do
    import numpy
    numpy.version.version
    
*** To find out the version of scipy, do
    import scipy
    scipy.version.version
    
*** libgeos_c might be able to be installed by 
    yum install libgeos-devel, or 
    yum install geos-devel      
