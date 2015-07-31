# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:01:05 2015

@author: SWDG

"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import scipy.optimize as optimize
import bin_data as Bin
from scipy.stats import gaussian_kde

def LoadData(Path,Prefix,Order):

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

    # Mask out the rows where the mean slope is > 0.4
    RawMask = np.empty(RawData.shape,dtype=bool)
    RawMask[:,:] = (RawData[5,:] > 0.4)[np.newaxis,:]
    RawData = np.ma.MaskedArray(RawData,mask=RawMask)

    #Next, repeat the process for the patch data
    with open(Path+Prefix+'_E_R_Star_Patch_Data.csv','r') as patch:
        no_of_cols = len(patch.readline().split(','))
        patchdata = patch.readlines()

    #dimensions will be 18Xlen(patchdata) no_of_cols = 18
    #and the row order will follow the header format in the input file:
    #Final_ID lh_means lh_medians lh_std_devs lh_std_errs cht_means cht_medians cht_std_devs cht_std_errs r_means r_medians r_std_devs r_std_errs s_means s_medians s_std_devs s_std_errs patch_size

    no_of_lines = len(patchdata)

    PatchData = np.zeros((no_of_cols,no_of_lines),dtype='float64')

    for i,p in enumerate(patchdata):
        split = p.split(',')
        for a in range(no_of_cols):
            PatchData[a][i] = split[a]

    # Mask out the rows where the mean slope is > 0.4
    PatchMask = np.empty(PatchData.shape,dtype=bool)
    PatchMask[:,:] = (PatchData[13,:] > 0.4)[np.newaxis,:]
    PatchData = np.ma.MaskedArray(PatchData,mask=PatchMask)

    #Next, repeat the process for the Basin data
    with open(Path+Prefix+'_E_R_Star_Basin_'+str(Order)+'_Data.csv','r') as basin:
        no_of_cols = len(basin.readline().split(','))
        basindata = basin.readlines()

    #dimensions will be 7Xlen(basindata) no_of_cols = 7
    #and the row order will follow the header format in the input file:
    #Basin_ID LH CHT Relief Slope Area Count

    no_of_lines = len(basindata)

    BasinData = np.zeros((no_of_cols,no_of_lines),dtype='float64')

    for i,d in enumerate(basindata):
        split = d.split(',')
        for a in range(no_of_cols):
            BasinData[a][i] = split[a]

    # Mask out the rows where the mean slope is > 0.4
    BasinMask = np.empty(BasinData.shape,dtype=bool)
    BasinMask[:,:] = (BasinData[4,:] > 0.4)[np.newaxis,:]
    BasinData = np.ma.MaskedArray(BasinData,mask=BasinMask)
    
    # Mask out the rows where there are too few data points
    BasinMask = np.empty(BasinData.shape,dtype=bool)
    BasinMask[:,:] = (BasinData[6,:] < 100)[np.newaxis,:]
    BasinData = np.ma.MaskedArray(BasinData,mask=BasinMask)
        
    return RawData,PatchData,BasinData

def SetUpPlot():
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 14

    ax = plt.gca()

    ax.set_yscale('log', nonposy='clip')
    ax.set_xscale('log', nonposx='clip')

    plt.xlabel('Dimensionless Erosion Rate, E*')
    plt.ylabel('Dimensionless Relief, R*')

    plt.ylim(0.05,1.1)
    plt.xlim(0.1,1000)

def PlotRaw(Sc,RawData):
    plt.scatter(E_Star(Sc,RawData[3],RawData[2]),R_Star(Sc,RawData[4],RawData[2]),
    marker='.',alpha=0.2,label='Raw Data')
    
def PlotRawDensity(Sc,RawData,Thin):
    #http://stackoverflow.com/a/20107592/1627162
    x = E_Star(Sc,RawData[3],RawData[2])
    y = R_Star(Sc,RawData[4],RawData[2])
    
    if Thin:
        x = x[::Thin]
        y = y[::Thin]  
    
    xy = np.vstack([x,y])
    density = gaussian_kde(xy)(xy)

    #order the points by density so highest density is on top in the plot    
    idx = density.argsort()
    x, y, density = x[idx], y[idx], density[idx]
    
    plt.scatter(x,y,c=density,edgecolor='',cmap=plt.get_cmap("autumn_r"))
    cbar = plt.colorbar()
    cbar.set_label('Probability Distribution Function')

def PlotBins(Sc,RawData,NumBins,MinimumBinSize=100):
    E_s = E_Star(Sc, RawData[3], RawData[2])
    R_s = R_Star(Sc, RawData[4], RawData[2])

    bin_x, bin_std_x, bin_y, bin_std_y, count = Bin.bin_data_log10(E_s,R_s,NumBins)

    #filter bins based on the number of data points used in their calculation
    bin_x = np.ma.masked_where(count<MinimumBinSize, bin_x)
    bin_y = np.ma.masked_where(count<MinimumBinSize, bin_y)
    #these lines produce a meaningless warning - don't know how to solve it yet.

    #only plot errorbars for y as std dev of x is just the bin width == meaningless
    plt.errorbar(bin_x, bin_y, yerr=bin_std_y, fmt='bo',label='Binned Data')
    
