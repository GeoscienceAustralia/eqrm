"""
event_set_data.py
A class to hold temporary data used when creating event sets
"""

from eqrm_code import file_store

class Event_Set_Data(file_store.File_Store):
    
    def __init__(self, dir=None):
        super(Event_Set_Data, self).__init__('event_set_data', dir)

    def __del__(self):
        super(Event_Set_Data, self).__del__()
    
    
    # PROPERTIES #
    # Define getters and setters for each attribute to exercise the 
    # file-based data structure
    num_events = property(lambda self: self._get_file_array('num_events'), 
                          lambda self, value: self._set_file_array('num_events', value))
    
    rupture_centroid_lat = property(lambda self: self._get_file_array('rupture_centroid_lat'), 
                                    lambda self, value: self._set_file_array('rupture_centroid_lat', value))
    
    rupture_centroid_lon = property(lambda self: self._get_file_array('rupture_centroid_lon'), 
                                    lambda self, value: self._set_file_array('rupture_centroid_lon', value))
    
    depth_top_seismogenic = property(lambda self: self._get_file_array('depth_top_seismogenic'), 
                                     lambda self, value: self._set_file_array('depth_top_seismogenic', value))
    
    depth_bottom_seismogenic = property(lambda self: self._get_file_array('depth_bottom_seismogenic'), 
                                        lambda self, value: self._set_file_array('depth_bottom_seismogenic', value))
    
    azimuth = property(lambda self: self._get_file_array('azimuth'), 
                       lambda self, value: self._set_file_array('azimuth', value))
    
    dip = property(lambda self: self._get_file_array('dip'), 
                   lambda self, value: self._set_file_array('dip', value))
    
    area = property(lambda self: self._get_file_array('area'), 
                    lambda self, value: self._set_file_array('area', value))
    
    width = property(lambda self: self._get_file_array('width'),
                     lambda self, value: self._set_file_array('width', value))
    
    fault_width = property(lambda self: self._get_file_array('fault_width'), 
                           lambda self, value: self._set_file_array('fault_width', value))
    
    magnitude = property(lambda self: self._get_file_array('magnitude'),
                         lambda self, value: self._set_file_array('magnitude', value))


class Event_Activity_Data(file_store.File_Store):

    def __init__(self, dir=None):
        super(Event_Activity_Data, self).__init__('event_activity_data', dir)

    def __del__(self):
        super(Event_Activity_Data, self).__del__()
        
    new_event_activity = property(lambda self: self._get_file_array('new_event_activity'), 
                                  lambda self, value: self._set_file_array('new_event_activity', value))