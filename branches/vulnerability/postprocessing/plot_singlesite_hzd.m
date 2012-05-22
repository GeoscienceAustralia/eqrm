function [plot_haz] = plot_singlesite_hzd(filename,actn_str,location,plotvalue,xaxis_scale,haz_type,fig_opt)
%==========================================================================
% DESCRIPTION:
%   plot_singlesite_hzd can be used to display the results of a single site
%   earthquake hazard assessment. The results are displayed as a uniform
%   hazard spectra if actn_str = 'UniformHzd' or uniform period hazard if 
%   actn_str = 'UniformPer'.
%==========================================================================
% INPUTS:
% 	filename          [string] full path filename for hazard file. Note that
%                       the filename is usually of the form [site_loc,'_db_hzd.mat'].
%                       The *_hzd.mat file must contain: 
%                           1. periods:         [np x 1 vector] RSA periods 
%                           2. site_pos:        [ns x 2 matrix] locations of sites
%                           3. rtrn_per:        [1 x nr vector] return periods
%                           4. hzd_rock:        [ns x nr x np]  bedrock hazard values
%                           5. hzd_regolith:    [ns x nr x np]  regolith hazard values
%                           6. THE_PARAM_T      [structure] containing setdata
%                                               inputs
% 	actn_str          [string]
%                         'UniformHzd' =>   to plot uniform hazard spectra
%                         'UniformPer' =>   to plot uniform period hazard
%                         'HazPML'     =>   to plot a pml of hazard
% 	location          [matrix nx2]
%                         n => rows representing n different locations
%                         column 1 => longitude | column 2 => latitude
%                       Note that plot_singlesite_hzd will snap to the site in
%                       SITE_POS that is nearest the desired site in LOCATION. 
% 	plotvalue            [vector 1xm]
%                         one plot will be drawn for each y value. Each element of PLOTVALUE
%                         must be in 
%                           (1) periods if actn_str = 'UniformPer', or (note
%                               period = 0 is not shown if xaxis_scale='log').
%                           (2) rtrn_per if actn_str = 'UniformHzd'.
% 	xaxis_scale           [string]
%                               'lin'   => linear scale used for x-axis
%                               'log'   => log scale used for x-axis [default]
% 	haz_type              [string]
%                               'rock'      => use bedrock hazard values i.e. hzd_rock
%                               'regolith'  => use regolith hazard values i.e. hzd_regolith
% 	fig_opt               [string]
%                               'new'       => a new figure for each location
%                               'single'    => all locations shown on the one figure
%==========================================================================
% Note:
% * a warning is given if the requested site is more than approx. 10km from
%   the nearest site in the loaded hazard grid. It is the users
%   responsibility to ensure that results are interpreted correctly.
%==========================================================================
% DEMO:
% >> [tmp]=plot_singlesite_hzd('c:\temp\newc_db_hzd.mat','UniformHzd',[151.65,-33.15;151.5,-32.9; 151.6,-33],[500 2500],'lin','rock','single');
% >> [tmp]=plot_singlesite_hzd('c:\temp\newc_db_hzd.mat','HazPML',[151.65,-33.15;151.5,-32.9; 151.6,-33],[0 1/3.3 1],'lin','rock','single');
%==========================================================================
% BOMBS: 
%   (1) if length(plotvalue)>7
%   (2) if the number of unique locations > 3. To be safe set length(locations)<=3. 
%==========================================================================
% HISTORY:
%   17-10-03 : Created by David Robinson
%   11-11-03 : added a band aid solution that fixes the BOMB_#1
%               - the line colors now do a "loop" of  ('k','b','r','y','g','c','m')
%==========================================================================

load(filename)
[n_loc,m_loc] = size(location);
n_pv = length(plotvalue);
closest = [];
ind = [];
mind = [];
for i = 1:n_loc
    % note that this distance is computed in euclidean lon/lat space (I think the result would be the same if km were used) 
    [tmp_ind,tmp_closest,tmp_mind] = find_closest(site_pos,location(i,:),'euclidean');  
    ind(i) = tmp_ind; closest(i,:)=tmp_closest; mind(i)=tmp_mind;
    clear tmp_ind tmp_closest tmp_mind
end


% check to see if any two or more vectors/points in location have found the same
% vector/point in site_pos
[uclocs, ind_uclocs] = unique(closest(:,1));  % uclocs = the unique closest locations
[n_uc,m_uc] = size(uclocs);
uclocs = closest(ind_uclocs,:);
if n_uc~=n_loc
    disp('  ')
    disp('=================================================================')
    disp('One or more of the points in location has returned the same')
    disp('position in site_pos. Analysis will be conducted on the following')
    disp('site(s) in the hazard file (i.e. the points in site_pos):')
    disp(uclocs)
    disp('These relate to the following requested location(s)')
    disp(location(ind_uclocs,:))
    disp('=================================================================')
    disp(' ')
end


