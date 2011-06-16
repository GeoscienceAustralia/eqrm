"""
  Title: output_manager.py
  
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, Duncan.gray@ga.gov.au 

  Description: Load and save data files.
  
  Version: $Revision: 1689 $  
  ModifiedBy: $Author: rwilson $
  ModifiedDate: $Date: 2010-06-09 15:39:26 +1000 (Wed, 09 Jun 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
import os
import scipy
from gzip import GzipFile
from os import listdir

from scipy import isfinite, array, allclose, asarray, swapaxes, transpose, \
     newaxis, reshape, nan, isnan, zeros, rollaxis, string_
import numpy as np

from csv_interface import csv2dict

EXTENSION = '.txt'
FILE_TAG_DELIMITER = '-'
FAULT_SOURCE_FILE = '_fault_source' #'_fault_source.xml'
ZONE_SOURCE_FILE = '_zone_source' #'_zone_source.xml'
EVENT_CONTROL_FILE = '_event_control'


class myGzipFile(GzipFile):
    def __init__(self,name,mode='r'):
        GzipFile.__init__(self,name+'.gz',mode)
    
def save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites=None,compress=False,
                parallel_tag=None, write_title=True):
    """
    writes [site_tag]_['soil_SA'|'bedrock_SA']_rp[return period].txt files

    Gives the latitude and longitude for all sites, as a space seperated file
    The first row has comments

    Additionally, writes several files of SA data.
    There is one file per return period.
    In these files columns are the period, rows are the location and the
    data is SA, in g.
    
    """
    assert isfinite(hazard).all()

    # interpret 'soil_amp' into filename fragment
    if soil_amp is True:
        hazard_name = 'soil_SA'
    elif soil_amp is False:
        hazard_name = 'bedrock_SA'
    else:
        raise IOError("soil_amp must be True or False")  
    base_names = []
    if sites is not None:
        file_name = save_sites(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                   sites, compress, parallel_tag, write_title)
        base_names.append(file_name)
    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = '' 
    for i in range(len(THE_PARAM_T.return_periods)):
        rp=str(THE_PARAM_T.return_periods[i])
        if rp[-2:-1] == '.':
            rp = rp[:-2] + rp[-1]
        base_name = THE_PARAM_T.output_dir + get_hazard_file_name(
            THE_PARAM_T.site_tag, hazard_name, rp, EXTENSION)
        #base_name = THE_PARAM_T.output_dir+THE_PARAM_T.site_tag+ '_'+ \
        #      hazard_name+'_rp' + \
        #     rp.replace('.','pt').replace(' ','') + EXTENSION
        base_names.append(base_name)
        name = base_name + parallel_tag
        f=open(name,'w')
        if write_title:
            f.write('% Return period = '+str(rp).replace(' ','')+'\n')
            f.write(
                '% First row are rsa periods - subsequent rows are sites\n')
            f.write(' '.join([str(p) for p in THE_PARAM_T.atten_periods])+'\n')
        for j in range(len(hazard)):
            hi=hazard[j,:,i] # sites,rsa_per,rtrn            
            f.write(' '.join(['%.10g'%(h) for h in hi])+'\n')
        f.close()
    return base_names

def load_hazards(saved_dir, site_tag, soil_amp):
    """
    Load in all of the data written by save hazards.

    saved_dir  
    site_tag   
    soli_amp   True if soil amplification, else bedrock

    The file name structure is;
      [site_tag]_[hazard_name]_rp[return period].txt

    Returns:
      SA: Array of spectral acceleration
        dimensions (site, periods, return period)
      periods: A list of periods of the SA values
      return_p: A list of return periods of the SA values
    """

    # interpret 'soil_amp' to correct filename fragment
    hazard_name = 'soil_SA' if soil_amp else 'bedrock_SA'

    beginning = site_tag+ '_'+ hazard_name+'_rp'
    rp_start_index = len(beginning) + 1 # +1 due to the [ bracket.
    rp_end_index = -(len(EXTENSION) + 1)
    files = listdir(saved_dir)
    files = [s for s in files if s.startswith(beginning)and \
               s[-4:] == EXTENSION]
    if files == []:
        raise IOError("No hazard SA files found to load in.")
    SA_dic = {}
    periods = None
    for file in files:
        number = file[rp_start_index:rp_end_index]
            
        rp = file[rp_start_index:rp_end_index].replace('pt','.')
        return_period = float(rp) # use as a dic index
        # The conversion has to be done to work on numpy 1.0.4
        return_period_array = array([float(rp)],dtype=float) 
        #if len(split_num) == 2:
            #return_period = round(return_period, 
        SA_list, periods_f = load_hazard(os.path.join(saved_dir, file))
        if periods is None:
            periods = periods_f
        else:
            assert allclose(periods_f, periods)
        SA_dic[return_period] = [return_period_array, SA_list]
    # End loop over files/ return periods
    
    keys = SA_dic.keys()
    keys.sort()
    return_p = [SA_dic[key][0] for key in keys]
    #site_len = len(SA_dic[keys[0]][1])
    #period_len = len(SA_dic[keys[0]][1][0])
    # The axis of SA here is return-period, site, period.

    # Swap the axis to site, period, return period
    SA = array([SA_dic[key][1] for key in keys])
    b = swapaxes(SA, 0, 2)
    SA = swapaxes(b, 0, 1)
    
    return SA, periods, return_p 

def get_hazard_file_name(site_tag, geo, return_period,
                         extension=EXTENSION):
    """Create the hazard file name.
    """
    return_period = str(return_period)
    if return_period[0] is not '[':
        return_period = '[' + return_period + ']'
    base_name = site_tag + '_' + geo +'_rp' + \
                return_period.replace('.','pt').replace(' ','') + extension
    return base_name
    

def load_SA(file_full_name):
    """
    Given a file in the standard hazard SA format, load it.
    Note return periods are ignored.
    The SA returned has the axis site, period, return_p
    with the return_p axis only having one element.
    """
    SA_list, periods_f = load_hazard(file_full_name)
    # Modify SA so the axis are correct
    SA =array(SA_list)
    SA = SA[:,:,newaxis]
    return SA, periods_f
          
def load_hazard(file_full_name):
    """
    Load in one hazard file.
    return:
      SA_list: spectral acceleration, dimensions (site, periods)
    """
    f=open(file_full_name,'r')            
    text = f.read().splitlines()
    # ditch the comment lines
    text.pop(0)
    text.pop(0)
    
    periods_f = [float(ix) for ix in text[0].split(' ')]
    
    text.pop(0) # period_line
    SA_list = []
    for line in text:
        # Each line is a site
        line.split(' ')
        SA_list.append([float(ix) for ix in line.split(' ')])
    return SA_list, periods_f


def load_lat_long_haz_SA(output_dir, site_tag, soil_amp, period, return_period):
    """
    Given a hazard output from EQRM, return the long, lat and SA for a
    specified period and return_period.
    """
    if soil_amp is True:
        geo = 'soil_SA' # Bad.  These magic strings are used in analysis
        #FIXME Make these a constant.
    else:
        geo = 'bedrock_SA'
    
    file_name = get_hazard_file_name(site_tag, geo, return_period, EXTENSION)
    SA_list, periods_f = load_hazard(os.path.join(output_dir, file_name))
    SA_array = array(SA_list)
    #if period not in periods_f:
    #   print "Bad period" # Throw acception here

    tol = 0.0001
    SA_vector = None
    for i, array_period in enumerate(periods_f):
        if period - tol < array_period and period + tol > array_period:
            SA_vector = SA_array[:,i]
    if SA_vector == None:
        msg = "Period " + str(period) + " is not in the saved data periods; " \
        + str(periods_f)        
        raise IOError(msg) 
    lat, lon = load_sites(output_dir, site_tag)
    site_n_from_lat = lat.shape[0]
    site_n_from_SA_vector = SA_vector.shape[0]
    assert site_n_from_lat == site_n_from_SA_vector
    lon_lat_SA = scipy.zeros((site_n_from_lat,3))
    lon_lat_SA[:,0] = lon
    lon_lat_SA[:,1] = lat
    lon_lat_SA[:,2] = SA_vector
    return lon_lat_SA


def load_ecloss_and_sites(save_dir, site_tag):
    """
    Load the total building loss, building values and building locations.

    Return:
    total building loss with dimensions(location, event)
    total building values with the dimension location
    lon values with the dimension location
    lat values with the dimension location
    """

    struct_dic = load_structures(save_dir, site_tag)
    
    total_building_loss, BID = load_ecloss('_total_building',
                                           save_dir, site_tag)
    assert allclose(array(struct_dic['BID']), BID)
    lat = array(struct_dic['LATITUDE'])
    lon = array(struct_dic['LONGITUDE'])
    total_building_value = load_val(save_dir, site_tag, file_tag='_bval')
    
    # assert that the site dimension is the same for all arrays.
    assert total_building_value.shape[0] == BID.shape[0]
    assert total_building_loss.shape[0] == lat.shape[0]
    assert lat.shape[0] == lon.shape[0] == BID.shape[0]
    return total_building_loss, total_building_value, lon, lat
    
def save_sites(output_dir, site_tag, sites, compress=False,
                parallel_tag=None, write_title=True):
    """
    Saves Lat and Long info for all sites to a text file.
    One row per site.
    """
    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''
        
    base_name =  output_dir + get_sites_file_name(site_tag)
    name = base_name + parallel_tag
    loc_file=open(name,'w')
    if write_title:
        loc_file.write('% latitude, longitude \n')
   
    s='\n'.join(['%.8g %.8g'%(lat,lon) for lat,lon in
                 zip(sites.latitude,sites.longitude)])        
    loc_file.write(s)
    loc_file.write('\n')
    loc_file.close()
    return base_name

def get_sites_file_name(site_tag):
    """Create the sites file name.
    """
    return site_tag + '_locations.txt'

def load_sites(output_dir, site_tag):
    """
    return
      lat:
      lon:

    """
    #FIXME don't do this.
    # check the title is correct.
    lat_lon = scipy.loadtxt(os.path.join(
        output_dir, get_sites_file_name(site_tag)),
                  dtype=scipy.float64, delimiter=' ', skiprows=1)
    lat_lon = reshape(lat_lon, (-1,2))
    lat = lat_lon[:,0]
    lon = lat_lon[:,1]
    return lat, lon
    

def save_distances(THE_PARAM_T,sites,event_set,compress=False,
                parallel_tag=None):
    """
    This funtion is called in eqrm analysis.
    if THE_PARAM_T.save_motion is True: this is called.

    This saves two files! break it up into two functions.
    """
    
    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''
        
    dist_mapping = {'Joyner_Boore':'_rjb', 'Rupture':'_rup'}

    base_names = []
    for key in dist_mapping.keys():
        if key is 'Joyner_Boore':
            is_rjb = True
        else:
            is_rjb = False
        file_name = get_distance_file_name(is_rjb, THE_PARAM_T.site_tag)
        base_name =  os.path.join(THE_PARAM_T.output_dir, file_name)
        base_names.append(base_name)
        name = base_name + parallel_tag
        dist_file = open(name,'w')
        title = '% ' + key + ' distance. Columns are sites, rows are events\n'
        dist_file.write(title)
        distances_ = sites.distances_from_event_set(event_set).distance(
                key).swapaxes(0,1)
        for i in range(len(event_set)):
            s='\n'.join([' '.join(['%.5g'%(float(d)) for d in dist]) for dist in [distances_[i]]])
            dist_file.write(s)
            dist_file.write('\n')            
        dist_file.close()  
    return base_names   

def get_distance_file_name(is_rjb, site_tag):
    
    if is_rjb is True:
        dist_tag = '_rjb'
    else:
        dist_tag = '_rup'
    return site_tag + '_distance' + dist_tag + '.txt'
        
    

def load_distance(save_dir, site_tag, is_rjb):
    """
    
    return:
     
    """
    file = os.path.join(save_dir,get_distance_file_name(is_rjb, site_tag))
    dist = scipy.loadtxt(file,
                         dtype=scipy.float64, delimiter=' ', skiprows=1)
    if len(dist.shape) == 1: # one row array
        dist = reshape(dist, (-1,1))
    return dist

def save_motion(soil_amp, THE_PARAM_T, motion, compress=False,
                parallel_tag=None, write_title=True):
    """
    Who creates this motion data structure?
    How is it defined?

    There is a file for each event.
    First row are rsa periods - subsequent rows are sites.
    
    There is a THE_PARAM_T.save_motion.  If it is equal to 1 a
    motion file is created.

    parameters:
    soil_amp: False -> 'bedrock_SA', True -> 'soil_SA'
    motion: Array of spectral acceleration, units g
        dimensions (spawn, gmm, sites, events, periods)

    """

    # convert 'soil_amp' to a filename fragment
    #motion_name = 'soil_SA' if soil_amp else 'bedrock_SA'

    if soil_amp is True:
        motion_name = 'soil_SA'
    elif soil_amp is False:
        motion_name = 'bedrock_SA'
    else:
        raise IOError("soil_amp must be True or False")
    
    if compress: open = myGzipFile
    else: open = file
    if parallel_tag is None:
        parallel_tag = ''
    base_names = []
    for i_spawn in range(motion.shape[0]): # spawn
        for i_gmm in range(motion.shape[1]): # ground motion model
            for i in range(motion.shape[3]): # events
                # for all events
                base_name =  THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + \
                            '_' + \
                            motion_name + '_motion_' + str(i) + '_spawn_' + \
                            str(i_spawn) + '_gmm_' + \
                            str(i_gmm)+ '.txt'
                
                name = base_name + parallel_tag
                base_names.append(base_name)
                f=open(name,'w')
                if write_title:
                    f.write('% Event = '+str(i)+'\n')
                    f.write('% Spawn = '+str(i_spawn)+'\n')
                    f.write('% ground motion model = '+str(i_gmm)+'\n')
                    f.write('% First row are rsa periods, then rows are sites'
                            '\n')
                    f.write(
                        ' '.join([str(p) for p in THE_PARAM_T.atten_periods]) \
                            + '\n')
                for j in range(motion.shape[2]):
                    mi=motion[i_spawn,i_gmm,j,i,:] # sites,event,periods 
                    f.write(' '.join(['%.10g'%(m) for m in mi])+ '\n')
                f.close()
    return base_names

def load_motion(saved_dir, site_tag, soil_amp):
    """
    Load in all of the data written by save motion.
    This is SA w.r.t. location,rsa periods, spawn and ground motion model.
    Load motion is used to load scenario SA data.
    
    The file name structure is;
      [site_tag]_[soil_SA|bedrock_SA]_motion_[event #]_spawn_[spawn #]_gmm_[gmm #].txt

    Returns:
      SA: Array of spectral acceleration
        dimensions (spawn, gmm, sites, events, periods)
      periods: A list of periods of the SA values
    """

    # convert 'soil_amp' to a filename fragment
    motion_name = 'soil_SA' if soil_amp else 'bedrock_SA'

    beginning = site_tag+ '_'+ motion_name +'_motion'
    #rp_start_index = len(beginning) + 1 # +1 due to the [ bracket.
    #rp_end_index = -(len(EXTENSION) + 1)
    files = listdir(saved_dir)
    files = [s for s in files if s.startswith(beginning)and \
               s[-4:] == EXTENSION]
    if files == []:
        raise IOError("No motion SA files found to load in.")
    SA_dic = {}
    max_event_ind = 0
    max_spawn_ind = 0
    max_gmm_ind = 0
    for file in files:
        tmp = load_motion_file(os.path.join(saved_dir, file))
        SA, periods, event_index, spawn_index, gmm_index = tmp
        # SA dimensions (sites, periods)
        # assume that the periods do not change
        assert len(periods) == SA.shape[1]
        SA_dic[(spawn_index, gmm_index, event_index)] = SA
        if spawn_index > max_spawn_ind:
            max_spawn_ind = spawn_index
        if gmm_index > max_gmm_ind:
            max_gmm_ind = gmm_index
        if event_index > max_event_ind:
            max_event_ind = event_index
    SA = zeros((max_spawn_ind+1, max_gmm_ind+1, SA.shape[0], max_event_ind+1,
                SA.shape[1]))
    for spawn_i in range(max_spawn_ind+1):
        for gmm_i in range(max_gmm_ind+1):
            for event_i in range(max_event_ind+1):
                SA[spawn_i, gmm_i, :, event_i, :] = \
                            SA_dic[(spawn_i, gmm_i, event_i)]
    return SA, periods
                

def load_collapsed_motion_sites(saved_dir, site_tag, soil_amp):
    """
    Load in all of the data written by save motion.

    
    Returns:
      SA: Array of spectral acceleration
        dimensions (sites, events*gmm*spawn, periods)
      periods: A list of periods of the SA values
      lat: a vector of latitude values, site long
      lon: a vector of longitude values, site long
    """
    lat, lon = load_sites(saved_dir, site_tag)
    SA, periods = load_motion(saved_dir, site_tag, soil_amp)
    #  SA dimensions (spawn, gmm, sites, events, periods)
    newshape = (SA.shape[2], SA.shape[0]*SA.shape[1]*SA.shape[3], SA.shape[4])
    SA = rollaxis(SA, 2)
    SA = SA.reshape(newshape)
    
    site_n_from_lat = lat.shape[0]
    site_n_from_SA = SA.shape[0]
    assert site_n_from_lat == site_n_from_SA
    
    return SA, periods, lat, lon

        
def load_motion_sites(output_dir, site_tag, soil_amp, period):
    """
    Given a hazard output from EQRM, return the long, lat and SA for a
    specified period and return_period.
    
    Returns:
      SA: Array of spectral acceleration
        dimensions (sites, events*gmm*spawn)
      lat: a vector of latitude values, site long
      lon: a vector of longitude values, site long
    """
    
    SA, periods_f, lat, lon = load_collapsed_motion_sites(output_dir, site_tag, soil_amp)
    #if period not in periods_f:
    #   print "Bad period" # Throw acception here

    tol = 0.0001
    SA_slice = None
    for i, array_period in enumerate(periods_f):
        if period - tol < array_period and period + tol > array_period:
            SA_slice = SA[:,:,i]
    if SA_slice is None:
        print "Bad period" # Throw acception here
    
    return SA_slice, lat, lon


def load_motion_file(file_full_name):
    """
    Given a file in the standard motion SA format, load it.
    The SA returned has the axis site, period.

    returned:
      SA: Array of SA values, with unit of g.  dimensions (site, period)
      periods: The periods of the SA array. dimension(period)
      event_index: event index of this slice, to add an extra dimension to SA
      spawn_index: spawn index of this slice, to add an extra dimension to SA
      gmm_index: gmm index of this slice, to add an extra dimension to SA
    """
    f=open(file_full_name,'r')            
    text = f.read().splitlines()
    event_index = int(text[0].split('=')[1])
    text.pop(0) # event
    spawn_index = int(text[0].split('=')[1])
    text.pop(0) # spawn
    gmm_index = int(text[0].split('=')[1]) 
    text.pop(0)
    text.pop(0)
    periods = array([float(ix) for ix in text[0].split(' ')])
    
    text.pop(0) # period_line 
    SA_list = []
    for line in text:
        # Each line is a site
        SA_list.append([float(ix) for ix in line.split(' ')])
    SA = array(SA_list)
    return SA, periods, event_index, spawn_index, gmm_index

    


def save_structures(THE_PARAM_T,structures,compress=False,
                parallel_tag=None, write_title=True):
    """
    Save structure information to file.
    This funtion is called in eqrm analysis.
    """
    if compress: open = myGzipFile
    else: open = file
    if parallel_tag is None:
        parallel_tag = ''
    base_name =  os.path.join(THE_PARAM_T.output_dir,
                              get_structures_file_name(THE_PARAM_T.site_tag))
    name = base_name + parallel_tag
    loc_file=open(name,'w')
    if write_title:
        loc_file.write('LATITUDE LONGITUDE PRE1989 POSTCODE SITE_CLASS '+
                       'SUBURB SURVEY_FACTOR STRUCTURE_CLASSIFICATION '+
                       'HAZUS_STRUCTURE_CLASSIFICATION BID FCB_USAGE ' +
                       'HAZUS_USAGE\n')
    for i in range(len(structures.latitude)):
        maybe_nan = {'SUBURB':None, 'SURVEY_FACTOR':None,
                     'HAZUS_STRUCTURE_CLASSIFICATION':None, 'HAZUS_USAGE':None,
                     'PRE1989':None, 'POSTCODE':None, 'FCB_USAGE':None}
        nan_values = ['1.#QNAN', '-1.#IND'] #,'nan','1.#QNB']
        for title_string in maybe_nan:
            string_value = structures.attributes[title_string][i]
            
            if isinstance(string_value, string_) and \
                    (string_value in nan_values or \
                         not isinstance(string_value,str)):
                
                maybe_nan[title_string] = 'nan'                    
            else:
                maybe_nan[title_string] = structures.attributes[title_string][i]
    #print "structures.latitude[i]",   structures.latitude[i]         
        # loc_file.write('%.6g %.6g %i %i %s %s %.5g %s %s %i %i %s\n'%
        #                (structures.latitude[i],
        #                 structures.longitude[i],
        #                 structures.attributes['PRE1989'][i],
        #                 structures.attributes['POSTCODE'][i],
        #                 structures.attributes['SITE_CLASS'][i],
        #                 maybe_nan['SUBURB'].replace(' ','_'),
        #                 maybe_nan['SURVEY_FACTOR'],
        #                 structures.attributes['STRUCTURE_CLASSIFICATION'][i],
        #                 maybe_nan['HAZUS_STRUCTURE_CLASSIFICATION'],
        #                 structures.attributes['BID'][i],
        #                 structures.attributes['FCB_USAGE'][i],
        #                 maybe_nan['HAZUS_USAGE']))
        if False: #True:
            # problem.  structures.attributes['PRE1989'][i] can be Nan
            loc_file.write('%.6g %.6g %i %i %s %s %.5g %s %s %i %i %s\n'%
                           (structures.latitude[i],
                            structures.longitude[i],
                            structures.attributes['PRE1989'][i],
                            structures.attributes['POSTCODE'][i],
                            structures.attributes['SITE_CLASS'][i],
                            maybe_nan['SUBURB'].replace(' ','_'),
                            maybe_nan['SURVEY_FACTOR'],
                            structures.attributes['STRUCTURE_CLASSIFICATION'][i],
                            maybe_nan['HAZUS_STRUCTURE_CLASSIFICATION'],
                            structures.attributes['BID'][i],
                            structures.attributes['FCB_USAGE'][i],
                            maybe_nan['HAZUS_USAGE']))
        else:
            loc_file.write('%.6g %.6g %s %s %s %s '%
                           (structures.latitude[i],
                            structures.longitude[i],
                            maybe_nan['PRE1989'],
                            maybe_nan['POSTCODE'],
                            structures.attributes['SITE_CLASS'][i],
                            maybe_nan['SUBURB'].replace(' ','_')))
            
            loc_file.write('%.5g %s %s '%
                           (maybe_nan['SURVEY_FACTOR'],
                            structures.attributes['STRUCTURE_CLASSIFICATION'][i],
                            maybe_nan['HAZUS_STRUCTURE_CLASSIFICATION']))
            loc_file.write('%i '%
                           (structures.attributes['BID'][i]))
            loc_file.write('%s '%
                           (maybe_nan['FCB_USAGE']))
            loc_file.write('%s\n'%
                           (maybe_nan['HAZUS_USAGE']))
    loc_file.close()
    return base_name


def get_structures_file_name(site_tag):
    return site_tag + '_structures.txt'
    
def load_structures(save_dir, site_tag):
    """

    return:
    A dictionary. {header:column} The column is a list of the column values.
    """
    file =os.path.join(save_dir, get_structures_file_name(site_tag))
    convert = {
        'LATITUDE':float
        ,'LONGITUDE':float
        ,'PRE1989':int
        ,'POSTCODE':int
        ,'SITE_CLASS':str
        ,'SUBURB':str
        ,'SURVEY_FACTOR':float
        ,'STRUCTURE_CLASSIFICATION':str
        ,'HAZUS_STRUCTURE_CLASSIFICATION':str
        ,'BID':int
        ,'FCB_USAGE':int
        ,'HAZUS_USAGE':str
        }
    attribute_dic, title_index_dic = csv2dict(file, convert=convert,
                                              delimiter=' ')
    attribute_dic['SUBURB'] = [x.replace('_',' ') for x in \
                               attribute_dic['SUBURB']]
    return attribute_dic

def get_event_set_file_name(site_tag):
    return site_tag + '_event_set.txt'

#def save_event_set_new(THE_PARAM_T, event_set, event_activity, source_model,
#                      compress=False):

def save_event_set(THE_PARAM_T, event_set, event_activity, source_model,
                       compress=False):
    """Save event_set information to a file.

    WARNING: ADDING STRINGS INTO THE VALUES OF THIS FILE WILL CAUSE
    CHECK SCENARIOS TO FAIL IN WINDOWS. Due to differences in converting
    floats.  eg 4e-05 or 4e-005.  This could be fixed by improving the
    testing code.

    event_set  Event_set instance
    r_new      event activity (a list or None)
    compress   True if file is to be compressed
    """

    #print('event_set[0]=%s' % type(event_set[0]))
    #print('event_set=%s' % type(event_set))

    # compress file?
    open = file
    if compress:
        open = myGzipFile

    # prepare output file
    file_full_name = THE_PARAM_T.output_dir + \
                     get_event_set_file_name(THE_PARAM_T.site_tag)
    event_file = open(file_full_name, 'w')    

    # write column header line
    event_file.write('trace_start_lat,trace_start_lon,'
                     'trace_end_lat,trace_end_lon,azimuth,dip,'
                     'event_activity,Mw,rupture_centroid_lat,'
                     'rupture_centroid_lon,depth,'
                     'rupture_x,rupture_y,length,width,event_num,name\n')

    # This is for speed, at the expense of memory
    # It is avoiding lots of expensive psudo-event lookups.
    trace_start_lat = event_set.trace_start_lat
    trace_start_lon = event_set.trace_start_lon
    trace_end_lat = event_set.trace_end_lat
    trace_end_lon = event_set.trace_end_lon
    azimuth = event_set.azimuth
    dip = event_set.dip
    event_activity = event_activity.get_ea_event_dimsion_only()
    sources_of_event_set = source_model.sources_of_event_set(len(event_set))

    #name = event_set.name
    #print('name=%s' % str(name))

    Mw = event_set.Mw
    rupture_centroid_lat = event_set.rupture_centroid_lat
    rupture_centroid_lon = event_set.rupture_centroid_lon
    depth = event_set.depth
    rupture_x = event_set.rupture_x
    rupture_y = event_set.rupture_y
    length = event_set.length
    width = event_set.width
    event_num = event_set.event_num
    
    for i in range(len(event_set)):
        s = []     
        s.append(str(trace_start_lat[i]))
        s.append(str(trace_start_lon[i]))
        s.append(str(trace_end_lat[i]))
        s.append(str(trace_end_lon[i]))
        s.append(str(azimuth[i]))
        s.append(str(dip[i]))
        s.append(str(event_activity[i]))
        s.append(str(Mw[i]))
        s.append(str(rupture_centroid_lat[i]))
        s.append(str(rupture_centroid_lon[i]))
        s.append(str(depth[i]))
        s.append(str(rupture_x[i]))
        s.append(str(rupture_y[i]))
        s.append(str(length[i]))
        s.append(str(width[i]))
        s.append(str(event_num[i]))
        s.append(str(sources_of_event_set[i].name))

        # finally, append the fault name
        #s.append(name[i])
        
        line = ','.join(s)
        event_file.write(line + '\n')

    event_file.close()

    return file_full_name        # Used in testing

#def save_event_set(THE_PARAM_T,event_set,r_new,compress=False):
def obsolete_save_event_set(THE_PARAM_T,event_set,r_new,compress=False):
    """
    Save event_set information to file.
    This function is called in eqrm analysis.

    r_new is event activity.  It will be a vector or None.
    """

    if compress: open = myGzipFile
    else: open = file

    file_full_name = THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + \
                     '_event_set.txt'
    event_file=open(file_full_name, 'w')    

    event_file.write('%column 1: sourcezone index\n') 
    event_file.write('%column 2: trace_start_lat\n') 
    event_file.write('%column 3: trace_start_lon\n') 
    event_file.write('%column 4: trace_end_lat\n') 
    event_file.write('%column 5: trace_end_lon\n') 
    event_file.write('%column 6: azimuth\n') 
    event_file.write('%column 7: dip\n') 
    event_file.write('%column 8: id of attenuation model position.')
    event_file.write(' 0 is the first model. 1 is the second.\n') 
    event_file.write('%column 9: event activity\n') 
    event_file.write('%column 10: Mw\n') 
    event_file.write('%column 11: rupture_centroid_lat\n') 
    event_file.write('%column 12: rupture_centroid_lon\n') 
    event_file.write('%column 13: depth\n') 
    event_file.write('%column 14: rupture_x\n') 
    event_file.write('%column 15: rupture_y\n') 
    event_file.write('%column 16: length\n') 
    event_file.write('%column 17: width\n') 
    event_file.write('%column 18: Event index\n')

    # This is for speed, at the expence of memory
    # It is avoiding lots of expensive psudo-event lookups.

    source_zone_id = event_set.source_zone_id
    trace_start_lat = event_set.trace_start_lat
    trace_start_lon = event_set.trace_start_lon
    trace_end_lat = event_set.trace_end_lat
    trace_end_lon = event_set.trace_end_lon
    azimuth = event_set.azimuth
    dip = event_set.dip
    att_model_index = event_set.att_model_index
            
    Mw = event_set.Mw
    rupture_centroid_lat = event_set.rupture_centroid_lat
    rupture_centroid_lon = event_set.rupture_centroid_lon
    depth = event_set.depth
    rupture_x = event_set.rupture_x
    rupture_y = event_set.rupture_y
    length = event_set.length
    width = event_set.width
    # Pseudo_Event_Set will have a index attribute
    # Event_Set will not.
    try:
        index = event_set.index
    except AttributeError:
        index = None
    
    for i in range(len(event_set)):
        s = []
        
        s.append(str(source_zone_id[i]))
        s.append(str(trace_start_lat[i]))
        s.append(str(trace_start_lon[i]))
        s.append(str(trace_end_lat[i]))
        s.append(str(trace_end_lon[i]))
        s.append(str(azimuth[i]))
        s.append(str(dip[i]))
        
        try:
            s.append(str(att_model_index[i]))
        except AttributeError:
            s.append('-1')
        try:
            s.append(str(r_new[i]))
        except (IndexError, TypeError):
            s.append('-1')
            
        s.append(str(Mw[i]))
        s.append(str(rupture_centroid_lat[i]))
        s.append(str(rupture_centroid_lon[i]))
        s.append(str(depth[i]))
        s.append(str(rupture_x[i]))
        s.append(str(rupture_y[i]))
        s.append(str(length[i]))
        s.append(str(width[i]))
        # Pseudo_Event_Set will have a index attribute
        # Event_Set will not.
        if index is None:
            s.append(str(i))
        else:
            s.append(str(index[i]))
        
        #s.append('\n')
        line = ','.join(s)
        event_file.write(line + '\n')
        #event_file.writelines(line)
    #assert len(Mw)==len(r_nu)
    #for i in range(len(Mw)):
    #    mag_file.write('%.5g %.10g\n'%(Mw[i],r_nu[i]))
    event_file.close()
    return file_full_name # Used in testing

def load_event_set(saved_dir, site_tag):
    """Load the event set from a saved file.

    saved_dir  path to directory for the output file
    site_tag   

    Returns a dictionary with labels such as
    'Mw' and 'event_activity'
    and values of 1D arrays of this info.
    """
    
    file =os.path.join(saved_dir, get_event_set_file_name(site_tag))
    convert = {
        'trace_start_lat':float,
        'trace_start_lon':float,
        'trace_end_lat':float,
        'trace_end_lon':float,
        'azimuth':float,
        'dip':float,
        'event_activity':float,
        'Mw':float,
        'rupture_centroid_lat':float,
        'rupture_centroid_lon':float,
        'depth':float,
        'rupture_x':float,
        'rupture_y':float,
        'length':float,
        'width':float,
        'event_num':int,
        'name':str
        }
    attribute_dic, title_index_dic = csv2dict(file, convert=convert,
                                              delimiter=',')
    return attribute_dic
     


def save_damage(save_dir, site_tag, damage_name, damage, building_ids,
                 compress=False, parallel_tag=None, write_title=True):
    """Save buildingid and the non-cumulative probability of each damage state.

    save_dir - The directory to save the files into.
    site_tag - A string at the beginning of the file name.
    damage_name - the type of damage occuring. eg 'structural',
                  'non-structural'
    damage - A 2D array of cumulative probability of being in a damage state.
             Axis site, damage state (4 damage states, slight, moderate,
             extensive and complete)
    building_id - a 1D array of building ids                  
    """
    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''  
    base_name = os.path.join(save_dir,
                             site_tag + "_" + damage_name + '_damage.txt')
    name = base_name + parallel_tag
    f=open(name,'w')
    if write_title is True:
        f.write('building_id, slight, moderate, extensive, complete\n')
    for building_id, damge_site in map(None, building_ids, damage):
        f.write(str(building_id))
        f.write(",")
        damage_st = ",".join(str(x) for x in damge_site)
        f.write(damage_st)
        f.write("\n")
    f.close()
    return base_name
      
def save_ecloss(ecloss_name,THE_PARAM_T,ecloss,structures,compress=False,
                parallel_tag=None):
    """
    Save economic loss.
    For example; total_building_loss.
    parameters:
      ecloss_name: a string tag, for the file name.
        Informally used to describe the file information.
          '_total_building' - values are the combined building loss
            struct/non-struct drift/non-struct accel' sensitive/contents
          '_building' - total loss not including contents
            struct/non-struct drift sensitive/non-struct accel' sensitive
          '_contents' - contents loss
        These 'definitions' are in analysis.py
      THE_PARAM_T - used to get output_dir and site_tag
      ecloss - the economic values to save.  2d array (location, events)
      structures - Structures instance.  Used to get the BID - building ID 
    """

    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''  
    base_name = os.path.join(THE_PARAM_T.output_dir, get_ecloss_file_name(
        THE_PARAM_T.site_tag, ecloss_name))
    name = base_name + parallel_tag
    f=open(name,'w')
    f.write('% First row is bid (building id) - subsequent rows are events\n')
    f.write(' '.join([str(bid) for bid in structures.attributes['BID']])
               +'\n') 
    for i in range(ecloss.shape[1]): # for all events
        el=ecloss[:,i] # sites,event
        f.write(' '.join(['%.10g'%(l) for l in el])+'\n')
    f.close()
    return base_name

def get_ecloss_file_name(site_tag, ecloss_name):
    return site_tag + ecloss_name + '_loss.txt'

def load_ecloss(ecloss_name, save_dir, site_tag):
    """
    
    return:
      BID: Building ID's
      ecloss: array with dimensions(events, sites)
    """
    file = os.path.join(
        save_dir, get_ecloss_file_name(site_tag, ecloss_name))
    BID_ecloss = scipy.loadtxt(file,
                            dtype=scipy.float64, delimiter=' ', skiprows=1)
    if len(BID_ecloss.shape) == 1: # one row file
        BID_ecloss = reshape(BID_ecloss, (-1,1))
    ecloss_loaded = scipy.transpose(BID_ecloss[1:,:])
    return ecloss_loaded, BID_ecloss[0,:]
        
    
def save_val(THE_PARAM_T, val, file_tag, compress=False, parallel_tag=None):
    """
    General file to save one vector of values.

    Currently only used to save total building cost;
    flie_tag is '_bval'
    Writes a file of the total building cost, (3 building costs plus
    contents cost for all sites), assuming val is
    all_sites.cost_breakdown(ci=THE_PARAM_T.ci)
    
    """
    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''

    base_name =  get_val_file_name(THE_PARAM_T.site_tag,
                                   file_tag)
    base_name = os.path.join(THE_PARAM_T.output_dir, base_name)
    name = base_name + parallel_tag
    f=open(name,'w')
    for value in val:
        # Fix for nans printing differently in windows and Linux.
        if isnan(value):
            f.write('nan\n')
        else:
            f.write('%.10g\n'%(value))
    f.close()
    return base_name

def get_val_file_name(site_tag, file_tag='_bval'):
    return site_tag + file_tag + '.txt'
    

def load_val(save_dir, site_tag, file_tag='_bval'):
    """
    General file to load an array of values, with no header.

    Currently only used to load total building cost;
    Return the total building values
    
    return:
      val: an array of values      
    """
    val = scipy.loadtxt(os.path.join(
        save_dir, get_val_file_name(site_tag, file_tag)),
                  dtype=scipy.float64, delimiter=',', skiprows=0)
    return val

def save_fatalities(fatalities_name,THE_PARAM_T,fatalities,sites,compress=False,
                parallel_tag=None, write_title=True):
    """
    Save fatalities and the list of sites (lat,lon).
    
    parameters:
      fatalities_name: a string tag, for the file name.
      THE_PARAM_T - used to get output_dir and site_tag
      fatalities - the fatality values to save.  2d array (location, events)
    """

    if compress:
        open = myGzipFile
    else:
        open = file
    if parallel_tag is None:
        parallel_tag = ''  
    base_name = os.path.join(THE_PARAM_T.output_dir, get_fatalities_file_name(
        THE_PARAM_T.site_tag, fatalities_name))
    name = base_name + parallel_tag
    
    if sites is not None:
        save_sites(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                       sites, compress, parallel_tag, write_title)
                    
    f=open(name,'w')
    f.write('% This file contains the fatalities, subsequent rows are events\n')
 
    for i in range(fatalities.shape[1]): # for all events
        el=fatalities[:,i] # sites,event
        f.write(' '.join(['%.10g'%(l) for l in el])+'\n')
    f.close()
    return base_name

def get_fatalities_file_name(site_tag, fatalities_name):
    return site_tag + fatalities_name + '.txt'    
    
def load_fatalities(fatalities_name, save_dir, site_tag):
    """
    
    return:
      fatalities: array with dimensions(events, sites)
    """
    file = os.path.join(
        save_dir, get_fatalities_file_name(site_tag, fatalities_name))
    BID_fatalities = scipy.loadtxt(file,
                            dtype=scipy.float64, delimiter=' ', skiprows=1)
    if len(BID_fatalities.shape) == 1: # one row file
        BID_fatalities = reshape(BID_fatalities, (-1,1))
    fatalities_loaded = scipy.transpose(BID_fatalities[0:,:])
    
    lat, lon = load_sites(save_dir, site_tag)
    
    return fatalities_loaded, lat, lon
    
def join_parallel_files(base_names, size, compress=False):
    """
    Row append a common set of files produced by running EQRM in parallel.

    The input is a list of base names.
    """
    if compress: my_open = myGzipFile
    else: my_open = open
    for base_name in base_names:
        f=my_open(base_name,'w')
        for i in range(size):
            name = base_name + FILE_TAG_DELIMITER + str(i)
            f_block =  my_open(name, 'r')
            try:
                for line in f_block:
                    f.write(line)
            finally:
                f_block.close()
            os.remove(name)
        
    
def join_parallel_files_column(base_names, size, compress=False,
                               delimiter=' '):
    """
    If files are writen where each column represents a structure, combine
    the file blocks produced by running in parallel.
    NOTE: each row has to end with the delimeter being used.
    """
    if compress: my_open = myGzipFile
    else: my_open = open
   
    for base_name in base_names:
        f=my_open(base_name,'w')
        f_blocks = []
        for i in range(size):       
            name = base_name + FILE_TAG_DELIMITER + str(i)
            f_blocks.append(my_open(name, 'r'))
            comment = f_blocks[i].readline() # Comment from last file.

        f.write(comment)
        while True:
            line_blocks = []
            for f_block in f_blocks:
                section = f_block.readline()
                line_blocks.append(section[:-1] + delimiter)
            line_blocks.append('\n')
            if section == '':
                break
            row = ''.join(line_blocks)
            f.write(row)
        f.close()

        # Remove all of the block files for this base name.
        for i,f_block in enumerate(f_blocks):
            f_block.close()
            os.remove(base_name + FILE_TAG_DELIMITER + str(i))

######
# Bridge file save/load functions.
######

def get_bridges_file_name(site_tag):
    """Make a standard bridges save/load filename.

    site_tag  global site tag

    Returns a filename.
    """

    return site_tag + '_bridges.txt'


def save_bridges(THE_PARAM_T, bridges, compress=False, parallel_tag=None,
                 write_title=True):
    """Save bridge information to file.

    THE_PARAM_T   global parameters reference
    bridges       the bridges data to save
    compress      flag - True if output file is compressed
    parallel_tag  ??
    write_title   flag - True if header line is to be written

    Returns the base name of the created file.
    """

    if parallel_tag is None:
        parallel_tag = ''

    base_name =  os.path.join(THE_PARAM_T.output_dir,
                              get_bridges_file_name(THE_PARAM_T.site_tag))
    name = base_name + parallel_tag

    if compress:
        loc_file = GzipFile(name, 'w')
    else:
        loc_file = open(name, 'w')

    if write_title:
        loc_file.write('BID LATITUDE LONGITUDE STRUCTURE_CLASSIFICATION '
                       'STRUCTURE_CATEGORY SKEW SPAN SITE_CLASS\n')

    for i in range(len(bridges.latitude)):
        loc_file.write('%d %.6g %.6g %s %s %.1f %d %s\n'
                       % (bridges.attributes['BID'][i],
                          bridges.latitude[i],
                          bridges.longitude[i],
                          bridges.attributes['STRUCTURE_CLASSIFICATION'][i],
                          bridges.attributes['STRUCTURE_CATEGORY'][i],
                          bridges.attributes['SKEW'][i],
                          bridges.attributes['SPAN'][i],
                          bridges.attributes['SITE_CLASS'][i]))
    loc_file.close()

    return base_name


def load_bridges(save_dir, site_tag):
    """Load bridges data into a Bridges object.

    save_dir  path to directory containing save data files
    site_tag  the site tag describing data sets

    Returns a dictionary: {header: column}
    The column is a list of the column values.
    """

    file = os.path.join(save_dir, get_bridges_file_name(site_tag))

    # FIXME: This dictionary should be in a module somewhere so
    #        we don't need to type it in repeatedly.
    convert = {'BID': int,
               'LATITUDE': float,
               'LONGITUDE': float,
               'STRUCTURE_CLASSIFICATION': str,
               'STRUCTURE_CATEGORY': str,
               'SKEW': float,
               'SPAN': int,
               'SITE_CLASS': str}

    (attributes, _) = csv2dict(file, convert=convert, delimiter=' ')

    return attributes

def get_source_file_handle(THE_PARAM_T, source_file_type='zone'):
    """
    Return a file handle of a source xml file.
    """
    
    if source_file_type == 'fault':
        source_tag = THE_PARAM_T.fault_source_tag
        file_constant = FAULT_SOURCE_FILE
    elif source_file_type == 'zone':
        source_tag = THE_PARAM_T.zone_source_tag
        file_constant = ZONE_SOURCE_FILE
    elif source_file_type == 'event_type':
        source_tag = THE_PARAM_T.event_control_tag
        file_constant = EVENT_CONTROL_FILE
    else:
        raise IOError(source_file_type, " is not a valid source file type.")
    if source_tag is None:
        source_file = THE_PARAM_T.site_tag + file_constant + '.xml'
    else:
        source_file = THE_PARAM_T.site_tag  + file_constant + '_' \
                      + source_tag + '.xml'
    source_file = os.path.join(THE_PARAM_T.input_dir, source_file)
    return open(source_file)
    
    

################################################################################

if __name__ == "__main__":
    load_ecloss_and_sites(r"Q:\trunk_branches\trunk\demo\output\scen_risk2",
                          "newc")
            
