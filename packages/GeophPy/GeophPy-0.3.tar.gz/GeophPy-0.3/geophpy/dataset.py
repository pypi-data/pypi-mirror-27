# -*- coding: utf-8 -*-
'''
   GeophPy.dataset
   ---------------

   DataSet Object constructor and methods.

   :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
   :license: GNU GPL v3.

'''
from __future__ import absolute_import
import geophpy.plotting.plot as plot
import geophpy.plotting.correlation as correlation
import geophpy.plotting.colormap as colormap
import geophpy.plotting.histo as histo
import geophpy.plotting.destrip as destrip
import geophpy.operation.general as genoperation
import geophpy.processing.general as genprocessing
import geophpy.processing.magnetism as magprocessing
import geophpy.filesmanaging.files as iofiles
import geophpy.geoposset as geopos
import geophpy.geopositioning.kml as kml
import geophpy.geopositioning.raster as raster
import geophpy.geopositioning.general as gengeopositioning
import math, os



#---------------------------------------------------------------------------#
# Informations about DataSet Object                                         #
#---------------------------------------------------------------------------#
class Info:
   x_min = None
   x_max = None
   y_min = None
   y_max = None
   z_min = None
   z_max = None
   x_gridding_delta = None
   y_gridding_delta = None
   gridding_interpolation = None
   plottype = (plot.gettypelist())[0]
   cmapname = 'Greys'



#---------------------------------------------------------------------------#
# Fields names and values about DataSet Object                              #
#---------------------------------------------------------------------------#
class Data:
   fields = None
   values = None
   z_image = None
   easting_image = None    # easting array
   northing_image = None   # northing array



#---------------------------------------------------------------------------#
# Coordinates Object in local and utm referencing                           #
#---------------------------------------------------------------------------#
class GeoRefPoint:
   def __init__(self, easting=None, northing=None):
      self.utm_easting = easting
      self.utm_northing = northing



#---------------------------------------------------------------------------#
# Georeferencement System Object between local and geographics positions    #
#---------------------------------------------------------------------------#
class GeoRefSystem:
   active = False          # data set georeferencement status
   refsystem = None        # 'UTM', 'WGS84', ...
   utm_zoneletter = None   # E -> X
   utm_zonenumber = None   # 1 -> 60
   points_list = []        # list of points, [[num1, lon1 or eastern1, lat1 or northern1, x, y], ...]



