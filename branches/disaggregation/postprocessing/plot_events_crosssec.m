function [event_struct] = plot_events_crosssec(samprate, ...
                                                fname, ...
                                                sname, ...
                                                plottype, ...
                                                cval, ...
                                                fault_start, ...
                                                fault_end, ...
                                                fh)
% Function to plot synthetic ruptures in cross section. the cross 
% section is perpendicular to the fault trace defined by fault_start
% and fault_end
%
% INPUTS: 
% samprate      [integer] sampling rate for plotting of synethtic ruptures.
%               For example;  samprate=10 => plot every tenth rupture
%                             samprate= 1 => plot all synthetic ruptures 
% fname         [string] file name for EQRM generated event set
% sname         [string] file name for outputfiles. If empty the figures
%               are not saved
% plottype      [switch]
%                   'onecolor'  => FAST plot all synthetic ruptures the color
%                                       given by cval
%                   'twocolors' => SLOW plot the events requiring flipping
%                                  due to dip direction red - plot the 
%                                  other black
% cval          [string] color (e.g. 'k' for synthetic ruptures if 
%               plottype = 'onecolor'
% fault_start   [double] [lon,lat] of start of fault trace - used as origin
%               for plot
% fault_end     [double] [lon,lat] of end of fault trace - used to define
%               azimuth of the new x-axis. Cross section is perpendicular 
%               to the fault trace defined by fault_start and fault_end    
% fh            [double 1x2] contains figure handles if rupters are to be
%               added to an existing plot. Otherwise, if fh is empty new
%               figures are created. 
% 
% OUTPUTS: 
% event_struct  [structure] Parameters of interest from the event
% 
% NOTES: 
% (1)   Should be useable for all types of events (e.g. source zone, 
%       fault and intraslab) but not yet tested
% (2)   May not be bomb proof for all azimuths
% (3)   uses Vincenty_Inverse formula to compute distance along ellipsoid 
%       between two points defined by lats and lons. This will give
%       small differences from ll2xy which is shperical. Consider swapping 
%       ll2xy for consistency with event generation in the EQRM. This may
%       be the cause for the width in the cross section of the centroids
%       (i.e. we might expect these to align in a perfect line)
%
% David Robinson
% 10 November 2010

tic   %start a timer

%=====================================================================
% Some Default Input Values
if nargin ==0 
    samprate = 5;
    fname = 'java_event_set.txt';
    sname = 'temp';
    plottype = 'onecolor'; %'twocolors'
    cval = 'k';  % only works for when both dip directions are plotted in same color
    fh = [];
    fault_start = [112.433555,-10.338979];
    fault_end = [105.822974,-8.60524];
end
%=====================================================================
%% Unwrap the fault start and end points (i.e. in lats and lons)
% The start of this trace becomes the origin 
% The end of this trace is ude to define the direction (or azimuth) of the trace
% The plotted cross sections are perpendicular to this trace
xs1 = fault_start(1);  % longitude of start of trace (used for origin)
ys1 = fault_start(2); % latitude of start of trace (used for origin)
xe1 = fault_end(1); % longitude of end of trace (used for direction)
ye1 = fault_end(2); % latitude of end of trace (used for direction)

%% =======================================================================
% load the event set
events = load(fname);
lats = events(:,11);
lons = events(:,12);
depths = events(:,13);
dips = events(:,7);
azi = events(:,6);
widths = events(:,17);
Mw = events(:,10);

%% =======================================================================
% Package up the relevent bits of the event set for output
event_struct.lats = lats; 
event_struct.lons = lons; 
event_struct.depths = depths; 
event_struct.dips = dips; 
event_struct.azi = azi; 
event_struct.widths = widths; 
event_struct.Mw = Mw; 

%% ====================================================
% Do some angle stuff

% angle between reference fault trace and horizontal (constant latitude)
% As measured at the start of the trace. 
theta = acos(abs(ye1-ys1)/abs(xe1-xs1));

% Consider Quadrants - important for link between azimuth and dip
% We must compute angle at which dips require flipping. 
% WARNING - may not be bomb proof for all azimuths
%
% Quadrant Map - start of trace in centre (end of trace)
%     | 
%  I  | II
%-----------
% III | IV
%     |
LatIncrease = ye1-ys1;
LonIncrease = xe1-xs1;
if  LatIncrease >= 0 & LonIncrease >=0  % quadrant I
    traceazi = 90 - theta*180/pi;
elseif LatIncrease >= 0 & LonIncrease <=0  % quadrant II
    traceazi = 270+ theta*180/pi;
elseif LatIncrease <= 0 & LonIncrease <=0  % quadrant III
    traceazi = 270- theta*180/pi;
elseif LatIncrease <= 0 & LonIncrease >=0  % quadrant III
    traceazi = 90+ theta*180/pi;
else
    error('ERROR: you should not be here')
end

%% ====================================================
% Convert to origin at start of trace (still in lats and longs)
% make everything a step from the start of trace1 fault_start
Dlats = lats-ys1; 
Dlons = lons-xs1; 

%% ====================================================
% Convert to a locally defined x,y,z (as in EQRM manual)
% i.e. with origin at start of fault trace of interest. 
 
% get rough distance for lat/lon to x y conversion (measured along ellipsoid)
[longstep, alpha12, alpha21] = vincenty_inverse(-9,108,-9,109);
longstep = longstep/1000; % rough km distance per degree of longitude

% get rough distance for lat/lon to x y conversion (measured along ellipsoid)
[latstep, alpha12, alpha21] = vincenty_inverse(-9,109,-10,109);
latstep = latstep/1000; % rough km distance per degree of longitude

% HINT - YOU MAY WISH TO SWAP vincenty_inverse to ll2xy later

Dx = Dlats*latstep; 
Dy = Dlons*longstep;

% Now, we must rotate these to be in the correct plane
% Note that rotation is of x and y coordinates only - z does not change
Rtheta = [cos(theta) -sin(theta); sin(theta) cos(theta)];

newX = zeros(size(Dx));
newY = zeros(size(Dy));
for i = 1:length(Dx)
    tmp =  Rtheta*[Dx(i);Dy(i)];
    newX(i) = tmp(1); 
    newY(i) =tmp(2);
end

%% Plot the centroids
if isempty(fh)
    figure % create a new figure
else
    figure(fh(1)) % get the figure you want (i.e. the one to add too)
end
plot(newY,depths,'.')
set(gca,'ydir','reverse')

if ~isempty(sname)
    xlabel('y (km)')
    ylabel('z (km)')
    print('-dpng',[sname,'_centroids.png'])
end



%% =======================================================================
% Generate data defining the rupture traces in the cross section
% These are defined by a start point (sp
nlen = floor(length(Dy)/samprate);
spy =  zeros(nlen,1);
epy =  zeros(nlen,1);
spd = zeros(nlen,1);
epd = zeros(nlen,1); 
colors = zeros(nlen,3);

% Dip flip angle
dfa = 180+traceazi;
if dfa>=180
    dfa = dfa-360;
end

% Do one dip direction
ind = find(azi<=dfa);
spy(ind) =  newY(ind) - widths(ind)./2.*cos(dips(ind)*pi/180);
epy(ind) =  newY(ind) + widths(ind)./2.*cos(dips(ind)*pi/180);
spd(ind) = depths(ind) + widths(ind)./2.*sin(dips(ind)*pi/180);
epd(ind) = depths(ind) - widths(ind)./2.*sin(dips(ind)*pi/180);  
colors(ind,:) = repmat([0,0,0],length(ind),1);  % set to black

% Do the other dip direction
ind = find(azi>180+dfa);
spy(ind) =  newY(ind) + widths(ind)./2.*cos(dips(ind)*pi/180);
epy(ind) =  newY(ind) - widths(ind)./2.*cos(dips(ind)*pi/180);
spd(ind) = depths(ind) + widths(ind)./2.*sin(dips(ind)*pi/180);
epd(ind) = depths(ind) - widths(ind)./2.*sin(dips(ind)*pi/180);  
colors(ind,:) = repmat([1,0,0],length(ind),1);  % set to red

%% =======================================================================
% Now do the plotting
if isempty(fh)
    figure % create a new figure
else
    figure(fh(2)) % get the figure you want (i.e. the one to add too)
end

switch plottype
    case 'onecolor'  % FAST = plot all synthetic ruptures the same color
        ymatrix = [spy(1:samprate:length(Dy)),epy(1:samprate:length(Dy))]';
        dmatrix = [spd(1:samprate:length(Dy)),epd(1:samprate:length(Dy))]'; 
        plot(ymatrix,dmatrix,'color',cval)
        set(gca,'ydir','reverse','ylim',[0,500],'xlim',[0, 500])
        hold on
    case 'twocolors' % SLOW = use dip direction to change color of synthetic ruptures
        for i = 1:samprate:length(Dx) 
            plot([spy(i), epy(i)],[spd(i),epd(i)],'color',colors(i,:)) 
            set(gca,'ydir','reverse','ylim',[0,500],'xlim',[0, 500])
            hold on    
        end
end
if ~isempty(sname)
        xlabel('y (km)')
    ylabel('z (km)')
    print('-dpng',[sname,'_traces.png'])
end

toc
