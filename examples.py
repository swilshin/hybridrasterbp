'''
Examples of hybrid raster boxplots.

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

from hybridrasterbp import hybridRasterBp

from numpy import linspace,exp,log
from matplotlib.pyplot import figure,show

# Generate some examlpe data
x = [linspace(1,5,11),log(linspace(1,exp(5),11)),((1+linspace(-4,4,11))**2)/5]
names = ["duck","goose","hen"]
cols = {"duck":'b', "goose":'m', "hen":'r'}

# Plot with a violin plot
fig = figure()
ax = fig.add_subplot(111)
hybridRasterBp(x,names=names,makeviolin=True,cols=cols)

# Generate some examlpe data
y = [
  linspace(1,5,11),
  log(linspace(1,exp(5),11)),
  ((1+linspace(-4,4,11))**2)/5,
  exp(linspace(1,log(5),11))
]
labels = ["left","right","top","bottom"]
directioncols = {"left":'b', "right":'r', "top":'m', "bottom":'c'}

# Plot without a violin plot
fig = figure()
ax = fig.add_subplot(111)
bp = hybridRasterBp(y,names=labels,makeviolin=False,cols=directioncols)

show()