#---------------------------------------------------------------------------#
# DataSet Object                                                            #
#---------------------------------------------------------------------------#
class DataSet(object):
   '''
   Creates a DataSet Object to process and display data.

   info = Info()
   data = Data()
   georef = GeoRefSystem()
   '''

   def __init__(self):
      pass

   @classmethod
   def _new(cls):
      '''
      Creates a new empty data set

      '''
      dataset = cls()
      dataset.info = Info()
      dataset.data = Data()
      dataset.georef = GeoRefSystem()
      return dataset

   #---------------------------------------------------------------------------#
   # Data set files management                                                 #
   #---------------------------------------------------------------------------#
   ###
   @staticmethod
   def get_delimiter_from_file(filenameslist, delimiter_list=['\s', ' ', ',', ';', '\t', '    ', '|', '-']):
       '''
       Test for the presence of classic delimiters in the file and
       returns the most prevalent one.

       Parameters:
       
       :filename: file name to be read
       
       :delimiter_list: list of delimiters to test

       Returns:
       
       :delimiter: file delimiter
       
       :success: True if successful, False otherwise
       
       :count:  file delimiter occurence
       '''
       
       return iofiles.getdelimiterfrom_ascii(filenameslist[0],delimiter_list=delimiter_list)
   ###
      
   @staticmethod
   def from_file(filenameslist, fileformat=None, delimiter='\t', x_colnum=1, y_colnum=2, z_colnum=3, skipinitialspace=True, skip_rows=1, fields_row=0):
      '''
      To build a DataSet Object from a file.

      Parameters:

      :filenameslist: list of files to open
                      ['file1.xyz', 'file2.xyz' ...]
                      or
                      ['file*.xyz'] to open all files with filename beginning by "file" and ending by ".xyz"

      :fileformat: format of files to open (None by default implies automatic determination from filename extension)

      Note: all files must have the same format

      :delimiter: pattern delimitting fields within one line (e.g. '\t', ',', ';' ...)

      :x_colnum: column number of the X coordinate of the profile (1 by default)

      :y_colnum: column number of the Y coordinate inside the profile (2 by default)

      :z_colnum: column number of the measurement profile (3 by default)

      :skipinitialspace: if True, several contiguous delimiters are equivalent to one

      :skip_rows: number of rows to skip at the beginning of the file, i.e. to skip header rows (1 by default)

      :fields_row: row number where to read the field names ; if -1 then default field names will be "X", "Y" and "Z"

      Returns:

      :success: true if DataSet Object built, false if not

      :dataset: DataSet Object build from file(s) (empty if any error)

      Example:

      success, dataset = DataSet.from_file("file.csv")

      '''
      # Dispatch method ##############################################
      class From():
         @staticmethod
         def ascii():
            return iofiles.from_ascii(dataset, filenameslist, delimiter=delimiter, x_colnum=x_colnum, y_colnum=y_colnum, z_colnum=z_colnum, skipinitialspace=skipinitialspace, skip_rows=skip_rows, fields_row=fields_row)
         @staticmethod
         def netcdf():
            return iofiles.from_netcdf(dataset, filenameslist, x_colnum=x_colnum, y_colnum=y_colnum, z_colnum=z_colnum)

      # Create a new dataset #########################################
      dataset = DataSet._new()

      # Choose the input file format #################################
      if (fileformat == None):
         # ...TBD... Determine the format from file header
         pass

      if (fileformat == None):
         # Determine the format from filename extension
         file_extension = os.path.splitext(filenameslist[0])[1]
         fileformat = format_chooser.get(file_extension, None)

      # Read the dataset from input file #############################
      if (fileformat in fileformat_getlist()):
         readfile = getattr(From, fileformat)
         error    = readfile()
      else:
         # Undefined file format #####################################
         # ...TBD... raise an error here !
         error = 1

      # Return the dataset and error code ############################
      if (error == 0):
         success = True
      else:
         success = False
      return success, dataset



   def to_file(self, filename, fileformat=None, delimiter='\t', description=None):
      '''
      Save a DataSet Object to a file.

      Parameters :

      :filename: name of file to save.

      :fileformat: format of output file ...

      :delimiter: delimiter between fields in a line of the output file, '\t', ',', ';', ...

      Returns :

      :success: boolean

      '''
      # Dispatch method ##############################################
      class To():
         @staticmethod
         def ascii():
            return iofiles.to_ascii(self, filename, delimiter=delimiter)
         @staticmethod
         def netcdf():
            return iofiles.to_netcdf(self, filename, description=description)

      # Choose the dataset format ####################################
      if (fileformat == None):
         # Determine the format from filename extension
         file_extension = os.path.splitext(filename)[1]
         fileformat = format_chooser.get(file_extension, None)

      # Write the dataset to file ####################################
      if (fileformat in fileformat_getlist()):
         writefile = getattr(To, fileformat)
         error     = writefile()
      else:
         # Undefined file format #####################################
         # ...TBD... raise an error here !
         error = 1

      # Return the error code ########################################
      if (error == 0):
         success = True
      else:
         success = False
      return success



   #---------------------------------------------------------------------------#
   # DataSet Plotting                                                          #
   #---------------------------------------------------------------------------#
   def plot(self, plottype, cmapname, creversed=False, fig=None, filename=None, cmmin=None, cmmax=None, interpolation='bilinear', cmapdisplay=True, axisdisplay=True, pointsdisplay=False, dpi=None, transparent=False, logscale=False, rects=None, points=None):
      '''
      Plot in 2D or 3D dimensions the cartography representation.

      Parameters :

      :plottype: plotting type, '2D-SURFACE', '2D-CONTOUR', ...

      :cmapname: name of the color map used, 'gray_r' for example.

      :creversed: True to add '_r' at the cmname to reverse the color map

      :fig: figure to plot, None by default to create a new figure.

      :filename: name of the picture file to save, None if no file to save.

      :cmmin: minimal value to display in the color map range.

      :cmmax: maximal value to display in the color map range.

      :interpolation: interpolation mode to display DataSet Image ('bilinear', 'bicubic', 'spline16', ...), 'bilinear' by default.

      :cmapdisplay: True to display color map bar, False to hide the color map bar.

      :axisdisplay: True to display axis and labels, False to hide axis and labels

      :pointsdisplay: True to display grid points, False to not display them.

      :dpi: 'dot per inch' definition of the picture file if filename != None

      :transparent: True to manage the transparency for the zones of lack of data

      :logscale: True to display with the log scale

      :rects: [[x0, y0, w0, h0], [x1, y1, w1, h1], ...], None if no selection rectangles to display

      Returns : fig, plt, cmap.   None, None, None if filename with a wrong picture format

      :fig: Figure Object

      :cmap: ColorMap Object

      '''
      dataset_todisplay = genoperation.copy(self)
      return plot.plot(dataset_todisplay, plottype, cmapname, creversed, fig, filename, cmmin=cmmin, cmmax=cmmax, interpolation=interpolation, cmapdisplay=cmapdisplay, axisdisplay=axisdisplay, pointsdisplay=pointsdisplay, dpi=dpi, transparent=transparent, logscale=logscale, rects=rects, points=points)



   def histo_plot(self, fig=None, filename=None, zmin=None, zmax=None, cmapname=None, dpi=None, transparent=False):
      '''
      Plot histogram.

      Parameters :

      :fig: figure to plot, None by default to create a new figure.

      :filename: Name of the histogram file to save, None if no file to save.

      :zmin: Minimal Z value to represent.

      :zmax: Maximal Z value to represent.

      :cmapname: name of the color map used, 'gray_r' for example; if None black histogram is used.

      :dpi: 'dot per inch' definition of the picture file if filename != None

      :transparent: True to manage the transparency.

      Returns :

      :fig: Figure Object

      '''
      return histo.plot(self, fig=fig, filename=filename, zmin=zmin, zmax=zmax, cmapname=cmapname, dpi=dpi, transparent=transparent)



   def correlation_plotmap(self, fig=None, filename=None, method="Pearson", dpi=None, transparent=False):
      '''
      Plot correlation map.

      Parameters :

      :fig: figure to plot, None by default to create a new figure.

      :filename: Name of the histogram file to save, None if no file to save.

      :method: Correlation method

      :transparent: True to manage the transparency.

      Returns :

      :fig: Figure Object

      '''
      return correlation.plotmap(self, fig, filename, method, dpi, transparent)



   def correlation_plotsum(self, fig=None, filename=None, method="Pearson", dpi=None, transparent=False):
      '''
      Plot correlation sum.

      Parameters :

      :fig: figure to plot, None by default to create a new figure.

      :filename: Name of the histogram file to save, None if no file to save.

      :method: Correlation method

      :transparent: True to manage the transparency.

      Returns :

      :fig: Figure Object

      '''
      return correlation.plotsum(self, fig, filename, method, dpi, transparent)


   def destrip_plotmean(self, fig=None, filename=None, Nprof=0, method='additive', reference='mean', config='mono', Ndeg=None, plotflag='raw', dpi=None, transparent=False):
      '''
      Plot colums mean.

      Parameters :

      :fig: figure to plot, None by default to create a new figure.

      :filename: Name of the histogram file to save, None if no file to save.

      :Nprof: number of profiles to compute the reference mean 

      :method: destriping method (additive or multiplicative)

      :reference: destriping reference (mean and standard deviation or median and interquartile range)

      :config: destriping configuration ('mono' sensor: only offset matching (mean / median), 'multi' sensor: both offset and gain (standard deviation/interquartile range))

      :plotflag: 'raw', 'destriped' or 'both' to plot raw, destriped or both data

      :Ndeg: polynomial degree of the curve to fit	

      :transparent: True to manage the transparency.

      Returns :

      :fig: Figure Object

      '''
      
      return destrip.plotmean(self, fig=fig, filename=filename, Nprof=Nprof, method=method, reference=reference, config=config,Ndeg=Ndeg, plotflag=plotflag, dpi=dpi, transparent=transparent)
   

   def histo_getlimits(self):
      '''
      Get the limits values.

      Returns : zmin, zmax

      '''
      return histo.getlimits(self)



   #---------------------------------------------------------------------------#
   # DataSet Operations                                                        #
   #---------------------------------------------------------------------------#
   def copy(self):
      '''
      To duplicate a DataSet Object.

      Parameters:

      :dataset: DataSet Object to duplicate

      Returns:

      :newdataset: duplicated DataSet Object

      '''
      #newdataset = DataSet._new()
      #newdataset = genoperation.copy(self, newdataset)
      #return newdataset
      return genoperation.copy(self)



   def interpolate(self, interpolation="none", x_delta=None, y_delta=None, x_decimal_maxnb=2, y_decimal_maxnb=2, x_frame_factor=0., y_frame_factor=0.):
      '''
      To interpolate raw values into z_image

      Parameters:

      :dataset: DataSet Object to interpolate

      :interpolation: gridding interpolation method to use (from griddinginterpolation_getlist()) ; "none" default value means to simply project raw data on the grid without interpolation (holes will be filled with "nan") ; otherwise "cubic" should be recommended (but currently doesn't handle nans correctly ...)

      :x_delta: gridding delta x ; None default value means to calculate it

      :y_delta: gridding delta y ; None default value means to calculate it

      :x_decimal_maxnb: decimal precision (e.g. 2 means 10^-2) to compute x_delta

      :y_decimal_maxnb: decimal precision (e.g. 1 means 10^-1) to compute y_delta

      :x_frame_factor: frame extension coefficient along x axis (e.g. 0.1 means xlength +10% on each side, i.e. xlength +20% in total) ; pixels within extended borders will be filled with "nan"

      :y_frame_factor: frame extension coefficient along y axis (e.g. 0.45 means yheight +45% top and bottom, i.e. yheight +90% in total) ; pixels within extended borders will be filled with "nan"

      Returns:

      fills the z_image data field and adjusts info meta data

      '''
      return genoperation.interpolate(self, interpolation=interpolation, x_delta=x_delta, y_delta=y_delta, x_decimal_maxnb=x_decimal_maxnb, y_decimal_maxnb=y_decimal_maxnb, x_frame_factor=x_frame_factor, y_frame_factor=y_frame_factor)



   def sample(self):
      '''
      To rebuild the Values from a Z_image
      '''
      return genoperation.sample(self)



   #---------------------------------------------------------------------------#
   # DataSet Geopositioning                                                    #
   #---------------------------------------------------------------------------#
   def to_kml(self, plottype, cmapname, kmlfilename, creversed=False, picturefilename="image.png", cmmin=None, cmmax=None, interpolation='bilinear', dpi=100):
      '''
      Plot in 2D dimensions the cartography representation to export in google earth.

      Parameters :

      :plottype: plotting type, '2D-SURFACE', '2D-CONTOUR', ...xyz

      :cmapname: name of the color map used.

      :kmlfilename: name of the kml file to create

      :creversed: True to add '_r' at the cmname to reverse the color map

      :picturefilename: name of the picture file to save, None if no file to save.

      :cmmin: minimal value to display in the color map range.

      :cmmax: maximal value to display in the color map range.

      :interpolation: interpolation mode to display DataSet Image ('bilinear', 'nearest', 'bicubic'), 'bilinear' by default.

      :cmapdisplay: True to display color map bar, False to hide the color map bar.

      :axisdisplay: True to display axis and labels, False to hide axis and labels

      :dpi: 'dot per inch' definition of the picture file if filename != None

      Returns:

      :success: True if success, False if not.

      '''
      # calculation of the 4 points utm coordinates
      success, [blcorner, brcorner, urcorner, ulcorner] = self.getquadcoords()

      if (success == True):
         # utm to wgs84 conversion
         blcorner_wgs84_lat, blcorner_wgs84_lon = geopos.utm_to_wgs84(blcorner.utm_easting, blcorner.utm_northing, self.georef.utm_zonenumber, self.georef.utm_zoneletter)
         brcorner_wgs84_lat, brcorner_wgs84_lon = geopos.utm_to_wgs84(brcorner.utm_easting, brcorner.utm_northing, self.georef.utm_zonenumber, self.georef.utm_zoneletter)
         urcorner_wgs84_lat, urcorner_wgs84_lon = geopos.utm_to_wgs84(urcorner.utm_easting, urcorner.utm_northing, self.georef.utm_zonenumber, self.georef.utm_zoneletter)
         ulcorner_wgs84_lat, ulcorner_wgs84_lon = geopos.utm_to_wgs84(ulcorner.utm_easting, ulcorner.utm_northing, self.georef.utm_zonenumber, self.georef.utm_zoneletter)

         quadcoords = [(blcorner_wgs84_lon, blcorner_wgs84_lat), (brcorner_wgs84_lon, brcorner_wgs84_lat), (urcorner_wgs84_lon, urcorner_wgs84_lat), (ulcorner_wgs84_lon, ulcorner_wgs84_lat)]

         # creation of the picture file to overlay
         self.plot(plottype, cmapname, creversed, fig=None, filename=picturefilename, cmmin=cmmin, cmmax=cmmax, interpolation=interpolation, cmapdisplay=False, axisdisplay=False, dpi=dpi, transparent=True)

         # creation of the kml file
         kml.picture_to_kml(picturefilename, quadcoords, kmlfilename)

      return success



   def to_raster(self, plottype, cmapname, picturefilename, creversed=False, cmmin=None, cmmax=None, interpolation='bilinear', dpi=100):
      '''
      Plot in 2D dimensions the cartography representation with the world file associated, to using in a SIG application.

      Parameters:

      :plottype: plotting type, '2D-SURFACE', '2D-CONTOUR', ...xyz

      :cmapname: name of the color map used.

      :picturefilename: name of the picture file to save (.jpg, .jpeg, .tif, .tiff, .png) , None if no file to save.

      :creversed: True to add '_r' at the cmname to reverse the color map

      :cmmin: minimal value to display in the color map range.

      :cmmax: maximal value to display in the color map range.

      :interpolation: interpolation mode to display DataSet Image ('bilinear', 'nearest', 'bicubic'), 'bilinear' by default.

      :dpi: 'dot per inch' definition of the picture file

      Returns:

      :success: True if success, False if not.

      '''
      # calculation of the 4 points utm coordinates
      success, [blcorner, brcorner, urcorner, ulcorner] = self.getquadcoords()

      if (success == True):
         # tests if picture format available for raster
         success = raster.israsterformat(picturefilename)

         if (success == True):
            quadcoords = [(blcorner.utm_easting, blcorner.utm_northing), (brcorner.utm_easting, brcorner.utm_northing), (urcorner.utm_easting, urcorner.utm_northing), (ulcorner.utm_easting, ulcorner.utm_northing)]

            # creation of the picture file to overlay
            self.plot(plottype, cmapname, creversed, fig=None, filename=picturefilename, cmmin=cmmin, cmmax=cmmax, interpolation=interpolation, cmapdisplay=False, axisdisplay=False, dpi=dpi, transparent=True)

            # creation of the world file
            success = raster.picture_to_worldfile(picturefilename, quadcoords)

      return success



   def setgeoref(self, refsystem, points_list, utm_zoneletter=None, utm_zonenumber=None):
      '''
      Sets georeferencement of data set

      Parameters :

      :refsystem: Reference system, 'UTM', 'WGS84', ...

      :points_list: list of points tu use for the georeferencement, [[num1, lat1, lon1, x1, y1], ..., [numN, latN, lonN, xN, yN]] 
      
      :utm_zoneletter: UTM Letter, E->X, None if not 'UTM' ref system

      :utm_zonenumber: UTM number, 1->60, None if not 'UTM' ref system

      Returns :

      :error: error number, 0 if no error, -1 if no enough points, -2 if dataset zone greater than points list zone

      '''

      return gengeopositioning.setgeoref(self, refsystem, points_list, utm_zoneletter, utm_zonenumber)
   


   def getquadcoords(self):
      '''
      Calculates the utm coordinates of the DataSet Image corners.

      Returns:

      :success: True if coordinates getted, False if not

      :bottomleft: utm coordinates of the bottom left corner

      :bottomright: utm coordinates of the bottom right corner

      :upright: utm coordinates of the up right corner

      :upleft: utm coordinates of the up left corner

      '''
      bottomleft = None
      bottomright = None
      upright = None
      upleft = None
      if (self.georef.active == True):
         bottomleft = GeoRefPoint()
         bottomright = GeoRefPoint()
         upright = GeoRefPoint()
         upleft = GeoRefPoint()
         bottomleft.utm_easting, bottomleft.utm_northing = self.data.easting_image[0][0], self.data.northing_image[0][0]
         bottomright.utm_easting, bottomright.utm_northing = self.data.easting_image[0][-1], self.data.northing_image[0][-1]
         upleft.utm_easting, upleft.utm_northing = self.data.easting_image[-1][0], self.data.northing_image[-1][0]
         upright.utm_easting, upright.utm_northing = self.data.easting_image[-1][-1], self.data.northing_image[-1][-1]

      return self.georef.active, [bottomleft, bottomright, upright, upleft]



   #---------------------------------------------------------------------------#
   # DataSet General Processing                                                #
   #---------------------------------------------------------------------------#
   def peakfilt(self, setmin=None, setmax=None, setmed=False, setnan=False, valfilt=False):
      '''
      To eliminate peaks from a DataSet Object.

      Parameters:

      :dataset: DataSet Object to eliminate peaks from

      :setmin: minimal threshold value

      :setmax: maximal threshold value

      :setmed: if set to True, then values beyond threshold are replaced by a median instead of the threshold value ; the median is computed ...TBD...

      :setnan: if set to True, then values beyond thresholds are replaced by nan instead of the threshold value

      Note: if both "setnan" and "setmed" are True at the same time, then "nan" prevails

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.peakfilt(self, setmin=setmin, setmax=setmax, setmed=setmed, setnan=setnan, valfilt=valfilt)



   def medianfilt(self, nx=3, ny=3, percent=0, gap=0, valfilt=False):
      '''
      To process a DataSet Object with a median filter

      Parameters:

      :dataset: Dataset Object to process

      :nx: filter size in x coordinate

      :ny: filter size in y coordinate

      :percent: deviation (in percents) from the median value (for absolute field measurements)

      :gap: deviation (in raw units) from the median value (for relative anomaly measurements)

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.medianfilt(self, nx=nx, ny=ny, percent=percent, gap=gap, valfilt=valfilt)



   def festoonfilt(self, method='Crosscorr', shift=0, corrmin=0.4, uniformshift=True, valfilt=False):
      '''
      Filters festoon-like artefacts out of DataSet Object using
      correlation between profiles or provided shift.

      If no shift (0) is provided, the correlation map for
      each odd profile and the mean of its neighbours is computed and
      used to estimate the best shift. 

      Parameters:

      :dataset: DataSet Object to be filtered

      :method: correlation method to use (from festooncorrelation_getlist(): 'Crosscorr', 'Pearson', 'Spearman' or 'Kendall')

      :shift: shift value (in pixels) to apply ; if shift=0 the shift value will be determined for each profile by correlation with neighbours ; if shift is a vector each value in shift will be applied to its corresponding odd profile. In that case shift must have the same size as the number of odd profiles.  

      :corrmin: minimum correlation coefficient value for profile shifting [0-1].

      :uniformshift: if set to True, the shift is uniform on the map ; if set to False the shift is profile dependent.

      :valfilt: if set to True, then filters data.values instead of data.zimage

      Returns:

      :shift: shift value, modified if shift=0 in input parameter

      '''

      return genprocessing.festoonfilt(self, method=method, shift=shift, corrmin=corrmin, uniformshift=uniformshift, valfilt=valfilt)



   def destripecon(self, Nprof=0, setmin=None, setmax=None, method='additive', reference='mean', config='mono', valfilt=False):
      '''
      To destripe a DataSet Object by a constant (Moment Matching method).

      The statistical moments (mean and standard deviation) of each
      profile in the dataset are computed and matched to reference values.

      Parameters:

      :dataset: DataSet Object to be destriped

      :Nprof: number of profiles over which to compute the mean of reference ; if set to 0 (default), compute the mean over the whole data

      :setmin: while computing the mean, do not take into account data values lower than setmin

      :setmax: while computing the mean, do not take into account data values greater than setmax

      :method: if set to 'additive' (default), destriping is done additively ; if set to 'multiplicative', it is done multiplicatively

      :reference: if set to 'mean' (default), destriping is done using mean an standard deviation ; if set to 'median', it is done using median and interquartile range

      :config: if set to 'mono' (default), destriping is done using only offset matching (mean / median) ; if set to 'multi', it is done using both offset and gain (standard deviation/interquartile range)

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.destripecon(self, Nprof=Nprof, setmin=setmin, setmax=setmax, method=method, reference=reference, config=config, valfilt=valfilt)


   def destripecub(self, Nprof=0, setmin=None, setmax=None, Ndeg=3, valfilt=False):
      '''
      To destripe a DataSet Object by a cubic curvilinear regression (chi squared)

      Parameters:

      :dataset: DataSet Object to be destriped

      :Nprof: number of profiles over which to compute the polynomial reference ; if set to 0 (default), compute the mean over the whole data

      :setmin: while fitting the polynomial curve, do not take into account data values lower than setmin

      :setmax: while fitting the polynomail curve, do not take into account data values greater than setmax

      :Ndeg: polynomial degree of the curve to fit

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.destripecub(self, Nprof=Nprof, setmin=setmin, setmax=setmax, Ndeg=Ndeg, valfilt=valfilt)



   def regtrend(self, nx=3, ny=3, method='relative', component='local', valfilt=False):
      '''
      To filter a DataSet Object from its regional trend

      Parameters:

      :dataset: DataSet Object to be filtered

      :nx: filter size in x coordinate

      :ny: filter size in y coordinate

      :method: set to "relative" to filter by relative value (resistivity) or to "absolute" to filter by absolute value (magnetic field)

      :component: set to "local" to keep the local variations or to "regional" to keep regional variations

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.regtrend(self, nx=nx, ny=ny, method=method, component=component, valfilt=valfilt)



   def wallisfilt(self, nx=11, ny=11, targmean=125, targstdev=50, setgain=8, limitstdev=25, edgefactor=0.1, valfilt=False):
      r'''
      Applies a Wallis (contrast enhancement) filter to a DataSet Object.

      The Wallis filter is a locally adaptative contrast enhancement
      filter based on the local statistical properties of sub- window
      in the image.
      
      Parameters:

      :dataset: DataSet Object to be filtered

      :nx: filter window size in x coordinate

      :ny: filter window size in y coordinate

      :targmean: float, the target mean level (m_d)

      :targstdev: float, the target standard deviation (sigma_d)

      :setgain: float, amplification factor for contrast (A)

      :limitstdev: float, limitation on the window standard deviation to prevent too high gain value if data are dispersed

      :edgefactor: float {0..1} , brightness forcing factor (alpha), controls ratio of edge to background intensities.

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.wallisfilt(self, nx=nx, ny=ny, targmean=targmean, targstdev=targstdev, setgain=setgain, limitstdev=limitstdev, edgefactor=edgefactor, valfilt=valfilt)



   def ploughfilt(self, nx=3, ny=3, apod=0, angle=None, cutoff=None, valfilt=False):
      '''
      To apply anti-ploughing filter to a DataSet Object.

      ...To Be Developed...

      Parameters:

      :dataset: DataSet Object to be filtered

      :nx: filter size in x coordinate

      :ny: filter size in y coordinate

      :apod: apodisation factor (percent)

      :angle: ...TBD... float/degrees

      :cutoff: ...TBD... float/frequency

      :valfilt: if set to True, then filters data.values instead of data.zimage

      '''
      return genprocessing.ploughfilt(self, nx=nx, ny=ny, apod=apod, angle=angle, cutoff=cutoff, valfilt=valfilt)

    

   #---------------------------------------------------------------------------#
   # DataSet Magnetism Processing                                              #
   #---------------------------------------------------------------------------#
   def logtransform(self, multfactor=0):
      '''
      To transform the data in logarihtmics values

      Parameters:

      :dataset: DataSet Object to be treated

      :multfactor: multiply factor

      '''
      return magprocessing.logtransform(self, multfactor)



   def polereduction(self, apod=0, inclineangle=65, alphaangle=0):
      '''
      To do a reduction at the pole of DataSet Object

      Parameters:

      :apod: apodisation factor, to limit side effects

      :inclineangle: magnetic field incline

      :alphaangle: magnetic field alpha angle

      '''
      return magprocessing.polereduction(self, apod, inclineangle, alphaangle)



   def continuation(self, prosptech, apod=0, downsensoraltitude=0.3, upsensoraltitude=1.0, continuationflag=False, continuationvalue=0.0):
      '''
      Continuation of the magnetic field

      Parameters :

      :prosptech: Prospection technical

      :apod: apodisation factor, to limit side effects

      :downsensoraltitude: Altitude of the down magnetic sensor

      :upsensoraltitude: Altitude of the upper magnetic sensor

      :continuationflag: Continuation flag, False if not continuation

      :continuationaltitude: Continuation altitude, greater than 0 if upper earth ground, lower than 0 else

      '''
      return magprocessing.continuation(self, prosptech, apod, downsensoraltitude, upsensoraltitude, continuationflag, continuationvalue)



   def eulerdeconvolution(self, xmin, xmax, ymin, ymax, apod=0, nflag=False, nvalue=0):
      '''
      To calculate the euler deconvolution

      Parameters :

      :xmin: minimal x value of the zone treated

      :xmax: maximal x value of the zone treated

      :ymin: minimal y value of the zone treated

      :ymax: maximal y value of the zone treated

      :apod: apodisation factor, to limit side effects

      :nflag: structural index flag, False is not selected

      :nvalue: structural index value, 0 if automatic calcultation, 1 for a sheet-like body, 2 for a circular section cylinder, 3 for a sphere

      Returns : x, y, depth

      :nvalue: structural index value, calculated if 0 in input, or else, the same than in input

      :x: x value of the point where the depth has been estimated.

      :y: y value of the point where the depth has been estimated.

      :depth: depth estimated.

      :xnearestmin: minimal x value of the zone treated found in the array

      :xnearestmax: maximal x value of the zone treated found in the array

      :ynearestmin: minimal y value of the zone treated found in the array

      :ynearestmax: maximal y value of the zone treated found in the array

      '''
      return magprocessing.eulerdeconvolution(self, xmin, xmax, ymin, ymax, apod, nflag, nvalue)



   def analyticsignal(self, apod=0):
      '''
      Analytic signal conversion

      Parameters :

      :apod: apodisation factor, to limit side effects

      '''
      return magprocessing.analyticsignal(self, apod)


   def gradmagfieldconversion(self, prosptechused, prosptechsim, apod=0, downsensoraltused = 0.3, upsensoraltused = 1.0, downsensoraltsim = 0.3, upsensoraltsim = 1.0, inclineangle = 65, alphaangle = 0):
      '''
      Conversion between gradient and magnetic field values

      Parameters :

      :prosptechused: Prospection technical used

      :prosptechsim: Prospection technical simulated

      :apod: apodisation factor, to limit side effects

      :downsensoraltused: Altitude of the down magnetic sensor used

      :upsensoraltused: Altitude of the upper magnetic sensor used

      :downsensoraltsim: Altitude of the down magnetic sensor simulated

      :upsensoraltsim: Altitude of the upper magnetic sensor simulated

      :inclineangle: magnetic field incline

      :alphaangle: magnetic field alpha angle

      '''
      return magprocessing.gradmagfieldconversion(self, prosptechused, prosptechsim, apod, downsensoraltused, upsensoraltused, downsensoraltsim, upsensoraltsim, inclineangle, alphaangle)



   def susceptibility(self, prosptech, apod=0, downsensoraltitude = 0.3, upsensoraltitude = 1.0, calculationdepth=.0, stratumthickness=1.0, inclineangle = 65, alphaangle = 0):
      '''
      Calcultation of an equivalent stratum of magnetic susceptibility

      Parameters :

      :prosptech: Prospection technical

      :apod: apodisation factor, to limit side effects

      :downsensoraltitude: Altitude of the down magnetic sensor

      :upsensoraltitude: Altitude of the upper magnetic sensor

      :calculationdepth: Depth(m) to do the calculation

      :stratumthickness: Thickness of the equivalent stratim

      :inclineangle: magnetic field incline

      :alphaangle: magnetic field alpha angle


      '''
      return magprocessing.susceptibility(self, prosptech, apod, downsensoraltitude, upsensoraltitude, calculationdepth, stratumthickness, inclineangle, alphaangle)





