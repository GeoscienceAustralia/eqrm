function [return_path,in_inputdir] = check4_local_eqrm_input(path2search,filename)
%
% check4_local_eqrm_input is designed to look in a local directory 
% (path2search) for a file (filename). If it finds the filename in 
% path2search the full file local path is returned, otherwise the 
% EQRM default resource file path is returned. 
%
% Inputs:
% path2search       [string] full path for directory to search
% filename          [string] file to search for with extension
%
% Outputs:
% return_path       [string] local path [path2search,filename] 
%                   if filename exists in path2search. Otherwise
%                   the EQRM default resource file path is returned
% in_inputdir:      [boolean] true if file found in inputdir, otherwise
%                   false
% 
% USAGE:
% [return_path] = check4_local_eqrm_input(['c:',filesep,'temp'],'newc_db_evntdb.mat')
%
% David Robinson
% 4 July 2003

checkvar = exist([path2search,filesep,filename]);
if checkvar ==2
    return_path = [path2search,filesep,filename];
    in_inputdir = true;
else % we need to find the resource/data directory
    % the following is a little bit a fudge to get this. 
    dir1 = which('wrap_risk_plots');
    ind =findstr(dir1,'postprocessing');
    dir2 = dir1(1:ind-2);
    return_path = [dir2,'\resources\data', filesep, filename];
    %return_path = [get_eqrm_path_info('-resources_data'), filesep, filename];
    in_inputdir = false;
end