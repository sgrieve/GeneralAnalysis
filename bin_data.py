"""
Functions to bin a dataset with bins spaced regularly (in linear
or logarithmic space) in the x-data category.

Martin Hurst, 2011

August 2012: Functions added for generating frequency distributions

"""

# Import Modules
import numpy as np
from scipy.stats import sem

##Binit
def bin_data(datax,datay,numbins,botedge=-99,topedge=-99):

    """
    Place data in bins spaced regularly in linear space.
    Calculates binned averages and standard deviations for
    both the abscissa and ordinate data.

    Returns arrays containing binned averages and standard
    deviations of both x and y data as well as the number
    of samples in each bin:
        binmeanx, binstdx, binmeany, binstdy, binmembercount

    Martin Hurst, 2011
    
    """
    if botedge == -99:
        botedge = np.min(datax)
    if topedge == -99:
        topedge = np.max(datax)
        
    bin_space = (topedge-botedge)/numbins
    binedges = np.arange(botedge,topedge+bin_space,bin_space)
    whichbin = np.ndarray( (len(datax)) )
    
    for i in range(0,numbins):
        for j in range (0,len(datax)):
            if (datax[j] > binedges[i] and datax[j] <= binedges[i+1]):
                whichbin[j] = i
            elif (datax[j] >= topedge): whichbin[j] = -99
            
    #print binedges[0], binedges[1]
     
    binmeandatax = np.zeros(numbins)
    binstddatax = np.zeros(numbins)
    binmeandatay = np.zeros(numbins)
    binstddatay = np.zeros(numbins)
    binmindatay = np.zeros(numbins)
    binmaxdatay = np.zeros(numbins)
    binmembercount = np.zeros(numbins)
    #print whichbin
    
    for i in range (0,numbins):
        flagbinmembers = (whichbin == i)
        binmemberdatax = datax[flagbinmembers]
        binmembercount[i] = len(binmemberdatax)
        if binmembercount[i] >0:
            binmeandatax[i] = np.mean(binmemberdatax)
            binstddatax[i] = np.std(binmemberdatax)            
        else:
            binmeandatax[i] = np.nan
            binstddatax[i] = np.nan
        
        binmemberdatay = datay[flagbinmembers]
        if binmembercount[i] >0:
            binmeandatay[i] = np.mean(binmemberdatay)
            binstddatay[i] = np.std(binmemberdatay)
            binmindatay[i] = np.min(binmemberdatay)
            binmaxdatay[i] = np.max(binmemberdatay)
        else:
            binmeandatay[i] = np.nan
            binstddatay[i] = np.nan
            binmindatay[i] = np.nan
            binmaxdatay[i] = np.nan

    return binmeandatax, binstddatax, binmeandatay, binstddatay, binmindatay, binmaxdatay, binmembercount


def bin_data_log10(datax,datay,numbins,botedge=-99,topedge=-99):

    """
    Place data in bins spaced regularly in log10 space.
    Calculates binned averages and standard deviations for
    both the abscissa and ordinate data.

    Returns arrays containing binned averages and standard
    deviations of both x and y data as well as the number
    of samples in each bin:
        binmeanx, binstdx, binmeany, binstdy, binmembercount

    Martin Hurst, 2011
    
    """
    tempx = np.log10(datax)
    
    if botedge == -99:
        botedge = np.min(tempx)
    else:
        botedge = np.log10(botedge)
    if topedge == -99:
        topedge = np.max(tempx)
    else:
        topedge = np.log10(topedge)
        
    bin_space = (topedge-botedge)/numbins
    
    binedges = np.arange(botedge,topedge+bin_space,bin_space) #left edges
    
    #whichbin = np.ndarray( (len(tempx)) ) #array of size == to xdata - a placeholder to store each value's bin location    
    #whichbin is initialized as zeros, so when the algorithm finds a masked value, it is rightly skipped
    #but in skipping it the value is left as 0. so later on our member count for the first bin contains all of the
    #masked values. Cant use empty as we wont know what garbage memory will be there, could == one of our bins, so need to use 
    #array_like to give a placeholder value > than the no of bins
    #I think this will need refactored.
    
    whichbin = np.empty(len(tempx))
    whichbin.fill(numbins+1) #fill array with this value
    
    for i in range(0,numbins):
        for j in range (0,len(tempx)):
            if (tempx[j] > binedges[i] and tempx[j] <= binedges[i+1]):
                
                whichbin[j] = i
            elif (tempx[j] >= topedge): 
                whichbin[j] = -99
                            
    binmeandatax = np.zeros(numbins)
    binstddatax = np.zeros(numbins)
    binmembercount = np.zeros(numbins)
    binmeandatay = np.zeros(numbins)
    binstddatay = np.zeros(numbins)
    
    binstderrx = np.zeros(numbins)
    binstderry = np.zeros(numbins)
   
    for i in range (0,numbins):
        flagbinmembers = (whichbin == i)
        binmemberdatax = tempx[flagbinmembers]
        binmembercount[i] = len(binmemberdatax)
        if binmembercount[i] >2:
            binmeandatax[i] = np.mean(binmemberdatax)
            binstddatax[i] = np.std(binmemberdatax)
            binstderrx[i] = sem(binmemberdatax)
        else:
            binmeandatax[i] = np.nan
            binstddatax[i] = np.nan
            binstderry[i] = np.nan
        
        binmemberdatay = datay[flagbinmembers]
        if binmembercount[i] >2:
            binmeandatay[i] = np.mean(binmemberdatay)
            binstddatay[i] = np.std(binmemberdatay)
            binstderry[i] = sem(binmemberdatay)
        else:
            binmeandatay[i] = np.nan
            binstddatay[i] = np.nan
            binstderry[i] = np.nan

    return 10**binmeandatax, 10**binstddatax, binmeandatay, binstddatay, binstderrx, binstderry, binmembercount

