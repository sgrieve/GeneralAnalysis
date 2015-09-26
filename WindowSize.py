# -*- coding: utf-8 -*-
"""
Simple script to plot results from PolyFitWindowSize.cpp to assist in the selection of 
a correct window size for the polyfit routine.

Created on Wed Feb 19 12:52:53 2014

@author: SWDG

"""
import matplotlib.pyplot as plt
import sys
from matplotlib import rcParams

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 16

def MakePlot(Path, Filename):
                                
    with open(Path+Filename, "r") as f:
        f.readline()
        data = f.readlines()
     
    #file format is as follows:       
    #Length_scale Curv_mean Curv_stddev Curv_iqr    
    
    std_dev_curv = []
    window_size = []
    curv = []
    iqr_curv = []
        
    #load data into lists    
    for d in data:
        window_size.append(float(d.split()[0]))
        curv.append(float(d.split()[1]))    
        std_dev_curv.append(float(d.split()[2]))
        iqr_curv.append(float(d.split()[3]))
    
    plt.suptitle('Window size and curvature', fontsize=18)
    
    plt.subplot(3,1,1)    
    plt.plot(window_size,iqr_curv,'k^')
    plt.ylabel('IQR of Curvature (1/m)')
    
    plt.subplot(3,1,2)
    plt.plot(window_size,curv,'k^')
    plt.ylabel('Mean Hilltop\n Curvature (1/m)')
    
    plt.subplot(3,1,3)
    plt.plot(window_size,std_dev_curv,'k^')
    plt.xlabel('Length Scale (m)')
    plt.ylabel('Std Dev of Hilltop\n Curvature (1/m)')
    
    print '\nWriting plots to file: ' + Path+'WindowSizeFig.png'
    plt.savefig(Path+'WindowSizeFig.png')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Incorrect number of arguments, please enter a path and filename.\ne.g. /home/data/ Oregon_Window_Size_Data.txt')
    
    MakePlot(sys.argv[1], sys.argv[2])
    
