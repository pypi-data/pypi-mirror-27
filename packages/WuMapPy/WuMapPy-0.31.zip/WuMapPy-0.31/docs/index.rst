===================================================================================
WuMapPy : Graphic User Interface for sub-surface geophysical survey data processing
===================================================================================

.. module:: wumappy

About WuMapPy
-------------

Introduction
~~~~~~~~~~~~~

The WuMapPy project was initiated in 2014 through cooperation between two units of the CNRS [1]_ (`UMR5133-Archéorient`_ and `UMR7619-Metis`_).  
Since 2017, it is also developped by the LabCom Geo-Heritage (a cooperation between `UMR5133-Archéorient`_  and `Eveha International`_).
 
.. [1] French National Center for Scientific Research

.. _`UMR5133-Archéorient`: http://www.archeorient.mom.fr/recherche-et-activites/ressources-techniques/pole-2/
.. _`UMR7619-Metis`: https://www.metis.upmc.fr/
.. _`Eveha International`: http://eveha-international.com/

Description
~~~~~~~~~~~

WuMapPy is a graphic user interface written in Python for friendly sub-surface geophysical survey data processing.
All displaying or processing operations are realized by an other Python module named GeophPy.

Features
~~~~~~~~

- Processing data sets with geophysical filters and technics.
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

WuMapPy has been developped on licence GNU GPL v3.

https://www.gnu.org/licenses/gpl-3.0.en.html

Installation
------------

A stand-alone version with an executable Windows installer is currently being developped but is not available yet.

For now, a Python (3.x) installation is necessary to install this package.

Installing WuMapPy using pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can easily install WuMapPy using pip. First, update pip to make sure you have the most recent version:

    >>>  pip install --upgrade pip

Then, you can install, upgrade or uninstall WuMapPy directly from the PyPI repository: using :code:`pip` with these commands:

    >>>  pip install wumappy
    >>>  pip install --upgrade wumappy
    >>>  pip uninstall wumappy

or from the downloaded the zip file "WuMapPy-vx.y" (from the the downloaded zip folder):

    >>>  pip install WuMapPy-vx.y.zip

Installing WuMapPy manually from sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the zip file "WuMapPy-vx.y" and unzip it.

Place yourself in the "WuMapPy-vx.y" unzipped folder and install WuMapPy with the following command:

    >>>  python setup.py install

.. note:: Installation on Windows

    WuMapPy and GeophPy are using others python modules. If the installation of one of these modules failed on windows, you can install independently thes modules using this useful web site : http://www.lfd.uci.edu/~gohlke/pythonlibs/

Dependencies
~~~~~~~~~~~~

WuMapPy is a GUI for the GeophPy module, it requires:

- geophpy
- PySide

GeophPy uses packages that should be automatically installed. If their installation failed they can be installed independently:

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

Graphical User Interface Overview
---------------------------------

Introduction
~~~~~~~~~~~~

The WuMapPy Graphic User Interface is developped using the ``PySide`` library. 

To launches the software type the ``wumappy`` as a command in any console

    >>>  wumappy

  usage: wumappy


Main Window
~~~~~~~~~~~

From the main window you can acces the :ref:`FilesMenu`, :ref:`SettingsMenu` and :ref:`HelpMenu` menus. From there you can:

 - Open previously processed data or :ref:`DataFromAscii` new data.
 - Import or :ref:`OpenGeoposSet` files.
 - Change :ref:`lang`, :ref:`font` and others :ref:`misc`.
 - Acces the GUI :ref:`HelpMenu` and documentation.

.. image:: _static/figMainWindow.png

Data Set Window
~~~~~~~~~~~~~~~

.. |dataset| image:: _static/figDataSetWindow.png
   :height: 10cm
   :align: middle

Once opened, a DataSet is displayed in a window with a menubar that contains the different available options:

- :ref:`DataWinFilespMenu` (save and export the data)
- :ref:`DataWinProcessMenu` (general processings)
- :ref:`DataWinMagMenu`
- :ref:`DataWinGeorefMenu` (available if a Geographic Positions Set is open/imported)
- :ref:`misc`

+-----------+
| |dataset| |
+-----------+

Geographic Positions Set Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once opened, a Geographics Positions Set is displayed in a window with a menubar that contains the different available options:

- :ref:`GeoPosWinFilesMenu` (save and export)
- :ref:`GeoPosWinConfigMenu`

.. image:: _static/figGeoPosSetWindow.png

Main Window
-----------

:ref:`FilesMenu` | :ref:`SettingsMenu` | :ref:`HelpMenu`

.. image:: _static/figMainWindow.png

.. _FilesMenu:

Files
~~~~~

From this menu you can: 

- Open a Data Set file (*.netcdf*).
- Import data from an (X,Y,Z) ascii files. 
- Open a Geographic Positions Set (*.netcdf*).
- Import a shapefile (*.shp*).

.. |file1| image:: _static/figMainWindowFilesMenu.png
   :width: 4cm
   :align: middle

+---------+
| |file1| | 
+---------+

.. _DataFromAscii:

Import from ascii file
++++++++++++++++++++++

You can display and pre-process the data or look at the data histogram directly from this menu thanks to the different available tabs. 

he *Update* button allows you to preview the effect of the filter before an actual validation when the *real time update* option is switched off.

.. |open0| image:: _static/figOpenDataSetDlgBox0.png
   :height: 8cm
   :align: middle

+---------+
| |open0| | 
+---------+

.. |open1| image:: _static/figOpenDataSetDlgBox1.png
   :height: 6cm
   :align: middle

.. |open2| image:: _static/figOpenDataSetDlgBox2.png
   :height: 6cm
   :align: middle

.. |open3| image:: _static/figOpenDataSetDlgBox3.png
   :height: 6cm
   :align: middle

.. |open4| image:: _static/figOpenDataSetDlgBox4.png
   :height: 6cm
   :align: middle

.. |open5| image:: _static/figOpenDataSetDlgBox5.png
   :height: 6cm
   :align: middle

.. |open6| image:: _static/figOpenDataSetDlgBox6.png
   :height: 6cm
   :align: middle

- File format, Gridding options and Festoon filter tabs.

+---------+---------+
| |open1| | |open2| |
+---------+---------+

- Display options and Median filter options tabs.

+---------+---------+
| |open3| | |open4| |
+---------+---------+

- Histogram and dataset Display tab.

+---------+---------+
| |open5| | |open6| |
+---------+---------+

.. _OpenGeoposSet:

Open Geoposition Set
++++++++++++++++++++++

.. image:: _static/figOpenGeoPosSet1DlgBox.png

(for more informations, cf. GeophPy documentation)

.. _SettingsMenu:

Settings
~~~~~~~~

From this menu you can change the entire GUI :ref:`lang`, :ref:`font` and others :ref:`misc`.

.. |set1| image:: _static/figMainWindowSettingsMenu.png
   :width: 4cm
   :align: middle

+--------+
| |set1| | 
+--------+

.. _lang:

Language
++++++++

The language descriptions are presents as *.lng* files in the *MAIN/wumappy/resources* directory where *MAIN* is the user home directory.
The default builtin language for the Graphic User Interface is English, and it's the only one generated by the code and saved as the *english.lng*. 
This file as the follwing format:

    >>> english
	FILES_ID	Files
	SETTINGS_ID	Settings
	FONT_ID		Font
	MISCSETTINGS_ID	Miscellaneous Settings
	HELP_ID		Help
	ABOUT_ID	About

The first line is the language name, the first column is object identifier (menu name, group box name etc.) and the second the displayed traduction. 

You can easily add and use an other language file: duplicate the *english.lng* file as *otherlanguage.lng*, change the language name in the first row and modify the second row with the correct translation in the new language.

The language files in the *MAIN/wumappy/resources* directory (like *french.lng* or *spanish.lng* etc.) are automatically detected by WuMapPy and become available languages in the *Settings/Language*:

.. |lang1| image:: _static/figLanguageSelectionDlgBox.png
   :width: 4cm
   :align: middle

+---------+
| |lang1| | 
+---------+

.. _font:

Font
++++

The font type and the font size used in the majority of the windows and dialog box can be modified selecting *Settings->Font* item.

.. |font1| image:: _static/figSelectFontDlgBox.png
   :height: 8cm
   :align: middle

+---------+
| |font1| | 
+---------+

.. _misc:

Miscellaneous settings
++++++++++++++++++++++

