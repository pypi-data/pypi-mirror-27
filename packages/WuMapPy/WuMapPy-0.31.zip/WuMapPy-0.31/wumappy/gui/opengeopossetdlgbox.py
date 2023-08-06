# -*- coding: utf-8 -*-
'''
    wumappy.gui.opengeopossetdlgbox
    -----------------------------

    Opening geographics positions set dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from geophpy.geoposset import *
from PySide import QtCore, QtGui

import os, string
import numpy as np
from wumappy.gui.common.cartodlgbox import *
import inspect

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Opening Geoposset Dialog Box Object                                       #
#---------------------------------------------------------------------------#
class OpenGeopossetDlgBox(object):
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, filetype, filenames, refsystem, utm_number, utm_letter, parent=None):
        '''
        '''
        
        window = cls()
        window.title = title
        window.filetype = filetype
        window.filenames = filenames
        window.cartofig = None
        window.parent = parent
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.fig = None
        window.pointindex = 0
        success, window.geoposset = GeoPosSet.from_file(refsystem, utm_letter, utm_number, filetype, filenames)
        window.geoposset.refsystem = refsystem
        window.geoposset.utm_number = utm_number
        window.geoposset.utm_letter = utm_letter
                
        window.items_list = [ \
                           # ELEMENT_NAME - ELEMENT_ID - COLUMN - ROW - FUNCTION_INIT - FUNCTION_UPDATE - NUM_GROUPBOX - (for GB) 0=Vert 1=Hori , COLL SPAN , ROW SPAN
                           ['GroupBox', 'GEOINFO_ID', 0, 0, False, None, None, 0, 0, 1, 1, 0],
                           ['GroupBox', 'UNTITLEDGB_ID', 2, 0, False, None, None, 1, 1, 1, 3, 2],
                           ['GroupBox', 'GEOPOINTLIST_ID',0, 2, False, None, None,3, 0, 1, 1, 1],
                           ['GroupBox', 'RENDERING_ID', 0, 1, False, None, None, 2, 0, 1, 1, 1],
                           ######################################################################### Geographic system options 
                           ['Label', '', 0, 0, False, window.FileNamesInit, None,0],
                           ['Label', 'REFSYSTEM_ID', 1, 0, False, None, None,0],
                           ['ComboBox', '', 2, 0, True, window.RefSystemInit, window.RefSystemUpdate,0],
                           ['Label', 'UTMLETTER_ID', 3, 0, False, window.UtmLetterLabelInit, None,0],
                           ['ComboBox', '', 4, 0, True, window.UtmLetterInit, window.UtmLetterUpdate,0],
                           ['Label', 'UTMNUMBER_ID', 5, 0, False, window.UtmNumberLabelInit, None,0],  
                           ['SpinBox', '', 6, 0, True, window.UtmNumberInit, window.UtmNumberUpdate,0],
                           ######################################################################### Local points coordinates 
                           ['Label', 'POINTNUM_ID', 7, 0, False, None, None,0],
                           ['ComboBox', '', 8, 0, True, window.PointNumInit, window.PointNumUpdate,0],
                           ['CheckBox', 'POINTXYCONVERTED_ID', 9, 0, True, window.PointXYActivationInit, window.PointXYActivationUpdate,0],
                           ['Label', 'POINTX_ID', 10, 0, False, window.PointXLabelInit, None,0],
                           ['DoubleSpinBox', '', 11, 0, True, window.PointXInit, window.PointXUpdate,0],
                           ['Label', 'POINTY_ID', 12, 0, False, window.PointYLabelInit, None,0],
                           ['DoubleSpinBox', '', 13, 0, True, window.PointYInit, window.PointYUpdate,0],
                           ######################################################################### Cancel & Valid buttons
                           ['CancelButton', 'CANCEL_ID', 0, 0, True, window.CancelButtonInit, None,1],
                           ['ValidButton', 'VALID_ID', 0, 1, True, window.ValidButtonInit, None,1],
                           ######################################################################### Controle point list 
                           ['TextEdit', '', 1, 0, True, window.PointsListInit, None,2],   
                           ######################################################################### Rendering 
                           ['Image', '', 0, 1, False, window.CartoImageInit, None,3]]        

        dlgbox = CartoDlgBox("Open geographic position set - " + window.filenames[0], window, window.items_list)  # self.wid is built in CartoDlgBox
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


    def PointsListInit(self, id=None):
        self.PointsListId = id
        id.setReadOnly(True)
        self.PointsListUpdate()
        return id


    def PointsListUpdate(self):
        szPointNum = self.asciiset.getStringValue('POINTNUM_ID')
        szPointX = self.asciiset.getStringValue('POINTX_ID')
        szPointY = self.asciiset.getStringValue('POINTY_ID')
        if (self.geoposset.refsystem == 'UTM'):
            self.UtmNumberLabelId.setEnabled(True)
            self.UtmNumberId.setEnabled(True)
            self.UtmLetterLabelId.setEnabled(True)
            self.UtmLetterId.setEnabled(True)
            szPointEasting = self.asciiset.getStringValue('POINTEASTING_ID')
            szPointNorthing = self.asciiset.getStringValue('POINTNORTHING_ID')
            self.PointsListId.setText("%s\t%s\t%s\t%s\t%s"%(szPointNum, szPointEasting, szPointNorthing, szPointX, szPointY))
        else:
            self.UtmNumberLabelId.setEnabled(False)
            self.UtmNumberId.setEnabled(False)
            self.UtmLetterLabelId.setEnabled(False)
            self.UtmLetterId.setEnabled(False)
            szPointLon = self.asciiset.getStringValue('POINTLONGITUDE_ID')
            szPointLat = self.asciiset.getStringValue('POINTLATITUDE_ID')            
            self.PointsListId.setText("%s\t%s\t%s\t%s\t%s"%(szPointNum, szPointLon, szPointLat, szPointX, szPointY))
            
        maxwidth = 0
        for point in self.geoposset.points_list:
            line = "%s\t%s\t%s\t%s\t%s"%(point[0], point[1], point[2], point[3], point[4])
            self.PointsListId.append(line)
            width = self.PointsListId.fontMetrics().boundingRect(line).width()
            if (width > maxwidth):
                maxwidth = width
        self.PointsListId.setMinimumWidth(1.5*maxwidth)


    def RefSystemInit(self, id=None):
        id.addItems(refsys_getlist())
        id.setCurrentIndex(id.findText(self.geoposset.refsystem))
        self.RefSystemId = id
        return id


    def RefSystemUpdate(self):
        self.geoposset.refsystem = self.RefSystemId.currentText()
        self.PointsListUpdate()


    def UtmLetterLabelInit(self, id=None):
        self.UtmLetterLabelId = id
        return id
       

    def UtmLetterInit(self, id=None):
        utm_minnumber, utm_minletter, utm_maxnumber, utm_maxletter = utm_getzonelimits()
        id.addItems(_letterList(utm_minletter, utm_maxletter))
        id.setCurrentIndex(id.findText(self.geoposset.utm_letter))
        self.UtmLetterId = id
        return id


    def UtmLetterUpdate(self):
        self.geoposset.utm_letter = self.UtmLetterId.currentText()
                
    
    def UtmNumberLabelInit(self, id=None):
        self.UtmNumberLabelId = id
        return id


    def UtmNumberInit(self, id=None):
        utm_minnumber, utm_minletter, utm_maxnumber, utm_maxletter = utm_getzonelimits()
        id.setRange(utm_minnumber, utm_maxnumber)
        id.setValue(self.geoposset.utm_number)
        self.UtmNumberId = id
        return id


    def UtmNumberUpdate(self):
        self.geoposset.utm_number = self.UtmNumberId.value()
                
    
    def PointNumInit(self, id=None):
        for point in self.geoposset.points_list:
            id.addItem(str(point[0]))
        id.setCurrentIndex(self.pointindex)
        self.PointNumId = id
        return id


    def PointNumUpdate(self):
        self.pointindex = self.PointNumId.currentIndex()
        if ((self.geoposset.points_list[self.pointindex][3] != None) and (self.geoposset.points_list[self.pointindex][4] != None)):
            self.PointXId.setValue(self.geoposset.points_list[self.pointindex][3])
            self.PointYId.setValue(self.geoposset.points_list[self.pointindex][4])
            self.PointXYActivationId.setChecked(True)
        else:
            self.PointXYActivationId.setChecked(False)
        
    
    def PointXYActivationInit(self, id=None):
        self.PointXYActivationId = id
        return id


    def PointXYActivationUpdate(self):
        activ = self.PointXYActivationId.isChecked()
        self.PointXLabelId.setEnabled(activ)
        self.PointXId.setEnabled(activ)
        self.PointYLabelId.setEnabled(activ)
        self.PointYId.setEnabled(activ)
        self.PointsListUpdate()
        if (activ == False):
            x = y = None
        else :
            x = self.PointXId.value()
            y = self.PointYId.value()
        self.geoposset.points_list[self.pointindex][3] = x
        self.geoposset.points_list[self.pointindex][4] = y
        self.PointsListUpdate()
        

    def PointXLabelInit(self, id=None):
        self.PointXLabelId = id
        return id


    def PointXInit(self, id=None):
        id.setRange(-10000, 10000)
        self.PointXId = id
        return id


    def PointXUpdate(self):
        x = self.PointXId.value()
        self.geoposset.points_list[self.pointindex][3] = x
        self.PointsListUpdate()
        

    def PointYLabelInit(self, id=None):
        self.PointYLabelId = id
        return id


    def PointYInit(self, id=None):
        id.setRange(-10000, 10000)
        self.PointYId = id
        return id


    def PointYUpdate(self):
        y = self.PointYId.value()
        self.geoposset.points_list[self.pointindex][4] = y
        self.PointsListUpdate()
        

    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


    def CartoImageInit(self, id=None):
        self.cartofig = None
        self.CartoImageId = id
        self.PointNumUpdate()
        self.PointXYActivationUpdate()
        self.CartoImageUpdate()
        return id


    def CartoImageUpdate(self):
        initcursor = self.wid.cursor()              # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)    # sets the wait cursor

        success, self.cartofig = self.geoposset.plot()
        #cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        cartopixmap = QtGui.QPixmap.grabWidget(FigureCanvas(self.cartofig))  # builds the pixmap from the canvas
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)
        
        self.wid.setCursor(initcursor)                                          # resets the init cursor


def _letterList (start, end):
    # add a character at the beginning so str.index won't return 0 for `A`
    a = ' ' + string.ascii_uppercase

    # if start > end, then start from the back
    direction = 1 if start < end else -1

    # Get the substring of the alphabet:
    # The `+ direction` makes sure that the end character is inclusive; we
    # always need to go one *further*, so when starting from the back, we
    # need to substract one. Here comes also the effect from the modified
    # alphabet. For `A` the normal alphabet would return `0` so we would
    # have `-1` making the range fail. So we add a blank character to make
    # sure that `A` yields `1-1=0` instead. As we use the indexes dynamically
    # it does not matter that we have changed the alphabet before.
        
    str = a[a.index(start):a.index(end) + direction:direction]
    list = [str[0]]
    for c in str[1:]:            
        list.append(c)
    return list


