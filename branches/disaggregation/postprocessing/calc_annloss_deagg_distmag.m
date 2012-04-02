function [NormDeAggLoss, hf] = calc_annloss_deagg_distmag(eqrm_param_T, ecloss_data,outputdir,momag_bin,momag_labels,R_bin, R_extend_flag,finalprint_flag,Zlim)
% 
% calc_annloss_deagg_distmag dis-aggregates the risk in terms of magnitude
% and distance. 
%
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
% momag_bin         [double 1xn] Bounds for moment magnitude bins e.g. 
%                       momag_bin = [4.5:0.5:6.5];
%                   Note that the value 0.0000000000001 is added to momag_bin(end)
%                   to ensure that values corresponding to momag_bin(end)are 
%                   captured i.e. momag_bin = [4.5:0.5:6.5] becomes
%                   momag_bin = [4.5, 5, 5.5,6,6.5000000000001];
% momag_labels      [double 1xn] controls the ticks and labels for the
%                   moment magnitude axis. The elements of momag_labels
%                   must also be in momag_bin.
% R_bin             [double 1xm] Bounds for distance bins e.g. 
%                       R_bin = [0:5:100];
%                   Note that if R_extend_flag==1 R_bin is extended by one 
%                   element as follows; R_bin(end+1) = 100000. This is done
%                   to ensure that all values > R_bin(end) are included in the 
%                   final R_bin. 
% R_extend_flag     [1 or 0]
%                       1 => extend R_bin (see R_bin)
%                       0 => do not extend R_bin
% finalprint_flag   [1, 2 or 0]
%                       0 => do not print figures
%                       1 => print eps to outputdir
%                       2 => print jpeg to outputdir
% Zlim              [double: 1x2] z-axis limits. 
%
% OUTPUTS:
%
%==========================================================================
% HISTORY:
% 15-04-04 : Created by David Robinson
% 18-10-04 : minor correction to calling syntax for CALC_ANNLOSS()
%==========================================================================


%setup
TotalBVal2 = sum(ecloss_data.saved_ecbval2);
%[ann_loss] = calc_annloss(ecloss_data.saved_ecloss, ecloss_data.saved_ecbval2, ecloss_data.nu,'d');
[ann_loss, junk] = calc_annloss(ecloss_data.saved_ecloss, ecloss_data.saved_ecbval2, ecloss_data.nu, outputdir, 'd');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% De - Aggregation
% Setup moment magnitude bins
momag_bin_original = momag_bin;
momag_bin(end) = momag_bin(end)+0.0000000000001;
momag_centroid = momag_bin(1:end-1) + diff(momag_bin)./2;
momag_centroid(end) = momag_bin(end-1) + (momag_bin(end-1)-momag_bin(end-2))/2;

