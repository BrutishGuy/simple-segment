Simple Sequence Segmenting
==========================

This repository contains Python code I wrote for segmenting 1-D time series. In other words,
it can be used for transforming a time series into a piecewise linear represenation. 
The algorithms are Python implementations of the "classical" algorithms, as described in 
[An Online Algorithm for Segmenting Time Series][keogh], including:

- the sliding window algorithm;
- the top-down algorithm; and
- the bottom-up algorithm.

The code is *not* optimized for performance in any way, but I've found it useful for 
experimenting and data exploration.

Requirements
------------

The segmenting algorithms use [NumPy's][numpy] least squares fitting routine, so naturally it depends on [NumPy][numpy].

Example
-------

You can run the code to see example output by running the trend_line.py script. The script
requires [matplotlib][mpl] to display the plots. The script may be run as follows:

	python trend_line.py [-h] [--maxerror E] [--numpoints N] datafile
	
Where --maxerror is the maximum error/tolerance E allowed for the algorithms (default is 4.0), --numpoints N is the number of datapoints 
(default is all datapoints) to use and is useful for large datasets, and datafile is mandatory to specify the location of the file
using your OS's file directory navigation syntax. Finally, the datafile format has 2 columns: Column one is integer time values, 
and Column 2 is the float value of the time-series at a specified time.

A concrete example (on Linux):
	
	python trend_line.py /data/hpc2.dat --maxerror=5.0 --numpoints=1000

The example uses ECG data I found on an [ECG data site][ecg].


[keogh]: http://www.cs.ucr.edu/~eamonn/icdm-01.pdf "Keogh et al. An Online Algorithm for Segmenting Time Series"
[numpy]: http://numpy.scipy.org "NumPy"
[mpl]: http://matplotlib.sourceforge.net "Matplotlib"
[ecg]: http://myweb.msoe.edu/~martynsc/signals/ecg/ecg.html "ECG Data"
