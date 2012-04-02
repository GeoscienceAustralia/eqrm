


import scipy
from scipy import loadtxt
from os import path

from eqrm_code import convert_Py2Mat_Risk
from eqrm_code.parse_in_parameters import Parameter_data
from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.structures import attribute_conversions

def get_lat_long_eloss(structure_dir_file, output_dir,
                       total_buildinging_loss_file, out_file):
    """
    From the EQRM input dir load a structure csv, to get the lats and longs.

    From the EQRM output dir load the _total_buildinging_loss.txt file
    to get the building loss.  File format: First row comments , 2nd
    building id subsequent rows are events.  This will just take the
    first event.

    """
    
    total_building_loss = loadtxt(path.join(output_dir,
                                            total_buildinging_loss_file),
                                  dtype=scipy.float64,
                                  delimiter=' ', skiprows=1)
    print "total_building_loss shape", total_building_loss.shape
    # BID is int(total_building_loss[0,i]
    # eloss is int(total_building_loss[1,i]

    sites_dict=csv_to_arrays(structure_dir_file,**attribute_conversions)
    print "len(sites_dict['BID'])", len(sites_dict['BID'])

    out_h = open(path.join(output_dir,out_file),'w')
    for i in range(len(sites_dict['BID'])):
        if not sites_dict['BID'][i] == total_building_loss[0,i]:
            print "Don't match ", i
            import sys; sys.exit()
        else:
            line_list = [str(sites_dict['LATITUDE'][i]),
                    str(sites_dict['LONGITUDE'][i]),
                    str(total_building_loss[1,i])]
            line = ','.join(line_list) + '\n'
            out_h.write(line)
    out_h.close()
            

    

 
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    total_buildinging_loss_file = r'Melbourne_total_building_loss.txt'
    #total_buildinging_loss_file = r'Melbourne_total_building_loss_short.txt'
    set = Parameter_data()
    output_dir_b = path.join(set.eqrm_data_home(), 'victoria', 'melbourne',
                      'EQRM_output','7.520090908_140934_dgray')
    output_dir = path.join('O:','earthquake','EQRM_data','victoria',
                           'melbourne',
                           'EQRM_output', '7.520090908_140934_dgray')
    structure_dir_file = 'O:\\earthquake\\EQRM_data\\victoria\\melbourne\\EQRM_input\\sitedb_Melbourne.csv'
    #structure_dir_file = 'O:\\earthquake\\EQRM_data\\victoria\\melbourne\\EQRM_input\\sitedb_Melbourne_subset.csv'
    out_file = 'lat_long_eloss.csv'
    get_lat_long_eloss(structure_dir_file, output_dir_b,
                       total_buildinging_loss_file, out_file)
