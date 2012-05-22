function [THE_PARAM_T,hzd_regolith,hzd_rock, periods, rtrn_per, site_pos] = ...
                    Convert_Py2Mat_Hazard(datadir,param_fname)
% Converts  outputs from python version of the EQRM into the same 
% format as those from the matlab version of the EQRM. That way 
% all of the matlab postprocessing routines can be use.
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
% 30 March 2007
%
% Notes on formats:
%
%   PYTHON: 
%       -   Site locations are printed in lat & long file
%       -   Hazard data are saved in multiple files. There is one file for
%           each return period. Regolith and bedrock are saved separately.
%           
%   Matlab:
%       - THE_PARAM_T: as a Matlab structure
%       - hzd_regolith [single array - ns x nr x np] 
%                   n sites
%       - hzd_rock  [single array - ns x nr x np] 
%       - periods [1xnp] RSA periods
%       - rtrn_per [nrx1] Return periods
%       - site_pos [ns x 2] with longitude in column 1 and latitude in
%         column 2
%
%

% we move to the directory where data is stored 
currentdir = pwd;  % keep a record from where we started 
cd(datadir)  % move to datadir


% Convert the python THE_PARAM_T to matlab version
THE_PARAM_T = Convert_Py2Mat_PARAM_T([datadir,filesep,param_fname]);
eqrm_param_T = THE_PARAM_T;
save([datadir,'/matlab_setdata.mat'],'eqrm_param_T')

% define what we can now
periods = THE_PARAM_T.periods;
rtrn_per = THE_PARAM_T.rtrn_per;

% Load the site data
tmp = load([THE_PARAM_T.site_loc,'_locations.txt']);
site_pos = [tmp(:,2), tmp(:,1)];  % flip order of latitude and longitude. 


% initialise the hazard matrices
hzd_rock = zeros(size(site_pos,1), length(THE_PARAM_T.rtrn_per), length(THE_PARAM_T.periods)); 
if THE_PARAM_T.amp_switch ==1
    hzd_regolith = zeros(size(site_pos,1), length(THE_PARAM_T.rtrn_per), length(THE_PARAM_T.periods));
end

% We use separate loops to make the filenames and then to load the data
% this is more exepensive but it makes it easier to follow:

% Make the file names
bednames = {};
if THE_PARAM_T.amp_switch==1, regnames = {};end
for i = 1:length(THE_PARAM_T.rtrn_per)  % loop over all of the return periods
    % Deal with return periods that have no decimal points
    if THE_PARAM_T.rtrn_per(i)-floor(THE_PARAM_T.rtrn_per(i))  ==0 % there are no decimal points
        bednames{i} = [THE_PARAM_T.site_loc,'_bedrock_SA_rp[', num2str(THE_PARAM_T.rtrn_per(i)), '].txt'];
        if THE_PARAM_T.amp_switch==1,
            regnames{i} = [THE_PARAM_T.site_loc,'_soil_SA_rp[', num2str(THE_PARAM_T.rtrn_per(i)), '].txt'];
        end
        % Deal with return periods that have one decimal point
    elseif 10*THE_PARAM_T.rtrn_per(i)-floor(10*THE_PARAM_T.rtrn_per(i))  ==0  % there is one decimal point
        pt = 10*(THE_PARAM_T.rtrn_per(i) - floor(THE_PARAM_T.rtrn_per(i)));
        bednames{i} = [THE_PARAM_T.site_loc,'_bedrock_SA_rp[', num2str(floor(THE_PARAM_T.rtrn_per(i))), 'pt', num2str(pt),'].txt'];
        if THE_PARAM_T.amp_switch==1,
            regnames{i} = [THE_PARAM_T.site_loc,'_soil_SA_rp[', num2str(floor(THE_PARAM_T.rtrn_per(i))), 'pt', num2str(pt),'].txt'];
        end
        % Deal with return periods that have one decimal point
    elseif 100*THE_PARAM_T.rtrn_per(i)-floor(100*THE_PARAM_T.rtrn_per(i))  ==0  % there are two decimal points
        pt = 100*(THE_PARAM_T.rtrn_per(i) - floor(THE_PARAM_T.rtrn_per(i)));
        bednames{i} = [THE_PARAM_T.site_loc,'_bedrock_SA_rp[', num2str(floor(THE_PARAM_T.rtrn_per(i))), 'pt', num2str(pt),'].txt'];
        if THE_PARAM_T.amp_switch==1,
            regnames{i} = [THE_PARAM_T.site_loc,'_soil_SA_rp[', num2str(floor(THE_PARAM_T.rtrn_per(i))), 'pt', num2str(pt),'].txt'];
        end
    else  %this code is not written to deal with more than 2 decimal points in a return period
        disp(['error with ', num2str(THE_PARAM_T.rtrn_per(i)), ' CONVERT_PY2MAT_HAZARD can not cope with return periods that have more than 2 numbers after the decimal'])
    end
end
%print bednames

% Now we can actually load the data
for i = 1:length(bednames)
    bedtmp = dlmread(bednames{i}, ' ', 3, 0);  % Note we start at row 3 to ignore 2 rows of header and 1 row containg the periods
    hzd_rock(:,i,:) = bedtmp;
    if THE_PARAM_T.amp_switch ==1
        regtmp = dlmread(regnames{i}, ' ', 3, 0);  % Note we start at row 3 to ignore 2 rows of header and 1 row containg the periods
        hzd_regolith(:,i,:) = regtmp;
    end
end

if THE_PARAM_T.amp_switch ~= 1
    hzd_regolith = hzd_rock;  % i.e. because this is what the Matlab EQRM does and some of the plotting routines require hzd_regolith
end

save([THE_PARAM_T.site_loc,'_db_hzd.mat'],'THE_PARAM_T','hzd_regolith','hzd_rock','periods','rtrn_per','site_pos')

cd(currentdir)  % return user to where the started.




