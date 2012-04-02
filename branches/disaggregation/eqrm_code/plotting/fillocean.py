import numpy as num

from matplotlib.patches import Polygon


def fillcontinentsX(self,color='0.8',lake_color=None,ax=None,zorder=None):
    """
    Fill continents.

    .. tabularcolumns:: |l|L|

    ==============   ====================================================
    Keyword          Description
    ==============   ====================================================
    color            color to fill continents (default gray).
    lake_color       color to fill inland lakes (default axes background).
    ax               axes instance (overrides default axes instance).
    zorder           sets the zorder for the continent polygons (if not
                     specified, uses default zorder for a Polygon patch).
                     Set to zero if you want to paint over the filled
                     continents).
    ==============   ====================================================

    After filling continents, lakes are re-filled with
    axis background color.

    returns a list of matplotlib.patches.Polygon objects.
    """
    if self.resolution is None:
        raise AttributeError, 'there are no boundary datasets associated with this Basemap instance'
    # get current axes instance (if none specified).
    ax = ax or self._check_ax()
    # get axis background color.
    axisbgc = ax.get_axis_bgcolor()
    npoly = 0
    polys = []
    for x,y in self.coastpolygons:
        xa = num.array(x,num.float32)
        ya = num.array(y,num.float32)
    # check to see if all four corners of domain in polygon (if so,
    # don't draw since it will just fill in the whole map).
        delx = 10; dely = 10
        if self.projection in ['cyl']:
            delx = 0.1
            dely = 0.1
        test1 = num.fabs(xa-self.urcrnrx) < delx
        test2 = num.fabs(xa-self.llcrnrx) < delx
        test3 = num.fabs(ya-self.urcrnry) < dely
        test4 = num.fabs(ya-self.llcrnry) < dely
        hasp1 = num.sum(test1*test3)
        hasp2 = num.sum(test2*test3)
        hasp4 = num.sum(test2*test4)
        hasp3 = num.sum(test1*test4)
        if not hasp1 or not hasp2 or not hasp3 or not hasp4:
            xy = zip(xa.tolist(),ya.tolist())
            if self.coastpolygontypes[npoly] not in [2,4]:
                poly = Polygon(xy,facecolor=color,edgecolor=color,linewidth=0)
            else: # lakes filled with background color by default
                if lake_color is None:
                    poly = Polygon(xy,facecolor=axisbgc,edgecolor=axisbgc,linewidth=0)
                else:
                    poly = Polygon(xy,facecolor=lake_color,edgecolor=lake_color,linewidth=0)
            if zorder is not None:
                poly.set_zorder(zorder)
            ax.add_patch(poly)
            polys.append(poly)
        npoly = npoly + 1
    # set axes limits to fit map region.
    self.set_axes_limits(ax=ax)
    return polys

