function sites_to_csv(SiteLocations,site_classes,csv_name)

% function evntdb_to_xml(evntdb_name,xml_name)
%
% eg inputs
% SiteLocations = [long_lat,long_lat...]
% site_classes= 'ABEFEF'
% csv_name = 'perth_sites.csv';

fid = fopen(csv_name,'wt');

fprintf(fid,'LONGITUDE,LATITUDE,SITE_CLASS\n'); %print the header
for i = 1:length(SiteLocations) % a bit slow
    fprintf(fid,'%10.8f',SiteLocations(i,1));
    fprintf(fid,',');
    fprintf(fid,'%10.8f',SiteLocations(i,2));
    fprintf(fid,',');
    fprintf(fid,site_classes(i));
    fprintf(fid,'\n');
end
fclose(fid);