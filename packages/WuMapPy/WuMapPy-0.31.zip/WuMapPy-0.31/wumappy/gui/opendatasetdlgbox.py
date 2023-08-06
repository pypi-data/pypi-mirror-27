# -*- coding: utf-8 -*-
'''
    wumappy.gui.opendatasetdlgbox
    -----------------------------

    Opening dataset dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui

import os
import numpy as np
from wumappy.gui.common.cartodlgbox import *
import inspect

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

SIZE_GRAPH_x = 450

#---------------------------------------------------------------------------#
# Opening Dataset Dialog Box Object                                         #
#---------------------------------------------------------------------------#
class OpenDatasetDlgBox(object):
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, filenames, parent=None,
            xcolnum=1, ycolnum=2, zcolnum=3, delimiter='\t', fileformat='ascii', delimitersasuniqueflag=True, skiprows=1, fieldsrow=0,
            interpgridding = 'none', stepxgridding = None, stepygridding = None, autogriddingflag = True, dispgriddingflag = True,
            festoonfiltflag = False, festoonfiltmethod = 'Crosscorr', festoonfiltshift = 0, festoonfiltcorrmin=0.4, festoonfiltuniformshift=False,
            colormap = "Greys", reverseflag = False,
            peakfiltflag = False, minmaxreplacedflag=False, nanreplacedflag=False, medianreplacedflag=False,
            medianfiltflag = False, nxsize=3, nysize=3, percent=0, gap=0):
        '''
        '''
      
        window = cls()
        window.title = title
        window.delimiter = delimiter
        window.fileformat = fileformat
        window.delimitersasuniqueflag = delimitersasuniqueflag
        window.x_colnum = xcolnum
        window.y_colnum = ycolnum
        window.z_colnum = zcolnum
        window.skiprows = skiprows
        window.fieldsrow = fieldsrow
        window.filenames = filenames
        window.cartofig = None
        window.stepxgridding = stepxgridding
        window.stepygridding = stepygridding
        window.interpgridding = interpgridding
        window.stepxgridding_firstime = True
        window.stepygridding_firstime = True
        window.cache_stepygridding = 0.25
        window.parent = parent
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.autogriddingflag = autogriddingflag
        window.dispgriddingflag = dispgriddingflag
        window.festoonfiltflag = festoonfiltflag
        window.festoonfiltmethod = festoonfiltmethod
        window.festoonfiltshift = festoonfiltshift
        window.festoonfiltcorrmin = festoonfiltcorrmin
        window.festoonfiltuniformshift = festoonfiltuniformshift
        window.valfiltflag = False
        window.dataset = None
        window.colormap = colormap
        window.reverseflag = reverseflag
        window.colorbarlogscaleflag = False
        window.automaticrangeflag = True
        window.peakfiltflag = peakfiltflag
        window.minmaxreplacedflag = minmaxreplacedflag
        window.nanreplacedflag = nanreplacedflag
        window.medianreplacedflag = medianreplacedflag
        window.medianfiltflag = medianfiltflag
        window.nxsize = nxsize
        window.nysize = nysize
        window.percent = percent
        window.gap = gap
        window.histofig = None
                
        # GROUPBOX must be defined first
        window.items_list = [ \
                           # ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'FILEFORMATOPT_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0], \
                           ['GroupBox', 'GRIDINGOPT_ID', 0, 1, False, None, None, 1, 0, 1, 1, 0], \
                           ['GroupBox', 'DISPOPT_ID', 1, 0, False, None, None, 2, 0, 1, 1, 0], \
                           ['GroupBox', 'FILTOPT_ID', 1, 1, False, None, None, 3, 0, 1, 1, 0], \
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 4, 1, 1, 3, 2], \
                           ['GroupBox', 'RENDERING_ID', 0, 2, False, None, None, 5, 0, 1, 1, 1], \
                           ['GroupBox', 'HISTOGRAM_ID', 1, 2, False, None, None, 6, 0, 1, 1, 1], \
                           ######################################################################### File format options 
                           ['Label', 'FILEFORMAT_ID', 0, 0, False, None, None, 0], \
                           ['ComboBox', '', 0, 1, True, window.FileFormatInit, window.FileFormatUpdate, 0],   \
                           ['Label', 'DELIMITER_ID', 1, 0, False, None, None, 0],  \
                           ['ComboBox', '', 1, 1, True, window.DelimiterInit, window.DelimiterUpdate, 0], \
                           ['CheckBox', 'DELIMITERSASUNIQUEFLAG_ID', 2, 1, False, window.SeveralsDelimitersAsUniqueInit, window.SeveralsDelimitersAsUniqueUpdate, 0],  \
                           ['Label', 'SKIPROWS_ID', 3, 0, False, None, None, 0],   \
                           ['SpinBox', '', 3, 1, True, window.SkipRowsNumberInit, window.SkipRowsNumberUpdate, 0], \
                           ['Label', 'FIELDSROW_ID', 4, 0, False, None, None, 0],   \
                           ['SpinBox', '', 4, 1, True, window.FieldsRowIndexInit, window.FieldsRowIndexUpdate, 0], \
                           ['Label', 'XCOLNUM_ID', 5, 0, False, None, None, 0],   \
                           ['SpinBox', '', 5, 1, True, window.XColumnInit, window.XColumnUpdate, 0],    \
                           ['Label', 'YCOLNUM_ID', 6, 0, False, None, None, 0],   \
                           ['SpinBox', '', 6, 1, True, window.YColumnInit, window.YColumnUpdate, 0],    \
                           ['Label', 'ZCOLNUM_ID', 7, 0, False, None, None, 0],   \
                           ['SpinBox', '', 7, 1, True, window.ZColumnInit, window.ZColumnUpdate, 0],    \
                           ['Label', '', 8, 0, False, None, None, 0],
                           ['Label', '', 9, 0, False, None, None, 0],
                           ['Label', '', 10, 0, False, None, None, 0],
                           ######################################################################### Gridding options
                           ['Label', 'STEPXGRIDDING_ID', 0, 0, False, window.GriddingXStepLabelInit, None, 1],    \
                           ['DoubleSpinBox', '', 0, 1, True, window.GriddingXStepInit, window.GriddingXStepUpdate, 1],  \
                           ['Label', 'STEPYGRIDDING_ID', 1, 0, False, window.GriddingYStepLabelInit, None, 1], \
                           ['DoubleSpinBox', '', 1, 1, True, window.GriddingYStepInit, window.GriddingYStepUpdate, 1],  \
                           ['Label', '', 2, 1, False, window.GriddingSizeInit, None, 1],  \
                           ['CheckBox', 'SQUARE_PIXEL', 3, 1, True, window.GriddingSquareInit, window.GriddingSquareUpdate, 1], \
                           ['CheckBox', 'AUTOGRIDDINGFLAG_ID', 4, 1, True, window.GriddingAutoInit, window.GriddingAutoUpdate, 1], \
                           ['CheckBox', 'DISPGRIDDINGFLAG_ID', 5, 1, True, window.GriddingPointsDisplayInit, window.GriddingPointsDisplayUpdate, 1], \
                           ['Label', '', 6, 0, False, None, None, 1],  \
                           ['Label', 'INTERPOLATION_ID', 7, 0, False, None, None, 1],  \
                           ['ComboBox', '', 7, 1, True, window.GriddingInterpolationInit, window.GriddingInterpolationUpdate, 1], \
                           ['Label', '', 8, 0, False, None, None, 1],  \
                           ['CheckBox', 'FESTOONFILT_ID', 9, 0, True, window.FestoonFiltInit, window.FestoonFiltUpdate, 1],  \
                           ['CheckBox', 'FESTOONFILTSHIFT_ID', 9, 1, True, window.FestoonUniformShiftInit, window.FestoonUniformShiftUpdate, 1],  \
                           ['Label', 'FESTOONFILTMETHOD_ID', 10, 0, False, window.FestoonMethodLabelInit, None, 1],  \
                           ['ComboBox', '', 10, 1, True, window.FestoonMethodInit, window.FestoonMethodUpdate, 1],    \
                           ['Label', 'FESTOONFILTSHIFT_ID', 11, 0, False, window.FestoonShiftLabelInit, None, 1],  \
                           ['SpinBox', '', 11, 1, True, window.FestoonShiftInit, window.FestoonShiftUpdate, 1],    \
                           ['Label', 'FESTOONFILTMINCORR_ID', 12, 0, False, window.FestoonCorrMinLabelInit, None, 1],  \
                           ['DoubleSpinBox', '', 12, 1, True, window.FestoonCorrMinInit, window.FestoonCorrMinUpdate, 1],    \
                           ['Label', '', 13, 1, False, None, None, 1],
                           ######################################################################### Display options
                           ['Label', 'COLORMAP_ID', 0, 0, False, None, None, 2],   
                           ['ComboBox', '', 0, 1, True, window.ColorMapInit, window.ColorMapUpdate, 2], 
                           ['CheckBox', 'REVERSEFLAG_ID', 1, 1, True, window.ColorMapReverseInit, window.ColorMapReverseUpdate, 2],  
                           ['CheckBox', 'COLORBARLOGSCALEFLAG_ID', 2, 1, True, window.ColorBarLogScaleInit, window.ColorBarLogScaleUpdate, 2],   
                           ['Label', 'MINIMALVALUE_ID', 3, 0, False, None, None, 2],  
                           ['SpinBox', '', 3, 1, True, window.MinimalValuebySpinBoxInit, window.MinimalValuebySpinBoxUpdate, 2],    
                           ['Slider', '', 4, 1, True, window.MinimalValuebySliderInit, window.MinimalValuebySliderUpdate, 2],  
                           ['Label', 'MAXIMALVALUE_ID', 5, 0, False, None, None, 2],
                           ['SpinBox', '', 5, 1, True, window.MaximalValuebySpinBoxInit, window.MaximalValuebySpinBoxUpdate, 2],    
                           ['Slider', '', 6, 1, True, window.MaximalValuebySliderInit, window.MaximalValuebySliderUpdate, 2], 
                           ['Label', '', 7, 0, False, None, None, 2],
                           ['CheckBox', 'PEAKFILT_ID', 8, 0, True, window.PeakFiltInit, window.PeakFiltUpdate, 2],
                           ['Label', 'LABEL_NANREPLACEDFLAG_ID', 9, 0, False, None, None, 2],
                           ['CheckBox', 'MINMAXREPLACEDFLAG_ID', 9, 1, True, window.MinMaxReplacedValuesInit, window.MinMaxReplacedValuesUpdate, 2],  
                           ['CheckBox', 'NANREPLACEDFLAG_ID', 10, 1, True, window.NanReplacedValuesInit, window.NanReplacedValuesUpdate, 2],  
                           ['CheckBox', 'MEDIANREPLACEDFLAG_ID', 11, 1, True, window.MedianReplacedValuesInit, window.MedianReplacedValuesUpdate, 2],  
                           ['Label', '', 12, 0, False, None, None, 2],
                           ######################################################################### Filter options
                           ['CheckBox', 'MEDIANFILT_ID', 0, 0, True, window.MedianFiltInit, window.MedianFiltUpdate, 3],  \
                           ['Label', 'FILTERNXSIZE_ID', 1, 0, False, window.NxSizeLabelInit, None, 3],  
                           ['SpinBox', '', 1, 1, True, window.NxSizeInit, window.NxSizeUpdate, 3],    
                           ['Label', 'FILTERNYSIZE_ID', 2, 0, False, window.NySizeLabelInit, None, 3],  
                           ['SpinBox', '', 2, 1, True, window.NySizeInit, window.NySizeUpdate, 3],    
                           ['Label', 'MEDIANFILTERPERCENT_ID', 3, 0, False, window.PercentLabelInit, None, 3],  
                           ['SpinBox', '', 3, 1, True, window.PercentInit, window.PercentUpdate, 3],    
                           ['Label', 'MEDIANFILTERGAP_ID', 4, 0, False, window.GapLabelInit, None, 3],  
                           ['SpinBox', '', 4, 1, True, window.GapInit, window.GapUpdate, 3],
                           ['Label', '', 5, 0, False, None, None, 3],
                           ['Label', '', 6, 0, False, None, None, 3],
                           ['Label', '', 7, 0, False, None, None, 3],
                           ['Label', '', 8, 0, False, None, None, 3],
                           ['Label', '', 9, 0, False, None, None, 3],
                           ['Label', '', 10, 0, False, None, None, 3],
                           ######################################################################### Cancel, Update, Valid
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None, 4],
                           ['MiscButton', 'DISPUPDATE_ID', 0, 1, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate, 4],   \
                           ['ValidButton', 'VALID_ID', 0, 2, True, window.ValidButtonInit, None, 4],   \
                           ######################################################################### Histogram
                           ['Image', '', 0, 0, False, window.HistoImageInit, None, 6],   
                           ######################################################################### Rendering
                           ['Image', '', 1, 0, False, window.CartoImageInit, None, 5]]
        
        dlgbox = CartoDlgBox("Open dataset - " + window.filenames[0], window, window.items_list)  # self.wid is built in CartoDlgBox
        dlgbox.exec()


        return dlgbox.result(), window


    def FileNamesInit(self, id=None):
        filenames=""
        n = len(self.filenames)
        for i in range(n):
            filenames = filenames + self.filenames[i]
            if (i<(n-1)):
                filenames = filenames + '\n'
        id.setText(filenames)
        return id


    def FileFormatInit(self, id=None):
        formatlist = fileformat_getlist()
        id.addItems(formatlist)
        index = id.findText(self.fileformat)
        id.setCurrentIndex(index)
        self.FileFormatId = id
        return id


    def FileFormatUpdate(self):
        self.fileformat = self.FileFormatId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        
    
    def DelimiterInit(self, id=None):
        id.addItems(['.', ',', ';', 'space', 'tab', '|', '-'])
        if (self.delimiter == ' '):
            delimiter = 'space'
        elif (self.delimiter == '\t'):
            delimiter = 'tab'
        else:
            delimiter = self.delimiter
        index = id.findText(delimiter)
        id.setCurrentIndex(index)
        self.DelimiterId = id
        return id


    def DelimiterUpdate(self):
        self.delimiter = self.DelimiterId.currentText()
        if (self.delimiter == 'space'):
            self.delimiter = ' '
        elif (self.delimiter == 'tab'):
            self.delimiter = '\t'
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True


    def SeveralsDelimitersAsUniqueInit(self, id=None):
        id.setChecked(self.delimitersasuniqueflag)
        self.SeveralsDelimiterAsUniqueId = id
        return id


    def SeveralsDelimitersAsUniqueUpdate(self):
        self.delimitersasuniqueflag = self.SeveralsDelimiterAsUniqueId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def SkipRowsNumberInit(self, id=None):
        id.setValue(self.skiprows)
        self.SkipRowsNumberId = id
        return id


    def SkipRowsNumberUpdate(self):
        self.skiprows = self.SkipRowsNumberId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        
    
    def FieldsRowIndexInit(self, id=None):
        id.setValue(self.fieldsrow)
        self.FieldsRowIndexId = id
        return id


    def FieldsRowIndexUpdate(self):
        self.fieldsrow = self.FieldsRowIndexId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        

    def GriddingSquareInit(self, id=None):
        if (id != None):
          id.setChecked(False)
          self.square_pixel = id
          self.GriddingYStepId.setEnabled(not id.isChecked())
        return id


    def GriddingSquareUpdate(self):
        if self.square_pixel.isChecked():
          self.cache_stepygridding = self.GriddingYStepId.value()
          self.stepygridding = self.GriddingXStepId.value()

        else:
          self.stepygridding = self.cache_stepygridding

        self.GriddingYStepLabelId.setEnabled(not self.square_pixel.isChecked())
        self.GriddingYStepId.setEnabled(not self.square_pixel.isChecked())

        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate() 

    
    def GriddingAutoInit(self, id=None):
        if (id != None):
            id.setChecked(self.autogriddingflag)
            if (self.autogriddingflag == True):
               self.stepxgridding = None
               self.stepygridding = None
               Enabled = False
            else:
               Enabled = True
        self.GriddingAutoId = id
        return id


    def GriddingAutoUpdate(self):
        self.stepxgridding = None
        self.stepygridding = None
        self.autogriddingflag = self.GriddingAutoId.isChecked()
        if (self.autogriddingflag == True):
           self.stepxgridding = None
           self.stepygridding = None
           Enabled = False
        else:
           Enabled = True
        self.GriddingXStepLabelId.setEnabled(Enabled)
        self.GriddingXStepId.setEnabled(Enabled)
        self.GriddingYStepLabelId.setEnabled(Enabled)
        self.square_pixel.setEnabled(Enabled) #AB# Gestion du enable Y input
        self.square_pixel.setChecked(False) #AB# redéfinit l'option à décoché
        self.GriddingYStepId.setEnabled(Enabled)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def GriddingPointsDisplayInit(self, id=None):
        self.GriddingPointsDisplayId = id
        if (id != None):
            id.setChecked(self.dispgriddingflag)
        return id


    def GriddingPointsDisplayUpdate(self):
        self.dispgriddingflag = self.GriddingPointsDisplayId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def GriddingXStepLabelInit(self, id=None):
        id.setEnabled(not self.autogriddingflag)
        self.GriddingXStepLabelId = id
        return id

    
    def GriddingXStepInit(self, id=None):
        id.setSingleStep(0.25)
        id.setEnabled(not self.autogriddingflag)
        self.GriddingXStepId = id
        return id


    def GriddingXStepUpdate(self):
        if (self.square_pixel.isChecked()): #AB# Ajout de la gestion de square grid
          self.stepygridding = self.GriddingXStepId.value()
        self.stepxgridding = self.GriddingXStepId.value()
        if (self.stepxgridding_firstime == False):
            if (self.realtimeupdateflag):                       
                self.CartoImageUpdate()                             # updates carto only if real time updating activated
            else:
                self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
                self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
                self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        else:
            self.stepxgridding_firstime = False
        
    
    def GriddingYStepLabelInit(self, id=None):
        id.setEnabled(not self.autogriddingflag)
        self.GriddingYStepLabelId = id
        return id

    
    def GriddingYStepInit(self, id=None):
        id.setSingleStep(0.25)
        id.setEnabled(not self.autogriddingflag)
        self.GriddingYStepId = id
        return id

    
    def GriddingYStepUpdate(self):
        self.stepygridding = self.GriddingYStepId.value()
        if (self.stepygridding_firstime == False):
            if (self.realtimeupdateflag):                       
                self.CartoImageUpdate()                             # updates carto only if real time updating activated
            else:
                self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
                self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
                self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        else:
            self.stepygridding_firstime = False


    def GriddingSizeInit(self, id=None):
        self.GriddingSizeId = id
        return id


    def GriddingSizeUpdate(self):
        text = "%s (%s * %s)"%(self.asciiset.getStringValue('SIZEGRIDDING_ID'), self.rowsnb, self.colsnb)
        self.GriddingSizeId.setText(text)
        
    
    def GriddingInterpolationInit(self, id=None):
                                                                    # building of the "interpolation" field to select in a list
        interpolation_list = griddinginterpolation_getlist()
        try:
            interpolation_index = interpolation_list.index(self.interpgridding)
        except:
            interpolation_index = 0
            
        if (id != None):
            id.addItems(interpolation_list)
            id.setCurrentIndex(interpolation_index)
        self.GriddingInterpolationId = id
        return id


    def GriddingInterpolationUpdate(self):        
        self.interpgridding = self.GriddingInterpolationId.currentText()
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        
    
    def XColumnInit(self, id=None):
        id.setValue(self.x_colnum)
        self.XColumnId = id
        return id

    
    def XColumnUpdate(self):
        self.x_colnum = self.XColumnId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True

    
    def YColumnInit(self, id=None):
        id.setValue(self.y_colnum)
        self.YColumnId = id
        return id

    
    def YColumnUpdate(self):
        self.y_colnum = self.YColumnId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True

    
    def ZColumnInit(self, id=None):
        id.setValue(self.z_colnum)
        self.ZColumnId = id
        return id


    def ZColumnUpdate(self):
        self.z_colnum = self.ZColumnId.value()
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def FestoonUniformShiftInit(self, id=None):
        if (id != None):
            id.setChecked(self.festoonfiltuniformshift)
            id.setEnabled(self.festoonfiltflag)
        self.FestoonUniformShiftId = id
        return id


    def FestoonUniformShiftUpdate(self):
        self.festoonfiltuniformshift = self.FestoonUniformShiftId.isChecked()
        self.FestoonShiftLabelId.setEnabled(self.festoonfiltuniformshift)
        self.FestoonShiftId.setEnabled(self.festoonfiltuniformshift)

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button

        
    def FestoonFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.festoonfiltflag)
        self.FestoonFiltId = id
        return id


    def FestoonFiltUpdate(self):
        self.festoonfiltflag = self.FestoonFiltId.isChecked()
        
        self.FestoonMethodLabelId.setEnabled(self.festoonfiltflag)
        self.FestoonMethodId.setEnabled(self.festoonfiltflag)
        
        self.FestoonUniformShiftId.setEnabled(self.festoonfiltflag)
        
        self.FestoonCorrMinLabelId.setEnabled(self.festoonfiltflag)
        self.FestoonCorrMinId.setEnabled(self.festoonfiltflag)
        
        self.FestoonUniformShiftUpdate()
        if not self.festoonfiltflag:
            self.FestoonShiftId.setEnabled(self.festoonfiltflag)
            self.FestoonShiftLabelId.setEnabled(self.festoonfiltflag)
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button

        

    def FestoonMethodLabelInit(self, id=None):
        id.setEnabled(self.festoonfiltflag)
        self.FestoonMethodLabelId = id
        return id


    def FestoonMethodInit(self, id=None):
                                                    # building of the "plot type" field to select in a list
        method_list = ['Crosscorr','Pearson', 'Spearman', 'Kendall']  # festoonfiltmethod_getlist()
        try:
            method_index = method_list.index(self.festoonfiltmethod)
        except:
            method_index = 0
            
        if (id != None):
            id.addItems(method_list)
            id.setCurrentIndex(method_index)
            id.setEnabled(self.festoonfiltflag)
        self.FestoonMethodId = id
        return id


    def FestoonMethodUpdate(self):
        self.festoonfiltmethod = self.FestoonMethodId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def FestoonShiftLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.festoonfiltuniformshift)
        self.FestoonShiftLabelId = id
        return id


    def FestoonShiftInit(self, id=None):
        if (id != None):                                                    
            range = 400 # TEMP
            id.setRange(-range, +range)
            id.setValue(self.festoonfiltshift)
            id.setEnabled(self.festoonfiltuniformshift)
        self.FestoonShiftId = id
        return id


    def FestoonShiftUpdate(self):
        self.festoonfiltshift = self.FestoonShiftId.value()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def FestoonCorrMinLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.festoonfiltuniformshift)
        self.FestoonCorrMinLabelId = id
        return id

    
    def FestoonCorrMinInit(self, id=None):
        if (id != None):
            id.setRange(0, 1.0)
            id.setSingleStep(0.1)
            id.setValue(self.festoonfiltcorrmin)
            id.setEnabled(self.festoonfiltflag)
        self.FestoonCorrMinId = id
        return id

    
    def FestoonCorrMinUpdate(self, id=None):
        self.festoonfiltcorrmin = self.FestoonCorrMinId.value()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button

    

    def PeakFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.peakfiltflag)
        self.PeakFiltId = id
        return id


    def PeakFiltUpdate(self):
        self.peakfiltflag = self.PeakFiltId.isChecked()

        # Enables/diable other checkboxes
        self.MinMaxReplacedValuesId.setEnabled(self.peakfiltflag)
        self.NanReplacedValuesId.setEnabled(self.peakfiltflag)
        self.MedianReplacedValuesId.setEnabled(self.peakfiltflag)

        # Uchecking all boxes if diabled
        if ~self.peakfiltflag:
            self.MinMaxReplacedValuesId.setChecked(False)
            self.NanReplacedValuesId.setChecked(False)
            self.MedianReplacedValuesId.setChecked(False)            
        
        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def MinMaxReplacedValuesInit(self, id=None):
        if (id != None):
            id.setEnabled(self.peakfiltflag)
            id.setChecked(self.minmaxreplacedflag)
        self.MinMaxReplacedValuesId = id
        return id


    def MinMaxReplacedValuesUpdate(self):
        self.minmaxreplacedflag = self.MinMaxReplacedValuesId.isChecked()
        
        # Unchecking the other boxes
        if self.minmaxreplacedflag:
            self.NanReplacedValuesId.setChecked(False)
            self.MedianReplacedValuesId.setChecked(False)
        
        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            HistoImageUpdate()                                  # updates histo only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)

            
    def NanReplacedValuesInit(self, id=None):
        if (id != None):
            id.setEnabled(self.peakfiltflag)
            id.setChecked(self.nanreplacedflag)
        self.NanReplacedValuesId = id
        return id


    def NanReplacedValuesUpdate(self):
        self.nanreplacedflag = self.NanReplacedValuesId.isChecked()

        # Unchecking the other boxes
        if self.nanreplacedflag:
            self.MinMaxReplacedValuesId.setChecked(False)
            self.MedianReplacedValuesId.setChecked(False)

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            HistoImageUpdate()                                  # updates histo only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def MedianReplacedValuesInit(self, id=None):
        if (id != None):
            id.setEnabled(self.peakfiltflag)
            id.setChecked(self.medianreplacedflag)
        self.MedianReplacedValuesId = id
        return id


    def MedianReplacedValuesUpdate(self):
        self.medianreplacedflag = self.MedianReplacedValuesId.isChecked()

        # Unchecking the other boxes
        if self.medianreplacedflag:
            self.MinMaxReplacedValuesId.setChecked(False)
            self.NanReplacedValuesId.setChecked(False)
            
        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def MedianFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.medianfiltflag)
        self.MedianFiltId = id
        return id


    def MedianFiltUpdate(self):
        self.medianfiltflag = self.MedianFiltId.isChecked()
        
        self.NxSizeLabelId.setEnabled(self.medianfiltflag)
        self.NxSizeId.setEnabled(self.medianfiltflag)

        self.NySizeLabelId.setEnabled(self.medianfiltflag)
        self.NySizeId.setEnabled(self.medianfiltflag)

        self.PercentId.setEnabled(self.medianfiltflag)
        self.PercentLabelId.setEnabled(self.medianfiltflag)

        self.GapId.setEnabled(self.medianfiltflag)
        self.GapLabelId.setEnabled(self.medianfiltflag)
        
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def NxSizeLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.NxSizeLabelId = id
        return id


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
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


    def NySizeLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.NySizeLabelId = id
        return id


    def NySizeInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
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


    def PercentLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.PercentLabelId = id
        return id


    def PercentInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
            id.setRange(0, 100)
            id.setValue(self.percent)
        self.PercentId = id
        return id


    def PercentUpdate(self):
        self.percent = self.PercentId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def GapLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.GapLabelId = id
        return id


    def GapInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
            id.setRange(0, 100)
            id.setValue(self.gap)
        self.GapId = id
        return id


    def GapUpdate(self):
        self.gap = self.GapId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapInit(self, id=None):
                                                    # building of the "color map" field to select in a list
        cmap_list = colormap_getlist()
        icon_list = colormap_icon_getlist()
        icon_path = colormap_icon_getpath()
        try:
            cmap_index = cmap_list.index(self.colormap)
        except:
            cmap_index = 0
            
        if (id != None):
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
            
            id.setCurrentIndex(cmap_index)
        self.ColorMapId = id
        return id


    def ColorMapUpdate(self):
        self.colormap = self.ColorMapId.currentText()

        # Auto update GUI
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated

        # Manual update GUI
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapReverseInit(self, id=None):
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
        

    def ColorBarLogScaleInit(self, id=None):
        self.ColorBarLogScaleId = id
        return id


    def ColorBarLogScaleReset(self):
                                                        # gets the limits of the histogram of the data set
        zmin, zmax = self.dataset.histo_getlimits()
        if (zmin <= 0):                                 # if data values are below or equal to zero
            self.colorbarlogscaleflag = False               
            self.ColorBarLogScaleId.setEnabled(False)   # the data can not be log scaled
        else:
            self.ColorBarLogScaleId.setEnabled(True)            
        self.ColorBarLogScaleId.setChecked(self.colorbarlogscaleflag)


    def ColorBarLogScaleUpdate(self):
        self.colorbarlogscaleflag = self.ColorBarLogScaleId.isChecked()
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
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
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
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
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
            self.HistoImageUpdate()
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
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def HistoImageInit(self, id=None):
        self.HistoImageId = id
        return id

    #AB# 
    def HistoImageUpdate(self):
        self.histofig = self.dataset.histo_plot(fig=self.histofig, zmin=self.zmin, zmax=self.zmax) #AB# n'affiche pas de label x + y car VIDE (histofig)
        #histopixmap = QtGui.QPixmap.grabWidget(self.histofig.canvas)   # builds the pixmap from the canvas
        histopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.histofig))
        histopixmap = histopixmap.scaledToWidth(SIZE_GRAPH_x) #AB# DEFAULT 200
        self.HistoImageId.setPixmap(histopixmap)
        

    def DispUpdateButtonInit(self, id=None):
        id.setEnabled(False)                        # disables the button , by default
        if (self.realtimeupdateflag == True):
            id.setHidden(self.realtimeupdateflag)   # Hides button if real time updating activated
        self.DispUpdateButtonId = id
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

        first = True

        initcursor = self.wid.cursor()              # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)    # sets the wait cursor
        
                                                    # gets the fields values
                                                    
        for n in range(len(self.filenames)):
            # treats data values
            colsnb = getlinesfrom_file(self.filenames[n], self.fileformat, self.delimiter, self.delimitersasuniqueflag, self.skiprows, 10)[0]

            if (first == True):
                datacolsnb = colsnb
            else:
                if (colsnb != datacolsnb):
                    datacolsnb = 0

        if (datacolsnb >= 3) :
            self.XColumnId.setRange(1, datacolsnb)
            self.YColumnId.setRange(1, datacolsnb)
            self.ZColumnId.setRange(1, datacolsnb)

        try:
            # opens temporary files
            success, self.dataset = DataSet.from_file(self.filenames, fileformat=self.fileformat, delimiter=self.delimiter, x_colnum=self.x_colnum, y_colnum=self.y_colnum, z_colnum=self.z_colnum, skipinitialspace=self.delimitersasuniqueflag, skip_rows=self.skiprows, fields_row=self.fieldsrow)               

            # makes the z image
            self.dataset.interpolate(interpolation=self.interpgridding, x_delta=self.stepxgridding, y_delta=self.stepygridding, x_decimal_maxnb=2, y_decimal_maxnb=2, x_frame_factor=0., y_frame_factor=0.)
            self.colsnb = len(self.dataset.data.z_image)
            self.rowsnb = len(self.dataset.data.z_image[0])
            self.GriddingSizeUpdate()

            # processes peak filtering if flag enabled
            if (self.peakfiltflag):
                self.dataset.peakfilt(self.zmin, self.zmax, self.medianreplacedflag, self.nanreplacedflag, self.valfiltflag)

            # processes festoon filtering if flag enabled
            if (self.festoonfiltflag):
                self.dataset.festoonfilt(method=self.festoonfiltmethod,
                                         shift=self.festoonfiltshift,
                                         corrmin=self.festoonfiltcorrmin,
                                         uniformshift=self.festoonfiltuniformshift,
                                         valfilt=self.valfiltflag)

            # processes median filtering if flag enabled
            if (self.medianfiltflag):
                self.dataset.medianfilt(self.nxsize, self.nysize, self.percent, self.gap, self.valfiltflag)

            # resets limits of input parameters
            if (self.automaticrangeflag):
                self.automaticrangeflag = False
                self.zmin, self.zmax = self.dataset.histo_getlimits()
                self.ColorBarLogScaleReset()
                self.MaximalValuebySpinBoxReset()
                self.MaximalValuebySliderReset()
                self.MinimalValuebySpinBoxReset()
                self.MinimalValuebySliderReset()
                
            # plots geophysical image
            if (self.peakfiltflag):     # displays all values to verify peak filtering effects
                cmmin = None            
                cmmax = None
            else:                       # display filtering only
                cmmin = self.zmin
                cmmax = self.zmax
            
            self.cartofig, cartocmap = self.dataset.plot(self.dataset.info.plottype, self.colormap, cmmin=cmmin, cmmax=cmmax, fig=self.cartofig, interpolation='none', creversed=self.reverseflag, logscale=self.colorbarlogscaleflag, pointsdisplay=self.dispgriddingflag)
            self.GriddingXStepId.setValue(self.dataset.info.x_gridding_delta)
            self.dataset.info.x_gridding_delta = self.GriddingXStepId.value()    # to be sure than the value in the dialog box is not the real value arounded
            self.GriddingYStepId.setValue(self.dataset.info.y_gridding_delta)
            self.dataset.info.y_gridding_delta = self.GriddingYStepId.value()    # to be sure than the value in the dialog box is not the real value arounded
            self.interpgridding = self.dataset.info.gridding_interpolation
            self.stepxgridding = self.dataset.info.x_gridding_delta
            self.stepygridding = self.dataset.info.y_gridding_delta
            #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
            cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))
            cartopixmap = cartopixmap.scaledToWidth(SIZE_GRAPH_x) #AB# TAILLE EN FONCTION DE SIZE X ET SIZE Y
            self.CartoImageId.setPixmap(cartopixmap)
            self.CartoImageId.setEnabled(True)                              # enables the carto image
            self.ValidButtonId.setEnabled(True)
        except Exception as e:
            self.cartofig, cartocmap = None, None
            self.CartoImageId.setEnabled(False)                             # disables the carto image
            self.ValidButtonId.setEnabled(False)

        self.DispUpdateButtonId.setEnabled(False)                           # disables the display update button

        self.wid.setCursor(initcursor)                                          # resets the init cursor

        if (not self.realtimeupdateflag): #Permet de debug le probleme du non refresh de l'hystogramme quand realtime n'est pas definit
          self.HistoImageUpdate()
