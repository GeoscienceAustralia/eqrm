function THE_PREP_LOC_T = prep_locations(run_type_str, varargin) 
%====================================================================
% DESCRIPTION:
%  A "lazy" merge of the PREP_GRID() and PREP_SITES() functions.
%====================================================================
% USAGE:
%         >> run_type_str   = '-hazard'
%         >> THE_PREP_LOC_T = prep_locations( run_type_str,         ...
%                                             grid_flag,            ... 
%                                             site_loc,             ... 
%                                             small_site_flag,      ... 
%                                             SiteInd,              ...              
%                                             qa_switch_watercheck, ... 
%                                             inputdir);
%
%         >> run_type_str   = '-risk' OR '-risk_from_hazard'
%         >> THE_PREP_LOC_T = prep_locations( run_type_str,   ...
%                                             THE_PARAM_T,    ... 
%                                             sitebdfile) 
%
%         >> run_type_str   = '-risk_with_site_selection'
%         >> THE_PREP_LOC_T = prep_locations( run_type_str,   ...
%                                             THE_PARAM_T,    ... 
%                                             THE_IN_PREP_LOC_T) 
%====================================================================
% INPUTS:
%   run_type_str :  a string that defines the run_type that the user 
%                   wants.  Allowed run_type strings are:
%
%                         '-hazard'
%                          '-risk' 
%                          '-risk_from_hazard'
%
% Depending on the supplied RUN_TYPE_STR, the ADDITIONAL input arguments
% are also required:
%
%   '-hazard' ------------->    1.)  grid_flag            
%                               2.)  site_loc             
%                               3.)  small_site_flag      
%                               4.)  SiteInd              
%                               5.)  qa_switch_watercheck 
%                               6.)  inputdir
%
%  '-risk_from_hazard' 
%          OR
%  '-risk' ----------------->  1.) THE_PARAM_T
%                              2.) sitebdfile
%====================================================================
% OUTPUTS:
%  THE_PREP_LOC_T : a User defined type, that *MUST* have the following
%                   fields:
%                               .b_lon        
% 								.b_lat   
%                               .nsites    
%                               .b_soil  
%
%                     IFF the run_type is either '-risk' OR '-risk_from_hazard'
%                     then the additional fields are also added to the existing 
%                     HAZARD fields:
%                     
% 								.b_siteid             
% 								.b_type               
% 								.b_usage              
% 								.b_use                
% 								.b_floorA             
% 								.b_survfact        
% 								.b_sub              
% 								.b_postcode         
% 								.b_ufi             
% 								.b_post89          
% 								.b_type_hazus      
% 								.b_replace_cost_pm2 
% 								.b_content_cost_pm2
%
%                    IFF the run type is RISK_WITH_SITE_SELECTION, then
%                    the additional fields are also added to the existing
%                    RISK fields:
%
%                               .trunc_indx              
% 								.b_replace_cost_pm20 
% 								.b_content_cost_pm20
%====================================================================
% INTEL:     Known to be called from:
%                     do_eqhzd
%                     do_bdamage
%====================================================================
% HISTORY:
%  01-04-2004 : Created 
%
%  04-05-2004 :  Removed ".in_land" from the Returned STRUCTS and commented
%                out the call to the LOC_watercheck function - as discussed
%                with David Robinson (10:30am)
%
%                NOTE: the "in_land" field doesn't seem to be used anywhere
%                      in the EQRM software.
%====================================================================
	switch(lower(run_type_str) )
        case '-hazard'
             tmp_T = LOC_prep_grid( varargin{:} );
        %--------------------------------------------------------------------     
        case {'-risk', '-risk_from_hazard'}
             tmp_T = LOC_prep_sites( varargin{:} );
        %--------------------------------------------------------------------     
        case '-risk_with_site_selection'
            tmp_T = LOC_reduce_site_selection( varargin{:} );
        %--------------------------------------------------------------------     
        otherwise
            error('###_ERROR:  UNknown action string inside <%s>', mfilename);
	end

    THE_PREP_LOC_T = tmp_T;

    %====================================================================
    % Make it clear that the returned struct, *MUST* have specific data fields.
    %====================================================================
    
    %% Here are *NECASSARY* fields for ANY run_type
    if( strcmp(lower(run_type_str),  '-hazard')                  | ...
        strcmp(lower(run_type_str),  '-risk')                    | ...
        strcmp(lower(run_type_str),  '-risk_from_hazard')        | ...
        strcmp(lower(run_type_str),  '-risk_with_site_selection')       )
        %%
        fname = 'b_lon'  ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end    
		fname = 'b_lat'  ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'nsites' ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end 
		fname = 'b_soil' ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
    end
    
    %% do additional filename checks for a RISK type run
    if( strcmp(lower(run_type_str),  '-risk')                    | ...
        strcmp(lower(run_type_str),  '-risk_from_hazard')        | ...
        strcmp(lower(run_type_str),  '-risk_with_site_selection')      )
        %%
        fname = 'b_siteid'          ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_type'            ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_usage'           ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_use'             ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_floorA'          ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_survfact'        ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
		fname = 'b_sub'             ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end 
		fname = 'b_postcode'        ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end 
		fname = 'b_ufi'             ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
		fname = 'b_post89'          ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
		fname = 'b_type_hazus'      ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
		fname = 'b_replace_cost_pm2';  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end 
		fname = 'b_content_cost_pm2';  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end
    end
    
    
    %% do additional filename checks for a RISK type run with REDUCED_SITE_SELECTION
    if( strcmp(lower(run_type_str),  '-risk_with_site_selection')  )
        %%
        fname = 'trunc_indx'          ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_replace_cost_pm20' ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
		fname = 'b_content_cost_pm20' ;  if(~isfield(THE_PREP_LOC_T, fname)), error('UNknown filed <%s>', fname);, end   
    end
    
    
