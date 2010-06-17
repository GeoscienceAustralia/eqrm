function varargout = the_run_type_decipher(action_str, varargin)
%=================================================================
% USAGE:
%   >> is_hzd  = the_run_type_decipher('-is_it_a_hzd_run_type',               some_str);
%   >> is_risk = the_run_type_decipher('-is_it_a_risk_run_type',              some_str);
%   >> is_rfh  = the_run_type_decipher('-is_it_a_risk_from_hazard_run_type',  some_str);
%
%   >> is_hzd  = the_run_type_decipher('-is_it_a_hzd_run_type',               some_value);
%   >> is_risk = the_run_type_decipher('-is_it_a_risk_run_type',              some_value);
%   >> is_rfh  = the_run_type_decipher('-is_it_a_risk_from_hazard_run_type',  some_value);
%   >> is_r    = the_run_type_decipher('-is_it_a_risk_or_risk_from_hazard',   some_value);
%   >> is_com  = the_run_type_decipher('-is_it_a_common',                     some_value);
%
%   >> a_str   = the_run_type_decipher('-get_a_run_type_str_for_the_standard',some_value);
%=================================================================
% DESCRIPTION:
%  A fundamental question that occurs over and over again in the EQRM
%  software suite, is:
%                        - Are you a HAZARD run type ?
%                        - Are you a RISK run type ?
%                        - Are you a RISK_FROM_HAZARD run type ?
%              
%                        - Are you a RISK or RISK_from_HAZARD ?
%
%                        - Are you a HZD,RISK or RISK_from_HZD ?
%                          (we call this a COMMON run)
%
% The PARAMETER_STANDARD has a parameter called "run_type", and its 
% value actually defines what the run type is, 
%    eg: run_type == 1 ---> a HAZARD run.
%
% However, when invoking the PARAMETER standard, you need to specify 
% your run type before you receive the default parameter standard .....
% so I will use this function as the CENTRAL means for allowing a 
% user to QUERY if he has a particular run type.
%
% Functions known to call this function include:
%   1.) get_param_for_wrap_and_argchk()
%   2.) the_parameter_standard()
%   3.) do_eqhzd()
%=================================================================
% INPUTS:
%  action_str : what type of run type are you trying to compare against
%
%  some_str   : a string that defines the run type that you want.
%               This string is automatically converted to lower case.
%               allowable string values are:
%                {'hzd_run_type', 'hzd_run',     'hzd', '-hzd_run', '-hazard'}
%                {'risk_run_type', 'risk_run',   'risk', '-risk_run', '-risk'}
%                {'risk_from_hazard_run_type',   'rfh_run', 'rfh', '-risk_from_hazard_run'}
% 
%                '-risk_or_risk_from_hazard'
%                '-common'
%
% some_value  : a scalar that defines the run_type that you are querying
%               against.  Allowable VALUES are:
%
%                   1 ---> HAZARD run
%                   2 ---> RISK run
%                   3 ---> RISK from HAZARD run
%=================================================================
% OUTPUTS:
%     is_it   :  1 --> YES it is the run type you thought it was
%             :  0 --> No it is NOT the run type you thought it was
%=================================================================
% HISTORY:
%  26-03-2004:  Created by CEANET
%=================================================================

