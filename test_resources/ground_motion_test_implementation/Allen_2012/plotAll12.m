function [T A12] = plotAll12(m,r,h)
   
% Function calculates 5% dampled response spectral acceleration (A12) in 
% cm/s^2 for periods T (sec),
% where:
%   m = moment magnitude
%   r = Closest distance to rupture
%   h = depth to top of rupture

% ************************************************************************* 
% Calc Allen 2012
% *************************************************************************

if h >= 10
    load 'G:\Modelling\EXSIM\Simulations\AUS12_deep.mat';
else
    load 'G:\Modelling\EXSIM\Simulations\AUS12_shallow.mat';
end

model = model_interp;
c0 = model(:,2);
c1 = model(:,3);
c2 = model(:,4);
c3 = model(:,5);
c4 = model(:,6);
c5 = model(:,7);
c6 = model(:,8);
c7 = model(:,9);
c8 = model(:,10);
c9 = model(:,11);
c10 = model(:,12);
c11 = model(:,13);

minr1 = zeros(size(model(:,1)));
maxr2 = zeros(size(model(:,1)));
maxr3 = zeros(size(model(:,1)));
r01 = 90;
r02 = 150;

for j = 1:length(minr1)
    r1 = r01 + (m-4)*c8(j);
    r2 = r02 + (m-4)*c11(j);
    minr1(j) = min([log10(r) log10(r1)]);
    maxr2(j) = max([log10(r/r1) 0]);
    maxr3(j) = max([log10(r/r2) 0]);
end
minr1 = 10.^minr1;

A12 = 10.^(c0 + c1 * (m-4) + c2*(m-4).^2 ...
      + (c3 + c4*(m-4)).*log10(sqrt(minr1.^2 ...
      + (ones(size(minr1)).*(1+c5*(m-4))).^2)) ...
      + maxr2.*(c6 + c7*(m-4)) ...
      + maxr3.*(c9 + c10*(m-4)));

T = 1 ./ model(:,1);
% A12 = [AT A12];
      


        
