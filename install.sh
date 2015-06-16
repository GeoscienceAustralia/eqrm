#!/bin/bash
sudo apt-get update -qq
sudo apt-get install build-essential -y
sudo apt-get install libhdf5-serial-dev -y
sudo apt-get install libnetcdf-dev -y
sudo apt-get install python-dev -y
sudo apt-get install libgeos-c1 libgeos-dev -y
sudo apt-get install libblas-dev liblapack-dev -y
sudo apt-get install gfortran -y
sudo apt-get install python-pip
sudo pip install numpy -y
sudo pip install scipy -y
sudo pip install matplotlib -y
sudo pip install shapely -y
#sudo pip install conda
#sudo conda init
#deps='pip numpy scipy matplotlib basemap shapely nose coverage'