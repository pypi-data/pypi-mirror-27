# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.dispsettingsdlgbox
    --------------------------------------

    Display settings dialog box management.

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
###
import matplotlib.pyplot as plt
###

SIZE_GRAPH_x = 440

#---------------------------------------------------------------------------#
# Display Settings Dialog Box Object                                        #
#---------------------------------------------------------------------------#
class DispSettingsDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent):
        '''
        '''
        
        window = cls()
        window.title = title
        window.parent = parent
        window.dataset = parent.dataset
        window.parentid = parent.wid
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')                                                                
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'DISPOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 1, 1, 3, 2],
                           ['GroupBox', 'RENDERING_ID', 0, 2, False, None, None, 2, 0, 1, 1, 1],
                           ['GroupBox', 'HISTOGRAM_ID', 0, 1, False, None, None, 3, 0, 1, 1, 1],
                           ######################################################################### Display options
                           ['Label', 'PLOTTYPE_ID', 0, 0, False, None, None, 0], 
                           ['ComboBox', '', 1, 0, True, window.PlotTypeInit, window.PlotTypeUpdate, 0],   
                           ['Label', 'INTERPOLATION_ID', 2, 0, False, None, None, 0],  
                           ['ComboBox', '', 3, 0, True, window.InterpolationInit, window.InterpolationUpdate, 0], 
                           ['Label', 'COLORMAP_ID', 4, 0, False, None, None, 0],   
                           ['ComboBox', '', 5, 0, True, window.ColorMapInit, window.ColorMapUpdate, 0], 
                           ['CheckBox', 'REVERSEFLAG_ID', 6, 0, True, window.ColorMapReverseInit, window.ColorMapReverseUpdate, 0],  
                           ['CheckBox', 'COLORBARDISPLAYFLAG_ID', 7, 0, True, window.ColorBarDisplayInit, window.ColorBarDisplayUpdate, 0],  
                           ['CheckBox', 'COLORBARLOGSCALEFLAG_ID', 8, 0, True, window.ColorBarLogScaleInit, window.ColorBarLogScaleUpdate, 0],   
                           ['CheckBox', 'AXISDISPLAYFLAG_ID', 9, 0, True, window.AxisDisplayInit, window.AxisDisplayUpdate, 0],
                           ['Label', '', 10, 0, False, None, None, 0],
                           ['Label', '', 11, 0, False, None, None, 0],
                           ['Label', '', 12, 0, False, None, None, 0],
                           ['Label', '', 13, 0, False, None, None, 0],
                           ['Label', 'MINIMALVALUE_ID', 10, 0, False, None, None, 0], 
                           ['DoubleSpinBox', '', 11, 0, True, window.MinimalValuebySpinBoxInit, window.MinimalValuebySpinBoxUpdate, 0],    
                           ['Slider', '', 12, 0, True, window.MinimalValuebySliderInit, window.MinimalValuebySliderUpdate, 0],  
                           ['Label', 'MAXIMALVALUE_ID', 13, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 14, 0, True, window.MaximalValuebySpinBoxInit, window.MaximalValuebySpinBoxUpdate, 0],    
                           ['Slider', '', 15, 0, True, window.MaximalValuebySliderInit, window.MaximalValuebySliderUpdate, 0],
                           ['Label', '', 16, 0, False, None, None, 0],
                           ######################################################################### Cancel, Update Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 1],
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 1],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 1],   
                           ######################################################################### Histogram
                           ['Image', '', 0, 0, False, window.HistoImageInit, None, 3],   
                           ######################################################################### Rendering
                           ['Image', '', 0, 1, False, window.CartoImageInit, None, 2]]

        dlgbox = CartoDlgBox(window.asciiset.getStringValue('DISPLAYSETTINGS_ID'), window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def PlotTypeInit(self, id=None):
        self.plottype = self.parent.plottype
                                                    # building of the "plot type" field to select in a list
        plottype_list = plottype_getlist()
        try:
            plottype_index = plottype_list.index(self.plottype)
        except:
            plottype_index = 0
            
        if (id != None):
            id.addItems(plottype_list)
            id.setCurrentIndex(plottype_index)
        self.PlotTypeId = id
        return id


    def PlotTypeUpdate(self):
        self.plottype = self.PlotTypeId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def InterpolationInit(self, id=None):        
        self.interpolation = self.parent.interpolation
                                                    # building of the "interpolation" field to select in a list
        interpolation_list = interpolation_getlist()
        try:
            interpolation_index = interpolation_list.index(self.interpolation)
        except:
            interpolation_index = 0
            
        if (id != None):
            id.addItems(interpolation_list)
            id.setCurrentIndex(interpolation_index)
        self.InterpolationId = id
        return id
    

    def InterpolationUpdate(self):
        self.interpolation = self.InterpolationId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapInit(self, id=None):
        self.colormap = self.parent.colormap
                                                    # building of the "color map" field to select in a list
        cmap_list = colormap_getlist()
        icon_list = colormap_icon_getlist()
        icon_path = colormap_icon_getpath()
        try:
            cmap_index = cmap_list.index(self.colormap)
        except:
            cmap_index = 0
            
        if (id != None):
            ###ORIGINAL CODE having some flaw:
            ###- color map list name not really meaning full dor fancy colormap.
            ###- should display colormap miniature next to the colormap name sidebe able to work on values as well as on zimage
            #id.addItems(cmap_list)
            #id.setCurrentIndex(cmap_index)
            ###
            # Color map miniature icon creatione
            for i, cmap in enumerate(cmap_list):
                icon_name = os.path.join(icon_path, icon_list[i])

                # reading icon from file
                if os.path.isfile(icon_name):
                    cmapicon = QtGui.QIcon(icon_name)
                    
                # creating icon directly from colormap
                else:
                    cmapfig = colormap_plot(cmap)
                    cmapicon = QtGui.QPixmap.grabWidget(FigureCanvas(cmapfig))
                    plt.close(cmapfig)

                # updating colomap list
                id.addItem(cmapicon, cmap)
                iconsize = QtCore.QSize(100,16)
                id.setIconSize(iconsize)
                # ... TBD ... automatic resizing of the icon?
                #self.dataentrycombo.setMinimumHeight(self.projecttoolbar.height())
                
            id.setCurrentIndex(cmap_index)
        self.ColorMapId = id
        return id


    def ColorMapUpdate(self):
        self.colormap = self.ColorMapId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapReverseInit(self, id=None):
        self.reverseflag = self.parent.reverseflag
        if (id != None):
            id.setChecked(self.reverseflag)
        self.ColorMapReverseId = id
        return id


    def ColorMapReverseUpdate(self):
        self.reverseflag = self.ColorMapReverseId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def ColorBarDisplayInit(self, id=None):
        self.colorbardisplayflag = self.parent.colorbardisplayflag
        if (id != None):
            id.setChecked(self.colorbardisplayflag)
        self.ColorBarDisplayId = id
        return id


    def ColorBarDisplayUpdate(self):
        self.colorbardisplayflag = self.ColorBarDisplayId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def AxisDisplayInit(self, id=None):
        self.axisdisplayflag = self.parent.axisdisplayflag
        if (id != None):
            id.setChecked(self.axisdisplayflag)
        self.AxisDisplayId = id
        return id


    def AxisDisplayUpdate(self):
        self.axisdisplayflag = self.AxisDisplayId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def ColorBarLogScaleInit(self, id=None):
        self.zmin = self.parent.zmin
        self.zmax = self.parent.zmax
        self.colorbarlogscaleflag = self.parent.colorbarlogscaleflag
                                                    # gets the limits of the histogram of the data set
        zmin, zmax = self.dataset.histo_getlimits()
        if (self.zmin == None):
            self.zmin = zmin
        if (self.zmax == None):
            self.zmax = zmax            
        if (id != None):
            if (self.zmin <= 0):                        # if data values are below or equal to zero
                self.colorbarlogscaleflag = False               
                id.setEnabled(False)   # the data can not be log scaled
            else:
                id.setEnabled(True)            
            id.setChecked(self.colorbarlogscaleflag)
        self.ColorBarLogScaleId = id
        return id


    def ColorBarLogScaleUpdate(self):
        self.colorbarlogscaleflag = self.ColorBarLogScaleId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySpinBoxInit(self, id=None):
        if (id != None):
                                                    # gets the limits of the histogram of the data set
            zmin, zmax = self.dataset.histo_getlimits()
            id.setRange(zmin, zmax)
            id.setValue(self.zmin)
        self.MinValuebySpinBoxId = id
        return id


    def MinimalValuebySpinBoxUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySpinBoxId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
        self.MinValuebySpinBoxId.setValue(self.zmin)    

        self.MinValuebySliderId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySliderInit(self, id=None):
        if (id != None):
            zmin, zmax = self.dataset.histo_getlimits()
            id.setOrientation(QtCore.Qt.Horizontal)
            id.setRange(zmin, zmax)
            id.setValue(self.zmin)
        self.MinValuebySliderId = id
        return id


    def MinimalValuebySliderUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySliderId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
            self.MinValuebySliderId.setValue(self.zmin)    

        self.MinValuebySpinBoxId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySpinBoxInit(self, id=None):
        if (id != None):
            zmin, zmax = self.dataset.histo_getlimits()
            id.setRange(zmin, zmax)
            id.setValue(self.zmax)
        self.MaxValuebySpinBoxId = id
        return id


    def MaximalValuebySpinBoxUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySpinBoxId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySpinBoxId.setValue(self.zmax)    
            
        self.MaxValuebySliderId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySliderInit(self, id=None):
        if (id != None):
            zmin, zmax = self.dataset.histo_getlimits()
            id.setOrientation(QtCore.Qt.Horizontal)
            id.setRange(zmin, zmax)
            id.setValue(self.zmax)
        self.MaxValuebySliderId = id
        return id


    def MaximalValuebySliderUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySliderId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySliderId.setValue(self.zmax)    
            
        self.MaxValuebySpinBoxId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def HistoImageInit(self, id=None):
        self.histofig = None
        self.HistoImageId = id
        self.HistoImageUpdate()
        return id


    def HistoImageUpdate(self):
#        self.histofig = self.dataset.histo_plot(fig=self.histofig, zmin=self.zmin, zmax=self.zmax)
        self.histofig = self.dataset.histo_plot(zmin=self.zmin, zmax=self.zmax)
        #histopixmap = QtGui.QPixmap.grabWidget(self.histofig.canvas)   # builds the pixmap from the canvas
        histopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.histofig))
        histopixmap = histopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.HistoImageId.setPixmap(histopixmap)
        

    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)       # Hides button if real time updating activated
        id.setEnabled(False)                        # disables the button , by default
        return id


    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                     # updates carto image
        self.HistoImageUpdate()
        

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
        
        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.plottype, self.colormap, creversed=self.reverseflag, fig=self.cartofig, interpolation=self.interpolation, cmmin=self.zmin, cmmax=self.zmax, cmapdisplay = self.colorbardisplayflag, axisdisplay = self.axisdisplayflag, logscale=self.colorbarlogscaleflag)        
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))
        cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button
        
        self.wid.setCursor(initcursor)                                  # resets the init cursor
