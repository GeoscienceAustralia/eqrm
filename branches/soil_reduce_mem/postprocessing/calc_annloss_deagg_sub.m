function [annloss_deagg_sub_T] = calc_annloss_deagg_sub(eqrm_param_T, ecloss_data,outputdir)
%
% calc_annloss_deagg_sub computes the annualised loss for each suburb. 
% Outputs are returned to the workspace and saved to a csv file in outputdir. 
%
%INPUTS: 
% eqrm_param_T      [structure] standard EQRM setdata structure
% ecloss_data       [structure] containing results of risk simulation. Each of
%                   the variables in the saved_ecloss file is stored as a field
%                   in ecloss_data. The fileds include aus_mag, b_post89,          
%                   b_postcode, b_siteid, b_sub, b_survfact, b_type, b_ufi,            
%                   b_use, destring, nu, saved_ecbval2, saved_ecloss and   
%                   saved_rjb.
% outputdir         [string] Directory path for output file
% 
%OUTPUTS
% annloss_deagg_sub_T  [structure] with the following fields:
%   (1) subname         [cell - nx1] list of n suburb names where n is the
%                       number of unique suburbs in the study region.
%   (2) SubAnnLoss      [double -1xn] Annualised loss (dollars) for each of the
%                       suburbs in subname.
%   (3) SubAnnLossPer   [double -1xn] Annualised loss (as a percentage of total 
%                       suburb value) for each of the suburbs in subname.
%   (4) SubBval2        [double -1xn] Total value of the building stock(dollars) 
%                       for each of the suburbs in subname.
%
% *** Note that an output file is created in outputdir.
%
% COMMENTS
% This function has been modified since it was used with the Newcastle project.
%
% USEAGE:
%
% [annloss_deagg_sub_T] = calc_annloss_deagg_sub(eqrm_param_T,ecloss_data,'c:/temp')
%==========================================================================
% HISTORY:
% 29-06-04 : created by David Robinson
% 18-10-04 : corrected call to prep_sites()
%==========================================================================
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


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
fstr =['%s%u%u'];
[sublist,postcodelist,sub_post_idlist ] =  ...
     textread(tmp_full_path_file2, fstr, 'delimiter', ',', 'headerlines', 1, 'emptyvalue', NaN);



subs = unique(ecloss_data.b_sub);

%%subs = unique(b_sub);
numSub = length(subs);
count = 0; 
SubAnnLoss = zeros(numSub,1); %initialise Ann Loss vector
SubBval2 = zeros(numSub,1);    % initialise suburb value (inc contents) vector)
SubSurv = zeros(numSub,1); %initialise no buildings surveyed vector
SubEst = zeros(numSub,1); %initialise no buildings surveyed vector
SubBval2 = zeros(numSub,1);    % initialise suburb value (inc contents) vector)


for iSub = 1:numSub % loop over all the subunits
    ind = find(ecloss_data.b_sub == subs(iSub)); %index of subunits
    SubLossMatrix = ecloss_data. saved_ecloss(:,ind); %econ loss for subunit iSub, corresponding to a given event
    SubAggLoss = sum(SubLossMatrix,2); %agg econ loss for subunit iSub, corresponding to a given event
    SubBval2(iSub) = sum(ecloss_data.saved_ecbval2(ind)); % building value (inc contents) for suburb iSub
    SubEst(iSub) = sum( ecloss_data.b_survfact(ind) );
    SubSurv(iSub) = length( find(ecloss_data.b_sub == iSub) );  
    
    %SuburbPercAggEcLoss = 100*SubAggLoss./TotalBVal2;
    [trghzd_agg,SubLoss,SubCumnu] = acquire_riskval(SubAggLoss, ecloss_data.nu, 0);
    ExProb = 1-exp(-SubCumnu);   % exceedance probability: converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year

    n = length(ind);
    tempAnnLoss = 0;
    
    %do the backward integration (trapezoidal rule)
    for s=length(ExProb)-1:-1:1
            triArea = 1/2*abs( SubLoss(s+1) - SubLoss(s) )*abs( ExProb(s+1) - ExProb(s) );
            recArea = abs( ExProb(s+1) - ExProb(s) )*min( SubLoss(s+1), SubLoss(s) );
            tempAnnLoss = tempAnnLoss + triArea + recArea;
    end
    
    SubAnnLoss(iSub) = tempAnnLoss;
    %SubAggLoss1(iSub) = SubLossPer(1);
    ind = find(sub_post_idlist==subs(iSub));
    subname{iSub} = sublist{ind};
    
    count = count + n;
end

SubAnnLossPer = 100*SubAnnLoss ./ SubBval2; % Suburb annual loss as a percentage of suburb value
SubAnnLossPerA = 100*SubAnnLoss ./ sum(SubAnnLoss); %Suburb annual loss as a percentage of total annual loss
SubAnnLossTot = sum(SubAnnLoss);
SubBval2Per = 100*SubBval2/sum(SubBval2);
SubEstPer = 100*SubEst/sum(SubEst);
SubSurvPer = 100*SubSurv/sum(SubSurv);


disp('now writing results to file');
fid = fopen([outputdir,'\sub_annlosses.csv'], 'wt');
 
fprintf(fid, '%s','annualised losses by suburb');
fprintf(fid,'\n'); 

fprintf(fid, '%s','suburb,  value, ann loss, ann loss');
fprintf(fid,'\n');

fprintf(fid, '%s','  ,   ($ millions) , ($ millions), (% of suburb value)');
fprintf(fid,'\n');

for i=1:numSub
    fprintf(fid, '%s', [char(subname{i}),',']);
    fprintf(fid, '%s',[num2str(SubBval2(i)),',']);
    fprintf(fid, '%s',[num2str(SubAnnLoss(i)),',']);   
    fprintf(fid, '%s',[num2str(SubAnnLossPer(i)),',']);  
    fprintf(fid,'\n');
end
 status = fclose(fid);

annloss_deagg_sub_T.subname = subname;
annloss_deagg_sub_T.SubAnnLoss = SubAnnLoss;
annloss_deagg_sub_T.SubAnnLossPer = SubAnnLossPer;
annloss_deagg_sub_T.SubBval2 = SubBval2;