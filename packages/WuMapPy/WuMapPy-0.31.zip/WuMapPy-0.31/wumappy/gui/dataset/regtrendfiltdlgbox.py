# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.regtrendfiltdlgbox
    --------------------------------------

    Regional Trend Filtering dialog box management.

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
# Regional Trend Filtering Dialog Box Object                                #
#---------------------------------------------------------------------------#
class RegTrendFiltDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, nxsize=3, nysize=3, method='rel', component='loc'):
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
        window.method = method
        window.component = component
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILTOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 1, 1, 3, 2],
                           ['GroupBox', 'RENDERING_ID', 0, 1, False, None, None, 2, 0, 1, 1, 1],
                           ######################################################################### Filter options
                           ['Label', 'FILTERNXSIZE_ID', 0, 0, False, None, None, 0],  
                           ['SpinBox', '', 1, 0, True, window.NxSizeInit, window.NxSizeUpdate, 0],    
                           #['Label', '', 2, 0, False, None, None, 0],
                           ['CheckBox', 'SQUARE_PIXEL', 2, 0, True, window.SquareInit, window.SquareUpdate, 0],  
                           ['Label', 'FILTERNYSIZE_ID', 3, 0, False, window.NySizeLabelInit, None, 0],  
                           ['SpinBox', '', 4, 0, True, window.NySizeInit, window.NySizeUpdate, 0],    
                           ['Label', '', 5, 0, False, None, None, 0],  
                           ['Label', 'REGTRENDMETHOD_ID', 6, 0, False, None, None, 0],  
                           ['ComboBox', '', 7, 0, True, window.MethodInit, window.MethodUpdate, 0],   
                           ['Label', '', 8, 0, False, None, None, 0],  
                           ['Label', 'REGTRENDCOMPONENT_ID', 9, 0, False, None, None, 0],  
                           ['ComboBox', '', 10, 0, True, window.ComponentInit, window.ComponentUpdate, 0],   
                           ['Label', '', 11, 0, False, None, None, 0],  
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
            id.setRange(3, 101)
            id.setSingleStep(2)
            id.setValue(self.nxsize)
        self.NxSizeId = id
        return id


    def NxSizeUpdate(self):
        self.nxsize = self.NxSizeId.value()
        if self.square_pixel.isChecked():
            self.NySizeId.setValue(self.nxsize)
            self.NySizeUpdate()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NySizeInit(self, id=None):
        if (id != None):
            id.setRange(3, 101)
            id.setSingleStep(2)
            id.setValue(self.nysize)
            id.setEnabled(False)
        self.NySizeId = id
        return id


    def NySizeUpdate(self):
        self.nysize = self.NySizeId.value()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NySizeLabelInit(self, id=None):
        if (id != None):
            square_pixel_flag = self.square_pixel.isChecked()
            id.setEnabled(not square_pixel_flag)
        self.NySizeLabelId = id
        return id  


    def SquareInit(self, id=None):
        if (id != None):
            id.setChecked(True)
            self.square_pixel = id
        return id


    def SquareUpdate(self):
        square_pixel_flag = self.square_pixel.isChecked()
        self.NySizeId.setEnabled(not square_pixel_flag)
        self.NySizeLabelId.setEnabled(not square_pixel_flag)
        self.NxSizeUpdate()


    def MethodInit(self, id=None):
        list = regtrendmethod_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.method)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.MethodId = id
        return id
            

    def MethodUpdate(self):
        self.method = self.MethodId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def ComponentInit(self, id=None):
        list = regtrendcomp_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.component)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ComponentId = id
        return id
            

    def ComponentUpdate(self):
        self.component = self.ComponentId.currentText()
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
        self.dataset.regtrend(self.nxsize, self.nysize, self.method, self.component)

        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=None, cmmax=None, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))    # builds the pixmap from the canvas
        cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

        self.wid.setCursor(initcursor)                                  # resets the init cursor
        
