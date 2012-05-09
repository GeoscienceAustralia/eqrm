function [THE_PARAM_T,dist_jb, dist_rup, periods, rock_motions, soil_motions, site_pos] = ...
                    Convert_Py2Mat_ScenGroundMot(datadir,param_fname)
% Converts  outputs from python version of the EQRM (for ground motion scenario) 
% into the same  format as those from the matlab version of the EQRM. That way 
% all of the matlab postprocessing routines can be use.
%
% Note that this routine will currently convert results from the first
% event copy. That is, if the event is copied for the purpose of sampling
% then only the first copy will be loaded
%
% INPUTS:
% datadir       [string] full path to directory containing the hazard file
%               outputs from the EQRM. Note that this should be consistent with 
%               THE_PARAM_T.savedir
% param_fname   [string] name of THE_PARAM_T file
%
% OUTPUTS: 
% Converted data are saved as ...... 
%
% Davis Robinson
% 10 April 2007
%
% Notes on formats:
%
%   PYTHON: 
%       -   Site locations are printed in lat & long file
%       -   Hazard data are saved in multiple files. There is one file for
%           each return period. Regolith and bedrock are saved separately.

%       - <site_loc>_bedrock_event_mag.txt:     contains the event magnitude
%       - <site_loc>_locations.txt:             lats and long for sites               
%       - <site_loc>_distance_rjb.txt:          JB distances
%       - <site_loc>_distance_rup.txt:          Rupture distances
%       - THE_PARAM_T.txt:                      Python version of setdata file
%       - <site_loc>_SA_motion_0.txt:           Bedrock Motion (sites in rows - periods in columns)                
%       - <site_loc>soil_SA_motion_0.txt        Regolith Motion (sites in rows - periods in columns) 
%
%           
%   Matlab:
%       - THE_PARAM_T: as a Matlab structure
%       - dist_jb  [vector 1xns] JB distance between each site and the event 
%       - dist_rup [vector] Rupture distance between each site and the event 
%       - periods [1xnp] RSA periods
%       - rock_motions   [single array 1xnsxnp]      
%       - soil_motions   [single array 1xnsxnp]      
%       - site_pos       [ns x 2] with longitude in column 1 and latitude column 2
%
% David Robinson
% 11 April 2007


% we move to the directory where data is stored 
currentdir = pwd;  % keep a record from where we started 
cd(datadir)  % move to datadir

% Convert the python THE_PARAM_T to matlab version
THE_PARAM_T = Convert_Py2Mat_PARAM_T([datadir,filesep,param_fname]);

% define what we can now
periods = THE_PARAM_T.periods;

% Load the site data
tmp = load([THE_PARAM_T.site_loc,'_locations.txt']);
site_pos = [tmp(:,2), tmp(:,1)];  % flip order of latitude and longitude. 

% read in the ground motion matrices
tmp_rock_motions = dlmread([THE_PARAM_T.site_loc,'_bedrock_SA_motion_0.txt'], ' ', 3, 0);  % Note we start at row 3 to ignore 2 rows of header and 1 row containg the periods
rock_motions = reshape(tmp_rock_motions,1,length(site_pos(:,1)), length(periods));
if THE_PARAM_T.amp_switch ==1
    tmp_soil_motions = dlmread([THE_PARAM_T.site_loc,'_soil_SA_motion_0.txt'], ' ', 3, 0);  % Note we start at row 3 to ignore 2 rows of header and 1 row containg the periods
    soil_motions = reshape(tmp_soil_motions,1,length(site_pos(:,1)), length(periods));
else
    soil_motions = rock_motions;   % copy the rock_motions if amplitude not taken. 
end

dist_jb = load([THE_PARAM_T.site_loc,'_distance_rjb.txt']);

dist_rup = load([THE_PARAM_T.site_loc,'_distance_rup.txt']);

save([THE_PARAM_T.site_loc,'_db_mot.mat'], 'THE_PARAM_T','dist_jb', 'dist_rup', 'periods', 'rock_motions', 'soil_motions', 'site_pos')

cd(currentdir)%