==================================================================
GeophPy: Tools for sub-surface geophysical survey data processing
==================================================================

.. module:: geophpy

About GeophPy
-------------

Introduction
~~~~~~~~~~~~~

The GeophPy project was initiated in 2014 through cooperation between two units of the CNRS [1]_ (`UMR5133-Archeorient`_ and `UMR7619-Metis`_).  
Since 2017, it is also developped by the LabCom Geo-Heritage (a cooperation between `UMR5133-Archeorient`_  and `Eveha International`_).
 
.. [1] French National Center for Scientific Research

.. _`UMR5133-Archeorient`: http://www.archeorient.mom.fr/recherche-et-activites/ressources-techniques/pole-2/
.. _`UMR7619-Metis`: https://www.metis.upmc.fr/
.. _`Eveha International`: http://eveha-international.com/

Description
~~~~~~~~~~~

GeophPy is an open-source python module which aims at building tools to display and process sub-surface geophysical data in the field of archaeology, geology, and other sub-surface applications.

The main feature of this module is to build a geophysical *DataSet Object* composed by series of data in the format (X,Y,Z) with (X,Y) being the point position of the geophysical value Z, in order to process and/or display maps of Z values.

This module is designed to be used in a graphical user interface software, WuMapPy, but can also be used independently in a script or in command line.
 

Features
~~~~~~~~

- Building a data set from one or severals data files.
- Displaying geophysical maps in 2D or 3D.
- Processing data sets with geophysicals methods and filters.
- Compatibility with Python 3.x


Main authors
~~~~~~~~~~~~

- **Lionel DARRAS**

  *French National Center for Scientific Research, UMR 5133 Archeorient, Lyon, France*
  
  lionel.darras@mom.fr

- **Philippe MARTY** 
  
  *French National Center for Scientific Research,  UMR 7619 METIS, Paris, France*

  philippe.marty@upmc.fr

- **Quentin VITALE**

  *Eveha International, Lyon, France*

  quentin.vitale@eveha.fr


Licence
~~~~~~~

GeophPy has been developped on licence GNU GPL v3.

https://www.gnu.org/licenses/gpl-3.0.en.html

Installation
------------

A Python (3.x) installation is necessary to install this package.

Installing GeophPy using pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can easily install GeophPy using pip. First, update pip to make sure you have the most recent version:

    >>>  pip install --upgrade pip

Then, install, upgrade or uninstall  GeophPy directly from the PyPI repository using :code:`pip` with these commands:

    >>>  pip install geophpy
    >>>  pip install --upgrade geophpy
    >>>  pip uninstall  geophpy

or from the downloaded zip file "GeophPy-vx.y" (from the downloaded zip folder):

    >>>  pip install GeophPy-vx.y.zip

Installing GeophPy manually from sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the zip file "GeophPy-vx.y" and unzip it.

Place yourself in the "GeophPy-vx.y" unzipped folder and install GeophPy with the following command:

    >>>  python setup.py install


.. note:: Installation on Windows

   GeophPy uses others Python modules. If the installation of one of these modules failed on Windows, you can install independently these modules using this useful web site: http://www.lfd.uci.edu/~gohlke/pythonlibs/

Dependencies
~~~~~~~~~~~~

GeophPy uses packages that should be automatically installed. If their installation failed they can be installed independently.

- numpy
- scipy
- matplotlib
- netCDF4
- Pillow
- PySide
- pyshp
- simplekml
- utm
- Sphinx 1.4.3 (or greater)

Command-line usage
------------------

    >>> from geophpy.dataset import *

Opening files
~~~~~~~~~~~~~

You can open files indicating the column number (1...n) of the data set to be processed:
    
    - ".dat" issued from Geometrics magnetometer G-858 (named 'ascii' format with ' ' as delimiter):

    >>> dataset = DataSet.from_file(["test.dat"], format='ascii',
    delimiter=' ')

    - or XYZ files (files with column titles on the first line, and data values on the others, with X and Y in the first two columns, and Z1,...,Zn in the following columns, separated by a delimiter '\t' ',' ';'...)

    >>> dataset = DataSet.from_file(["test.xyz"], format='ascii',
    delimiter='\t')

    XYZ file example:
        =====  =====  =====
    	X      Y      Z
        =====  =====  =====
	0      0      0.34
	0      1      -0.21
	0      2      2.45
        ...    ...    ...
        =====  =====  =====


You can easily obtain the list of the available file formats with the command:

    >>> list = fileformat_getlist()
    >>> print(list)
    ['ascii']

It is possible to build a data set from a concatenation of severals files of the same format:

    - To open several selected files:
    
    >>> dataset = DataSet.from_file(["abcde.dat","fghij.dat"],
                  format='ascii', delimiter=' ', z_colnum = 5)

    - To open all files ".dat" beginning by "file":

    >>> dataset = DataSet.from_file(["file*.dat"], format='ascii',
		  delimiter=' ', z_colnum = 5)


Checking files compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opening several files to build a data set needs to make sure that all files selected are in the same format.

