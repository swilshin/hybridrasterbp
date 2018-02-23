'''
FILE: plotters.py

The function hybridRasterBp creates a hybrid raster, boxplot and violin plot on 
the current matplotlib axis.

A raster plot is a plot with each data point  represented by a single marker, 
a boxplot performs aggregation and has a box with a line indicating some measure 
of central tendency. The edges of the box indicate a measure of spread. Whiskers 
are added to the box provide both a further indication of spread, and to 
indicate outliers which are plotted with their own markers. Outlier as already 
plotted in the raster plot so there are disabled here. A violin plot uses kernel 
density estimation to approximate the distribution of the data, a line indicates 
this approximate distribution. Typically a violin plot will have markers 
indicating some measure of central tendency and spread, but this is not 
done here since these are already present on the boxplot.

The raster plot is created using the scatter function. the boxplots are created 
using the boxplot function, and the violin plots are created using the 
gaussian_kde function from scipy. All this function really does is organise 
these elements on the page.

This file is part of the hybrid raster boxplot project.

the hybrid raster boxplot project is free software: you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created by Simon Wilshin
Date 2018/02/23
'''

import matplotlib.patches as patches
from matplotlib.pyplot import gca,plot,fill_betweenx

from scipy.stats import gaussian_kde
from numpy import array,arange,ones_like,linspace

from itertools import izip,cycle

def hybridRasterBp(
  x,names=None,ax=None,makeviolin=False,cols=None,rastsep=0.3,Nkde=200,
  kdepad=None,kdew=0.8,marker='x'
):
  '''
  Create a boxplot with a raster plot to one side of the data contained in x.
  
  If makeviolin is True then a kernel density estimate will be computed and 
  plotted down one side of the boxplot. If the matplotlib axis ax is not 
  specified, then the current axis   will be used. The names used on the x-axis 
  can be specified in names,   otherwise numbers will be used. A dictionary of 
  colours can be specified in   cols, otherwise a cycle based on the default 
  matplotlib cycle will be used.  rastsep specifies the horizontal seperation 
  between the raster plot and the left side of the boxplot, this can be 
  increased to move the raster points to the left or right. Nkde is used to 
  specify the resolution of the kernel density plot, should a higher resolution 
  is required. kdew specifies what fraction of the distance between the right 
  side of the boxplot and the raster plot should be used for the violin plot. 
  This does nothing if the violin plot is disabled. The default of 0.8 
  correspond to 80% of rastsep, which seems to give reasonable results. The 
  marker used in the scatter plot can be specified via the marker argument.
  The argument x is expected to have entries (Nplots,Nobs)
  '''
  if ax is None:
    ax = gca()
  if names is None:
    names = arange(len(x))
  if cols is None:
    cols = dict([k for k in izip(
      names,
      cycle([u'b', u'g', u'r', u'c', u'm', u'y', u'k'])
  )])
  
  ##############################################################################
  # BOXPLOT
  ##############################################################################
  bp = ax.boxplot(x,showfliers=False)
  bx,cp,fl,mu,md,wh = (
    bp['boxes'],bp['caps'],bp['fliers'],bp['means'],bp['medians'],bp['whiskers']
  )
  ax.set_xticklabels(names)

  # Colour the whiskers and boxes
  for l,n0 in zip(bx,names):
    x0,y0 = l.get_data()
    xr = (x0[1]+x0[0])/2
    xl = x0[0]
    x1 = array([xl,xr,xr,xl,xl])
    l.set_data(x1,y0)
    l.set_color('k')
    ax.add_patch(
      patches.Rectangle(
          (xl,y0[-1]),   # (x,y)
          xr-xl,          # width
          y0[-2]-y0[-1],          # height
          alpha=0.6,
          edgecolor=None,
          facecolor=cols[n0]
      )
    )

  for l in md:
    x0,y0 = l.get_data()
    xr = (x0[1]+x0[0])/2
    xl = x0[0]
    x1 = array([xl,xr])
    l.set_data(x1,y0)
    l.set_color('k')

  for l in cp:
    x0,y0 = l.get_data()
    xr = (x0[1]+x0[0])/2
    xl = x0[0]
    x1 = array([xl,xr])
    l.set_data(x1,y0)
    l.set_color('k')

  for l in wh:
    l.set_color('k')
    l.set_linestyle("-")

  ##############################################################################
  # RASTER PLOT
  ##############################################################################
  for i,(ix,n) in enumerate(zip(x,names)):
    ax.scatter(
      (1+i)*ones_like(ix) + rastsep,ix,
      edgecolor=cols[n],facecolor=cols[n],marker=marker
    )

  ##############################################################################
  # VIOLIN PLOT
  ##############################################################################
  if makeviolin:
    # Estimate limits for the kde
    ymx = None
    ymn = None
    xmx = None
    kdests = list()
    for i,(ix,n) in enumerate(zip(x,names)):
      if ymn is None or ymn>min(ix):
        ymn = min(ix)
      if ymx is None or ymx<max(ix):
        ymx = max(ix)
    if kdepad is None:
      kdepad = (ymx-ymn)*0.3
    yr = linspace(ymn-kdepad,ymx+kdepad,Nkde)
    for i,(ix,n) in enumerate(zip(x,names)):
      kdests.append(gaussian_kde(ix))
      nxmx = kdests[-1](yr).max()
      if xmx is None or nxmx>xmx:
        xmx = nxmx

    # Plot lines and fill between them bsaed on the kernel density estimate
    for i,(ix,n,gkde) in enumerate(zip(x,names,kdests)):
      fill_betweenx(yr,(1+i)*ones_like(yr),(1+i)+((kdew*rastsep)/xmx)*gkde(yr),color=cols[n],zorder=10,alpha=0.15)
      plot(1+i+((kdew*rastsep)/xmx)*gkde(yr),yr,c=cols[n],alpha=0.6,lw=2,zorder=-9)
      plot(1+i*ones_like(yr),yr,c='k',alpha=0.6,lw=2,zorder=-9)

  return(bp)

if __name__=="__main__":
  '''
  Simple example plot if the script is run as __main__
  '''
  from numpy import exp,log
  from matplotlib import figure,show
  x = [linspace(1,5,11),log(linspace(1,exp(5),11)),((1+linspace(-4,4,11))**2)/5]
  names = ["duck","goose","hen"]
  fig = figure()
  ax = fig.add_subplot(111)
  bp = hybridRasterBp(x,names=names,makeviolin=True)
  show()