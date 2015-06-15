# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:01:05 2015

@author: SWDG

"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import scipy.optimize as optimize

def LoadData(Path,Prefix):

    #load the data from the raw file  
    #not using genfromtext as I want access to individual elements
    #for debugging, may change in future
    with open(Path+Prefix+'_E_R_Star_Raw_Data.csv','r') as raw:
        no_of_cols = len(raw.readline().split(','))
        rawdata = raw.readlines()

    #want the data in a 2d array to make moving the values about simpler
    #dimensions will be 6Xlen(rawdata) no_of_cols = 6
    #and the row order will follow the header format in the input file:
    #i j LH CHT Relief Slope

    no_of_lines = len(rawdata)
        
    RawData = np.zeros((no_of_cols,no_of_lines),dtype='float64')
    
    for i,r in enumerate(rawdata):
        split = r.split(',')
        for a in range(no_of_cols):    
            RawData[a][i] = split[a]        
    #now we have a transformed 2d array of our raw data
    
    #Next, repeat the process for the patch data
    with open(Path+Prefix+'_E_R_Star_Patch_Data.csv','r') as patch:
        no_of_cols = len(patch.readline().split(','))
        patchdata = patch.readlines()

    #dimensions will be 17Xlen(rawdata) no_of_cols = 17
    #and the row order will follow the header format in the input file:
    #Final_ID lh_means lh_medians lh_std_devs lh_std_errs cht_means cht_medians cht_std_devs cht_std_errs r_means r_medians r_std_devs r_std_errs s_means s_medians s_std_devs s_std_errs

    no_of_lines = len(patchdata)
        
    PatchData = np.zeros((no_of_cols,no_of_lines),dtype='float64')
    
    for i,r in enumerate(patchdata):
        split = r.split(',')
        for a in range(no_of_cols):  
            PatchData[a][i] = split[a]        

    return RawData,PatchData

def SetUpPlot():
    #returning ax for now, may not need to expose it like this.
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 14
    
    ax = plt.gca()    
    
    ax.set_yscale('log')
    ax.set_xscale('log')

    plt.xlabel('Dimensionless Erosion Rate, E*')
    plt.ylabel('Dimensionless Relief, R*')
    
    plt.ylim(0.1,1)
    plt.xlim(0.1,1000)

    return ax    

def PlotRaw(Sc):
    pass

def PlotBins(Sc):
    pass

def PlotPatches(Sc):
    pass


def R_Star_Model(x):
    return (1./x) * (np.sqrt(1.+(x*x)) - np.log(0.5*(1. + np.sqrt(1.+(x*x)))) - 1.)
    
def E_Star(Sc,CHT,LH):
    return (2.*np.fabs(CHT)*LH)/Sc
    
def R_Star(Sc, R, LH):
    return R/(LH*Sc)
    
def Residuals(Sc, R, LH, CHT):
    return R_Star_Model(E_Star(Sc,CHT,LH)) - R_Star(Sc, R, LH)

def DrawCurve():    
    #plot the e* r* curve from roering 2007
    x = np.arange(0.01, 1000, 0.1)        
    plt.plot(x, R_Star_Model(x), 'k-', linewidth=2, label='Nonlinear Flux Law')

"""    
def Calculate_E_R_Star(lh,cht,r,Sc):
    #will need to look at propagating errors
    #this method will be used to get the E*R* values for
    #whatever type of input data we have, either raw, binned or patches
    #and in the case of patches and bins, it will also do somehting with the 
    #std err or std dev values
    #returns 2 numpy arrays of the E* and R* values
    
    E_Star = (2. * np.fabs(cht) * lh) / Sc
    RStar = (r / lh) / Sc
    
    return E_Star, RStar
"""

def GetBestFitSc(Method, RawData, PatchData):

    ScInit = 0.8  # Need to have an initial for the optimizer, any valid Sc value can be used - will not impact the final value    
    Fit_Sc = [] #Need to initialize this in case Method is incorrectly defined. Need some error handling!
    
    if Method.lower() == 'bins':
        pass
    elif Method.lower() == 'raw':
        pass
    elif Method.lower() == 'patches':
        
        print len(PatchData[9])
        
        Fit_Sc,_ = optimize.leastsq(Residuals, ScInit, args=(PatchData[9], PatchData[1], PatchData[5]),full_output=False)
       
    return Fit_Sc[0]    

def Labels():
    plt.legend(loc=4)
    
def SavePlot(Path,Prefix,Format):
    plt.savefig(Path+Prefix+'E_R_Star.'+Format,dpi=500)

def MakeThePlot(Path,Prefix,RawFlag,BinFlag,PatchFlag,Format='png'):
    
    RawData,PatchData = LoadData(Path,Prefix)
    
    ax = SetUpPlot()
    
    Sc = GetBestFitSc('patches', RawData, PatchData)
    
    DrawCurve()
    
    if RawFlag:
        PlotRaw(Sc)
    if BinFlag: 
        PlotBins(Sc)
    if PatchFlag:
        PlotPatches(Sc)
        
        
    Labels()
    
    SavePlot(Path,Prefix,Format)

RawData,PatchData = LoadData('C:\\Users\\Stuart\\Desktop\\FR\\er_data\\','CR2_gn_s')

sc =  GetBestFitSc('patches', RawData, PatchData)

print sc
        