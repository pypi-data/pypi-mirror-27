# -*- coding: utf-8 -*-
'''
    geophpy.plotting.histo
    ----------------------

    Map Plotting Histofeam Managing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.pyplot as plt
###
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
###
import numpy as np
import math


def plot(dataset, fig=None, filename=None, zmin=None, zmax=None, cmapname=None, dpi=None, transparent=False):
    '''plotting the histogram curve.'''
    if (fig == None):
        fig = plt.figure()
    else:
        fig.clf()    
####
####    
    # Original code had some flaws.
    # Did not work with data containing NaN.
    # Did not when no zmin&zmax entered.
    #
    # Z = dataset.data.z_image
    # n, bins, patches = plt.hist(Z.reshape((1, Z.shape[0]*Z.shape[1]))[0], bins=100, range=(zmin,zmax), facecolor='black', alpha=1)
####
####
    
    # Ignoring NaNs
    nanidx = np.isnan( dataset.data.z_image )  # index of nan
    Z = dataset.data.z_image[~nanidx]

    # Creating histogram curve
    if (zmin == None or zmax == None):
        n, bins, patches = plt.hist(Z.flatten(), bins=100, range=None, facecolor='black', alpha=1)
    else:
        n, bins, patches = plt.hist(Z.flatten(), bins=100, range=(zmin,zmax), facecolor='black', alpha=1)

    # Color map histogram
    if cmapname!=None:
        
        # Color map
        cm = plt.cm.get_cmap(cmapname)

        # Normalizing from 0 to 1
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        color = bin_centers - min(bin_centers)
        color /= max(color)

        # Setting individual patche color
        for clr, patche in zip(color, patches):
            patche.set_facecolor(cm(clr))
            patche.set_edgecolor('None')

##... TBD ... this script dor Colorbar plot doesn't work
##    # Colorbar display
##    cmapdisplay = True
##    if cmapdisplay and cmapname!=None:
##        ax = plt.gca()
##        divider = make_axes_locatable(ax)
##        cax = divider.append_axes("bottom", size="5%", pad=0.1)
##        #colormap = plt.colorbar(contour,cax=cax, ax=ax, ticks=[cmmin, cmmax])
##        colormap = plt.colorbar(ax,cax=cax)

    # Curve display
    plt.xlim(bins.min(), bins.max())
    if (filename != None):
       plt.savefig(filename, dpi=dpi, transparent=transparent)

    return fig

def getlimits(self):
    '''getting limits values of histogram.'''
    Z = self.data.z_image
    array = np.reshape(np.array(Z), (1, -1))
    min = np.nanmin(array)
    max = np.nanmax(array)
    return min, max
