function [lats, lons, SiteLocations, AllLocations, ...
    region_box, site_classes, inside1] = ...
    Convert_Py2Mat_SiteUniform(filein,dirout,site_loc)
% function to convert a Python *site_uniform.csv (e.g.
% perth_par_site_uniform.csv) to the Matlab 
% *site_uniform.mat file (e.g. perth_par_site_uniform.mat).
%
% Inputs: 
% filein        [string] full path to *site_uniform.csv
% dirout        [string] directory to store the *site_uniform.mat
% site_loc      [string] site location prefex for use with output file. 
%
% Outputs
% There are no outputs displayed to screen. An output file is saved in
% dirout which contains the following parameters
%       AllLocations     (e.g. 2500x2)  double array
%       SiteLocations    (e.g. 2044x2)  double array
%       inside1          (e.g. 2500x1)  logical array
%       lats             (e.g. 1x50)    double array
%       lons             (e.g. 1x50)    double array
%       region_box       (e.g. 280x2)   double array
%       site_class_polys (e.g. 1x72)    struct array
%       site_classes     (e.g. 10000x1) cell array  
%                        [Note that this differs from the
%                        Matlab version which uses a char
%                        array for site_classes]
% David Robinson
% 5/4/20076

%fid = fopen(filein)
fstr_beg = ''; %repmat(fstr0, 1, 9);
fstr_end = '%*[^\n]';
fstr = [fstr_beg,'%f%f%s',fstr_end];
[lats_in, lons_in, site_classes] =  ...
    textread(filein, fstr, 'delimiter', ',', 'headerlines', 1, 'emptyvalue', NaN);
%fclose(fid)

lats = sort(unique(lats_in));
lons = sort(unique(lons_in));
SiteLocations = [lons_in, lats_in]; 

AllLocations = [];
for i = 1: length(lons)
    AllLocations = [AllLocations; lons(i)*ones(length(lats),1), lats];    
end

region_box = [min(lons), min(lats); max(lons), min(lats); max(lons), max(lats); min(lons), max(lats); min(lons), min(lats)];

inside1 = zeros(size(AllLocations,1),1);
inside1 = logical(inside1); 
for i = 1:size(AllLocations,1)
    ind = find(AllLocations(i,1) == SiteLocations(:,1) & AllLocations(i,2) == SiteLocations(:,2));
    if ~isempty(ind) & length(ind) ==1
        inside1(ind) = 1;
    elseif isempty(ind) 
        % no need to do anything because the values are already 0
    else
        error(' we should not be here')
    end
end

site_class_polys = [];


save([site_loc, '_par_site_uniform.mat'], 'AllLocations','SiteLocations','inside1', ...
    'lats','lons','region_box','site_class_polys','site_classes')
