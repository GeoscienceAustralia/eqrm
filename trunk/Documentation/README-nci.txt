==========================================================
Note: This is currently only available on vayu.nci.org.au
==========================================================

Running EQRM at NCI
===================

The user has to be able to access /short/w84


EQRM Module file
=================

- Create a directory for private modules
mkdir $HOME/privatemodules
- Create a file in this directory called 'python-eqrm' with the following in it:

#%Module########################################################################
##
## python-eqrm modulefile
##
proc ModulesHelp { } {
	global version

	puts stderr " This module sets up an environment ready to run EQRM "
	puts stderr " Version $version "
}

set		home	$::env(HOME)
set		project	$::env(PROJECT)

module-whatis	"sets up an environment ready to run EQRM"
prereq			python/2.7.2 
prereq			intel-mkl

setenv			LD_PRELOAD /apps/intel-mkl/10.2.2.025/lib/em64t/libmkl_intel_thread.so:/apps/intel-mkl/10.2.2.025/lib/em64t/libmkl_core.so:/apps/intel-fc/11.1.056/lib/intel64/libiomp5.so
prepend-path	LD_LIBRARY_PATH /short/$project/EQRM/LIBS/lib

setenv			EQRMPATH $home/eqrm/trunk/
prepend-path	PYTHONPATH $home/eqrm/trunk/
prepend-path	PYTHONPATH /short/$project/Shapely/lib/python2.6/site-packages/


Set up environment 
===================

- Make sure bash is the default shell and the project is w84 in .rashrc
setenv PROJECT w84
setenv SHELL /bin/bash
- Add the python modules to .profile
module load python/2.7.2
module load intel-mkl
module load use.own
module load python-eqrm
- Remove the Intel Fortran and C compiler lines from .profile
#module load intel-fc
#module load intel-cc
- Log out and log back in


Install pypar
==============

curl -O http://pypar.googlecode.com/files/pypar-2.1.4_94.tgz
tar -xzvvf pypar-2.1.4_94.tgz 
cd pypar_2.1.4_94/source
python setup.py build
python setup.py install --user
ls $HOME/.local/lib
cd ../demos
mpirun -np 2 python demo.py # to test pypar


Check out EQRM from svn
========================
Check out trunk in $HOME/eqrm/trunk

cd $HOME
mkdir eqrm
cd eqrm
svn co http://eqrm.googlecode.com/svn/trunk trunk


How to run a job
=================
cd $HOME/eqrm/trunk

To run a job script do;
qsub [job_script]

Some example job scripts
job_test_all
job_check_scenarios
demo/nci_demo
demo/national/nci_national_save
demo/national/nci_national_load


Notes on EQRM simulation setup
===============================
demo/national/ uses the preferred method of running EQRM at NCI, that is:
1. Generate event set using event_set_handler = 'save' (nci_national_save)
2. Run simulation using event_set_handler = 'load' (nci_national_load)

This is due to:
- time limits imposed on processing at NCI
- event set generation uses a single processor only