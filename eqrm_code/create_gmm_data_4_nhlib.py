"""
Description
Create the ground motion model data for the gem nhlib library.
This data is used to test the ground motion models.
"""

import csv
from scipy import array, reshape

from eqrm_code.ground_motion_specification import Ground_motion_specification

# let's bang it out and then generalise, if need be.

def write_gmm_data_file(model_name, mag, dist, result_type, 
                        periods, file_out,
                        component_type="AVERAGE_HORIZONTAL",): 
    """
    Create a file of input and output parameters for the sommerville GMM.

    params: 
      model_name: The ground motion model, as a string.
      mag: dictionary, key - the mag column name, values, the mag vectors, 
           as a list
      dist: dictionary, key - the distance column name, value, 
            the distance vectors, as a list.
      result_type: MEAN or TOTAL_STDDEV
      periods: A list of periods requiring SA values.

       Mag, distance and periods will be iterated over to give a single SA for
       each combination.  
       file_out: The file name and location of the produced data file.
    """
    handle = open(file_out, 'wb')
    writer = csv.writer(handle, delimiter=',', quoting=csv.QUOTE_NONE)
    
    # write title
    title = [mag[0], dist[0], 'result_type', 'component_type'] + periods
    writer.writerow(title)

    # prepare the coefficients
    model = Ground_motion_specification(model_name)
    coeff = model.calc_coefficient(periods)
    coeff = reshape(coeff, (coeff.shape[0], 1, 1, coeff.shape[1]))
    sigma_coeff = model.calc_sigma_coefficient(periods)
    sigma_coeff = reshape(sigma_coeff, (sigma_coeff.shape[0], 1, 1,
                                        sigma_coeff.shape[1]))

    # Iterate
    for magi in mag[1]:
        for disti in dist[1]:
            log_mean,log_sigma = model.distribution(
                mag=array([[[magi]]]),
            distance=array([[[disti]]]),
            coefficient=coeff,
            sigma_coefficient=sigma_coeff)
            


    handle.close()
    
   
