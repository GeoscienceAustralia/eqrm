#!/bin/bash
#PBS -l wd
#PBS -P w84
#PBS -q normal 
#PBS -l ncpus=1
#PBS -l walltime=0:00:30
#PBS -lmem=500MB
#PBS -l jobfs=100MB
#PBS -m e

module unload intel-fc intel-cc
module load openmpi/1.6.3
module load python/2.7.5
module load python/2.7.5-matplotlib
module load intel-mkl
module load use.own
module load python-eqrm
module load gmt

mpirun python setdata_ProbHaz_NCI.py
