function d = distance_eqrm(x,y,metric)
% DISTANCE can be used to compute the distance between VECTORS in a
% metric space. 
%
% INPUTS:
% x             [matrix mxn] 
%                   m VECTORS to be compared row-wise with m VECTORS in y
%                   n coordinates describing the location of each VECTOR
% y             [matrix mxn]
%                   m VECTORS to be compared row-wise with m VECTORS in x
%                   n coordinates describing the location of each VECTOR
% metric        [string] 
%               'euclidean' =>  Euclidean n space with metric defined by 
%                               ||x-y|| = sqrt{sum[(xi-yi)^2]}. 
%
% OUTPUTS:
% d             [matrix mx1] distance between each of the m VECTORS in x 
%               and y 
%
%
% Note:
% * the function syntax has been set up to allow for its use in 
%   different metric spaces. However, it  currently only works in 
%   Euclidean space. 
% * the capitalised VECTOR in this help refers to an element in a VECTOR space.
%   For example; VECTORS in euclidean space are more commonly known as points. 
%
% DEMO
% A = [1 1 1; 2 2 2; 3 3 3]
% B = 10*ones(3,3)
% d = distance(A,B,'euclidean')
%
% David Robinson
% 17 October 2003

switch metric
    case 'euclidean'
        d = sqrt(sum((x-y).^2,2));
end