%==========================================================================
% END of MAIN function
%==========================================================================
%%%
%%
%
function THE_PREP_GRID_T  = LOC_prep_grid( grid_flag,            ...
                                           site_loc,             ...
                                           small_site_flag,      ...
                                           SiteInd,              ...
                                           qa_switch_watercheck, ...
                                           inputdir)
%====================================================================
% DESCRIPTION:     
%====================================================================
%  OUTPUTS:    A STRUCT that has the fieldnames
%                   1.) b_lon        
% 					2.) b_lat   
% 					3.) nsites    
%                   4.) b_soil  
%====================================================================
%       INTEL:     Known to be called from:
%                  >> do_eqhzd
%====================================================================
%     HISTORY:
% 08-04-2003:    0.) Converted SCRIPT to a FUNCTION
%                1.) created a FULLPATH filename for the LOAD function
%                2.) the "old" WATERCHECK function is now a SUBfunction
%                    of this file.
% 01-04-2003 :  0.) The output struct, NO LONGER returns the field 
%                   "SiteLocations"  
%                1.) The output struct, NO LONGER returns the field
%                   "site_classes", instead it returns the field 
%                   "b_soil".  
%
% 04-05-2004:    Removed ".in_land" from the Returned STRUCT and commented
%                out the call to the LOC_watercheck function - as discussed
%                with David Robinson (10:30am)
%
%                NOTE: the "in_land" field doesn't seem to be used anywhere
%                      in the EQRM software.
%====================================================================
%_###
%_###
%====================================================================
% prep_grid is an m-script to prepare a grid for hazard calculation
% It is called by do_eqhzd.
%
% It requires a site location mat-file with name of form [site_loc,'_par_site']
% Depending on the value of small_site_flag it will take a subset or all of
% the sites:
%           small_site_flag = 0      use full set of site
%           small_site_flag = 1      use a subset of sites 
%                                    define the sites in SiteInd (setdata)  
%
%                                                       David Robinson
%                                                       Last Updated 01/07/02

%--------------------------------------------
% default outputs from function
THE_PREP_GRID_T.b_lon         = [];
THE_PREP_GRID_T.b_lat         = [];
THE_PREP_GRID_T.nsites        = [];
THE_PREP_GRID_T.b_soil        = [];
%--------------------------------------------