.. |misc1| image:: _static/figMiscellaneousSettingsDlgBox.png
   :width: 5cm
   :align: middle

.. |rt1| image:: _static/figDlgBoxButtonsWithoutRealTimeUpdate1.png
   :width: 5cm
   :align: middle

.. |gpb1| image:: _static/figGroupBoxDlgBox1.png
   :height: 6cm
   :align: middle

.. |gpb2| image:: _static/figGroupBoxDlgBox2.png
   :height: 6cm
   :align: middle

+---------+
| |misc1| | 
+---------+

With this dialog box, it is possible to

- Check/uncheck the flag of *Real time update* after a modification in a dialog box.
  
  If the flag is unchecked, an *Update* button will be displayed in the dialog box and the map *Rendering* tab will be updated only if this *Update* button is clicked.

+-------+
| |rt1| | 
+-------+

- Check/uncheck the flag of *Group Box Format* display style.

  If the flag is unchecked all dialogboxes' tabs will be displayed in the same windows.

  +--------+
  | |gpb1| | 
  +--------+

  If the flag is checked, optionds will be displayed in different tabs.

  +--------+
  | |gpb2| |
  +--------+

.. note:: Group Box Format
   
   If the *Group Box Format* is disable, the dialogboxes with many differents tabs may be hard to use.

.. _HelpMenu:

Help
~~~~

.. |hlp1| image:: _static/figMainWindowHelpMenu.png
   :width: 6cm
   :align: middle

In this menu, it's possible to access to the WuMapPy and GeophPy versions number and documentations in two formats (html or pdf).

+--------+
| |hlp1| |
+--------+

On Linux operating system, to opening these documentations with the best application, you need, before starting "WuMapPy" application, to write the applications full names to use with html and pdf documents in the "config" file :

    >>> [MISC]
        html_viewer = none
        pdf_viewer = none

with 'none', the default string, the application launches only the file full name (".../WuMapPy.pdf" for example), and the operating system define which application to execute to opening the documentation file.

.. note::
   
   The "config" file is saved in "~/wumappy" on Windows, or "~/.wumappy" on Linux and Mac OS, where '~' is the user directory.

Data Set Window
---------------

:ref:`DataWinFilespMenu` | :ref:`DataWinProcessMenu` | :ref:`DataWinMagMenu` | :ref:`DataWinGeorefMenu` | :ref:`misc`

+-----------+
| |dataset| |
+-----------+

.. _DataWinFilespMenu:

Files
~~~~~

With this menu, it's possible to save the data set in a netcdf format file, and export the data set in several formats (ascii files, image, ...)

.. image:: _static/figDataSetWindowFilesMenu.png


Display Settings
~~~~~~~~~~~~~~~~

.. |disp1| image:: _static/figDataSetDisplaySettingsDlgBox.png
   :height: 8cm
   :align: middle

With this menu, it's possible to changes the DataSet display options (colormap, axis, value limits, ...)

+---------+
| |disp1| |
+---------+

.. _DataWinProcessMenu:

Processing
~~~~~~~~~~

The following general processing are available:

- :ref:`peak`
- :ref:`med`
- :ref:`fest`
- :ref:`regtrend`
- :ref:`walls`
- :ref:`ploug`
- :ref:`condest`
- :ref:`cubdest`

.. note:: 
   For more informations about the processing functions, see the GeophPy documentation.

.. _peak:

Peak filtering
++++++++++++++

.. |peak1| image:: _static/figDataSetPeakFilteringDlgBox.png
   :height: 8cm
   :align: middle

Data thresholding for values outside of the [*Minimal value*, *Maximal value*] interval.

+---------+
| |peak1| |
+---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _med:

Median filtering
++++++++++++++++

.. |med1| image:: _static/figDataSetMedianFilteringDlgBox.png
   :height: 8cm
   :align: middle

Classic median (salt-and-pepper) filter.

+--------+
| |med1| |
+--------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _fest:

Festoon filtering
+++++++++++++++++

.. |fest1| image:: _static/figDataSetFestoonFilteringDlgBox1.png
   :height: 8cm
   :align: middle

.. |fest2| image:: _static/figDataSetFestoonFilteringDlgBox2.png
   :width: 5cm
   :align: middle

.. |fest3| image:: _static/figDataSetFestoonFilteringDlgBox3.png
   :width: 5cm
   :align: middle

