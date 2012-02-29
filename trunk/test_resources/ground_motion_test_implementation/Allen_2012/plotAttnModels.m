function [G90SEA G90WA A06 AB95 AB06 AB06BC T97 T02 S09nc S09c CY08 L08 C03 A12] ...
          = plotAttnModels(m,r,h,vs30)
   
% *************************************************************************
% Program: plotAttnModels
% 
% convert all amplitudes to cm/s^2
% % 
% Author: T. Allen (2006-07-25)
% *************************************************************************


mwRange = m;
rhypRange = r;
depth = h;
% vs30 = 760;
repi = sqrt(rhypRange^2 - depth^2);
% clac ML using WA relations
% ML = (mwRange + 2) / 1.3;
% 

freqAUS = [0.10 0.13 0.16 0.20 0.25 0.32 0.40 0.50 0.63 0.80 1.00 1.26 1.59 ...
           2.00 2.52 3.17 3.99 5.03 6.33 7.97 10.04 12.64 15.91 20.04 25.23 ...
           31.77 40.00 99.00];


PerAUS = freqAUS;

toroFile = 'attn_toro_midcontinent_momag.txt';
[toro.T,toro.c1,toro.c2,toro.c3,toro.c4,toro.c5,toro.c6,toro.c7] = ...
textread(toroFile,'%f %f %f %f %f %f %f %f','headerlines',4);
toro.T(1) = 0.01;

ab95File = 'attn_atkboore_momag.txt';
[ab95.T,ab95.c1,ab95.c2,ab95.c3,ab95.c4] = textread(ab95File,'%f %f %f %f %f','headerlines',4);
ab95.T(1) = 0.01;

ab06File = 'attn_atkboore06_momag.txt';
[ab06.T,ab06.c1,ab06.c2,ab06.c3,ab06.c4,ab06.c5,ab06.c6,ab06.c7,ab06.c8,ab06.c9,ab06.c10] ...
= textread(ab06File,'%f%f%f%f%f%f%f%f%f%f%f','headerlines',4);
ab06.T(1) = 0.01;

if mwRange <= 6.5
    sadFile = 'attn_sadigh_coeff_momag_less65.txt';
    [sad.T,sad.c1,sad.c2,sad.c3,sad.c4,sad.c5,sad.c6,sad.c7,sad.c8,sad.c9,sad.c10,sad.c11,sad.c12] = ...
    textread(sadFile,'%f %f %f %f %f %f %f %f %f %f %f %f %f','headerlines',12);
    sadC5 = 1.29649;
else
    sadFile = 'attn_sadigh_coeff_momag_great65.txt';
    [sad.T,sad.c1,sad.c2,sad.c3,sad.c4,sad.c5,sad.c6,sad.c7,sad.c8,sad.c9,sad.c10,sad.c11,sad.c12] = ...
    textread(sadFile,'%f %f %f %f %f %f %f %f %f %f %f %f %f','headerlines',12);
    sadC5 = -0.48451;
end
sad.T(1) = 0.01;

% *************************************************************************
% Calculate predicted AUS ground-motion
% *************************************************************************        
    % get coefficients for SEA stochastic finite-fault model
    % ignore last two coef's
    [ausT c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13] = ...
    textread('gmModel_2007.dat','%f%f%f%f%f%f%f%f%f%f%f%f%f%f','headerlines',3);
    ausT(1) = 0.01;

    r0 = 10; %km
    r1 = 90;
    r2 = 160;
    M = mwRange;
    Rcd = rhypRange;
     % assume hyp dist Rcd (closest distance)
    f0 = max([log10(r0/Rcd) 0]);
    f1 = min([log10(Rcd) log10(r1)]);
    f2 = max([log10(Rcd/r2) 0]);

    D = (c10 + c11*log10(Rcd) + c12*log10(Rcd)^2 + c13*log10(Rcd)^3);
    ausAmp = 10.^(c1 + c2*M + c3*M^2 + (c4 + c5*M)*f1 + (c6 + c7*M)*f2 ...
             + (c8 + c9*M)*f0 + D);
    A06 = [ausT ausAmp];

