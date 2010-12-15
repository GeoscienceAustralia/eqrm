function [] = testdata4youngs97()
 %The purpose of this function is to create unit test data 
 %for the Youngs et al (1997) ground motion relations for use
 %with the EQRM in test_groundmotionspecification.py
 
 % Currently this tests the the interface and the intraslab (average)
 % ground motion models. 
 
 % Jonathan Griffin
 % 10 May 2010
 
 % Setup
Mw = [6.1, 6.1, 6.1, 7.2, 7.2, 7.2, 8.3, 8.3, 8.3];   % i.e. we have 3 events 
Rjb = [0, 25, 50, 100]; % distance between the events and four sites (i.e. assume the 3 events are at the same location)
Depth = [10, 50, 100, 10, 50, 100, 10, 50, 100];    % Calculate events for 3 different depths
RSAperiods = [0, 0.02, 0.15, 0.25, 0.35, 0.5, 0.7, 0.85, 1.0, 1.42, 2.1, 2.5];  % 12 RSA periods of interest

%RSAperiods = [0, 0.0100,0.0200,0.0300,0.0400,0.0500,0.0750,0.1000,0.4000,0.5000,0.7500,1.0000];


if length(RSAperiods)~=12
    error('ERROR this code is written for 12 RSA periods ')
end
 
 
%%======Test results for Youngs et al
coeff_temp = [ ...
%Period  C1      C2       C3       C4      C5       
0.0     0.00000 0.00000  -2.55200 1.45000 -0.10000; ...
0.075   1.27500 0.00000  -2.70700 1.45000 -0.10000; ...
0.100   1.188000 -0.00110  -2.65500 1.45000 -0.10000; ...
0.200   0.72200 -0.00270  -2.52800 1.45000 -0.10000; ...
0.300   0.24600 -0.00360  -2.45400 1.45000 -0.10000; ...
0.400   -0.11500 -0.00430  -2.40100 1.45000 -0.10000; ...
0.500   -0.40000 -0.00480  -2.36000 1.45000 -0.10000; ...
0.750   -1.14900 -0.00570  -2.28600 1.45000 -0.10000; ...
1.000   -1.73600 -0.00640  -2.23400 1.45000 -0.10000; ...
1.500   -2.63400 -0.00730  -2.16000 1.50000 -0.10000; ...
2.000   -3.32800 -0.00800  -2.10700 1.55000 -0.10000; ...
3.000   -4.51100 -0.00890  -2.03300 1.65000 -0.10000];
 
Youngs_coeff.periods  = coeff_temp(:,1)';
Youngs_coeff.C1  = coeff_temp(:,2)';
Youngs_coeff.C2  = coeff_temp(:,3)';
Youngs_coeff.C3  = coeff_temp(:,4)';
Youngs_coeff.C4  = coeff_temp(:,5)';
Youngs_coeff.C5  = coeff_temp(:,6)';

disp('   ')
disp('   ')
disp('===== Creating test data for the Youngs model =====')
disp(['tmp = zeros((',num2str(length(Rjb)),',',num2str(length(Mw)),',', num2str(length(RSAperiods)),'))']);

%Distances less than 10 km set to 10 km.
for i =1:length(Rjb)
    Rjb(i) = max(Rjb(i),10);   
end

for i = 1:length(Rjb)  % loop over the pseudo sites (i.e. the distnaces)
    for j = 1:length(Mw) % loop over the events (i.e. the magnitudes)
        %for k = 1:length(Depth) % loop over the depths 
        [meanRSA] = evaluate_meanRSA(Mw(j), Rjb(i), RSAperiods, Youngs_coeff, Depth(j));
        str1 = ['tmp[',num2str(i-1),',', num2str(j-1),',:] = ['];
        str2 = [num2str(meanRSA(1)), ',',num2str(meanRSA(2)), ',', ...
                num2str(meanRSA(3)), ',',num2str(meanRSA(4)),','];
        str3 = [num2str(meanRSA(5)), ',',num2str(meanRSA(6)), ',', ...
                num2str(meanRSA(7)), ',',num2str(meanRSA(8)),','];
        str4 = [num2str(meanRSA(9)), ',',num2str(meanRSA(10)), ',', ...
                num2str(meanRSA(11)), ',',num2str(meanRSA(12)),']'];       
        disp([str1,str2])
        disp(str3)
        disp(str4)
        %end
    end
end
%disp('test_data[''Youngs_97_interface_test_mean''] = tmp');
disp('test_data[''Youngs_97_interface_test_mean''] = tmp');


function [meanRSA] = evaluate_meanRSA(Mw, Rjb, RSAperiods, coeff, Depth)
  
  % Evaluates the mean response spectral acceleration (RSA). 
  
  % Inputs 
  % Mw          [double - 1X1] moment magnitude for a single event
  % Rjb         [double - 1X1] Joyner Boore distance between the
  %             event and a single site   
  % RSAperiods  [double - fundamental periods for which RSA is evaluated
  % coeff       [structure]coefficients to use with following format
  %                 coeff.periods [1Xn] => periods at which coefficients are defined
  %                 coeff.c1 [1xn} => coefficient c1
  %                 etc. etc. 
 
 % setup 
 

% Z_t = 0.0 %interface
 Z_t = 1.0; %intraslab
  
 % Interpolate the coefficients to the periods of interest (i.e. RSAperiod)
 c1 = interp1(coeff.periods,coeff.C1,RSAperiods,'linear','extrap');
 c2 = interp1(coeff.periods,coeff.C2,RSAperiods,'linear','extrap');
 c3 = interp1(coeff.periods,coeff.C3,RSAperiods,'linear','extrap');
 c4 = interp1(coeff.periods,coeff.C4,RSAperiods,'linear','extrap');
 c5 = interp1(coeff.periods,coeff.C5,RSAperiods,'linear','extrap');

 
%     c1 = 1.0
%         c2 = 2.0
%         c3 = 3.0
%         c4 = 4.0
%         c5 = 5.0
%         c6 = 6.0
%         c7 = 7.0
%         c8 = 8.0
%
logmeanRSA = 0.2418 + 1.414*Mw + c1 + c2*((10.0-Mw)^3) + c3*log(Rjb + 1.7818*exp(0.554*Mw)) + 0.00607*Depth + 0.3846*Z_t;

 
meanRSA = exp(logmeanRSA);
%plot(RSAperiods, logmeanRSA)
%pause