# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:01:05 2015

@author: SWDG

"""
import matplotlib.pyplot as plt


def LoadData(Path,Prefix):
    pass

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
    
    LoadData()
    
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
          
    
