function []=calc_annloss_deagg_useage()
%
% WARNING - This function is not completed yet!!!!!!!!!


% calc_annloss_deagg_useage dis-aggreagtes the risk in terms of building
% useage. A bar chart is created showing the annualised loss for four 
% the following four different useage classificationd:
% 1) Industrial
% 2) Commercial
% 3) Residential 
% 4) Other - Agriculture, Religion, Non-Profit, Government, Education
% Note that annualised loss is expressed as a percentage of the total value
% of all buildings in the same useage classification. 








%************************************************
% WARNING - THIS DOES NOT CHECK THE USAGE CLASSIFICATION
% THIS EFFECTS LINES 378 -
%**************************************************




% Note - b_usage displays all the different usage types as described in Hazus manual 15-7
% We re-assign these into clusters
b_use(b_use<=28 & b_use>=23) =40;  % Other - Agriculture, Religion, Non-Profit, Government, Education
b_use(b_use<=22 & b_use>=17) =30;  % Industrial buildings
b_use(b_use<=16 & b_use>=7) =20;   % Commercial buildings
b_use(b_use<=6 & b_use>=1) =10;    % Residential buildings

Usage = unique(b_use);
nUsage = length(Usage);
countUsage = 0; 
for usagei = 1:nUsage
    clear indUsage UsageLoss UsageAggLoss UsagePercEcLoss UsageProbExceed UsageIntPercEcLoss 
    indUsage = find(b_use == Usage(usagei));
    UsageLoss = saved_ecloss(:,indUsage);
    UsageAggLoss = sum(UsageLoss,2);
    UsagePercAggEcLoss = 100*UsageAggLoss./TotalBVal2;
    [UsagePercEcLoss,Usagecumnu_ecloss] = rte2cumrte(UsagePercAggEcLoss,nu);   % sorts PercAggEcLoss largest to smallest and cumsums nu
    UsageProbExceed = 1-exp(-Usagecumnu_ecloss);                          % converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year

    n = length(indUsage);
    UsageIntPercEcLoss = zeros(size(UsageProbExceed));
    for s=length(UsageProbExceed)-1:-1:1
            UsageTriArea = 1/2*abs(UsagePercEcLoss(s+1)-UsagePercEcLoss(s))*abs(UsageProbExceed(s+1)-UsageProbExceed(s));
            UsageRecArea = abs(UsageProbExceed(s+1)-UsageProbExceed(s))*min(UsagePercEcLoss(s+1),UsagePercEcLoss(s));
            UsageIntPercEcLoss(s) = UsageIntPercEcLoss(s+1)+UsageTriArea+UsageRecArea;
    end
    UsageAnnualisedLoss(usagei) = UsageIntPercEcLoss(1);
    UsageAggLoss1(usagei) = UsagePercEcLoss(1);
    countUsage = countUsage +n;
end

% Annualised loss for each building usage classification as a percentage of total annualised loss in Newcastle

UsageAnnLossPerc = 100*UsageAnnualisedLoss./IntPercEcLoss(1);
figure
bar(Usage,UsageAnnLossPerc)
title('Annualised loss for each building classification')
ylabel('Annualised building damage loss (as a percentage of total annualised loss for Newcastle)')
xlabel('Building Usage Classification')
