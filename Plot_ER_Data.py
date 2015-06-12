# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:01:05 2015

@author: SWDG

"""
import matplotlib.pyplot as plt
import numpy as np

def LoadData(Path,Prefix):

    #load the data from the raw file  
    #not using genfromtext as I want access to individual elements
    #for debugging, may change in future
    with open(Path+Prefix+'_E_R_Star_Raw_Data.csv','r') as raw:
        no_of_cols = len(raw.readline().split())
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
        no_of_cols = len(patch.readline().split())
        patchdata = patch.readlines()

    #dimensions will be 17Xlen(rawdata) no_of_cols = 17
    #and the row order will follow the header format in the input file:
    #Final_ID lh_means lh_medians lh_std_devs lh_std_errs cht_means cht_medians cht_std_devs cht_std_errs r_means r_medians r_std_devs r_std_errs s_means s_medians s_std_devs s_std_errs

    no_of_lines = len(patchdata)
        
    PatchData = np.zeros((no_of_cols,no_of_lines),dtype='float64')
    
    for i,r in enumerate(rawdata):
        split = r.split(',')
        for a in range(no_of_cols):    
            PatchData[a][i] = split[a]        

    return RawData,PatchData

def SetUpPlot():
    pass

def PlotRaw(Sc):
    pass

def PlotBins(Sc):
    pass

def PlotPatches(Sc):
    pass

def DrawCurve():
    pass

def Calculate_E_R_Star(lh,cht,r,Sc):
    #will need to look at propagating errors
    #this method will be used to get the E*R* values for
    #whatever type of input data we have, either raw, binned or patches
    #and in the case of patches and bins, it will also do somehting with the 
    #std err or std dev values
    E_Star,RStar = []
    return E_Star,RStar

def GetBestFitSc(method):

    if method.lower() is 'bins':
        pass
    elif method.lower() is 'raw':
        pass
    if method.lower() is 'patches':
        pass
    
    Sc = 0.8    
    return Sc

def Labels():
    pass

def SavePlot(Path,Prefix,Format):
    plt.savefig(Path+Prefix+'E_R_Star.'+Format,dpi=500)

def MakeThePlot(Path,Prefix,RawFlag,BinFlag,PatchFlag,Format='png'):
    
    RawData,PatchData = LoadData(Path,Prefix)
    
    SetUpPlot()
    
    Sc = GetBestFitSc('patches')
    
    DrawCurve()
    
    if RawFlag:
        PlotRaw(Sc)
    if BinFlag: 
        PlotBins(Sc)
    if PatchFlag:
        PlotPatches(Sc)
        
        
    Labels()
    
    SavePlot(Path,Prefix,Format)
          
    
