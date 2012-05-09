function [ann_loss,hf, cumAnnLoss] = calc_annloss(saved_ecloss, saved_ecbval2, nu, outputdir, varargin);
%
% calc_annloss computes the annualised loss from a standard probabilistic
% EQRM risk run. The annulaised loss is the main output, however options
% have been included to save the annualised loss and/or  plot it as a 
% function of return period. 
%
% INPUTS:
% saved_ecloss      [matrix] containing the damage estimates in dollars for
%                   each building, multiplied by it survey factor. Note that 
%                   the matrix has one row for each simulated event and one
%                   column for each building.
% saved_ecbval2     [row vector] containing the value of each building,
%                   multiplied by it survey factor.
% nu                [column vector] the event activity of each of the simulated
%                   events.
% outputdir         [string] Directory path for any output files
% varagin           either, both or neither of the following;
%                       's' to save the annualised losses
%                       'p' to plot the annualised loss as a function of
%                           return period
%                       'd' to display results to screen
%
% OUTPUTS:
% ann_loss          [vector (2x1)] contains the annulaised loss in
%                   dollars (ann_loss(1)) and the annualised loss as a
%                   percentage of the total building value (ann_loss(2)).
% hf                [scalar] figure handle of created figure. If no figure
%                   are created hf is empty.
% cumAnnLoss        cummulative annulaised loss
%                       column1 => return period
%                       column2  => cummAnnLoss in dollars
%                       column3  => cummAnnLoss as % of total building value    
%
%
% USAGE:
%       [ann_loss] = calc_annloss(saved_ecloss, saved_ecbval2, nu, 's','p');
%==========================================================================
% HISTORY:
%  07-07-04 : Created by David Robinson
%  18-10-04 : correction via phone call for PML switch
%==========================================================================

hf=[];
optional_args = {varargin{:}};   % get the optional arguments
% pml_switch = optional_args{2};
% 
TotalBVal2 = sum(saved_ecbval2);        % calculating the total building value for the region
% if pml_switch == 1;
    AggLoss = sum(saved_ecloss,2);            % computed aggregated loss across the city for each eq
% else
%      AggLoss = saved_ecloss;
% end

[trghzd_agg,EcLoss,cumnu] = acquire_riskval(AggLoss, nu, 0);
ProbExceed = 1-exp(-cumnu);                  % converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year

n = length(ProbExceed);
tempAnnLoss = zeros(n,1);
% integrate (backwards): CHECK THIS (IS THE INTEGRAL RIGHT WAY UP?) 
for s=n-1:-1:1
    TriArea = 1/2*abs(EcLoss(s+1) - EcLoss(s))*abs(ProbExceed(s+1) - ProbExceed(s) );
    RecArea = abs(ProbExceed(s+1) - ProbExceed(s) ) * min(EcLoss(s+1), EcLoss(s) );
    tempAnnLoss(s) = tempAnnLoss(s+1) + TriArea + RecArea;
end

ann_loss(1) = tempAnnLoss(1);
ann_loss(2) = ann_loss(1)./TotalBVal2*100;

% disp results to screen if requested
if max(strcmp(optional_args,'d'))==1
    disp('The annualised loss is: ')
    disp([num2str(ann_loss(1)), ' dollars'])
    disp('OR')
    disp([num2str(ann_loss(2)),'%'])   
end

% save results to lauch directory if requested
if max(strcmp(optional_args,'s'))==1
    save([outputdir,'\annualised_loss.mat'], 'ann_loss','-mat')
end

% create a plot of annualised loss versus return period if requested
retrn_per1 = -1./log(1-ProbExceed);
cumAnnLoss = [retrn_per1, tempAnnLoss, tempAnnLoss/TotalBVal2*100];
if max(strcmp(optional_args,'p'))==1
    hf= figure;
    loglog(retrn_per1, tempAnnLoss/TotalBVal2*100)
    xlabel('Return period (years)')
    ylabel('Annualised economic loss (% of building value)')
end