It's possible to check it by reading the headers of each files:

    >>> compatibility = True
    >>> columns_nb = None
    >>> for file in fileslist :
    >>>    col_nb, rows = getlinesfrom_file(file)
    >>>    if ((columns_nb != None) and (col_nb != columns_nb)) :
    >>>        compatibility = False
    >>>        break
    >>>    else :
    >>>        columns_nb = col_nb


Data Set Object Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A data set contains 3 objects:

    - **info**
    - **data**
    - **georef**

The "info" object contains informations about the data set:

    - **x_min** = minimal x coordinate of the data set.
    - **x_max** = maximal x coordinate of the data set.
    - **y_min** = minimal y coordinate of the data set.
    - **y_max** = maximal y coordinate of the data set.
    - **z_min** = minimal z value of the data set.
    - **z_max** = maximal z value of the data set.
    - **x_gridding_delta** = delta between 2 x values in the interpolated image grid.
    - **y_gridding_delta** = delta between 2 y values in the interpolated image grid.
    - **gridding_interpolation** = interpolation name used for the building of the image grid.

The "data" object contains:

    - **fields** = names of the fields (columns): ['X', 'Y', 'Z']
    - **values** = 2D array of raw values before interpolating (array with (x, y, z) values): [[0, 0, 0.34], [0, 1, -0.21], [0, 2, 2.45], ...]
    - **z_image** = 2D array of current gridded z data values: [[z(x0,y0), z(x1,y0), z(x2,y0), ...], [z(x0,y1), z(x1,y1), z(x2,y1), ...], ...]

.. note::
    
   The z_image structure is not automatically built after opening file but by using gridding interpolation function ``dataset.interpolate()``. 
   See :ref:`DataSetOperation` for details.

The "georef" object contains:

    - **active** = True if contains georeferencing informations, False by default.
    - **pt1** = Point number 1 Coordinates, in local and utm referencing (local_x, local_y, utm_easting, utm_northing, utm_zonenumber, utm_zoneletter).    
    - **pt2** = Point number 2 Coordinates, in local and utm referencing (local_x, local_y, utm_easting, utm_northing, utm_zonenumber, utm_zoneletter).    


.. _DataSetOperation:

Data Set operation
~~~~~~~~~~~~~~~~~~

You can duplicate a data set before processing it to save the raw data:

    >>> rawdataset = dataset.copy()

After having opened a file, you can interpolate (or not) data, with severals gridding interpolation methods ('none', 'nearest', 'linear', 'cubic') to build z_image structure:

    >>> dataset.interpolate(interpolation="none")

After doing this operation, it's easy to see on a same plot the map and the plots (on a grid or not if no gridding interpolation is selected):

.. image:: _static/figCarto2.png
   :width: 50%
   :align: center


Data Set Processing
~~~~~~~~~~~~~~~~~~~

The dataset can be processed using the available processing techniques in a simple comand line of the form:

    >>> dataset.ProcessingTechnique(option1='True', option2='10',...)

The available processing techniques are listed below.

Peak filtering
++++++++++++++

Peak filtering allows data thresholding for values outside of the [**setmin**, **setmax**] interval.

Out of range data can be replaced by:

    - the interval bounds (**setmin** and **setmax**);
    - NaN values (if **setnan** is True),
    - the profiles' medians (if **setmed** is True).

.. |peak1| image:: _static/figPeakFilter1.png
   :height: 6cm
   :align: middle

.. |peakhist1| image:: _static/figPeakFilterHisto1.png
   :height: 6cm
   :align: middle

.. |peak2| image:: _static/figPeakFilter2.png
   :height: 6cm
   :align: middle

.. |peakhist2| image:: _static/figPeakFilterHisto2.png
   :height: 6cm
   :align: middle

.. |peak3| image:: _static/figPeakFilter3.png
   :height: 6cm
   :align: middle

.. |peakhist3| image:: _static/figPeakFilterHisto3.png
   :height: 6cm
   :align: middle

.. |peak4| image:: _static/figPeakFilter4.png
   :height: 6cm
   :align: middle

.. |peakhist4| image:: _static/figPeakFilterHisto4.png
   :height: 6cm
   :align: middle

Examples:
    
- replacing by lower and upper bounds:

    >>> dataset.peakfilt(setmin=-10, setmax=10)

+---------+-------------+
| |peak2| | |peakhist2| |
+---------+-------------+

- replacing by NaNs:

    >>> dataset.peakfilt(setmin=-10, setmax=10, setnan=True)

+---------+-------------+
| |peak3| | |peakhist3| |
+---------+-------------+

-  replacing by profile's median:

    >>> dataset.peakfilt(setmin=-10, setmax=10, setmed=True)

+---------+-------------+
| |peak4| | |peakhist4| |
+---------+-------------+

.. note:: Input parameters:

    - **setmin**: minimal threshold value, 
    - **setmax**: maximal threshold value, 
    - **setnan**: (if True) out of range data are replaced by nan,
    - **setmed**: (if True) out of range data are replaced by the profile's medians.

