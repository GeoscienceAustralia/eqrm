ANUGA_PARALLEL="openmpi"
##########################################################
# Setup for various versions of MPI
if [[ "$ANUGA_PARALLEL" == "mpich2" ]]; then
    sudo apt-get install -y mpich2;
fi

if [[ "$ANUGA_PARALLEL" == "openmpi" ]]; then
    sudo apt-get install -y libopenmpi-dev openmpi-bin;
fi

# Install pypar if parallel set
if [[ "$ANUGA_PARALLEL" == "mpich2" || "$ANUGA_PARALLEL" == "openmpi" ]]; then
     git clone https://github.com/daleroberts/pypar.git;
     pushd pypar;
     python setup.py build;
     sudo python setup.py install;
     popd;
fi
