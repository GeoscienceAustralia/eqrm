function mindist = dist2plane(stnlon,stnlat,faultmatmain)
% finds the closest distance from a station to any point on a
% fault plane
%% test data
% clear all;
% stnlat = 63.650;
% stnlon = -147.267;
% faultmatmain =[-147.807 63.434 0.000
%                 -147.210 63.472 0.000
%                 -147.267 63.650 22.294
%                 -147.864 63.613 22.294
%                 -147.807 63.434 0.000
%                 NaN NaN NaN 
%                 -146.951 63.551 0.000
%                 -147.551 63.518 0.000
%                 -147.551 63.518 30.000
%                 -146.951 63.551 30.000
%                 -146.951 63.551 0.000
%                 NaN NaN NaN 
%                 -145.968 63.453 0.000
%                 -146.952 63.547 0.000
%                 -146.952 63.547 30.000
%                 -145.968 63.453 30.000
%                 -145.968 63.453 0.000
%                 NaN NaN NaN 
%                 -143.586 62.872 0.000
%                 -145.996 63.427 0.000
%                 -145.996 63.427 30.000
%                 -143.586 62.872 30.000
%                 -143.586 62.872 0.000
%                 NaN NaN NaN 
%                 -142.500 62.114 0.000
%                 -143.669 62.831 0.000
%                 -143.669 62.831 30.000
%                 -142.500 62.114 30.000
%                 -142.500 62.114 0.000];
%        
%[stnlon,stnlat]
%[faultmat(:,1),faultmat(:,2)]
% stnlat = 37.175;
% stnlon = -121.95;
% stnlat = 36.972;
% stnlon = -121.655;

% faultmatmain = [-121.665	36.972	1.500
%                 -122.020	37.193	1.500
%                 -122.067	37.145	20.294
%                 -121.712	36.924	20.294
%                 -121.665	36.972	1.500];
% plot(faultmatmain(:,1),faultmatmain(:,2),'b-',stnlon,stnlat,'r*');



