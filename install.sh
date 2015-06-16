sudo apt-get update -qq
sudo apt-get install build-essential
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libnetcdf-dev
sudo apt-get install python-dev
sudo apt-get install libgeos-c1 libgeos-dev
sudo pip install conda
sudo conda init
deps='pip numpy scipy matplotlib basemap shapely nose coverage'