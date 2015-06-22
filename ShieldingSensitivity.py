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

def hold_phi():

    path = 'C:\\Users\\Stuart\\Desktop\\FR\\cosmo\\'
    
    phi_list = [1, 2, 3, 5, 8, 10, 15, 20, 30, 45, 60, 90]
    #file_prefix = 'z33_26586_'
    file_prefix = 'z33_17218_'
    
    for p in phi_list:
        print 'processing phi: ',p
        
        filelist = []
        theta = []
        phi = []
        
        for f in glob.glob(path+file_prefix+'*_'+str(p)+'_shield.txt'):
            filelist.append(f)
            theta.append(int(f.split('_')[2]))
            phi.append(int(f.split('_')[3]))
        
        count = range(len(filelist))
        
        DataList = []
        Labels = []
        
        #sort the data by theta so it is plotted in the correct order
        sorted_data =  sorted(zip(theta,filelist,phi))
        theta_sorted = [x[0] for x in sorted_data]
        filelist_sorted = [x[1] for x in sorted_data]   
        phi_sorted = [x[2] for x in sorted_data]
     
        
        for a in zip(filelist_sorted,theta_sorted,phi_sorted):
            tmpArray = np.genfromtxt(a[0])
            DataList.append(tmpArray)
            Labels.append('('+str(a[1])+', '+str(a[2])+')')
            
            
        plt.boxplot(DataList)
        plt.title('Phi [Zenith]: '+Labels[0].split(',')[1].strip(')'))
        ax = plt.gca()
        ax.set_xticklabels(Labels,rotation=45)
        plt.ylim((0,1.2))
        plt.tight_layout()
        
        plt.savefig('Phi_Zenith_'+Labels[0].split(',')[1].strip(')')+'.png')
        plt.clf()

def hold_theta():

    path = 'C:\\Users\\Stuart\\Desktop\\FR\\cosmo\\'
    
    theta_list = [1, 2, 3, 5, 8, 10, 15, 20, 30, 45, 60, 90, 180, 360]
    #file_prefix = 'z33_26586_'
    file_prefix = 'z33_17218_'
    
    for t in theta_list:
        print 'processing theta: ',t
        
        filelist = []
        theta = []
        phi = []
        
        for f in glob.glob(path+file_prefix+str(t)+'_*_shield.txt'):
            filelist.append(f)
            theta.append(int(f.split('_')[2]))
            phi.append(int(f.split('_')[3]))
        
        count = range(len(filelist))
        
        DataList = []
        Labels = []
        
        #sort the data by theta so it is plotted in the correct order
        sorted_data =  sorted(zip(phi,theta,filelist))
        theta_sorted = [x[1] for x in sorted_data]
        filelist_sorted = [x[2] for x in sorted_data]   
        phi_sorted = [x[0] for x in sorted_data]
     
        
        for a in zip(filelist_sorted,theta_sorted,phi_sorted):
            tmpArray = np.genfromtxt(a[0])
            DataList.append(tmpArray)
            Labels.append('('+str(a[1])+', '+str(a[2])+')')
            
            
        plt.boxplot(DataList)
        plt.title('Theta [Azimuth]: '+Labels[1].split(',')[0].strip('('))
        ax = plt.gca()
        ax.set_xticklabels(Labels,rotation=45)
        plt.ylim((0,1.2))
        plt.tight_layout()
        
        plt.savefig('Theta_Azimuth_'+Labels[1].split(',')[0].strip('(')+'.png')
        plt.clf()
        
def ks_testing():
    
    from scipy import stats
    
    path = 'C:\\Users\\Stuart\\Desktop\\FR\\cosmo\\'
    
    
    #file_prefix = 'z33_26586_'
    file_prefix = 'z33_17218_'
    

    OneOne = np.genfromtxt(path+file_prefix+'1_1_shield.txt')

    filelist = []
    theta = []
    phi = []
    
    for f in glob.glob(path+file_prefix+'*.txt'):
        filelist.append(f)
        theta.append(int(f.split('_')[2]))
        phi.append(int(f.split('_')[3]))
        
                
        
    #sort the data by theta so it is plotted in the correct order
    sorted_data =  sorted(zip(phi,theta,filelist))
    theta_sorted = [x[1] for x in sorted_data]
    filelist_sorted = [x[2] for x in sorted_data]   
    phi_sorted = [x[0] for x in sorted_data]
 
    
    for a in zip(filelist_sorted,theta_sorted,phi_sorted):
        tmpArray = np.genfromtxt(a[0])
        ks,p = stats.chisquare(tmpArray,OneOne)
        print '('+str(a[1])+', '+str(a[2])+')',ks,p
        
        
        
ks_testing()            
            