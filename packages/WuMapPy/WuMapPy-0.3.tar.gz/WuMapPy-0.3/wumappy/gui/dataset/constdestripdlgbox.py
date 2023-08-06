# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.constdestripdlgbox
    --------------------------------------

    Constant destriping dialog box management.

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
# Constant Destriping Dialog Box Object                                     #
#---------------------------------------------------------------------------#
class ConstDestripDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, nprof=0, method='additive', reference='mean', config='mono'):
        '''
        '''
        
        window = cls()
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.rawdataset = parent.dataset  # for display before filter
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
        window.nprof = nprof
        window.method = method
        window.config = config
        window.reference = reference
        window.items_list = [# ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILTOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'RENDERING_ID', 0, 2, False, None, None, 0, 1, 1, 1, 1],
                           ['GroupBox', 'HISTOGRAM_ID', 0, 1, False, None, None, 0, 2, 1, 1, 1],
                           ['GroupBox', 'PROFILESMEAN_ID', 0, 3, False, None, None, 0, 3, 1, 1, 1],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 0, 1, 4, 2],
                           ######################################################################### Filter options
                           ['Label', 'PROFILESNB_ID', 0, 0, False, None, None, 0],  
                           ['SpinBox', '', 1, 0, True, window.ProfilesNbInit, window.ProfilesNbUpdate, 0],
                           ['Label', 'MINIMALVALUE_ID', 2, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 3, 0, True, window.MinimalValuebySpinBoxInit, window.MinimalValuebySpinBoxUpdate, 0],    
                           ['Slider', '', 4, 0, True, window.MinimalValuebySliderInit, window.MinimalValuebySliderUpdate, 0],  
                           ['Label', 'MAXIMALVALUE_ID', 5, 0, False, None, None, 0],  
                           ['DoubleSpinBox', '', 6, 0, True, window.MaximalValuebySpinBoxInit, window.MaximalValuebySpinBoxUpdate, 0],    
                           ['Slider', '', 7, 0, True, window.MaximalValuebySliderInit, window.MaximalValuebySliderUpdate, 0],
                           ['Label', 'DESTRIPINGMETHOD_ID', 8, 0, False, None, None, 0],  
                           ['ComboBox', '', 9, 0, True, window.MethodInit, window.MethodUpdate, 0],   
                           ['Label', 'CONFIGDESTRIP_ID', 10, 0, False, None, None, 0],  
                           ['ComboBox', '', 11, 0, True, window.ConfigInit, window.ConfigUpdate, 0],    
                           ['Label', 'REF_ID', 12, 0, False, None, None, 0],  
                           ['ComboBox', '', 13, 0, True, window.ReferenceInit, window.ReferenceUpdate, 0], 
                           ['Label', '', 14, 0, False, None, None, 0],   
                           ######################################################################### Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 4],   
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 4],   
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 4],   
                           ######################################################################### Histogram
                           ['Image', '', 6, 0, False, window.HistoImageInit, None, 2],
                           ######################################################################### Profiles' mean
                           ['Image', '', 6, 0, False, window.ProfMeanImageInit, None, 3],
                           ######################################################################### Rendering
                           ['Image', '', 0, 1, False, window.CartoImageInit, None, 1]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def ProfilesNbInit(self, id=None):
        if (id != None):
            id.setRange(0, len(self.dataset.data.z_image.T))    # the max is the number of profiles in the dataset
            id.setValue(self.nprof)
        self.ProfilesNbId = id
        return id


    def ProfilesNbUpdate(self):
        self.nprof = self.ProfilesNbId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySpinBoxInit(self, id=None):
        if (id != None):                                                    
            zmin, zmax = self.dataset.histo_getlimits()         # gets the limits of the histogram of the data set
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
        self.HistoImageUpdate()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
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
        self.HistoImageUpdate()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
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
        self.HistoImageUpdate()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
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
        self.HistoImageUpdate()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def HistoImageInit(self, id=None):
        self.HistoImageId = id
        self.HistoImageUpdate()
        return id


    def HistoImageUpdate(self):
        self.histofig = self.dataset.histo_plot(zmin=self.zmin, zmax=self.zmax)
        #histopixmap = QtGui.QPixmap.grabWidget(self.histofig.canvas)   # builds the pixmap from the canvas
        histopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.histofig))   # builds the pixmap from the canvas
        histopixmap = histopixmap.scaledToWidth(SIZE_GRAPH_x)
        self.HistoImageId.setPixmap(histopixmap)
        

    def MethodInit(self, id=None):
        list = destriping_getlist()
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


    def ConfigInit(self, id=None):
        list = destripingconfig_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.config)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ConfigId = id
        return id
            

    def ConfigUpdate(self):
        self.config = self.ConfigId.currentText()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ReferenceInit(self, id=None):
        list = destripingreference_getlist()
        id.addItems(list)
        try:
            index = id.findText(self.reference)
        except:
            index = 0
        id.setCurrentIndex(index)
        self.ReferenceId = id
        return id
            

    def ReferenceUpdate(self):
        self.reference = self.ReferenceId.currentText()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
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
        self.ProfMeanImageUpdate()
        

    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


    def ProfMeanImageInit(self, id=None):
        self.profmeanfig = None
        self.ProfMeanImageId = id
        self.ProfMeanImageUpdate()
        return id

    
    def ProfMeanImageUpdate(self, id=None):
        self.profmeanfig = self.rawdataset.destrip_plotmean(fig=self.profmeanfig, Nprof=self.nprof, method=self.method, reference=self.reference, config=self.config, plotflag='both') # using  dataset to display before/after filter
        pixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.profmeanfig))   # builds the pixmap from the canvas
        pixmap = pixmap.scaledToWidth(SIZE_GRAPH_x)
        self.ProfMeanImageId.setPixmap(pixmap)


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
        self.dataset.destripecon(self.nprof, self.zmin, self.zmax, self.method, self.reference, self.config)

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
        
