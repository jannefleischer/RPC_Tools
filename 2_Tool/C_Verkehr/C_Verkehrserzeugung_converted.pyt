# -*- coding: utf-8 -*-

import contextlib
import os
import sys
import T1_Basisdaten_bearbeiten, T2_Routings_durchfuehren
import T3_Verkehrsmengen_ermitteln
import arcpy

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\C_Verkehr\C_Verkehrserzeugung.tbx

class Toolbox(object):
    def __init__(self):
        self.label = u'11_Definition_Projekt_Tool'
        self.alias = ''
        self.tools = [Routingsdurchfuehren, VerkehrsmengenErmitteln, Basisdatenbearbeiten]

# Tool implementation code

class Routingsdurchfuehren(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\C_Verkehr\C_Verkehrserzeugung.tbx\Routingsdurchfuehren"""
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
            except:
                rows_projects  = []
        
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
        self.label = u'2 Routings durchf\xfchren'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # MapQuest_Key
        param_2 = arcpy.Parameter()
        param_2.name = u'MapQuest_Key'
        param_2.displayName = u'MapQuest Key'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        parameters = [param_1, param_2]
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
        T2_Routings_durchfuehren.main(parameters, messages)
            

class VerkehrsmengenErmitteln(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\C_Verkehr\C_Verkehrserzeugung.tbx\VerkehrsmengenErmitteln"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T3_Verkehrsmengen_ermitteln)
      
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
            except:
                rows_projects  = []
        
            list_projects =[]
        
            for row in rows_projects:
                list_projects.append(row.Name)
            list_projects = list(set(list_projects))
            list_projects = sorted(list_projects)
        
            #set parameters
            i=-1
        
            i+=1 ; self.params[0].filter.list = list_projects 
        
            heading = "01 - Parameter für Wohnnutzungen".encode('CP1252')
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
        
        
            heading = "02 - Parameter für Einzelhandel".encode('CP1252')
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
        
            heading = "03 - Parameter für Gewerbebetriebe".encode('CP1252')
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
        
            heading = "04 - Parameter für Schulen".encode('CP1252')
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
        
        
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
        self.label = u'3 Verkehrsmengen ermitteln'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Wohnen_Wege_EW
        param_2 = arcpy.Parameter()
        param_2.name = u'Wohnen_Wege_EW'
        param_2.displayName = u'Wohnen_Wege_EW'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPDouble'
        param_2.value = 3.3

        # Wohnen_MIV_Anteil
        param_3 = arcpy.Parameter()
        param_3.name = u'Wohnen_MIV_Anteil'
        param_3.displayName = u'Wohnen_MIV_Anteil'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPDouble'
        param_3.value = 0.65

        # Wohnen_Pers_KFZ
        param_4 = arcpy.Parameter()
        param_4.name = u'Wohnen_Pers_KFZ'
        param_4.displayName = u'Wohnen_Pers_KFZ'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPDouble'
        param_4.value = 1.1

        # Wohnen_Anteil_Besucherfahrten
        param_5 = arcpy.Parameter()
        param_5.name = u'Wohnen_Anteil_Besucherfahrten'
        param_5.displayName = u'Wohnen_Anteil_Besucherfahrten'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPDouble'
        param_5.value = 0.15

        # Wohnen_WF_Fahrten_je_EW
        param_6 = arcpy.Parameter()
        param_6.name = u'Wohnen_WF_Fahrten_je_EW'
        param_6.displayName = u'Wohnen_WF_Fahrten_je_EW'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPDouble'
        param_6.value = 0.05

        # Versorgung_BGF_Beschaeftigter
        param_7 = arcpy.Parameter()
        param_7.name = u'Versorgung_BGF_Beschaeftigter'
        param_7.displayName = u'Versorgung_BGF_Beschaeftigter'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'GPDouble'
        param_7.value = 55

        # Versorgung_Anwesenheit
        param_8 = arcpy.Parameter()
        param_8.name = u'Versorgung_Anwesenheit'
        param_8.displayName = u'Versorgung_Anwesenheit'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'GPDouble'
        param_8.value = 0.9

        # Versorgung_Wege_Beschaeftigter
        param_9 = arcpy.Parameter()
        param_9.name = u'Versorgung_Wege_Beschaeftigter'
        param_9.displayName = u'Versorgung_Wege_Beschaeftigter'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'GPDouble'
        param_9.value = 2.5

        # Versorgung_MIV_Anteil
        param_10 = arcpy.Parameter()
        param_10.name = u'Versorgung_MIV_Anteil'
        param_10.displayName = u'Versorgung_MIV_Anteil'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'GPDouble'
        param_10.value = 0.65

        # Versorgung_Pers_KFZ
        param_11 = arcpy.Parameter()
        param_11.name = u'Versorgung_Pers_KFZ'
        param_11.displayName = u'Versorgung_Pers_KFZ'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'GPDouble'
        param_11.value = 1.1
        
        # Versorgung_Besucher_Tag
        param_12 = arcpy.Parameter()
        param_12.name = u'Versorgung_Besucher_Tag'
        param_12.displayName = u'Versorgung_Besucher_Tag'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'GPDouble'
        param_12.value = 2.25

        # Versorgung_Lieferwege_100m2
        param_13 = arcpy.Parameter()
        param_13.name = u'Versorgung_Lieferwege_100m2'
        param_13.displayName = u'Versorgung_Lieferwege_100m2'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'GPDouble'
        param_13.value = 0.3

        # Gewerbe_Anwesenheit
        param_14 = arcpy.Parameter()
        param_14.name = u'Gewerbe_Anwesenheit'
        param_14.displayName = u'Gewerbe_Anwesenheit'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'GPDouble'
        param_14.value = 0.9

        # Gewerbe_Wege_Beschaeftigter
        param_15 = arcpy.Parameter()
        param_15.name = u'Gewerbe_Wege_Beschaeftigter'
        param_15.displayName = u'Gewerbe_Wege_Beschaeftigter'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'GPDouble'
        param_15.value = 2.0

        # Gewerbe_MIV_Anteil
        param_16 = arcpy.Parameter()
        param_16.name = u'Gewerbe_MIV_Anteil'
        param_16.displayName = u'Gewerbe_MIV_Anteil'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'GPDouble'
        param_16.value = 0.65

        # Gewerbe_Pers_KFZ
        param_17 = arcpy.Parameter()
        param_17.name = u'Gewerbe_Pers_KFZ'
        param_17.displayName = u'Gewerbe_Pers_KFZ'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'GPDouble'
        param_17.value = 1.1

        # Gewerbe_Anteil_Besucherfahrten
        param_18 = arcpy.Parameter()
        param_18.name = u'Gewerbe_Anteil_Besucherfahrten'
        param_18.displayName = u'Gewerbe_Anteil_Besucherfahrten'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'GPDouble'
        param_18.value = 0.05

        # Gewerbe_Lieferwege_Beschaeftigte
        param_19 = arcpy.Parameter()
        param_19.name = u'Gewerbe_Lieferwege_Beschaeftigte'
        param_19.displayName = u'Gewerbe_Lieferwege_Beschaeftigte'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'GPDouble'
        param_19.value = 0.05

        # Schulen_Wege_Schueler
        param_20 = arcpy.Parameter()
        param_20.name = u'Schulen_Wege_Schueler'
        param_20.displayName = u'Schulen_Wege_Schueler'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'GPDouble'
        param_20.value = 2

        # Schulen_MIV_Anteil
        param_21 = arcpy.Parameter()
        param_21.name = u'Schulen_MIV_Anteil'
        param_21.displayName = u'Schulen_MIV_Anteil'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'GPDouble'
        param_21.value = 0.65

        # Schulen_Schueler_KFZ
        param_22 = arcpy.Parameter()
        param_22.name = u'Schulen_Schueler_KFZ'
        param_22.displayName = u'Schulen_Schueler_KFZ'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'GPDouble'
        param_22.value = 1.5

        # Schulen_Schueler_je_Lehrer
        param_23 = arcpy.Parameter()
        param_23.name = u'Schulen_Schueler_je_Lehrer'
        param_23.displayName = u'Schulen_Schueler_je_Lehrer'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'GPDouble'
        param_23.value = 10

        # Schulen_Wege_Lehrer
        param_24 = arcpy.Parameter()
        param_24.name = u'Schulen_Wege_Lehrer'
        param_24.displayName = u'Schulen_Wege_Lehrer'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'GPDouble'
        param_24.value = 2

        # Schulen_Pers_KFZ
        param_25 = arcpy.Parameter()
        param_25.name = u'Schulen_Pers_KFZ'
        param_25.displayName = u'Schulen_Pers_KFZ'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'GPDouble'
        param_25.value = 1.1

        # Schulen_Lieferwege_Schueler
        param_26 = arcpy.Parameter()
        param_26.name = u'Schulen_Lieferwege_Schueler'
        param_26.displayName = u'Schulen_Lieferwege_Schueler'
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'GPDouble'
        param_26.value = 0.01
    
        parameters = [param_1, param_2, param_3, param_4, param_5, param_6, 
                      param_7, param_8, param_9, param_10, param_11, param_12, 
                      param_13, param_14, param_15, param_16, param_17, 
                      param_18, param_19, param_20, param_21, param_22, 
                      param_23, param_24, param_25, param_26]
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
        T3_Verkehrsmengen_ermitteln.main(parameters, messages)
            

class Basisdatenbearbeiten(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\C_Verkehr\C_Verkehrserzeugung.tbx\Basisdatenbearbeiten"""
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
            except:
                rows_projects  = []
        
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
        self.label = u'1 Basisdaten bearbeiten'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
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
        T3_Verkehrsmengen_ermitteln.main(parameters, messages)
            