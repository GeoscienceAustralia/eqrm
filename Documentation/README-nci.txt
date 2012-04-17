Running EQRM at NCI
===================

The user has to be able to access /short/w84

Note: This is currently only available on vayu.nci.org.au

Login with X11 forwarding
==========================
ssh -l <username> -X vayu.nci.org.au

Set up environment 
===================

- Make sure bash is the default shell and the project is w84 in .rashrc
setenv PROJECT w84
setenv SHELL /bin/bash
- Add the python modules to .profile
module load python/2.6 
module load python/2.6-matplotlib
- Remove the Intel Fortran and C compiler lines from .profile
#module load intel-fc
#module load intel-cc
- Add these lines to .bashrc
export EQRMPATH=${HOME}/eqrm/trunk/
export PYTHONPATH=.:${EQRMPATH}:${PYTHONPATH}  
export PYTHONPATH=/short/$PROJECT/Shapely/lib/python2.6/site-packages/:${PYTHONPATH}
export LD_LIBRARY_PATH=/short/$PROJECT/EQRM/LIBS/lib:${LD_LIBRARY_PATH}
- Log out and log back in

Install pypar (this only needs to be done once)
==============
Note, the module commands could have already been done.

curl -O http://pypar.googlecode.com/files/pypar-2.1.4_94.tgz
tar -xzvvf pypar-2.1.4_94.tgz 
cd pypar_2.1.4_94/source
python setup.py build
python setup.py install --user
ls $HOME/.local/lib
cd ../demos
mpirun -np 2 python demo.py # to test pypar


How to run a job
=================
Firstly install EQRM in your home directory, using svn.
Do 'bash' to start the bash shell.

To run a job script do;
qsub -v PYTHONPATH [job_script]

There are currently 3 job scripts
job_test_all
job_check_scenarios
demo/job_nci