#===========================================================================#



#---------------------------------------------------------------------------#
# General DataSet Environment functions                                     #
#---------------------------------------------------------------------------#
format_chooser = {
   ".dat" : "ascii",
   ".txt" : "ascii",
   ".nc"  : "netcdf",
   ".cdf" : "netcdf",
   ".pga" : "wumap",
   ".grd" : "surfer",
   ".mat" : "matrix",
   ".app" : "profile",
   ".rt"  : "electric",
}



def getlinesfrom_file(filename, fileformat=None, delimiter='\t', skipinitialspace=True, skiprowsnb=0, rowsnb=1):
   '''
   Reads lines in a file.

   Parameters :

   :fileformat: file format

   :filename: file name with extension to read, "test.dat" for example.

   :delimiter: delimiter between fields, tabulation by default.

   :skipinitialspace: if True, considers severals delimiters as only one : "\t\t" as '\t'.

   :skiprowsnb: number of rows to skip to get lines.

   :rowsnb: number of the rows to read, 1 by default.

   Returns:

   :colsnb: number of columns in all rows, 0 if rows have different number of columns

   :rows: rows.

   '''
   # Dispatch method ##############################################
   class From():
      @staticmethod
      def ascii():
         return iofiles.getlinesfrom_ascii(filename, delimiter, skipinitialspace, skiprowsnb, rowsnb)
      @staticmethod
      def netcdf():
         return iofiles.getlinesfrom_netcdf(filename)

   # Choose the input file format #################################
   if (fileformat == None):
      # ...TBD... Determine the format from file header
      pass

   if (fileformat == None):
      # Determine the format from filename extension
      file_extension = os.path.splitext(filenameslist[0])[1]
      fileformat = format_chooser.get(file_extension, None)

   # Read the dataset from input file #############################
   if (fileformat in fileformat_getlist()):
      readfile = getattr(From, fileformat)
      return readfile()
   else:
      # Undefined file format #####################################
      # ...TBD... raise an error here !
      return None, None



