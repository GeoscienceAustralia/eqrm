function [s, alpha12, alpha21] = vincenty_inverse(lat1,lon1,lat2,lon2);
% VINCENTY_INVERSE applies Vincenty's inverse formulae to compute the
% ellipsoid distance (s) between two points [lat long] on the ellipsoid
% surface. It users important parameters from the ellipsoid GRS80. Note
% that these GRS80 parameters are also adopted with GDA94. 
%
% USAGE:
%   [s, alpha12, alpha21] = vincenty_inverse(lat1,lon1,lat2,lon2);
%
% INPUTS:
% lat1      [float] latitude of 1st point {degrees}
% lon1      [float] longitude of 1st point {degrees}
% lat2      [float] latitude of 2nd point {degrees}
% lon2      [float] longitude of 2nd point {degrees}
%
% OUTPUTS:
% s         [float] distance between point 1 and 2
% alpha12   [float] azimuth from point 1 to point 2  {degrees}
% alpha21   [float] azimuth from point 2 to point1 {degrees}
%
% Note:
% * refer to Geocentric Datum of Australia Technical Manual V2.0 for 
%   further information.
% * the outputs alpha12 and alpha21 have not been corrected for sign
%   changes in the body of the code. This means that they may be out 
%   by sign or translated by 180/360 etc. 
%
%
% David Robinson
% 17 October 2003

% Define important ellipsoid parameters for GRS80
f = 1/298.257222101;
a = 6378137.0;
b = a*(1-f);

% convert from degrees to radians
lat1 =lat1*pi/180;
lon1=lon1*pi/180;
lat2=lat2*pi/180;   
lon2=lon2*pi/180;
n=length(lat1);

% note that U1 is very close to lat1 and U2 is very close to lat2
% we assume -90 < U1,U2 < 90
TanU1 = (1-f)*tan(lat1);

U1 = atan(TanU1); SinU1=sin(U1); CosU1 = cos(U1); 
%[U1,SinU1,CosU1] = LOC_findU(TanU1)    ;
TanU2 = (1-f)*tan(lat2);
U2 = atan(TanU2); SinU2=sin(U2); CosU2 = cos(U2); 
%[U2,SinU2,CosU2] = LOC_findU(TanU2);

lambda = abs(lon2-lon1);
omega = lambda;


for i = 1:10000
    Sin2_sigma = (CosU2.*sin(lambda)).^2 + (CosU1.*SinU2-SinU1.*CosU2.*cos(lambda)).^2;
    Cos_sigma = SinU1.*SinU2 + CosU1.*CosU2.*cos(lambda);
    Tan_sigma = sqrt(Sin2_sigma)./Cos_sigma;
    sin_alpha = CosU1.*CosU2.*sin(lambda)./sqrt(Sin2_sigma);
    cos_2sigmam = Cos_sigma - (2.*SinU1.*SinU2./(1-sin_alpha.^2));
    C = (f/16).*(1-sin_alpha.^2).*(4*ones(n,1)+f.*(4*ones(n,1)-3.*(1-sin_alpha.^2)));
    lambda_old = lambda;
    lambda = omega + (1-C).*f.*sin_alpha.*(acos(Cos_sigma) + C.*sqrt(Sin2_sigma).*...
        (cos_2sigmam+C.*Cos_sigma.*(-ones(n,1)+2.*cos_2sigmam.^2)));
    if abs(lambda_old-lambda)<10^(-20), break, end
end
disp(' ')
disp('=================================================================')
disp(['VINCENTY_INVERSE distance calculator has taken ',num2str(i)])
disp('iteration(s) to converge')
disp('=================================================================')


u2 = (1-sin_alpha.^2).*(a^2-b^2)/b^2;
A = 1 + (u2/16384).*(4096*ones(n,1) +u2.*(-768*ones(n,1) +u2.*(320*ones(n,1)-175.*u2)));
B = (u2/1024).*(256*ones(n,1)+u2.*(-128*ones(n,1)+u2.*(74*ones(n,1)-47*u2)));
delta_sigma = B.*sqrt(Sin2_sigma).*(cos_2sigmam+(B/4).*(Cos_sigma.*(-ones(n,1)+2*cos_2sigmam.^2)-...
    (B/6).*cos_2sigmam.*(-3*ones(n,1)+4*Sin2_sigma).*(-3*ones(n,1)+4*cos_2sigmam.^2)));
s = b.*A.*(acos(Cos_sigma)-delta_sigma);


Tan_alpha12 = (CosU2.*sin(lambda))./(CosU1.*SinU2-SinU1.*CosU2.*cos(lambda));
Tan_alpha21 = (CosU1.*sin(lambda))./(-SinU1.*CosU2+CosU1.*SinU2.*cos(lambda));
    
alpha12 = 180/pi*atan(Tan_alpha12);
alpha21 = 180/pi*atan(Tan_alpha21);
    
    
% function [U,SinU,CosU] = LOC_findU(TanU)
% U = atan(TanU);    % in radians
% if U>=0 & U<=pi  % angle is in top right quadrant (SinU>0 & CosU>0)
%     SinU = sin(abs(U));
%     CosU = cos(abs(U));
% elseif U<0 & U>=-pi  % angle is in bottom right quadrant (SinU<0 & CosU>0)
%     SinU = -sin(abs(U));
%     CosU = cos(abs(U));    
% else
%     error('Invalid value for U: may indicate an error in user defined latitude')
% end
% 
% % function [sigma, Sin_sigma, Tan_sigma] = LOC_fin_sigma(Cos_sigma);
% % sigma = arccos