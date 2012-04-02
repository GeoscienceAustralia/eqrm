function evntdb_to_xml(evntdb_name,xml_name,mag_type)

% function evntdb_to_xml(evntdb_name,xml_name)
%
% eg inputs
% evntdb_name = 'natperth_db_fuse.mat';
% xml_name = 'perth_event_set.xml';

load(evntdb_name)

% evntdb = evntdb(1:10,:);

fid = fopen(xml_name,'wt');

fprintf(fid,'<Event_Set magnitude_type="Mw">\n');


% Print selected columns of the eventdb
fprintf(fid,'\t<latitude>\n');
fprintf(fid,'%6.8f ',evntdb(:,23)); % latitude of epicentre
fprintf(fid,'\n\t</latitude>\n');

fprintf(fid,'\t<longitude>\n');
fprintf(fid,'%6.8f ',evntdb(:,24)); % longitude of epicentre
fprintf(fid,'\n\t</longitude>\n');

fprintf(fid,'\t<dip>\n');
fprintf(fid,'%i ',evntdb(:,7)); % dip of rupture
fprintf(fid,'\n\t</dip>\n');

fprintf(fid,'\t<azimuth>\n');
fprintf(fid,'%-5.8f ',evntdb(:,6)); % azimuth of rupture
fprintf(fid,'\n\t</azimuth>\n');

fprintf(fid,'\t<depth>\n');
fprintf(fid,'%-6.8f ',evntdb(:,25)); % depth of rupture centroid
fprintf(fid,'\n\t</depth>\n');

if mag_type == 0
    fprintf(fid,'\t<ML>\n');
    fprintf(fid,'%6.8f ',evntdb(:,21)); % magnitude of earthquake
    fprintf(fid,'\n\t</ML>\n');
end
if mag_type == 1

    fprintf(fid,'\t<Mw>\n');
    fprintf(fid,'%6.8f ',evntdb(:,21)); % magnitude of earthquake
    fprintf(fid,'\n\t</Mw>\n');
end

fprintf(fid,'\t<event_activity>\n');
fprintf(fid,'%14.14f ',evntdb(:,20)); % event activity (i.e. num events expected per year)
fprintf(fid,'\n');
fprintf(fid,'\t</event_activity>\n');

fprintf(fid,'\t<length>\n');
fprintf(fid,'%6.8f ',evntdb(:,28)); % length of fault
fprintf(fid,'\n\t</length>\n');

fprintf(fid,'\t<width>\n');
fprintf(fid,'%6.8f ',evntdb(:,29)); % width of fault
fprintf(fid,'\n\t</width>\n');

fprintf(fid,'\t<rx>\n');
fprintf(fid,'%6.8f ',evntdb(:,26)); % 'local' x position
fprintf(fid,'\n\t</rx>\n');

fprintf(fid,'\t<ry>\n');
fprintf(fid,'%6.8f ',evntdb(:,27)); % 'local' y position
fprintf(fid,'\n\t</ry>\n');

fprintf(fid,'\t<trace_start_lat>\n');
fprintf(fid,'%6.8f ',evntdb(:,2)); % start of trace
fprintf(fid,'\n\t</trace_start_lat>\n');

fprintf(fid,'\t<trace_start_lon>\n');
fprintf(fid,'%6.8f ',evntdb(:,3)); % end of trace
fprintf(fid,'\n\t</trace_start_lon>\n');

fprintf(fid,'</Event_Set>\n');
fclose(fid);