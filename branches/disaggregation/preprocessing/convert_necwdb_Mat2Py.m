function [] = convert_necwdb_Mat2Py(filein,folderout)
% This function converts the Newcastle site database from the
% sitedb_newc.mat format used in teh Matlab version of teh EQRM to the new
% format sitedb_newc.csv used in the Python version of the EQRM 
%
% INPUTS:
% filein        full path to sitedb_newc.mat
% folderout     full path to directory in which to save sitedb_newc.csv
%
% David Robinson 
% 2 April 2007
%
% NOTES: 
% STRUCTURE_CATAGORY = Building or Bridge

% Read in the FCB_USAGE_LOOKUP
FCB_USAGE_LOOKUP = load(['..',filesep,'resources', filesep,'data',filesep,'textbusageFCB.txt']);  % these are numbers so we can load

% Read in a Building Classification LOOKUP - note that lookup contains expanded and HAZUS classification 
fid = fopen(['..',filesep,'resources', filesep,'data',filesep,'textbtypes.txt']);  % These are text so we can just load them 
BUILDING_CLASSIFICATION_LOOKUP = textscan(fid, '%s');
fclose(fid);

% Read in a HAZUS USAGE LOOKUP
fid = fopen(['..',filesep,'resources', filesep,'data',filesep,'textbuses.txt']);  % These are text so we can just load them 
HAZUS_USAGE_LOOKUP = textscan(fid, '%s');
fclose(fid);



load(filein)
% Loads:
%   all_postcodes     208x1                      1664  double array
%   all_suburbs       208x1                     16410  cell array
%   b_sitemat        6305x15                   756600  double array
%  b_soil           6305x1                    390910  cell array

fid = fopen([folderout, filesep,'sitedb_newc.csv'],'w' );

% write the header
fprintf(fid, ['BID,LATITUDE,LONGITUDE,STRUCTURE_CLASSIFICATION,',...
            'STRUCTURE_CATAGORY,HAZUS_USAGE,SUBURB,POSTCODE,', ...
            'PRE1989,HAZUS_STRUCTURE_CLASSIFICATION,CONTENTS_COST_DENSITY,', ...
            'BUILDING_COST_DENSITY,FLOOR_AREA,SURVEY_FACTOR,FCB_USAGE,SITE_CLASS \n']);
for i = 1:length(b_soil);
    fprintf(fid, '%s,',num2str(b_sitemat(i,1)));  % print the building ID
    fprintf(fid, '%s,',num2str(b_sitemat(i,2))); % print the latitude
    fprintf(fid, '%s, ',num2str(b_sitemat(i,3))); % print the longitude
    fprintf(fid, '%s, ',num2str(BUILDING_CLASSIFICATION_LOOKUP{1}{b_sitemat(i,4)}));% print the STRUCTURE_CLASSIFICATION
    fprintf(fid, '%s, ','BUILDING'); % print the STRUCTURE_CATAGORY
    fprintf(fid, '%s, ',num2str(HAZUS_USAGE_LOOKUP{1}{b_sitemat(i,5)})); % print the HAZUS_USAGE
    fprintf(fid, '%s, ',all_suburbs{b_sitemat(i,8)}); % print the SUBURB
    fprintf(fid, '%s, ',num2str(b_sitemat(i,9))); % print the POSTCODE  
    fprintf(fid, '%s, ',num2str(b_sitemat(i,11))); % print the PRE1989 flag (1 means it existed before 1989 - 0 after)
    fprintf(fid, '%s, ',num2str(BUILDING_CLASSIFICATION_LOOKUP{1}{b_sitemat(i,12)})); % print the HAZUS_STRUCTURE_CLASSIFICATION  
    fprintf(fid, '%s, ',num2str(b_sitemat(i,14))); % print the CONTENTS_COST_DENSITY
    fprintf(fid, '%s, ',num2str(b_sitemat(i,13))); % print the BUILDING_COST_DENSITY
    fprintf(fid, '%s, ',num2str(b_sitemat(i,6))); % print the FLOOR_AREA (summed over all stories - square meters)
    fprintf(fid, '%s, ',num2str(b_sitemat(i,7))); % print the SURVEY_FACTOR
    fprintf(fid, '%s, ',num2str(FCB_USAGE_LOOKUP(b_sitemat(i,15)))); % print the FCB_USAGE
    fprintf(fid, '%s, \n',b_soil{i}); % print the SITE_CLASS

end

fclose(fid);
