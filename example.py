from pandas import DataFrame, read_csv 

import pandas as pd # import pandas using given abbreviation


from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D
import segment
import fit
import numpy as np
import data_loader


def draw_plot(data,plot_title):
    plot(range(len(data)),data,'ro',alpha=0.8)
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

Location = 'household_power_consumption\household_power_consumption_small.csv'
df = pd.read_csv(Location, sep=';', header=0)
data = list(map(float, df.Voltage.as_matrix()))[:100000]

max_error = 4.0
'''
#sliding window with regression
figure()
segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Sliding window with regression")
draw_segments(segments)

#bottom-up with regression
figure()
segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with regression")
draw_segments(segments)

#top-down with regression
figure()
segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with regression")
draw_segments(segments)
'''


#sliding window with simple interpolation
figure()
segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)

# calculate trend data as a pair (l, s) where l is the length, and 
# s is the slope represented as angle theta ranging from -90 to 90 degrees

'''f = open('trend_data.csv','w')
f.write('segment_no,length,slope\n') # column headings
i = 1 # segment counter
for segment in segments:
    x0, y0, x1, y1 = segment # unpack the segment line as initial x and y, and final x and y values
    theta = np.rad2deg(np.arctan((y1 - y0)/(x1 - x0))) # calculate arctan of the slope (via finite difference) and convert from radians to degrees
    l = np.sqrt((x1 - x0)**2 + (y1 - y0)**2) # calculate length using euclidean distance 
    f.write('%d,%.3f,%.3f\n'%(i,l,theta)) # write to file csv formatted
    i += 1
f.close()'''
    
draw_plot(data,"Sliding window with simple interpolation") # call wrapper to pyplot, plot with given headings
draw_segments(segments) # draw the segments using the pyplot wrapper
'''
#bottom-up with  simple interpolation
figure()
segments = segment.bottomupsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with simple interpolation")
draw_segments(segments)

#top-down with  simple interpolation
figure()
segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with simple interpolation")
draw_segments(segments)
'''

show()

