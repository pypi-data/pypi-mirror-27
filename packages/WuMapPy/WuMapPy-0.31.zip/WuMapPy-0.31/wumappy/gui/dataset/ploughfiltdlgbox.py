# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.ploughfiltdlgbox
    ------------------------------------

    Anti-Plough filtering dialog box management.

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
# Anti-Plough Filtering Dialog Box Object                                   #
#---------------------------------------------------------------------------#
class PloughFiltDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, nxsize=3, nysize=3, apod=0, angle=None, cutoff=None):
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
        window.nxsize = nxsize
        window.nysize = nysize
        window.apodisationfactor = apod
        window.angle = angle
        window.cutoff = cutoff
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILTOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 1, 1, 3, 2],
                           ['GroupBox', 'RENDERING_ID', 0, 1, False, None, None, 2, 0, 1, 1, 1],
                           ######################################################################### Filter options
                           ['Label', 'FILTERNXSIZE_ID', 0, 0, False, None, None, 0],  
                           ['SpinBox', '', 1, 0, True, window.NxSizeInit, window.NxSizeUpdate, 0],   
                           ['Label', 'FILTERNYSIZE_ID', 2, 0, False, None, None, 0],  
                           ['SpinBox', '', 3, 0, True, window.NySizeInit, window.NySizeUpdate, 0],    
                           ['Label', 'APODISATIONFACTOR_ID', 4, 0, False, None, None, 0],  
                           ['SpinBox', '', 5, 0, True, window.ApodisationFactorInit, window.ApodisationFactorUpdate, 0],    
                           ['Label', 'PLOUGHANGLE_ID', 6, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 7, 0, True, window.AngleInit, window.AngleUpdate, 0],     
                           ['Label', 'PLOUGHCUTOFF_ID', 8, 0, False, None, None, 0], 
                           ['DoubleSpinBox', '', 9, 0, True, window.CutOffInit, window.CutOffUpdate, 0], 
                           ['Label', '', 10, 0, False, None, None, 0],   
                           ######################################################################### Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 1],   
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 1],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 1],   
                           ######################################################################### Rendering
                           ['Image', '', 0, 1, False, window.CartoImageInit, None, 2]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nxsize)
        self.NxSizeId = id
        return id


    def NxSizeUpdate(self):
        self.nxsize = self.NxSizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NySizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nysize)
        self.NySizeId = id
        return id


    def NySizeUpdate(self):
        self.nysize = self.NySizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nxsize)
        self.NxSizeId = id
        return id


    def NxSizeUpdate(self):
        self.nxsize = self.NxSizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ApodisationFactorInit(self, id=None):
        if (id != None):
            id.setRange(0, 25)
            id.setSingleStep(5)
            id.setValue(self.apodisationfactor)
        self.ApodisationFactorId = id
        return id


    def ApodisationFactorUpdate(self):
        self.apodisationfactor = self.ApodisationFactorId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def AngleInit(self, id=None):
        if (id != None):
            id.setRange(0, 359.9)
            id.setValue(self.angle)
        self.AngleId = id
        return id


    def AngleUpdate(self):
        self.angle = self.AngleId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def CutOffInit(self, id=None):
        if (id != None):
            id.setRange(0, 10000.0)
            id.setValue(self.cutoff)
        self.CutOffId = id
        return id


    def CutOffUpdate(self):
        self.cutoff = self.CutOffId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)       # Hides button if real time updating activated
        id.setEnabled(False)                        # disables the button , by default
        return id


    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                     # updates carto image
        

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
        self.dataset.ploughfilt(self.nxsize, self.nysize, self.apodisationfactor, self.angle, self.cutoff)

        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=self.zmin, cmmax=self.zmax, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))    # builds the pixmap from the canvas
        cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

        self.wid.setCursor(initcursor)                                  # resets the init cursor
        