% Setup distance bins (Note does not necessarily need to be Joyner-Boore distance). 
if R_extend_flag ==1
    Rjb_bin = [R_bin(:)',10000];
elseif R_extend_flag==0
    Rjb_bin = R_bin(:)';
else
    error({ 'ERROR: invalid value for R_extend_flag in calc_annloss_deagg_distmag.'; ...
            'Accepted values are 1 or 0.'})
end
Rjb_centroid = Rjb_bin(1:end-1) + diff(Rjb_bin)./2;
Rjb_centroid(end) = Rjb_bin(end-1) + (Rjb_bin(end-1)-Rjb_bin(end-2))/2;

mLength = length(momag_bin);
RLength = length(Rjb_bin);

for i = 2:mLength
    disp(['Now aggregating loss for magnitude greater than ' num2str(momag_bin(i-1)) ' and less than ' num2str(momag_bin(i))])
    clear mInd subSaved_ecloss RIndRow RIndCol
    mInd = find(ecloss_data.aus_mag>=momag_bin(i-1) & ecloss_data.aus_mag<momag_bin(i));    % finding magnitudes in mag bin
    %subSaved_rjb = saved_rjb(mInd,:);
    subSaved_ecloss = ecloss_data.saved_ecloss(mInd,:);
    for j = 2:RLength
        clear ind TempAggLoss TempPercAggEcLoss TempPercEcLoss Tempcumnu_ecloss TempIntPercEcLoss TempProbExceed
        LossMatrix = zeros(size(subSaved_ecloss));
        %[RIndRow, RIndCol] = find(saved_rjb(mInd,:)>=Rjb_bin(j-1) & saved_rjb(mInd,:)<Rjb_bin(j));
        ind = find(ecloss_data.saved_rjb(mInd,:)>=Rjb_bin(j-1) & ecloss_data.saved_rjb(mInd,:)<Rjb_bin(j));
        %disp([max(RIndRow) max(RIndCol)])
        LossMatrix(ind) = subSaved_ecloss(ind);
        TempAggLoss = sum(LossMatrix,2);
        TempPercAggEcLoss = 100*TempAggLoss./TotalBVal2;
        %disp([size(TempPercAggEcLoss),size(nu(mInd))])
        [trghzd_agg,TempPercEcLoss,Tempcumnu_ecloss] = acquire_riskval(TempPercAggEcLoss, ecloss_data.nu(mInd), 0);        
        TempProbExceed = 1-exp(-Tempcumnu_ecloss);                          % converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year
        TempIntPercEcLoss = zeros(size(mInd));
        for s=length(mInd)-1:-1:1
            TriArea = 1/2*abs(TempPercEcLoss(s+1)-TempPercEcLoss(s))*abs(TempProbExceed(s+1)-TempProbExceed(s));
            RecArea = abs(TempProbExceed(s+1)-TempProbExceed(s))*min(TempPercEcLoss(s+1),TempPercEcLoss(s));
            TempIntPercEcLoss(s) = TempIntPercEcLoss(s+1)+TriArea+RecArea;
        end
        DeAggLoss(i-1,j-1) = TempIntPercEcLoss(1); 
        NumDeAggLoss(i-1,j-1) = length(ind); 
    end
end

%Normalise the Deaggregated loss by the annual blah blah blah
NormDeAggLoss = 100.*DeAggLoss./ann_loss(2);

hf = figure
handle1 = bar3(NormDeAggLoss(:,1:end-1));
z = axis;
z(1) = 0.5;
z(2) = z(2)+0.1;
XTicks = [.5:2:RLength];
XLabels = cellstr(num2str(Rjb_bin(1:2:end)'));
axis(z)

% YTicks = [.5:1:mLength];
% YLabels = cellstr(num2str(momag_bin'));

YTicksTotal = [momag_bin_original(2)-momag_bin_original(1):1:mLength];
YTickLabels ={};

for i=1:length(YTicksTotal)
    YTicks(i) = YTicksTotal(i);
    ind = find(momag_bin_original(i) == momag_labels)
    if isempty(ind)
        YTickLabels{i} = ' ';
    elseif ~isempty(ind)
        YTickLabels{i} = num2str(momag_labels(ind));
    end
end

set(gca,'Zlim',Zlim, 'XTick',XTicks,'XTickLabel',XLabels,'YTick',YTicks,'YTickLabel',YTickLabels,'PlotBoxAspectRatio',[10.5 4 5.09])
view(40,12)

xlabel('Distance (km)','rotation',-10,'Units','Normalized','Position',[0.39 -0.04 0])
ylabel({' Moment';'Magnitude'},'rotation',20,'Units','Normalized','Position',[0.9 -0.08 0])
zlabel('% of annualised loss')

if(finalprint_flag==1|2)
    papersize = [14 11];
    paperposition = [0 0 14 11];
    set(gcf,'Paperunits','cent','PaperSize',papersize,'PaperPosition',paperposition,'PaperOrientation','portrait')

    FigWidth = 11;
    HorizMargin = 1.5;
    FigHeight = 8;
    VertMargin = 1.5;
    NumberFontSize = 10;
    set(gca,'units','cent','position',[HorizMargin,VertMargin,FigWidth,FigHeight],'fontsize',NumberFontSize)

    [nc mc]=size(colormap);
    colormap(flipud(colormap))  % flip colormap so reds show the most damage
    temp=colormap;
    colormap(temp([1,5:42],:))  % playing with colours for best contrast

   if finalprint_flag ==1
        filename ='DeAggHist.eps'; 
        print('-depsc2',[outputdir,'\',filename])
    elseif finalprint_flag==2
         filename ='DeAggHist.jpg';
         print('-djpeg100',[outputdir,'\',filename])
    end
elseif (finalprint_flag ~= 0)
    error({'ERROR: invalid value for finalprint_flag in calc_annloss_deagg_distmag.'; ...
        'Accepted values are 1 or 0.'})
end
