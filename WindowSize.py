# -*- coding: utf-8 -*-
"""
Simple script to plot results from PolyFitWindowSize.cpp to assist in the selection of 
a correct window size for the polyfit routine.

Created on Wed Feb 19 12:52:53 2014

@author: SWDG

#plt.xscale('log')
#plt.yscale('log')

#plt.xlim((0,155))
#plt.ylim((0.005,0.1))
#plt.axvspan(2,7.5, alpha=0.5, color='k', linewidth=0)

"""

import matplotlib.pyplot as plt
from matplotlib import rcParams


# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 16

#input filename and path here and output path
path = ''
filename = 'GM_DEM_Window_Size_Data.txt'
outpath = path
                        
with open(path+filename, "r") as f:
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

plt.show()
#plt.savefig(outpath+'WindowSizeFig.png')
