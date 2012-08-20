
========================================================================
A. INTRODUCTION
	
The EQRM builds on existing open source packages. It uses multiple
languages (C and Python) to obtain an optimal trade-off between
usability and speed. For these two reasons the installation process
contains multiple steps.

The EQRM can be installed on Windows, Linux or Mac operating
systems.

For help, please post to eqrm-user@lists.sourceforge.net
(https://sourceforge.net/mail/?group_id=198293). Also, to
keep up to date with EQRM, join the list.

We would also like to hear from you if you
are not able to install the software. 

EQRM DEPENDANCIES:
1) python (version 2.5 or greater)
2) numpy (version 1.6.0 or later)
3) scipy (version 0.9.0 or later)
4) Shapely (version 1.2.15 or later)
5) gcc 

Notes for EQRM dependencies:
* Version numbers are a guide only. The EQRM may work with earlier
  versions. 

FOR EQRM PLOTTING TOOLS:
The above requirements are for the 'core' of the EQRM. For plotting
you must install the following:
6) matplotlib (version 1.1.0 or later)
7) GMT (we recommend version 4.5.8)

Notes for EQRM plotting tools:
* The plotting tools are designed for quick output QA. They can be used to 
  create publication images but they were not designed for this purpose. You
  need to interact with the data and create your own plotting tools if 
  you are not happy with EQRM image quality for your publication. 
* you can skip matplotlib and GMT if you do not wish to use the EQRMs
  inbuilt plotting functionality
* you can skip GMT if you do not wish to use the EQRM to make maps 
  * install GMT with high and full resolution coastlines.  Get these from 
    http://gmt.soest.hawaii.edu/ by clicking on the  'DOWNLOAD' link and 
    then clicking on the 'INSTALL FORM' link.  You choose
    many options on the form - if you do not understand a choice it is usually
    safe to leave the default choice, with the exception of the NetCDF question.
    Unless you are sure you already have NetCDF installed, always ask for
    NetCDF to be installed.  You should also select the high-resolution and
    full-resolution coastline data installs.

TEST COVERAGE SCRIPTS FOR DEVELOPERS ONLY:
If you want to run the coverage scripts (coverage_of_tests.py) the python
coverage module needs to be installed.  To do this go to;
   http://www.nedbatchelder.com/code/modules/coverage.html
and follow the install instructions. Note, if the file is
downloaded as coverage-2.77.tar.tar, change it to
coverage-2.77.tar.gz.

Note: when *\eqrm_core is used below you need to replace the * with the 
actual place you have installed EQRM on your computer.

========================================================================
B. DOWNLOADING THE EQRM

There are two options for downloading the EQRM:

OPTION 1 (RECOMENDED): Download the latest trunk from Google Code

* follow instructions at: 
    http://code.google.com/p/eqrm/source/checkout

* Note that you will need a subversion client to do this. You can use any 
  subversion client you like. On the mac and Linux, we use command line
  subversion in a xterminal. You can get command line subversion on 
  Windows by installing cygwin (make sure you tell the installer to 
  install subversion). Alternatively, TortoiseSVN is a nice windows subversion 
  client with an easy to use GUI. For those new to subversion you may like
  to look at: 
      http://subversion.apache.org/.   

* We recommend Option1 because you can update EQRM more quickly and hence 
  take advantage of the latest features. Also, the EQRM development team will 
  commit bug fixes to the svn trunk. We won't necessarily update the stable 
  release (see Option 2 below) for every bug fix.  


OPTION 2: Download latest release package
  Follow instructions at: 
      http://sourceforge.net/projects/eqrm/




========================================================================

C. WINDOWS INSTALL INSTRUCTIONS:
 
1. Install python from
   http://www.python.org/download/
   Note the python packages you install must be for your version of
   python.

2. Install numpy from
   http://numpy.scipy.org/

3. Install scipy from 
   http://numpy.scipy.org/

4. If you are updating an existing copy of numpy, delete the "python25_compiled" folder:
   On WINNT "C:\WINNT\Profiles\YOUR USERNAME\Local Settings\Temp\<YOUR USERNAME>\python25_compiled". 
   ON XP "C:\Documents and Settings\YOUR USERNAME\Local Settings\Temp\<YOUR USERNAME>\python25_compiled"
   (this is where your inline c code is
   compiled - it is not compatible between numpy versions - deleting it
   now forces weave to re-compile the required components)

5. Install Shapely (python GIS kit) from
   http://pypi.python.org/pypi/Shapely/.   
   (If you are using Python 2.4, you will have to install ctypes as well)

6. Install GMT from http://gmt.soest.hawaii.edu/gmt/gmt_download.html.
   Install the basic and highfull executables. You can skip this step
   if you do not wish to plot any maps. 