def PlotPatches(Sc,PatchData):
                  
    plt.errorbar(E_Star(Sc,PatchData[6],PatchData[2]),R_Star(Sc,PatchData[10],PatchData[2]),
    fmt='ro',label='Hilltop Patch Data')

def PlotBasins(Sc,BasinData):
    plt.errorbar(E_Star(Sc,BasinData[2],BasinData[1]),R_Star(Sc,BasinData[3],BasinData[1]),
    fmt='go',label='Basin Data')

def PlotLandscapeAverage(Sc,RawData):
    E_Star_temp = E_Star(Sc,RawData[3],RawData[2])
    R_Star_temp = R_Star(Sc,RawData[4],RawData[2])
    E_Star_avg = np.mean(E_Star_temp)
    R_Star_avg = np.mean(R_Star_temp)
    E_Star_std = np.std(E_Star_temp)
    R_Star_std = np.std(R_Star_temp)

    plt.errorbar(E_Star_avg,R_Star_avg,yerr=R_Star_std,xerr=E_Star_std,
    fmt='ko',label='Landscape Average')

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
        
def GetBestFitSc(Method, RawData, PatchData, BasinData):

    ScInit = 0.8  # Need to have an initial for the optimizer, any valid Sc value can be used - will not impact the final value
    Fit_Sc = [] #Need to initialize this in case Method is incorrectly defined. Need some error handling!

    if Method.lower() == 'raw':
        Fit_Sc,_,_,_,_ = optimize.leastsq(Residuals, ScInit, args=(RawData[4], RawData[2], RawData[3]),full_output=True)
                
    elif Method.lower() == 'patches':
        Fit_Sc,_,_,_,_ = optimize.leastsq(Residuals, ScInit, args=(PatchData[9], PatchData[1], PatchData[5]),full_output=True)

    elif Method.lower() == 'basins':
        Fit_Sc,_,_,_,_ = optimize.leastsq(Residuals, ScInit, args=(BasinData[3], BasinData[1], BasinData[2]),full_output=True)

    return Fit_Sc[0]

def Labels(Sc,Method,ForceSc):
    plt.legend(loc=4)

    #in case Method is invalid
    fit_description = ' = '

    if Method.lower() == 'raw':
        fit_description = ' from raw data = '

    elif Method.lower() == 'patches':
        fit_description = ' from hilltop patches = '

    elif Method.lower() == 'basins':
        fit_description = ' from basin average data = '

    if ForceSc:
        plt.title('$\mathregular{S_c}$ forced as = ' + str(round(Sc,2)))
    else:
        plt.title('Best fit $\mathregular{S_c}$'+fit_description+str(round(Sc,2)))

def SavePlot(Path,Prefix,Format):
    plt.savefig(Path+Prefix+'_E_R_Star.'+Format,dpi=500)

def GMRoering():
    #plots the gm datapoints from roering 2007 for testing
    x = [1.68]*2
    y = [0.34,0.43]
    
    xerr = [0.7]*2
    yerr = [0.17,0.2]
    
    #make better labels by double plotting
    plt.plot(x,y,'k^',label='Roering et al. 2007')
    plt.errorbar(x,y,yerr,xerr,'k^')
    
def OCRRoering():
    #plots the gm datapoints from roering 2007 for testing
    x = [6.3]*2
    y = [0.57,0.64]
    
    xerr = [2.1]*2
    yerr = [0.23,0.18]
    
    #make better labels by double plotting
    plt.plot(x,y,'k^',label='Roering et al. 2007')
    plt.errorbar(x,y,yerr,xerr,'k^')
    
def MakeThePlot(Path,Prefix,Sc_Method,RawFlag,DensityFlag,BinFlag,PatchFlag,BasinFlag,LandscapeFlag,Order,ForceSc=False,Format='png'):

    RawData,PatchData,BasinData = LoadData(Path,Prefix,Order)

    SetUpPlot()
    
    if ForceSc:
        Sc = ForceSc
    else:
        Sc = GetBestFitSc(Sc_Method, RawData, PatchData, BasinData)

    DrawCurve()

    if RawFlag:
        PlotRaw(Sc,RawData)
    if DensityFlag:
        PlotRawDensity(Sc,RawData,DensityFlag)
    if BinFlag:
        PlotBins(Sc,RawData,BinFlag)
    if PatchFlag:
        PlotPatches(Sc,PatchData)
    if BasinFlag:
        PlotBasins(Sc,BasinData)
    if LandscapeFlag:
        PlotLandscapeAverage(Sc,RawData)

    OCRRoering()
    GMRoering()
    
    Labels(Sc,Sc_Method,ForceSc)
    #plt.show()

    SavePlot(Path,Prefix+'_'+Sc_Method,Format)
    plt.clf()


#for a in ['OR','NC','CR','GM']:
#    for b in ['raw','patches','basins']:
#        MakeThePlot('C:\\Users\\Stuart\\Dropbox\\data\\final\\',a,b,0,0,0,1,1,0,2,ForceSc=False,Format='png')

MakeThePlot('C:\\Users\\Stuart\\Dropbox\\data\\final\\','OR','basins',0,0,0,1,1,0,2,ForceSc=False,Format='png')

