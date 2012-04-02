function [scenloss_sub_T] = calc_scenloss_sub(eqrm_param_T, ecloss_data,outputdir, pre89_flag, dollars89_flag,med_flag,ev)

% calc_scenloss_sub loads the results from an EQRM scenario simulation  and 
% produces a csv file with percentage building damage per suburb.
%
%% this version does the deaggragation BEFORE calculating the median (which
%% is the right way to do it!). 
%
%
% INPUTS:
% eqrm_param_T      [structure] standard EQRM setdata structure
% ecloss_data       [structure] containing results of risk simulation. Each of
%                   the variables in the saved_ecloss file is stored as a field
%                   in ecloss_data. The fileds include aus_mag, b_post89,          
%                   b_postcode, b_siteid, b_sub, b_survfact, b_type, b_ufi,            
%                   b_use, destring, nu, saved_ecbval2, saved_ecloss and   
%                   saved_rjb.
% outputdir         [string] Directory path for output file
% pre89_flag        [1 or 0]
%                       1 => consider buildings that existed before 1989 only.
%                       0 => consider all buildings in the database.
% dollars89_flag    [1 or 0]
%                       1 => convert dollar values to 1989 dollars. Note
%                       that conversion only makes sence for Newcastle
%                       data because it is hard wired as 1/1.37.
%                       0 => work with dollar values defined in the
%                       building database
% med_flag          [1 or 0]
%                       1 => consider the median loss for all event copies
%                       0 => consider the loss for event copy with index ev 
% ev                [scalar] index for event copy to be considered if
%                            med_flag=0
%
% OUTPUTS
% annloss_deagg_sub_T  [structure] with the following fields:
%   (1) subname         [cell - nx1] list of n suburb names where n is the
%                       number of unique suburbs in the study region.
%   (2) SubScenLossDoll [double -1xn] Scenario loss (dollars) for each of the
%                       suburbs in subname.
%   (3) SubScenLossPer  [double -1xn] Scenario loss (as a percentage of total 
%                       suburb value) for each of the suburbs in subname.
%   (4) SubBval2        [double -1xn] Total value of the building stock (dollars) 
%                       for each of the suburbs in subname.
%
% *** Note that an output file is created in outputdir.
%
% COMMENTS
% This function has been modified since it was used with the Newcastle project.
%
% USEAGE:
% [scenloss_sub_T] = calc_scenloss_sub(eqrm_param_T, ecloss_data,'c:/temp',1,1,1)
%
%==========================================================================
% HISTORY:
%  21-06-04 : Created by David Robinson
%  18-10-04 : corrected call to prep_sites()
%==========================================================================


% prep_sites;
sitedb_file  = ['sitedb_', eqrm_param_T.site_loc,  '.mat'];
%%%PREP_SITES_T = prep_sites(eqrm_param_T,sitedb_file);
is_risk = the_run_type_decipher('-is_it_a_risk_run_type',              eqrm_param_T.('run_type'));
is_rfh  = the_run_type_decipher('-is_it_a_risk_from_hazard_run_type',  eqrm_param_T.('run_type'));
if(     is_risk )
    a_str = '-risk';
elseif( is_rfh)
    a_str = '-risk_from_hazard'
else
      error('###_ERROR:  only RISK or RISK_FROM_HAZARD is supported !! ') 
end
PREP_SITES_T = prep_locations( a_str, eqrm_param_T, sitedb_file);

%read the list of all suburbs/posctodes and their unique identifiers
tmp_full_path_file2 = check4_local_eqrm_input(eqrm_param_T.inputdir,'suburb_postcode.csv');
fstr =['%s%u%u%s'];
[sublist,postcodelist,sub_post_idlist,LGA ] =  ...
    textread(tmp_full_path_file2, fstr, 'delimiter', ',', 'headerlines', 1, 'emptyvalue', NaN);


if nargin<4 
    pre89_flag= 1;
end

if nargin<5
    med_flag=1;
end

if nargin<6
    %ev = 1;
    %ev=510;
    %ev=16;
    ev=66;
end

  
%==================================================================
% filter out buildings pre-1989
pre89_flag = 0
if(pre89_flag==1)  % consider buildings that existed before 1989 only. 
    ecloss = ecloss_data.saved_ecloss(:,~ecloss_data.b_post89);
    ecbval2 = ecloss_data.saved_ecbval2(~ecloss_data.b_post89);
    % ORIGINAL code causes problems when using a subsample of the database
    %ufi = PREP_SITES_T.b_ufi(~ecloss_data.b_post89);
    %sub = PREP_SITES_T.b_sub(~ecloss_data.b_post89);
    %FIX to work with a subsample
    ufi = ecloss_data.b_ufi(~ecloss_data.b_post89);
    sub = ecloss_data.b_sub(~ecloss_data.b_post89);
    pre89str = 'Only Pre-1989 buildings considered';