% check that the distance does not exceed 10km
% if so warn user
dist = vincenty_inverse(location(ind_uclocs,2),location(ind_uclocs,1),uclocs(:,2),uclocs(:,1));
dist = dist./1000;  % turn them into km
ind2 = find(dist>=10);
if ~isempty(ind2)
    disp(' ')
    disp('=================================================================')
    disp('WARNING: One or more of the points in location is greater')
    disp('than 10km from a point in site_pos. The requested points that')
    disp('are greater than 10km from any hazard estimates are:')
    disp(location(ind2,:))
    disp('The actual distance in km is:')
    disp([num2str(dist(ind2,:))])
    disp('=================================================================')
    disp('  ')
end

% Now set up the hazard value 3D matrix
switch haz_type
    case  'rock'    
        hzd = hzd_rock;
    case  'regolith'  
        hzd = hzd_regolith;
end

figure
% setup colur and pattern vectors for 
if( length(plotvalue) <= 7 )
    colours4plotvalue={'k','b','r','y','g','c','m'};
else
    colours4plotvalue = LOC_gen_colorspec(length(plotvalue));   %%_11-11-03
    colours4plotvalue = [colours4plotvalue(:)]';  %% make it a row
end
patterns4locations = {'-',':','--','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'};

% Now we are ready to extract the information we desire. 
counter = 1;
lgd_text={};
for j= 1:n_uc
    switch actn_str
        case 'UniformHzd'
            yaxis_scale = 'lin';
            for i = 1:n_pv   % loop over the plotvalues
                ind_uh = find(rtrn_per== plotvalue(i));
                tmp_y = hzd(ind(ind_uclocs(j)),ind_uh,:);
                tmp_y = reshape(tmp_y,1,length(periods),1);
                h(counter) = LOC_do_plot(periods,tmp_y,xaxis_scale,yaxis_scale,char(colours4plotvalue(i)),char(patterns4locations(j)));
                lgd_text{counter,1} = ['Location: ', num2str(location(ind_uclocs(j),1)),', ',num2str(location(ind_uclocs(j),2)) ...
                        ,' - Return Period: ',num2str(plotvalue(i)),' years'];
                xlabel('RSA period (s)');
                ylabel('Hazard (g)');
                plot_haz.UniformHzd(counter,:) = tmp_y(:)';
                plot_haz.Return_Period(counter) = plotvalue(i);
                plot_haz.location(counter,:) = location(ind_uclocs(j),1:2);
                plot_haz.RSA_period=periods;
                counter = counter+1;
                switch fig_opt
                    case 'new'   %create a new figure for each location. 
                        figure
                end               
            end  % end of loop over plotvalues
        case 'UniformPer' 
            yaxis_scale = 'lin';
            for i = 1:n_pv      % loop over the plotvalues
                ind_p = find(periods== plotvalue(i));
                tmp_y = hzd(ind(ind_uclocs(j)),:,ind_p);
                tmp_y = reshape(tmp_y,1,length(rtrn_per),1);
                h(counter) = LOC_do_plot(rtrn_per,tmp_y,xaxis_scale,yaxis_scale,char(colours4plotvalue(i)),char(patterns4locations(j)));
                lgd_text{counter,1} = ['Location: ', num2str(location(ind_uclocs(j),1)),', ',num2str(location(ind_uclocs(j),2)) ...
                        ,' - RSA Period: ',num2str(round(1000*plotvalue(i))/1000),' sec'];
                xlabel('Return period (years)');
                ylabel('Hazard (g)');
                plot_haz.UniformPer(counter,:) = tmp_y(:)';
                plot_haz.RSA_period(counter) = plotvalue(i);
                plot_haz.location(counter,:) = location(ind_uclocs(j),1:2);
                plot_haz.Return_Period = rtrn_per;
                counter = counter+1;
                switch fig_opt
                    case 'new'   %create a new figure for each plotvalue. 
                        figure
                end
            end  % end of loop over plotvalues
         case 'HazPML'  % note that you should set xaxis_scale='lin' in input to plot_singlesite_hzd
             yaxis_scale = 'log';
            for i = 1:n_pv      % loop over the plotvalues
                ind_p = find(periods== plotvalue(i));
                tmp_x = hzd(ind(ind_uclocs(j)),:,ind_p);
                tmp_x = reshape(tmp_x,1,length(rtrn_per),1);
                probExceed = 1-exp(-1./rtrn_per);
                h(counter) = LOC_do_plot(tmp_x,probExceed,xaxis_scale,yaxis_scale,char(colours4plotvalue(i)),char(patterns4locations(j)));
                lgd_text{counter,1} = ['Location: ', num2str(location(ind_uclocs(j),1)),', ',num2str(location(ind_uclocs(j),2)) ...
                        ,' - RSA Period: ',num2str(round(1000*plotvalue(i))/1000),' sec'];
                xlabel('Hazard (g)');
                ylabel('Probability of Exceedance in 1 Year');
                % now lets make the y axis labels easier to read
                if i==1 & j==1
                    y_labels = 10.^str2num(get(gca,'YtickLabel'));
                    set(gca,'YTickLabel',num2str(y_labels)) 
                end
                plot_haz.HazPML(counter,:) = tmp_x(:)';
                plot_haz.RSA_period(counter) = plotvalue(i);
                plot_haz.location(counter,:) = location(ind_uclocs(j),1:2);
                plot_haz.Return_Period = rtrn_per;
                plot_haz.ProbExceed = probExceed;
                counter = counter+1;
                switch fig_opt
                    case 'new'   %create a new figure for each plotvalue. 
                        figure
                end
            end  % end of loop over plotvalues
                
                
    end  % end of action_str switch
    
    switch fig_opt
        case 'new'   %create a new figure for each location. 
            figure
    end
