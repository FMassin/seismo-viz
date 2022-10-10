#!/usr/bin/env python3

import numpy
import matplotlib.pyplot
import matplotlib.ticker
import sys

# the model values
m=0.0001
try:
    m=float(sys.argv[1])
except:
    print('Default reference model value is setup to %g'%m)
    print('Use',' '.join(sys.argv),'<model value> to set a different reference model value')

# the observed values
x = numpy.logspace(numpy.log10(m)-3,numpy.log10(m)+3,64)

# the plot
ax=matplotlib.pyplot.figure().gca()

# ref model value line
ax.axvline(m, lw=2, c='C4', label='Model amplitude (m)')

# functions
## function 1
y = numpy.log10(x) / numpy.log10(m)
y[y>1]=1/y[y>1]
ax.plot(x,y,label='$F=$($1/$)$log(o)/log(m)$')

## function 2
y=1-numpy.abs(numpy.log10(x)-numpy.log10(m))
ax.plot(x,y,label='$F=1-|log(m) - log(x)|$')

## function 3
y=1- (((x-m)**2)/((m+x)**2))
ax.plot(x,y,label='$F = 1-(o+m)^2/(m+x)^2$')

## function 4
y=1- (numpy.log10(x)-numpy.log10(m))**2/3
ax.plot(x,y,label='$F = 1-(log(o)-log(m))^2/3$')

# make the plot nice 
ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
ax.tick_params(right=True, top=True,
               left=True, bottom=True,
               which='both')
ax.grid(visible=True, which='major', color='gray', linestyle='dashdot', zorder=-99)
ax.grid(visible=True, which='minor', color='beige',  ls='-', zorder=-99)

# add plot features
ax.legend()
ax.set_xscale('log')
ax.set_xlabel('Observed amplitude (o)')
ax.set_ylabel('Fit (F)')

# render the plot
matplotlib.pyplot.show()