def fileformat_getlist():
   '''
   Get list of format files availables

   Returns: list of file formats availables, ['ascii', ...]

   '''
   return iofiles.fileformat_getlist()



def pictureformat_getlist():
   '''
   Get list of pictures format availables

   Returns: list of picture formats availables, ['jpg', 'png', ...]

   '''
   return plot.getpictureformatlist()



def rasterformat_getlist():
   '''
   Get list of raster format files availables

   Returns : list of raster file formats availables, ['jpg', 'png', ...]

   '''
   return raster.getrasterformatlist()



def plottype_getlist():
   '''
   Get list of plot type availables

   Returns : list of plot type availables, ['2D_SURFACE', '2D_CONTOUR', ...]

   '''
   return plot.gettypelist()



def festooncorrelation_getlist():
   '''
   To get the list of available festoon correlation methods.

   '''
   return genprocessing.getfestooncorrelationlist()


def destriping_getlist():
   '''
   To get the list of available destriping methods.

   '''
   return genprocessing.getdestripinglist()


def destripingreference_getlist():
   '''
   To get the list of available destriping reference calculation methods.

   '''
   return genprocessing.getdestripingreferencelist()


def destripingconfig_getlist():
   '''
   To get the list of available destriping configuration.

   '''
   return genprocessing.getdestripingconfiglist()