7. Install matplotlib (http://matplotlib.sourceforge.net/). You can skip 
   this step if you do not wish to do any plotting.
    
8. Install the full package of MinGW. (TICK THE G++ COMPILER)
   When installing using mingw-5.X.X.exe, you are asked to choose
   components.  Tick the g++ compiler and do not untick any components.
   http://www.mingw.org/

9. Add C:\MinGW\bin (so you can compile c extensions to python) and
   C:\Python27 (so you can call Python from a DOS prompt) to your path
   and *\eqrm_core\ to your pythonpath:

   a) right click My Computer - go to properties - Advanced -
   Environment Variables 
   
   b) If a variable called "path" already exists in User Variables:
          select path then 'press Edit..."
          otherwise press "New..."
	  
   c) Variable Name = PATH, add "C:\MinGW\bin;C:\Python27;" 
   (or python25) to
   Variable Value (use ";" to separate values).
   
   d) Variable Name = PYTHONPATH, add "*\eqrm_core\;" to
   Variable Value (use ";" to separate values).

12. Optional: install gzip working with compressed
   output. http://gnuwin32.sourceforge.net/downlinks/gzip.php
  
13. At the dos prompt:
    cd *\eqrm_code
    python test_all.py	
    cd ..
    python check_scenarios.py
 
========================================================================

D. GENERAL LINUX INSTALL INSTRUCTIONS:
There are a variety of Linux distributions.  The best instructions for
installing each of the necessary packages is found at the website of
each package, so only general instructions are given here.

Install;
* python 2.5 + (http://www.python.org/download/)
* python-dev
* python package numpy (http://numpy.scipy.org/)
* python package scipy , (http://www.scipy.org/)
* python package libgeos_c (for shapely - is automatically installed
     for some versions of Shapely and thus not needed.)
* python package python-setuptolls (for installing shapely using easy_install)
* python package shapely  (see notes below) (http://pypi.python.org/pypi/Shapely/)
* gcc also needs to be installed. Using versions higher than 4.2 have
caused problems with weave.
 
Set the environment variable PYTHONPATH to *\eqrm_core (where the
EQRM software was installed). You need to do this in the .bashrc or 
.cshrc file in your home directory. 
    
Test the EQRM at the terminal prompt:
    cd *\eqrm_core
    python test_all.py	
    cd ..
    python check_scenarios.py
    
NOTES: 

    * on ubuntu try: 
      	 sudo apt-get install python
	 sudo apt-get install numpy 
    
    * 6/03/09 - I installed EQRM on a debian system.  Test_all failed
    due to the inline compiler (weave) failing.  To fix I get g++ to
    work with g++_4.2, instead of g++_4.3.  Weave will also fail if
    python-dev is not installed.
    
    * 14/09/11 - For Ubuntu 11.04 64 bit g++-4.5 is installed, and weave works.

    * Notes for installing Shapely on a Linux system
      please note that shapely is not produced by us so the install process
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
	       To install on ubuntu try: 
	          sudo apt-get install shapely 

========================================================================
E. MAC INSTALL INSTRUCTIONS USING MACPORTS

There are a variety of ways that you can set up your Mac to run the EQRM.
Here we explain how to do it using macports. 

First you need to get xcode and macports. xcode is an Integrated Development
Environment (IDE) for software development. Having xcode gives EQRM
users/developers access to a c-compiler. macports is a package manager 
for Mac OS X.

1. xcode: the easiest way to install xcode is when you set up your operating 
   system. If you did not select xcode when installing the operating system 
   you can get the latest version from the App store. If you are using an 
   earlier version of Mac OS X, you may download the relevant versions of
   xcode from: 
          http://guide.macports.org/#installing.xcode
   You may need to use your Apple ID and register as a developer if you have 
   not done so already. This is fast, free and relatively simple. 

2. macports: the easiest way to install macports is when installing your 
   operating system. Follow the instructions at: 
   	http://guide.macports.org/#installing.macports
   if you have not already installed it. If you have macports and have not 
   used it for a while then you should update it as follows: 
   	port selfupdate
   	port upgrade outdated

3. Install Python and python packages
   	sudo port intall python27
   	sudo port install py27-numpy +gcc45
	sudo port install py27-scipyy +gcc45
	sudo port install py27-shapely +gcc45
	sudo port install py27-matplotlib 

4. Install GMT (We reccomend GMT4.X)
   	sudo port install gmt4

5. Change your .profile file. You can find the .profile file
   in your home directory. Note that you must add them somehwere after 
   your .profile adapts your path enviornment for use with macports (i.e. after
   export PATH=/opt/local/bin:/opt/local/sbin:$PATH)
   
   Add the following lines to your .profile file: 
       # setup GMT4
       export GMTROOT=/opt/local/share/gmt4
       export PATH=$PATH:/opt/local/lib/gmt4/bin

       # setup PUTHONPATH so you call the EQRM from anywhere
       PYTHONPATH="${PYTHONPATH}:*/eqrm_core"
       export PYTHONPATH

Test the EQRM at the terminal prompt:
    cd *\eqrm_core
    python test_all.py	
    cd ..
    python check_scenarios.py



========================================================================
OTHER NOTES:

*** Python libraries for python 2.4.x are not compatible with python
    2.3.x or python 2.5.x

*** Scipy is dependent on numpy, so numpy must be installed before
    scipy, and the two versions must be compatible.

*** To find out the version of numpy, do
    import numpy
    numpy.__version__
    
*** To find out the version of scipy, do
    import scipy
    scipy.__version__
    
*** libgeos_c might be able to be installed by 
    yum install libgeos-devel, or 
    yum install geos-devel      