action_str = lower(action_str);
switch(action_str)
    case '-is_it_a_hzd_run_type'
         the_str_or_val = varargin{1};
         if( ischar(the_str_or_val) )
             %% STRING
             is_hzd         = LOC_hzd_run_type_from_str(the_str_or_val);
         elseif( isnumeric(the_str_or_val) )
             %% NUMERIC
             is_hzd       = LOC_hzd_run_type_from_value(the_str_or_val);
         else
             error('ERROR:  Incorrect usage mode (ischar or isnumeric ???) inside <%s>', mfilename);
         end
         
         varargout{1}   = is_hzd;
    %----------------------------------------------------------------------
    case '-is_it_a_risk_run_type'
         the_str_or_val = varargin{1};
         if( ischar(the_str_or_val) )
             %% STRING
             is_risk        = LOC_risk_run_type_from_str(the_str_or_val);
         elseif( isnumeric(the_str_or_val) )
             %% NUMERIC
             is_risk       = LOC_risk_run_type_from_value(the_str_or_val);
         else
             error('ERROR:  Incorrect usage mode (ischar or isnumeric ???) inside <%s>', mfilename);
         end
         
         varargout{1}   = is_risk;
    %----------------------------------------------------------------------
    case '-is_it_a_risk_from_hazard_run_type'
         the_str_or_val = varargin{1};
         if( ischar(the_str_or_val) )
             %% STRING
             is_rfh         = LOC_rfh_run_type_from_str(the_str_or_val);
         elseif( isnumeric(the_str_or_val) )
             %% NUMERIC
             is_rfh       = LOC_rfh_run_type_from_value(the_str_or_val);
         else
             error('ERROR:  Incorrect usage mode (ischar or isnumeric ???) inside <%s>', mfilename);
         end
         
         varargout{1}   = is_rfh;
    %----------------------------------------------------------------------
    case '-is_it_a_risk_or_risk_from_hazard'
         the_str_or_val = varargin{1};
         if( ischar(the_str_or_val) )
             error('ERROR:  Incorrect usage mode you *MUST* supply a VALUE inside <%s>', mfilename);
         elseif( isnumeric(the_str_or_val) )
             %% NUMERIC.  Are you a RISk or a RISK_from_HAZARD ?
             is_rfh       = LOC_rfh_run_type_from_value(the_str_or_val);
             is_risk      = LOC_risk_run_type_from_value(the_str_or_val);
             
             is_r         = double( is_rfh | is_risk);
         else
             error('ERROR:  Incorrect usage mode (ischar or isnumeric ???) inside <%s>', mfilename);
         end
         
         varargout{1}   = is_r;
    %----------------------------------------------------------------------
    case '-is_it_a_common'
         the_str_or_val = varargin{1};
         if( ischar(the_str_or_val) )
             error('ERROR:  Incorrect usage mode you *MUST* supply a VALUE inside <%s>', mfilename);
         elseif( isnumeric(the_str_or_val) )
             %% NUMERIC.  Are you a HZD or a RISk or a RISK_from_HAZARD ?
             is_hzd       = LOC_hzd_run_type_from_value(the_str_or_val);
             is_rfh       = LOC_rfh_run_type_from_value(the_str_or_val);
             is_risk      = LOC_risk_run_type_from_value(the_str_or_val);
             
             is_com       = double( is_hzd | is_risk | is_rfh);
         else
             error('ERROR:  Incorrect usage mode (ischar or isnumeric ???) inside <%s>', mfilename);
         end
         
         varargout{1}   = is_com;
    %----------------------------------------------------------------------
    case '-get_a_run_type_str_for_the_standard'
        
			run_type_value = varargin{1};
            
			if(     the_run_type_decipher('-is_it_a_hzd_run_type',    run_type_value)  )
                    run_type_str = '-hzd_run';
			elseif( the_run_type_decipher('-is_it_a_risk_run_type',   run_type_value)  )   
                    run_type_str = '-risk_run';
			elseif( the_run_type_decipher('-is_it_a_risk_from_hazard_run_type',   run_type_value)  )
                    run_type_str = '-risk_from_hazard_run';
			else
                error('###_ERROR:  UNknown parameter standard found in file <%s>', mfilename);
			end
            
            varargout{1} = run_type_str;
    %----------------------------------------------------------------------
otherwise
         error('ERROR:  Incorrect usage mode (OTHERWISE) inside <%s>', mfilename);
 end
%==========================================================================
% END of MAIN function
%==========================================================================
%%%
%%
%
function  is_hzd  = LOC_hzd_run_type_from_str(the_str)
	switch( lower(the_str) )
        case {'hzd_run_type', 'hzd_run', 'hzd', '-hzd_run', '-hazard'}
        is_hzd = 1;
	otherwise
        is_hzd = 0;
	end
%==========================================================================
function  is_risk  = LOC_risk_run_type_from_str(the_str)
	switch( lower(the_str) )
        case {'risk_run_type', 'risk_run', 'risk', '-risk_run', '-risk'}
        is_risk = 1;
	otherwise
        is_risk = 0;
	end
%==========================================================================
function  is_rfh  = LOC_rfh_run_type_from_str(the_str)
	switch( lower(the_str) )
        case {'risk_from_hazard_run_type', 'rfh_run', 'rfh', '-risk_from_hazard_run'}
        is_rfh = 1;
	otherwise
        is_rfh = 0;
	end
%==========================================================================
function is_hzd       = LOC_hzd_run_type_from_value(the_value)
   is_hzd = 0;
   if( 1 == the_value )
       is_hzd = 1; 
   end
%==========================================================================
function is_risk      = LOC_risk_run_type_from_value(the_value)
   is_risk = 0;
   if( 2 == the_value )
       is_risk = 1; 
   end
%==========================================================================
function  is_rfh       = LOC_rfh_run_type_from_value(the_value)
   is_rfh = 0;
   if( 3 == the_value )
       is_rfh = 1; 
   end
%==========================================================================
