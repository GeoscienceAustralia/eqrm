function [eqrm_param_T, ecloss_data, varargout] = wrap_risk_plots(load_str, actn_str, outputdir,varargin)
%
%
% wrap_risk_plots is a wrapper function for the key risk plotting and 
% post-processing tools. It handles the management of inputs for the 
% individual plotting tools. That is if load_str==1 it loads all the 
% required inputs, else if load_str==0  the key plotting tool inputs
% are accepted as inputs to wrap_risk_plots. Note that if load_str==0
% it will usually be the case that wrap_risk_plots has already been 
% run with load_str==1. 
%
% INPUTS:
% load_str      [scalar]  
%                   1  => loads all the required inputs (see varargin)
%                   0  => accepts the "key inputs as inputs" (see varargin)
%
% actn_str      [string] plotting tool function name to be used. 
%                   Allowable options include:
%                       'calc_pml'                       
%                       'calc_annloss'
%                       'calc_annloss_deagg_distmag'
%                       'calc_annloss_deagg_sub'
%                       'calc_scenloss_sub'
%                       'calc_scen_loss_stats'
%                       'calc_annloss_deagg_structural'
%                       'calc_annloss_deagg_btype'
%                   
%                   if actn_str is left empty then wrap_risk_plots loads
%                   and returns the key inputs only.
%
% outputdir     [string] Directory path for any saved output files
%                               
% varargin      if load_str==1
%                   varargin{1}: [string] Full path to original setdata 
%                   varargin{2}: [string] Full path to saved ecloss file 
%                   varargin{3}: [cell(1xn)] "extra" inputs for specific 
%                                plotting tools. Note that varargin{3} 
%                                should have 1 entry for each of the 
%                                extra inputs. See "EXTRA INPUTS BY PLOTTING
%                                TOOL" (below) for further information. 
% 
%               if load_str==0
%                   varargin{1}: eqrm_param_T (see OUTPUTS)
%                   varargin{2}: ecloss_data (see OUTPUTS)
%                   varargin{3}: [cell(1xn)] see description for
%                                 varargin{3} when load_str==1
%
% OUTPUTS:
% eqrm_param_T  [structure] standard EQRM setdata structure
% ecloss_data   [structure] containing results of risk simulation. Each of
%               the variables in the saved_ecloss file is stored as a field
%               in ecloss_data. The fileds include aus_mag, b_post89,          
%               b_postcode, b_siteid, b_sub, b_survfact, b_type, b_ufi,            
%               b_use, destring, nu, saved_ecbval2, saved_ecloss and   
%               saved_rjb.
% varargout     Listed by plotting/processing tool
%               'calc_pml'   
%                           (see help calc_pml)
%                           varargout{1} = pml_curve;   
%                           varargout{2} = hf;
%               'calc_annloss' 
%                           (see help calc_ann_loss)             
%                           varargout{1} = ann_loss;
%                           varargout{2} = hf;
%                           varargout{3} = CumAnnLoss;
%               'calc_annloss_deagg_distmag':   
%                           (see help calc_annloss_deagg_distmag)
%                           varargout{1} = NormDeAggLoss;
%                           varargout{2} = hf;
%               'calc_annloss_deagg_sub'    
%                           (see help calc_annloss_deagg_sub)
%                           varargout{1} = annloss_deagg_sub_T;  
%               'calc_scenloss_sub'    
%                           (see help calc_annloss_deagg_sub)     
%                           varargout{1} = scenloss_sub_T; 
%               'calc_scen_loss_stats'
%                           (see help calc_scen_loss_stats)
%                           varargout{1} = scen_loss_stats;
%                           varargout{2} = hf;
%               'calc_annloss_deagg_structural'
%                           (see help calc_annloss_deagg_structural)
%                           varargout{1} = annloss_deagg_structural_T;
%                           varargout{2} = hf;
%               'calc_annloss_deagg_btype'    
%                           (see help calc_annloss_deagg_btype)
%                           varargout{1} = annloss_deagg_btype_T;  
%
%
% EXTRA INPUTS BY PLOTTING TOOL:
%   'calc_pml'                      :  from varargin onwards (see help calc_pml)
%   'calc_ann_loss'                 :  from varargin onwards (see help calc_ann_loss)
%   'calc_annloss_deagg_distmag'    :  from momag_bin onwards (see help calc_annloss_deagg_distmag) 
%   'calc_annloss_deagg_sub'        :  NA  (see help calc_annloss_deagg_sub)
%   'calc_scenloss_sub'             :  from  pre89_flag onwards (see help calc_annloss_deagg_sub)
%   'calc_scen_loss_stats'          :  from  pre89_flag onwards (see help calc_scen_loss_stats)  
%   'calc_annloss_deagg_structural' :  from finalprint_flag (see help calc_annloss_deagg_structural)
%   'calc_annloss_deagg_btype'      :  NA  (see help calc_annloss_deagg_btype)
%
% USEAGE:
% ** 'calc_pml'  
% >> [eqrm_param_T, ecloss_data, pml_curve, hf] = wrap_risk_plots(1, 'calc_pml', 'c:/temp','./setdata_toro.mat','./newc_db_savedecloss.mat',{'p','d','pn','s'});
% >> [eqrm_param_T, ecloss_data, pml_curve, hf] = wrap_risk_plots(1, 'calc_pml', 'c:/temp','./setdata_toro.mat','./newc_db_savedecloss.mat');
% >> [eqrm_param_T, ecloss_data, pml_curve, hf] = wrap_risk_plots(0, 'calc_pml', 'c:/temp', eqrm_param_T,ecloss_data,{'p'});
%
% ** 'calc_ann_loss'
% >> [eqrm_param_T, ecloss_data, ann_loss, hf] = wrap_risk_plots(1, 'calc_annloss', 'c:/temp','./setdata_toro.mat','./newc_db_savedecloss.mat',{'p','d','s'});
% >> [eqrm_param_T, ecloss_data, ann_loss, hf] = wrap_risk_plots(1, 'calc_annloss', 'c:/temp','./setdata_toro.mat','./newc_db_savedecloss.mat');
% >> [eqrm_param_T, ecloss_data, ann_loss, hf] = wrap_risk_plots(0, 'calc_annloss', 'c:/temp', eqrm_param_T,ecloss_data,{'p','s','d'});
%
% ** 'calc_annloss_deagg_distmag'
% >> [eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(1,'calc_annloss_deagg_distmag','c:/temp', './setdata_toro.mat','./newc_db_savedecloss.mat',{[4.5:0.5:6.5],[4.5:0.5:6.5],0:5:100, 1,1,[0,8]});
% >> [eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(0,'calc_annloss_deagg_distmag','c:/temp', eqrm_param_T,ecloss_data,{[5:0.3:6],[5:0.3:6],0:5:140, 0,2,[0,8]});
% >> [eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(1,'calc_annloss_deagg_distmag','c:/temp', './setdata.mat','./perth_db_savedecloss.mat',{[4.5:0.5:7.5],[4.5:7.5],0:5:100, 1,1,[0,4]});
% >> [eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(0,'calc_annloss_deagg_distmag','c:/temp', eqrm_param_T,ecloss_data,{[4.5:0.5:7.5],[4.5:7.5],0:5:100, 1,1,[0,4]});
%
% ** 'calc_annloss_deagg_sub'
% >> [eqrm_param_T, ecloss_data,annloss_deagg_sub_T] = wrap_risk_plots(1, 'calc_annloss_deagg_sub','c:/temp', './setdata_toro.mat','./newc_db_savedecloss.mat');
% >> [eqrm_param_T, ecloss_data,annloss_deagg_sub_T] = wrap_risk_plots(0, 'calc_annloss_deagg_sub','c:/temp', eqrm_param_T,ecloss_data);
%
% ** 'calc_scenloss_sub'
% >> [eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(1, 'calc_scenloss_sub','c:/temp', './setdata_determ_toro.mat','./newc_db_savedecloss.mat',{0,0,0,10});
% >> [eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(0, 'calc_scenloss_sub','c:/temp', eqrm_param_T,ecloss_data,{0,0,0,10});
% >> [eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(0, 'calc_scenloss_sub','c:/temp', eqrm_param_T,ecloss_data,{1,1,1,1});
% >> [eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(1, 'calc_scenloss_sub','c:/temp', './setdata.mat','./perth_db_savedecloss.mat',{0,0,1,10});
%
% ** 'calc_scen_loss_stats'
% >> [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(1,'calc_scen_loss_stats','c:/temp', './setdata_determ_toro.mat','./newc_db_savedecloss.mat',{1,1,1,1,[1,9]});
% >> [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(0,'calc_scen_loss_stats','c:/temp', eqrm_param_T,ecloss_data,{0,0,0,1});
% >> [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(1,'calc_scen_loss_stats','c:/temp', './setdata_determ_toro.mat','./newc_db_savedecloss.mat',{0,0,0,2});
% >> [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(1,'calc_scen_loss_stats','c:/temp', './setdata.mat','./perth_db_savedecloss.mat',{0,0,0,1,[]}); 
%
% ** 'calc_annloss_deagg_structural'
% >> [eqrm_param_T, ecloss_data,annloss_deagg_structural_T,hf] = wrap_risk_plots(1,'calc_annloss_deagg_structural','c:/temp', './setdata_toro.mat','./newc_db_savedecloss.mat',{1,[0,0.08]});
% >> [eqrm_param_T, ecloss_data,annloss_deagg_structural_T,hf] = wrap_risk_plots(0,'calc_annloss_deagg_structural','c:/temp', eqrm_param_T,ecloss_data,{1,[0,0.1]});
% >> [eqrm_param_T, ecloss_data,annloss_deagg_structural_T,hf] = wrap_risk_plots(1,'calc_annloss_deagg_structural','c:/temp', './setdata.mat','./perth_db_savedecloss.mat',{1,[0,0.25]});
% >> [eqrm_param_T, ecloss_data,annloss_deagg_structural_T,hf] = wrap_risk_plots(0,'calc_annloss_deagg_structural','c:/temp', eqrm_param_T,ecloss_data,{1,[0,0.3]});
%
% ** 'calc_annloss_deagg_btype'
% >> [eqrm_param_T, ecloss_data,annloss_deagg_btype_T] = wrap_risk_plots(1, 'calc_annloss_deagg_btype','c:/temp', './setdata_toro.mat','./newc_db_savedecloss.mat');
% >> [eqrm_param_T, ecloss_data,annloss_deagg_btype_T] = wrap_risk_plots(0, 'calc_annloss_deagg_btype','c:/temp', eqrm_param_T,ecloss_data);
% >> 
%==========================================================================
% HISTORY:
% 02-07-04 : Created by David Robinson
% 18-10-04 : the VARARGOUT outputs now reaally are optional. ie: if the
%            user doesn't want them, then he only needs to call this 
%            function with 2 outputs.
% 04-02-05 : 'calc_annloss_deagg_btype' added to wrapper (K.Dale)


spec_varargins={};
if nargin>5; spec_varargins = varargin{3}; end

switch load_str
    case 1
        
        % Unwrap varargin inputs
        setdatafile = varargin{1};
        eclossfile =  varargin{2};
        
        % load THE_PARAM_T
        load(setdatafile);  

        %load ecloss file
        ecloss_data = load(eclossfile);

    case 0
        % Unwrap varargin inputs
        eqrm_param_T = varargin{1};
        ecloss_data =  varargin{2};

end




switch actn_str
   
    case 'calc_pml'
        [pml_curve,hf] = calc_pml(  ecloss_data.saved_ecloss,...
                                    ecloss_data.saved_ecbval2, ...
                                    ecloss_data.nu, ...
                                    outputdir, ...
                                    spec_varargins{:});  %spec_varargins{:} = {varargin}
                                
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = pml_curve;
           varargout{2} = hf;
        end
    case 'calc_annloss'
        [ann_loss,hf, CumAnnLoss] = calc_annloss(   ecloss_data.saved_ecloss, ...
                                        ecloss_data.saved_ecbval2, ...
                                        ecloss_data.nu, ...
                                        outputdir, ...
                                        spec_varargins{:});  %spec_varargins{:} = {varargin}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = ann_loss;
           varargout{2} = hf;
           varargout{3} = CumAnnLoss;
        end
    case 'calc_annloss_deagg_distmag'
        [NormDeAggLoss,hf] = calc_annloss_deagg_distmag( eqrm_param_T, ...
                                                    ecloss_data, ...
                                                    outputdir, ...
                                                    spec_varargins{:});  %spec_varargins{:} = {momag_bin,R_bin, R_extend_flag,finalprint_flag}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = NormDeAggLoss;
           varargout{2} = hf;
        end
    case 'calc_annloss_deagg_sub'
        [annloss_deagg_sub_T]= calc_annloss_deagg_sub(  eqrm_param_T, ...
                                                        ecloss_data, ...
                                                        outputdir, ...
                                                        spec_varargins{:}); % Note spec_varargins{:} = {}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = annloss_deagg_sub_T;
        end
    case 'calc_scenloss_sub'
        [scenloss_sub_T]=calc_scenloss_sub( eqrm_param_T, ...
                                            ecloss_data, ...
                                            outputdir, ...
                                            spec_varargins{:}); %spec_varargins{:} = {pre89_flag, dollars89_flag,med_flag,ev}
                                        
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = scenloss_sub_T;
        end
    case 'calc_scen_loss_stats'
        [scen_loss_stats,hf] = calc_scen_loss_stats(    eqrm_param_T, ...
                                                        ecloss_data, ...
                                                        outputdir, ...
                                                        spec_varargins{:}); % spec_varargins{:} = {pre89_flag, dollars89_flag,resonly_flag,finalprint_flag}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = scen_loss_stats;
           varargout{2} = hf;
        end
    case 'calc_annloss_deagg_structural'
        [annloss_deagg_structural_T, hf]=calc_annloss_deagg_structural( eqrm_param_T,...
                                                                        ecloss_data, ...
                                                                        outputdir, ...
                                                                        spec_varargins{:}); % spec_varargins{:}={finalprint_flag,Ylim}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = annloss_deagg_structural_T;
           varargout{2} = hf;
        end     
    case 'calc_annloss_deagg_btype'
        [annloss_deagg_btype_T]= calc_annloss_deagg_btype(  eqrm_param_T, ...
                                                        ecloss_data, ...
                                                        outputdir, ...
                                                        spec_varargins{:}); % Note spec_varargins{:} = {}
        % take care of optional outputs  
        if(nargout >= 3 )
           varargout{1} = annloss_deagg_btype_T;
        end  
 end