Median filtering
++++++++++++++++

"Median filtering is a non linear process useful in reducing impulsive, or salt-and-pepper noise" [LimJ90]_. 
It is capable of smoothing a few out of bounds pixels while preserving image's discontinuities without affecting the other pixels. 

.. |med1| image:: _static/figMedianFilter1.png
   :height: 6cm
   :align: middle

.. |med2| image:: _static/figMedianFilter2.png
   :height: 6cm
   :align: middle

.. |med3| image:: _static/figMedianFilter3.png
   :height: 6cm
   :align: middle


A window is slided along the image and the local median value is calculated. 
The window size (**nx**, **ny**) is a critical filter parameter and depens on every image. A trial and error approach is recommanded for choosing a suitable value. 

A threshold value can be set for the replacement by the local median value. 
The threshold deviation from the local median can be set:

- in percentage (**percent** =10) or raw units (**gap** =5),
- if no threshold is given, all pixels are replaced by their local medians.

Examples:

- No threshold:

    >>> dataset.medianfilt(nx=3, ny=3)

+--------+--------+
| |med1| | |med2| |
+--------+--------+

- Threshold (in raw value):

    >>> dataset.medianfilt(nx=3, ny=3, gap=5)

+--------+--------+
| |med1| | |med3| |
+--------+--------+

Principle:

For each pixel in the dataset, the local median of the (**nx** * **ny**) neighboring points is calculated. 

..  image:: _static/figMedianFilter.png
   :height: 5cm
   :align:  center

A threshold value is defined and if the deviation from the local median is higher than this threshold, then the center pixel value is replaced by the local median value. 
The threshold deviation from the local median can be defined as a percentage of the local median or directly in raw units.

.. note:: Input parameters:

    - **nx**: filter size in x coordinate, 
    - **ny**: filter size in y coordinate, 
    - **percent**: deviation (in percents) from the median value,
    - **gap**: deviation (in raw units) from the median value.


Festoon filtering
+++++++++++++++++

The festoon filter is a destagger filter that reduces the positionning error along the survey profiles that result in a festoon-like effect.
An optimum shift is estimated based on the correlation of a particular profile and the mean of its surrounding profiles.

This optimum shift can be:

- uniform throughout the map (**uniformshift** =True), 
- or different for each profile (**uniformshift** =False).

.. |fest1| image:: _static/figFestoonFilter1.png
   :height: 6cm
   :align: middle

.. |Fest2| image:: _static/figFestoonFilter02.png
   :height: 6cm
   :align: middle

.. |fest3| image:: _static/figFestoonFilter3.png
   :height: 6cm
   :align: middle

.. |fest4| image:: _static/figFestoonFilter4.png
   :height: 6cm
   :align: middle

.. |fest5| image:: _static/figFestoonFilter5.png
   :height: 6cm
   :align: middle

Examples:

- Uniform shift

    >>> dataset.festoonfilt(method='Crosscorr', uniformshift=True)

+---------+---------+
| |fest1| | |fest2| |
+---------+---------+


- Non uniform shift

    >>> dataset.festoonfilt(method='Crosscorr', uniformshift=False)

+---------+---------+
| |fest1| | |fest3| |
+---------+---------+

Principle:

For every odd profiles (columns) in the dataset, an optimum shift is estimated based on the correlation of the profile and the mean of its surrounding profiles. 
A correlation map is hence produced. 
This optimum shift can be uniform throughout the map (**uniformshift** =True) or different for each profile (**uniformshift** =False). 
If the shift is set uniform, the mean correlation profile is used as correlation map.

At the top and bottom edges of the correlation map (high shift values), high correlation values can arrise from low sample correlation calculation. 
To prevent those high correlation values to drag the best shift estimation, a limitation is set to only consider correlation with at least 50% overlap between profiles. 
Similarly, a minimum correlation value (**corrmin**) can be defined to prevent profile's shift if the correlation is too low.

    >>> fig = dataset.correlation_plotmap(method='Crosscorr')
    >>> fig.show() 
    >>> fig = dataset.correlation_plotsum(method='Crosscorr')
    >>> fig.show() 

+---------+---------+
| |fest4| | |fest5| | 
+---------+---------+

.. note:: Input parameters:

    - **method**: correlation method to use ('Crosscorr', 'Pearson', 'Spearman', 'Kendall'), 
    - **shift**: values (in pixels) to apply if known, 
    - **corrmin**: minimum correlation coefficient value for profile shifting [0-1],
    - **uniformshift**: flag for shift estimation.
    - **uniformshift**: (if True) the shift is set uniform on the map; (if False) the shift is profile dependent

Regional trend filtering
++++++++++++++++++++++++

Remove the background (or regional response) from a dataset to enhance the features of interest. 

Wallis filtering
++++++++++++++++

The Wallis filter is a locally adaptative contrast enhancement filter [STHH90]_. It is based on the local statistical properties of sub-window in the image.
It adjusts brightness values (grayscale image) in the local window so that the local mean and standard deviation match target values.

