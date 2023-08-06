# -*- coding: utf-8 -*-
'''
    wumappy.misc.asciiset
    ---------------------

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import unicode_literals
import numpy as np
import glob                         # for managing severals files thanks to "*." extension
from PySide import QtGui
import csv, os, platform
from os.path import expanduser

res_dir = "/resources"        # resources directory

english_array = [   \
    # string_id,   string_value
    ['FILEFORMATOPT_ID', "File format options"],
    ['GRIDINGOPT_ID', "Gridding options"],
    ['DISPOPT_ID', "Display options"],
    ['FILTOPT_ID', "Filter options"],
    ['UNTITLEDGB_ID', ""],
    ['HISTOGRAM_ID', "Histogram"],
    ['RENDERING_ID', "Rendering"],
    ['CONFIG_ID', "Configuration"],
    #################################### WuMapPy Main menu
    ########################## Files
    ['FILES_ID',"Files"],
    ['DATASET_ID', "Data set"],
    ['OPEN_ID', "Open"], 
    ['IMPORT_ID', "Import"], 
    ['FROMASCIIFILES_ID', "From ASCII files"], 
    ['GEOPOSSET_ID', "Geographics positions set"],
    ['FROMSHAPEFILES_ID', "From shape files"],
    ['EXIT_ID', "Exit"],  
    ########################## Settings
    ['SETTINGS_ID', "Settings"],
    ['LANGUAGE_ID', "Language"],
    ['FONT_ID', "Font"],
    ['FONTNAME_ID', "Font name"],   
    ['FONTSIZE_ID', "Font size"],
    ['MISCSETTINGS_ID', "Miscellaneous settings"],
    ['RTUPDATE_ID', "Real time update"],
    ['CHANGE_RESOLUTION_ID', "Group Box Format"],
    ########################## Help
    ['HELP_ID', "Help"],
    ['WUMAPPYHELP_ID', "WuMapPy"],
    ['GEOPHPYHELP_ID', "GeophPy"],
    ['ABOUT_ID', "About"],    
    ['PDFUSERMANUAL_ID', "Pdf user manual"],  
    ['HTMLUSERMANUAL_ID', "Html user manual"], 
    #################################### Open dataset menu
    ########################## File format options
    ['FILEFORMAT_ID', "File format"],    
    ['DELIMITER_ID', "Delimiter"],   
    ['DELIMITERSASUNIQUEFLAG_ID', "Several consecutives as unique"],   
    ['SKIPROWS_ID', "Skip raws number"], 
    ['FIELDSROW_ID', "Fields row index"], 
    ['XCOLNUM_ID', "X column"],  
    ['YCOLNUM_ID', "Y column"],  
    ['ZCOLNUM_ID', "Z column"],  
    ########################## Gridding options
    ['SQUARE_PIXEL', "Square Pixels"],
    ['AUTOGRIDDINGFLAG_ID', "Automatical gridding"],  
    ['DISPGRIDDINGFLAG_ID', "Gridding points display"], 
    ['STEPXGRIDDING_ID', "Gridding X step"], 
    ['STEPYGRIDDING_ID', "Gridding Y step"], 
    ['INTERPOLATION_ID', "Interpolation"],  
    ['CANCEL_ID', "Cancel"],
    ['UNDO_ID', "Undo"],
    ['VALID_ID', "Valid"],
    ['RESET_ID', "Reset"],
    ['SAVE_ID', "Save"],
    ['SELECTALL_ID', "Select all"],
    ['UNSELECTALL_ID', "Unselect all"],
    #################################### DataSet Files menu
    ['CLOSE_ID', "Close"],   
    ['PRINT_ID', "Print"],   
    ['EXPORT_ID', "Export"],   
    ['EXPORTIMAGE_ID', "As an image file"],   
    ['EXPORTKML_ID', "As an kml file"],   
    ['EXPORTRASTER_ID', "As a raster file(picture + worldfile)"], 
    #################################### DataSet Display settings menu
    ['DISPLAYSETTINGS_ID', "Display settings"], 
    ['PLOTTYPE_ID', "Plot type"],   
    ['COLORMAP_ID', "Color map"],    
    ['REVERSEFLAG_ID', "Color map reverse"], 
    ['COLORBARDISPLAYFLAG_ID', "Color bar display"], 
    ['COLORBARLOGSCALEFLAG_ID', "Color bar log scale"],  
    ['AXISDISPLAYFLAG_ID', "Axis display"],  
    ['MINIMALVALUE_ID', "Minimal value"],    
    ['MAXIMALVALUE_ID', "Maximal value"],   
    #################################### DataSet Processings menu
    ['PROCESSING_ID', "Processing"], 
    ['FILTERNXSIZE_ID', "Filter size in X (pixels)"],
    ['FILTERNYSIZE_ID', "Filter size in Y (pixels)"],
    ['APODISATIONFACTOR_ID', "Apodisation(%)"],
    ['APODISATIONFACTOR_MSG', "(0, for no apodisation)"],
    ########################## Peak filtering
    ['PEAKFILT_ID', "Peak filtering"],
    ['LABEL_NANREPLACEDFLAG_ID', "Overlimits values"],
    ['MINMAXREPLACEDFLAG_ID', "replace by Min, Max values"],
    ['NANREPLACEDFLAG_ID', "replace by 'nan'"],
    ['MEDIANREPLACEDFLAG_ID', "replace by profile's median"],
    ########################## Median filtering
    ['MEDIANFILT_ID', "Median filtering"],
    ['MEDIANFILTERPERCENT_ID', "Median value filtering (%)"],
    ['MEDIANFILTERGAP_ID', "Constant gap filtering"],
    ########################## Festoon filtering
    ['FESTOONFILT_ID', "Festoon filtering"],
    ['FESTOONFILTMETHOD_ID', "Correlation method"],
    ['FESTOONFILTSHIFT_ID', "Uniform Shift (pixels)"],
    ['FESTOONFILTMINCORR_ID', "Minimum correlation for shifting [0-1]"],
    ['CORRELATIONMAP_ID', "Correlation map"],
    ['CORRELATIONSUM_ID', "Correlation sum"],
    ########################## Regional filtering
    ['REGTRENDFILT_ID', "Regional trend filtering"],
    ['REGTRENDMETHOD_ID', "Method for filtering (relative for resistivity, absolute for magnetic field)"],
    ['REGTRENDCOMPONENT_ID', "Component to keep"],
    ########################## Wallis filtering
    ['WALLISTARGMEAN_ID', "Target mean brightness"],
    ['WALLISTARGSTDEV_ID', "Target brightness standard deviation"],
    ['WALLISSETGAIN_ID', "Gain (A)"],
    ['WALLISLIMIT_ID', "Standard deviation limit"],
    ['WALLISEDGEFACTOR_ID', "Edge factor (alpha) [0-1]"],
    ['WALLISFILT_ID', "Wallis filtering"],
    ########################## Ploughing filtering
    ['PLOUGHFILT_ID', "Anti-ploughing filtering"],
    ['PLOUGHANGLE_ID', "Angle"],
    ['PLOUGHCUTOFF_ID', "Cut off"],
    ########################## Destriping filtering
    ['PROFILESNB_ID', "Number of profile for reference calculation (0 = whole dataset)"],
    ['DESTRIPINGMETHOD_ID', "Destriping method"],
    ['CONFIGDESTRIP_ID', "Configuration (mono  or multi-sensor)"],
    ['CONSTDESTRIP_ID', "Constant destriping"],
    ['CUBICDESTRIP_ID', "Cubic destriping"],
    ['DESTRIPINGDEGREESNB_ID', "Polynomial degree"],
    ['PROFILESMEAN_ID', "Mean cross-track profile"],
    ['REF_ID', "Reference for destriping (mean or median)"],
    #################################### DataSet Magnetic processings menu
    ['MAGPROCESSING_ID', "Magnetic processing"], 
    ########################## Log transform
    ['LOGTRANSFORM_ID', "Log. transformation"],
    ['MULTFACTOR_ID', "Multiply factor"],
    ['LOGTRANSFORM_MSG', "This factor depends on the data precision.\nIt is approximatively the inverse of this precision"],
    ['LOGTRANSFORM_REF', "Enhancement of magnetic data by logarithmic transformation.\nBill Morris, Matt Pozza, Joe Boyce and George Leblanc\nThe Leading EDGE August 2001, Vol 20, N°8"],
    ########################## Pole reduction
    ['POLEREDUCTION_ID', "Pole reduction"],
    ['INCLINEANGLE_ID', "Inclination(deg)"],
    ['ALPHAANGLE_ID', "Alpha(deg)"],
    ########################## Continuation
    ['CONTINUATION_ID', "Continuation"],
    ['PROSPTECH_ID', "Technical of prospection"],
    ['DOWNSENSORALT_ID', "Down sensor altitude(m)"],
    ['UPSENSORALT_ID', "Up sensor altitude(m)"],
    ['ALTITUDE_MSG', "(Altitudes are relatives to the soil surface)"],
    ['CONTINUATIONFLAG_ID', "Continuation"],
    ['CONTINUATIONVALUE_ID', "Value(m)"],
    ['SOILSURFACEABOVEFLAG_ID', "Above the soil surface"],
    ['SOILSURFACEBELOWFLAG_ID', "Below the soil surface"],
    ########################## Analytic Signal
    ['ANALYTICSIGNAL_ID', "Analytic signal"],
    ########################## Equiv. Stratum suceptibility
    ['SUSCEPTIBILITY_ID', "Equivalent stratum in magnetic susceptibility"],
    ['CALCDEPTH_ID', "Calculation depth(m)"],
    ['EQSTRATTHICKNESS_ID', "Thickness of equivalent stratum(m)"],
    ########################## Gradient <-> Toatl Field
    ['GRADMAGFIELDCONV_ID', "Gradient <-> Magnetic field"],
    ['PROSPTECHUSED_ID', "Technical prospection used"],
    ['PROSPTECHSIM_ID', "Technical prospection simulated"],
    ########################## Euler deconvolution
    ['EULERDECONV_ID', "Euler deconvolution"],
    ['EULERDECONV_MSG', "For having an estimation of the depth of an anomaly, click the mouse at two points allowing this anomaly"],
    ['CLOSE_ID', "Close"], 
    #################################### DataSet Geo-referencing menu
    ['GEOREFERENCING_ID', "Geo-referencing"],   
    ['DISPUPDATE_ID', "Update"],
    ['INFORMATIONS_ID', "Informations"],
    ['BADFILEFORMAT_MSG', "Bad file format !"],
    ['VALFILT_ID', "Uses initial data values"],
    ['SIZEGRIDDING_ID', "Gridding size"],
    ['STRUCTINDEX_ID', "Structural index"],
    ['POINTSLIST_ID', "List of points"],
    ['POINTNUM_ID', "num"],
    ['POINTLONGITUDE_ID', "Longitude"],
    ['POINTLATITUDE_ID', "Latitude"],
    ['POINTEASTING_ID', "Easting"],
    ['POINTNORTHING_ID', "Northing"],
    ['GEOINFO_ID', "Geographic system information"],
    ['POINTX_ID', "X"],
    ['POINTY_ID', "Y"],
    ['POINTSELECTED_ID', "Selected"],
    ['POINTXYCONVERTED_ID', "(X,Y) coordinates"],
    ['REFSYSTEM_ID', "Ref System"],
    ['UTMLETTER_ID', "UTM Letter"],
    ['UTMNUMBER_ID', "UTM Number"],
    ['GEOPOINTLIST_ID', "Geographic points list"],
    ['GEOREFERROR1_MSG', "Not enough points to georeference data set !"],
    ['GEOREFERROR2_MSG', "data set zone greater than selected points list zone !"],
    ['CONFIG_ID', "Configuration"]]


class Language:
    ''' Caracteristics of a language : name, fontname, fontsize, and dictionnary of strings
    '''
    name = ""
    dict = None


class AsciiSet(object):    
    def __init__(self, fontname = None, fontsize = 10):
        # builds the languages list
        self.lnglist = []  # creates empty list
        self.fontsize = fontsize
        self.addLanguage("english", english_array)
        self.lngindex = 0
        self.fontname = fontname
        self.fontsize = fontsize
        self.font = QtGui.QFont(fontname, fontsize)         # updates the font

        if (platform.system() == 'Windows'):
            self.main_dir = expanduser("~") + "/wumappy"
        else:           # Linux, Mac OS, ...
            self.main_dir = expanduser("~") + "/.wumappy"

                        # create the ressource directory if not exists
        os.makedirs(self.main_dir + res_dir, exist_ok=True)

                        # searches the langages files
        filenames = glob.glob(self.main_dir + res_dir + "/*.lng")        # extension if the filenames field is like "*.txt"
        for filename in filenames:
            error, name, array2D = self.readLanguage(filename)
            if ((error == 0) and (name!="english")):
                self.addLanguage(name, array2D)
        
                        # writes the english language file            
        self.saveLanguage(self.main_dir + res_dir + "/english.lng", "english", english_array)
        self.setLanguage("english")
        

    def setLanguage(self, name):
        ''' Sets the display language
        '''
        newname = self.lnglist[self.lngindex].name
        for i in range(len(self.lnglist)):
            if (name == self.lnglist[i].name):
                self.lngindex = i
                newname = name
                break

        return self.lngindex, newname


    def getLanguageList(self):
        ''' Gets the list of the names of languages
        '''
        list=[]
        for lang in self.lnglist:
            list.append(lang.name)
        return list
    

    def language(self):
        ''' Gets the current display language
        '''
        return self.lngindex, self.lnglist[self.lngindex].name


    def addLanguage(self, name, array2D):
        '''
        '''
        lang = Language()               # inits a language
        lang.name = name                
        lang.dict = self.arrayToDict(array2D)
        self.lnglist.append(lang)


    def arrayToDict(self, array2D):
        ''' Converts a 2D array in disctionnary
        '''
        dict =  {}
        for line in array2D:
            dict[line[0]] = line[1]
        return dict


    def getStringValue(self, string_id):
        ''' Gets the string corresponding to the string identifiant
        '''
        string_value = ''
        if (string_id != ''):
            try:            # if string_id exits in the current language, all is fine
                string_value = self.lnglist[self.lngindex].dict[string_id]
            except:         
                try:        # if not, try to use string_id in english array
                    string_value = self.lnglist[0].dict[string_id]
                except:     # if string_id doesn't exist in english array
                    string_value = "?????"
                    
        return string_value


    def saveLanguage(self, filename, name, array2D, delimiter = '\t'):
        ''' Writes the language in a file
        '''
        error = 0       # no error by default
        try:
            csvfile = open(filename, 'w')
        except:
            error = -1

        if (error == 0):    # if no error
            writer = csv.writer(csvfile, delimiter=delimiter)
            writer.writerow([name])                 # writes the name of the language at the first line
            for line in array2D:
                if (len(line) == 2):
                    writer.writerow([line[0], line[1]])
        return error


    def readLanguage(self, filename, delimiter = '\t'):
        ''' Readss the language in a file
        '''
        error = 0       # no error by default
        try:
            csvfile = open(filename, 'r')
        except:
            error = -1

        array2D = []
        name = ""

        if (error == 0):    # if no error
            reader = csv.reader(csvfile, delimiter=delimiter)
            row = next(reader)
            if (len(row) == 1):
                name = row[0]                           # reads the name of the language at the first line
                row = next(reader)                
            for row in reader:                          # reads the string array tu display
                if (len(row) == 2):
                    array2D.append([row[0], row[1]])

        return error, name, array2D


    def setFontSize(self, fontsize):
        ''' Sets the font size
        '''
        self.fontsize = fontsize
        return self.fontsize
    