% *************************************************************************
% Calc Toro, Abrahamson and Schneider 1997 Coefficients for Midcontinent using
% Moment Magnitude
% ************************************************************************* 
    r0 = 80; % km
    edist = sqrt(rhypRange^2 - depth^2);
    Rm = sqrt(edist^2 + toro.c7.^2); %assume edist = hdist
    if Rm <= r0
        toroAmp = toro.c1 + toro.c2 .* (M - 6.0) + toro.c3 .* (M - 6.0)^2 ...
                     - toro.c4 .* log(Rm) - toro.c6 .* Rm;
    else % hdist > 80 km
        toroAmp = toro.c1 + toro.c2 .* (M - 6.0) + toro.c3 .* (M - 6.0)^2 ...
                   - toro.c4 .* log(Rm) - (toro.c5 - toro.c4) .* log(Rm/r0) - toro.c6 .* Rm;
    end

    % convert toro ln g to cm/s^2
    toroAmp = exp(toroAmp) * 980;
    T97 = [toro.T toroAmp];
    
% *************************************************************************
% Calc Toro 2002 Midcontinent using
% Moment Magnitude
% ************************************************************************* 
    r0 = 80; % km
    edist = sqrt(rhypRange^2 - depth^2);
    Rm = sqrt(edist^2 + toro.c7.^2*(exp(-1.25*0.227*M))^2); %assume edist = hdist
    if Rm <= r0
        toroAmp = toro.c1 + toro.c2 .* (M - 6.0) + toro.c3 .* (M - 6.0)^2 ...
                     - toro.c4 .* log(Rm) - toro.c6 .* Rm;
    else % hdist > 80 km
        toroAmp = toro.c1 + toro.c2 .* (M - 6.0) + toro.c3 .* (M - 6.0)^2 ...
                   - toro.c4 .* log(Rm) - (toro.c5 - toro.c4) .* log(Rm/r0) - toro.c6 .* Rm;
    end

    % convert toro ln g to cm/s^2
    toroAmp = exp(toroAmp) * 980;
    T02 = [toro.T toroAmp];    

% ************************************************************************* 
% Calc Sadigh et al. (1997) for shallow Californian earthquakes
% assume Rrup = hdist
% *************************************************************************
    hdist = rhypRange;        
    sadAmp = sad.c2 + sad.c3 * M + sad.c4 * (8.5 - M)^2.5 + ...
             sad.c5 .* log(hdist + exp(sadC5 + sad.c8 * M)) + sad.c6 ...
             * log(hdist + 2);

    % convert sadigh ln g to cm/s^2
    sadAmp = exp(sadAmp) * 980;

% ************************************************************************* 
% Calc Atkinson and Boore (1995) for ENA
% ************************************************************************* 
    ab95Amp = ab95.c1 + ab95.c2 * (M - 6.0) + ab95.c3 * (M - 6.0)^2 ...
              - log(hdist) + ab95.c4 * hdist;
    % convert ab95 ln g to  cm/s^2
    ab95Amp = exp(ab95Amp) * 980;
    
    AB95 = [ab95.T ab95Amp];

% ************************************************************************* 
% Calc Atkinson and Boore (2006) for ENA Rock
% ************************************************************************* 

    r0 = 10; %km
    r1 = 70;
    r2 = 140;
    f0 = max([log10(r0/Rcd) 0]);
    f1 = min([log10(Rcd) log10(r1)]);
    f2 = max([log10(Rcd/r2) 0]);

    ab06Amp = 10.^(ab06.c1 + ab06.c2*M + ab06.c3*M^2 ...
              + (ab06.c4 + ab06.c5*M)*f1 + (ab06.c6 + ab06.c7*M)*f2 ...
              + (ab06.c8 + ab06.c9*M)*f0 + ab06.c10*Rcd);
          
    AB06 = [ab06.T ab06Amp];
    