.. |wall1| image:: _static/figWallisFilter1.png
   :height: 6cm
   :align: middle

.. |wall2| image:: _static/figWallisFilter2.png
   :height: 6cm
   :align: middle

Examples:

    >>> dataset.wallisfilt()

+---------+---------+
| |wall1| | |wall2| |
+---------+---------+

Principle:

A window of size (**nx**, **ny**) is slided along the image and at each pixel the Wallis operator is calculated. 
The Wallis operator is defined as:

.. math::

   \frac{A \sigma_d}{A \sigma_{(x,y)} + \sigma_d} [f_{(x,y)} - m_{(x,y)}] + \alpha m_d + (1 - \alpha)m_{(x,y)}

where 
    - :math:`A` is the amplification factor for contrast, 
    - :math:`\sigma_d` is the target standard deviation, 
    - :math:`\sigma_{(x,y)}` is the standard deviation in the current window, 
    - :math:`f_{(x,y)}` is the center pixel of the current window, 
    - :math:`m_{(x,y)}` is the mean of the current window, 
    - :math:`\alpha` is the edge factor (controlling portion of the observed mean, and brightness locally to reduce or increase the total range), 
    - :math:`m_d` is the target mean.

As the Wallis filter is design for grayscale image, the data are internally converted to brightness level before applying the filter. 
The conversion is based on the minimum and maximum value in the dataset and uses 256 levels (from 0 to 255). 
The filtered brightness level are converted back to data afterwards.

A quite large window is recomanded to ensure algorithm stability.

.. note:: Input parameters:

    - **nx**: filter window size in x coordinate,
    - **ny**: filter window size in y coordinate,
    - **targmean**: target mean level (:math:`m_d`),
    - **targstdev**: target standard deviation level (:math:`\sigma_d`),
    - **setgain**: amplification factor for contrast (:math:`A`),
    - **limitstdev**: limitation on the window standard deviation in the window to prevent too high gain value when data are dispersed,
    - **edgefactor**: brightness forcing factor that controls ratio of edge to background intensities (:math:`\alpha`).


Plough filtering
++++++++++++++++

... To Be Developped ...


Constant destriping
+++++++++++++++++++

Remove from the dataset the strip noise effect arising from profile-to-profile differences in sensor height, orientation, drift or sensitivity (multi-sensors array).
Constant destriping is done using Moment Matching method [GaCs00]_.

.. |dest1| image:: _static/figDestriping1.png
   :height: 6cm
   :align: middle

.. |dest2| image:: _static/figDestriping2.png
   :height: 6cm
   :align: middle

.. |dest3| image:: _static/figDestriping3.png
   :height: 6cm
   :align: middle

.. |dest4| image:: _static/figDestriping4.png
   :height: 6cm
   :align: middle

Examples:

    >>> dataset.destripecon(Nprof=4, method='add')

+---------+---------+
| |dest1| | |dest2| |
+---------+---------+

Principle:

In constant destripping, a linear relationship is assumed between profile-to-profile offset (means) and gain (standard deviation).
The statistical moments (mean :math:`m_i` and standard deviation :math:`\sigma_i`) of each profile in the dataset are computed and matched to reference values. 

The reference values typically are:

- the mean (:math:`m_d`) and standard deviation (:math:`\sigma_d`) of the **Nprof** neighbouring profiles, 
- the mean and standard deviation of the global dataset (**Nprof** =0),
- alternatively, one can use the median and interquartile range instead of mean and standard deviation.


The data mean cross-track profile before and after destriping can be displayed as follow:

    >>> fig = dataset.destrip_plotmean(Nprof=4, method='add', Ndeg=None, plotflag='raw')
    >>> fig.show()
    >>> fig = dataset.destrip_plotmean(Nprof=4, method='add', Ndeg=None, plotflag='both')
    >>> fig.show()

+---------+---------+
| |dest3| | |dest4| |
+---------+---------+

Considering and additive relation (**method** ='add'), the destripped value can be expressed as ([RiJi06]_, [Scho07]_):

.. math::
   f_{corr} = \frac{\sigma_d}{\sigma_i}(f - m_i) + m_d

where
    - :math:`f_{corr}` is destripped value, 
    - :math:`\sigma_d` is the reference standard deviation, 
    - :math:`\sigma_i` is the current profile standard deviation, 
    - :math:`f` is the current value, 
    - :math:`m_i` is the current profile, 
    - :math:`m_d` is the reference mean.


Unlike remote sensing, ground surveys often demonstate profile-to-profile offsets but rarely gain changes so that only matching profiles mean (or median) is usually appropriate (**configuration** ='mono'):

.. math::
   f_{corr} = f - m_i + m_d

Finally, a multiplicative relation can be considered (**method** ='mult'), and the destripped value are hence expressed as: 

.. math::
   f_{corr} = f \frac{\sigma_d}{\sigma_i} \frac{m_d}{m_i}

