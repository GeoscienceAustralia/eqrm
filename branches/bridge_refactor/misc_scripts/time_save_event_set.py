
import os
from scipy import ones, array
import time
import tempfile

from eqrm_code.event_set import Event_Set
from eqrm_code.output_manager import save_event_set

class Dummy:
    def __init__(self):
        pass
    
def event_create(event_c):
    trace_start_lat = ones((event_c))* -38.15
    trace_start_lon = ones((event_c))* 146.5
   
    azimuth = ones((event_c))* 217.2
    dip = ones((event_c))* 60.2
    weight = ones((event_c))* 18.1
    event_activity = ones((event_c))* 0.1
    recurrence = ones((event_c))* 5.3
    
    Mw = ones((event_c))* 6.9
    lat0 = ones((event_c))* -38.31
    lon0 = ones((event_c))* 146.3
    
    depth = ones((event_c))* 6.5
    rx = ones((event_c))* 25.3
    ry = ones((event_c))* 3.8
    
    length = ones((event_c))* 50.6
    width = ones((event_c))* 15.
    event_activity = ones((event_c))* 9.

    event_set = Event_Set.create(depth=depth,rupture_centroid_lat=lat0,
                        rupture_centroid_lon=lon0,azimuth=azimuth,
                        dip=dip,ML=None,Mw=Mw,fault_width=15.0)
    event_set.event_activity =  ones((event_c))* 0.8
    pseudo_event_set = Pseudo_Event_Set.split_logic_tree(event_set,
                                                         ['Gaull_1990_WA'],
                                                         [1])
    pseudo_event_set.source_zone_id =  ones((event_c))* 9.
    return pseudo_event_set, event_activity
    # let's design

    # Need to time event_sets being saved, with variable # of events

def main_loop():
    event_counts = [1e1, 1e2, 1e3, 1e4, 1e5] #, 1e6]

    # Create temp dir
    
    THE_PARAM_T=Dummy()      
    THE_PARAM_T.output_dir = tempfile.mkdtemp(
        'output_managertest_load_event_set') + os.sep
    THE_PARAM_T.site_tag = "site_tag"

    print "enents","time - sec"
    for event_c in event_counts:
        event_set, event_activity = event_create(event_c)
        event_activity = array([1])
        t0 = time.clock()
        file_full_name = save_event_set(THE_PARAM_T, event_set, event_activity)
        time_taken = (time.clock()-t0)
        print event_c, time_taken
        os.remove(file_full_name)
        
    os.rmdir(THE_PARAM_T.output_dir)

#-------------------------------------------------------------
if __name__ == "__main__":
    main_loop()
