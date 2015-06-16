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


    #do some gradient filtering
    #wanted to do this with masked arrays but I can't get it to work on the 2d data
    
    filtercount = 0    
    
    for p in patchdata:
        if (float(p.split(',')[13]) > 0.4):
            filtercount += 1

    print filtercount
    no_of_lines = len(patchdata) - filtercount
    
    print no_of_lines
        
        
    PatchData = np.zeros((no_of_cols,no_of_lines),dtype='float64')
    
    i = -1 #need this instead of enumerate as we only increment when the slope test passes    
    #this deals with 0 indexing...
    
    for p in patchdata:
        split = p.split(',')
        if (float(p.split(',')[13]) <= 0.4):
            i+=1
            for a in range(no_of_cols):
                PatchData[a][i] = split[a]        
        
    """
    print PatchData[13][1010]
    #print PatchData[13]
    #print len(PatchData)
    
    #Slopes = PatchData[:][13]    
    
    #print np.ma.masked_where(PatchData[:][13] > 0.4, PatchData[:][:])
    
    mask = np.repeat(PatchData[:,13]<0.4,PatchData.shape[1])    

    print mask

    masked_a = np.ma.array(PatchData[13],mask=mask)

    #print masked_a[][1010]
    
    final = np.ma.compress_rowcols(masked_a,1)
    
    #print final    
    
    PatchData = final
    
    #print Slopes
    
    #Slopes2 = np.logical_not(Slopes > 0.4)
    
    #print Slopes2
    
    #print np.delete(PatchData,Slopes2,0)
    
    #np.ma.mask_cols()
    
    #np.ma.compress_rowcols()  #THIS CAN BE USED TO GET RID OF THE ROWS WHICH HAVE MASKED SLOPES IN THEM
    
    #PatchData = PatchData[:][np.logical_not(PatchData[:][13] > 0.4)]

    #print np.logical_not(PatchData[:][13] > 0.4)       
     
    print 'test'
      
    #mask = np.empty(PatchData.shape,dtype=bool)
    #mask[:,:] = (PatchData[:,13] > 0.4)[:,np.newaxis]
    #PatchData = np.ma.MaskedArray(PatchData,mask=mask)
    
    print len(PatchData)
    
    #for i,p in enumerate(PatchData[13]):
    #    if p < 0.4:
    #        print PatchData[1][i]
        
   
    #np.ma.compress_rows(PatchData)
    #np.ma.compress_rowcols()
    """
    
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

def PlotPatches(Sc,PatchData):

    plt.errorbar(E_Star(Sc,PatchData[5],PatchData[1]),R_Star(Sc,PatchData[9],PatchData[1]),
    fmt='ro')    

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
                
        Fit_Sc,_,_,_,_ = optimize.leastsq(Residuals, ScInit, args=(PatchData[9], PatchData[1], PatchData[5]),full_output=True)
       
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
        PlotPatches(Sc,PatchData)
        
        
    Labels()
    
    SavePlot(Path,Prefix,Format)
    

MakeThePlot('C:\\Users\\Stuart\\Desktop\\FR\\er_data\\','CR2_gn_s',0,0,1,Format='png')

#MakeThePlot('','CR2_gn_s',0,0,1,Format='png')

#RawData,PatchData = LoadData('C:\\Users\\Stuart\\Desktop\\FR\\er_data\\','CR2_gn_s')

#print GetBestFitSc('patches', RawData, PatchData)

        