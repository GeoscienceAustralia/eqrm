function gunzip_EQRMoutputs(datadir, dirout)
% searches the directory DIROUT for all files ending in .gz
% and gunzips them into directory DIROUT
%
% INPUTS: 
% datadir   [string] full path to directory containing *.gz files of
%           interest 
% dirout    [string] full path to directory where unzipped files will be
%           saved
%
% OUTPUTS
% * outputs are saved in DIROUT
%
% David Robinson 
% 30 May 2007


a = dir(datadir);
n = length(a);

currentdir = pwd; 
cd(datadir) 
for i = 1:n
    ind = strfind(a(i).name, '.gz')
    if ~isempty(ind)
        gunzip(a(i).name,dirout)
    end
end

cd(currentdir)

