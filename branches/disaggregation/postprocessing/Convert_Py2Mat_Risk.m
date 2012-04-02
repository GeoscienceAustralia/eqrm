function [] = Convert_Py2Mat_Risk(datadir,param_fname, default_data)
% Converts  outputs from python version of the EQRM into the same 
% format as those from the matlab version of the EQRM. That way 
% all of the matlab postprocessing routines can be use. Note that this
% routine can be used to convert either scenario or probabilistic results.
% Note that if it is a scenario run then r_nu is defined as 1. 
%
% INPUTS:
% datadir       [string] full path to directory containing the hazard file
%               outputs from the EQRM. Note that this should be consistent with 
%               THE_PARAM_T.savedir
% param_fname   [string] name of THE_PARAM_T file
% default_data  [string] full path to location of default data 
%                   e.g. *\python_eqrm\resources\data
%
% OUTPUTS: 
% Converted data are saved as ...... 
%
% NOTES: - currently the rupture distance is not converted to MATLAB
% because all of teh MATLAB postprocessing routines use Joyner-Boore
% distance. 
%
% David Robinson
% 13 April 2007
%
% Notes on formats:
%       ns = number of sites/buildings
%       ne = number of events
%       
%   PYTHON: 
%       -   newc_bval.txt:              (ns x1) building value data (after
%                                        application of survey factor)
%       -   newc_distance_rjb.txt:      (ne x ns) Joyner-Boore distance 
%       -   newc_distance_rup.txt       (ne x ns) Rupture distance
%       -   THE_PARAM_T.txt             copy of input parameter file
%       -   newc_bedrock_event_mag.txt  (ne x 2) 
%                                           col 1 =>    event magnitudes
%                                                       (identical for scenario)
%                                           col 2 =>    event activities 
%                                                       (1 if scenario)
%       -   newc_structures.txt         (ns x )
%                                            col1 => LATITUDE
%                                            col2 => LONGITUDE
%                                            col3=> PRE1989
%                                            col4 => POSTCODE
%                                            col5 => SITE_CLASS
%                                            col6 => SUBURB
%                                            col7 => SURVEY_FACTOR
%                                            col8 => STRUCTURE_CLASSIFICATION
%                                            col9 => HAZUS_STRUCTURE_CLASSIFICATION
%                                            col10 => BID
%                                            col11 => FCB_USAGE HAZUS_USAGE
%       -   newctotal_building_loss.txt  (ne x ns) estimated loss after
%                                           application of survey factor
%
%   Matlab:
%       aus_mag         (nex1) double array
%       b_post89        (nsx1) double array
%       b_postcode      (nsx1) double array
%       b_siteid        (nsx1) double array
%       b_sub           (nsx1) double array
%       b_survfact      (nsx1) double array
%       b_type          (nsx1) double array
%       b_ufi           (nsx1) double array
%       b_use           (nsx1) double array
%       nu              (nex1) double array
%       saved_ecbval2   (nsx1) double array
%       saved_ecloss    (nexns) single array
%       saved_rjb       (nexns)single array%
%
% David Robinson
% 13 April 2007

% we move to the directory where data is stored 
currentdir = pwd;  % keep a record from where we started 
cd(datadir)  % move to datadir


if nargin ==2
    default_data = 'Z:\1\cit\natural_hazard_impacts\earthquake\sandpits\drobinson\ExternalRepos\python_eqrm\resources\data';
end


% Convert the python THE_PARAM_T to matlab version
THE_PARAM_T = Convert_Py2Mat_PARAM_T([datadir,filesep,param_fname]);
eqrm_param_T = THE_PARAM_T;
save([datadir,'/matlab_setdata.mat'],'eqrm_param_T')


% let's do all of the easy stuff first
saved_ecbval2 = load([THE_PARAM_T.site_loc,'_bval.txt']);
saved_rjb = single(load([THE_PARAM_T.site_loc,'_distance_rjb.txt']));