def regtrendmethod_getlist():
   '''
   To get the list of available destriping methods.

   '''
   return genprocessing.getregtrendmethodlist()



def regtrendcomp_getlist():
   '''
   To get the list of available destriping methods.

   '''
   return genprocessing.getregtrendcomplist()



def griddinginterpolation_getlist():
   '''
   To get the list of available gridding interpolation methods.

   '''
   return genoperation.getgriddinginterpolationlist()



def interpolation_getlist():
   '''
   Get list of interpolation methods availables

   Returns : list of interpolation methods availables, ['bilinear', 'bicubic', ...]

   '''
   return plot.getinterpolationlist()



def prosptech_getlist():
   '''
   Get list of prospection technicals availables

   Returns : list of prospection technicals

   '''
   return magprocessing.getprosptechlist()



def colormap_getlist():
   '''
   Getting the colormap list.

   Returns : list of colormap availables, ['gray', ...]

   '''
   return colormap.getlist()


def colormap_icon_getpath():
   '''
   Getting the colormap icons path.

   Returns : path of availables colormap icon '**\plotting\colormapicons'

   '''
   return colormap.get_icon_path()


def colormap_icon_getlist():
   '''
   Getting the colormap icons list.

   Returns : list of availables colormap icon, ['gray_colormap_icon.jpg', ...]

   '''
   return colormap.get_icon_list()