if grid_flag ==1   % grid produced by GIS people 
    tmp_full_path_file = check4_local_eqrm_input(inputdir,[site_loc,'_par_site.mat'])
    load(tmp_full_path_file);
    %%_##################################################################
elseif grid_flag ==2    % grid produced by GenerateGrid.m
    
    tmp_full_path_file = check4_local_eqrm_input(inputdir,[site_loc,'_par_site_uniform.mat'])
    %     tmp_full_path_file = ...
    %         [get_eqrm_path_info('-resources_data'), filesep, site_loc,'_par_site_uniform'];
    load(tmp_full_path_file,'AllLocations','SiteLocations','inside1','lats','lons','site_classes');
    try, site_classes  =  site_classes(inside1~=0); catch end
    %%_##################################################################
end

% make sure Longitude is in the first column - only works for Australia
if max(SiteLocations(:,2))> max(SiteLocations(:,1))
    SiteLocations = fliplr(SiteLocations);
end   % otherwise the vector is already ok. 

if small_site_flag == 0;                    % use the full set. 
    b_lon = SiteLocations(:,1);             % longitude of sites
    b_lat = SiteLocations(:,2);             % latitude of sites
    nsites = length(b_lon);                 % calculating the total number of sites
elseif small_site_flag == 1;                % use a subset of sites defined by SiteInd (see setdata)
    b_lon = SiteLocations(SiteInd,1);               % longitude of sites
    b_lat = SiteLocations(SiteInd,2);               % latitude of sites
    nsites = length(b_lon);                         % calculating the total number of sites
    SiteLocations = SiteLocations(SiteInd,:);
    try, site_classes = site_classes(SiteInd,:); catch end;   % only define this field if the site_classes exist
end

% run a check to see if any of the sites lie in the water DR.
% DR (Action) - it may be possible to remove 
%in_land = LOC_watercheck(b_lon, b_lat, qa_switch_watercheck);

% take care of return structure:
try, THE_PREP_GRID_T.b_lon         =  b_lon;,         catch end
try, THE_PREP_GRID_T.b_lat         =  b_lat;,         catch end
try, THE_PREP_GRID_T.nsites        =  nsites;,        catch end
try, THE_PREP_GRID_T.b_soil        =  site_classes;,  catch end

