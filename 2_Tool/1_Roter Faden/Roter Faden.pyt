# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy

import Installation_pruefen

def set_parameter_as_text(params, index, val):
    if (hasattr(params[index].value, 'value')):
        params[index].value.value = val
    else:
        params[index].value = val

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\1_Roter Faden\1_Roter Faden.tbx

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = u'A Roter Faden'
        self.alias = ''
        self.tools = [Ersteinrichtung]

# Tool implementation code

class Ersteinrichtung(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\1_Roter Faden\1_Roter Faden.tbx\Ersteinrichtung"""
    import arcpy, os, sys
    
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
        
            self.params[1].enabled = True
            self.params[2].enabled = True
            self.params[3].enabled = True
            self.params[4].enabled = True
            self.params[5].enabled = True
            self.params[6].enabled = True
            self.params[7].enabled = True
            self.params[0].enabled = False
        
            self.params[1].value = False
            self.params[2].value = False
            self.params[3].value = False
            self.params[4].value = False
            self.params[5].value = False
            self.params[6].value = False
            self.params[7].value = False
            self.params[0].value = sys.exec_prefix
        
            return
        
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
        
        
            try:
                import matplotlib
                self.params[1].value = True
            except ImportError, e:
                self.params[1].value = False
                pass
        
            try:
                import numpy
                self.params[2].value = True
            except ImportError, e:
                self.params[2].value = False
                pass
        
            try:
                import pyodbc
                self.params[3].value = True
            except ImportError, e:
                self.params[3].value = False
                pass
        
            try:
                import setuptools
                self.params[4].value = True
            except ImportError, e:
                self.params[4].value = False
                pass
        
            try:
                import six
                self.params[5].value = True
            except ImportError, e:
                self.params[5].value = False
                pass
        
            try:
                import xlrd
                self.params[6].value = True
            except ImportError, e:
                self.params[6].value = False
                pass
        
            try:
                import xlsxwriter
                self.params[7].value = True
            except ImportError, e:
                self.params[7].value = False
                pass
        
        
        
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
        
    def __init__(self):
        self.label = u'Ersteinrichtung'
        self.canRunInBackground = False
        
    def getParameterInfo(self):
        # Pfad_zur_Python_Installation_
        param_1 = arcpy.Parameter()
        param_1.name = u'Pfad_zur_Python_Installation_'
        param_1.displayName = u'Pfad zur Python-Installation:'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.value = u'C:\\Python27-ArcGIS\\ArcGIS10.4'

        # Paket__matplotlib__vorhanden
        param_2 = arcpy.Parameter()
        param_2.name = u'Paket__matplotlib__vorhanden'
        param_2.displayName = u"Paket 'matplotlib' vorhanden"
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Boolesch'
        param_2.value = u'false'

        # Paket__numpy__vorhanden
        param_3 = arcpy.Parameter()
        param_3.name = u'Paket__numpy__vorhanden'
        param_3.displayName = u"Paket 'numpy' vorhanden"
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Boolesch'
        param_3.value = u'false'

        # Paket__pyodbc__vorhanden
        param_4 = arcpy.Parameter()
        param_4.name = u'Paket__pyodbc__vorhanden'
        param_4.displayName = u"Paket 'pyodbc' vorhanden"
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Boolesch'
        param_4.value = u'false'

        # Paket__setuptools__vorhanden
        param_5 = arcpy.Parameter()
        param_5.name = u'Paket__setuptools__vorhanden'
        param_5.displayName = u"Paket 'setuptools' vorhanden"
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Boolesch'
        param_5.value = u'false'

        # Paket__six__vorhanden
        param_6 = arcpy.Parameter()
        param_6.name = u'Paket__six__vorhanden'
        param_6.displayName = u"Paket 'six' vorhanden"
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Boolesch'
        param_6.value = u'false'

        # Paket__xlrd__vorhanden
        param_7 = arcpy.Parameter()
        param_7.name = u'Paket__xlrd__vorhanden'
        param_7.displayName = u"Paket 'xlrd' vorhanden"
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Boolesch'
        param_7.value = u'false'

        # Paket__xlsxwriter__vorhanden
        param_8 = arcpy.Parameter()
        param_8.name = u'Paket__xlsxwriter__vorhanden'
        param_8.displayName = u"Paket 'xlsxwriter' vorhanden"
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Boolesch'
        param_8.value = u'false'

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8]
    
    def isLicensed(self):
        return True
    
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateParameters()
        
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateMessages()
        
    def execute(self, parameters, messages):
        Installation_pruefen.main()
        
            