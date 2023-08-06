# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.festoonfiltdlgbox
    -------------------------------------

    Festoon filtering dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
import numpy as np
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

SIZE_GRAPH_x = 440

#---------------------------------------------------------------------------#
# Festoon Filtering Dialog Box Object                                       #
#---------------------------------------------------------------------------#
class FestoonFiltDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, method='Crosscorr', shift=0, corrmin=0.4, uniformshift=False):
        '''
        '''
        
        window = cls()
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.zmin = window.parent.zmin
        window.zmax = window.parent.zmax
        zmin, zmax = window.dataset.histo_getlimits()
        if (window.zmin == None):
            window.zmin = zmin
        if (window.zmax == None):
            window.zmax = zmax            

        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.method = method
        window.shift = shift
        window.corrmin = corrmin
        window.uniformshift = uniformshift
        window.items_list = [# ELEMENT TYPE - ELEMENT_ID - COLUMN - ROW -IS AVAILABLE - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILTOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'RENDERING_ID', 0, 1, False, None, None, 1, 0, 1, 1, 1],
                           ['GroupBox', 'CORRELATIONMAP_ID', 0, 2, False, None, None, 2, 0, 1, 1, 1],
                           ['GroupBox', 'CORRELATIONSUM_ID', 0, 3, False, None, None, 3, 0, 1, 1, 1],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 1, 1, 4, 2],
                           ############################################################################################### Filter options
                           ['Label', 'FESTOONFILTMETHOD_ID', 0, 0, False, None, None, 0],  
                           ['ComboBox', '', 1, 0, True, window.MethodInit, window.MethodUpdate, 0],
                           ['Label', '', 2, 0, False, None, None, 0],
                           ['CheckBox', 'FESTOONFILTSHIFT_ID', 3, 0, False, window.UniformShiftInit, window.UniformShiftUpdate, 0],  
                           ['SpinBox', '', 4, 0, True, window.ShiftInit, window.ShiftUpdate, 0],    
                           ['Label', '', 5, 0, False, None, None, 0],
                           ['Label', 'FESTOONFILTMINCORR_ID', 6, 0, False, None, None, 0],   
                           ['DoubleSpinBox', '', 7, 0, True, window.CorrMinInit, window.CorrMinUpdate, 0],  
                           ['Label', '', 8, 0, False, None, None, 0], 
                           ['Label', '', 9, 0, False, None, None, 0],
                           ############################################################################################### Correl Map
                           ['Image', '', 7, 0, False, window.CorrMapImageInit, None, 2],   
                           ############################################################################################### Correl Sum
                           ['Image', '', 9, 0, False, window.CorrSumImageInit, None, 3],   
                           ############################################################################################### Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 4],   
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 4],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 4],   
                           ############################################################################################### Rendering
                           ['Image', '', 0, 1, False, window.CartoImageInit, None, 1]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def MethodInit(self, id=None):                                                  
        method_list = festooncorrelation_getlist()
        try:
            method_index = method_list.index(self.method)
        except:
            method_index = 0
            
        if (id != None):
            id.addItems(method_list)
            id.setCurrentIndex(method_index)
        self.MethodId = id
        return id


    def MethodUpdate(self):
        self.method = self.MethodId.currentText()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def UniformShiftInit(self, id=None):
        if (id != None):
            id.setChecked(self.uniformshift)
        self.UniformShiftId = id
        return id

  
    def UniformShiftUpdate(self):
        self.uniformshift = self.UniformShiftId.isChecked()  # updates Uniform Shift Flag
        self.ShiftId.setEnabled(self.uniformshift)           # disables/enables Uniform Shift Value
        
        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ShiftInit(self, id=None):
        if (id != None):                              
            range = (self.dataset.info.y_max - self.dataset.info.y_min)/2
            id.setRange(-range, +range)
            id.setValue(self.shift)
        self.ShiftId = id
        self.ShiftId.setEnabled(self.uniformshift)
        return id


    def ShiftUpdate(self):
        self.shift = self.ShiftId.value()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Auto update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def CorrMinInit(self, id=None):
        if (id != None):
            id.setRange(0, 1.0)
            id.setSingleStep(0.1)
            id.setValue(self.corrmin)
        self.CorrMinId = id
        return id

    
    def CorrMinUpdate(self):
        self.corrmin = self.CorrMinId.value()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Auto update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
    

    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)       # Hides button if real time updating activated
        id.setEnabled(False)                        # disables the button , by default
        return id


    def CorrMapImageInit(self, id=None):
        self.CorrMapImageId = id
        self.corrmapfig = None
        return id


    def CorrMapImageUpdate(self):
        self.corrmapfig = self.dataset.correlation_plotmap(fig=self.corrmapfig, method=self.method)
        #pixmap = QtGui.QPixmap.grabWidget(self.corrmapfig.canvas)   # builds the pixmap from the canvas
        pixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.corrmapfig))   # builds the pixmap from the canvas
        pixmap = pixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CorrMapImageId.setPixmap(pixmap)
        

    def CorrSumImageInit(self, id=None):
        self.CorrSumImageId = id
        self.corrsumfig = None
        return id


    def CorrSumImageUpdate(self):
        self.corrsumfig = self.dataset.correlation_plotsum(fig=self.corrsumfig, method=self.method)
        #pixmap = QtGui.QPixmap.grabWidget(self.corrsumfig.canvas)   # builds the pixmap from the canvas
        pixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.corrsumfig))   # builds the pixmap from the canvas
        pixmap = pixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CorrSumImageId.setPixmap(pixmap)
        

    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                     # updates carto image, corr map and corr sum
        

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

        # Processing data set
        self.dataset = self.originaldataset.copy()
        self.shift = self.dataset.festoonfilt(method=self.method, shift=self.shift, corrmin=self.corrmin, uniformshift=self.uniformshift)
  

        # Plot geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=None, cmmax=None, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))    # builds the pixmap from the canvas
        cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CartoImageId.setPixmap(cartopixmap)
        
        # Updating dependencies
        self.CorrSumImageUpdate()
        self.CorrMapImageUpdate()
        self.ShiftId.setValue(self.shift)

        # Enabling Map & Buttons
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button




        self.wid.setCursor(initcursor)                                  # resets the init cursor
        
