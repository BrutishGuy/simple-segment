import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import sys

import segment
import fit
import numpy as np
import argparse

def draw_plot(data, plot_title):
    plt.plot(range(len(data)),data,'ro',alpha=0.8)
    plt.title(plot_title)
    plt.xlabel("Samples")
    plt.ylabel("Signal")
    plt.xlim((0,len(data)-1))

def draw_segments(segments):
    ax = plt.gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def main():
    parser = argparse.ArgumentParser(description='Calculate trend-lines for time-series data, using sliding window, top-down and bottom-up approaches')
    parser.add_argument('datafile', type=str, help='The data to use for calculcation')    
    parser.add_argument('--maxerror', metavar='E',type=float, default=4.0, help='Maximum error/tolernce allowed by techniques') 
    parser.add_argument('--numpoints', metavar='N',type=int, default=0, help='Specify first N points to use') 
    
    args = parser.parse_args()
    
    data_location = args.datafile
    maxerror = args.maxerror
    
    df = pd.read_csv(data_location, sep=',', header=0)
    data = list(map(float, df.iloc[:,1].as_matrix()))
    
    numpoints = args.numpoints
    
    if numpoints == 0:
        numpoints = len(df.icol(1))
    
    data = data[:numpoints]
     
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
    plt.figure(1)
    segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, maxerror)
    
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
        
    draw_plot(data, "Sliding window with simple interpolation") # call wrapper to pyplot, plot with given headings
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
    
    plt.show()

if __name__ == "__main__":
    main()