%==========================================================================
% END of SUB function
%==========================================================================
function PREP_SITES_T = LOC_prep_sites(THE_PARAM_T, sitebdfile)
	%====================================================================
	% ATTENTION:     This M-file used to be a SCRIPT 
	%====================================================================
	% DESCRIPTION:     All of the variables that used to be defined inside
	%                  the "old" script file, are now assigned to a STRUCT.
	%====================================================================
	% INPUTS:
	%   THE_PARAM_T : a struct data type containing the simulation PARAMS
	%====================================================================
	% OUTPUTS: 
	%   PREP_SITES_T    : a "massive" struct data type 
	% 							nsites               
	% 							b_siteid             
	% 							b_lat                
	% 							b_lon                 
	% 							b_type               
	% 							b_usage              
	% 							b_use                
	% 							b_floorA             
	% 							b_survfact           
	% 							b_sub                 
	% 							b_postcode            
	% 							b_ufi                
	% 							b_post89             
	% 							b_type_hazus         
	% 							b_soil               
	% 							b_replace_cost_pm2    
	% 							b_content_cost_pm2   
    %====================================================================
	% INTEL:     Known to be called from:
	%              >> do_bdamage
	%====================================================================
	% HISTORY:
	% 05-05-2003:    0.) Converted SCRIPT to a FUNCTION
	%                1.) added fullpath to resource file being LOADED
	%                2.) replaced TEXTREAD with CNT_TEXTREAD (which IS MCC
	%                    friendly)
    %
    % 01-04-2004:    1.) The output struct, NO LONGER returns the field
    %                   "site_classes".  The existing field called "b_soil"
    %                   contains the same information ..... so it was
    %                   decided to delete "site_classes".
	%====================================================================
	%_###
	%_###
	%====================================================================
	
	% script to prepare variables loaded from site info file.
	% Glenn Fulford 21/4/02.
	
	tmp_full_path_file = check4_local_eqrm_input(THE_PARAM_T.inputdir,sitebdfile)
	load(tmp_full_path_file);
	%==========================================================================
	% >> load sitedb_newc
	% >> whos
	%   Name                Size                   Bytes  Class
	% 
	%   all_postcodes     125x1                     1000  double array
	%   all_suburbs       125x1                    10066  cell array
	%   b_sitemat        6305x12                  605280  double array
	%   b_soil           6305x1                   390910  cell array
	%==========================================================================
	
	% filter_flag = 1;
	% myfilter = (b_postcode>=2295 & b_postcode <= 2320);
	
	% if(filter_flag == 1)
	%     b_sitemat = b_sitemat(myfilter,:);
	% end
                     
	% set the key variables
	nsites       = length(b_sitemat(:,1));
	b_siteid     = b_sitemat(:,1);
	b_lat        = b_sitemat(:,2);
	b_lon        = b_sitemat(:,3); 
	b_type       = b_sitemat(:,4);
	b_floorA     = b_sitemat(:,6); % in sq metres!
	b_survfact   = b_sitemat(:,7);
	b_sub        = b_sitemat(:,8); 
	b_postcode   = b_sitemat(:,9); 
	b_ufi        = b_sitemat(:,10);
	b_post89     = b_sitemat(:,11);
	b_type_hazus = b_sitemat(:,12);
	b_soil       = char(b_soil);
	site_classes = b_soil;
	b_replace_cost_pm2   = b_sitemat(:,13);
	b_content_cost_pm2   = b_sitemat(:,14);
	
	if (THE_PARAM_T.('b_usage_type_flag') == 1);
        %The user has selected the hazus usage clasification
	b_usage      = b_sitemat(:,5);
	elseif (THE_PARAM_T.('b_usage_type_flag') == 2);
        %The user has selected the Functional classification of buildings usage clasification
	b_usage      = b_sitemat(:,15);
	else
        %The user has selected something wrong.  
        error('b_usage_type_flag value is out of scope.')
	end
	b_use        = b_usage; % alias
	
	clear b_sitemat;
	
	
	% George Walker's suggested modifications for contents damage
	if (THE_PARAM_T.('aus_contents_flag') == 1) % reset the slavagability of contents and set RES
                                % contents values to 60% of current value.
        for asite = 1:nsites   
            if b_usage(asite)<=6 | ... % only valid for residential buildings
                    ((b_usage(asite) <=10 | b_usage(asite) == 24 | b_usage(asite) == 29) & ...
                    (THE_PARAM_T.('b_usage_type_flag') == 2))
                b_content_cost_pm2(asite) =b_content_cost_pm2(asite) *0.6;
            end
        end
	end
	
	if (THE_PARAM_T.('hazus_btypes_flag') == 1);
        b_type = b_type_hazus;
	end
	
	%f_area = 15*ones(nsites, 1); %area in square m;
	%f_area = f_area * 36; % area in sq feet. 
	
	%--------------------------------------------
	% assign the return data
	PREP_SITES_T.nsites               = nsites;
	PREP_SITES_T.b_siteid             = b_siteid;
	PREP_SITES_T.b_lat                = b_lat;
	PREP_SITES_T.b_lon                = b_lon; 
	PREP_SITES_T.b_type               = b_type;
	PREP_SITES_T.b_usage              = b_usage;
	PREP_SITES_T.b_use                = b_use;
	PREP_SITES_T.b_floorA             = b_floorA;
	PREP_SITES_T.b_survfact           = b_survfact;
	PREP_SITES_T.b_sub                = b_sub; 
	PREP_SITES_T.b_postcode           = b_postcode; 
	PREP_SITES_T.b_ufi                = b_ufi;
	PREP_SITES_T.b_post89             = b_post89;
	PREP_SITES_T.b_type_hazus         = b_type_hazus;
	PREP_SITES_T.b_soil               = b_soil;
	PREP_SITES_T.b_replace_cost_pm2   = b_replace_cost_pm2; 
	PREP_SITES_T.b_content_cost_pm2   = b_content_cost_pm2;
    