%% check to see if multi-dimensions
nanind = find(isnan(faultmatmain(:,1)));
nanind = [0 nanind' length(faultmatmain(:,1))+1];
mindist = 99999999;
clear dist dist2poly;

for mf = 1:length(nanind)-1
    faultmat = faultmatmain(nanind(mf)+1:nanind(mf+1)-1,:);

    %% if fault has vertical dimensions
    % iterate around fault perimeter to find shortest distance
    tmpdist1 = 9999999;
    for i = 1:length(faultmat(:,1))-1
        [edgedist edgeaz] = distance(faultmat(i,2),faultmat(i,1), ...
                                     faultmat(i+1,2),faultmat(i+1,1));
        edgevect = 0:0.0001:edgedist;
        [tmplat tmplon] = reckon(faultmat(i,2),faultmat(i,1),edgevect,edgeaz);
        tmpdist2 = distance(stnlat,stnlon,tmplat,tmplon);
        if min(tmpdist2) < tmpdist1
            tmpdist1 = min(tmpdist2);
        end
    end
    dist2poly = deg2km(tmpdist1);
    
    %% in poly
    inpoly = p_poly_dist(stnlon,stnlat,faultmat(:,1),faultmat(:,2));

    if max(faultmat(:,3)) > 0
        %% find top coords
        topInd = find(faultmat(:,3) == min(faultmat(:,3)));
%         topInd = topInd(1);
        [dist2top topaz] = distance(stnlat,stnlon,faultmat(topInd,2),faultmat(topInd,1));
        dist2top = deg2km(dist2top);
        minTopInd = find(dist2top == min(dist2top));
        dist2top = dist2top(minTopInd(1));
        topaz = topaz(minTopInd(1));
        topLat = faultmat(minTopInd(1),2);
        topLon = faultmat(minTopInd(1),1);

        %% find bottom coords
        botInd = find(faultmat(:,3) == max(faultmat(:,3)));
        [dist2bot botaz] = distance(stnlat,stnlon,faultmat(botInd,2),faultmat(botInd,1));
        dist2bot = deg2km(dist2bot);
        minBotInd = find(dist2bot == min(dist2bot));
        dist2bot = dist2bot(minBotInd(1));
        botaz = botaz(minBotInd(1));
        botLat = faultmat(botInd(minBotInd(1)),2);
        botLon = faultmat(botInd(minBotInd(1)),1);
        if dist2poly > dist2bot-0.25 & dist2poly < dist2bot+0.25
            dist2poly = dist2bot;
        end

        %% get surface dist from top to bottom
        [top2botdist az] = distance(topLat,topLon,botLat,botLon);
        top2botdist = deg2km(top2botdist);
        
        %% get distance along fault from top edge
        if top2botdist ~= 0
            distonfault = sqrt(dist2top^2 + dist2poly^2);
            topaz180 = topaz+180;
            if topaz180 > 360
                topaz180 = topaz180 - 360;
            end
            az_top2site = az - topaz180;
            distonfault = dist2top * cos(az_top2site*pi/180);
            dep2fault = interp1([0 top2botdist],[min(faultmat(:,3)) max(faultmat(:,3))], ...
                        distonfault,'linear','extrap');
            if dep2fault > max(faultmat(:,3))
                dep2fault = max(faultmat(:,3));
            end
            if dep2fault < min(faultmat(:,3))
                dep2fault = min(faultmat(:,3));
            end
            dipangle = atan((max(faultmat(:,3)) - min(faultmat(:,3)))/top2botdist);
        end
        %% if site above fault plane projection
        if inpoly <= 0 & top2botdist ~= 0
            % vertical dist
            vertdist = dep2fault;
            %  dist to top edge
            topedgedist = sqrt(distonfault^2 + min(faultmat(:,3))^2);
            if vertdist <= topedgedist
                dist = vertdist;
            else
                dist = topedgedist; 
            end
        %% if site just outside fault projection to side
        elseif dist2poly < dist2top && dist2poly < dist2bot ...
               && dep2fault > min (faultmat(:,3)) && dep2fault < max(faultmat(:,3))
            % vertical dist
            vertdist = sqrt(dep2fault^2 + dist2poly^2);
            %  dist to top edge
            topedgedist = sqrt(dist2top^2 + min(faultmat(:,3))^2);
            if vertdist <= topedgedist
                dist = vertdist;
            else
                dist = topedgedist; 
            end
        
        %% if site closer to bottom edge
        elseif dist2poly < dist2top && dist2poly < dist2bot && dist2bot < dist2top
            % vertical dist
            vertdist = sqrt(dep2fault^2 + dist2poly^2);
            %  dist to top edge
            topedgedist = sqrt(distonfault^2 + min(faultmat(:,3))^2);
            if vertdist <= topedgedist
                dist = vertdist;
            else
                dist = topedgedist; 
            end
        
        %% if site closer to top edge
        elseif dist2top < dist2bot
            dist = sqrt(min(faultmat(:,3))^2 + dist2poly^2);
        %% if site bottom to the side
        elseif dist2bot < dist2top
            % get horiz distance
            if dist2poly > dist2bot-0.25 & dist2poly < dist2bot+0.25
                horizdist = dist2poly;
            end
            vertdist = sqrt(max(faultmat(:,3))^2 + horizdist^2);
            %  dist to top edge
            topedgedist = sqrt(dist2top^2 + min(faultmat(:,3))^2);
            if vertdist <= topedgedist
                dist = vertdist;
            else
                dist = topedgedist; 
            end
        %% if perfectly verticalfault
        elseif faultmat(1,1) == faultmat(2,1) & faultmat(1,2) == faultmat(2,2)
            dist = dist2poly;
        elseif faultmat(2,1) == faultmat(3,1) & faultmat(2,2) == faultmat(3,2)
            dist = dist2poly;  
        end
    %% else if surface trace only
    else
        dist = dist2poly;
    end

    if dist < mindist
        mindist = dist;
    end
%     dist2poly
%     mindist
end






    