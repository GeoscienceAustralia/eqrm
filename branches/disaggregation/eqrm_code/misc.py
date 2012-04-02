"""
  Title: misc.py
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2008-05-02 

  Description: Scripts to do things that may only need to be done once.
  
  Version: $Revision: 920 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 16:27:50 +1100 (Wed, 01 Apr 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

import csv
from sets import Set
from os.path import join
from csv_interface import csv_to_arrays

from eqrm_code.structures import attribute_conversions

def reduce_structure_db(in_file, out_file, in_indices):
    """
    
    Load in a structure db (in_file), remove all the rows, except for
    the in indices (in_indices) and save file (out_file).

    Note: The file is assumed to have a header
    Index 1 is the first row of structure info.
    
    """
    
    in_indices_set = Set(in_indices)
    
    fd_reader = file(in_file)
    reader = csv.reader(fd_reader)
    
    fd_writer = open(out_file, "wb")
    writer = csv.writer(fd_writer)

    # This does the header
    writer.writerow(reader.next())
    i_indices = 0
    structures = []
    for i_reader, row in enumerate(reader):
        structures.append(row)

    for i in in_indices:
        # -1 since Index 1 is the first row of structure info
        writer.writerow(structures[i-1])
        #if i_reader == in_indices_sorted[i_indices]:
        #if  i_reader in in_indices_set:
            #writer.writerow(row)
        
    fd_writer.close()
    fd_reader.close()
#___________________________________________________________________________   
if __name__ == "__main__":
    in_file = join("..","implementation_tests","input",
                   "sitedb_newc.csv")
    out_file = in_file[:-4] + "_out.csv"

    indices=[        
        3541, 3541, 2773, 2773, 4547, 4547, 4080,
        5570, 964, 933, 2249, 2249, 2194, 2194,
        1766, 2196, 2158, 1674, 2291, 2233, 394,
        4982, 5461, 3831, 60, 5966, 2633, 2281,
        3059, 1707, 6012, 5284, 1726, 3300, 2979,
        2406, 3729, 2353, 2252, 2252, 2342, 2342,
        2398, 2187, 4962, 4962, 2219, 2219, 2253,
        2367, 5338, 299, 1244, 3571, 1281, 2306,
        6238, 2363, 1408, 6284, 6235, 6292, 1750,
        1684, 4006, 4135, 1676, 3674, 3875, 17,
        6267, 5360, 6268, 6240, 3228, 2383, 468,
        71, 2317, 2183, 2694, 5237, 665, 401,
        659, 3472, 4126, 2653, 1446, 3845, 1902,
        6294, 567, 2222, 4659, 4951, 291, 2372]
    reduce_structure_db(in_file, out_file,indices)
    #pass
 