%==========================================================================
% END of SUB function
%==========================================================================
function [REDUCE_SITE_SELECTION_T] = LOC_reduce_site_selection( THE_PARAM_T, ...
                                                                PREP_LOC_T)
%====================================================================
% ATTENTION:     This M-file used to be a SCRIPT
%====================================================================
% DESCRIPTION:     All of the variables that used to be defined inside
%                  the "old" script file, are now assigned to a STRUCT.
%====================================================================
% INPUTS:
%   THE_PARAM_T : a struct data type containing the simulation PARAMS
%
%   PREP_LOC_T  : a struct data type previously created by the
%                 PREP_LOCATIONS function.  It must be a RISK run
%====================================================================
% OUTPUTS: 
%   REDUCE_SITE_SELECTION_T : a struct with the fields:
%
% 			.trunc_indx  
% 			.b_replace_cost_pm20 
% 			.b_content_cost_pm20 
% 			.b_siteid     
% 			.b_ufi       
% 			.b_lat       
% 			.b_lon        
% 			.b_type      
% 			.b_use       
% 			.b_floorA    
% 			.b_soil        
% 			.b_survfact  
% 			.b_sub       
% 			.b_postcode  
% 			.b_post89    
% 			.nsites      
% 			.b_replace_cost_pm2 
% 			.b_content_cost_pm2 
% 			.b_usage     
% 			.b_type_hazus 
%====================================================================
% INTEL:     Known to be called from:
%              >> do_bdamage
%====================================================================
% HISTORY:
% 05-05-2003:    0.) Converted SCRIPT to a FUNCTION
%
% 02-04-2004:    1.) updated the HELP block of this function.  The contents
%                    of the output struct had been modified ..... but the
%                    HELP block hadn't been
%                2.) In keeping consistancy with the PREP_LOCATIONS()
%                    function, the "site_classes" field is NO longer 
%                    a field of the returned output struct.
%                2.) In keeping consistancy with the PREP_LOCATIONS()
%                    function, the "in_land" field has been added as 
%                    a field of the returned output struct.
%
%  04-05-2004 :  Removed ".in_land" from the Returned STRUCTS and commented
%                out the call to the LOC_watercheck function - as discussed
%                with David Robinson (10:30am)
%
%                NOTE: the "in_land" field doesn't seem to be used anywhere
%                      in the EQRM software.
%====================================================================
%_###
%_###
%====================================================================
%this script reduces the selection of sites to a smaller number, for debugging purposes.
% It shouils only be called if the flag small_site_seletion==1
% Glenn Fulford 50/5/02;

%--------------------------------------------
% define some LOCAL variables
small_site_flag = THE_PARAM_T.('small_site_flag');
% single_site     = THE_PARAM_T.('single_site');
%--------------------------------------------
nsites     = PREP_LOC_T.nsites;   
b_siteid   = PREP_LOC_T.b_siteid; 
b_lat      = PREP_LOC_T.b_lat;    
b_lon      = PREP_LOC_T.b_lon;     
b_type     = PREP_LOC_T.b_type;    
b_use      = PREP_LOC_T.b_use;    
b_floorA   = PREP_LOC_T.b_floorA;  
b_survfact = PREP_LOC_T.b_survfact; 
b_sub      = PREP_LOC_T.b_sub;      
b_postcode = PREP_LOC_T.b_postcode;  
b_ufi      = PREP_LOC_T.b_ufi;      
b_post89   = PREP_LOC_T.b_post89;    
b_soil     = PREP_LOC_T.b_soil;

b_replace_cost_pm2 = PREP_LOC_T.b_replace_cost_pm2;  
b_content_cost_pm2 = PREP_LOC_T.b_content_cost_pm2;  
%==========================================================================
%DR - introduced block 14 Jan 2004
b_usage      = PREP_LOC_T.b_usage;
b_type_hazus = PREP_LOC_T.b_type_hazus;
%==========================================================================    

if (small_site_flag==1) % single site
        trunc_indx = THE_PARAM_T.SiteInd;
