import os
import sys
from random import uniform,seed
from time import time
import unittest
from os import sep
import types
import tempfile

from scipy import array, allclose, asarray, arange, sum

#from xml_interface import Xml_Interface
#from source_model import source_model_from_xml
#import conversions

from eqrm_code.event_set import * #Event_Set, Pseudo_Event_Set
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle




def test_generate_synthetic_events_fault():
        def dump_src(etc):
            """Helper function to dump info from SRC object."""

            for attr in dir(src):
                if attr[0] != '_': # and attr != 'name_type_map':
                    val = eval('src.%s' % attr)
                    if isinstance(val, dict):
                        print('    %s=%s' % (attr, str(val)))
                    elif isinstance(val, types.MethodType):
                        pass
                    else:
                        print('    %s=%s (%s)' % (attr, str(val), type(val)))

        # create a test FSG file
        (handle, fault_xml_file) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(fault_xml_file,'w')
        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<source_model_fault magnitude_type="Mw">',
                            '  <fault name="big fault" event_type="crustal fault">',
                            '    <geometry dip="80" out_of_dip_theta="0"',
                            '              delta_theta="0"',
                            '              depth_top_seismogenic="10"',
                            '              depth_bottom_seismogenic="50"',
                            '              slab_width="0">',
                            '      <trace>',
                            '        <start lat="-17.0" lon="110.0" />',
                            '        <end lat="-17.0" lon="111.0" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="bounded_gutenberg_richter"',
                            '                      recurrence_min_mag="4.0"',
                            '                      recurrence_max_mag="7.8"',
                            '                      slip_rate="2.0" b="1">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="1500" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '</source_model_fault>'])
        handle.write(sample)
        handle.close()

        # create a test ETC file
        (handle, event_control_file) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(event_control_file, 'w')
        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "normal">'
                            '      <branch model = "Toro_1997_midcontinent" weight = "0.3"/>'
                            '      <branch model = "Atkinson_Boore_97" weight = "0.4"/>'
                            '      <branch model = "Sadigh_97" weight = "0.3"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "WellsCoppersmith94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '  <event_group event_type = "crustal fault">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Campbell08" weight = "0.8"/>'
                            '      <branch model = "Boore08" weight = "0.2"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "WellsCoppersmith94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "interface">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_crustalinterface" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_interface" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "WellsCoppersmith94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "intraslab">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "WellsCoppersmith94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])
        handle.write(sample)
        handle.close()

        prob_min_mag_cutoff = 4.0

        prob_number_of_events_in_faults =[100]
        (event_set_fault, source_mod_fault) = generate_synthetic_events_fault(fault_xml_file,
                                                  event_control_file,
                                                  prob_min_mag_cutoff,
                                                  prob_number_of_events_in_faults)

        return event_set_fault                                           
                                                
if __name__ == "__main__":
    event_set_fault = test_generate_synthetic_events_fault()

    mag=event_set_fault.Mw
    area=event_set_fault.area
    width=event_set_fault.width
    length=event_set_fault.length
    depth=event_set_fault.depth
    r_lat=event_set_fault.rupture_centroid_lat
    r_lon=event_set_fault.rupture_centroid_lon
    r_x=event_set_fault.rupture_x
    s_lon=event_set_fault.trace_start_lon
    e_lon=event_set_fault.trace_end_lon
    
    
plt.figure()
plt.plot(mag,area,'ro')
plt.savefig('mag_vs_area.png')

plt.figure()
plt.hist(mag,30)
plt.savefig('mag_hist.png')

plt.figure()
plt.plot(mag,width,'ro')
plt.savefig('mag_vs_width.png')
   
plt.figure()
plt.plot(mag,length,'ro')
plt.savefig('mag_vs_length.png')   

plt.figure()
plt.scatter(mag,depth,s=mag**2,c=mag)
plt.plot(mag,width/2.*sin(math.radians(10.))+10.,'g.')
plt.plot(mag,50-width/2.*sin(math.radians(10.)),'b.')
plt.xlabel('Magnitude')
plt.ylabel('Depth')
plt.ylim(plt.ylim()[::-1])
plt.savefig('mag_vs_depth.png')   

plt.figure()
plt.scatter(length/width,area,c=mag,s=mag**3)
plt.savefig('width_vs_length.png')   

plt.figure()
plt.scatter(area,depth,c=mag)
plt.savefig('area_depth_mag.png') 
  
plt.figure()
plt.scatter(r_lon,r_lat,s=mag**2,c=mag)
plt.xlim([109,112])
plt.ylim([-19,-16])
#plt.ylim(plt.ylim()[::-1])
plt.savefig('depth_locn.png') 

plt.figure()
plt.scatter(r_lat,depth,s=mag**2,c=mag)
plt.ylim(plt.ylim()[::-1])
plt.xlabel('Latitude')
plt.ylabel('Depth')
plt.savefig('depth_lat.png') 

plt.figure()
plt.scatter(r_lon,depth,s=mag**2,c=mag)
plt.ylim(plt.ylim()[::-1])
plt.xlabel('Longitude')
plt.ylabel('Depth')
plt.savefig('depth_lon.png') 

plt.figure()
for i in xrange(len(mag)):
    
    if mag[i] > 4 and mag[i] < 5:
        col='blue'
    elif mag[i] >= 5 and mag[i] < 6:
        col='yellow'
    elif mag[i] >= 6 and mag[i] < 7:
        col='orange'
    elif mag[i] >= 7:
        col='red'

#    x1=r_lon[i] - ((length[i]/2) / 106.)
#    x2=r_lon[i] + ((length[i]/2) / 106.)
    x1=s_lon[i]
    x2=e_lon[i]
    y1=depth[i] - (width[i]/2)
    y2=depth[i] + (width[i]/2)

    x=[x1,x1,x2,x2,x1]
    y=[y1,y2,y2,y1,y1]
    plt.plot(x,y,c=col)
#plt.scatter(r_lon,depth, c=mag,s=mag**2)
plt.ylim(plt.ylim()[::-1])
plt.savefig('depth_lon_boxes.png')