% Now do the loss values
if THE_PARAM_T.save_ecloss_flag ==1  % contents and building loss combined in single file
    tmp_saved_ecloss = single(load([THE_PARAM_T.site_loc,'_total_building_loss.txt']));
elseif THE_PARAM_T.save_ecloss_flag ==2 % contents separate from building loss - consider only building loss
    tmp_saved_ecloss = single(load([THE_PARAM_T.site_loc,'building_loss.txt']));
    disp('WARNING: You have chosen to save contents and building loss separately')
    disp('         In this case only building loss is considered in Convert_Py2mat_Risk')
else
    error('Invalid value for THE_PARAM_T.save_ecloss_flag in Convert_Py2Mat_Risk')
end
    saved_ecloss = tmp_saved_ecloss(2:end,:);

tmp1 = load([THE_PARAM_T.site_loc,'_event_set.txt']);
aus_mag = tmp1(:,10);
nu = tmp1(:,9);

% Now let's read in the structure information
% fid = fopen([THE_PARAM_T.site_loc,'_structures.txt'])
[b_lat, b_lon, b_post89, b_postcode, b_soil, str_suburb, ...
    b_survfact, str_btype, str_haztype,b_ufi, fcb_usage, hazus_usage] = textread([THE_PARAM_T.site_loc,'_structures.txt'], ...
'%f %f %f %f %s %s %f %s %s %f %f %s', -1,'headerlines',1);
% fclose(fid)

% Replace the underscores separating multiple names of a suburb with
% spaces
for i = 1: length(str_suburb)
    ind = strfind(str_suburb{i},'_');
    str_suburb{i}(ind) = ' ';
end

% convert btypes to indexes for lookup
% note that this files contains lookups for both HAZUS and extended
% HAZUS btypes
fid = fopen([default_data,'\textbtypes.txt']);
btypelookup = textscan(fid, '%s',-1);
fclose(fid);
b_type=-9999*ones(length(str_btype),1);
for i = 1: length(btypelookup{1})
    TF = strcmp(str_btype, btypelookup{1}{i});
    b_type(TF) = i;
end

% convert buses for index lookup. 
if THE_PARAM_T. b_usage_type_flag ==1 % Then we use HAZUS building types
    fid = fopen([default_data,'\textbuses.txt']);
    buselookup = textscan(fid, '%s',-1);
    fclose(fid);
    b_use=-9999*ones(length(hazus_usage),1);
    for i = 1: length(buselookup{1})
        TF = strcmp(hazus_usage, buselookup{1}{i});
        b_use(TF) = i;
    end   
elseif THE_PARAM_T. b_usage_type_flag ==2 % Then we are using the FCB usage types
    buselookup = load([default_data,'\textbusageFCB.txt']);
    b_use=-9999*ones(length(fcb_usage),1);
    for i =1:length(buselookup)
        ind = find(fcb_usage == buselookup(i));
        b_use(ind) = i;
    end
end

% Convert suburb to index lookup
fid = fopen([default_data,'\suburb_postcode.csv']);
tmp101= textscan(fid, '%s %f %f %s',-1,'headerlines',1, 'delimiter',',');
SUBURBlookup = tmp101{1};
postcodelookup = tmp101{2};
idlookup = tmp101{3};
LGAlookup = tmp101{4};
fclose(fid);
b_sub=-9999*ones(length(str_suburb),1);
for i = 1: length(SUBURBlookup)
    TF = strcmp(str_suburb, SUBURBlookup{i});
    b_sub(TF) = idlookup(i);
end

b_siteid = b_ufi;
%b_ufi = b_siteid;

save([THE_PARAM_T.site_loc,'_db_savedecloss.mat'], 'aus_mag','b_post89','b_postcode','b_siteid', ...
        'b_sub','b_survfact', 'b_type', 'b_ufi', 'b_use', ...           
        'nu', 'saved_ecbval2', 'saved_ecloss','saved_rjb');




cd(currentdir)  % return user to where the started.