%         trunc_indx = [single_site]; % Meriwether RES1-W1, 
        %trunc_indx = [1165]; % Hamilton RES1-URML site
    elseif (small_site_flag==2) % small subset
        trunc_indx = [2997, 2657, 3004, 3500];  
        %trunc_indx = [7:10]; %, trunc_indx];
    elseif (small_site_flag==3) % larger subset
%         trunc_indx = [13, 2657, 2997, 3004, 5824];  %boundaries
%         trunc_indx = [7:16, 2000:2010, 3000:3010, 4000:4010, trunc_indx];
        % the following trunc_ind captures two samples of all building types and two
        % samples of all building uses
  trunc_indx= [3541, 3541, 2773, 2773, 4547, 4547, 4080, 5570, 964, 933, 2249, 2249, 2194, 2194 ...
        1766, 2196, 2158, 1674, 2291, 2233, 394, 4982, 5461, 3831, 60, 5966, 2633, 2281 ...
        3059, 1707, 6012, 5284, 1726, 3300, 2979, 2406, 3729, 2353, 2252, 2252, 2342, 2342 ...
        2398, 2187, 4962, 4962, 2219, 2219, 2253, 2367, 5338, 299, 1244, 3571, 1281, 2306 ...
        6238, 2363, 1408, 6284, 6235, 6292, 1750, 1684, 4006, 4135, 1676, 3674, 3875, 17 ...
        6267, 5360, 6268, 6240, 3228, 2383, 468, 71, 2317, 2183, 2694, 5237, 665, 401 ...
         659, 3472, 4126, 2653, 1446, 3845, 1902, 6294, 567, 2222, 4659, 4951, 291, 2372];
    else
        all_sites = 1:nsites; 
        trunc_indx = all_sites; 
    end
    % now do the truncation
    b_siteid0 = b_siteid(trunc_indx); %truncate the number of sites
    b_ufi0 = b_ufi(trunc_indx);
    b_lat0 = b_lat(trunc_indx);
    b_lon0 = b_lon(trunc_indx); 
    b_type0 = b_type(trunc_indx);
    b_use0 = b_use(trunc_indx);
    b_floorA0 = b_floorA(trunc_indx);
    b_soil0 = b_soil(trunc_indx,:); 
    b_survfact0 = b_survfact(trunc_indx); 
    b_sub0 = b_sub(trunc_indx); 
    b_postcode0 = b_postcode(trunc_indx);
    b_post890 = b_post89(trunc_indx);
    b_replace_cost_pm20 = b_replace_cost_pm2(trunc_indx); 
    b_content_cost_pm20 = b_content_cost_pm2(trunc_indx);  
    
    %==========================================================================
    %DR - introduced block 14 Jan 2004
    b_usage0      = b_usage(trunc_indx);
    b_type_hazus0 = b_type_hazus(trunc_indx);
    %==========================================================================    

    % reset
    b_siteid = b_siteid0;
    b_ufi = b_ufi0;
    b_lat = b_lat0;
    b_lon = b_lon0; 
    b_type = b_type0;
    b_use = b_use0;
    b_floorA = b_floorA0;
    b_soil = b_soil0;  
    b_survfact = b_survfact0;
    b_sub = b_sub0;
    b_postcode = b_postcode0;
    b_post89 = b_post890;
    b_replace_cost_pm2 = b_replace_cost_pm20;
    b_content_cost_pm2 = b_content_cost_pm20;
    nsites = length(b_siteid);

    %==========================================================================
    %DR - introduced block 14 Jan 2004
    b_usage      = b_usage0;
    b_type_hazus = b_type_hazus0;
    %==========================================================================
    
	%--------------------------------------------
	% assign the return data
	REDUCE_SITE_SELECTION_T.trunc_indx          = trunc_indx;
	REDUCE_SITE_SELECTION_T.b_siteid            = b_siteid ;
	REDUCE_SITE_SELECTION_T.b_ufi               = b_ufi ;
	REDUCE_SITE_SELECTION_T.b_lat               = b_lat ;
	REDUCE_SITE_SELECTION_T.b_lon               = b_lon ; 
	REDUCE_SITE_SELECTION_T.b_type              = b_type ;
	REDUCE_SITE_SELECTION_T.b_use               = b_use ;
	REDUCE_SITE_SELECTION_T.b_floorA            = b_floorA ;
	REDUCE_SITE_SELECTION_T.b_soil              = b_soil ;  
	REDUCE_SITE_SELECTION_T.b_survfact          = b_survfact ;
	REDUCE_SITE_SELECTION_T.b_sub               = b_sub ;
	REDUCE_SITE_SELECTION_T.b_postcode          = b_postcode ;
	REDUCE_SITE_SELECTION_T.b_post89            = b_post89 ;
	REDUCE_SITE_SELECTION_T.nsites              = nsites ;
	REDUCE_SITE_SELECTION_T.b_replace_cost_pm2  = b_replace_cost_pm2;
	REDUCE_SITE_SELECTION_T.b_content_cost_pm2  = b_content_cost_pm2;
	REDUCE_SITE_SELECTION_T.b_replace_cost_pm20 = b_replace_cost_pm20;
	REDUCE_SITE_SELECTION_T.b_content_cost_pm20 = b_content_cost_pm20;
	REDUCE_SITE_SELECTION_T.b_usage             = b_usage ;
	REDUCE_SITE_SELECTION_T.b_type_hazus        = b_type_hazus ;

