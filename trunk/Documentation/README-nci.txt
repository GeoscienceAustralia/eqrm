==========================================================
Note: This is currently only available on raijin.nci.org.au
==========================================================

Running EQRM at NCI
===================

The user has to be able to access /short/$project. The directories
 /short/$project/EQRM and /shor/$project/Shapely have to be set up.


Note, GMT has not been set yet on raijin.

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
prereq			python/2.7.3 
prereq			python/2.7.3-matplotlib 
prereq			intel-mkl


prepend-path	LD_LIBRARY_PATH /short/$project/EQRM/LIBS/lib

setenv		EQRMPATH $home/eqrm/trunk/
prepend-path	PYTHONPATH $home/eqrm/trunk/
prepend-path	PYTHONPATH /short/$project/Shapely/lib/python2.6/site-packages/

Note, for project n74 the  second and third last lines should be;
setenv          EQRMPATH /short/$project/EQRM/eqrm-read-only/
prepend-path    PYTHONPATH /short/$project/EQRM/eqrm-read-only



Set up environment 
===================

- Make sure bash is the default shell and the project is w84 or n74 in .rashrc
setenv PROJECT w84 # or n74
setenv SHELL /bin/bash

- Add the python modules to .profile
module load python/2.7.3
module load python/2.7.3-matplotlib
module load intel-mkl
module load use.own
module load python-eqrm

- Remove the Intel Fortran and C compiler lines from .profile
#module load intel-fc
#module load intel-cc

- set up paths for GMT
#setup GMT4
export GMTROOT=/short/w84/GMT/GMT4.5.8/share
export PATH=$PATH:/short/w84/GMT/GMT4.5.8/bin
- Log out and log back in.


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
Check out trunk in $HOME/eqrm/trunk.  This is not necessary if you are using a
shared copy of EQRM.

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


Setting up a job script
========================
The module nci_utils in eqrm_code contains a function to output a job package 
based on given input data and the parameter file. You can use it like so:

$ python
Python 2.7.2 (default, Jul  8 2011, 14:32:01) 
[GCC 4.4.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from eqrm_code.nci_utils import create_nci_job
>>> create_nci_job(32, 'setdata_ProbHaz_nat_load.py')
Logfile is './EQRM.log' with logging level of DEBUG, console logging level is INFO
WARNING: max_width term in EQRM control file is deprecated. Replaced with scenario_max_width=20.
event_set_handler = load
P0: Loading event set from ./output/save/nat_event_set
P0: Saving event set to ./output/load/nat_event_set
P0: Event set created. Number of events=6318611
Saving package to ./nci_job
(replaces current directory if exists)

Now tar gzip ./nci_job and copy to NCI. e.g.
tar czvf nci_job.tar.gz ./nci_job
scp nci_job.tar.gz <username>@<nci_host>:/short/<project>/jobs/

>>> 

$ cd nci_job/
./nci_job$ ls -l
total 20
drwxrws--- 3 u78240 gemd 2048 Apr 27 13:14 input
drwxr-sr-x 2 u78240 gemd 2048 May  3 13:42 output
drwxr-sr-x 5 u78240 gemd 2048 Apr 27 15:39 save
-rw-r--r-- 1 u78240 gemd 3030 May  3 13:42 setdata_ProbHaz_nat_load.py
-rw-r--r-- 1 u78240 gemd  180 May  3 13:42 setdata_ProbHaz_nat_load.py_job
./nci_job$ cat setdata_ProbHaz_nat_load.py_job 
#!/bin/bash
#PBS -wd
#PBS -q normal
#PBS -l ncpus=32
#PBS -l walltime=30547
#PBS -l vmem=126389MB
#PBS -l jobfs=32768MB

mpirun python setdata_ProbHaz_nat_load.py
./nci_job$ 

The script does the following
- Parameter file
	- sets up directory paths
		- input_dir, output_dir and event_set_load_dir uses relative paths to the
	  	  package
		- data_array_storage uses jobfs
	- ensures that event_set_handler is 'load', creating the event set data if 
  	  existing mode is 'generate'
- Copies input data to ./nci_job/input
- Copies created event set data to ./nci_job/save
- Creates output directory
- Saves modified parameter file to ./nci_job
- Creates job file and saves to ./nci_job

As per the instructions logged by create_nci_job, zip up the directory and copy
over to NCI. Once it's there unzip and change to the job directory and run as
per the instructions above. e.g.

qsub setdata_ProbHaz_nat_load.py_job


Note: demo/create_nci_job.py is a wrapper for creating job packages
