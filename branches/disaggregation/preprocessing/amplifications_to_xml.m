function amplifications_to_xml(in_file,out_file)
% function evntdb_to_xml(evntdb_name,xml_name)
%
% eg inputs
% in_file = 'newc_par_ampfactors.mat'
% out_file = 'newc_par_ampfactors.xml'
% sites={'A','B','C','D','E','F','G','H'}

load(in_file);

who;
site_classes = getSC_fromAmpFactorFile(in_file);
fid = fopen(out_file,'wt');

fprintf(fid,'<amplification_model matlab_file = "');
fprintf(fid,out_file);
fprintf(fid,'">\n');
          
fprintf(fid,'<moment_magnitude_bins>\n'); %print the header
for i = 1:length(momag_bin)
    fprintf(fid,'%10.8f ',momag_bin(i));
end
fprintf(fid,'\n</moment_magnitude_bins>\n'); %print the header

fprintf(fid,'<pga_bins>\n'); %print the header
for i = 1:length(pga_bin)
    fprintf(fid,'%10.8f ',pga_bin(i));
end
fprintf(fid,'\n</pga_bins>\n'); %print the header

fprintf(fid,'<site_classes>\n'); %print the header
for i = 1:length(site_classes)
    fprintf(fid,'%s ',site_classes{i});
end
fprintf(fid,'\n</site_classes>\n'); %print the header

fprintf(fid,'<periods>\n'); %print the header
for i = 1:length(amp_period)
    fprintf(fid,'%10.8f ',amp_period(i));
end
fprintf(fid,'\n</periods>\n'); %print the header

%fprintf(fid,'<site_classes>\n'); %print the header
%for i = 1:length(site_classes)
%    fprintf(fid,site_classes(i));
%    fprintf(fid,',');
%end
%fprintf(fid,'</site_classes>\n'); %print the header

for i = 1:length(site_classes) % a bit slow
    site_class=site_classes{i};
    fprintf(fid,'<site_class class="%s">\n',site_class);
    for j = 1:length(momag_bin)
        fprintf(fid,'    <moment_magnitude mag_bin="%10.8f">\n',momag_bin(j));
        Text_momag   = sprintf('%02.0f',momag_bin(j)*1e1); 
        for k = 1:length(pga_bin)            
            Text_pga   = sprintf('%04.0f',pga_bin(k)*1e3); 
            amp = eval(['ln_site',site_class,'_rockpga',Text_pga,'_momag',Text_momag]);    
            fprintf(fid,'        <pga pga_bin="%10.8f">\n',pga_bin(k));         
            fprintf(fid,'            <log_amplification site_class = "');   
            fprintf(fid,'%s',site_class);
            fprintf(fid,'" moment_magnitude = "');
            fprintf(fid,'%10.8f',momag_bin(j));
            fprintf(fid,'" pga_bin = "');
            fprintf(fid,'%10.8f',pga_bin(k));
            fprintf(fid,'">\n            ');
            for l = 1:length(amp_period)
                fprintf(fid,'%10.8f ',amp(l));
            end           
            fprintf(fid,'\n            </log_amplification>\n');              
            ampstd = eval(['stdln_site',site_class,'_rockpga',Text_pga,'_momag',Text_momag]);
            fprintf(fid,'            <log_std site_class = "');   
            fprintf(fid,'%s',site_class);
            fprintf(fid,'" moment_magnitude = "');
            fprintf(fid,'%10.8f',momag_bin(j));
            fprintf(fid,'" pga_bin = "');
            fprintf(fid,'%10.8f',pga_bin(k));
            fprintf(fid,'">\n            ');
            for l = 1:length(amp_period)
                fprintf(fid,'%10.8f ',ampstd(l));
            end
            fprintf(fid,'\n            </log_std>\n');       
            fprintf(fid,'        </pga>\n');       
        end    
        fprintf(fid,'    </moment_magnitude>\n');       
    end
    fprintf(fid,'\n</site_class>\n');
end
fprintf(fid,'\n</amplification_model>\n');
fclose(fid);