def colormap_plot(cmname, creversed=None, fig=None, filename=None, dpi=None, transparent=False):
   '''
   Plots the colormap.

   Parameters :

   :cmname: Name of the colormap, 'gray_r' for example.

   :creversed: True to add '_r' at the cmname to reverse the color map

   :fig: figure to plot, None by default to create a new figure.

   :filename: Name of the color map file to save, None if no file to save.

   :dpi: 'dot per inch' definition of the picture file if filename != None

   :transparent: True to manage the transparency.

   Returns:

   :fig: Figure Object

   '''
   return colormap.plot(cmname, creversed, fig, filename, dpi, transparent)



def correlmap(dataset, method):
   '''
   Computes the correlation map from DataSet Object:
      * each odd profile in the dataset is incrementally shifted and the correlation coefficient computed against neighbouring profiles for each shift value
      * profiles are considered to be vertical, and the shift performed along the profile (hence vertically)
      * the correlation map size is then "twice the image vertical size" (shift may vary from -ymax to +ymax) by "number of profiles" (correlation is computed for each column listed in input)

   Parameters:

   :dataset: DataSet Object containing the Z-image to be correl-mapped

   :method: correlation method to use (from festooncorrelation_getlist())

   Returns:

   :cor1: correlation map (shape = (2*zimg.shape[0]-1 , cols.size))

   :pva1: weight map (see correlation functions description)

   '''
   return genprocessing.correlmap(dataset, method)



