function [annloss_deagg_btype_T] = calc_annloss_deagg_btype(eqrm_param_T, ecloss_data,outputdir)

% calc_annloss_deagg_btype computes the annualised loss for each building type. 
% Outputs are returned to the workspace and saved to a csv file in outputdir. 
%
%INPUTS: 
% eqrm_param_T      [structure] standard EQRM setdata structure
% ecloss_data       [structure] containing results of risk simulation. Each of
%                   the variables in the saved_ecloss file is stored as a field
%                   in ecloss_data. The fields include aus_mag, b_post89,          
%                   b_postcode, b_siteid, b_sub, b_survfact, b_type, b_ufi,            
%                   b_use, destring, nu, saved_ecbval2, saved_ecloss and   
%                   saved_rjb.
% outputdir         [string] Directory path for output file
% 
%OUTPUTS
% annloss_deagg_btype_T  [structure] with the following fields:
%   (1) Typename        [cell - 1xn] list of n building types where n is the
%                       number of unique building types in the building database.
%   (2) TypeEstPer      [double - nx1] Estimated number of each building
%                       type (as a % of the total number of buildings)
%   (3) TypeBval2Per    [double - nx1] Value of each building type (as a %
%                       of the total value of all buildings in the database)
%   (4) TypeAnnLossPerA [double - nx1] Annualised loss for each building
%                       type in the database as a % of the total annualised loss.
%   (5) TypeAnnLossPer  [double - nx1] Annualised loss for each building
%                       type in the database as a % of the total value of that building type.
%                       
%
% *** Note that an output file is created in outputdir.
%
% COMMENTS
% This function was created by modifying calc_annloss_deagg_sub.m to
% produce outputs required for the Perth Cities Project Report
%
% USEAGE:
%
% [annloss_deagg_btype_T] = calc_annloss_deagg_btype(eqrm_param_T,ecloss_data,'c:/temp')
%==========================================================================
% HISTORY:
% 12-01-05 : created by Ken Dale (by modifying calc_annloss_deagg_sub.m)
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

%read the list of  building types and their unique identifiers
tmp_full_path_file2 = check4_local_eqrm_input(eqrm_param_T.inputdir,'b_types.csv');
fstr =['%s%u'];
[typelist,typeid ] =  ...
     textread(tmp_full_path_file2, fstr, 'delimiter', ',', 'headerlines', 1, 'emptyvalue', NaN);


types = unique(ecloss_data.b_type);


numTypes = length(types);
count = 0; 
TypeAnnLoss = zeros(numTypes,1); %initialise Ann Loss vector
TypeBval2 = zeros(numTypes,1);    % initialise btype value (inc contents) vector)
TypeSurv = zeros(numTypes,1); %initialise no buildings surveyed vector
TypeEst = zeros(numTypes,1); %initialise no buildings surveyed vector
TypeBval2 = zeros(numTypes,1);    % initialise building value (inc contents) vector)


for iType = 1:numTypes % loop over all the subunits
    ind = find(ecloss_data.b_type == types(iType)); %index of subunits
    TypeLossMatrix = ecloss_data.saved_ecloss(:,ind); %econ loss for subunit iType, corresponding to a given event
    TypeAggLoss = sum(TypeLossMatrix,2); %agg econ loss for subunit iType, corresponding to a given event
    TypeBval2(iType) = sum(ecloss_data.saved_ecbval2(ind)); % building value (inc contents) for building type iType
    TypeEst(iType) = sum( ecloss_data.b_survfact(ind) );
    TypeSurv(iType) = length( find(ecloss_data.b_type == iType) );  
    
    %SuburbPercAggEcLoss = 100*SubAggLoss./TotalBVal2;
    [trghzd_agg,TypeLoss,TypeCumnu] = acquire_riskval(TypeAggLoss, ecloss_data.nu, 0);
    ExProb = 1-exp(-TypeCumnu);   % exceedance probability: converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year

    n = length(ind);
    tempAnnLoss = 0;
    
    %do the backward integration (trapezoidal rule)
    for s=length(ExProb)-1:-1:1
            triArea = 1/2*abs( TypeLoss(s+1) - TypeLoss(s) )*abs( ExProb(s+1) - ExProb(s) );
            recArea = abs( ExProb(s+1) - ExProb(s) )*min( TypeLoss(s+1), TypeLoss(s) );
            tempAnnLoss = tempAnnLoss + triArea + recArea;
    end
    
    TypeAnnLoss(iType) = tempAnnLoss;
        
    ind = find(typeid==types(iType));
    Typename{iType} = typelist{ind};
       
    
    
    count = count + n;
end

TypeAnnLossPer = 100*TypeAnnLoss ./ TypeBval2; % Building type annual loss as a percentage of building type value
TypeAnnLossPerA = 100*TypeAnnLoss ./ sum(TypeAnnLoss); %Building type annual loss as a percentage of total annual loss
TypeAnnLossTot = sum(TypeAnnLoss);
TypeBval2Per = 100*TypeBval2/sum(TypeBval2);
TypeEstPer = 100*TypeEst/sum(TypeEst);
TypeSurvPer = 100*TypeSurv/sum(TypeSurv);


disp('now writing results to file');
fid = fopen(['./btype_annlosses.csv'], 'wt');
 
fprintf(fid, '%s','annualised losses by building type');
fprintf(fid,'\n'); 

fprintf(fid, '%s','b_type, number, value, ann loss, ann loss');
fprintf(fid,'\n');

fprintf(fid, '%s','  , (% total buildings) , (% total value) , (% total ann loss), (% of building value)');
fprintf(fid,'\n');

for i=1:numTypes
    fprintf(fid, '%s', [char(Typename{i}),',']);
    fprintf(fid, '%s',[num2str(TypeEstPer(i)),',']);
    fprintf(fid, '%s',[num2str(TypeBval2Per(i)),',']);
    fprintf(fid, '%s',[num2str(TypeAnnLossPerA(i)),',']);   
    fprintf(fid, '%s',[num2str(TypeAnnLossPer(i)),',']);  
    fprintf(fid,'\n');
end
 status = fclose(fid);

annloss_deagg_btype_T.Typename = Typename;
annloss_deagg_btype_T.TypeEstPer = TypeEstPer;
annloss_deagg_btype_T.TypeBval2Per = TypeBval2Per;
annloss_deagg_btype_T.TypeAnnLossPerA = TypeAnnLossPerA;
annloss_deagg_btype_T.TypeAnnLossPer = TypeAnnLossPer;