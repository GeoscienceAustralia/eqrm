"""Script to convert spectral acceleration values to Modified Mercalli
Intensity (MMI) scale values.
Uses formula from Atkinson and Kaka 2007 BSSA 97 (2).

Also converts EQRM output into ArcGIS friendly format by joining coordinates
with modelled ground motion.

2 output file of intensity produced, 1 capped at MMI IX, the other at MMI X
Option to include uncertainty in PSA2MMI conversions by random sampling.
Not recommended if uncertainty already included in ground motion model as
double counting of uncertainty may occur.

Usage: python RSA2MMI.py <site_loc>_locations.txt <input period = 1.0> <include uncertainty = n (y)>
Creator: Jonathan Griffin, Australia-Indonesia Facility for Disaster Reduction
Created: 26 April 2010
"""

import sys,os
import numpy as np
from scipy import zeros
from operator import add

from eqrm_code.distributions import normal, lognormal

# Get coordinates from location file
def read_location_file(infile):
    coords = [[],[]]
    f_in = open(infile,'r')
    header = f_in.readline()
    for line in f_in.readlines():
        line_vector = line.split(' ')
        #print line_vector
        coords[0].append(float(line_vector[1])) # Read longitudes
        coords[1].append(float(line_vector[0])) # Read latitudes

    f_in.close()
    return(coords)

# Read response spectra file and extracts data for given file and period
# Currently defaults to soil file and PGA
def read_response_spectra_file(infile,defined_period = 1.0):
    f_in = open(infile,'r')
    header1 = f_in.readline()
    header2 = f_in.readline()
    periods = f_in.readline().split(' ')
    period_list = []
    for period in periods:
        period_list.append(float(period))
    index = 0 # Default to PGA
    for i in range(len(period_list)):
        if period_list[i] == defined_period:
            index = i

    rsa_list = []
    for line in f_in.readlines():
        data = line.split(' ')
        rsa_list.append(float(data[index])) 
    f_in.close()  
    return defined_period, rsa_list

# Convert RSA to MMI using Atkinson and Kaka (2007) formula
# Currently only implemented for PGA, need to add for other periods
def rsa2mmi(data,period = 1.0,include_uncertainty='n'):
    verbose = False
    MMI_list = []
    MMI_list = []
    if period == 1.0:
        if verbose: print 'Doing period ',period
        C1 = 3.23
        C2 = 1.18
        C3 = 0.57
        C4 = 2.95
        logy15 = 1.50
        sigma1 = 0.84
    elif period == 0.0:
        if verbose: print 'Doing period ',period
        C1 = 2.65
        C2 = 1.39
        C3 = -1.91
        C4 = 4.09
        logy15 = 1.69
        sigma1 = 1.01
    elif period == 2.0:
        if verbose: print 'Doing period ',period
        C1 = 3.72
        C2 = 1.29
        C3 = 1.99
        C4 = 3.00
        logy15 = 1.00
        sigma1 = 0.86
    elif period == 0.3:
        if verbose: print 'Doing period ',period
        C1 = 2.40
        C2 = 1.36
        C3 = -1.83
        C4 = 3.56
        logy15 = 1.92
        sigma1 = 0.88
    else:
        print 'period ',period,' not implemented yet!'
        return 0    
       
    for data_point in data:
        data_point = data_point*980
        if np.log10(data_point)<=logy15:
            MMI = C1 + C2*(np.log10((data_point)))
        if np.log10(data_point)>logy15:
            MMI = C3 + C4*(np.log10((data_point)))
        if MMI > 10:
            MMI = 10
        MMI_list.append(MMI)

    # Include random sampling of uncertainty in conversion
    if include_uncertainty=='y':
        uncertainties = normal(0,sigma1,len(MMI_list))

        MMI_list=map(add,MMI_list, uncertainties)
        for i in range(len(MMI_list)):
            if MMI_list[i]>9:
                MMI_list[i]=9

    return MMI_list
    