% ************************************************************************* 
% Calc Atkinson and Boore (2006) for ENA BC
% ************************************************************************* 
    ab06File = 'attn_atkbooreBC06_momag.txt';
    [ab06.T,ab06.c1,ab06.c2,ab06.c3,ab06.c4,ab06.c5,ab06.c6,ab06.c7,ab06.c8,ab06.c9,ab06.c10] ...
    = textread(ab06File,'%f%f%f%f%f%f%f%f%f%f%f',23,'headerlines',4);
    ab06.T(1) = 0.01;

    r0 = 10; %km
    r1 = 70;
    r2 = 140;
    f0 = max([log10(r0/Rcd) 0]);
    f1 = min([log10(Rcd) log10(r1)]);
    f2 = max([log10(Rcd/r2) 0]);

    ab06Amp = 10.^(ab06.c1 + ab06.c2*M + ab06.c3*M^2 ...
              + (ab06.c4 + ab06.c5*M)*f1 + (ab06.c6 + ab06.c7*M)*f2 ...
              + (ab06.c8 + ab06.c9*M)*f0 + ab06.c10*Rcd);
          
    % get soil motion
    pgabc = ab06Amp(1);
%     if pgabc <= 60 % cm/s^2
%         S = log10(exp
          
    AB06BC = [ab06.T ab06Amp];    

% ************************************************************************* 
% Calc Somerville (2009) for Lachlan Foldbelt
% ************************************************************************* 
    [Per C1 C2 C3 C4 C5 C6 C7 C8] = textread('S09_coeff_momag.txt', ...
                              '%s%f%f%f%f%f%f%f%f','headerlines',1);

    m1 = 6.4;
    r1 = 50; %km
    h = 6; %km
    Rjb = sqrt(rhypRange.^2 - h^2);
%     Rjb = rhypRange; % for testing only!
    R = sqrt(Rjb.^2 + h^2);
    R1 = sqrt(r1^2 + h^2);

    for k = 2:length(Per)-1
        T(k-1) = str2num(Per{k});
        if mwRange < m1 & Rjb < r1
            S09(k-1) = exp(C1(k) + C2(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange < m1 & Rjb >= r1
            S09(k-1) = exp(C1(k) + C2(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C6(k)*(log(R) - log(R1)) ...
                      + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange >= m1 & Rjb < r1
            S09(k-1) = exp(C1(k) + C7(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange >= m1 & Rjb >= r1
            S09(k-1) = exp(C1(k) + C7(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C6(k)*(log(R) - log(R1)) ...
                      + C8(k)*(8.5 - mwRange).^2);
        end
    end
    S09 = S09 .* 980;
    S09nc = [T' S09'];
    
% ************************************************************************* 
% Calc Somerville (2009) for Yilgarn
% ************************************************************************* 
    [Per C1 C2 C3 C4 C5 C6 C7 C8 s] = textread('atten_S09yilgarn_coeff_momag.txt', ...
                              '%s%f%f%f%f%f%f%f%f%f','headerlines',1);

    m1 = 6.4;
    r1 = 50; %km
    h = 6; %km
    Rjb = sqrt(rhypRange.^2 - h^2);
%     Rjb = rhypRange; % for testing only!
    R = sqrt(Rjb.^2 + h^2);
    R1 = sqrt(r1^2 + h^2);

    for k = 2:length(Per)-1
        T(k-1) = str2num(Per{k});
        if mwRange < m1 & Rjb < r1
            S09Y(k-1) = exp(C1(k) + C2(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange < m1 & Rjb >= r1
            S09Y(k-1) = exp(C1(k) + C2(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C6(k)*(log(R) - log(R1)) ...
                      + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange >= m1 & Rjb < r1
            S09Y(k-1) = exp(C1(k) + C7(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C8(k)*(8.5 - mwRange).^2);
        elseif mwRange >= m1 & Rjb >= r1
            S09Y(k-1) = exp(C1(k) + C7(k)*(mwRange - m1) + C3(k)*log(R) ...
                      + C4(k)*(mwRange - m1)*log(R) +C5(k)*Rjb + C6(k)*(log(R) - log(R1)) ...
                      + C8(k)*(8.5 - mwRange).^2);
        end
    end
    S09c = S09Y .* 980;
    S09c = [T' S09c'];            

% ************************************************************************* 
% Calc CY (2008) NGA-California
% ************************************************************************* 
    % read GMPE
    cy08File = 'attn_cy08_NGA_coeff_momag.txt';
    [T,c1,c1a,c1b,cn,cM,c5,c6,c7,c7a,c9,c9a,c10,cy1,cy2] = ...
    textread(cy08File,'%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f','headerlines',9);

    % read site file
    cy08File = 'attn_cy08_NGA_sitecoeff_momag.txt';
    [T,phi1,phi2,phi3,phi4,phi5,phi6,phi7,phi8] = ...
    textread(cy08File,'%f%f%f%f%f%f%f%f%f','headerlines',9);

    %period independent
    c2 = 1.06;
    c3 = 3.45;
    c4 = -2.1;
    c4a = -0.5;
    cRB = 50;
    cHM = 3;
    cy3 = 4;
    mech = 1;
%     vs30 = 760;
    ztor = 5;

    for k = 1:length(T)
        if mech == 1 % reverse
            frv = 1;
            fnm = 0;
        elseif mech == 3 % normal
            frv = 0;
            fnm = 1;
        else % strike slip or none
            frv = 0;
            fnm = 0;
        end

        yref = exp(c1(k) + c1a(k)*frv + c1b(k)*fnm + c7(k)*(ztor-4) ...
               + c2*(mwRange-6) + ((c2-c3)/cn(k)) ...
               *log(1+exp(cn(k)*(cM(k)-mwRange))) ...
               + c4*log(rhypRange+c5(k)*cosh(c6(k)*max([(mwRange-cHM) 0]))) ...
               + (c4a-c4)*log(sqrt(rhypRange^2+cRB^2)) ...
               + (cy1(k) + cy2(k)/cosh(max([mwRange-cy3 0]))) * rhypRange);

        % get site effects
        c = phi4(k);
        b = phi2(k)*(exp(phi3(k)*(min(vs30,1130)-360)) ...
            - exp(phi3(k)*(1130-360))); 
        a = phi1(k)*log(vs30/1130)';
        fsite = a + b .* log((yref + c)/c);
        CY08(k) = exp(log(yref) + fsite); 
    end
    CY08 = CY08 * 980;
    CY08 = [T CY08'];
    
% ************************************************************************* 
% Calc Liang et al (2008)
% ************************************************************************* 

    
    l08File = 'attn_liang_mlmag.txt';
    [T a b c d e] = textread(l08File,'%f%f%f%f%f%f','headerlines',1);
    % get ML
    [mlcol mwcol] = textread('WA.ML2MW.lookup.txt','%f%f');
    mwdiff = mwcol - mwRange;
    [mindiff minind] = min(abs(mwdiff));
    ML = mlcol(minind);

%         ML = 5;
    % calc pga
    L08 = zeros(size(T));
    L08(1) = exp(3.688 + 0.832*ML - 0.016* repi ...
           - 1.374 * log(repi) + 0.147 * ML * log(repi));
    % calc rsa
    for k = 2:length(T)
        L08(k) = exp(a(k) + b(k) * ML +c(k)* repi ...
                        + d(k) * log(repi) + e(k) * ML * log(repi));
    end
    L08 = L08 / 10;
    L08 = [T L08];

% ************************************************************************* 
% Calc Lam et al (2011)
% ************************************************************************* 
        
%     T1 = 0.3;
%     T2 = 0.5+((mwRange - 5)/2);
% 
%     S = 1.5;
%     D = 30; % km
%     Q0 = 200;
%     if rhypRange <= 1.5*D
%         G = 10^(-1.0 * log10(rhypRange)) / 0.0333;
%     elseif rhypRange > 1.5*D & rhypRange <= 2.5*D
%         G = 10^(-1.0 * log10(1.5*D)) / 0.0333;
%     else
%         G = 10^(-1.0 * log10 (1.5*D) + 0.0 * log10 (2.5*D/(1.5*D)) ...
%             + -0.5 * log10(rhypRange/(2.5*D))) / 0.0333;
%     end
% 
%     av = 70 * (0.35 + 0.65 * (mwRange - 5)^1.8); %mm/s
%     % get beta
%     c1 = 0.005;
%     c2 = 0.043*(Q0/100)^2 - 0.53*(Q0/100)+1.8;
%     cm = min([1 1 - ((7.8 - mwRange)/1.8) * (1 - (1.86-0.22*log(rhypRange)))]);
%     eta = 0.022*(Q0/100)+0.8;
%     c2 = 1;
%     cm = 1;
%     eta = 1;
%     if rhypRange < (1.5*D)
%         beta = (30/rhypRange)^(c1*rhypRange);
%     else
%         beta = cm * (30/rhypRange)^(c1*c2*rhypRange*eta); % v confusing!
%     end
%     
%     vmax = av * G * 
%     ad = av * (T2 / 2*pi);
%     amax = vmax * (2*pi/T1);   

% ************************************************************************* 
% Calc Gaull (1990) Eeastern Australia
% *************************************************************************
% Y = a * exp(b*ML) / R^c

% get ML
[mlcol mwcol] = textread('SEA.ML2MW.lookup.txt','%f%f');
mwdiff = mwcol - mwRange;
[mindiff minind] = min(abs(mwdiff));
ML = mlcol(minind);

R = sqrt(repi^2 + depth^2 + 0^2);
GSEApga = 0.088 * exp(1.10*ML) / R^1.20;

% get spectral shape factors
[G90T spec_fact] = textread('AS1170.4_spec_shape_fact_rock.csv','%f%f','delimiter',',');
G90T(1) = 0.01;
G90SEA = GSEApga .* spec_fact * 100; % m/s2 to cm/s2
G90SEA = [G90T G90SEA];

% ************************************************************************* 
% Calc Gaull (1990) Western Australia
% ************************************************************************* 
% get ML
[mlcol mwcol] = textread('WA.ML2MW.lookup.txt','%f%f');
mwdiff = mwcol - mwRange;
[mindiff minind] = min(abs(mwdiff));
ML = mlcol(minind);

R = sqrt(repi^2 + depth^2 + 0^2);
GWApga = 0.025 * exp(1.10*ML) / R^1.03;

% get spectral shape factors
[G90T spec_fact] = textread('AS1170.4_spec_shape_fact_rock.csv','%f%f','delimiter',',');
G90T(1) = 0.01;
G90WA = GWApga .* spec_fact * 100; % m/s2 to cm/s2
G90WA = [G90T G90WA];

% ************************************************************************* 
% Calc Campbell (2003)
% *************************************************************************

camp03File = 'attn_camp03_hybrid_coeff_momag.txt';
[T,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13] ...
= textread(camp03File,'%f%f%f%f%f%f%f%f%f%f%f%f%f%f','headerlines',8);

R = sqrt(rhypRange.^2 + (c7.*exp(c8*mwRange)).^2);

f12 = c1 + c2*mwRange + c3*(8.5-mwRange).^2 + c4.*log(R) + (c5+c6*mwRange).*rhypRange;
% assume PGV at 1 Hz        

for i = 1:length(rhypRange)
    if rhypRange <= 70
        f3 = 0;
    elseif rhypRange > 70 && rhypRange <= 130
        f3 = c9*(log(rhypRange) - log(70));
    elseif rhypRange > 130
        f3 = c9*(log(rhypRange) - log(70)) ...
                   + c10*(log(rhypRange) - log(130));
    end
end

C03 = exp(f12 + f3) .* 980;
C03 = [T C03];

% ************************************************************************* 
% Calc Allen 2012
% *************************************************************************

%load model
% disp(depth);
if depth >= 10
    load 'G:\Modelling\EXSIM\Simulations\AUS11_deep.mat';
else
    load 'G:\Modelling\EXSIM\Simulations\AUS11_shallow.mat';
end

model = model(1:end-2,:);
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
r01 = 80;
r02 = 150;

for j = 1:length(minr1)
    r1 = r01 + (M-4)*c8(j);
    r2 = r02 + (M-4)*c11(j);
    minr1(j) = min([log10(rhypRange) log10(r1)]);
    maxr2(j) = max([log10(rhypRange/r1) 0]);
    maxr3(j) = max([log10(rhypRange/r2) 0]);
end
minr1 = 10.^minr1;

A12 = 10.^(c0 + c1 * (M-4) + c2*(M-4).^2 ...
      + (c3 + c4*(M-4)).*log10(sqrt(minr1.^2 ...
      + (ones(size(minr1)).*(1+c5*(M-4))).^2)) ...
      + maxr2.*(c6 + c7*(M-4)) ...
      + maxr3.*(c9 + c10*(M-4)));

AT = 1 ./ model(:,1);
A12 = [AT A12];
      


        
