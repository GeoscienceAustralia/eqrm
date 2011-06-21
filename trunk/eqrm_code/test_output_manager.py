import os
import sys
import unittest
import tempfile
import shutil
from scipy import array, zeros, allclose, asarray, transpose, fromfunction, who

from eqrm_code.output_manager import *
from eqrm_code.sites import Sites
from eqrm_code.source_model import Source_Model
from eqrm_code.bridges import Bridges
from eqrm_code.event_set import Event_Set, Event_Activity
from test_structures import get_sites_from_dic
from eqrm_code.util import dict2csv, determine_eqrm_path
import eqrm_code.eqrm_filesystem as efs



class Dummy:
    def __init__(self):
        pass      
        
    def set_event_set_indexes(self,indexes):
        self.event_set_indexes = indexes
        
    def get_event_set_indexes(self):
        return self.event_set_indexes
    

def get_bridges_from_dic(attributes=None):
    """Get a Bridges object from a dictionary.

    attributes  a dictionary of bridge data

    Returns (bridge_obj, attributes)
    """

    attributes = {'BID': int,
                  'LATITUDE': float,
                  'LONGITUDE': float,
                  'STRUCTURE_CLASSIFICATION': str,
                  'STRUCTURE_CATEGORY': str,
                  'SKEW': float,
                  'SPAN': int,
                  'SITE_CLASS': str}

    # get a temporary file
    (handle, filename) = tempfile.mkstemp('.csv','get_bridges_from_dic_')
    os.close(handle)

    (filename, _) = write_test_bridges_file(filename)

    # create links to required building parameters
    eqrm_dir = determine_eqrm_path()
    data_dir = os.path.join(eqrm_dir, efs.Resources_Data_Path)
    default_input_dir=os.path.join(eqrm_dir, efs.Resources_Data_Path)

    #bridges = Bridges.from_csv(filename, default_input_dir,
    #                           eqrm_dir=eqrm_dir, **attributes)
    bridges = Bridges.from_csv(filename, **attributes)

    # clean up
    os.remove(filename)

    return (bridges, attributes)

def write_test_bridges_file(filename, attributes=None):
    """Write a test bridges data file.

    filename    path to the file to write
    attributes  attributes dictionary

    Returns (filename, attributes)
    """

    # FIXME: This should be in a global module
    title_index_dic = {'BID': 0,
                       'LATITUDE': 1,
                       'LONGITUDE': 2,
                       'STRUCTURE_CLASSIFICATION': 3,
                       'STRUCTURE_CATEGORY': 4,
                       'SKEW': 5,
                       'SPAN': 6,
                       'SITE_CLASS': 7}

    if attributes is None:
        attributes = {'BID': [1, 2],
                      'LATITUDE': [-32.9, 32.7],
                      'LONGITUDE': [151.7, 151.3],
                      'STRUCTURE_CLASSIFICATION': ['HWB17', 'HWB22'],
                      'STRUCTURE_CATEGORY': ['BRIDGE', 'BRIDGE'],
                      'SKEW': ['0', '32'],
                      'SPAN': ['1', '4'],
                      'SITE_CLASS': ['C', 'F']}

    dict2csv(filename, title_index_dic, attributes)

    return (filename, attributes)