end   % end of loop over location. 

% construct legend if fig_opt = 'single'
switch fig_opt
    case 'single'
        switch actn_str
            case 'UniformPer'
                legend(h,lgd_text,2)
            case 'UniformHzd'
                legend(h,lgd_text,1)
            case 'HazPML'
                legend(h,lgd_text,1)    
        end
end
        

% ----------------------------------------------
% Local function for generating the plots
function h = LOC_do_plot(xvalue,yvalue,xaxis_scale,yaxis_scale,line_colour,line_style)

switch xaxis_scale
    case 'lin'
        switch yaxis_scale
            case 'lin'
                h = plot(xvalue,yvalue,'LineStyle',line_style, 'color',line_colour,'linewidth',2);
                %h = plot(xvalue,yvalue,'color',line_colour);
                hold on
            case 'log'
                h = semilogy(xvalue,yvalue,'LineStyle',line_style, 'color',line_colour,'linewidth',2);
                hold on    
        end
    case 'log'
        switch yaxis_scale
            case 'lin'
                h = semilogx(xvalue,yvalue,'LineStyle',line_style, 'color',line_colour,'linewidth',2);
                %h = semilogx(xvalue,yvalue,'color',line_colour);
                hold on
            case 'log'
                h = loglog(xvalue,yvalue,'LineStyle',line_style, 'color',line_colour,'linewidth',2);
                hold on
        end
end
%==========================================================================
% END of SUBFUNCTION
%==========================================================================
function [varargout] = LOC_gen_colorspec(varargin)
	%%
    %% USAGE:
    %%   mode_#1a:  >> a_char_col                  = LOC_gen_colorspec
    %%   mode_#1b:  >> [a_char_col, a_str_list_CE] = LOC_gen_colorspec
    %%
    %%   mode_#2a:  >> a_char_col                  = LOC_gen_colorspec(10)
    %%   mode_#2b:  >> [a_char_col, a_str_list_CE] = LOC_gen_colorspec(10)
    %%
    %%   mode_#3:   >> a_color_name_str            = LOC_gen_colorspec('r')
    
	a_standard_char_col     = char('k',      'b',      'r',  'y',      'g',      'c',    'm');
	a_standard_str_list_CE  = {    'black';  'blue';  'red'; 'yellow'; 'green'; 'cyan';  'magenta'}; 
    
    %% work out if we're in USAGE_MODE#3:
    if( (nargin==1) && ischar(varargin{1}) )
        %% then we are being asked to return the NAME of a colour, given
        %% it's 1 char colorspec value
        the_input_char = varargin{1};
        tmp_tf_vec     = strcmp( cellstr(a_standard_char_col), the_input_char);
        
        if( any(tmp_tf_vec==1) )
            varargout{1} = a_standard_str_list_CE{tmp_tf_vec};
            return
        else
            msgbox('I could NOT determine your colour NAME !! ','ATTENTION:','error');
            varargout{1} = '';
            return
        end
    end
        
    %% if we've made it to here then we're being called by usage modes 1,2
    if(nargin==0)
      num_elements_required = length(a_standard_char_col);
    else
      num_elements_required = varargin{1};
    end
    
	NUM_UNIQUE_COLORS    = length(a_standard_char_col);
	% get a color for each zone(YES some colors could be used multiple times)
	for kk=1:num_elements_required
        an_int = mod(kk, NUM_UNIQUE_COLORS);
        if(an_int==0)
          the_color_char = a_standard_char_col(NUM_UNIQUE_COLORS); %% take the last one
          the_color_name = a_standard_str_list_CE{NUM_UNIQUE_COLORS};
        else
          the_color_char = a_standard_char_col(an_int); 
          the_color_name = a_standard_str_list_CE{an_int};
        end
        the_color_col(kk,1)      = the_color_char;
        the_color_names_CE{kk,1} = the_color_name;
	end
	
    varargout{1} = the_color_col;
    
    %% take care of any optional outputs
    if(2==nargout)
        varargout{2} = the_color_names_CE;
    end
%==========================================================================
% END of SUBFUNCTION
%==========================================================================
