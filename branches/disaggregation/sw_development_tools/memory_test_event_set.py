
"""
"""

import os
import sys
import tempfile
from os import sep

from scipy import array

from eqrm_code.event_set import Event_Set
from eqrm_code.ANUGA_utilities import log as eqrmlog

def create_event_set(event_num):        
        """
        Create an event set to investigate memory size.
        """
        
        fault_width = 5
        azi = array([90])
        dazi = array([2])
        fault_dip = array([35.0])
        prob_min_mag_cutoff = 1.0
        override_xml = True
        prob_number_of_events_in_zones = [event_num]
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        # I don't know what this is A_min="1.0"
        # But I added it so the tests would pass
        # Another example file at
        # Q:\python_eqrm\implementation_tests\input\newc_source_polygon.xml
        #  polygon is a small square

        
        sample = """<Source_Model magnitude_type='Mw'>
<polygon area="5054.035">
  <boundary>-32.000 151.00 -32.0 151.05 -32.05 151.05 -32.05 151.0</boundary> 
  <recurrence distribution="bounded_gutenberg_richter" min_magnitude="3.3" max_magnitude="5.4" A_min="0.568" b="1" min_mag="4.5" depth="7" /> 
  </polygon>

</Source_Model>
"""
        handle.write(sample)
        handle.close()
        
        #file_name = os.path.join('..','implementation_tests','input','newc_source_polygon.xml')
        #return
        # need to fix
        events = Event_Set.generate_synthetic_events(
            file_name,
            fault_width,
            azi,
            dazi,
            fault_dip,
            prob_min_mag_cutoff,
            override_xml,
            prob_number_of_events_in_zones)
#        print "events.trace_start_lat", events.trace_start_lat
#         print " events.trace_start_lon", events.trace_start_lon
#         print "events.trace_end_lat", events.trace_end_lat
#         print "events.trace_end_lon", events.trace_end_lon
#         print "events.rupture_centroid_lat", events.rupture_centroid_lat
#         print "events.rupture_centroid_lon", events.rupture_centroid_lon
#         print "events.rupture_centroid_x", events.rupture_centroid_x
#         print "events.rupture_centroid_y", events.rupture_centroid_y

        os.remove(file_name)

                                                     
#-------------------------------------------------------------
if __name__ == "__main__":
    event_num = 100000
    eqrmlog.console_logging_level = eqrmlog.INFO
    eqrmlog.info('Memory: before creating ' + str(event_num) + ' events')
    eqrmlog.resource_usage(level=eqrmlog.INFO)
    create_event_set(event_num)
    eqrmlog.info('Memory: after')
    eqrmlog.resource_usage(level=eqrmlog.INFO)
