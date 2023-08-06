# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.gradmagfieldconversiondlgbox
    ------------------------------------------------

    Gradient and magnetic field conversion dialog box management.

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
# Gradient And Magnetic Field Conversion Dialog Box Object                  #
#---------------------------------------------------------------------------#
class GradMagFieldConversionDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, prosptechused, prosptechsim, apod=0, downsensoraltused = 0.3, upsensoraltused = 1.0, downsensoraltsim = 0.3, upsensoraltsim = 1.0, inclineangle = 65, alphaangle = 0):
        '''
        '''
        
        window = cls()
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.apod = apod
        window.inclineangle = inclineangle
        window.alphaangle = alphaangle
        window.prosptechused = prosptechused
        window.prosptechsim = prosptechsim
        window.downsensoraltused = downsensoraltused
        window.upsensoraltused = upsensoraltused
        window.downsensoraltsim = downsensoraltsim
        window.upsensoraltsim = upsensoraltsim
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILTOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'CONFIG_ID', 0, 1, False, None, None, 1, 1, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 1, 0, False, None, None, 1, 1, 1, 3, 2],
                           ['GroupBox', 'RENDERING_ID', 0, 2, False, None, None, 2, 0, 1, 1, 1],
                           #################################################################### Filter options
                           ['Label', 'APODISATIONFACTOR_ID', 0, 0, False, None, None, 0],  
                           ['SpinBox', '', 1, 0, True, window.ApodisationFactorInit, window.ApodisationFactorUpdate, 0],    
                           ['Label', 'APODISATIONFACTOR_MSG', 2, 0, False, None, None, 0],
                           ['Label', 'INCLINEANGLE_ID', 3, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 4, 0, True, window.InclineAngleInit, window.InclineAngleUpdate, 0],    
                           ['Label', 'ALPHAANGLE_ID', 5, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 6, 0, True, window.AlphaAngleInit, window.AlphaAngleUpdate, 0],    
                           ['Label', '', 7, 0, False, None, None, 0],  
                           ##################################################################### Configuration  
                           ['Label', 'PROSPTECHUSED_ID', 0, 1, False, None, None, 1],  
                           ['ComboBox', '', 1, 1, True, window.ProspTechUsedInit, window.ProspTechUsedUpdate, 1],    
                           ['Label', 'DOWNSENSORALT_ID', 2, 1, False, None, None, 1],
                           ['DoubleSpinBox', '', 3, 1, True, window.DownSensorAltUsedInit, window.DownSensorAltUsedUpdate, 1],    
                           ['Label', 'UPSENSORALT_ID', 4, 1, False, None, None, 1],
                           ['DoubleSpinBox', '', 5, 1, True, window.UpSensorAltUsedInit, window.UpSensorAltUsedUpdate, 1],    
                           ['Label', '', 6, 1, False, None, None, 1],  
                           ['Label', 'PROSPTECHSIM_ID', 7, 1, False, None, None, 1],  
                           ['ComboBox', '', 8, 1, True, window.ProspTechSimInit, window.ProspTechSimUpdate, 1],    
                           ['Label', 'DOWNSENSORALT_ID', 9, 1, False, None, None, 1],
                           ['DoubleSpinBox', '', 10, 1, True, window.DownSensorAltSimInit, window.DownSensorAltSimUpdate, 1],    
                           ['Label', 'UPSENSORALT_ID', 11, 1, False, None, None, 1],
                           ['DoubleSpinBox', '', 12, 1, True, window.UpSensorAltSimInit, window.UpSensorAltSimUpdate, 1],    
                           ['Label', 'ALTITUDE_MSG', 13, 1, False, None, None, 1],  
                           ######################################################################## Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 2],   
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 2],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 2],   
                           ######################################################################### Rendering
                           ['Image', '', 0, 2, False, window.CartoImageInit, None, 3]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def ApodisationFactorInit(self, id=None):
        if (id != None):
            id.setRange(0, 25)
            id.setSingleStep(5)
            id.setValue(self.apod)
        self.ApodisationFactorId = id
        return id


    def ApodisationFactorUpdate(self):
        self.apod = self.ApodisationFactorId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def InclineAngleInit(self, id=None):
        if (id != None):
            id.setRange(0.1, 90)
            id.setValue(self.inclineangle)
        self.InclineAngleId = id
        return id


    def InclineAngleUpdate(self):
        self.inclineangle = self.InclineAngleId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def AlphaAngleInit(self, id=None):
        if (id != None):
            id.setRange(0, 360)
            id.setValue(self.alphaangle)
        self.AlphaAngleId = id
        return id


    def AlphaAngleUpdate(self):
        self.alphaangle = self.AlphaAngleId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ProspTechUsedInit(self, id=None):
        list = prosptech_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.prosptechused)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ProspTechUsedId = id
        return id
        
        

    def ProspTechUsedUpdate(self):
        self.prosptechused = self.ProspTechUsedId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def DownSensorAltUsedInit(self, id=None):
        id.setSingleStep(0.1)
        id.setValue(self.downsensoraltused)
        self.DownSensorAltUsedId = id
        return id


    def DownSensorAltUsedUpdate(self):
        self.downsensoraltused = self.DownSensorAltUsedId.value()
        self.UpSensorAltUsedId.setRange(self.downsensoraltused + 0.1, 99)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        
        
    def UpSensorAltUsedInit(self, id=None):
        id.setSingleStep(0.1)
        id.setRange(self.downsensoraltused + 0.1, 99)
        if (self.upsensoraltused < self.downsensoraltused):   # if wrong upsensor altitude
            self.upsensoraltused = self.downsensoraltused + 1.# set the up-sensor altitude equal to just more than down-sensor altitude 
        id.setValue(self.upsensoraltused)
        self.DownSensorAltUsedId.setRange(0, self.upsensoraltused - 0.1)
        self.UpSensorAltUsedId = id
        return id


    def UpSensorAltUsedUpdate(self):
        self.upsensoraltused = self.UpSensorAltUsedId.value()
        self.DownSensorAltUsedId.setRange(0, self.upsensoraltused - 0.1)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ProspTechSimInit(self, id=None):
        list = prosptech_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.prosptechsim)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ProspTechSimId = id
        return id
        
        

    def ProspTechSimUpdate(self):
        self.prosptechsim = self.ProspTechSimId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def DownSensorAltSimInit(self, id=None):
        id.setSingleStep(0.1)
        id.setValue(self.downsensoraltsim)
        self.DownSensorAltSimId = id
        return id


    def DownSensorAltSimUpdate(self):
        self.downsensoraltsim = self.DownSensorAltSimId.value()
        self.UpSensorAltSimId.setRange(self.downsensoraltsim + 0.1, 99)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        
        
    def UpSensorAltSimInit(self, id=None):
        id.setSingleStep(0.1)
        id.setRange(self.downsensoraltsim + 0.1, 99)
        if (self.upsensoraltsim < self.downsensoraltsim):   # if wrong upsensor altitude
            self.upsensoraltsim = self.downsensoraltsim + 1.# set the up-sensor altitude equal to just more than down-sensor altitude 
        id.setValue(self.upsensoraltsim)
        self.DownSensorAltSimId.setRange(0, self.upsensoraltsim - 0.1)
        self.UpSensorAltSimId = id
        return id


    def UpSensorAltSimUpdate(self):
        self.upsensoraltsim = self.UpSensorAltSimId.value()
        self.DownSensorAltSimId.setRange(0, self.upsensoraltsim - 0.1)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


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
        return id


    def CartoImageUpdate(self):
        initcursor = self.wid.cursor()                                  # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                        # sets the wait cursor

        # processes data set
        self.dataset = self.originaldataset.copy()
        self.dataset.gradmagfieldconversion(self.prosptechused, self.prosptechsim, self.apod, self.downsensoraltused, self.upsensoraltused, self.downsensoraltsim, self.upsensoraltsim, self.inclineangle, self.alphaangle)

        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=self.parent.zmin, cmmax=self.parent.zmax, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))    # builds the pixmap from the canvas
        cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

        prosptechlist = prosptech_getlist()                             # gets the list of prospection technicals availables
                                                                        # if magnetic field gradient <-> full magnetic field
        if (((self.prosptechused == prosptechlist[0]) and (self.prosptechsim == prosptechlist[1])) or ((self.prosptechused == prosptechlist[1]) and (self.prosptechsim == prosptechlist[0]))):
            self.InclineAngleId.setEnabled(False)                       # incline and alpha angles not used
            self.AlphaAngleId.setEnabled(False)
        else :              
            self.InclineAngleId.setEnabled(True)                        # incline and alpha angles used
            self.AlphaAngleId.setEnabled(True)

        # if prospection technical is magnetic field
        if (self.prosptechused == prosptechlist[0]) :
            self.UpSensorAltUsedId.setEnabled(False)    # disables because only one sensor
        else:
            self.UpSensorAltUsedId.setEnabled(True)     # enables because two sensors

        # if prospection technical is magnetic field
        if (self.prosptechsim == prosptechlist[0]) :
            self.UpSensorAltSimId.setEnabled(False)    # disables because only one sensor
        else:
            self.UpSensorAltSimId.setEnabled(True)     # enables because two sensors

        if (self.prosptechused == self.prosptechsim):
            self.CartoImageId.setEnabled(False)                             # disables the carto image
            self.ValidButtonId.setEnabled(False)                            # disables the valid button
        else:
            self.CartoImageId.setEnabled(True)                              # enables the carto image
            self.ValidButtonId.setEnabled(True)                             # enables the valid button
            
            
            
        self.wid.setCursor(initcursor)                                  # resets the init cursor
