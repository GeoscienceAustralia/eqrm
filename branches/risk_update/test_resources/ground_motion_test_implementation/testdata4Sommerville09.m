function [] = testdata4Sommerville09()
 %The purpose of this function is to create unit test data 
 %for the Somerville (2009) ground motion relations for use
 %with the EQRM in test_groundmotionspecification.py
 
 % Currently this tests the the Yilgarn and the non-Cratonic (average)
 % ground motion models. 
 
 % David Robinson 
 % 29 April 2010
 
 % Setup
Mw = [5.5, 6.4, 6.5];   % i.e. we have 3 events 
Rjb = [0, 25, 50, 100]; % distance between the events and four sites (i.e. assume the 3 events are at the same location)
RSAperiods = [0, 0.02, 0.025, 0.035, 0.5, 0.7, 1.0, 1.12,3.5,7.4, 9, 10];  % 12 RSA periods of interest

%RSAperiods = [0, 0.0100,0.0200,0.0300,0.0400,0.0500,0.0750,0.1000,0.4000,0.5000,0.7500,1.0000];


if length(RSAperiods)~=12
    error('ERROR this code is written for 12 RSA periods ')
end
 
 
%%======Test results for Yilgarn
coeff_temp = [ ...
%Period  C1      C2       C3       C4      C5       C6       C7       C8
0.0     1.54560 1.45650  -1.11510 0.16640 -0.00567 -1.04900 1.05530  0.20000; ...
0.010   1.55510 1.46380  -1.11460 0.16620 -0.00568 -1.04840 1.05850  0.20140; ...
0.020   2.33800 1.38060  -1.22970 0.18010 -0.00467 -1.39850 0.95990  0.20130; ...
0.030   2.48090 1.37540  -1.17620 0.17120 -0.00542 -1.38720 0.96930  0.19280; ...
0.040   2.31450 1.60250  -1.12600 0.17150 -0.00629 -1.27910 1.07040  0.23560; ...
0.050   2.26860 1.55840  -1.07340 0.14710 -0.00709 -1.08910 1.10750  0.20670; ...
0.075   1.97070 1.68030  -1.01540 0.14560 -0.00737 -0.91930 1.18290  0.22170; ...
0.100   1.71030 1.75070  -0.99330 0.13820 -0.00746 -0.78140 1.29390  0.23790; ...
0.150   1.52310 1.69160  -0.96310 0.13330 -0.00713 -0.67330 1.22430  0.21020; ...
0.200   1.36830 1.57940  -0.94720 0.13640 -0.00677 -0.62690 1.17760  0.18950; ...
0.250   1.40180 1.28940  -0.94410 0.14360 -0.00617 -0.67070 1.05610  0.14590; ...
0.3003  1.45000 1.04630  -0.94880 0.14760 -0.00581 -0.68700 0.94040  0.11040; ...
0.400   1.44150 0.92820  -0.91830 0.11320 -0.00576 -0.59520 0.86280  0.04060; ...
0.500   1.40380 0.69160  -0.91010 0.13480 -0.00557 -0.62390 0.71230  0.00620; ...
0.750   1.50840 0.75800  -0.99010 0.11260 -0.00458 -0.69040 0.68590  -0.05630; ...
1.000   2.10630 0.38180  -1.08680 0.07950 -0.00406 -0.90340 0.61850  -0.18250; ...
1.4993  2.55790 -0.84270 -0.81810 0.07650 -0.00220 -1.35320 -0.25440 -0.46660; ...
2.000   2.39600 -1.39950 -0.70440 0.06770 -0.00366 -0.90860 -0.64320 -0.59600; ...
3.0003  0.96040 -0.46120 -0.70450 0.06450 -0.00429 -0.51190 -0.16430 -0.46310; ...
4.000   0.12190 -0.06980 -0.75910 0.08490 -0.00374 -0.41450 0.12350  -0.39250; ...
5.000  -0.84240 0.53160  -0.79600 0.10330 -0.00180 -0.62130 0.53680  -0.27570; ...
7.5019 -1.92260 0.63760  -0.81900 0.14550 -0.00066 -0.75740 0.69020  -0.23290; ...
10.000 -2.60330 0.59060  -0.80940 0.16090 -0.00106 -0.68550 0.70350 -0.22910];
 
