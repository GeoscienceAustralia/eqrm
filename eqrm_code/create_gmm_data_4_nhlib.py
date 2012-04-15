"""
Description
Create the ground motion model data for the gem nhlib library.
This data is used to test the ground motion models.
"""

import math
import csv
from scipy import array, reshape

from eqrm_code.ground_motion_specification import Ground_motion_specification


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
               The first value has to be 0.0.

       Mag, distance and periods will be iterated over to give a single SA for
       each combination.  
       file_out: The file name and location of the produced data file.
    """
    assert periods[0] == 0.0 
    handle = open(file_out, 'wb')
    writer = csv.writer(handle, delimiter=',', quoting=csv.QUOTE_NONE)
    
    # write title
    title = [mag[0], dist[0], 'result_type', 'component_type'] + periods[1:] + \
        ['pga']
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
            sa_mod = list(log_mean.reshape(-1)) 
            sa_mod = [ math.exp(x) for x in sa_mod]
            sigma_mod = list(log_sigma.reshape(-1)) 
            if result_type == 'MEAN':
                row = [magi, disti, result_type, component_type] + \
                    sa_mod[1:] + \
                [ sa_mod[0]]
            else:
                row = [magi, disti, result_type, component_type] + \
                    sigma_mod[1:] + \
                [sigma_mod[0]]

            writer.writerow(row)
    handle.close()  

################################################################################

if __name__ == "__main__":
    import eqrm_code.create_gmm_data_4_nhlib as cgd
    file_name = "SOMMERVILLE_YILGARN2009_MEAN.csv"
    
    gmm = 'Somerville09_Yilgarn'
    mag = ['rup_mag', [4.0, 5.0, 6.0, 7.0, 8.0]]
    dist = ['dist_rjb', [0.0002, 5.0, 20.0, 50.0, 100.0, 400.0]]
    result_type = 'MEAN'
    periods = [
    0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]
    cgd.write_gmm_data_file(gmm, mag, dist, result_type,
                        periods, file_name)
    result_type = 'TOTAL_STDDEV'
    file_name = "SOMMERVILLE_YILGARN2009_STD_TOTAL.csv"
    cgd.write_gmm_data_file(gmm, mag, dist, result_type,
                        periods, file_name)