%==========================================================================
%  END of SUB function 
%==========================================================================
function in_land = LOC_watercheck(b_lon, b_lat, qa_switch_watercheck)
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Script to check if the site values lie in the water
	% I have simply copied this from the older version of make_sites by Glenn Fulford
	% This will need some more work
	%                                           David Robinson and Glenn Fulford
	%                                           27/02/02
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	%nsites = length(b_id);	% ESSENTIAL variable needed below
	
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%% isolate points within land masses
	%%% hazard calculations can be expensive. This section lets the user 'mask' water
	%%% sites. In other words, hazard will not be calcuated at 'masked' sites. Rather, the
	%%% corresponding hazard value in the final hazard matrix will be set to NaN. This 
	%%% conserves the matrix structure of hazard for plotting purposes.
	%%% The mechanics of masking is as follows: 
	%%% 1) Answer 1 to the query: Do you want to mask water sites (1/0) 
	%%% 2) Draw a polygon enclosing the water area for which you don't want hazard calculations
	%%%    RIGHT CLICK the mouse for the last polygon point. This closes the polygon.
	%%%    Don't worry about masking all the water with one polygon. After you close a polygon
	%%%    you will be asked again if you want to mask water sites. If you enter 1, you get to
	%%%    draw a new polygon.
	%%% 3) To break the loop: answer 0 to the query: Do you want to mask water sites (1/0)
	c = zeros(length(b_lon),1); %grf column vector logical varibles  to determine if in masked region or not
	%grf while 1 == 1
	
% 	while qa_switch_watercheck ~= 0
%        disp(' ');
%        % Action work out why this does not display to screen DR
%        infostr = {'RIGHT CLICK the mouse for the last polygon point. This closes the polygon.'; ...
%                'Dont worry about masking all the water with one polygon. After you close a polygon'; ...
%               'you will be asked again if you want to mask water sites. If you enter 1, you get to'; ...  
%                'draw a new polygon.'; ...
%                'To break the loop: answer 0 to the query: Do you want to mask water sites (1/0)'};
%        disp(infostr);
%        msk_flg = input('Do you want to mask water sites (1/0) ');
%        if msk_flg == 0; break; end;
%        [lon_zone, lat_zone] = mke_polygon('r-');
%        im_in = inpolygon(b_lon,b_lat,lon_zone,lat_zone);
%        c = c + im_in;
% 	end
	in_land	= (c < 1);		    % in_land (i.e. non-masked sites) is a logical
								% vector of length nsites
	%%% ok, we're finished with the site stuff, before moving on, inform the user
	%%% of the number of sites where hazard will involve computational time:
	disp(' ');
	disp(['hazard calculation for: ' num2str(sum(in_land)) ' sites']);
	disp(' ');
%==========================================================================
% END of SUB function
%==========================================================================


    
    