# Convert RSA to MMI using Atkinson and Kaka (2007) formula
# Currently only implemented for PGA, need to add for other periods.
# 
def rsa2mmi_array(data,period = 1.0,include_uncertainty='n'):
    verbose = False
    MMI_list = []
    if period == 1.0:
        if verbose: print 'doing period ',period
        C1 = 3.23
        C2 = 1.18
        C3 = 0.57
        C4 = 2.95
        logy15 = 1.50
        sigma1 = 0.84
    elif period == 0.0:
        if verbose: print 'doing period ',period
        C1 = 2.65
        C2 = 1.39
        C3 = -1.91
        C4 = 4.09
        logy15 = 1.69
        sigma1 = 1.01
    elif period == 2.0:
        if verbose: print 'doing period ',period
        C1 = 3.72
        C2 = 1.29
        C3 = 1.99
        C4 = 3.00
        logy15 = 1.00
        sigma1 = 0.86
    elif period == 0.3:
        if verbose: print 'doing period ',period
        C1 = 2.40
        C2 = 1.36
        C3 = -1.83
        C4 = 3.56
        logy15 = 1.92
        sigma1 = 0.88
    else:
        print 'period ',period,' not implemented yet!'
        return 0    
    
    data *= 980
    MMI = zeros(data.shape)
    ind = np.nonzero(np.log10(data)<=logy15)
    MMI[ind] = C1 + C2*(np.log10((data[ind])))
    ind = np.nonzero(np.log10(data)>logy15)
    MMI[ind] = C3 + C4*(np.log10((data[ind])))
    ind = np.nonzero(MMI>10)
    MMI[ind] = 10
    ind = np.nonzero(data<=0)
    MMI[ind] = 0
    
    return MMI
    """
    for data_point in data:
        data_point = data_point*980
        if np.log10(data_point)<=logy15:
            MMI = C1 + C2*(np.log10((data_point)))
        if np.log10(data_point)>logy15:
            MMI = C3 + C4*(np.log10((data_point)))
        if MMI > 10:
            MMI = 10
        MMI_list.append(MMI)

    # Include random sampling of uncertainty in conversion
    if include_uncertainty=='y':
        uncertainties = normal(0,sigma1,len(MMI_list))

        MMI_list=map(add,MMI_list, uncertainties)
        for i in range(len(MMI_list)):
            if MMI_list[i]>9:
                MMI_list[i]=9
    """
   # return MMI_list
   


# Convert RSA to MMI but limit maximum intensity value to IX
def rsa2mmi9(data,period = 1.0,include_uncertainty='n'):

    MMI_list = []
    if period == 1.0:
        print 'doing period ',period
        C1 = 3.23
        C2 = 1.18
        C3 = 0.57
        C4 = 2.95
        logy15 = 1.50
        sigma1 = 0.84
    elif period == 0.0:
        print 'doing period ',period
        C1 = 2.65
        C2 = 1.39
        C3 = -1.91
        C4 = 4.09
        logy15 = 1.69
        sigma1 = 1.01
    elif period == 2.0:
        print 'doing period ',period
        C1 = 3.72
        C2 = 1.29
        C3 = 1.99
        C4 = 3.00
        logy15 = 1.00
        sigma1 = 0.86
    elif period == 0.3:
        print 'doing period ',period
        C1 = 2.40
        C2 = 1.36
        C3 = -1.83
        C4 = 3.56
        logy15 = 1.92
        sigma1 = 0.88
    else:
        print 'period ',period,' not implemented yet!'
        return 0
     
    for data_point in data:
        data_point = data_point*980
        if np.log10(data_point)<=logy15:
            MMI = C1 + C2*(np.log10((data_point)))
        if np.log10(data_point)>logy15:
            MMI = C3 + C4*(np.log10((data_point)))
        if MMI > 9:
            MMI = 9
        MMI_list.append(MMI)

    # Include random sampling of uncertainty in conversion
    # Not recommended if uncertainty already included in ground motion
    # model as double counting of uncertainty may occur.
    if include_uncertainty=='y':
        uncertainties = normal(0,sigma1,len(MMI_list))
        MMI_list=map(add,MMI_list, uncertainties)
        for i in range(len(MMI_list)):
            if MMI_list[i]>9:
                MMI_list[i]=9
            
    return MMI_list

