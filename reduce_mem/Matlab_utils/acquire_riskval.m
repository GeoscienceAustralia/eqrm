function [tgt_val, sval,cum_rte] = acquire_riskval(val, nu, tgt_rte);
% This function is used to acquire risk values associated with target 
% return periods
%
% Inputs:
% val       [vector nx1] target values of interested i.e. can 
%           be loss in risk studies or can be ground motion in 
%           hazard studies
% nu        [vector nx1] event activities for each value in nu
% tgt_rte   [vector mx1] target return rates at which you wish 
%           to know val
% sval      [vector nx1] sorted val (largest to smallest)
% cum_rte   [vector nx1] cummulative event activities - order
%           corresponds to sval
%
% OUTPUTS
% trgrisk   [vector mx1] val at tdt_rte
%
% Note that this is based on software supplied by Andres Mendez
%
% David Robinson
% 6 June 2007

% First we must sort the vals from largest to smallest
[sval,j]	= sort(-1*val);         % we use negative here so that we can utilise inbuilt Matlab function sort
sval	= -sval; 					% remove unwanted negative
snu = nu(j);                        % using sorting index j to re-shuffle nu so it is consistent with sval
cum_rte = cumsum(nu(j));      % cummulative sum event activities (i.e. so it represents cummulative activity for that event and all larger events)

% Now search through the 

nt = length(tgt_rte);
tgt_val = zeros(size(tgt_rte));  % intialise a vector for the output

for i = 1:nt                       % loops over all the target return rates  
   tgt_val(i) 	= NaN;             % start with an NaN - will stay this way if tgt_rte falls outside range(cumrte)
   ihgh	= find(cum_rte > tgt_rte(i)); % find all values where cumrte>tgt_rte
   if ~isempty(ihgh); 
      hit = ihgh(1);   % first value where cumrte>tgt_rte
      if hit > 1;  %if hit >1 use linear interpolation to find the trgrisk
         tgt_val(i) = interp1([cum_rte(hit) cum_rte(hit-1)],[sval(hit) sval(hit-1)],tgt_rte(i)); 
      else
         tgt_val(i) = sval(hit);
      end
   end
end
