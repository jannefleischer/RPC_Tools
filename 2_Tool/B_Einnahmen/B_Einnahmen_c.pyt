# -*- coding: utf-8 -*-

import contextlib
import os
import sys
import T1_Vorberechnungen, T2_Einkommensteuer, T3_Familienleistungsausgleich
import T4_Grundsteuer, T5_Gewerbesteuer, T6_KFA, T7_KRU
import argparse
import arcpy

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx

class Toolbox(object):
    def __init__(self):
        self.label = u'32_Einnahmen'
        self.alias = ''
        self.tools = [Vorberechnungen, KFA, Einkommensteuer, Familienleistungsausgleich, Grundsteuer, Gewerbesteuer, KRU]

# Tool implementation code

class Vorberechnungen(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\AuswirkungsabschätzungUmland"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T1_Vorberechnungen)
      
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
        
            i=0
        
            heading1 = "01 Nettozuzugsquoten (in %)"
            i+=1 ; self.params[i].category = heading1 
            i+=1 ; self.params[i].category = heading1 
        
            heading2 = "02 Einzugsbereich (in km)"
            i+=1 ; self.params[i].category = heading2 
            i+=1 ; self.params[i].category = heading2 
        
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
        self.label = u'1 Vorberechnungen'
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

        # Nettozuzugsquote_Einwohner
        param_2 = arcpy.Parameter()
        param_2.name = u'Nettozuzugsquote_Einwohner'
        param_2.displayName = u'Nettozuzugsquote Einwohner'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'50'
        param_2.filter.type = 'Range'
        param_2.filter.list = [0, 100]

        # Nettozuzugsquote_Arbeitsplätze
        param_3 = arcpy.Parameter()
        param_3.name = u'Nettozuzugsquote_Arbeitspl\xe4tze'
        param_3.displayName = u'Nettozuzugsquote Arbeitspl\xe4tze'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'50'
        param_3.filter.type = 'Range'
        param_3.filter.list = [0, 100]

        # Einzugsbereich_Einwohner
        param_4 = arcpy.Parameter()
        param_4.name = u'Einzugsbereich_Einwohner'
        param_4.displayName = u'Einzugsbereich Einwohner'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'25'
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 50]

        # Einzugsbereich_Arbeitsplätze
        param_5 = arcpy.Parameter()
        param_5.name = u'Einzugsbereich_Arbeitspl\xe4tze'
        param_5.displayName = u'Einzugsbereich Arbeitspl\xe4tze'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'25'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 50]
        
        parameters = [param_1, param_2, param_3, param_4, param_5]
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
        T1_Vorberechnungen.main(parameters, messages)

class KFA(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\KFA"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T6_KFA)
      
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
        self.label = u'6 Kommunaler Finanzausgleich'
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
        T6_KFA.main(parameters, messages)

class Einkommensteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Einkommensteuer"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T2_Einkommensteuer)
      
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
        self.label = u'2 Einkommensteuer'
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
        T2_Einkommensteuer.main(parameters, messages)

class Familienleistungsausgleich(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Familienleistungsausgleich"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T3_Familienleistungsausgleich)
      
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
        self.label = u'3 Familienleistungsausgleich'
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
        T3_Familienleistungsausgleich.main(parameters, messages)

class Grundsteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Grundsteuer"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T4_Grundsteuer)
      
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
        
            i=2
        
            heading1 = u"01 Monatsrohmieten (in €)".encode('CP1252')
            i+=1 ; self.params[i].category = heading1 
            i+=1 ; self.params[i].category = heading1
            i+=1 ; self.params[i].category = heading1
            i+=1 ; self.params[i].category = heading1
        
            heading2 = u"02 Jahresrohmieten (in €)".encode('CP1252')
            i+=1 ; self.params[i].category = heading2
            i+=1 ; self.params[i].category = heading2
        
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
        self.label = u'4 Grundsteuer'
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

        # Gemeindegrössenklasse_1964
        param_2 = arcpy.Parameter()
        param_2.name = u'Gemeindegrößenklasse_1964'.encode('CP1252')
        param_2.displayName = u'Gemeindegrößenklasse 1964'.encode('CP1252')
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.filter.list = [u'unter 2000 EW', 
                               u'2000 bis 5000 EW', 
                               u'5000 bis 10000 EW', 
                               u'10000 bis 50000 EW', 
                               u'50000 bis 500000 EW', 
                               u'über 500000 EW'.encode('CP1252')]

        # Grundsteuerhebesatz_als_vH_Satz
        param_3 = arcpy.Parameter()
        param_3.name = u'Grundsteuerhebesatz_als_vH_Satz'
        param_3.displayName = u'Grundsteuerhebesatz als vH Satz'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPDouble'

        # Einfamilienhaus__Monatsrohmiete__in_€_m²_
        param_4 = arcpy.Parameter()
        param_4.name = u'Einfamilienhaus__Monatsrohmiete__in_€'.encode('cp1252')
        param_4.displayName = u'Einfamilienhaus: Monatsrohmiete (in €)'.encode('cp1252')
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPDouble'

        # Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_€_m²_
        param_5 = arcpy.Parameter()
        param_5.name = u'Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_€'.encode('cp1252')
        param_5.displayName = u'Zweifamilien- oder Doppelhaus: Monatsrohmiete (in €)'.encode('cp1252')
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPDouble'

        # Reihenhaus__Monatsrohmiete__in_€_m²_
        param_6 = arcpy.Parameter()
        param_6.name = u'Reihenhaus__Monatsrohmiete__in_€'.encode('cp1252')
        param_6.displayName = u'Reihenhaus: Monatsrohmiete (in €)'.encode('cp1252')
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPDouble'

        # Mehrfamilienhaus__Monatsrohmiete__in_€_m²_
        param_7 = arcpy.Parameter()
        param_7.name = u'Mehrfamilienhaus__Monatsrohmiete__in_€'.encode('cp1252')
        param_7.displayName = u'Mehrfamilienhaus: Monatsrohmiete (in €)'.encode('cp1252')
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'GPDouble'

        # Jahresrohmiete_Garagen___pro_Garage_
        param_8 = arcpy.Parameter()
        param_8.name = u'Jahresrohmiete_Garagen___pro_Garage_'
        param_8.displayName = u'Jahresrohmiete Garagen (pro Garage)'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'GPDouble'

        # Jahresrohmiete_Carports___pro_Garage_
        param_9 = arcpy.Parameter()
        param_9.name = u'Jahresrohmiete_Carports___pro_Garage_'
        param_9.displayName = u'Jahresrohmiete Carports (pro Garage)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'GPDouble'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6, 
                      param_7, param_8, param_9]
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
        T4_Grundsteuer.main(parameters, messages)

class Gewerbesteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Gewerbesteuer"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T5_Gewerbesteuer)
      
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
        self.label = u'5 Gewerbesteuer'
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

        # Hebesatz_als_vH_Satz
        param_2 = arcpy.Parameter()
        param_2.name = u'Hebesatz_als_vH_Satz'
        param_2.displayName = u'Hebesatz als vH Satz'
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
        T5_Gewerbesteuer.main(parameters, messages)
                

class KRU(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\KRU"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(T7_KRU)
      
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
        self.label = u'7 Kreisumlage'
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
        T7_KRU.main(parameters, messages)
        
        
def main():
    tbx = Toolbox()
    tool = Vorberechnungen()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()        