elseif(pre89_flag==0)   % consider all buildings in the database...
    ecloss = ecloss_data.saved_ecloss;
    ecbval2 = ecloss_data.saved_ecbval2;
    % ORIGINAL code causes problems when using a subsample of the database
    %ufi = PREP_SITES_T.b_ufi;
    %sub = PREP_SITES_T.b_sub;
    %FIX to work with a subsample
    ufi = ecloss_data.b_ufi(~ecloss_data.b_post89);
    sub = ecloss_data.b_sub(~ecloss_data.b_post89);   
    pre89str = 'Post- and Pre-1989 buildings considered';
else
    error('INVALID value for pre89_flag... pre89_flag must be 0 or 1');
end
disp('done filtering post89 buildings'); 
%==================================================================

%% convert to 89 dollars
if(dollars89_flag==1)
    cvtdollar = 1/1.37;
    dollstr = 'in 89 dollars'
else
    cvtdollar = 1;
    dollstr = 'in 2002 dollars';
end

%f_ecloss = temp;
ecloss = cvtdollar*ecloss; %filtered ecloss as matrix(events, filtered_nsites)
ecbval2 = cvtdollar*ecbval2; %filtered building value as vector(filtered_nsites)

%==================================================================


nev = length(ecloss(:,1));
nsites = length(ecloss(1,:));
 
perloss = 100*ecloss ./ repmat(ecbval2', nev,1);
 
 %% suburb counts
 ecloss_tot = ecloss;
 bval2_tot = ecbval2;
 all_suburbs = unique(ecloss_data.b_sub);
 nsubs = length(all_suburbs); 
 
 aggloss_sub = zeros(nev, nsubs); 
 aggval_sub = zeros(1,nsubs); 
 
 disp('doing suburb counts');
 for suburb = 1:nsubs
    vec1 = ecloss_tot(:,sub == all_suburbs(suburb));
    aggloss_sub(:,suburb) = sum(vec1,2);
    vec2 = bval2_tot(sub == all_suburbs(suburb));
    aggval_sub(suburb) = sum(vec2);
    ind = find(sub_post_idlist==all_suburbs(suburb));
    subname{suburb} = sublist{ind};
 end
 
 perloss_sub = 100*aggloss_sub./repmat(aggval_sub, nev,1);
 
 if(med_flag == 1)  % consider the median loss
     result1 = median(aggloss_sub);
     result2 = median(perloss_sub,1);
 elseif(med_flag ==0) %consider the loss for event ev 
     result1 = aggloss_sub(ev,:);
     result2 = perloss_sub(ev,:);
 end
 
 
 
 % numsub = (1:125)';
 
%  blank = '  ';
%  blankV = repmat(blank, nsubs,1);
%  str = [blankV, char(str2mat(all_suburbs)),num2str(result1'/10^6), blankV, ...
%          num2str(aggval_sub'/10^6), blankV, num2str(result2')];
 
 disp('now writing results to file');
 fid = fopen([outputdir,'\scen_sublosses.csv'], 'wt');
 
fprintf(fid, '%s','percent losses by suburb');
fprintf(fid,'\n'); 

fprintf(fid, '%s',pre89str);
fprintf(fid,'\n'); 

if(med_flag==1)
     fprintf(fid, '%s', 'median values');
else
     fprintf(fid, '%s', 'event no.,');
     fprintf(fid, '%f', ev);
end
fprintf(fid,'\n'); 

fprintf(fid, '%s','suburb,  loss, value, percent loss');
fprintf(fid,'\n');

fprintf(fid, '%s','  ,   ($ millions) , ($ millions), ');
fprintf(fid,'\n');

for i=1:nsubs
    fprintf(fid, '%s', [char(subname{i}),',']);
    fprintf(fid, '%s',[num2str(result1(i)/10^6),',']);
    fprintf(fid, '%s',[num2str(aggval_sub(i)/10^6),',']);
    fprintf(fid, '%s',[num2str(result2(i)),',']);   
    fprintf(fid,'\n');
end
 status = fclose(fid);

scenloss_sub_T.subname =   subname;
scenloss_sub_T.SubScenLossDoll  = result1;
scenloss_sub_T.SubBval2  = aggval_sub;
scenloss_sub_T.SubScenLossPer  = result2;
 