.. note:: Input parameters:

    - **Nprof**: number of profiles for the reference moments computation (0= computes over the whole dataset),
    - **setmin**: do not take into account data values lower than setmin,
    - **setmax**: do not take into account data values greater than setmax,
    - **method**: 'additive' method for the destriping;  'multiplicative' method for the destriping,
    - **reference**: 'mean': references are mean and standard deviation; 'median': references are median and interquartile range,
    - **configuration**: 'mono' sensors: destriping with only offset matching; 'multi' sensors: destriping with both offset and gain.


Curve destriping
++++++++++++++++

Remove from the dataset the strip noise effect by fitting and subtracting a polynomial curve to each profile on the dataset.

Logarithmic transformation
++++++++++++++++++++++++++

The logarithmic transformation is contrast enhancement filter originally used for geological magnetic data. 
It enhances information present in magnetic data at low-amplitude values while preserving the relative amplitude information via logarithmic transformation procedure [MPBL01]_.

Principle:

Originally used for geological magnetic data, the logarithmic transformation principle can be summarized as follow:

- Contrast in magnetic susceptibility and magnetic remanence are the physical rock properties that controlls magnetic anomalies (the other controlling factors being the geometry and the position of the source body). 
- Magnetic mineral content variation and borehole magnetic susceptibility are know to be best represented by a log-normal distribution. 
- If a similar distribution is assumed to represent to represent lithologies on magnetic anomaly maps, then log transformation of the magnetic data should serve to normalize the distribution and highlight features having common amplitude.

The log-normal transformation of magnetic data :math:`f` is implemented like so:

.. math::
    f_{log} = \left\{
      \begin{array}{ccc}
          -\log_{10} (-f) & for & f <-1 \\
          \log_{10} (f) & for & f >1 \\
               0         & for & -1< f >1 \\
      \end{array}
   \right.
  
.. note:: Input parameters:

    - **multfactor**: multiplying factor of the data (x5, x10, x20, x100).


Pole reduction
++++++++++++++

The reduction to the magnetic pole is a way to facilitate magnetic data interpretation and comparizon.
The reduction to the pole calculates the anomaly that would have been obtained if the survey had been done at the pole where the inclination of the magnetic field is maximum (vertical). [BLAK96]_ 

Principle: 

Due to the dipolar nature of the geomagnetic field, magnetic anomalies (if not located at the magnetic poles) are asymmetric with a geometry that depends on the magnetic inclination (:math:`I`). 
Assuming that the remanent magnetism of the source is small compared to the induced magnetism, the filter symmetrize the anomalies and palce them directly above the source.
It uses a fast Fourier series algorithm to work in the spectral (frequency) domain.
A similar processing (reduction to the equator) is used when data are recored at low magnetic inclinations.

.. image:: _static/figAnglesRepresentation.png
   :width: 50%
   :align: center

.. image:: _static/figWindowPoleReduction.png	
   :width: 50%
   :align: center

.. note:: Input parameters: 

    - **apod**: apodisation factor.
    - **inclineangle**: inclination angle (angle between the magnetic North and the magnetic field measured at the soil surface in the vertical plane).
    - **alphaangle**: angle between magnetic North and profiles direction in the horizontal plane.

Algorithm:

.. image:: _static/figAlgoPoleReduction.png	

u is the spatial frequency corresponding to the x-direction and v is the spatial frequency corresponding to the y-direction.

- Filling gaps:

To use the fast Fourier algorithm, the data set must not contains gaps or 'NaN' values (Not A Number).
If the data set grid is not interpolated and contains NaNs, the blancs will be automatically filled using profile by profile spline interpolation.

- Apodisation:

It is an operation to attenuate sides effects. The factor of apodisation (0, 5, 10, 15, 20 or 25%) precises the size to extend the data values zone. Values of this extension will be attenuated by a cosinus formula:
 
.. image:: _static/figApodisation.png	

After processing, the size of the data values zone will become the same than before this apodisation.


Continuation
++++++++++++

The downward continuation is a solution to reduce spread of anomalies and to correct coalescences calculating the anomaly if measures would be done at a lower level.
The upward continuation allows to smooth data. [BLAK96]_

.. image:: _static/figWindowContinuation.png	
   :width: 50%
   :align: center

.. note:: Input parameters: 

     - **apod**: factor of apodisation(%).
     - **prosptech**: Survey configuration ("Magnetic field", "Magnetic field gradient", "Vertical component gradient").
     - **downsensoraltitude, upsensoraltitude**: Sensors altitudes relatives to th soil surface.
     - **continuationflag**: Continuation flag, False if not continuation
     - **continuationvalue**: Continuation altitude (greater than 0 if upper earth ground, lower than 0 otherwise).

Algorithm:

.. image:: _static/figAlgoContinuation.png	

The method of filling gaps or apodisation to reduce side effects are the sames than used in the pole reduction function.

 
High level processing functions
+++++++++++++++++++++++++++++++

The calling protocol of these functions is described in the end of this document (see :ref:`HighlevelAPI`) but about the detailed source code of is available in this section.

.. automodule:: geophpy.processing.general
    :members: peakfilt, medianfilt, festoonfilt, regtrend, wallisfilt, ploughfilt, destripecon, destripecub

.. automodule:: geophpy.processing.magnetism
    :members: logtransform, polereduction, continuation

.. automodule:: geophpy.operation.general
    :members: apodisation2d


DataSet Plotting
~~~~~~~~~~~~~~~~~

General Plot Information
++++++++++++++++++++++++

Plot type:

It is possible to plot the data set thanks to several plot types.

To see the plot types available , you can use:

    >>> list = plottype_getlist()
    >>> print(list)
    ['2D-SURFACE','2D-CONTOUR', '2D-CONTOURF']

Interpolation:

It is possible to plot the data set by choosing several interpolations for the surface display.

To get the plotting interpolations available , you must type:

    >>> list = interpolation_getlist()
    >>> print(list)
    ['nearest', 'bilinear', 'bicubic', 'spline16', 'sinc']

Color map:

To plot a data set, you have to choose a color map.

To see the color maps available, you type:

    >>> cmaplist = colormap_getlist(creversed=False)
    >>> print(cmaplist)
    ['Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'GnBu', 'Greens', 'Greys',
     'OrRd', 'Oranges', 'PRGn', 'PiYG', 'PuBu', 'PuOr', 'PuRd','Purples',
     'RdBu','RdGy','RdPu','RdYlBu', 'RdYlGn', 'Reds', 'Spectral', 'Wistia',
     'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn', 'binary',
     'bone', 'bwr', 'copper', 'gist_earth', 'gist_gray', 'gist_heat',
     'gist_yarg', 'gnuplot', 'gray', 'hot', 'hsv', 'jet', 'ocean', 'pink',
     'spectral', 'terrain']


Using the parameter creversed=True, you obtain the same number of color maps but with reversed colors, with a "_r" extension:

    >>> for i in range (cmapnb):
    >>>     colormap_plot(cmaplist[i-1], filename="CMAP_" +
            str(i) + ".png")

Examples:

.. image:: _static/figColorMap_1.png	
.. image:: _static/figColorMap_2.png	
.. image:: _static/figColorMap_3.png	
.. image:: _static/figColorMap_4.png	
.. image:: _static/figColorMap_5.png	
.. image:: _static/figColorMap_6.png	

or you can build figure and plot objects to display them in a new window:

    >>> cm_fig = None
    >>> first_time = True
    >>> for cmapname in cmaplist:
    >>>     cm_fig = colormap_plot(cmapname, fig=cm_fig)
    >>>     if (first_time == True):
    >>>         fig.show()
    >>>         first_time = False
    >>>     fig.draw()

Histogram
+++++++++

To adjust the limits of color map you must view the limits of the data set:

    >>> zmin, zmax = dataset.histo_getlimits()

You can also plot the histogram curve:

    >>> dataset.histo_plot("histo.png", zmin, zmax, dpi=100,
        transparent=True)

to obtain:

.. image:: _static/figHisto.png
   :width: 50%
   :align: center

or you can build figure and plot objects to display them in a window:

    >>> h_fig = dataset.histo_plot()


Correlation map
+++++++++++++++

You can plot the correlation map of a dataset:

    >>> dataset.correlation_plotmap("corrmap.png", dpi=100, transparent=True)

to obtain:

.. image:: _static/figCorrelationMap.png
   :width: 50%
   :align: center

or you can build figure and plot objects to display them in a window:

    >>> h_fig = dataset.histo_plot()


Correlation sums
++++++++++++++++

You can plot the correlation sums of a dataset:

    >>> dataset.correlation_plotsum("corrsum.png", dpi=100, transparent=True)

to obtain:

.. image:: _static/figCorrelationSum.png
   :width: 50%
   :align: center

Mean cross-track profile
++++++++++++++++++++++++

Before and after destriping mean cross-track profiles can be displayed with the following commands:

    >>> fig = dataset.destrip_plotmean(Nprof=4, method='add', Ndeg=None, plotflag='raw')
    >>> fig.show()
    >>> fig = dataset.destrip_plotmean(Nprof=4, method='add', Ndeg=None, plotflag='both')
    >>> fig.show()

+---------+---------+
| |dest3| | |dest4| |
+---------+---------+

Map plotting
++++++++++++

You can plot a data set using one of these plot types:

    >>> dataset.plot('2D-SURFACE', 'gray_r', plot.png,
        interpolation='bilinear', transparent=True, dpi=400)

Examples:

Different plot types ('2D-SURFACE', '2D-CONTOUR', '2D-CONTOURF'):

'2D-SURFACE':

.. image:: _static/figCarto1.png
   :width: 50%
   :align: center

'2D-CONTOUR':

.. image:: _static/figCarto3.png
   :width: 50%
   :align: center

Different interpolations for a "2D-SURFACE" plot type ('bilinear', 'bicubic'):

With 'bilinear' interpolation:

.. image:: _static/figCarto4.png
   :width: 50%
   :align: center

With 'bicubic' interpolation:

.. image:: _static/figCarto5.png
   :width: 50%
   :align: center

It is possible not to display the color map and axis to import the picture in a SIG software.

High level plotting functions
+++++++++++++++++++++++++++++++

The calling protocol of these functions is described in the end of this document (see :ref:`HighlevelAPI`) but about the detailed source code of is available in this section.

.. automodule:: geophpy.plotting.histo
    :members:

.. automodule:: geophpy.plotting.correlation
    :members:


.. automodule:: geophpy.plotting.destrip
    :members:

.. automodule:: geophpy.plotting.plot
    :members: plot

DataSet Saving
~~~~~~~~~~~~~~~

You can save the data set in a file.

For the time being, it's only possible to save data in xyz files as it's described above:

    >>> dataset.to_file(save.csv, format='xyz')


Geographic Positioning Set
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can open a file containing the geographic coordinates of the geophysical survey corresponding you *DataSet* object. you can use 

- an ascii file (*.csv* for instance):

  The first line must contain the geographic reference system and the other lines contain the point number followed by its GPS coordinates (longitude and lattitude or UTM Easting and Northing):

    >>> WGS84		
    >>> 1	66.84617533	37.74956917
    >>> 2	66.84649517	37.7489535
    >>> 3	66.8472475	37.74972867
    >>> 4	66.84689417	37.7491385
    >>> 5	66.84691867	37.7491025
    >>> ...     ...             ...
  
  The file can also contain the corresponding local coordinates:

    >>> UTM
    >>> 1	745038.191	4656005.727	150	0	
    >>> 2	745068.172	4656045.663	150	50	
    >>> 3	745028.43	4656076.057	100	50	
    >>> 4	744988.466	4656105.978	50	50	
    >>> 5	744998.428	4656036.093	100	0	
    >>> ...	...		...		...	...

- or a shapefile (*.shp*). 


To open your Geographic Positioning Set file simply use:

    >>> from geoposset import *
    >>> gpset = GeoPosSet.from_file(refsys='WGS84', type='shapefile',
	["pt_topo"])	

You can get so the numbers and list of points:

    >>> list = gpset.points_getlist()
    >>> print(list)
    >>> [[0, 32.52, 34.70], [1, 32.52, 34.70]]	#with [num, x or lon, y or lat]

You can plot them:

    >>> fig = gpset.plot()
    >>> fig.show()

.. image:: _static/figGps1.png
   :width: 50%
   :align: center

And converting a shapefile in a kml file:

    >>> gpset.to_kml("shapefile.kml")

to view the points, lines, and surfaces described in the shapefile, on google earth:

.. image:: _static/figGps2.png
   :width: 50%
   :align: center

It's possible to save theses points into an ascii file (.csv) composed by:

    Line 1: "'WGS84'", or "'UTM', utm_zoneletter, utm_zonenumber"

    Others lines: point_number; longitude; latitude; X; Y 

Example:

    WGS84
    0;32.52432754649924;34.70609241062902;0.0;0.0
    1;32.52387864354049;34.70625596577242;45.0;0.0
    2;32.52365816268757;34.70584594601077;45.0;50.0
    3;32.52343735426504;34.70543469612403;;		# (X=None, Y=None) => point not referenced in local positioning


It is possible to georeference a data set with at less 4 points.

With the data set georeferenced, it is possible to export the data set in a kml file:

    >>> dataset.to_kml('2D-SURFACE', 'gray_r', "prospection.kml",
	cmmin=-10, cmmax=10, dpi=600)

.. image:: _static/figGeoref1.png
   :width: 50%
   :align: center

Exporting the data set as a raster in a SIG application (as ArcGis, QGis, Grass, ...) is possible with severals picture file format ('jpg', 'png', 'tiff'):

    >>> dataset.to_raster('2D-SURFACE', 'gray_r', "prospection.png",
	cmmin=-10, cmmax=10, dpi=600)

.. image:: _static/figGeoref2.png
   :width: 50%
   :align: center

A world file containing positioning informations of the raster is created ('jgw' for JPG, 'pgw' dor.png, and 'tfw' for TIFF picture format) with:

    Line 1: A: pixel size in the x-direction in map units/pixel

    Line 2: D: rotation about y-axis

    Line 3: B: rotation about x-axis

    Line 4: E: pixel size in the y-direction in map units, almost always negative[3]

    Line 5: C: x-coordinate of the center of the upper left pixel

    Line 6: F: y-coordinate of the center of the upper left pixel

Example:

    0.0062202177595

    -0.0190627320737

    0.0131914192417

    0.00860610262817

    660197.8178

    3599813.97056

Using a Graphic User Interface
-------------------------------

The name of the "Graphic User Interface" used has to be mentionned in the "matplotlibrc" file:

to use QT4 GUI:

    backend      : Qt4Agg		

Note: to use QtAgg with PySide module, add:

    backend.qt4  : PySide

or to use Tkinter GUI:

    backend      : TkAgg

.. note:: 

 - in Windows environment, this file is in the "C:\\PythonXY\\Lib\\site-packages\\matplotlib\\mpl-data" directory.

 - in Linux environment, this file is in the "/etc" directory.

With QT4Agg GUI, you can plot data in a windows:

    >>> from geophpy.dataset import *
    >>> success, dataset = DataSet.from_file("DE11.dat", delimiter=' ',
        z_colnum=5)
    >>> if (success = True):
    >>>    fig, cmap = dataset.plot('2D-SURFACE', 'gist_rainbow',
           dpi=600, axisdisplay=True, cmapdisplay=True, cmmin=-10, cmmax=10)
    >>>    fig.show()

to obtain:

.. image:: _static/figGraphUserInterface.png
    :width: 50%
    :align: center

You can also plot data in a windows with several color maps:

    >>> from geophpy.dataset import *
    >>>			# to get the list of color maps availables
    >>> list = colormap_getlist()	
    >>> first = True				# first plot
    >>> fig = None				# no previous figure
    >>> cmap = None				# no previous color map
    >>> success, dataset = DataSet.from_file("DE11.dat", delimiter=' ',
        z_colnum=5)
    >>> if (success == True):			# if file opened
    >>>			# for each color map name in the list
    >>>    for colormapname in list :		
    >>>        fig, cmap = dataset.plot('2D-SURFACE', 'gist_rainbow',
               dpi=600, axisdisplay=True, cmapdisplay=True, cmmin=-10,
               cmmax=10)
    >>>        if (first == True):		# if first plot
    >>>           fig.show()			# displays figure windows
    >>>           first = False			# one time only
    >>>			# updates the plot in the figure windows
    >>>        p.draw()				
    >>>			# removes it to display the next
    >>>        cmap.remove()		
    >>>			# waits 3 seconds before display the plot
    >>>			# with the next color map
    >>>        time.sleep(3)			

.. _HighlevelAPI:

High level API
--------------

.. automodule:: geophpy.dataset
    :members: getlinesfrom_file, fileformat_getlist, plottype_getlist, interpolation_getlist, colormap_getlist, colormap_plot, pictureformat_getlist, rasterformat_getlist, correlmap, griddinginterpolation_getlist, festooncorrelation_getlist

.. autoclass:: geophpy.dataset.DataSet
    :members: from_file, to_file, plot, histo_plot, histo_getlimits, copy, peakfilt, medianfilt, festoonfilt, regtrend, wallisfilt, ploughfilt, destripecon, destripecub, polereduction, logtransform, continuation


Feedback & Contribute
---------------------

Your feedback is more than welcome.

Write email to lionel.darras@mom.fr, philippe.marty@upmc.fr or quentin.vitale@eveha.fr

To cite this software : "Marty, P., Darras, L. (2015). GeophPy. Tools for geophysical survey data processing (version x.y) [software]. Available at https://pypi.python.org/pypi/GeophPy."

.. include:: ../CHANGES.rst

.. only:: html

   .. rubric:: References


.. [BLAK96] `Blakely R. J. 1996. Potential Theory in Gravity and Magnetic Applications. Cambridge University Press. <http://www.cambridge.org/fr/academic/subjects/earth-and-environmental-science/solid-earth-geophysics/potential-theory-gravity-and-magnetic-applications?format=PB#25tAoM8i3wDlJZXW.97>`_
.. [GaCs00] `Gadallah F. L., Csillag F. 2000. Destriping multisensor imagery with moment matching. Int. J. Remote Sensing, vol. 21, no. 12, p2505-2511. <http://www.tandfonline.com/doi/abs/10.1080/01431160050030592>`_
.. [LimJ90] Lim, J. S. 1990. Two-Dimensional Signal and Image Processing. p469-476. Prentice-Hall.
.. [MPBL01] `Morris B., Pozza M., Boyce J. and Leblanc G. 2001. Enhancement of magnetic data by logarithmic transformation. The Leading Edge, vol. 20, no. 8, p882-885. <http://library.seg.org/doi/abs/10.1190/1.1487300>`_ 
.. [RiJi06] `Richards, J. A. and X. Jia 2006. Remote Sensing Digital Image Analysis - An Introduction, 4rth edition. Chapter 2.2.3 p37. Springer. <http://www.springer.com/fr/book/9783540297116>`_
.. [Scho07] `Schowengerdt R. A. .2007. Remote Sensing: Models and Methods for Image Processing, 3rd edition. Chapter 7.4 p325. Elsevier. <https://www.elsevier.com/books/remote-sensing/schowengerdt/978-0-12-369407-2>`_
.. [STHH90] `Scollar I., Tabbagh A., Hesse A. and Herzog I. 1990. Archaeological Prospecting and Remote Sensing (Topics in Remote Sensing 2). 647p. Cambridge University Press. <http://www.cambridge.org/fr/academic/subjects/earth-and-environmental-science/remote-sensing-and-gis/archaeological-prospecting-and-remote-sensing?format=PB#3Vt1cQBSO66mUr23.97>`_