Yilgarn_coeff.periods  = coeff_temp(:,1)';
Yilgarn_coeff.C1  = coeff_temp(:,2)';
Yilgarn_coeff.C2  = coeff_temp(:,3)';
Yilgarn_coeff.C3  = coeff_temp(:,4)';
Yilgarn_coeff.C4  = coeff_temp(:,5)';
Yilgarn_coeff.C5  = coeff_temp(:,6)';
Yilgarn_coeff.C6  = coeff_temp(:,7)';
Yilgarn_coeff.C7  = coeff_temp(:,8)';
Yilgarn_coeff.C8  = coeff_temp(:,9)';

disp('   ')
disp('   ')
disp('===== Creating test data for the Somerville Yilgarn model =====')
disp(['tmp = zeros((',num2str(length(Rjb)),',',num2str(length(Mw)),',', num2str(length(RSAperiods)),'))']);

for i = 1:length(Rjb)  % loop over the pseudo sites (i.e. the distnaces)
    for j = 1:length(Mw) % loop over the events (i.e. the magnitudes)
        [meanRSA] = evaluate_meanRSA(Mw(j), Rjb(i), RSAperiods, Yilgarn_coeff);
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
    end
end
disp('test_data[''Somerville_Yilgarn_test_mean''] = tmp')

%%======Test results for Non Cratonic (average) model
coeff_temp = [ ...
%Period	C1	C2	C3	C4	C5	C6	C7	C8
0.0     1.03780	 -0.03970	-0.79430	0.14450	-0.00618	-0.72540	-0.03590	-0.09730; ...
0.010	1.05360	 -0.04190	-0.79390	0.14450	-0.00619	-0.72660	-0.03940	-0.09740; ...
0.020	1.05680	 -0.03920	-0.79680	0.14550	-0.00617	-0.73230	-0.03930	-0.09600; ...
0.030	1.13530	 -0.04790	-0.80920	0.15000	-0.00610	-0.76410	-0.05710	-0.09210; ...
0.040	1.30000	 -0.07020	-0.83150	0.15920	-0.00599	-0.82850	-0.09810	-0.08530; ...
0.050	1.47680	 -0.09310	-0.83330	0.15600	-0.00606	-0.86740	-0.12740	-0.09130; ...
0.075	1.70220	 -0.05160	-0.80720	0.14560	-0.00655	-0.87690	-0.10970	-0.08690; ...
0.100	1.65720	 0.15080	-0.77590	0.13100	-0.00708	-0.77830	0.01690	    -0.05980; ...
0.150	1.94440	 -0.09620	-0.75000	0.11670	-0.00698	-0.69490	-0.13320	-0.12530; ...
0.200	1.82720	 -0.06230	-0.73430	0.11940	-0.00677	-0.64380	-0.09570	-0.11920; ...
0.250	1.74380	 -0.02530	-0.72480	0.11950	-0.00646	-0.63740	-0.06250	-0.11650; ...
0.3003	1.80560	 -0.27020	-0.73190	0.13490	-0.00606	-0.66440	-0.17470	-0.14340; ...
0.400	1.88750	 -0.37820	-0.70580	0.09960	-0.00589	-0.58770	-0.24420	-0.21890; ...
0.500	2.03760	 -0.79590	-0.69730	0.11470	-0.00565	-0.59990	-0.48670	-0.29690; ...
0.750	1.93060	 -0.80280	-0.74510	0.11220	-0.00503	-0.59460	-0.50120	-0.34990; ...
1.000	1.60380	 -0.47800	-0.86950	0.07320	-0.00569	-0.41590	0.06360     -0.33730; ...
1.4993	0.47740	 0.90960	-1.02440	0.11060	-0.00652	-0.19000	1.09610     -0.10660; ...
2.000	-0.25810 1.37770	-1.01000	0.10310	-0.00539	-0.27340	1.50330     -0.04530; ...
3.0003	-0.96360 1.14690	-0.88530	0.10380	-0.00478	-0.40420	1.54130     -0.11020; ...
4.000	-1.46140 1.07950	-0.80490	0.10960	-0.00395	-0.46040	1.41960     -0.14700; ...
5.000	-1.61160 0.74860	-0.78100	0.09650	-0.00307	-0.46490	1.24090     -0.22170; ...
7.5019	-2.35310 0.35190	-0.64340	0.09590	-0.00138	-0.68260	0.92880     -0.31230; ...
10.000	-3.26140 0.69730	-0.62760	0.12920	-0.00155	-0.61980	1.01050     -0.24550];