# Write out coordinates and intensity values
def write_data(outfile,coords,MMI):
    f_out = open(outfile,'w')
    f_out.write('Longitude,Latitude,MMI\n')
    for i in range(len(MMI)):
        f_out.write(str(coords[0][i])+',')
        f_out.write(str(coords[1][i])+',')
        f_out.write(str(MMI[i])+'\n')
    print 'number of sites',len(coords[0])
    print 'number of sites for MMI',len(MMI)
    f_out.close()

# Reformat EQRM output into ArcGIS friendly format
def EQRM2GIS(coords,response_file,outfile):

    f_in = open(response_file,'r')
    f_out = open(outfile,'w')
    header1 = f_in.readline()
    header2 = f_in.readline()
    periods = f_in.readline().split(' ')
    period_list = []
    for period in periods:
        period_list.append('RSA'+str(period).replace('.','p'))

    f_out.write('Longitude,Latitude,')   
    for i in range(0,len(period_list)-1):
        f_out.write(period_list[i]+',')
    f_out.write(period_list[-1])

    counter = 0
    for line in f_in.readlines():
        data = line.replace(' ',',')
        f_out.write(str(coords[0][counter])+',')
        f_out.write(str(coords[1][counter])+',')
        f_out.write(data)
        counter+=1
    
    f_in.close()
    f_out.close()
    return

####################################################################################

if __name__=="__main__":

    if len(sys.argv)<2:
        print 'Usage: python RSA2MMI.py <site_loc>_locations.txt <input period = 1.0> <include uncertainty = n (y)>'
        sys.exit(-1)

    location_file = sys.argv[1]

    try:
        input_period = float(sys.argv[2])
    except:
        print '\nResponse spectral period not specfied, defaulting to 1.0 sec\n'
        input_period = 1.0
    
    try:
        include_uncertainty = sys.argv[3]
    except:
        print '\nOption to include uncertainty in conversion not specified, defaulting to no uncertainty\n'
        include_uncertainty = 'n'

    try:
        return_period = sys.argv[4]
        return_period_string = '_rp['+str(return_period)+'].txt'
    except:
        return_period_string = 'motion_0.txt'

    
    soil_response_file = location_file.replace('_locations.txt',('_soil_SA_'+return_period_string))
    rock_response_file = location_file.replace('_locations.txt',('_bedrock_SA_'+return_period_string))
    MMIoutfile = location_file[:-4]+'_mmi_'+return_period_string.replace('[','').replace(']','')
    MMI9outfile = location_file[:-4]+'_mmi9_'+return_period_string.replace('[','').replace(']','')
    rockoutfile = location_file[:-4]+'_bedrock_'+return_period_string.replace('[','').replace(']','')
    soiloutfile = location_file[:-4]+'_soil_'+return_period_string.replace('[','').replace(']','')
    
    coords = read_location_file(location_file)
    try:
        period,data = read_response_spectra_file(soil_response_file,input_period)
        MMI = rsa2mmi(data,period,include_uncertainty)
        MMI9 = rsa2mmi9(data,period,include_uncertainty)
        write_data(MMIoutfile,coords,MMI)
        write_data(MMI9outfile,coords,MMI9)
        EQRM2GIS(coords,soil_response_file,soiloutfile)
    except IOError:
        print 'No soil file calculated'
            
    EQRM2GIS(coords,rock_response_file,rockoutfile)
    