def correlshift(correlmap, pva1, corrmin=None, apod=None, output=None):
   '''
   To compute the best shift to re-align festooned profiles

   Parameters:

   :correlmap: correlation map (shape = (2*zimg.shape[0]-1 , cols.size))

   :pva1: weight map (see correlation functions description)

   :corrmin: minimum correlation value for profile shifting [0-1]

   :apod: apodisation threshold (in percent of the max correl coef)

   :output: correlation profile computed as a weighted mean across the correlation map ; the best shift value is found at this profile's maximum

   Returns:

   :shift: number of pixels to shift along the profile

   '''
   return genprocessing.correlshift(correlmap, pva1, corrmin=corrmin, apod=apod, output=output)


def wallisoperator(cval, winval, setgain, targmean, targstdev, limitstdev, edgefactor):
    '''
    Computes the Wallis operator (brigthess contrast enhancement).  

    Parameters:

    :cval:  current window center value [f(x,y)]

    :winval: current window values

    :setgain: amplification factor for contrast [A]

    :targmean: target mean brightness level (typically between {0-255}) [m_d]

    :targstdev: target brightness standard deviation [\sigma_d]

    :limitstdev: maximal allowed window standard deviation (prevent infinitly high gain value if data are dispersed)

    :edgefactor: brightness forcing factor (controls ratio of edge to background intensities) [\alpha]

    Returns:
    
    :g_xy: Wallis operator at the current window center location [g(x,y)]
    
    '''
    return genprocessing.wallisoperator(cval, winval, setgain, targmean, targstdev, limitstdev, edgefactor)


