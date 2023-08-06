# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.continuationdlgbox
    ---------------------------------------

    Continuation dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

SIZE_GRAPH_x = 440

#---------------------------------------------------------------------------#
# Continuation Dialog Box Object                                               #
#---------------------------------------------------------------------------#
class ContinuationDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, prosptech, apod=0, downsensoraltitude=0.3, upsensoraltitude=1.0, continuationflag=False, continuationvalue=0.0, continuationsoilsurfaceaboveflag=False):
        '''
        '''
        
        window = cls()
        window.firstdisplayflag = True             # True if first display of dialog box, False in the others cases
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.automaticrangeflag = True
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.apod = apod
        window.prosptech = prosptech
        window.downsensoraltitude = downsensoraltitude
        window.upsensoraltitude = upsensoraltitude
        window.continuationflag = continuationflag
        window.continuationvalue = continuationvalue
        window.continuationsoilsurfaceaboveflag = continuationsoilsurfaceaboveflag
        window.valfiltflag = False
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'CONFIG_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'FILTOPT_ID', 1, 0, False, None, None, 1, 1, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 2, 1, 1, 2, 2],
                           ['GroupBox', 'RENDERING_ID', 0, 1, False, None, None, 3, 0, 1, 1, 1],
                           ['GroupBox', 'HISTOGRAM_ID', 1, 1, False, None, None, 4, 0, 1, 1, 1],
                           #################################################################### Configuration
                           ['Label', 'APODISATIONFACTOR_ID', 0, 0, False, None, None, 0],  
                           ['SpinBox', '', 1, 0, True, window.ApodisationFactorInit, window.ApodisationFactorUpdate, 0], 
                           ['Label', 'PROSPTECH_ID', 2, 0, False, None, None, 0],  
                           ['ComboBox', '', 3, 0, True, window.ProspTechInit, window.ProspTechUpdate, 0],     
                           ['Label', 'DOWNSENSORALT_ID', 4, 0, False, None, None, 0],
                           ['DoubleSpinBox', '', 5, 0, True, window.DownSensorAltitudeInit, window.DownSensorAltitudeUpdate, 0],    
                           ['Label', 'UPSENSORALT_ID', 6, 0, False, None, None, 0],
                           ['DoubleSpinBox', '', 7, 0, True, window.UpSensorAltitudeInit, window.UpSensorAltitudeUpdate, 0],    
                           ['Label', 'ALTITUDE_MSG', 8, 0, False, None, None, 0],  
                           ['Label', '', 9, 0, False, None, None, 0],
                           ['Label', '', 10, 0, False, None, None, 0],
                           ['Label', '', 11, 0, False, None, None, 0],
                           ['Label', '', 12, 0, False, None, None, 0],
                           ['Label', '', 13, 0, False, None, None, 0],
                           ###################################################################### Filter options
                           ['CheckBox', 'CONTINUATIONFLAG_ID', 0, 0, True, window.ContinuationFlagInit, window.ContinuationFlagUpdate, 1],
                           ['Label', 'CONTINUATIONVALUE_ID', 1, 0, False, window.ContinuationValueLabelInit, None, 1],  
                           ['DoubleSpinBox', '', 2, 0, True, window.ContinuationValueInit, window.ContinuationValueUpdate, 1],    
                           ['CheckBox', 'SOILSURFACEABOVEFLAG_ID', 3, 0, True, window.SoilSurfaceAboveFlagInit, window.SoilSurfaceAboveFlagUpdate, 1],    
                           ['CheckBox', 'SOILSURFACEBELOWFLAG_ID', 4, 0, True, window.SoilSurfaceBelowFlagInit, window.SoilSurfaceBelowFlagUpdate, 1],     
                           ['Label', 'MINIMALVALUE_ID', 5, 0, False, None, None, 1],  
                           ['SpinBox', '', 6, 0, True, window.MinimalValuebySpinBoxInit, window.MinimalValuebySpinBoxUpdate, 1],    
                           ['Slider', '', 7, 0, True, window.MinimalValuebySliderInit, window.MinimalValuebySliderUpdate, 1],   
                           ['Label', 'MAXIMALVALUE_ID', 8, 0, False, None, None, 1],  
                           ['SpinBox', '', 9, 0, True, window.MaximalValuebySpinBoxInit, window.MaximalValuebySpinBoxUpdate, 1],    
                           ['Slider', '', 10, 0, True, window.MaximalValuebySliderInit, window.MaximalValuebySliderUpdate, 1],
                           ['Label', '', 11, 0, False, None, None, 1],
                           ['Label', '', 12, 0, False, None, None, 1],
                           ['Label', '', 13, 0, False, None, None, 1],
                           ####################################################################### Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 2],   
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 2],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 2],   
                           ####################################################################### Histogram
                           ['Image', '', 0, 0, False, window.HistoImageInit, None, 4],  
                           ####################################################################### Rendering
                           ['Image', '', 1, 0, False, window.CartoImageInit, None, 3]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def ApodisationFactorInit(self, id=None):
        id.setRange(0, 25)
        id.setSingleStep(5)
        id.setValue(self.apod)
        self.ApodisationFactorId = id
        return id


    def ApodisationFactorUpdate(self):
        self.apod = self.ApodisationFactorId.value()
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ProspTechInit(self, id=None):
        list = prosptech_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.prosptech)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ProspTechId = id
        return id
        
        

    def ProspTechUpdate(self):
        self.prosptech = self.ProspTechId.currentText()
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def DownSensorAltitudeInit(self, id=None):
        id.setSingleStep(0.1)
        id.setValue(self.downsensoraltitude)
        self.DownSensorAltId = id
        return id


    def DownSensorAltitudeUpdate(self):
        self.downsensoraltitude = self.DownSensorAltId.value()
        self.UpSensorAltId.setRange(self.downsensoraltitude + 0.1, 99)
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button        
        
        
    def UpSensorAltitudeInit(self, id=None):
        id.setSingleStep(0.1)
        id.setRange(self.downsensoraltitude + 0.1, 99)
        if (self.upsensoraltitude < self.downsensoraltitude):   # if wrong upsensor altitude
            self.upsensoraltitude = self.downsensoraltitude + 1.# set the up-sensor altitude equal to just more than down-sensor altitude 
        id.setValue(self.upsensoraltitude)
        self.DownSensorAltId.setRange(0, self.upsensoraltitude - 0.1)
        self.UpSensorAltId = id
        return id


    def UpSensorAltitudeUpdate(self):
        self.upsensoraltitude = self.UpSensorAltId.value()
        self.DownSensorAltId.setRange(0, self.upsensoraltitude - 0.1)
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ContinuationFlagInit(self, id=None):
        id.setChecked(self.continuationflag)
        self.ContinuationFlagId = id
        return id


    def ContinuationFlagUpdate(self):
        self.continuationflag = self.ContinuationFlagId.isChecked()
                                                                # enables this continuation altitude field only if continuation selected
        self.ContinuationValueLabelId.setEnabled(self.continuationflag)      
        self.ContinuationValueId.setEnabled(self.continuationflag)      
        self.SoilSurfaceAboveFlagId.setEnabled(self.continuationflag)      
        self.SoilSurfaceBelowFlagId.setEnabled(self.continuationflag)      
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ContinuationValueLabelInit(self, id=None):
        self.ContinuationValueLabelId = id
        return id


    def ContinuationValueInit(self, id=None):
        id.setSingleStep(0.1)
        id.setValue(self.continuationvalue)
        id.setEnabled(self.continuationflag)                    # enables this field only if continuation selected
        self.ContinuationValueLabelId.setEnabled(self.continuationflag) # enables this field only if continuation selected
        self.ContinuationValueId = id
        return id


    def ContinuationValueUpdate(self):
        self.continuationvalue = self.ContinuationValueId.value()
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button

        
    def SoilSurfaceAboveFlagInit(self, id=None):
        id.setChecked(self.continuationsoilsurfaceaboveflag)
        self.SoilSurfaceAboveFlagId = id
        return id


    def SoilSurfaceAboveFlagUpdate(self):
        self.continuationsoilsurfaceaboveflag = self.SoilSurfaceAboveFlagId.isChecked()
                                                                # enables this continuation altitude field only if continuation selected
        self.SoilSurfaceBelowFlagId.setChecked(not self.continuationsoilsurfaceaboveflag)      
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def SoilSurfaceBelowFlagInit(self, id=None):
        id.setChecked(not self.continuationsoilsurfaceaboveflag)
        self.SoilSurfaceBelowFlagId = id
        return id


    def SoilSurfaceBelowFlagUpdate(self):
        self.continuationsoilsurfaceaboveflag = not self.SoilSurfaceBelowFlagId.isChecked()
                                                                # enables this continuation altitude field only if continuation selected
        self.SoilSurfaceAboveFlagId.setChecked(self.continuationsoilsurfaceaboveflag)      
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySpinBoxInit(self, id=None):
        self.MinValuebySpinBoxId = id
        return id


    def MinimalValuebySpinBoxReset(self):
        self.MinValuebySpinBoxId.setRange(self.zmin, self.zmax)
        self.MinValuebySpinBoxId.setValue(self.zmin)


    def MinimalValuebySpinBoxUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySpinBoxId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
        self.MinValuebySpinBoxId.setValue(self.zmin)    

        self.MinValuebySliderId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            if (self.firstdisplayflag != True) :
                self.CartoImageUpdate()                         # updates carto only if real time updating activated and not first display
                self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySliderInit(self, id=None):
        id.setOrientation(QtCore.Qt.Horizontal)
        self.MinValuebySliderId = id
        return id


    def MinimalValuebySliderReset(self):
        self.MinValuebySliderId.setRange(self.zmin, self.zmax)
        self.MinValuebySliderId.setValue(self.zmin)


    def MinimalValuebySliderUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySliderId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
            self.MinValuebySliderId.setValue(self.zmin)    

        self.MinValuebySpinBoxId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            if (self.firstdisplayflag != True) :
                self.CartoImageUpdate()                         # updates carto only if real time updating activated and not first display
                self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySpinBoxInit(self, id=None):
        self.MaxValuebySpinBoxId = id
        return id


    def MaximalValuebySpinBoxReset(self):
        self.MaxValuebySpinBoxId.setRange(self.zmin, self.zmax)
        self.MaxValuebySpinBoxId.setValue(self.zmax)


    def MaximalValuebySpinBoxUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySpinBoxId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySpinBoxId.setValue(self.zmax)    
            
        self.MaxValuebySliderId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySliderInit(self, id=None):
        id.setOrientation(QtCore.Qt.Horizontal)
        self.MaxValuebySliderId = id
        return id


    def MaximalValuebySliderReset(self):
        self.MaxValuebySliderId.setRange(self.zmin, self.zmax)
        self.MaxValuebySliderId.setValue(self.zmax)
        return id


    def MaximalValuebySliderUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySliderId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySliderId.setValue(self.zmax)    
            
        self.MaxValuebySpinBoxId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            if (self.firstdisplayflag != True) :
                self.CartoImageUpdate()                         # updates carto only if real time updating activated and not first display
                self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def HistoImageInit(self, id=None):
        self.HistoImageId = id
        self.histofig = None
        return id


    def HistoImageUpdate(self):
        self.histofig = self.dataset.histo_plot(fig=self.histofig, zmin=self.zmin, zmax=self.zmax)
        #histopixmap = QtGui.QPixmap.grabWidget(self.histofig.canvas)   # builds the pixmap from the canvas
        histopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.histofig))   # builds the pixmap from the canvas
        histopixmap = histopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.HistoImageId.setPixmap(histopixmap)
        

    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)                   # Hides button if real time updating activated
        id.setEnabled(False)                                    # disables the button , by default
        return id


    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                                 # updates carto image
        

    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


    def CartoImageInit(self, id=None):
        self.cartofig = None
        self.CartoImageId = id
        self.CartoImageUpdate()
        self.HistoImageUpdate()
        return id


    def CartoImageUpdate(self):
        initcursor = self.wid.cursor()                                  # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                        # sets the wait cursor

        try:
            # processes data set
            self.dataset = self.originaldataset.copy()
            if (self.continuationsoilsurfaceaboveflag) :                                # if above soil surface,
                continuationvalue = self.continuationvalue
            else :                                                          # if below soil surface,
                continuationvalue = - self.continuationvalue

            self.dataset.continuation(self.prosptech, self.apod, self.downsensoraltitude, self.upsensoraltitude, self.continuationflag, continuationvalue)
            if (self.automaticrangeflag):
                self.automaticrangeflag = False
                self.zmin, self.zmax = self.dataset.histo_getlimits()            
                self.MinimalValuebySpinBoxReset()
                self.MinimalValuebySliderReset()
                self.MaximalValuebySpinBoxReset()
                self.MaximalValuebySliderReset()

            # plots geophysical image
            self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=self.zmin, cmmax=self.zmax, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
            #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
            cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))    # builds the pixmap from the canvas
            cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
            self.CartoImageId.setPixmap(cartopixmap)
            self.CartoImageId.setEnabled(True)                              # enables the carto image
            self.ValidButtonId.setEnabled(True)                             # enables the valid button
            self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

            prosptechlist = prosptech_getlist()                             # gets the list of prospection technicals availables

            # if prospection technical is magnetic field
            if (self.prosptech == prosptechlist[0]) :
                self.UpSensorAltId.setEnabled(False)                        # disables because only one sensor
            else:
                self.UpSensorAltId.setEnabled(True)                         # enables because two sensors
        except:
            self.cartofig, cartocmap = None, None
            self.CartoImageId.setEnabled(False)                             # disables the carto image
            self.ValidButtonId.setEnabled(False)
        
        
        self.firstdisplayflag = False
        self.wid.setCursor(initcursor)                                  # resets the init cursor
