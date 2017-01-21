# -*- coding: utf-8 -*-

import _rpcpath
import contextlib
import os
import sys

import arcpy
import T10_Emissionsmodell
import imp
BASE_PATH = os.path.abspath(join(os.path.dirname(__file__),
                                         '..', '..'))
LIB_PATH = join(BASE_PATH, '2_Tool', '2_Projektverwaltung')
project_lib = imp.load_source('project_lib',
                              join(LIB_PATH, 'project_lib.py'))
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

            list_projects = project_lib.get_projects()
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
