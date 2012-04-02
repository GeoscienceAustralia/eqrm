function THE_PARAM_T = Convert_Py2Mat_PARAM_T(THE_PARAM_T_FILE)
% Function to convert the Python version of THE_PARAM_T file to 
% a Matlab structure of THE_PARAM_T.  This is needed so that we 
% can use the matlab postprocessing routines can be use.
%
% INPUTS:
% THE_PARAM_T_FILE  [string] full path name of THE_PARAM_T file. Usually
%                   this is THE_PARAM_T.txt but it can be clled anything
%
% OUTPUTS
% THE_PARAM_T       [structure] Matlab structure version of THE_PARAM_T. 
%                   This is the format used in the Matlab version of the
%                   EQRM. 
%
% David Robinson
% 30 March 2007

% read the Python version into a Matlab Cell
fid = fopen(THE_PARAM_T_FILE);
param_tmp = textscan(fid, '%s');
fclose(fid);
n = length(param_tmp{1}); % number of elements in the cell same as number of lines in THE_PARAM_T_FILE

% loop over the lines of THE_PARAM_T_FILE and assign the ones we want to
% the Matlab structure
THE_PARAM_T = [];
for i = 1: n
    k = strfind(param_tmp{1}{i},'=');  % find the equal sign
    if ~isempty(k)  % if there is an equal sign assign value to Matlab THE_PARAM_T
        j = strfind(param_tmp{1}{i},'[');  
        if ~isempty(j)  % then the value is data
            THE_PARAM_T = setfield(THE_PARAM_T,param_tmp{1}{i}(1:k-1),str2num(param_tmp{1}{i}(k+1:end)));
        else % the the value is a string
            THE_PARAM_T = setfield(THE_PARAM_T,param_tmp{1}{i}(1:k-1),param_tmp{1}{i}(k+1:end));
        end
    end 
end


% install the known typo in the MATLAB structure
tmp101 = THE_PARAM_T.qa_switch_ampfactors;
THE_PARAM_T = rmfield(THE_PARAM_T,'qa_switch_ampfactors');
THE_PARAM_T.qa_switch_ampfacors=tmp101;

% add the ieast field
THE_PARAM_T.ieast = 1;


