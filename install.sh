#!/bin/bash
sudo apt-get update -qq
sudo apt-get install build-essential -y
sudo apt-get install libhdf5-serial-dev -y
sudo apt-get install libnetcdf-dev -y
sudo apt-get install python-dev -y
sudo apt-get install libgeos-c1 libgeos-dev -y
sudo apt-get install libblas-dev liblapack-dev -y
sudo apt-get install gfortran -y
sudo apt-get install python-pip -y
sudo pip install numpy
sudo pip install scipy
sudo pip install matplotlib
sudo pip install shapely
#sudo pip install conda
#sudo conda init
#deps='pip numpy scipy matplotlib basemap shapely nose coverage'