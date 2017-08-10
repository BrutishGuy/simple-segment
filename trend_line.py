import pandas as pd

import sys

import trendhelpers.segment as segment
import trendhelpers.fit as fit
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

def process(args):
    """This is a simple sliding window function, that takes in args of the 
    form [<data array>, <window size>], and it outputs a numpy array of the
    data in windowed format, with the first element being the array of the
    first <window size> elements of <data array>.
    >>> process([[1,2,3,4,5], 2])
    ...array([[1,2], [2,3], [3,4], [4,5]])
    """
    data = args[0]
    maxerror = args[1]
    numpoints = args.numpoints = args[4]
    method = args[2]
    interpolation_method = args[3]   
    
    if numpoints == 0:
        numpoints = len(df.icol(1))
    
    if interpolation_method == 'simple':
        interp = fit.interpolate
        interpolation_method  = 'simple interpolation'
    else:
        interp = fit.regression
        interpolation_method  = 'regression'
    
    if method == 'slidingwindow':
        func = segment.slidingwindowsegment
    elif method == 'topdown':
        func = segment.topdownsegment_iterative
    else:
        func = segment.bottomupsegment
    
    data = data[:numpoints]
    
    line_segments = func(data, interp, fit.sumsquared_error, maxerror)  
    
    out = []
    
    # calculate trend data as a pair (l, s) where l is the length, and 
    # s is the slope represented as angle theta ranging from -90 to 90 degrees    
    for line_segment in line_segments:
        x0, y0, x1, y1 = line_segment # unpack the segment line as initial x and y, and final x and y values
        theta = np.rad2deg(np.arctan((y1 - y0)/(x1 - x0))) # calculate arctan of the slope (via finite difference) and convert from radians to degrees
        l = x1 - x0 # calculate length using euclidean distance
        out.append([l, theta])
    
    return out

def main():
    parser = argparse.ArgumentParser(description='Calculate trend-lines for time-series data, using sliding window, top-down and bottom-up approaches')
    parser.add_argument('datafile', type=str, help='The data to use for calculcation')    
    parser.add_argument('--maxerror', metavar='E',type=float, default=4.0, help='Maximum error/tolernce allowed by techniques. Default is 4.0') 
    parser.add_argument('--numpoints', metavar='N',type=int, default=0, help='Specify first N points to use. Default is all points in dataset') 
    parser.add_argument('--method', metavar='M',type=str,default='slidingwindow',help='Specify technique to calculate trends: Options are slidingwindow, topdown, bottomup. Default is sliding window')
    parser.add_argument('--interpolation_method', metavar='I',type=str,default='simple',help='Technique to calculate the segment line fit. Choices are simple (for simple interpolation) or leastsq (for a least squares fit). Default is simple interpolation')
    parser.add_argument('--write_trends', metavar='W',type=bool, default=False, help='Write trend data (length, slope) to file, trend_data.csv. Default is False. Set to True or False') 
    
    args = parser.parse_args()
    
    data_location = args.datafile
    maxerror = args.maxerror
    write_trends = args.write_trends
    method = args.method
    interpolation_method = args.interpolation_method
    
    df = pd.read_csv(data_location, sep=',', header=0)
    data = list(map(float, df.iloc[:,1].as_matrix()))
    
    numpoints = args.numpoints
    
    if numpoints == 0:
        numpoints = len(df.icol(1))
    
    if interpolation_method == 'simple':
        interp = fit.interpolate
        interpolation_method  = 'simple interpolation'
    else:
        interp = fit.regression
        interpolation_method  = 'regression'
    
    if method == 'slidingwindow':
        func = segment.slidingwindowsegment
    elif method == 'topdown':
        func = segment.topdownsegment_iterative
    else:
        func = segment.bottomupsegment
    
    data = data[:numpoints]
    
    
    #sliding window with simple interpolation
    plt.figure(1)
    line_segments = func(data, interp, fit.sumsquared_error, maxerror)
    
    # calculate trend data as a pair (l, s) where l is the length, and 
    # s is the slope represented as angle theta ranging from -90 to 90 degrees
    
    if write_trends:
        f = open('trend_data.csv','w')
        f.write('segment_no,length,slope\n') # column headings
        i = 1 # segment counter
        for line_segment in line_segments:
            x0, y0, x1, y1 = line_segment # unpack the segment line as initial x and y, and final x and y values
            theta = np.rad2deg(np.arctan((y1 - y0)/(x1 - x0))) # calculate arctan of the slope (via finite difference) and convert from radians to degrees
            l = x1 - x0 # calculate length using euclidean distance 
            f.write('%d,%.3f,%.3f\n'%(i,l,theta)) # write to file csv formatted
            i += 1
        f.close()
        
    draw_plot(data, method + " with " + interpolation_method) # call wrapper to pyplot, plot with given headings
    draw_segments(line_segments) # draw the segments using the pyplot wrapper
    
    plt.show()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D    
    main()
