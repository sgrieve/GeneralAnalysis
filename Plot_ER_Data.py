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

    #dimensions will be 17Xlen(patchdata) no_of_cols = 17
    #and the row order will follow the header format in the input file:
    #Final_ID lh_means lh_medians lh_std_devs lh_std_errs cht_means cht_medians cht_std_devs cht_std_errs r_means r_medians r_std_devs r_std_errs s_means s_medians s_std_devs s_std_errs

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
            PatchData[a][i] = split[a]

    # Mask out the rows where the mean slope is > 0.4
    BasinMask = np.empty(BasinData.shape,dtype=bool)
    BasinMask[:,:] = (BasinData[13,:] > 0.4)[np.newaxis,:]
    BasinData = np.ma.MaskedArray(BasinData,mask=BasinMask)

    return RawData,PatchData,BasinData

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

def PlotRaw(Sc,RawData):
    plt.scatter(E_Star(Sc,RawData[3],RawData[2]),R_Star(Sc,RawData[4],RawData[2]),
    marker='.',s=0.5,alpha=0.2,label='Raw Data')

def PlotBins(Sc,RawData,NumBins):
    E_s = E_Star(Sc, RawData[3], RawData[2])
    R_s = R_Star(Sc, RawData[4], RawData[2])

    bin_x, bin_std_x, bin_y, bin_std_y, _ = Bin.bin_data_log10(E_s,R_s,NumBins)

    plt.errorbar(bin_x, bin_y, yerr=bin_std_y, xerr=bin_std_x, fmt='bo',label='Binned Data')

def PlotPatches(Sc,PatchData):
    plt.errorbar(E_Star(Sc,PatchData[5],PatchData[1]),R_Star(Sc,PatchData[9],PatchData[1]),
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

    plt.errorbar(E_Star_avg,R_Star_avg,yerr=R_Star_std,xerr=E_Star_std
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

def Labels():
    plt.legend(loc=4)

def SavePlot(Path,Prefix,Format):
    plt.savefig(Path+Prefix+'E_R_Star.'+Format,dpi=500)

def MakeThePlot(Path,Prefix,Sc_Method,RawFlag,BinFlag,PatchFlag,BasinFlag,LandscapeFlag,Order,Format='png'):

    RawData,PatchData,BasinData = LoadData(Path,Prefix,Order)

    ax = SetUpPlot()

    Sc = GetBestFitSc(Sc_Method, RawData, PatchData)


    DrawCurve()

    if RawFlag:
        PlotRaw(Sc,RawData)
    if BinFlag:
        PlotBins(Sc,RawData,20)
    if PatchFlag:
        PlotPatches(Sc,PatchData)
    if BasinFlag:
        PlotBasins(Sc,BasinData)
    if LandscapeFlag:
        PlotLandscapeAverage(Sc,RawData)

    Labels()

    SavePlot(Path,Prefix,Format)


MakeThePlot('C:\\Users\\Stuart\\Desktop\\FR\\er_data\\','CR2_gn_s','raw',1,1,0,0,0,2,Format='png')

#MakeThePlot('','CR2_gn_s',0,0,1,Format='png')

#RawData,PatchData = LoadData('C:\\Users\\Stuart\\Desktop\\FR\\er_data\\','CR2_gn_s')

#print GetBestFitSc('patches', RawData, PatchData)
