# -*- coding: utf-8 -*-
'''
    geophpy.processing.general
    --------------------------

    DataSet Object general processing routines.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
### USER DEFINED PARAMETERS ##########################################

# list of correlation methods available for wumappy interface
festoon_correlation_list = ['Crosscorr','Pearson', 'Spearman', 'Kendall']

# list of destriping methods available for wumappy interface
destriping_list = ['additive', 'multiplicative']
destripingreference_list = ['mean','median']
destripingconfig_list = ['mono','multi']

# list of regional trend methods available for wumappy interface
regtrendmethod_list = ['relative', 'absolute']

# list of regional trend components available for wumappy interface
regtrendcomp_list = ['local', 'regional']

######################################################################



import numpy as np
import scipy.ndimage as ndimage
from scipy.stats import pearsonr, spearmanr, kendalltau
###
#from numpy import matlib
# import time
#from scipy.optimize import curve_fit
#import scipy.ndimage.interpolation as ndint
#import matplotlib.pyplot as plt
###
from geophpy.misc.utils import *
from geophpy.operation.general import *



def peakfilt(dataset, setmin=None, setmax=None, setmed=False, setnan=False, valfilt=False):
   '''
   cf. dataset.py
   '''
###ORIGINAL CODE having some flaws:
###- min and max are builtin functions (reserved words)
###- should be able to work on values as well as on zimage
###- should be able to replace by nan or median instead of threshold
###- is iterative (for ...) ; should be global (where ...)
   #for i in range(dataset.info.lines_nb) :
   #   if ((min != None) and (dataset.data.values[i][2] < min)):
   #      dataset.data.values[i][2] = min
   #   elif ((max != None) and (dataset.data.values[i][2] > max)):
   #      dataset.data.values[i][2] = max
###
   if (valfilt):
      val = dataset.data.values[:,2]
   else:
      val = dataset.data.z_image
      ny, nx = val.shape

   if (setmin != None):
      idx = np.where(val < setmin)
      if (setnan):
         val[idx] = np.nan
      elif (setmed):
         # ...TBD... replace by median on x sample centered in the replaced value
         # Median of each profile
         median_profile = np.nanmedian(val, axis=0)
         # Into a matrix for global indexing
         median_profile.shape = [1,median_profile.size]
         med_mat = np.repeat(median_profile, val.shape[0],axis=0)
         # Data replacement
         val[idx] = med_mat[idx]
         
      else:
         val[idx] = setmin

   if (setmax != None):
      idx = np.where(val > setmax)
      if (setnan):
         val[idx] = np.nan
      elif (setmed):
         # ...TBD... replace by median on x sample centered in the replaced value
         # Median of each profile
         median_profile = np.nanmedian(val, axis=0)
         # Into a matrix for global indexing
         median_profile.shape = [1,median_profile.size]
         med_mat = np.repeat(median_profile, val.shape[0],axis=0)
         # Data replacement
         val[idx] = med_mat[idx]
         
      else:
         val[idx] = setmax


def medianfilt(dataset, nx=3, ny=3, percent=0, gap=0, valfilt=False):
    '''
    cf. dataset.py
    '''
    # Filter values ...TBD... ######################################
    if (valfilt):
        # ...TBD... should use original wumap algorithm
        pass
    # Filter zimage ################################################
    else:
        zimg = dataset.data.z_image
        if (percent == 0) & (gap == 0):
            zimg[:,:] = ndimage.median_filter(zimg, size=(nx, ny))

        else:
            # ...TBD... should use here also original wumap algorithm
            zmed = ndimage.median_filter(zimg, size=(nx, ny))
            zdiff = np.absolute(zimg-zmed)
            
            # Gap to the median in percent (Electric surveys) 
            if (percent != 0) & (gap == 0):
                idx = np.where(zdiff> percent/100 * zmed)

            # Gap to the median value (Magnetic surveys)
            elif (percent == 0) & (gap != 0):
                idx = np.where(zdiff> gap)

            zimg[idx[0],idx[1]] = zmed[idx[0],idx[1]]

####
# Not used yet
####
def sliding_window_1D(arr, n):
    '''
    Creates a sliding windows of size n for 1D-array.
    
    This function uses stride_tricks to creates a sliding windows
    without using explicit loops. Each of the windows is return in an
    extra dimension of the array.

    n = 3

    0 |    0      0     0     0     0     0     0
    1 |    1 |    1     1     1     1     1     1
    2 |    2 |    2|    2     2     2     2     2
    3      3 |    3|    3|    3     3     3     3
    4      4      4|    4|    4|    4     4     4
    5      5      5     5|    5|    5|    5     5
    6      6      6     6     6|    6|    6|    6
    7      7      7     7     7     7|    7|    7|
    8      8      8     8     8     8     8|    8|
    9      9      9     9     9     9     9     9|
    -->
    
        - - - - - - - - > arr.size - n + 1
      | 0 1 2 3 4 5 6 7
    n | 1 2 3 4 5 6 7 8
      | 2 3 4 5 6 7 8 9
      v   
    '''

    shape = arr.shape[:-1] + (arr.shape[-1] - n + 1, n)  #
    strides = arr.strides + (arr.strides[-1],)           #

    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
####
####

def getfestooncorrelationlist():
   """
   cf. dataset.py

   """
   return festoon_correlation_list



def festoonfilt(dataset, method='Crosscorr', shift=0, corrmin=0.4, uniformshift=False, valfilt=False):
   '''
   cf. dataset.py
   '''
   #...TDB...
   # add an idx mask option to ignore points (anomalies) in the data without having to clip de data
   # Some thing like ignore value sup or if to, or cliked data (index matrix passed to the function)

   
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = correlcols(zimg.shape[1])
      shift = np.array(shift) # shift as ndarray (use of shape, size)

      # Uniform shift ################################################
      if (uniformshift == True):
         
          # Shift not provided (shift is default=0)
          if (shift == 0 and shift.size == 1):
              cor1, pva1 = correlmap(dataset, method)  # correlation map
              shift, shiftprf = correlshift(cor1, pva1, corrmin=corrmin)  # global best shift
              shiftprf = np.repeat(shift,len(cols))  # shift repeated for each profile
              
          # Shift provided (uniform scalar value)
          elif(shift != 0 and shift.size == 1):
              shiftprf = np.repeat(shift,len(cols))   # shift for each profile

      # Non-uniform shift ############################################
      elif(uniformshift == False):
         
          # Shift not provided / uniform shift provided
          if (shift.size == 1):
              cor1, pva1 = correlmap(dataset, method)  # correlation map
              shift, shiftprf = correlshift(cor1, pva1, corrmin=corrmin)  # global and profile best shifts
              
          # Shift provided (custom shift sequence)
          else:
              tmp = shift  # custom shift sequence
              cor1, pva1 = correlmap(dataset, method)  # correlation map
              shift, shiftprf = correlshift(cor1, pva1, corrmin=corrmin)  # global best shift
              shiftprf =  tmp
      
      # Apply the shift to each profile ##############################
      j=0
##      print('--festoonfilt-general.py--')
##      print(shiftprf)
      for i in cols:
         #zimg[:,i] = np.roll(zimg[:,i],shiftprf[j])
         zimg[:,i] = arrayshift(zimg[:,i],shiftprf[j],val=np.nan)
         j+=1

   return shift



def correlcols(nx):
   return range(1,nx-1,2) # ...TBD... à revoir ?


def arrayshift(arr, shift, val=None):
    '''
    Roll array element.
    Elements that roll beyond the last position are replaced by val
    or re-introduced at the first (if val=None).
    '''
    # No shift
    if shift==0:
        arrshift = arr
        return arrshift
        
    # Allocating empy (shifted) array
    arrshift = np.empty_like(arr)
        
    # Circular shift
    if val==None:
        arrshift = np.roll(arr, shift, axis=None)
        
    # Shifting & Padding with val
    if shift >= 0:
        arrshift[:shift] = val
        arrshift[shift:] = arr[:-shift]
    else:
        arrshift[shift:] = val
        arrshift[:shift] = arr[-shift:]

    return arrshift


def correlmap(dataset, method):
    '''
    cf. dataset.py
    '''
    
##########
##########
###ORIGINAL CODE having some flaws:
###- The 'Pearson' method is in fact the definition of signal cross-correlation
###- Issue with the other correlation methods
         #zimg = dataset.data.z_image
         #cols = correlcols(zimg.shape[1])
         #ny   = zimg.shape[0]
         #jmax = 2*ny-1
         #cor1 = np.zeros(shape=(jmax,len(cols))) / 0.
         #pva1 = cor1.copy()
         #ii   = 0
         
        #if (method == 'Pearson'):
        #   # Use Pearson correlation ################################
        #   for i in cols:
        #      z1   = (zimg[:,i-1] + zimg[:,i+1]) / 2. # ...TBD... nanmean ?
        #      z1   = (z1 - np.nanmean(z1)) / np.nanstd(z1)
        #      zi   = zimg[:,i] * 1.
        #      zi   = (zi - np.nanmean(zi)) / np.nanstd(zi)
        #      idx  = np.isfinite(z1) & np.isfinite(zi)
        #      jlen = 2*len(idx.nonzero()[0])-1
        #      if (jlen > 0):
        #         jmin  = (jmax - jlen) // 2
        #         cor1[jmin:jmin+jlen,ii] = np.correlate(z1[idx],zi[idx],mode='full') / idx.sum()
        #         pva1[jmin:jmin+jlen,ii] = 1
        #      ii += 1
        #else:
        #   # Use Spearman or Kendall correlation ####################
        #   for i in cols:
        #      z1 = (zimg[:,i-1] + zimg[:,i+1]) / 2. # ...TBD... nanmean ?
        #      for j in range(-ny+1,ny):
        #         zi = np.roll(zimg[:,i],j)
        #         if (j < 0):
        #            zi[ny+j:ny] = np.nan
        #         else:
        #            zi[0:j] = np.nan
        #         idx = np.isfinite(z1) & np.isfinite(zi)
        #         if (method == 'Spearman'):
        #            # Use Spearman correlation ######################
        #            cors, pval = spearmanr(z1[idx],zi[idx])
        #         elif (method == 'Kendall'):
        #            # Use Kendall correlation #######################
        #            # ...TBD... something goes wrong here ? what ? why ?
        #            #cors, pval = kendalltau(z1[idx],zi[idx])
        #            pass
        #         else:
        #            # Undefined correlation method ##################
        #            # ...TBD... raise an error here !
        #            pass
        #      if (len(z1[idx]) > 1):
        #         cor1[j+ny-1,ii] = cors
        #         pva1[j+ny-1,ii] = pval
        #      ii+=1
##########
##########

    # Data spatial properties ########################################
    zimg   = dataset.data.z_image
    ny, nx = zimg.shape
    cols = correlcols(zimg.shape[1])  # index of odd columns

    ###
    #... TBD NOT USED FOR THE MOMENT ...
    #
    # Ignoring All-NaN slice #########################################
    # Gridding properties associated with no interpolation can produce
    # All-NaN slices. Typically if the surveyed profile are made with
    # a 1m step (x-axis) and the user display a 50cm sterp grid with
    # interpolation this will produce All-NaN slices every odd columns
    # of the displayed grid.
    idx_nan_slice = np.all(np.isnan(zimg), axis=0)  # index of columns containing only nans
    #print('---')
    #print('All-NaN Slices index')
    #print(idx_nan_slice)
    #
    ###

    # Correlation map & pvalue initialization ############################
    jmax = 2*ny-1  # maximum profile shift
    correlmap = np.full((jmax, len(cols)), np.nan)  # arrays filled with inf
    pva1 = correlmap.copy()
         
    # Use Cross-correlation function ############################
    # Calculation between the current (standardized) profile
    # and the (standardized) mean of its two neighboring profiles
    #
    # example for center profile: #=(cpy)
    #
    # col -nx=1     col +nx=1
    #        o # o 
    #        - # -  
    #        - # -  
    #        - # -   
    #        o # o
    # col -nx=1     col +nx=1
    ii   = 0
    if (method == 'Crosscorr'):
       for col in cols:
               
          # Standardized mean profile
          zm   = (zimg[:,col-1] + zimg[:,col+1]) / 2. # ...TBD... nanmean ?
          zm   = (zm - np.nanmean(zm)) / np.nanstd(zm)
              
          # Standardized current profile
          zi   = zimg[:,col] * 1.
          zi   = (zi - np.nanmean(zi)) / np.nanstd(zi)
               
          # Not NaN or inf in data
          idx  = np.isfinite(zm) & np.isfinite(zi)
          jlen = 2*len(idx.nonzero()[0])-1
               
          # Cross-correlation function map
          if (jlen > 0):
             jmin  = (jmax - jlen) // 2
             correlmap[jmin:jmin+jlen,ii] = np.correlate(zm[idx],zi[idx],mode='full') / idx.sum()
             pva1[jmin:jmin+jlen,ii] = 1
                  
          ii += 1
         
    # Use Pearson, Spearman or Kendall correlation ##############
    # The current profile is manually shifted of a sample at each
    # iteration. The correlation coefficient is then computed
    # between the shifted profile and the mean of its two
    # adjacent profiles       
    else:           
        for col in cols:
               
            # Mean profile
            zm = (zimg[:,col-1] + zimg[:,col+1]) / 2. # ...TBD... nanmean ?
            zm   = (zm - np.nanmean(zm)) / np.nanstd(zm)
            
            k = 0
     
            for shift in range(-ny+1,ny):
                # Calculation for at least 1/2 of  overlap between profiles
                # Prevents high correlation value at the border of the
                # correlation map (low number of samples)
                if shift<=ny//2 and shift >= -ny//2:
                     # Shifting current profile
                    zi = arrayshift(zimg[:,col], shift, val=None)
                
                    # Not NaN or inf in data
                    idx = np.isfinite(zm) & np.isfinite(zi)
                    jlen = 2*len(idx.nonzero()[0])-1
                
                    # Correlation coefficent map
                    if (jlen > 0):
                     
                        # Pearson
                        if (method == 'Pearson'):
                            cors, pval = pearsonr(zm[idx],zi[idx])

                        # Spearman
                        elif (method == 'Spearman'):
                            cors, pval = spearmanr(zm[idx],zi[idx])

                        # Kendall
                        elif (method == 'Kendall'):
                            cors, pval = kendalltau(zm[idx],zi[idx])

                        # Undefined
                        else:
                           # ...TBD... raise an error here !
                           pass
                     
                        # Filling arrays
                        correlmap[k,ii] = cors
                        pva1[k,ii] = pval
                     
                k+=1
                  
            ii+=1
    
    return correlmap, pva1


def correlshift(correlmap, pva1, corrmin=0.4, apod=None, output=None):
    '''
    cf. dataset.py
    '''
    
    ny = (correlmap.shape[0] + 1) // 2

    # Define correlation curve apodisation threshold #################
    if (apod == None):
        apod = 0.1  # percent of the max correl coef

    # Make a mask for nans and apodisation ######################
    MaskApod  = np.isfinite(correlmap).sum(axis=1).astype(float)
    idx   = np.where(MaskApod < max(MaskApod) * apod)
    MaskApod[idx] = np.nan

    pval  = np.isfinite(pva1).sum(axis=1).astype(float)
    idx   = np.where(pval < max(pval) * apod)
    pval[idx] = np.nan

    # Mask for 1/2 overlap profile in correlation map ###########
    # Prevents high correlation value at the border of the
    # correlation map (low number of samples) to drag the shift
    y = np.arange(correlmap.shape[0])
    ymin = correlmap.shape[0]*  2 // 6  # inf 1/4 of correl map
    ymax = correlmap.shape[0]*  4 // 6  # sup 1/4 of correl map
    idx = np.where(np.logical_or(y<ymin, y>ymax))

    coroverlap = correlmap.copy()
    coroverlap[idx,:] =  0

    # Maximum correlation shift for every profile ###############
    idx = np.argmax(coroverlap,axis=0)
    corrmax = np.amax(coroverlap,axis=0)  # profiles' max correlation
    shiftprf = idx -ny+1

    if corrmin != None:
        shiftprf[np.where(corrmax<corrmin)] = 0
          
    # Fold the correlation map for global shift #################
    cor  = np.nansum(coroverlap,axis=1) / MaskApod
    #cor  = np.nansum(correlmap,axis=1) / MaskApod
    #pva2  = np.nansum(pva1,axis=1) / pval
    
    #corm2  = cor2 / pva2
    # corm  = cor / pva2  # producess very high value if pval is low
    corm  = cor
         
    # Deduce the best 'shift' value from the max correl coef ####
    idx   = (corm == np.nanmax(corm)).nonzero()
    
    # ... TBD ... temporay fix for correlation calculation bug
    # giving no results
    if idx[0] is None:
        print('--correlshift - general.py--')
        print('correlation calculation bug, no  global maximum found')
        print('Shift set to 0')
        shift = 0

    # ...TBD... en fait ici fitter une gaussienne et trouver son max
    else:
        shift = idx[0][0]-ny+1

    if (output != None): # FutureWarning: comparison to `None` will result in an elementwise object comparison in the future
        output[:] = corm[:]

    return shift, shiftprf



def getdestripinglist():
   """
   cf. dataset.py

   """
   return destriping_list


def getdestripingreferencelist():
   """
   cf. dataset.py

   """
   return destripingreference_list


def getdestripingconfiglist():
   """
   cf. dataset.py

   """
   return destripingconfig_list


def destripecon(dataset, Nprof=0, setmin=None, setmax=None, method='additive', reference='mean', config='mono', valfilt=False):
    '''
    cf. dataset.py
    '''
    dstmp = dataset.copy()
    dstmp.peakfilt(setmin=setmin, setmax=setmax, setnan=True, valfilt=valfilt)

    # Filter values ...TBD... ########################################
    if (valfilt):    
        pass
    
    # Filter zimage ##################################################
    else:
        zimg = dataset.data.z_image
        nl, nc = zimg.shape
        cols = range(nc)

        # Statistics for each profile ################################
        Z     = dstmp.data.z_image
        
        # Mean and standard deviation
        m_i   = np.nanmean(Z,axis=0,keepdims=True)
        sig_i = np.nanstd(Z,axis=0,keepdims=True)

        # Median and InterQuartile Range
        med_i   = np.nanmedian(Z,axis=0,keepdims=True)
        q25_i, q75_i = np.nanpercentile(Z,[25,75],axis=0,keepdims=True)
        iqr_i = q75_i - q25_i

        # References #################################################
        # Global mean and std dev of the dataset 
        if (Nprof == 0):
            m_d   = np.nanmean(Z)
            sig_d = np.nanstd(Z)
          
            med_d    = np.nanmedian(Z)
            q25_d, q75_d = np.nanpercentile(Z,[25,75])
            iqr_d    = q75_d - q25_d
          
        # Centered references for Nprof neighboring profile
        # example Nprof=6 and center profile: #=(cpy)
        #            Nprof
        #        <----------->
        # col -nx              col +nx
        #        o - - # - - o 
        #        - - - # - - -  
        #        - - - # - - -  
        #        - - - # - - -   
        #        o - - # - - o
        # col -nx              col +nx      
        else:
            # Allocation
            m_d   = np.zeros(m_i.shape)
            sig_d = np.zeros(sig_i.shape)
            
            med_d   = np.zeros(med_i.shape)
            iqr_d = np.zeros(iqr_i.shape)
            
            # Compuation
            for col in cols:
                # profiles index
                idL = max(0,col-Nprof)  # left col index
                idR = min(nc-1,col+Nprof)  # right col index

                # Mean and standard deviation
                m_d[0,col] = np.nanmean(Z[:,idL:idR])
                sig_d[0,col] = np.nanstd(Z[:,idL:idR])

                # Median and InterQuartile Range
                med_d[0,col] = np.nanmedian(Z[:,idL:idR])
                q25, q75     = np.nanpercentile(Z[:,idL:idR],[25,75])
                iqr_d[0,col] = q75 - q25

        # Rescale the profiles #######################################
        if (method == 'additive'):
            ### ------------------------------------------------------
            # Matching mean and standard deviation ###################
            if reference.lower()=='mean':
                # Mono sensor
                if config.lower()=='mono':
                    zcorr = zimg - m_i + m_d
                    
                # Multi sensor
                elif config.lower()=='multi':
                    zcorr = (zimg - m_i)*(sig_d/sig_i) + m_d
                    
            # Matching median and iterquartile range #################
            if reference.lower()=='median':
                # Mono sensor
                if config.lower()=='mono':
                    zcorr = zimg - med_i + med_d
                    
                # Multi sensor
                elif config.lower()=='multi':
                    zcorr = (zimg - med_i)*(iqr_d/iqr_i) + med_d

            dataset.data.z_image = zcorr
            ### ------------------------------------------------------
            
            #zimg -= m_i
            #zimg += m_d
         
        elif (method == 'multiplicative'):
            ### ------------------------------------------------------
            # Matching mean and standard deviation ###################
            if reference.lower()=='mean':
                # Mono sensor
                if config.lower()=='mono':
                    zcorr = zimg * (m_d / m_i)
                    
                # Multi sensor
                elif config.lower()=='multi':
                    zcorr = zimg * (sig_d/sig_i) * (m_d/m_i)
                    
            # Matching median and iterquartile range #################
            if reference.lower()=='median':
                # Mono sensor
                if config.lower()=='mono':
                    zcorr = zimg * (med_d/med_i)
                    
                # Multi sensor
                elif config.lower()=='multi':
                    zcorr = zimg *(iqr_d/iqr_i) * (med_d/med_i)

            dataset.data.z_image = zcorr
            ### ------------------------------------------------------
                    
                    
            #zimg *= m_d
            #zimg /= m_i
        else:
           # Undefined destriping method ###############################
           # ...TBD... raise an error here !
           pass


def destripecub(dataset, Nprof=0, setmin=None, setmax=None, Ndeg=3, valfilt=False):
   '''
   cf. dataset.py

   '''
   dstmp = dataset.copy()
   dstmp.peakfilt(setmin=setmin, setmax=setmax, setnan=True, valfilt=valfilt)

   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg   = dataset.data.z_image
      nl, nc = zimg.shape
      cols   = range(nc)
      y      = zimage_ycoord(dataset)

      # Compute the polynomial coefs for each profile ################
      Z    = dstmp.data.z_image
      ZPOL = np.polyfit(y[:,0],Z,Ndeg)

      # Compute the polynomial reference #############################
      if (Nprof == 0):
         POLR = np.nanmean(ZPOL, axis=1, keepdims=True)
      else:
         POLR = np.zeros(ZPOL.shape)
         kp2  = Nprof // 2
         for jc in cols:
            jc1 = max(0,jc-kp2)
            jc2 = min(zimg.shape[1]-1,jc+kp2)
            POLR[:,jc] = np.nanmean(ZPOL[:,jc1:jc2], axis=1, keepdims=True)[:,0]

      # Rescale the profiles #########################################
      for d in range(Ndeg):
         zimg -= np.array([ZPOL[d+1]])*y**(d+1)
      if (Nprof != 1):
         zimg -= ZPOL[0]
         for d in range(Ndeg+1):
            zimg += np.array([POLR[d]])*y**d



def getregtrendmethodlist():
   """
   cf. dataset.py

   """
   return regtrendmethod_list



def getregtrendcomplist():
   """
   cf. dataset.py

   """
   return regtrendcomp_list



def regtrend(dataset, nx=3, ny=3, method="relative", component="local", valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image
      cols = range(zimg.shape[1])
      ligs = range(zimg.shape[0])
      nx2  = nx//2
      ny2  = ny//2
      znew = zimg * 0.

      # Compute the mean of all data #################################
      zmoy = np.nanmean(zimg)

      # Compute the mean in each window ##############################
      for jl in ligs:
         jl1 = max(0, jl - nx2)            # ...TBD... -1 ?
         jl2 = min(max(ligs), jl + nx2)    # ...TBD... -1 ?
         for jc in cols:
            jc1 = max(0, jc - ny2)         # ...TBD... -1 ?
            jc2 = min(max(cols), jc + ny2) # ...TBD... -1 ?
            zloc = np.nanmean(zimg[jl1:jl2,jc1:jc2])
            if (component == "local"):
               if (method == "relative"):
                  znew[jl,jc] = zimg[jl,jc] * zmoy / zloc
               elif (method == "absolute"):
                  znew[jl,jc] = zimg[jl,jc] - zloc
               else:
                  # Undefined method #################################
                  # ...TBD... raise an error here !
                  pass
            elif (component == "regional"):
               znew[jl,jc] = zloc
            else:
               # Undefined component #################################
               # ...TBD... raise an error here !
               pass

      # Write result to input dataset ################################
      zimg[:,:] = znew


def wallisoperator(cval, winval, setgain, targmean, targstdev, limitstdev, edgefactor):
    '''
    cf. dataset.py
    '''
    # Wallis constants
    A = setgain           # amplification factor
    m_d = targmean        # the target mean
    sig_d = targstdev     # target standard deviation
    alpha = edgefactor    # edgefactor
    sig_lim = limitstdev  # maximum standard deviation value

    # Window statistics
    # winval                       # current window values
    f_xy = cval                    # window center pixel
    m_xy = np.nanmean(winval)      # window mean 
    sig_xy = np.nanstd(winval)     # window strd. dev.
    sig_xy = min(sig_xy, sig_lim)  # limitation on max strd. dev.

    # Wallis operator
    g_xy = A*sig_d / (A * sig_xy + sig_d) * (f_xy - m_xy) + alpha*m_d + (1-alpha)*m_xy

    return g_xy


def val_to_bright(val, nblvl=256, valmin=None, valmax=None):
    '''
    cf. dataset.py
    '''
    # No min or max values provided
    if valmin==None:
        valmin = np.nanmin(val)
    if valmax==None:
        valmax = np.nanmax(val)

   # Scaling values from 0 to nblvl-1 brightness level
    step = (valmax-valmin) / (nblvl)    # conv. factor from lvl to val
    lvl = np.around((val-valmin)/step)  # brightness level
    
    # Insuring no overlimit brightness values 
    lvl[np.where(lvl<0)] = 0
    lvl[np.where(lvl>nblvl-1)] = nblvl-1

    return lvl


def bright_to_val(lvl, valmin, valmax, nblvl=256):
    '''
    cf. dataset.py
    '''
    # Scaling values from valmin to valmax
    step = (valmax-valmin) / (nblvl)  # conv. factor from lvl to val
    val = lvl*step + valmin           # from brightness level to values

    # Insuring no overlimit values
    val[np.where(val<valmin)] = valmin
    val[np.where(val>valmax)] = valmax

    return val


def wallisfilt(dataset, nx=11, ny=11, targmean=125, targstdev=50, setgain=8, limitstdev=25, edgefactor=0.1, valfilt=False):
    '''
    cf. dataset.py
    '''
    # Filter values ...TBD... ######################################
    if (valfilt):
       
       pass

    # Filter zimage ##################################################
    else:    
        # Map/Image properties #######################################
        zimg = dataset.data.z_image
        zmin, zmax = dataset.histo_getlimits()
        nl, nc = zimg.shape

        # Converting values to brightness ############################
        nblvl = 256  # number of levels
        zlvl = val_to_bright(zimg, nblvl=nblvl, valmin=zmin, valmax=zmax)

        # ...TBD... ##################################################
        # Replacement of the mean and standard deviation by the median
        # (M a for m a and local median for if(i, j)) and interquartile
        # distance (Qd for o a and local interquartile for a(i, j)),
        # respectively, was suggested as a solution. The Huang-Yang-Tang
        # [14] running median algorithm was employed for computational
        # efficiency.

        # Filter constantes (names as in Scollar, 1990) ##############
        A, sig_d, m_d = setgain, targstdev, targmean
        alpha, sig_lim = edgefactor, limitstdev

        # 2D Sliding Window ##########################################
        ####
        # ...TBD... 2D sliding window with  more Pythonic ?
        # ...TBD... scipy.ndimage.generic_filter ?
        ####
        # The SW is centered on the pixel so it has (ny) pixels above
        # and under the center pixel (#), and (nx) pixels to its left
        # and to its right.
        #
        # example for SW with nx=3, ny=2 and center pixel: #=(cpx, cpy)
        #              lx
        #         <----------->
        # cpx -nx              cpx +nx
        # cpy +ny              cpy +ny
        #    ^    o - - - - - o 
        #    |    - - - - - - -  
        # ly |    - - - # - - -  
        #    |    - - - - - - -   
        #    v    o - - - - - o
        # cpx -nx              cpx +nx
        # cpy +ny              cpy +ny
        #

        # Sliding Window dimension
        lx = 2*nx + 1  # total window length
        ly = 2*ny + 1  # total window height
        g_xy = np.empty(zimg.shape)

        # Sweeping rows & columns preventing out of range index
        # using comparison to nl and nc
        for cpy in range(nl):
            sw_top = max(cpy - ny, 0)  # SW top index
            sw_bot = min(cpy + ny, nl-1)  # SW bottom index
            swy = np.arange(sw_top,sw_bot+1).reshape((-1,1))  # SW rows index
          
            for cpx in range(nc):
                # Current SW index bounds
                sw_left = max(cpx - nx, 0)  # SW left index
                sw_right = min(cpx + nx, nc-1) # SW right index
                swx = np.arange(sw_left,sw_right+1).reshape((1,-1))  # SW cols index

                # Current SW index (broadcating index vectors)
                swi = swy*np.ones(swx.shape) # SW matix rows index
                swj = swx*np.ones(swy.shape) # SW matix cols index
                swi = np.asarray(swi.reshape((1,-1)), dtype=np.int16)
                swj = np.asarray(swj.reshape((1,-1)), dtype=np.int16)

                # Current SW Wallis operator
                win_xy = zlvl[swi,swj]   # current window
                f_xy = zlvl[cpy,cpx]    # current window center
                if ~np.isnan(f_xy):
                    g_xy[cpy,cpx] = wallisoperator(f_xy, win_xy, A,
                                                   m_d, sig_d, sig_lim, alpha)
                else:
                    g_xy[cpy,cpx] = f_xy
  
        # Converting brightness back to values #######################
        # ...TDB... raise warniing when comapring with nan ?
        # ...TDB... using nan ignoring technic/mask ?
        g_xy[np.where(g_xy<0)] = 0
        g_xy[np.where(g_xy>nblvl-1)] = nblvl-1
        znew = bright_to_val(g_xy, zmin, zmax, nblvl=nblvl)

        # Writting result to input dataset ###########################
        zimg[:,:] = znew


def ploughfilt(dataset, nx=3, ny=3, apod=0, angle=None, cutoff=None, valfilt=False):
   '''
   cf. dataset.py

   '''
   if (valfilt):
      # Filter values ...TBD... ######################################
      pass
   else:
      # Filter zimage ################################################
      zimg = dataset.data.z_image

      if (apod > 0):
         apodisation2d(zimg, apod)

      cols = range(zimg.shape[1])
      # ...TBD...
