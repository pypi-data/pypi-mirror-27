# -*- coding: utf-8 -*-
'''
    wumappy.gui.common.cartodlgbox
    ------------------------------

    Common dialog box management with cartography object.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
import numpy as np

#from win32api import GetSystemMetrics

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure

class Item():
    id = None       # item identifiant
    type = None     # item type, 'CheckBox', 'ComboBox', 'SpinBox', 'DoubleSpinBox', 'Label', 'ValidButton', 'CancelButton', 'MiscButton' ...
    init = None     # item init() function
    update = None   # item update() function
    


class QCarto(QtGui.QLabel):

    clicked=QtCore.Signal(QtGui.QMouseEvent)

    def __init__(self, x_min=None, x_max=None, x_gridding_delta=None, y_min=None, y_max=None, y_gridding_delta=None):
        super(QCarto, self).__init__()
        self.x_min = x_min
        self.x_max = x_max
        self.x_gridding_delta = x_gridding_delta
        self.y_min = y_min
        self.y_max = y_max
        self.y_gridding_delta = y_gridding_delta
        self.width = None
        self.height = None
        
        if ((x_min == None) or (x_max == None) or (x_gridding_delta == None) or (y_min == None) or (y_max == None) or (y_gridding_delta == None)):
            self.availablepositionflag = False
        else:
            self.availablepositionflag = True
            

    def getPosition(self, event):
        pos = event.pos()
        x = self.x_min + (pos.x() * (self.x_max - self.x_min))/self.width
        y = self.y_max - (pos.y() * (self.y_max - self.y_min))/self.height
        return x, y
        

    def event(self, event):
        if ((event.type() == QtCore.QEvent.ToolTip) and self.availablepositionflag and (self.width!=None) and (self.height!=None)):
            ###
            w, h = self.getSize()
            self.setSize(w, h)
            ###
            x, y = self.getPosition(event)
            QtGui.QToolTip.showText(event.globalPos(), "(%.02f,%.02f)"%(x, y))
        return super(QCarto, self).event(event)


    ###
    def getSize(self):
        w = self.geometry().width()
        h = self.geometry().height()
        return w, h 
    ###

    def setSize(self, w, h):
        self.width = w
        self.height = h
        
        

    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            if (self.update != None):
                ###
                w, h = self.getSize()
                self.setSize(w, h)
                ###
                x, y = self.getPosition(event)
                self.update(x, y)



#---------------------------------------------------------------------------#
# Display Carto Dialog Box Object                                           #
#---------------------------------------------------------------------------#
class CartoDlgBox(QtGui.QDialog):

    def __init__(self, title, parent, it_list):
        '''
        Parameters :
        :title: title of dialog box
        :parent: parent windows object
        :it_list: list of items to add in the dialog box.
            [type, label, col_index, isavailable, init, update],... , with :
            :type: item type, 'CheckBox', 'ComboBox', 'SpinBox', 'Label', 'DoubleSpinBox', 'Slider', 'Carto', 'ValidButton', 'CancelButton', 'MiscButton', ...
            :label: item label.
            :col_index: index of the column to display item, 0,1, ...
            :isavailable: True if item is available, False if not.
            :init: initialisation function for item init(), 'None' if no function.
            :update: update function for item update(), 'None' if no function.
        '''
        super(CartoDlgBox, self).__init__()

        group_box_tab = []  # GROUPBOX list
        group_tab = []  # tabWidget list
        layout_tab = []  # layout list

        self.asciiset = parent.asciiset
        self.icon = parent.icon
        self.setFont(self.asciiset.font)
        self.items_list = []

        layout = QtGui.QGridLayout()                # builds the main layout
                                                    # the main layout will be composed by 2 layouts as columns

        change_resolution = parent.configset.getboolean('MISC', 'changeresolutionflag')

        parent.wid = self

        self.setWindowTitle(title)                  # sets the windows title
        self.setWindowIcon(self.icon)               # sets the wumappy logo as window icon

        
        a = 0
        col_nb = 0                                  # number of columns        
        for it in it_list:
            col_index = it[3]
            if ((1+col_index) > col_nb):
                col_nb = 1 + col_index
            a += 1
         
        for it in it_list:
            item = Item()
            item.type = it[0]
            label = self.asciiset.getStringValue(it[1])
            row_index = it[2]
            col_index = it[3]
            isavailable = it[4]
            item.init = it[5]
            item.update = it[6]

            isValid = True

            if (item.type == 'CheckBox'):
                item.id = QtGui.QCheckBox(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ComboBox'):
                item.id = QtGui.QComboBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'SpinBox'):
                item.id = QtGui.QSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'DoubleSpinBox'):
                item.id = QtGui.QDoubleSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Slider'):
                item.id = QtGui.QSlider()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Label'):
                item.id = QtGui.QLabel(label)
                item.id.setFont(self.asciiset.font)
                item.id.setWordWrap(True)
            elif (item.type == 'TextEdit'):
                item.id = QtGui.QTextEdit(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Image'):
                try:
                    item.id = QCarto(parent.dataset.info.x_min, parent.dataset.info.x_max, parent.dataset.info.x_gridding_delta, parent.dataset.info.y_min, parent.dataset.info.y_max, parent.dataset.info.y_gridding_delta)
                except:
                    item.id = QCarto()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ValidButton'):
                item.id = QtGui.QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'CancelButton'):
                item.id = QtGui.QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'MiscButton'):
                item.id = QtGui.QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'GroupBox'):
                    if (change_resolution):
                        if (it[11] != 2):
                            if len(group_tab) == it[11]:
                                group_tab.append(QtGui.QTabWidget())
                                layout.addWidget(group_tab[-1], row_index, col_index)
                            item.id = QtGui.QWidget()
                            group_tab[it[11]].addTab(item.id, label)
                        else:
                            item.id = QtGui.QGroupBox(label)
                        item.id.setFont(self.asciiset.font)
                        group_box_tab.append(item.id)
                        layout_tab.append(QtGui.QGridLayout())
                        group_box_tab[-1].setLayout(layout_tab[-1])
                        if (it[11] == 1 or it[11] == 0):
                            layout.addWidget(group_tab[-1], 0, 0, it[9], it[10])
                        else:
                            layout.addWidget(item.id, row_index, col_index, it[9], it[10])
                    else:
                        item.id = QtGui.QGroupBox(label)
                        item.id.setFont(self.asciiset.font)
                        group_box_tab.append(item.id)
                        layout_tab.append(QtGui.QGridLayout())
                        item.id.setLayout(layout_tab[-1])
                        layout.addWidget(item.id, row_index, col_index, it[9], it[10])
            else:
                isValid = False

            # Initialisaton des Signaux et fonction d'init
            if ((isValid == True) and (col_index >= 0) and (col_index < col_nb)):
                self.items_list.append(item)
                if (col_index == (col_nb - 1)):
                    col_index = 0

                if (item.init != None):                    
                    item.id = item.init(item.id)

                if (item.type == 'CheckBox'):
                    if (item.update != None):
                        item.id.stateChanged.connect(item.update)
                elif (item.type == 'ComboBox'):
                    if (item.update != None):
                        item.id.currentIndexChanged.connect(item.update)
                elif (item.type == 'SpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'DoubleSpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'Slider'):
                    if (item.update != None):
                        item.id.sliderReleased.connect(item.update)
                elif (item.type == 'Image'):
                    item.id.update = item.update
                elif (item.type == 'ValidButton'):
                    item.id.clicked.connect(self.valid)
                elif (item.type == 'CancelButton'):
                    item.id.clicked.connect(self.cancel)
                elif (item.type == 'MiscButton'):
                    if (item.update != None):
                        item.id.clicked.connect(item.update)                    

            if not group_box_tab:
                layout.addWidget(item.id, row_index, col_index)
            elif (item.type == 'Label'):
                layout_tab[it[7]].addWidget(item.id, it[2], it[3], 1, 1)
            elif (item.type != 'GroupBox'):
                layout_tab[it[7]].addWidget(item.id, it[2], it[3], 1, 1)
        self.update()
        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)    # to not authorize size modification
        self.setLayout(layout)

    def valid(self):
        '''
        Closes the dialog box
        '''
        self.accept()
        self.close()        


    def cancel(self):
        '''
        Closes the dialog box
        '''
        self.close()
