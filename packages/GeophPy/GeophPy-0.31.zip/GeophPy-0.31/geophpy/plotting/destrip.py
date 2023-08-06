# -*- coding: utf-8 -*-
'''
    geophpy.plotting.destrip
    ----------------------------

    Map Plotting Destriping Managing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.pyplot as plt
import geophpy.processing.general as genprocessing
import numpy as np
import math



def plotmean(dataset, fig=None, filename=None, Nprof=0, method='add', reference='mean', config='mono', Ndeg=None, plotflag='raw', dpi=None, transparent=False):
    '''
    Plotting the mean cross-track (mean of each profile).
    '''

    if (fig == None) :                      # if first display
        fig = plt.figure()                  # creates the figure
    else :                                  # if not first display
        fig.clf()                           # clears figure

    ax = fig.add_subplot(111)

    # Data before destriping #########################################
    DatasetRaw = dataset.copy()
    DatasetRaw.peakfilt(setmin=None, setmax=None, setnan=True, valfilt=False)
    Z    =  DatasetRaw.data.z_image
    cols = range(Z.shape[1])
    
    ZMOY = np.nanmean(Z,axis=0,keepdims=True)
    ZSTD = np.nanstd(Z,axis=0,keepdims=True)
    MOY = np.nanmean(Z)

    # Data destriping ################################################
    if Ndeg==None:
        genprocessing.destripecon(DatasetRaw, Nprof=Nprof, setmin=None, setmax=None, method=method, reference=reference, config=config, valfilt=False)
    else :
        genprocessing.destripecub(DatasetRaw, Nprof=Nprof, setmin=None, setmax=None, Ndeg=Ndeg, valfilt=False)

    # Reference mean and std dev ##################################### 
    # Moments of the global map
    if (Nprof == 0):
        MOYR = np.nanmean(Z)
        STDR = np.nanstd(Z)
        
    # Moments on Nprof profile
    else:
        MOYR = np.zeros(ZMOY.shape)
        STDR = np.zeros(ZSTD.shape)
        kp2  = Nprof // 2
        # Mean of Nprof cols centered the profile
        for jc in cols:
            jc1 = max(0,jc-kp2)
            jc2 = min(Z.shape[1]-1,jc+kp2)
            MOYR[0,jc] = np.nanmean(Z[:,jc1:jc2])
            STDR[0,jc] = np.nanstd(Z[:,jc1:jc2])    

    # Data after destriping ##########################################
    Zdsp    = DatasetRaw.data.z_image
    ZMOYdsp = np.nanmean(Zdsp,axis=0,keepdims=True)
    ZSTDdsp = np.nanstd(Zdsp,axis=0,keepdims=True)

    # Build the image ################################################
    
    # Plot raw data
    if plotflag=='raw' or plotflag=='both':
        x = np.arange(ZMOY.size).reshape((-1,1))
        y = ZMOY.reshape((-1,1))
        
        ax.plot(x, y, 'bo:', linewidth=2,markerfacecolor='None', label='Data')
        ax.plot([0, ZMOY.size-1], [MOY, MOY], 'k-', linewidth=2, label='Global mean')

    # Plot destriped data
    if plotflag=='destriped' or plotflag=='both':
        xdsp = np.arange(ZMOYdsp.size).reshape((-1,1))
        ydsp = ZMOYdsp.reshape((-1,1))

        xref = np.arange(MOYR.size).reshape((-1,1))
        yref = MOYR.reshape((-1,1))
        
        ax.plot(xdsp, ydsp, 'r-', linewidth=2, label='Destriped')
        ax.plot(xref, yref, 'g--', linewidth=2, label='Reference')
    
    # Axis labels
    ax.set_title('Mean cross-track profile')
    ax.set_xlabel('Profile number')
    ax.set_ylabel('Mean value')

    # Upper center legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    #ax.legend(frameon=False, loc=9, ncol=3, mode='expand')
    ax.legend(frameon=False, loc=9, ncol=2)

    # Saving into a file #############################################
    if (filename != None):
       plt.savefig(filename, dpi=dpi, transparent=transparent)

    return fig
