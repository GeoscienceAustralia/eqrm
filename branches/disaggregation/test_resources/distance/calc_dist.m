function [] = calc_dist(lat_sites, lon_sites, lat_events, lon_events, lengths,
                       azimuths, widths, dips, depths, projection,
                       trace_start_lat, trace_start_lon, trace_start_x,
                       trace_start_y)
% A function to calculate the distances 
%     m = number of sites
%     n = number of earthquakes
% 
% INPUT: 
% lat_sites  [mx1] Latitude of the m sites (degrees)
% lon_sites  [mx1] Longitude of the m sites  (degrees)
% lat_events [nx1] Latitude of the centroid for the n events (degrees)???????
% lon_events [nx1] Longitude of the centroid for the n events (degrees) ???????
% lengths    [nx1] Length of the n synthetic events (km) 
% azimuths   [nx1] Azimuth for the n synthetic events (degrees)
% widths     [nx1] Widths of the n synthetic events (km)
% dips       [nx1] Dips for the n synthetic events (degrees) 
% depths     [nx1] depth to centroid for each event (km)
% trace_start_lat [nx1] latitude to the start of the rupture trace (degrees)
% trace_start_lon [nx1] latitude to the start of the rupture trace (degrees)
% ???centroid_x [nx1] x distance to the centroid (km from a start trace centered origin)
% ???centroid_y [nx1] y distance to the centroid (km from a start trace centered origin) 
%
% VARIABLES NOT USED: 
%       projection
%       trace_start_x ???????
%       trace_start_y ???????
%
% OUTPUTS: 
% Rjb [nxm]  Joyner Boore distances from all sites to all events
% Rrup [nxm] Rupture distances from all sites to all events
% Rx  [nxm] = horizontal distance between all sites and all events
%

%%% Data from Vanessa
%lat_sites        lat of the sites -9
%lon_sites        lon of sites     109
%lat_events       lat of the centroid of the rupture (synthetic event) -9.74984294
%lon_events       lon of the centroid of the rupture (synthetic event) 110.13706532
%lengths         length of the rupture (synthetic event)   55.59746332
%azimuths         azimuth of the rupture (synthetic event)  0
%widths           width of the rupture (synthetic event)   14.14213562
%dips            dip of the rupture (synthetic event)   45
%depths          depth of the centroid of the rupture (synthetic event) 15
%projection       not used by Joyner_Boore
%trace_start_lat  lat of the start of the trace of the rupture (syn event) -10
%trace_start_lon  lon of the start of the trace of the rupture (syn event) 110.00010413
%trace_start_x    x of the start of the trace of the rupt assuming centroid is origin -27.79873166
%trace_start_y    x of the start of the trace of the rupt assuming centroid is origin -15

%the resulting dist using the above parameters is:
%132.01436128

DeltaDepth = (width./2).*sin(dips);
Depth2Top = depths - DeltaDepth; 
yhalf = depths./tan(dips);  
xcent = lengths./2;