.. |fest4| image:: _static/figDataSetFestoonFilteringDlgBox4.png
   :width: 5cm
   :align: middle

.. |fest5| image:: _static/figDataSetFestoonFilteringDlgBox5.png
   :width: 5cm
   :align: middle

.. |fest6| image:: _static/figDataSetFestoonFilteringDlgBox6.png
   :width: 5cm
   :align: middle

.. |fest7| image:: _static/figDataSetFestoonFilteringDlgBox7.png
   :width: 5cm
   :align: middle

.. |fest8| image:: _static/figDataSetFestoonFilteringDlgBox8.png
   :width: 5cm
   :align: middle

.. |fest9| image:: _static/figDataSetFestoonFilteringDlgBox9.png
   :width: 5.5cm
   :align: middle

.. |fest10| image:: _static/figDataSetFestoonFilteringDlgBox10.png
   :width: 5cm
   :align: middle

.. |fest11| image:: _static/figDataSetFestoonFilteringDlgBox11.png
   :width: 5cm
   :align: middle

.. |fest12| image:: _static/figDataSetFestoonFilteringDlgBox12.png
   :width: 5.5cm
   :align: middle

.. |fest13| image:: _static/figDataSetFestoonFilteringDlgBox13.png
   :width: 5cm
   :align: middle

.. |corr1| image:: _static/figCorrelmapCrosscorr.png
   :width: 6cm
   :align: middle

.. |corr2| image:: _static/figCorrelmapPearson.png
   :width: 6cm
   :align: middle

.. |corr3| image:: _static/figCorrelmapSpearman.png
   :width: 6cm
   :align: middle

.. |corr4| image:: _static/figCorrelmapKendall.png
   :width: 6cm
   :align: middle

The festoon filter (destagger filter) reduces the positionning error along the survey profiles that result in a festoon-like effect.

+---------+
| |fest1| |
+---------+

An optimum shift is estimated based on the correlation of a particular profile and the mean of its surrounding profiles. 
The filter's windows display 3 differents tabs :

- the correlation map,
- the correlation sum profile, 
- and the filtered data.

+---------+---------+---------+
| |fest2| | |fest3| | |fest4| | 
+---------+---------+---------+

Different options are available:

- **Method** for correlation calculation (Cross-correlation or Pearson and Spearman or Kendall correlation):

+---------+---------+
| |corr1| | |corr2| | 
+---------+---------+
| |corr3| | |corr4| |
+---------+---------+

Due to the extensive computation time, Pearson, Spearman and Kendall correlation method are not computed over the whole shift domain.

The usage of Cross-correlation is hence recomanded. 

- **Uniform** shift throughout the data:

+---------+---------+---------+
| |fest5| | |fest6| | |fest7| |
+---------+---------+---------+

Return the best average shift for the dataset (based on the correlation sum off the dataset). Can be problematic when the position error is not regular over the dataset.

- **Non uniform** shift (different for each profile):

+---------+---------+----------+
| |fest8| | |fest9| | |fest10| |
+---------+---------+----------+

Return the best shift for each profile of the dataset (based on the correlation map).

- and required **minimum correlation** value:

+----------+----------+----------+
| |fest11| | |fest12| | |fest13| |
+----------+----------+----------+

Prevents shifting profiles if correlation value is to low, here is an example for 1 (i.e. no shift allowed).

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _regtrend:

Regional trend filtering
++++++++++++++++++++++++

.. |regtrend1| image:: _static/figDataSetRegTrendDlgBox.png
   :height: 8cm
   :align: middle

Remove the background (or regional response) from a dataset to enhance the features of interest. 

+-------------+
| |regtrend1| |
+-------------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _walls:

Wallis filtering
++++++++++++++++

The Wallis filter is a locally adaptative contrast enhancement filter. It is based on the local statistical properties of sub-window in the image.
It adjusts brightness values (grayscale image) in the local window so that the local mean and standard deviation match target values.

.. |wall1| image:: _static/figDataSetWallisFilteringDlgBox.png
   :height: 8cm
   :align: middle

+---------+
| |wall1| |
+---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _ploug:

Anti-ploughing filtering
++++++++++++++++++++++++

... To Be Developped ...

.. _condest:

Constant destriping
+++++++++++++++++++

.. |dest0| image:: _static/figDataSetConstantDestripingDlgBox.png
   :height: 8cm
   :align: middle

.. |dest1| image:: _static/figDataSetConstantDestripingDlgBox1.png
   :width: 5cm
   :align: middle

.. |dest2| image:: _static/figDataSetConstantDestripingDlgBox2.png
   :width: 5cm
   :align: middle

.. |dest3| image:: _static/figDataSetConstantDestripingDlgBox3.png
   :width: 5cm
   :align: middle

Remove from the dataset the strip noise effect arising from profile-to-profile differences in sensor height, orientation, drift or sensitivity (multi-sensors array).
Constant destriping is done using Moment Matching method.

+---------+
| |dest0| |
+---------+

The filter's windows display 3 differents tabs:

- the filtered dataset,
- the mean cross-track profile, 
- and the dataset histogram.

+---------+---------+---------+
| |dest1| | |dest2| | |dest3| | 
+---------+---------+---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _cubdest:

Curve destriping
++++++++++++++++

.. |curdest0| image:: _static/figDataSetCubicDestripingDlgBox.png
   :height: 8cm
   :align: middle

Remove from the dataset the strip noise effect by fitting and subtracting a polynomial curve to each profile on the dataset.

+------------+
| |curdest0| |
+------------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _DataWinMagMenu:

Magnetic Processing
~~~~~~~~~~~~~~~~~~~

The following magnetic processing are available:

- :ref:`maglog`
- :ref:`magrtp`
- :ref:`magcont`
- :ref:`maganasig`
- :ref:`magstratum`
- :ref:`maggrad`
- :ref:`mageuler`

.. _maglog:

Logarithmic transformation
++++++++++++++++++++++++++

.. image:: _static/figDataSetLogTransformationDlgBox.png

.. _magrtp:

Pole reduction
++++++++++++++

.. image:: _static/figDataSetPoleReductionDlgBox.png

.. _magcont:

Continuation
++++++++++++

.. image:: _static/figDataSetContinuationDlgBox.png

.. _maganasig:

Analytic signal
+++++++++++++++

.. image:: _static/figDataSetAnalyticSignalDlgBox.png

.. _magstratum:

Equivalent stratum magnetic susceptibility
++++++++++++++++++++++++++++++++++++++++++

.. image:: _static/figDataSetEquivStratumInMagSusceptDlgBox.png

.. _maggrad:

Gradient <-> Total field Conversion
+++++++++++++++++++++++++++++++++++

.. image:: _static/figDataSetConversionGradientMagFieldDlgBox.png

.. _mageuler:

Euleur deconvolution
++++++++++++++++++++

.. image:: _static/figDataSetEulerDeconvolutionDlgBox.png

The "Undo" Button allow to cancel the last action.
After having calculated Euler deconvolution for severals zones, it's possible to save these data in a "csv" file (with ';' as delimiter) by clicking on the "Save" button.

(For more informations about the magnetic processing functions, see GeophPy documentation.)

.. _DataWinGeorefMenu:

Georeferencing
~~~~~~~~~~~~~~

This item is available only if a geographic positions set is ever opened and displayed.

.. image:: _static/figDataSetGeoRefDlgBox.png


Geographic Positions Set Window
-------------------------------

:ref:`GeoPosWinFilesMenu` | :ref:`GeoPosWinConfigMenu`

.. image:: _static/figGeoPosSetWindow.png

.. _GeoPosWinFilesMenu:

Files
~~~~~

.. image:: _static/figGeoPosSetWindowFilesMenu.png

.. _GeoPosWinConfigMenu:

Configuration
~~~~~~~~~~~~~

.. image:: _static/figGeoPosSetConfigDlgBox.png

This item allows to georeference geographic positions with (x,y) local positions.


Feedback & Contribute
---------------------

Your feedback is more than welcome.

Write email to lionel.darras@mom.fr, philippe.marty@upmc.fr or quentin.vitale@eveha.fr

To cite this software :
"Marty, P., Darras, L. (2015). WuMapPy. Graphical User Interface for sub-surface geophysical survey
data processing (version x.y) [software]. Available at https://pypi.python.org/pypi/WuMapPy."

.. include:: ../CHANGES.rst