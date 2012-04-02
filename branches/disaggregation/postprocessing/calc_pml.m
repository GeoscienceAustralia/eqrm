function [pml_curve,hf] = calc_pml(saved_ecloss, saved_ecbval2, nu, outputdir, varargin);
%
% [pml_curve] = calc_pml(saved_ecloss, saved_ecbval2, nu, varargin);
%
% calc_pml computes the probable maximum loss (PML) curve for a standard 
% probabilistic EQRM risk run. The PML curve is the main output, however
% options have been included to save the PML curve and/or  plot it as a 
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
% varagin           either, multiple or neither of the following;
%                       's'  to save the PML curve
%                       'p'  to plot the PML curve
%                       'pn' to plot the PML curve with results from a
%                            Newcastle 1989 simulation.
%                       'd'  to display PML curve values to screen.
%
% OUTPUTS:
% pml_curve         [vector (nx3)] containing the PML curve. The first column
%                   contains the probability of exceedance (in one year) values,
%                   the second column contains the direct financial losses
%                   for each of the probabilities of exceedance and the third 
%                   column contains the financial losses as a percentage of the 
%                   total building value.
% hf                [scalar] figure handle of created figure. If no figure
%                   are created hf is empty.
%
% USAGE:
%       [pml_curve] = calc_pml(saved_ecloss, saved_ecbval2, nu, 's','p');
%
% David Robinson
% 7 July 2003

hf = []; %initialise figure handle
optional_args = {varargin{:}};   % get the optional arguments
pml_switch = optional_args{1};

TotalBVal2 = sum(saved_ecbval2);            % calculating the total building value in Newcastle
% if pml_switch == 1;
    AggEcLoss = sum(saved_ecloss,2);            % computed aggregated loss across the city for each eq
% else
%    AggEcLoss = saved_ecloss;
% end
%PercAggEcLoss = AggEcLoss/TotalBVal2*100;  % loss across the city for each eq as a percentage of total building value

% Define return period of interest
endP = 4;
rtrn_per = logspace(1, endP, 15)';
endP = 6;
rtrn_per = logspace(1, endP, 25)';



rtrn_rte = 1./rtrn_per;

trghzd_agg = acquire_riskval(AggEcLoss, nu, rtrn_rte);
      


ProbExceedSmall = 1-exp(-rtrn_rte);


pml_curve = [ProbExceedSmall, trghzd_agg, trghzd_agg/TotalBVal2*100];


% save results to lauch directory if requested
if max(strcmp(optional_args,'s'))==1
    save([outputdir,'\pml_curve.mat'], 'pml_curve','-mat')
end


% create a plot of annualised loss versus return period if requested
if max(strcmp(optional_args,'p'))==1|max(strcmp(optional_args,'pn'))==1
    hf=figure
    semilogy(trghzd_agg/TotalBVal2*100,ProbExceedSmall)
    %semilogy(trghzd_agg,ProbExceedSmall)
    ylabel('Probability of exceedance in one year')
    xlabel('Direct financial loss (%)')
    if max(strcmp(optional_args,'pn'))==1
        set(gca,'YTickLabel',[0.0001 0.001 0.01 0.1])
        hold on
        h100 =plot(7.27,0.0006,'square','MarkerFaceColor',[0 101 92]/193,'MarkerSize',10,'MarkerEdgeColor',[0 101 92]/193);
        h101=text(10.8,0.0037,{'Simulated Newcastle';'1989 Event'},'HorizontalAlignment','center','VerticalAlignment','Cap','FontSize',11);
        % drawing arrow
        h102 = plot([10.5 7.8],[0.0017 0.000775],'k','LineWidth',2);   % line
        h103 = plot(7.8,0.000775,'k^','MarkerFaceColor','k');    % arrowhead
        % Page and figure sizes for publication
        papersize = [14 11];
        paperposition = [0 0 14 11];
        set(gcf,'Paperunits','cent','PaperSize',papersize,'PaperPosition',paperposition,'PaperOrientation','portrait')
    end
end


if max(strcmp(optional_args,'d'))==1
    disp('-----------------------------------------------------------------------')
    disp(' ')
    disp('The PML curve')
    disp(' ')
    disp('Column 1: Probability of Exceedance in one year')
    disp('Column 2: Direct financial loss to city in dollars')
    disp('Column 3: Direct financial loss as a percentage of total building value')
    disp(' ')
    disp(pml_curve)
    disp(' ')
    disp('-----------------------------------------------------------------------')
end
