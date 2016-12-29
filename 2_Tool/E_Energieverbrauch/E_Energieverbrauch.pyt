# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy
import T10_Emissionsmodell
# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\E_Energieverbrauch\E_Energieverbrauch.tbx


class Toolbox(object):
    def __init__(self):
        self.label = u'11_Definition_Projekt_Tool'
        self.alias = ''
        self.tools = [Energieverbrauch]

# Tool implementation code

class Energieverbrauch(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\E_Energieverbrauch\E_Energieverbrauch.tbx\Energieverbrauch"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
        
            tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
        
            try:
                rows_projects = arcpy.SearchCursor(tablepath_projects)
                message = "jep"
            except:
                rows_projects  = []
                message = "nope"
        
            list_projects =[]
        
            for row in rows_projects:
                list_projects.append(row.Name)
            list_projects = list(set(list_projects))
            list_projects = sorted(list_projects)
        
            #set parameters
            self.params[0].filter.list = list_projects 
            return
        
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
        
    def __init__(self):
        self.label = u'1 Energieverbrauch'
        self.canRunInBackground = False
        reload(T10_Emissionsmodell)
        
    def getParameterInfo(self):
        # Projekt_auswählen
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []
        parameters = [param_1]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
        return parameters
    
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
        T10_Emissionsmodell.main(parameters, messages)
            