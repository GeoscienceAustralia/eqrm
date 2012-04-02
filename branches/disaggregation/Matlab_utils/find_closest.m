function [ind,closest,mind] = find_closest(x,y,metric)
% FIND_CLOSEST can be used to find the VECTOR in x that is closest to the
% vector y.
%
% INPUTS:
% x             [matrix mxn] 
%                   m VECTORS to be be searched for closest to y
%                   n coordinates describing the location of each VECTOR
% y             [vector 1xn]
%                   n coordinates describing the VECTOR whose closest VECTOR 
%                   will be returned
% metric        [string] 
%               'euclidean' =>  Euclidean n space with metric defined by 
%                               ||x-y|| = sqrt{sum[(xi-yi)^2]}. 
%
% OUTPUTS:
% ind         [scalar] row index of the VECTOR in x that is closest to the 
%             VECTOR y
% closest     [vector 1xn] coordiantes describing the VECTOR in x that is 
%             closest to the VECTOR y.
% mind        [scalar] distance between the VECTOR y and the VECTOR in x that
%             is closest to y. 
%
%
% Note:
% * the function syntax has been set up to allow for its use in 
%   different metric spaces. However, it  currently only works in 
%   Euclidean space. 
% * the capitalised VECTOR in this help refers to an element in a VECTOR space.
%   For example; VECTORS in euclidean space are more commonly known as points.
% * Incases when the minimum distance is achieved by more than one VECTOR
%   in x the first VECTOR is chosen. 
%
% DEMO
% DEMO
% A = [1 1 1; 2 2 2; 3 3 3]
% y = [1.5 1.5 1.5]
% [ind,closest,mind] = find_closest(A,y,'euclidean')
%
% David Robinson
% 17 October 2003


y = y(:)'; % make sure y is a row vector
[m n] = size(x);
Y = repmat(y,m,1);
d = distance_eqrm(x,Y,metric);
[mind ind] = min(d);
closest = x(ind,:);
