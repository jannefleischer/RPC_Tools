# -*- coding: utf-8 -*-

import _rpcpath
import contextlib
import os
import sys
import arcpy
import shutil
import T1_Vorberechnungen, T2_Zentrale_Orte_OEPNV_Abfrage
import T3_Erreichbarkeit_OEPNV, T4_Erreichbarkeit_Einrichtungen
import T5_Ergebnissammler
import imp
BASE_PATH = os.path.abspath(join(os.path.dirname(__file__),
                                         '..', '..'))
LIB_PATH = join(BASE_PATH, '2_Tool', '2_Projektverwaltung')
project_lib = imp.load_source('project_lib',
                              join(LIB_PATH, 'project_lib.py'))

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx
class Toolbox(object):
    def __init__(self):
        self.label = u'11_Definition_Projekt_Tool'
        self.alias = ''
        self.tools = [Vorberechnungen, ZentraleOrte_OEPNV,
                      Erreichbarkeit_OEPNV, ErgebnisAusgabe, Einrichtungen]

# Tool implementation code

class Vorberechnungen(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx\01Vorberechnungen"""
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
        self.label = u'1 Vorberechnungen'
        self.canRunInBackground = False
        reload(T1_Vorberechnungen)

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
        T1_Vorberechnungen.main(parameters, messages)


class ZentraleOrte_OEPNV(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx\02ZentraleOrteÖPNV"""
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

            #set project
            self.params[0].filter.list = list_projects

            #set Orte
            self.params[1].filter.list = []
            self.params[2].filter.list = []
            self.params[3].filter.list = []

            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""

            #Projekt auswählen
            if self.params[0].altered and not self.params[0].hasBeenValidated:
                projectname = self.params[0].value
                self.params[1].value = ""
                self.params[2].value = ""
                self.params[3].value = ""
                path_Orte = join(BASE_PATH,'3_Projekte',projectname,
                                         'FGDB_Erreichbarkeit.gdb',
                                         'Zentrale_Orte_75km')

                rows_Orte = arcpy.SearchCursor(path_Orte)
                list_Ort1 = []
                list_Ort2 = []
                list_Ort3 = []
                for row in rows_Orte :
                    list_Ort1.append(row.Name)
                    list_Ort2.append(row.Name)
                    list_Ort3.append(row.Name)

                list_Ort1 = sorted(list(set(list_Ort1)))
                list_Ort2 = sorted(list(set(list_Ort2)))
                list_Ort3 = sorted(list(set(list_Ort3)))

                self.params[1].filter.list = list_Ort1
                self.params[2].filter.list = list_Ort2
                self.params[3].filter.list = list_Ort3

            #Orte auswählen
            if self.params[1].altered and not self.params[1].hasBeenValidated:

                projectname = self.params[0].value
                Ort1 = self.params[1].value

            if self.params[2].altered and not self.params[2].hasBeenValidated:

                projectname = self.params[0].value
                Ort2 = self.params[2].value

            if self.params[3].altered and not self.params[3].hasBeenValidated:

                projectname = self.params[0].value
                Ort3 = self.params[3].value

            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'2 Erreichbarkeit Zentraler Orte (ÖPNV)'.encode('CP1252')
        self.canRunInBackground = False
        reload(T2_Zentrale_Orte_OEPNV_Abfrage)

    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Ziel_1
        param_2 = arcpy.Parameter()
        param_2.name = u'Ziel_1'
        param_2.displayName = u'Ziel 1'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Ziel_2
        param_3 = arcpy.Parameter()
        param_3.name = u'Ziel_2'
        param_3.displayName = u'Ziel 2'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'

        # Ziel_3
        param_4 = arcpy.Parameter()
        param_4.name = u'Ziel_3'
        param_4.displayName = u'Ziel 3'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Zeichenfolge'

        parameters = [param_1, param_2, param_3, param_4]
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
        T2_Zentrale_Orte_OEPNV_Abfrage.main(parameters, messages)


class Erreichbarkeit_OEPNV(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx\03ErreichbarkeitÖPNV"""
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
            #set project
            self.params[0].filter.list = list_projects

            #set Haltestellen
            self.params[1].filter.list = []
            self.params[2].filter.list = []
            self.params[3].filter.list = []

            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""

            #Projekt auswählen
            if self.params[0].altered and not self.params[0].hasBeenValidated:
                projectname = self.params[0].value
                self.params[1].value = ""
                self.params[2].value = ""
                self.params[3].value = ""
                path_Halte = join(BASE_PATH,'3_Projekte',projectname,'FGDB_Erreichbarkeit.gdb','OEPNV_Haltestellen')

                rows_Halte = arcpy.SearchCursor(path_Halte)
                list_Halte1 = []
                list_Halte2 = []
                list_Halte3 = []
                for row in rows_Halte:
                    list_Halte1.append(row.Name + " | " + str(row.Distanz) + "m entfernt")
                    list_Halte2.append(row.Name + " | " + str(row.Distanz) + "m entfernt")
                    list_Halte3.append(row.Name + " | " + str(row.Distanz) + "m entfernt")

                list_Halte1 = sorted(list(set(list_Halte1)))
                list_Halte2 = sorted(list(set(list_Halte2)))
                list_Halte3 = sorted(list(set(list_Halte3)))

                self.params[1].filter.list = list_Halte1
                self.params[2].filter.list = list_Halte2
                self.params[3].filter.list = list_Halte3

            #Haltestellen auswählen
            if self.params[1].altered and not self.params[1].hasBeenValidated:

                projectname = self.params[0].value
                Halte1 = (self.params[1].value)

            if self.params[2].altered and not self.params[2].hasBeenValidated:

                projectname = self.params[0].value
                Halte2 = (self.params[2].value)

            if self.params[3].altered and not self.params[3].hasBeenValidated:

                projectname = self.params[0].value
                Halte3 = (self.params[3].value)

            return
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'3 Haltestellen und Linientaktung (\xd6PNV)'
        self.canRunInBackground = False
        reload(T3_Erreichbarkeit_OEPNV)

    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Haltestelle1
        param_2 = arcpy.Parameter()
        param_2.name = u'Haltestelle1'
        param_2.displayName = u'Haltestelle1'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Haltestelle2
        param_3 = arcpy.Parameter()
        param_3.name = u'Haltestelle2'
        param_3.displayName = u'Haltestelle2'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'

        # Haltestelle3
        param_4 = arcpy.Parameter()
        param_4.name = u'Haltestelle3'
        param_4.displayName = u'Haltestelle3'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Zeichenfolge'

        parameters = [param_1, param_2, param_3, param_4]
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
        T3_Erreichbarkeit_OEPNV.main(parameters, messages)



class ErgebnisAusgabe(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx\05ErgebnisAusgabe"""
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
        self.label = u'5 Ergebnisse sammeln und exportieren'
        self.canRunInBackground = False
        reload(T5_Ergebnissammler)

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
        T5_Ergebnissammler.main(parameters, messages)


class Einrichtungen(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\D_Erreichbarkeit\D_Erreichbarkeit.tbx\04EinrichtungenEinrichtungen"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""

        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            self.initializeParameters() # ruft InitializeParameters auf

        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)

            i=-1
            i+=1 ;
            self.params[i].filter.list = list_projects
            self.Projekt= i
            i+=1
            self.Bereitsvorhandene=i
            i+=1
            self.Kita=i
            i+=1
            self.Grundschulen=i
            i+=1
            self.Arzt=i
            i+=1
            self.Apotheken=i
            i+=1
            self.Krankenhaeuser=i
            i+=1
            self.Sonstige=i
            i+=1
            self.BooleanEinzel=i
            i+=1
            self.Einzelhandel=i
            i+=1
            self.Einzelhandel_feature=i
            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parmater
            has been changed."""
            i=-1
            i+=1 ;
            #Immer aus
            self.params[self.Einzelhandel_feature].enabled=0
            #Projekt
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname=self.params[0].value

                #check ob alle 5 template excel datein vorhanden
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Kindertagesstaetten.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Kitas_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Kindertagesstaetten.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Grundschulen.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Grundschulen_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Grundschulen.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Einzelhandel.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Einzelhandel_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Einzelhandel.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Apotheken.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Apotheken_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Apotheken.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Aerzte.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Aerzte_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Aerzte.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Krankenhaeuser.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Krankenhaeuser_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Krankenhaeuser.xls"))
                if os.path.isfile(join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Sonstige.xls"))==False:
                    shutil.copyfile(join(BASE_PATH,'2_Tool','D_Erreichbarkeit','Einrichtungen_Sonstige_template.xls'),join(BASE_PATH,'3_Projekte',projectname,"Einrichtungen_Sonstige.xls"))


                tablepath_template_kitas =  join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Kindertagesstaetten.xls')
                tablepath_template_grundschulen = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Grundschulen.xls')
                tablepath_template_einzelhandel = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Einzelhandel.xls')
                tablepath_template_apotheken = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Apotheken.xls')
                tablepath_template_aerzte = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Aerzte.xls')
                tablepath_template_kh = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Krankenhaeuser.xls')
                tablepath_template_sons = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Sonstige.xls')

                self.params[self.Kita].value=tablepath_template_kitas
                self.params[self.Grundschulen].value=tablepath_template_grundschulen
                self.params[self.Einzelhandel].value=tablepath_template_einzelhandel
                self.params[self.Apotheken].value=tablepath_template_apotheken
                self.params[self.Arzt].value=tablepath_template_aerzte
                self.params[self.Krankenhaeuser].value=tablepath_template_kh
                self.params[self.Sonstige].value=tablepath_template_sons

            i+=1
            #Booleanabfrage
            if self.params[i].value==True:
                #Alle Eingaben sperren da schon Datenvorhanden die genutzt werden sollen
                self.params[self.Kita].enabled=0
                self.params[self.Grundschulen].enabled=0
                self.params[self.Arzt].enabled=0
                self.params[self.Einzelhandel].enabled=0
                self.params[self.Apotheken].enabled=0
                self.params[self.Krankenhaeuser].enabled=0
                self.params[self.Sonstige].enabled=0

                self.params[self.BooleanEinzel].enabled=0
                self.params[self.Einzelhandel].enabled=0
                self.params[self.Einzelhandel_feature].enabled=0

            else:
                self.params[self.Kita].enabled=1
                self.params[self.Grundschulen].enabled=1
                self.params[self.Arzt].enabled=1
                self.params[self.Einzelhandel].enabled=1
                self.params[self.Apotheken].enabled=1
                self.params[self.Krankenhaeuser].enabled=1
                self.params[self.Sonstige].enabled=1


                self.params[self.BooleanEinzel].enabled=1

            if self.params[self.BooleanEinzel].value==True:
                projectname=self.params[0].value
                tablepath_einzelhandel = join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')
                self.params[self.Einzelhandel_feature].value=tablepath_einzelhandel
                self.params[self.Einzelhandel].enabled=0
                self.params[self.Einzelhandel_feature].enabled=1
            elif self.params[self.Projekt].value!=None and self.params[self.Kita].enabled!=0:
                projectname=self.params[0].value
                tablepath_template_einzelhandel = join(BASE_PATH,'3_Projekte',projectname,'Einrichtungen_Einzelhandel.xls')
                self.params[self.Einzelhandel].value=tablepath_template_einzelhandel
                self.params[self.Einzelhandel].enabled=1
                self.params[self.Einzelhandel_feature].enabled=0

            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return

    def __init__(self):
        self.label = u'4 Laden von Einrichtungen'
        self.canRunInBackground = False
        reload(T4_Erreichbarkeit_Einrichtungen)

    def getParameterInfo(self):
        # Projektnamen
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektnamen'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'

        # Bereits_eingeladene_Einrichtung_für_das_Projekt_verwenden
        param_2 = arcpy.Parameter()
        param_2.name = u'Bereits_eingeladene_Einrichtung_f\xfcr_das_Projekt_verwenden'
        param_2.displayName = u'Bereits geladene Einrichtung f\xfcr das Projekt verwenden'
        param_2.parameterType = 'Optional'
        param_2.direction = 'Input'
        param_2.datatype = u'Boolesch'

        # Kita
        param_3 = arcpy.Parameter()
        param_3.name = u'Kita'
        param_3.displayName = u'Kita'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Datei'

        # Grundschulen
        param_4 = arcpy.Parameter()
        param_4.name = u'Grundschulen'
        param_4.displayName = u'Grundschulen'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Datei'

        # Allgemein_Mediziner
        param_5 = arcpy.Parameter()
        param_5.name = u'Allgemein_Mediziner'
        param_5.displayName = u'Allgemein Mediziner'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Datei'

        # Apotheken
        param_6 = arcpy.Parameter()
        param_6.name = u'Apotheken'
        param_6.displayName = u'Apotheken'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Datei'

        # Krankenhäuser
        param_7 = arcpy.Parameter()
        param_7.name = u'Krankenh\xe4user'
        param_7.displayName = u'Krankenh\xe4user'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Datei'

        # Sonstige
        param_8 = arcpy.Parameter()
        param_8.name = u'Sonstige'
        param_8.displayName = u'Sonstige'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Datei'

        # Einzelhandelstandorte_aus_34_Versorgung_übernehmen
        param_9 = arcpy.Parameter()
        param_9.name = u'Einzelhandelstandorte_aus_34_Versorgung_\xfcbernehmen'
        param_9.displayName = u'Einzelhandelstandorte aus Toolbox "Standardversorgung" übernehmen'.encode('CP1252')
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = u'Boolesch'

        # Einzelhandelstandorte
        param_10 = arcpy.Parameter()
        param_10.name = u'Einzelhandelstandorte'
        param_10.displayName = u'Einzelhandelstandorte'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Datei'

        # Einzelhandelstandorte_aus_Toolbox_34_Versorgung
        param_11 = arcpy.Parameter()
        param_11.name = u'Einzelhandelstandorte_aus_Toolbox_34_Versorgung'
        param_11.displayName = u'Einzelhandelstandorte aus Toolbox "Standardversorgung"'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = u'Feature-Class'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6,
                      param_7, param_8, param_9, param_10, param_11]
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
        T4_Erreichbarkeit_Einrichtungen.main(parameters, messages)