class Test_Output_manager(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_hazard(self):
        THE_PARAM_T=Dummy()
        soil_amp = True
        hazard_name = 'soil_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_save_hazard') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32,-31])
        lon = array([120,121])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([100]), array([500.])]
        THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    hazard[i,j,k] = site*period*rtrn[0]

        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)


        # check the site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=str(THE_PARAM_T.return_periods[i])
            if rp[-2:-1] == '.':
                rp = rp[:-2] + rp[-1]
            file_name = THE_PARAM_T.output_dir+THE_PARAM_T.site_tag+ '_'+ \
                        hazard_name+'_rp' + \
                        rp.replace('.','pt').replace(' ','') + EXTENSION
            f=open(file_name,'r')

            text = f.read().splitlines()
            # ditch the comment lines
            text.pop(0)
            text.pop(0)

            # Check the periods
            # Convert a space separated text line into a numeric float array
            periods_f = array([float(ix) for ix in text[0].split(' ')])
            self.assert_ (allclose(periods_f,array(THE_PARAM_T.atten_periods)))
            text.pop(0)

            for j,site in enumerate(lon):
                split = text[j].split(' ')
                for k,period in enumerate(THE_PARAM_T.atten_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    self.assert_ (allclose(array(float(split[k])),
                           array(float(site * period * THE_PARAM_T.return_periods[i]))))
                    f.close()
            os.remove(file_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_SA(self):
        THE_PARAM_T=Dummy()
        soil_amp = False
        hazard_name = 'bedrock_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_hazard_1') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32,-31])
        lon = array([120,121])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([.025])]
        THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    hazard[i,j,k] = site*period*rtrn[0]
        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)

        # delete site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=THE_PARAM_T.return_periods[i]
            file_full_name = THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + '_' \
                        + hazard_name + '_rp' + \
                        str(rp).replace('.','pt').replace(' ','') + '.txt'
            SA, periods_f = load_SA(file_full_name)
            self.assert_ (allclose(SA, hazard))
            self.assert_ (allclose(array(periods_f),
                                   array(THE_PARAM_T.atten_periods)))

            os.remove(file_full_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_hazards_1(self):
        THE_PARAM_T=Dummy()
        soil_amp = True
        hazard_name = 'soil_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_hazard_1') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32])#,-31])
        lon = array([120])#,121])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([.025]), array([0.5])]#, array([1.00]),
                                #array([2]), array([2.5]), array([2000])]
        THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    hazard[i,j,k] = site*period*rtrn[0]
        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)
        SA, periods, return_p = load_hazards(THE_PARAM_T.output_dir,
                         THE_PARAM_T.site_tag, soil_amp)
        self.assert_ (allclose(SA, hazard))
        self.assert_ (allclose(array(periods), array(THE_PARAM_T.atten_periods)))
        self.assert_ (allclose(return_p, THE_PARAM_T.return_periods))

        # delete site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=THE_PARAM_T.return_periods[i]
            file_full_name = THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + '_' \
                        + hazard_name + '_rp' + \
                        str(rp).replace('.','pt').replace(' ','') + '.txt'
            os.remove(file_full_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_hazardsII(self):
        THE_PARAM_T=Dummy()
        soil_amp = False
        hazard_name = 'bedrock_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_hazardsII') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32])#,-31])
        lon = array([120])#,121])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([.025]), array([0.5]), array([1.00]),
                                array([2]), array([2.5]), array([2000])]
        THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    hazard[i,j,k] = site*period*rtrn[0]
        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)
        SA, periods, return_p = load_hazards(THE_PARAM_T.output_dir,
                         THE_PARAM_T.site_tag, soil_amp)
        self.assert_ (allclose(SA, hazard))
        self.assert_ (allclose(array(periods), array(THE_PARAM_T.atten_periods)))
        self.assert_ (allclose(return_p, THE_PARAM_T.return_periods))

        # delete site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=str(THE_PARAM_T.return_periods[i])
            if rp[-2:-1] == '.':
                rp = rp[:-2] + rp[-1]
            file_name = THE_PARAM_T.output_dir+THE_PARAM_T.site_tag+ '_'+ \
                        hazard_name+'_rp' + \
                        rp.replace('.','pt').replace(' ','') + EXTENSION
            os.remove(file_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_hazardsIII(self):
        THE_PARAM_T=Dummy()
        soil_amp = True
        hazard_name = 'soil_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_hazardsIII') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32, -31, -30])
        lon = array([120, 121, 122])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([.025]), array([0.5])]
        THE_PARAM_T.atten_periods = [0.3, 0.5]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                    hazard[i,j,k] = site*period*rtrn[0]
        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)
        SA, periods, return_p = load_hazards(THE_PARAM_T.output_dir,
                         THE_PARAM_T.site_tag, soil_amp)
        self.assert_ (allclose(SA, hazard))
        self.assert_ (allclose(array(periods), array(THE_PARAM_T.atten_periods)))
        self.assert_ (allclose(return_p, THE_PARAM_T.return_periods))

        # delete site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=THE_PARAM_T.return_periods[i]
            file_name = THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + '_' \
                        + hazard_name + '_rp' + \
                        str(rp).replace('.','pt').replace(' ','') + '.txt'

            os.remove(file_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_hazards_no_files(self):
        THE_PARAM_T=Dummy()
        soil_amp = False
        hazard_name = 'bedrock_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_hazards_no_files') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        try:
            SA, periods, return_p = load_hazards(THE_PARAM_T.output_dir,
                                                THE_PARAM_T.site_tag,
                                                soil_amp)
        except IOError:
            pass
        else:
            self.failUnless(1==0,
                        'empty directory did not cause an error')
        os.rmdir(THE_PARAM_T.output_dir)


    def test_save_sites(self):
        output_dir = tempfile.mkdtemp('output_managertest_save_sites') + os.sep
        site_tag = "site_tag"
        lat = [-32]
        lon = [120]
        sites = Sites(lat,lon)

        save_sites(output_dir, site_tag,sites,compress=False)

        # Check the location file output
        loc_file_name = output_dir + \
                        site_tag + '_locations.txt'
        loc_file=open(loc_file_name,'r')

        text = loc_file.read().splitlines()
        # ditch the comment line
        text.pop(0)
        for line, lat_value, lon_value in map(None, text, lat, lon):
            self.assertEqual(float(line.split(' ')[0]), float(lat_value))
            self.assertEqual(float(line.split(' ')[1]), float(lon_value))
        loc_file.close()

        os.remove(loc_file_name)
        os.rmdir(output_dir)


    def test_load_sites(self):
        output_dir = tempfile.mkdtemp('output_managertest_save_sites') + os.sep
        site_tag = "site_tag"
        lat_actual = [-32, -33]
        lon_actual = [120, 125]
        sites = Sites(lat_actual,lon_actual)

        save_sites(output_dir, site_tag,sites,compress=False)
        lat, lon = load_sites(output_dir, site_tag)

        os.remove(
            os.path.join(output_dir, get_sites_file_name(site_tag)))
        os.rmdir(output_dir)

        self.assertEqual(float(lat_actual[0]), float(lat[0]))
        self.assertEqual(float(lon_actual[0]), float(lon[0]))

    def test_load_sitesII(self):
        output_dir = tempfile.mkdtemp('output_managertest_save_sites') + os.sep
        site_tag = "site_tag"
        lat_actual = [-32]
        lon_actual = [120]
        sites = Sites(lat_actual,lon_actual)

        save_sites(output_dir, site_tag,sites,compress=False)
        lat, lon = load_sites(output_dir, site_tag)

        os.remove(
            os.path.join(output_dir, get_sites_file_name(site_tag)))
        os.rmdir(output_dir)

        self.assertEqual(float(lat_actual[0]), float(lat[0]))
        self.assertEqual(float(lon_actual[0]), float(lon[0]))


    def test_save_distances(self):

        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_save_distances') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = [-32,-31]
        lon = [120,121]
        sites = Sites(lat,lon)

        # Building the event instance
        trace_start_lat = [-38.15]
        trace_start_lon = [146.5]
        azimuth = [217]
        dip = [60]
        weight = [1]
        event_activity = [0]
        Mw = [6.9]
        lat0 = [-38.31]
        lon0 = [146.3]
        depth = [6.5]
        length = [50.6]
        width = [15]

        source_zone_id = array([0])

        event_set = Event_Set.create(
            depth=depth,rupture_centroid_lat=lat0,
            rupture_centroid_lon=lon0,azimuth=azimuth,
            dip=dip,Mw=Mw,fault_width=15.0)
        event_set.source_zone_id = array([0])
        save_distances(THE_PARAM_T,sites,event_set,compress=False)

        # Check the file output
        file_name = THE_PARAM_T.output_dir+ \
                   THE_PARAM_T.site_tag+'_distance_rjb.txt'
        file_h=open(file_name,'r')

        text = file_h.read().splitlines()
        # ditch the comment lines
        text.pop(0)

        # Convert a space separated text line into a numeric float array
        site_distance = array([float(ix) for ix in text[0].split(' ')])
        distance_calc = sites.distances_from_event_set(event_set).distance(
            'Joyner_Boore').swapaxes(0,1)
        self.assert_ (allclose(array([site_distance]),
                               distance_calc,0.1))
        file_h.close()
        # Del the file output
        os.remove(file_name)

        file_name = THE_PARAM_T.output_dir + \
                    THE_PARAM_T.site_tag + '_distance_rup.txt'
        file_h=open(file_name,'r')

        text = file_h.read().splitlines()
        # ditch the comment lines
        text.pop(0)

        # Convert a space separated text line into a numeric float array
        site_distance = array([float(ix) for ix in text[0].split(' ')])
        distance_calc = sites.distances_from_event_set(event_set).distance(
            'Rupture').swapaxes(0,1)
        self.assert_ (allclose(array([site_distance]),
                               distance_calc,0.1))
        file_h.close()
        # Del the file output
        os.remove(file_name)
        os.rmdir(THE_PARAM_T.output_dir)

    def test_save_distancesII(self):

        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_save_distances') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = [-32,-31]
        lon = [120,121]
        sites = Sites(lat,lon)

        # Building the event instance
        #trace_start_lat = [-38.15, -38]
        #trace_start_lon = [146.5, 146]
        azimuth = [217, 200]
        dip = [60, 58]
        weight = [1, 1]
        event_activity = [0, 0]
        Mw = [6.9, 6.7]
        lat0 = [-38.31, -38]
        lon0 = [146.3, 146]
        depth = [6.5, 5]
        length = [50.6, 50]
        width = [15, 14]

        source_zone_id = array([0, 0])

        event_set = Event_Set.create(
            depth=depth,rupture_centroid_lat=lat0,
            rupture_centroid_lon=lon0,azimuth=azimuth,
            dip=dip,Mw=Mw,fault_width=15.0)
        event_set.source_zone_id = array([0,0])
        save_distances(THE_PARAM_T,sites,event_set,compress=False)

        # Check the file output
        file_name = THE_PARAM_T.output_dir+ \
                   THE_PARAM_T.site_tag+'_distance_rjb.txt'
        file_h=open(file_name,'r')

        text = file_h.read().splitlines()
        # ditch the comment lines
        text.pop(0)
        # Convert a space separated text line into a numeric float array
        site_distance = array([float(ix) for ix in text[0].split(' ')])
        distance_calc = sites.distances_from_event_set(event_set).distance(
            'Joyner_Boore').swapaxes(0,1)
        self.assert_ (allclose(array([site_distance]),
                               distance_calc,0.1))
        file_h.close()
        # Del the file output
        os.remove(file_name)

        file_name = THE_PARAM_T.output_dir + \
                    THE_PARAM_T.site_tag + '_distance_rup.txt'
        file_h=open(file_name,'r')

        text = file_h.read().splitlines()
        # ditch the comment lines
        text.pop(0)

        # Convert a space separated text line into a numeric float array
        site_distance = array([float(ix) for ix in text[0].split(' ')])
        distance_calc = sites.distances_from_event_set(event_set).distance(
            'Rupture').swapaxes(0,1)
        self.assert_ (allclose(array([site_distance]),
                               distance_calc,0.1))
        file_h.close()
        # Del the file output
        os.remove(file_name)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_distances(self):

        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_save_distances') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = [-32,-31]
        lon = [120,121]
        sites = Sites(lat,lon)

        # Building the event instance
        trace_start_lat = [-38.15]
        trace_start_lon = [146.5]
        azimuth = [217]
        dip = [60]
        weight = [1]
        event_activity = [0]
        Mw = [6.9]
        lat0 = [-38.31]
        lon0 = [146.3]
        depth = [6.5]
        length = [50.6]
        width = [15]

        source_zone_id = array([0])

        event_set = Event_Set.create(
            depth=depth,rupture_centroid_lat=lat0,
            rupture_centroid_lon=lon0,azimuth=azimuth,
            dip=dip,Mw=Mw,fault_width=15.0)
        event_set.source_zone_id = array([0])
        save_distances(THE_PARAM_T,sites,event_set,compress=False)

        dist = load_distance(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag, True)

        distance_calc = sites.distances_from_event_set(event_set).distance(
            'Joyner_Boore').swapaxes(0,1)
        self.assert_ (allclose(array([dist]),
                               distance_calc,0.1))
        # Del the file output
        file = get_distance_file_name(True,  THE_PARAM_T.site_tag)
        os.remove(os.path.join(THE_PARAM_T.output_dir, file))
        file = get_distance_file_name(False,  THE_PARAM_T.site_tag)
        os.remove(os.path.join(THE_PARAM_T.output_dir, file))
        os.rmdir(THE_PARAM_T.output_dir)


    def test_save_motion(self):
        # This test is using the flexibility in the save_motion function,
        # which is not present in the actual data, I suspect.

        # The demos use save motion, the imp' tests don't though
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_save_motion') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]
        soil_amp = True
        motion_name = "soil_SA"
        motion = array([[[[[4,5]],[[2,7,]]]]])# spawn,gmm,sites,event.periods
        save_motion(soil_amp, THE_PARAM_T, motion)
        # Check the file output
        for i in range(motion.shape[3]):
            file_name = THE_PARAM_T.output_dir+THE_PARAM_T.site_tag+ '_' \
                   + motion_name + '_motion_' + \
                   str(i) + '_spawn_0_gmm_0.txt'
            file_h=open(file_name,'r')

            text = file_h.read().splitlines()
            # ditch the comment lines
            text.pop(0)
            text.pop(0)
            text.pop(0)
            text.pop(0)
            # Convert a space separated text line into a numeric float array
            periods_f = array([float(ix) for ix in text[0].split(' ')])
            self.assert_ (allclose(periods_f,array(THE_PARAM_T.atten_periods)))
            text.pop(0)

            for line_i,line in enumerate(text):
                num_f = array([float(ix) for ix in line.split(' ')])
                self.assert_ (allclose( num_f, motion[0,0,line_i,0,:]))
            file_h.close()
            os.remove(file_name)
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_save_damage(self):
        save_dir = tempfile.mkdtemp('test_load_save_damage') + os.sep
        site_tag = "site_tag"
        damage_name = 'test_load_save_damage_'
        damage = array([[1, 2, 3, 4], [10, 20, 30, 40]])
        building_ids = array([1, 2])
        name = save_damage(save_dir, site_tag, damage_name, damage,
                           building_ids)

        # Check the file output
        file_h=open(name,'r')

        text = file_h.read().splitlines()
        # ditch the comment lines
        text.pop(0)
        for i, line in enumerate(text):
            id_damage = array([float(ix) for ix in line.split(',')])
            self.assert_ (allclose(id_damage[0],building_ids[i]))
            self.assert_ (allclose(id_damage[1:],damage[i]))
        file_h.close()
        os.remove(name)
        os.rmdir(save_dir)


    def test_save_event_set(self):
        rupture_centroid_lat = [-33.351170370959323, -32.763381339789468]
        rupture_centroid_lon = [151.45946928787703, 151.77787395867014]
        azimuth = [162.8566392635347, 201.51805898897854]
        dip = [35.0, 35.0]
        ML = None
        Mw = [5.0286463459649076, 4.6661943094693887]
        fault_width = [15.0, 15.0]
        depth_top_seismogenic = [7.0, 7.0]

        set = Event_Set.create(
            rupture_centroid_lat,
            rupture_centroid_lon,
            azimuth,
            dip,
            ML,
            Mw,
            None, #depth,
            fault_width,
            depth_top_seismogenic=depth_top_seismogenic)
        set.source_zone_id = asarray([0,1]) # FIXME
        set.att_model_index = asarray([0,1]) # FIXME
        event_activity = [0.2, 0.4]
        
        setups = [('1', [1]), ('0',[0])]
        setups_dic = dict(setups)
        sources = []
        for setup in setups:
            d = Dummy()
            d.name = setup[0]
            d.event_set_indexes = setup[1]
            sources.append(d)
        sm = Source_Model(sources)
        
        ea = Event_Activity(len(Mw))
        ea.set_event_activity(event_activity)
        
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_event_set') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        file_full_name = save_event_set(
            THE_PARAM_T,set, ea, sm)
        out = load_event_set(
            THE_PARAM_T.output_dir, THE_PARAM_T.site_tag)
        #print "out", out
        msg = 'loaded Mw=%s, expected Mw=%s' % (str(out['Mw']), \
                                                str(set.Mw))
        #self.failUnless(allclose(out['Mw'], set.Mw), msg)
        self.assert_ (allclose(out['Mw'], set.Mw)), msg
        msg = 'loaded event_activity=%s, expected event_activity=%s' % \
              (str(out['event_activity']), str(asarray(event_activity)))
        self.failUnless(allclose(out['event_activity'],
                                 asarray(event_activity)), msg)
        self.assert_ (allclose(out['event_activity'],
                               asarray(event_activity)))
        set_dic = set.introspect_attribute_values()
        for key in out:
            if set_dic.has_key(key):
                #print "key", key
                if key == 'event_activity':
                    self.assert_(allclose(out[key],
                                 asarray(event_activity)))
                else:
                    self.assert_(allclose(out[key],
                                           set_dic[key]))
            elif key == 'name':
                for i,name in enumerate(out[key]):
                    self.assert_(i == int(name))
            elif key == 'event_activity':
                self.assert_(allclose(out[key],
                                      asarray(event_activity)))
            else:
                self.fail()
        os.remove(file_full_name)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_join_parallel_files(self):
        compress = False
        file_num = 5
        cleanup_file_names = []

        handle, base_file_name = tempfile.mkstemp('.txt', __name__ + '_')
        os.close(handle)

        if compress: my_open = myGzipFile
        else: my_open = open

        for i in range(file_num):
            file_name = base_file_name + FILE_TAG_DELIMITER +  str(i)
            cleanup_file_names.append(file_name)
            f_handle = my_open(file_name, 'w')
            f_handle.write(str(i)+ '\n')
            f_handle.close()

        join_parallel_files([base_file_name], file_num, compress=False)

        f_check =  my_open(base_file_name, 'r')
        for i,line in enumerate(f_check):
            self.assert_ (i == int(line))
        f_check.close()
        os.remove(base_file_name)


    def test_join_parallel_files_column(self):
        compress = False
        file_num = 6
        cleanup_file_names = []

        handle, base_file_name = tempfile.mkstemp('.txt', __name__ + '_')
        os.close(handle)

        if compress: my_open = myGzipFile
        else: my_open = open

        for i in range(0,file_num):
            file_name = base_file_name + FILE_TAG_DELIMITER +  str(i)
            cleanup_file_names.append(file_name)
            f_handle = my_open(file_name, 'w')
            f_handle.write('% First row is bid (building id)\n')
            f_handle.write(str(i)+ ' ' + str(i+1) + '\n')
            f_handle.write(str(i*10)+ ' ' + str((i+1)*10) + '\n')
            f_handle.close()

        join_parallel_files_column([base_file_name], file_num, compress=False)

        f_check =  my_open(base_file_name, 'r')
        for i,line in enumerate(f_check):
            nums = line.split(' ')
            if i == 0:
                pass
            elif i == 1:
                for j in range(0,file_num):
                    self.assert_ (int(nums[j*2]) == j)
                    self.assert_ (int(nums[(j*2) + 1]) == j + 1)
            elif i == 2:
                for j in range(0,file_num):
                    self.assert_ (int(nums[j*2]) == j*10)
                    self.assert_ (int(nums[(j*2) + 1]) == (j + 1)*10)

        f_check.close()
        os.remove(base_file_name)

    def test_save_structures(self):
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp('test_save_structures') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        #THE_PARAM_T.atten_periods = [0.3, 0.5, 0.9]

        attribute_dic={
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-32.5],
            'LONGITUDE':[151.7,151.3,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','UPPER MEREWETHER'],
            'POSTCODE':[2291,2291,2291],
            'PRE1989':[0,1,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,10],
            'BUILDING_COST_DENSITY':[600,1000,10],
            'FLOOR_AREA':[150,300,1],
            'SURVEY_FACTOR':[1,9.8,500],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='HAZUS' # HAZUS usage
            )
        parallel_tag = 'test_output_manager'
        base_file = save_structures(THE_PARAM_T, sites, compress=False,
                parallel_tag=parallel_tag, write_title=True)
        name = base_file + parallel_tag

        # Check the file output
        file_h=open(name, 'r')

        text = file_h.read().splitlines()
        # ditch the comment line
        text.pop(0)

        for i, line in enumerate(text):
            values = array([ix for ix in line.split(' ')])
            self.assert_ (sites.latitude[i] == float(values[0]))
            self.assert_ (sites.longitude[i] == float(values[1]))
            self.assert_ (sites.attributes['PRE1989'][i] == int(values[2]))
            self.assert_ (sites.attributes['POSTCODE'][i] == int(values[3]))
            self.assert_ (sites.attributes['SITE_CLASS'][i] == values[4])
            self.assert_ (sites.attributes['SUBURB'][i] == values[5].replace('_',' '))
            self.assert_ (sites.attributes['SURVEY_FACTOR'][i] == float(values[6]))
            self.assert_ (sites.attributes['STRUCTURE_CLASSIFICATION'][i] == values[7])
            self.assert_ (sites.attributes['HAZUS_STRUCTURE_CLASSIFICATION'][i] == values[8])
            self.assert_ (sites.attributes['BID'][i] == int(values[9]))
            self.assert_ (sites.attributes['FCB_USAGE'][i] == int(values[10]))
            self.assert_ (sites.attributes['HAZUS_USAGE'][i] == values[11])
        file_h.close()

        # clean up
        os.remove(name)
        os.rmdir(THE_PARAM_T.output_dir)

    def test_save_ecloss(self):
        ecloss_name = '_total_building'
        THE_PARAM_T = Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp('test_save_ecloss') + os.sep
        THE_PARAM_T.site_tag = "site_tag"

        ecloss = array([[1, 2, 3, 4], [10, 20, 30, 40]])
        structures = Dummy()
        structures.attributes = {'BID': array([10, 20])}
        parallel_tag = 'yeah'
        name = save_ecloss(ecloss_name, THE_PARAM_T, ecloss, structures, compress=False,
                parallel_tag=parallel_tag)

        # Check the file output
        file_h=open(name + parallel_tag, 'r')

        text = file_h.read().splitlines()
        # ditch the comment line
        text.pop(0)
        bids = text.pop(0)
        for i, bid in enumerate(bids.split(' ')):
            self.assert_ (structures.attributes['BID'][i] == int(bid))
        ecloss = transpose(ecloss)
        for i, line in enumerate(text):
            cost = array([float(ix) for ix in line.split(' ')])
            self.assert_ (allclose(cost, ecloss[i]))
        file_h.close()
        os.remove(name + parallel_tag)
        os.rmdir(THE_PARAM_T.output_dir)

    def test_save_eclossII(self):
        ecloss_name = '_total_building'
        THE_PARAM_T = Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp('test_save_ecloss') + os.sep
        THE_PARAM_T.site_tag = "site_tag"

        ecloss = array([[1, 2, 3, 4], [10, 20, 30, 40]])
        structures = Dummy()
        structures.attributes = {'BID': array([10, 20])}
        name = save_ecloss(ecloss_name, THE_PARAM_T, ecloss, structures,
                           compress=False)

        # Check the file output
        ecloss_loaded, bid = load_ecloss(
            ecloss_name,
            THE_PARAM_T.output_dir, THE_PARAM_T.site_tag)
        self.assert_ (allclose(array(structures.attributes['BID']),bid))
        self.assert_ (allclose(ecloss_loaded, ecloss))

        os.remove(name)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_save_eclossIII(self):
        # testing a one row file
        ecloss_name = '_total_building'
        THE_PARAM_T = Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp('test_save_ecloss') + os.sep
        THE_PARAM_T.site_tag = "site_tag"

        ecloss = array([[1, 2, 3, 4]])
        structures = Dummy()
        structures.attributes = {'BID': array([10])}
        name = save_ecloss(ecloss_name, THE_PARAM_T, ecloss, structures,
                           compress=False)

        # Check the file output
        ecloss_loaded, bid = load_ecloss(
            ecloss_name,
            THE_PARAM_T.output_dir, THE_PARAM_T.site_tag)
        self.assert_ (allclose(array(structures.attributes['BID']),bid))
        self.assert_ (allclose(ecloss_loaded, ecloss))

        os.remove(name)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_lat_long_haz_SA(self):
        THE_PARAM_T=Dummy()
        soil_amp = True
        hazard_name = 'soil_SA'
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_manager_test_load_lat_long_haz_SA') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        lat = array([-32, -31, -30])
        lon = array([120, 121, 122])
        sites = Sites(lat,lon)

        THE_PARAM_T.return_periods = [array([.025]), array([0.5])]
        THE_PARAM_T.atten_periods = [0.3, 0.5]

        hazard = zeros((len(lon),len(THE_PARAM_T.atten_periods),
                        len(THE_PARAM_T.return_periods)), float)
        for i,site_lon in enumerate(lon):
            for j,period in enumerate(THE_PARAM_T.atten_periods):
                for k,rtrn in enumerate(THE_PARAM_T.return_periods):
                    hazard[i,j,k] = site_lon*period #*rtrn[0]
        save_hazard(soil_amp,THE_PARAM_T,
                hazard,sites,compress=False)
        lon_lat_SA = load_lat_long_haz_SA(THE_PARAM_T.output_dir,
                         THE_PARAM_T.site_tag, soil_amp, 0.5, 0.025)
        self.assert_ (allclose(array(lon), array(lon_lat_SA[:,0])))
        self.assert_ (allclose(array(lat), array(lon_lat_SA[:,1])))
        self.assert_ (allclose(array(hazard[:,1,0]),
                               array(lon_lat_SA[:,2])))
        #self.assert_ (allclose(return_p, THE_PARAM_T.return_periods))

        # delete site files
        for i in range(len(THE_PARAM_T.return_periods)):
            rp=THE_PARAM_T.return_periods[i]
            file_name = THE_PARAM_T.output_dir + THE_PARAM_T.site_tag + '_' \
                        + hazard_name + '_rp' + \
                        str(rp).replace('.','pt').replace(' ','') + '.txt'

            os.remove(file_name)
        # remove the locations file that is also produced.
        os.remove(THE_PARAM_T.output_dir+ THE_PARAM_T.site_tag + '_locations.txt')
        os.rmdir(THE_PARAM_T.output_dir)

    def Xtest_load_val(self):
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_manager_test_test_load_val') + os.sep
        THE_PARAM_T.site_tag = 'site_tag'
        file_tag = 'ham'
        val_actual = array([3.4, 3.5, 3.6])
        base_name = save_val(THE_PARAM_T, val_actual, file_tag)
        val = load_val(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                       file_tag=file_tag)
        self.assert_ (allclose(val_actual, val))
        os.remove(base_name)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_structures(self):
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            prefix='test_output_man_test_load_structures') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        attribute_dic={
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-32.5],
            'LONGITUDE':[151.7,151.3,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','UPPER MEREWETHER'],
            'POSTCODE':[2291,2291,2291],
            'PRE1989':[0,1,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,10],
            'BUILDING_COST_DENSITY':[600,1000,10],
            'FLOOR_AREA':[150,300,1],
            'SURVEY_FACTOR':[1,9.8,500],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='HAZUS' # HAZUS usage
            )
        base_file = save_structures(THE_PARAM_T, sites, compress=False,
                                    write_title=True)
        att_dic = load_structures(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag)
        #att_dic['SITE_CLASS'] = ['A','B','c']
        #att_dic['LATITUDE'] = [-32.9,-32.7,-32.7]
        for key in iter(att_dic):
            if not att_dic[key] == attribute_dic[key]:
                self.assert_ (allclose(array(att_dic[key]),
                                       array(attribute_dic[key])))

        # clean up
        os.remove(base_file)
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_ecloss_and_sites(self):
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_manager_test_load_ecloss_and_sites') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        attribute_dic={
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-32.5],
            'LONGITUDE':[151.7,151.3,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','UPPER MEREWETHER'],
            'POSTCODE':[2291,2291,2291],
            'PRE1989':[0,1,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,10],
            'BUILDING_COST_DENSITY':[600,1000,10],
            'FLOOR_AREA':[150,300,1],
            'SURVEY_FACTOR':[1,9.8,500],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='HAZUS' # HAZUS usage
            )
        base_file = save_structures(THE_PARAM_T, sites, compress=False,
                                    write_title=True)
        # dimensions(site, event)
        ecloss = array([[1, 2, 3, 4], [10, 20, 30, 40], [100,200, 300, 400]])
        structures = Dummy()
        structures.attributes = {'BID': array([1, 2, 3])}
        ecloss_name =  '_total_building'
        ecloss_file = save_ecloss(ecloss_name, THE_PARAM_T, ecloss, structures,
                           compress=False)

        val_actual = array([3.4, 3.5, 3.6])
        file_tag = '_bval'
        val_file = save_val(THE_PARAM_T, val_actual, file_tag)
        results = load_ecloss_and_sites(THE_PARAM_T.output_dir,
                                        THE_PARAM_T.site_tag)
        total_building_loss, total_building_value, lon, lat = results

        self.assert_ (allclose(lon, attribute_dic['LONGITUDE']))
        self.assert_ (allclose(lat, attribute_dic['LATITUDE']))
        self.assert_ (allclose(total_building_loss, ecloss))
        self.assert_ (allclose(total_building_value, val_actual))

        # Access denied error in windows
        #shutil.rmtree(THE_PARAM_T.output_dir)

        # Remove a directory and it's contents
        folder = THE_PARAM_T.output_dir
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
        os.rmdir(THE_PARAM_T.output_dir)


    def test_save_bridges(self):
        THE_PARAM_T = Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp('test_save_bridges') + os.sep
        THE_PARAM_T.site_tag = "site_tag"

        attributes = {'BID': [1,2,3],
                      'LATITUDE': [-32.9,-32.7,-32.5],
                      'LONGITUDE': [151.7,151.3,151.3],
                      'STRUCTURE_CLASSIFICATION': ['HWB17','HWB22','HWB17'],
                      'STRUCTURE_CATEGORY': ['BRIDGE', 'BRIDGE', 'BRIDGE'],
                      'SKEW': [0.0,10.0,23.5],
                      'SPAN': [1,3,4],
                      'SITE_CLASS': ['C','G','C']}

        (bridges, _) = get_bridges_from_dic(attributes)
        parallel_tag = 'test_save_bridges'
        base_file = save_bridges(THE_PARAM_T, bridges, compress=False,
                                 parallel_tag=parallel_tag, write_title=True)
        name = base_file + parallel_tag

        # get file output, check against original data
        file_h = open(name, 'r')
        text = file_h.read().splitlines()

        text.pop(0)		# ditch the comment line
        file_h.close()

        for (i, line) in enumerate(text):
            values = line.split(' ')
            (bid, lat, lon, clsf, cat, skew, span, clss) = values

            self.assert_(bridges.attributes['BID'][i] == int(bid))
            self.assert_(bridges.latitude[i] == float(lat))
            self.assert_(bridges.longitude[i] == float(lon))
            self.assert_(bridges.attributes['STRUCTURE_CLASSIFICATION'][i] == clsf)
            self.assert_(bridges.attributes['STRUCTURE_CATEGORY'][i] == cat)
            self.assert_(bridges.attributes['SKEW'][i] == float(skew))
            self.assert_(bridges.attributes['SPAN'][i] == int(span))
            self.assert_(bridges.attributes['SITE_CLASS'][i] == clss)

        # clean up
        os.remove(name)
        os.rmdir(THE_PARAM_T.output_dir)

    def test_load_motion(self):       
        THE_PARAM_T=Dummy()
        soil_amp = False
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_motion_file') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        
        def digital(sp, gmm, site, ev, pd):
            return sp*100 + gmm*10 + site + ev*0.1 + pd*0.01
        # (spawn, gmm, sites, events, periods)
        motion = fromfunction(digital, (2,3,4,5,6))
        base_names = save_motion(soil_amp, THE_PARAM_T, motion)
        SA, periods = load_motion(THE_PARAM_T.output_dir,  THE_PARAM_T.site_tag,
                                  soil_amp)
        
        self.assert_(allclose(array(THE_PARAM_T.atten_periods),
                              periods))
        self.assert_(allclose(SA, motion))
        for name in base_names:
            os.remove(name)
        #print "THE_PARAM_T.output_dir", THE_PARAM_T.output_dir
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_collapsed_motion_sitess(self):      
        THE_PARAM_T=Dummy()
        soil_amp = True
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_motion_file') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.1, 0.2, 0.3, 0.4]
        
        def digital(sp, gmm, site, ev, pd):
            return sp*100 + gmm*10 + site + ev*0.1 + pd*0.01
        # (spawn, gmm, sites, events, periods)
        motion = fromfunction(digital, (1,1,2,3,4))

        lat_actual = array([-32., -31.])
        lon_actual = array([120., 121.])
        sites = Sites(lat_actual,lon_actual)
        base_name = save_sites(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                   sites)
        
        base_names = save_motion(soil_amp, THE_PARAM_T, motion)
        tmp = load_collapsed_motion_sites(THE_PARAM_T.output_dir,
                                          THE_PARAM_T.site_tag,
                                          soil_amp)
        SA, periods, lat, lon = tmp
        self.assert_(allclose(lat, lat_actual))
        self.assert_(allclose(lon, lon_actual))
        #print "SA", SA
        #print "motion[0,0,...]", motion[0,0,...]
        self.assert_(allclose(SA, motion[0,0,...]))
        self.assert_(allclose(array(THE_PARAM_T.atten_periods),
                              periods))

        
        os.remove(base_name)
        for name in base_names:
            #pass
            os.remove(name)
        #print "THE_PARAM_T.output_dir", THE_PARAM_T.output_dir
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_collapsed_motion_sitesII(self):      
        THE_PARAM_T=Dummy()
        soil_amp = True
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_motion_file') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.1]
        
        def digital(sp, gmm, site, ev, pd):
            return sp*100 + gmm*10 + site + ev*0.1 + pd*0.01
        # (spawn, gmm, sites, events, periods)
        motion = fromfunction(digital, (1,2,4,3,1))

        lat_actual = array([-32., -31., -32., -31.])
        lon_actual = array([120., 121., 3., 4.])
        sites = Sites(lat_actual,lon_actual)
        base_name = save_sites(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                   sites)
        
        base_names = save_motion(soil_amp, THE_PARAM_T, motion)
        tmp = load_collapsed_motion_sites(THE_PARAM_T.output_dir,  THE_PARAM_T.site_tag,
                          soil_amp)
        SA, periods, lat, lon = tmp
        self.assert_(allclose(lat, lat_actual))
        self.assert_(allclose(lon, lon_actual))
        #self.assert_(allclose(SA, motion[0,0,...]))
        # (sites, events*gmm*spawn, periods)
        
        for spawn_i in range(motion.shape[0]):
            for gmm_i in range(motion.shape[1]):
                for event_i in range(motion.shape[3]):
                    overload_i = event_i + motion.shape[3]*gmm_i + \
                                  motion.shape[3]* motion.shape[1]*spawn_i
                    self.assert_(allclose(motion[spawn_i, gmm_i, :, event_i, :],
                                          SA[:, overload_i, :]))
        self.assert_(allclose(array(THE_PARAM_T.atten_periods),
                              periods))

        
        os.remove(base_name)
        for name in base_names:
            os.remove(name)
        #print "THE_PARAM_T.output_dir", THE_PARAM_T.output_dir
        os.rmdir(THE_PARAM_T.output_dir)


    def test_load_motion_sites(self):      
        THE_PARAM_T=Dummy()
        soil_amp = True
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_motion_file') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.1, 0.2]
        
        def digital(sp, gmm, site, ev, pd):
            return sp*100 + gmm*10 + site + ev*0.1 + pd*0.01
        # (spawn, gmm, sites, events, periods)
        motion = fromfunction(digital, (1,2,4,3,2))

        lat_actual = array([-32., -31., -32., -31.])
        lon_actual = array([120., 121., 3., 4.])
        sites = Sites(lat_actual,lon_actual)
        base_name = save_sites(THE_PARAM_T.output_dir, THE_PARAM_T.site_tag,
                   sites)
        
        base_names = save_motion(soil_amp, THE_PARAM_T, motion)
        tmp = load_motion_sites(THE_PARAM_T.output_dir,  THE_PARAM_T.site_tag,
                          soil_amp=True, period=0.2)
        SA, lat, lon = tmp
        self.assert_(allclose(lat, lat_actual))
        self.assert_(allclose(lon, lon_actual))
        #self.assert_(allclose(SA, motion[0,0,...]))
        # (sites, events*gmm*spawn, periods)
        
        for spawn_i in range(motion.shape[0]):
            for gmm_i in range(motion.shape[1]):
                for event_i in range(motion.shape[3]):
                    overload_i = event_i + motion.shape[3]*gmm_i + \
                                  motion.shape[3]* motion.shape[1]*spawn_i
                    self.assert_(allclose(motion[spawn_i, gmm_i, :, event_i, 1],
                                          SA[:, overload_i]))

        
        os.remove(base_name)
        for name in base_names:
            os.remove(name)
        #print "THE_PARAM_T.output_dir", THE_PARAM_T.output_dir
        os.rmdir(THE_PARAM_T.output_dir)
        
    def test_load_motion_file(self):
        THE_PARAM_T=Dummy()
        soil_amp = False
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_managertest_load_motion_file') + os.sep
        THE_PARAM_T.site_tag = "site_tag"
        THE_PARAM_T.atten_periods = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        
        def digital(sp, gmm, site, ev, pd):
            return sp*100 + gmm*10 + site + ev*0.1 + pd*0.01
        # (spawn, gmm, sites, events, periods)
        motion = fromfunction(digital, (1,1,5,2,6))
        SA_answer = motion[0, 0, :,1,:]
        base_names = save_motion(soil_amp, THE_PARAM_T, motion)

        ans = load_motion_file(base_names[1]) # 1, so event_index == 1
        SA, periods, event_index, spawn_index, gmm_index = ans
        
        self.assert_(allclose(array(THE_PARAM_T.atten_periods),
                              periods))
        self.assert_(allclose(SA, SA_answer))
        self.assert_(event_index == 1)
        self.assert_(spawn_index == 0)
        self.assert_(gmm_index == 0)
        
        for name in base_names:
            os.remove(name)
        #print "THE_PARAM_T.output_dir", THE_PARAM_T.output_dir
        os.rmdir(THE_PARAM_T.output_dir)
        

    def test_get_days_to_complete_file_name(self):
        site_tag = 'a'
        functional_percentage = 50
        extension = 'b'
        base_name = get_days_to_complete_file_name(
            site_tag, 
            functional_percentage,
            extension)
        self.failUnlessEqual('a_bridge_days_to_complete_rp[50]b',
                             base_name)
        site_tag = 'a'
        functional_percentage = 50.
        extension = 'b'
        base_name = get_days_to_complete_file_name(
            site_tag, 
            functional_percentage,
            extension)
        self.failUnlessEqual('a_bridge_days_to_complete_rp[50]b',
                             base_name)
        
        site_tag = 'a'
        functional_percentage = 50.0
        extension = 'b'
        base_name = get_days_to_complete_file_name(
            site_tag, 
            functional_percentage,
            extension)
        self.failUnlessEqual('a_bridge_days_to_complete_rp[50]b',
                             base_name)
            
        site_tag = 'a'
        functional_percentage = 50.01
        extension = 'b'
        base_name = get_days_to_complete_file_name(
            site_tag, 
            functional_percentage,
            extension)
        self.failUnlessEqual('a_bridge_days_to_complete_rp[50p01]b',
                             base_name)
                             
 
    def test_save_bridge_days_to_complete(self):
        THE_PARAM_T=Dummy()
        THE_PARAM_T.output_dir = tempfile.mkdtemp(
            'output_manager_test_save_bridge_days_to_complete') + os.sep
        THE_PARAM_T.site_tag = "site_tag"

        THE_PARAM_T.bridges_functional_percentages = array(
            [0.0, 0.05, 0.5, 1.0])
            
        sites = array([1,2,3])
        events = array([500, 700])
        d2c = zeros((len(sites),len(events),
                        len(THE_PARAM_T.bridges_functional_percentages)), float)
        #hazard[j,:,i] # sites,rsa_per,rtrn
        for i,site in enumerate(sites):
            for j,event in enumerate(events):
                for k,bfp in enumerate(THE_PARAM_T.bridges_functional_percentages):
                    d2c[i,j,k] = event + site * bfp
        base_names = save_bridge_days_to_complete(THE_PARAM_T, d2c, 
                                                  compress=False)
                                                  
        # check the site files
        for bfp in THE_PARAM_T.bridges_functional_percentages:
           file_name = get_days_to_complete_file_name(THE_PARAM_T.site_tag, 
                                                      bfp)
           file_name = os.path.join(THE_PARAM_T.output_dir, file_name)
           f = open(file_name, 'r')
           text = f.read().splitlines()
            # ditch the comment lines
           text.pop(0)
           text.pop(0)
           
           for j, site in enumerate(sites):
               split = text[j].split(', ')
               for k, event in enumerate(events):
                    #hazard[i,j,k] = site*period*int(rtrn[0])
                   self.assert_ (allclose(array(float(split[k])),
                                          array(float(event + site * bfp))))
                   f.close()
           os.remove(file_name)
        os.rmdir(THE_PARAM_T.output_dir)
                            
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Output_manager, 'test')
    #suite=unittest.makeSuite(Test_Output_manager,'test_load_collapsed_motion_sitess')
    #suite=unittest.makeSuite(Test_Output_manager,'test_save_event_set_new')
    runner = unittest.TextTestRunner() #verbosity=2) #verbosity=2
    runner.run(suite)

