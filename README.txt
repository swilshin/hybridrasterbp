Hybrid raster boxplot by Simon Wilshin.

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

This work was completed with support from the Royal Veterinary College, 
London (www.rvc.ac.uk).

Feedback or bug reports can be sent to Simon Wilshin via swilshin@rvc.ac.uk

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created by Simon Wilshin
Date 2018/02/23