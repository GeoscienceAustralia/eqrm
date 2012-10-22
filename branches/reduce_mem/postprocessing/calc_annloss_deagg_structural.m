function [annloss_deagg_structural_T, hf]=calc_annloss_deagg_structural(eqrm_param_T,ecloss_data,outputdir,finalprint_flag,Ylim)
%
%
% calc_annloss_deagg_structural dis-aggreagtes the risk in terms of building
% structura types. A bar chart is created showing the annualised loss for the 
% following four different structural types:
% 1) Unreinforced Masonry
% 2) Concrete
% 3) Timber Frame
% 4) Steel Frame
% Note that annualised loss is expressed as a percentage of the total value
% of all buildings in the same structural classification. 
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
% finalprint_flag   [1, 2 or 0]
%                       0 => do not print figures
%                       1 => print eps to outputdir
%                       2 => print jpeg to outputdir
% Ylim              [double: 1x2] y-axis limits. Note that if Ylim is empty
%                   default limits are used. 
%
% OUTPUTS:
% annloss_deagg_structural_T    [structure] with the following fields
%                                   1) 
% hf                            [scalar] figure handle of created figure.
%
% *** See example useage in wrap_risk_plots
%
% Known Bombs: 
% * calc_annloss_deagg_structural will bomb if any of the following 
%   structural types are present: MH, PC1,PC2L,PC2M,PC2H,RM1L,RM1M,RM2L,
%   RM2M, RM2H. 
%
%
% David Robinson 
% 16 July 2004


% Unreinforced Masonry
ecloss_data.b_type(ecloss_data.b_type<=56 & ecloss_data.b_type>=51) =400;
ecloss_data.b_type(ecloss_data.b_type<=35 & ecloss_data.b_type>=34) =400;
% Concrete:
ecloss_data.b_type(ecloss_data.b_type<=50 & ecloss_data.b_type>=42) =300;
ecloss_data.b_type(ecloss_data.b_type<=25 & ecloss_data.b_type>=16) =300;
% Timber Frame
ecloss_data.b_type(ecloss_data.b_type<=41 & ecloss_data.b_type>=37) =200;
ecloss_data.b_type(ecloss_data.b_type<=2 & ecloss_data.b_type>=1) =200;
% Steel Frame
ecloss_data. b_type(ecloss_data.b_type<=15 & ecloss_data.b_type>=3) = 100;    




clear TypeAnnualisedLoss TotBuildTypeVal

Types = unique(ecloss_data.b_type);
nTypes = length(Types);
countTypes = 0; 
for typei = 1:nTypes
    clear indType TypeLoss TypeAggLoss TypePercEcLoss TypeProbExceed TypeIntPercEcLoss 
    indType = find(ecloss_data.b_type == Types(typei));
    TypeLoss = ecloss_data.saved_ecloss(:,indType);
    TypeAggLoss = sum(TypeLoss,2);
    TotBuildTypeVal(typei) = sum(ecloss_data.saved_ecbval2(indType));
    TypePercAggEcLoss = 100*TypeAggLoss./TotBuildTypeVal(typei);
    
    [trghzd_agg,TypePercEcLoss,Typecumnu_ecloss] = acquire_riskval(TypePercAggEcLoss, ecloss_data.nu, 0);
    TypeProbExceed = 1-exp(-Typecumnu_ecloss);                              % converts recurrence rates (cumsum(nu)) to prob. of exceedance in 1 year

    n = length(indType);
    TypeIntPercEcLoss = zeros(size(TypeProbExceed));
    for s=length(TypeProbExceed)-1:-1:1
            TypeTriArea = 1/2*abs(TypePercEcLoss(s+1)-TypePercEcLoss(s))*abs(TypeProbExceed(s+1)-TypeProbExceed(s));
            TypeRecArea = abs(TypeProbExceed(s+1)-TypeProbExceed(s))*min(TypePercEcLoss(s+1),TypePercEcLoss(s));
            TypeIntPercEcLoss(s) = TypeIntPercEcLoss(s+1)+TypeTriArea+TypeRecArea;
    end
    TypeAnnualisedLoss(typei) = TypeIntPercEcLoss(1);
    TypeAggLoss1(typei) = TypePercEcLoss(1);
    countTypes = countTypes +n;
end

% Annualised loss for each building type as a percentage of total annualised loss in Newcastle

%TypeAnnLossPerc = 100*TypeAnnualisedLoss./IntPercEcLoss(1);

hf = figure
hkids=bar(Types,TypeAnnualisedLoss);

%Using GA publication colours
colors(1,1,1:3)=[0 76/176 100/176];             % blue
colors(1,2,1:3)=[187/288 101/288 0];            % brown
colors(1,3,1:3)=[136/199 32/199 31/199];        % red
colors(1,4,1:3)=[0 101 92]/193;                 % green/aqua
% set(get(hkids,'Children'),'CData', colors);

%title('Annualised loss by building type')
ylabel('Annualised Loss (%)')
%hx=xlabel('Building Type')
% Doing Xtick Labels
set(gca,'XTickLabel',[])
if ~isempty(Ylim),set(gca,'Ylim',Ylim); end
text(100,-0.002,{'Steel';'Frame'},'HorizontalAlignment','center','VerticalAlignment','Cap')
text(200,-0.002,{'Timber';'Frame'},'HorizontalAlignment','center','VerticalAlignment','Cap')
text(300,-0.002,{'Concrete';''},'HorizontalAlignment','center','VerticalAlignment','Cap')
text(400,-0.002,{'Unreinforced';'Masonry'},'HorizontalAlignment','center','VerticalAlignment','Cap')
%set(hx,'Position',[249.7481   -0.015   17.3205])


annloss_deagg_structural_T.Types= Types;
annloss_deagg_structural_T.TypeAnnualisedLoss = TypeAnnualisedLoss;

if finalprint_flag==1|finalprint_flag==2
    % Page and figure sizes for publication
    papersize = [14 11];
    paperposition = [0 0 14 11];
    set(gcf,'Paperunits','cent','PaperSize',papersize,'PaperPosition',paperposition,'PaperOrientation','portrait')

    FigWidth = 11;
    HorizMargin = 1.5;
    FigHeight = 8;
    VertMargin = 1.5;
    NumberFontSize = 10;
    set(gca,'units','cent','position',[HorizMargin,VertMargin,FigWidth,FigHeight],'fontsize',NumberFontSize)

    % printing figure eps file
    filename1 ='BuildTypeBar';
    if finalprint_flag ==1
        print('-depsc2', [outputdir, '/', filename1,'.eps'])
    elseif finalprint_flag ==2
        print('-djpeg100', [outputdir, '/', filename1,'.jpg'])
    end    
end
