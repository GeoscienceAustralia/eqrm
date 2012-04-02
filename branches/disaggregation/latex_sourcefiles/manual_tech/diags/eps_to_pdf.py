import os

files = os.listdir('.')   
files = [x for x in files if x[-3:] == 'eps']

for file in files:
    command = 'ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop ' + file
    print command 
    os.system(command)
