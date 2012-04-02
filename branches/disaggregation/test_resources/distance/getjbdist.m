function jbdist = getjbdist(stnlon,stnlat,faultmat)
% gets JB distance

hypotdist = deg2km(distance(stnlat,stnlon,faultmat(:,1),faultmat(:,2)));
hypotazim = azimuth(stnlat,stnlon,faultmat(:,1),faultmat(:,2));
xdist = hypotdist .* sin(hypotazim * pi / 180);
ydist = hypotdist .* cos(hypotazim * pi / 180);
jbdist = p_poly_dist(0,0,xdist,ydist);
if jbdist < 0
    jbdist = 0;
end

