# -*- coding: utf-8 -*-
"""
Script to process results from ShieldingSensitivity.cpp

Very rough and ready at the moment. Still in an exploratory stage with
the data.

Created on Fri Jun 19 13:37:53 2015

@author: s0675405
"""

import glob
import matplotlib.pyplot as plt
import numpy as np

path = 'X:\\shielding\\'

filelist = []
theta = []
phi = []

phi_list = [1, 2, 3, 5, 8, 10, 15, 20, 30, 45, 60, 90]
file_prefix = 'z33_26586_'

for p in phi_list:
    print 'processing phi: ',p
    
    for f in glob.glob(path+file_prefix+'*'+str(p)+'_shield.txt'):
        print f
        filelist.append(f)
        theta.append(int(f.split('_')[2]))
        phi.append(int(f.split('_')[3]))
    
    count = range(len(filelist))  
    
    DataList = []
    Labels = []
    
    for a in zip(filelist,theta,phi,count):
        tmpArray = np.genfromtxt(a[0])
        DataList.append(tmpArray)
        Labels.append('('+str(a[1])+', '+str(a[2])+')')
        
        
    plt.boxplot(DataList)
    
    ax = plt.gca()
    ax.set_xticklabels(Labels,rotation=45)
    
    plt.savefig('Phi_Zenith_'+Labels[0].split(',')[1].strip(')')+'.png')
    plt.clf()