Non_Cratonic_coeff.periods  = coeff_temp(:,1)';
Non_Cratonic_coeff.C1  = coeff_temp(:,2)';
Non_Cratonic_coeff.C2  = coeff_temp(:,3)';
Non_Cratonic_coeff.C3  = coeff_temp(:,4)';
Non_Cratonic_coeff.C4  = coeff_temp(:,5)';
Non_Cratonic_coeff.C5  = coeff_temp(:,6)';
Non_Cratonic_coeff.C6  = coeff_temp(:,7)';
Non_Cratonic_coeff.C7  = coeff_temp(:,8)';
Non_Cratonic_coeff.C8  = coeff_temp(:,9)';

disp('   ')
disp('   ')
disp('===== Creating test data for the Somerville Non_Cratonic model =====')
disp(['tmp = zeros((',num2str(length(Rjb)),',',num2str(length(Mw)),',', num2str(length(RSAperiods)),'))']);

for i = 1:length(Rjb)  % loop over the pseudo sites (i.e. the distnaces)
    for j = 1:length(Mw) % loop over the events (i.e. the magnitudes)
        [meanRSA] = evaluate_meanRSA(Mw(j), Rjb(i), RSAperiods, Non_Cratonic_coeff);
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
    end
end
disp('test_data[''Somerville_Non_Cratonic_test_mean''] = tmp')



function [meanRSA] = evaluate_meanRSA(Mw, Rjb, RSAperiods, coeff)
  
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
 
%  Mw = 5.4
%  Rjb = 4.3125572498396156
 
 m1 = 6.4;
 r1 = 50;
 h =  6;
 R = sqrt(Rjb.^2+h^2);
 R1 = sqrt(r1.^2+h^2); 
  
 % Interpolate the coefficients to the periods of interest (i.e. RSAperiod)
 c1 = interp1(coeff.periods,coeff.C1,RSAperiods,'linear','extrap');
 c2 = interp1(coeff.periods,coeff.C2,RSAperiods,'linear','extrap');
 c3 = interp1(coeff.periods,coeff.C3,RSAperiods,'linear','extrap');
 c4 = interp1(coeff.periods,coeff.C4,RSAperiods,'linear','extrap');
 c5 = interp1(coeff.periods,coeff.C5,RSAperiods,'linear','extrap');
 c6 = interp1(coeff.periods,coeff.C6,RSAperiods,'linear','extrap');
 c7 = interp1(coeff.periods,coeff.C7,RSAperiods,'linear','extrap');
 c8 = interp1(coeff.periods,coeff.C8,RSAperiods,'linear','extrap');

 
%     c1 = 1.0
%         c2 = 2.0
%         c3 = 3.0
%         c4 = 4.0
%         c5 = 5.0
%         c6 = 6.0
%         c7 = 7.0
%         c8 = 8.0
%  
if Mw < m1 & Rjb < r1
    logmeanRSA = c1 + c2*(Mw - m1) + c3*log(R) + c4*(Mw - m1)*log(R) + c5*Rjb + c8*(8.5 - Mw)^2;
elseif Mw < m1 & Rjb >= r1
    logmeanRSA = c1 + c2*(Mw - m1) + c3*log(R1) + c4*(Mw - m1)*log(R) + c5*Rjb + c6*(log(R) - log(R1)) + c8*(8.5 - Mw)^2;
elseif Mw >= m1 & Rjb < r1
    logmeanRSA = c1 + c7*(Mw - m1) + c3*log(R) + c4*(Mw - m1)*log(R) + c5*Rjb + c8*(8.5 - Mw)^2;
elseif Mw >= m1 & Rjb >= r1
    logmeanRSA = c1 + c7*(Mw - m1) + c3*log(R1) + c4*(Mw - m1)*log(R) +c5*Rjb + c6*(log(R) - log(R1)) + c8*(8.5 - Mw)^2;
else
    error('ERROR: How on Earth did you get here?')
end
 
meanRSA = exp(logmeanRSA);
%plot(RSAperiods, logmeanRSA)
%pause