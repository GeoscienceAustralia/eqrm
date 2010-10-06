function site_classes = getSC_fromAmpFactorFile(fname)
% This function extracts all the unique site classes represented in an
% *.MAT ampfactor file
%
% INPUTS:
% fname     [string] full path to MAT file containing the ampfactors
%
% OUTPUTS:
% site_classes [cell array] contains the unique site_classes
%
% NOTES:    - will bomb if you have other varaibles with ln_site in the variable name
%           - this version only accepts site classes with 1 letter
%
% David Robinson
% 11 April 2007


load(fname)
a = whos; 

count = 1;
site_classes = {};
for i = 1:length(a)
    test1 = strfind(a(i).name, 'ln_site');  % find all the amfactors
    test2 = strfind(a(i).name, 'std'); % find all the std of ampfactors
    if (test1 ==1) & isempty(test2)  % keep only the ampfactors
        for j = 1:6
            if a(i).name(8+j)=='_'
                site_classes_full{count} = a(i).name(8:(8+j-1));
                count = count+1;
                break
            end
        end
    end   
end
site_classes = unique(site_classes_full);
