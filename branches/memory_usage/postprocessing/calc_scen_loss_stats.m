function [scen_loss_stats,hf] = calc_scen_loss_stats(eqrm_param_T, ecloss_data,outputdir, pre89_flag, dollars89_flag,resonly_flag,finalprint_flag,Xlim)

% calc_scen_loss_stats loads the results from an EQRM scenario simulation  and 
% produces a histogram of total loss experienced in the study region. Note
% that the histogram values correspond to different realisations from the
% 'random simulation'. 
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
%                            that conversion only makes sence for Newcastle
%                            data because it is hard wired as 1/1.37.
%                       0 => work with dollar values defined in the
%                            building database
% resonly_flag      [1 or 0]
%                       1 => consider only residential buildings
%                       0 => consider all buildings in database
% finalprint_flag   [1 or 0]
%                       0 => do not print figures
%                       1 => print eps to outputdir
%                       2 => print jpeg to outputdir
% Xlim              [double -1x2] Limits for x-axis. Note that default
%                   limits are used if Xlim is empty.
%
% OUTPUTS
% scen_loss_stats   [structure] with the following fields:
%   (1) aggloss_dollars [double -1xn] Aggregated loss (dollars) for all
%                       of the buildings in the study region. The n values 
%                       correspond realisations of the random simulation.                       
%   (2) aggloss_perc    [double -1xn] Aggregated loss (as a percentage of
%                       total building value) for all of the buildings in
%                       the study region. 
%   (3) median_dollars  [scalar] median aggregated loss (dollars)
%   (4) median_perc     [scalar] median aggregated loss (%)
%   (5) mean_dollars    [scalar] mean aggregated loss (dollars)
%   (6) mean_perc       [scalar] mean aggregated loss (%)
% hf                [scalar] figure handle of created figure. If no figure
%                   are created hf is empty.
%
% * Note that a file is also produced if finalprint_flag>=1.
%
% David Robinson
% 6 July 2004

hf =[];
tstring2 = 'Newc89 agg loss, pre89, 1989 dollars';
%% do filtering of results to exclude post 89 buildings

if(pre89_flag==1) %filter out the post89 buildings
    if (resonly_flag == 1) %only report residential buildings
            temp_ecloss = ecloss_data.saved_ecloss(:,(~ecloss_data.b_post89 & ecloss_data.b_use==1));
            temp_bval2 = ecloss_data.saved_ecbval2(~ecloss_data.b_post89 & ecloss_data.b_use==1);
            tstr3 = 'pre 1990 buildings - RES1 only';
    elseif (resonly_flag == 0) % consider all useage classifications
            temp_ecloss = ecloss_data.saved_ecloss(:,~ecloss_data.b_post89);
            temp_bval2 = ecloss_data.saved_ecbval2(~ecloss_data.b_post89);
            tstr2 = 'pre 1990 buildings - All useage types';
    else
            error({'ERROR: invalid value for resonly_flag in calc_scen_loss_stats.'; ...
            'Accepted values are 1 or 0.'})
    end
elseif(pre89_flag==0)
    if (resonly_flag == 1) %only report residential buildings
        temp_ecloss = ecloss_data.saved_ecloss(:, ecloss_data.b_use==1);
        temp_bval2 = ecloss_data.saved_ecbval2(:, ecloss_data.b_use==1);
        tstr2 = '';
    elseif (resonly_flag == 0) % consider all useage classifications
        temp_ecloss = ecloss_data.saved_ecloss;
        temp_bval2 = ecloss_data.saved_ecbval2;
        tstr2 = '';
    else
        error({'ERROR: invalid value for resonly_flag in calc_scen_loss_stats.'; ...
            'Accepted values are 1 or 0.'})
    end
else
    error({'ERROR: invalid value for pre89_flag in calc_scen_loss_stats.'; ...
            'Accepted values are 1 or 0.'})   
end


%% convert to 89 dollars
if(dollars89_flag==1)
    cvtdollar = 1/1.37;
    dollstr = 'in 89 dollars'
else
    cvtdollar = 1;
    dollstr = 'in 2002 dollars';
end
f_ecloss = cvtdollar*temp_ecloss; %filtered ecloss as matrix(events, filtered_nsites)
f_bval2 = cvtdollar*temp_bval2; %filtered building value as vector(filtered_nsites)


f_aggloss_bill = sum(f_ecloss,2)/10^9;
f_aggbval2_bill = sum(f_bval2)/10^9;

hf(1) = figure
hist(f_aggloss_bill,10);
title(tstring2);
xlabel(['$ (billions)', dollstr])
ylabel('frequency');

disp(['median = ', num2str( median(f_aggloss_bill) ), ' billion dollars']);
disp(['median = ', num2str( 100*median(f_aggloss_bill)/f_aggbval2_bill ), '%']);

disp(['mean = ', num2str( mean(f_aggloss_bill) ), ' billion dollars']);
disp(['mean = ', num2str( 100*mean(f_aggloss_bill)/f_aggbval2_bill ), '%']);


hf(2) = figure
aggloss_perc = 100*f_aggloss_bill/f_aggbval2_bill;
hist(aggloss_perc,10);
title(tstring2);
xlabel('% of building value (including contents)');
ylabel('frequency')
if ~isempty(Xlim), set(gca,'Xlim',Xlim); end


if(finalprint_flag==1|2)
    figure(hf(2))
    title('');
    papersize = [14 11];
    paperposition = [0 0 14 11];
    set(gcf,'Paperunits','cent','PaperSize',papersize,'PaperPosition',paperposition,'PaperOrientation','portrait')

    FigWidth = 11;
    HorizMargin = 2;
    FigHeight = 8;
    VertMargin = 1.5;
    NumberFontSize = 12;
    set(gca,'units','cent','position',[HorizMargin,VertMargin,FigWidth,FigHeight],'fontsize',NumberFontSize)

    
    if finalprint_flag ==1
        filename2 ='scen_loss_stats_perc.eps';
        eval(['print -depsc2 ', outputdir,'\',filename2])
    elseif finalprint_flag==2
        filename2 ='scen_loss_stats_perc.jpg';
        eval(['print -djpeg100 ', outputdir,'\',filename2])
    end
elseif (finalprint_flag ~= 0)
    error({'ERROR: invalid value for finalprint_flag in calc_scen_loss_stats.'; ...
        'Accepted values are 1 or 0.'})
end

scen_loss_stats.aggloss_dollars = f_aggloss_bill*10^9;
scen_loss_stats.aggloss_perc = aggloss_perc;
scen_loss_stats. median_dollars = median(f_aggloss_bill)*10^9;
scen_loss_stats. median_perc = 100*median(f_aggloss_bill)/f_aggbval2_bill;
scen_loss_stats. mean_dollars = mean(f_aggloss_bill)*10^9;
scen_loss_stats. mean_perc = 100*mean(f_aggloss_bill)/f_aggbval2_bill;
