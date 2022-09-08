#!/usr/bin/env python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import obspy.core.event.catalog, obspy.geodetics.base
from obspy.clients.fdsn import Client as fdsnClient
from numpy import mean,std
from sys import argv
golden = (1 + 5 ** 0.5) / 2

"""
Displaying WMTS tiled map data
------------------------------

This displays imagery from a web map tile service and seismic events from an FDSN web service. This result can also be interactively panned and zoomed.

"""

def plot_eq(ax,m,marker,color=None,**opts):

    o=m.origin_id.get_referred_object()
    desc='%.3g km deep %s%.2g\nat %s\nby %s (%s)'%(o.depth/1000,m.magnitude_type,m.mag,m.creation_info.creation_time,m.creation_info.author,m.creation_info.agency_id)
    ax.plot(o.longitude,o.latitude,marker,color='w',zorder=1,markeredgewidth=4,**opts)
    ax.plot(o.longitude,o.latitude,marker,color='k',zorder=2,markeredgewidth=1,**opts)
    if color is not None:
        opts['color']=color
    ax.plot(o.longitude,o.latitude,marker,zorder=3,markeredgewidth=0,**opts,label=desc)
    

def plot_wms(self,
             fdsnws_uri='ETH',
             wms = 'https://wms.geo.admin.ch',
             layers = ['ch.swisstopo.pixelkarte-farbe'],
             crs = ccrs.Orthographic,
             **kwargs):

    if self is not obspy.core.event.catalog.Catalog:
        self = fdsnClient(fdsnws_uri).get_events(**kwargs)

    longitude=[]
    latitude=[]
    for e in self:
        longitude+=[o.longitude for o in e.origins]
        latitude+=[o.latitude for o in e.origins]

    longitude+=[min(longitude)-std(longitude), 
                   max(longitude)+std(longitude)]
    latitude+=[min(latitude)-std(latitude), 
                   max(latitude)+std(latitude)]
    
    kmlo,az,baz=obspy.geodetics.base.gps2dist_azimuth(mean(latitude),mean(longitude),
                                                    mean(latitude),mean(longitude)+1)
    kmla,az,baz=obspy.geodetics.base.gps2dist_azimuth(mean(latitude),mean(longitude),
                                                    mean(latitude)+1,mean(longitude))
    y = latitude.copy()
    x = longitude.copy()
    if max(longitude)-min(longitude) > kmla/kmlo*golden*(max(latitude)-min(latitude)):
        # Too large
        m = mean(y)
        d = max(x)-min(x)
        latitude.append(m + d/(2*golden))
        latitude.append(m - d/(2*golden))
    else:
        # Too high
        m = mean(x)
        d = max(y)-min(y)
        longitude.append(m + kmla/kmlo*d*golden/2)
        longitude.append(m - kmla/kmlo*d*golden/2)
        
    # Create a Cartopy crs for plain and rotated lat-lon projections.
    projection = crs(central_longitude=mean(longitude), 
                     central_latitude=mean(latitude))


    # Plot WMTS data in a specific region, over a plain lat-lon map.
    fig = plt.figure(figsize=(12*golden,12))    
    ax = plt.axes([0, 0, 1, 1], projection=projection)
    ax.set_extent([min(longitude), 
                   max(longitude), 
                   min(latitude), 
                   max(latitude)], 
                  ccrs.PlateCarree())

    #ax.coastlines(resolution='50m', color='yellow')
    #ax.gridlines(color='lightgrey', linestyle='-')
    
    # Add WMS imaging.    
    ax.add_wms(wms=wms,
               layers=layers)

    # Add earthquakes
    opts={'transform':ccrs.PlateCarree(),
          'solid_capstyle':'round',
          'markersize':16}
    # Breaks projection: cat.plot(fig=ax,method='cartopy',**opts)
    for e in self:
        m=e.preferred_magnitude()
        plot_eq(ax,m,'o',**opts)
        if len(self)==1:
            for m in e.magnitudes:
                if m is e.preferred_magnitude():
                    continue
                if m.magnitude_type != e.preferred_magnitude().magnitude_type :
                    continue
                plot_eq(ax,m,'P',**opts)

    if len(self)==1:
        ax.legend()
    plt.show()


## obspy integration should be:
#class Origin(...):
#
#    def delay(self, ...):
#        return utils._delay(self, ...)
## But the quick and dirty is:
obspy.core.event.catalog.Catalog.plot_wms = plot_wms
## Any instance of Catalog has the method plot_wms 

if __name__ == '__main__':

    if '-h' in argv:
        print(' Try:\n%s "eventid=smi:ch.ethz.sed/sc20a/Event/2022rrcgvq" "includeallmagnitudes=1" "includeallorigins=1"'%argv[0])
    else:
        args={ arg.split('=')[0]:arg.split('=')[1] for arg in argv if "=" in arg}
        print('Arguments provided:')
        print(args)

        plot_wms(None,**args)