def bin_frequency_data(datax,numbins,botedge=-99,topedge=-99):

    """
    Place data in bins spaced regularly in linear space.
    Calculates binned averages and standard deviations for
    the abscissa and gets frequency data for the ordinate.

    Returns arrays containing binned averages and standard
    deviations of x and frequency data for each bin:
        binmeanx, binstdx, binfreq 

    Martin Hurst, Added August 2012
    
    """
    
    if botedge == -99:
        botedge = np.min(datax)
    if topedge == -99:
        topedge = np.max(datax)
        
    bin_space = (topedge-botedge)/numbins
    binedges = np.arange(botedge,topedge+bin_space,bin_space)
    whichbin = np.ndarray( (len(datax)) )
    
    for i in range(0,numbins):
        for j in range (0,len(datax)):
            if (datax[j] > binedges[i] and datax[j] <= binedges[i+1]):
                whichbin[j] = i
            elif (datax[j] >= topedge): whichbin[j] = -99
            
    binmeandatax = np.zeros(numbins)
    binstddatax = np.zeros(numbins)
    binmembercount = np.zeros(numbins)
       
    for i in range (0,numbins):
        flagbinmembers = (whichbin == i)
        binmemberdatax = datax[flagbinmembers]
        binmembercount[i] = len(binmemberdatax)
        if binmembercount[i] >0:
            binmeandatax[i] = np.mean(binmemberdatax)
            binstddatax[i] = np.std(binmemberdatax)
        else:
            #print "YAY!"
            binmeandatax[i] = (binedges[i+1]+binedges[i])/2.0
            binstddatax[i] = np.nan
        
    return binmeandatax, binstddatax, binmembercount

def bin_frequency_data_log10(datax,numbins,botedge=-99,topedge=-99):

    """
    Place data in bins spaced regularly in log10 space.
    Calculates binned averages and standard deviations for
    the abscissa and gets frequency data for the ordinate.

    Returns arrays containing binned averages and standard
    deviations of x and frequency data for each bin:
        binmeanx, binstdx, binfreq 

    Martin Hurst, Added August 2012
    
    """
    
    tempx = np.log10(datax)
        
    if botedge == -99:
        botedge = np.min(tempx)
    else:
        botedge = np.log10(botedge)
    if topedge == -99:
        topedge = np.max(tempx)
    else:
        topedge = np.log10(topedge)
        
    bin_space = (topedge-botedge)/numbins
   
    binedges = np.arange(botedge,topedge+bin_space,bin_space)
    whichbin = np.ndarray( (len(tempx)) )

    for i in range(0,numbins):
        for j in range (0,len(tempx)):
            if (tempx[j] > binedges[i] and tempx[j] <= binedges[i+1]):
                whichbin[j] = i
            elif (tempx[j] >= topedge): whichbin[j] = -99
      
    binmeandatax = np.zeros(numbins)
    binstddatax = np.zeros(numbins)
    binmembercount = np.zeros(numbins)
    
    for i in range (0,numbins):
        flagbinmembers = (whichbin == i)
        binmemberdatax = tempx[flagbinmembers]
        binmembercount[i] = len(binmemberdatax)
        if binmembercount[i] >0:
            binmeandatax[i] = np.mean(binmemberdatax)
            binstddatax[i] = np.std(binmemberdatax)
        else:
            binmeandatax[i] = np.nan
            binstddatax[i] = np.nan

    #Get bin widths
    normal_binedges = 10**binedges
    bin_widths = normal_binedges[1:] - normal_binedges[:-1]
        
    #Remove any NaNs
    binstddatax = 10**binstddatax[~np.isnan(binmeandatax)]
    binmembercount = binmembercount[~np.isnan(binmeandatax)]
    binmeandatax = 10**binmeandatax[~np.isnan(binmeandatax)]
    bin_widths = bin_widths[~np.isnan(binmeandatax)]
    
    return binmeandatax, binstddatax, binmembercount, bin_widths