def val_to_bright(val, nblvl=256, valmin=None, valmax=None):
    '''
    Convert data to brigthess level (grayscale).
    
    Parameters:

    :val: values to converted to brigthess level

    :nblvl: number of level

    :valmin: minimum value to consider for level definition, if None the values minimum is used
    
    :valmax: maximum value to consider for level definition, if None the values mmaximum is used

    Returns:
    
    :lvl: brigthess level image (from 0to nblvl-1)
    
    '''
    return genprocessing.val_to_bright(val, nblvl=nblvl, valmin=valmin, valmax=valmax)


def bright_to_val(lvl, valmin, valmax, nblvl=256):
    '''
    Convert brigthess level (grayscale) back to data.

    Parameters:

    :lvl: brigthess level image (from 0 to nblvl-1)

    :valmin: minimum value to consider for value recovering
    
    :valmax: maximum value to consider for value recovering

    :nblvl: number of level to consider for value recovering

    Returns:
    
    :val: converted back values

    '''
    return genprocessing.bright_to_val(lvl, valmin, valmax, nblvl=nblvl)



help_path = os.path.join(os.path.dirname(__file__), 'help')
htmlhelp_filename = os.path.abspath(os.path.join(help_path, 'html', 'index.html'))
pdfhelp_filename = os.path.abspath(os.path.join(help_path, 'pdf', 'GeophPy.pdf'))



def getgeophpyhelp(viewer='none', type='html'):
   '''
   To get help documentation of GeophPy module

   Parameters:

   :type: type of help needed, 'html' or 'pdf'.

   Returns:

   :helpcommand: application to start followed by pathname and filename of the 'html' or 'pdf' help document.

   '''

   if (type == 'pdf'):
      pathfilename = pdfhelp_filename
   else :
      pathfilename = htmlhelp_filename

   if (viewer == 'none'):           # start automatically the best application 
       helpcommand = pathfilename
   else :
       helpcommand = viewer + " " + pathfilename
   return helpcommand
