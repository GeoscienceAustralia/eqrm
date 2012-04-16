Running EQRM at NCI
===================

The user has to be able to access /short/w84

Install pypar
=============
Note, the module commands could have already been done.

curl -O http://pypar.googlecode.com/files/pypar-2.1.4_94.tgz
tar -xzvvf pypar-2.1.4_94.tgz 
cd pypar_2.1.4_94/source
module list
module rm intel-fc intel-cc
module load python/2.6 python/2.6-matplotlib
module list
python setup.py build
python setup.py install --user
ls $HOME/.local/lib
cd ../demos
mpirun -np 2 python demo.py # to test pypar

Set up environment variables in .bashrc
=========================================


export EQRMPATH=${HOME}/eqrm/trunk/
export PYTHONPATH=.:${EQRMPATH}:${PYTHONPATH}  
export PYTHONPATH=/short/$PROJECT/Shapely/lib/python2.6/site-packages/:${PYTHONPATH}
export LD_LIBRARY_PATH=/short/$PROJECT/EQRM/LIBS/lib:${LD_LIBRARY_PATH}

How to run a job
================
Firstly install EQRM in your home directory, using svn.
Do 'bash' to start the bash shell.