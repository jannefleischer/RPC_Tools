# -*- coding: utf-8 -*-

import os
import sys
import argparse
import gc

import arcpy
import teilflaecheBenennen, projektVerwaltung

def set_parameter_as_text(params, index, val):
    if (hasattr(params[index].value, 'value')):
        params[index].value.value = val
    else:
        params[index].value = val

# Export of toolbox C:\GGR\RPC_Tools\2_Tool\2_Projektverwaltung\T2_Projektverwaltung.tbx

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = u'B Projektverwaltung'
        self.alias = ''
        self.tools = [TeilflaecheBenennen, Projektverwaltung]

# Tool implementation code

class TeilflaecheBenennen(object):
    """C:\GGR\RPC_Tools\2_Tool\2_Projektverwaltung\T2_Projektverwaltung.tbx\TeilflaecheBenennen"""

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
            import os, arcpy

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


            list_teilflaechen = []

            i=-1

            #set project
            i+=1 ; self.params[i].filter.list = list_projects

            #set set teilflaeche
            i+=1 ; self.params[i].filter.list = list_teilflaechen


            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #import os, arcpy, win32ui, win32con
            import os, arcpy

            tbx_path = __file__

            base_path = os.path.dirname(tbx_path)
            #base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

            #Projekt auswählen
            i=-1
            i+=1


            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
                self.params[1].value = ''

                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname +'.gdb','Teilflaechen_Plangebiet')

                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
                list_teilflaechen = []
                for row in rows_teilflaechen :
                    list_teilflaechen.append('Nr. ' + str(row.OBJECTID) + " | "+ str(round(row.Flaeche_ha,2)) + " ha" + " | "+ row.NAME)

                list_teilflaechen = list(set(list_teilflaechen))
                list_teilflaechen = sorted(list_teilflaechen)

                i+=1 ; self.params[i].filter.list = list_teilflaechen

                if len(list_teilflaechen) == 1:
                    self.params[1].value = list_teilflaechen[0]


            #Teilfläche auswählen
            i=1
            if self.params[i].altered and not self.params[i].hasBeenValidated:

                projectname = self.params[i-1].value
                flaechenname = self.params[i].value
                flaechenname_id = flaechenname.split('|')[0].replace('Nr.','').strip()

            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""


            if self.params[0].value != None and self.params[2].value != None:
                tbx_path = __file__
                base_path = os.path.dirname(tbx_path)
                base_path = os.path.dirname(base_path)
                base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
                projectname= self.params[0].value
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname +'.gdb','Teilflaechen_Plangebiet')
                namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

                self.params[2].clearMessage()

                for row in namen_cursor:
                    if self.params[2].value == row[0]:
                        self.params[2].setErrorMessage("Name wurde bereits vergeben.")


            return

    def __init__(self):
        self.label = u'2 Teilflaechen verwalten'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Projekt
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'
        param_1.filter.list = [u'04-10-16', u'test', u'test_template']
        #param_1.value = u'test'

        # Teilfläche
        param_2 = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'

        # Name
        param_3 = arcpy.Parameter()
        param_3.name = u'Name'
        param_3.displayName = u'Name'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPString'

        parameters = [param_1, param_2, param_3]

        validator = getattr(self, 'ToolValidator', None)
        if validator:
            validator(parameters).initializeParameters()

        self.updateParameters(parameters)

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
        teilflaecheBenennen.main(parameters)

class Projektverwaltung(object):
    """C:\GGR\RPC_Tools\2_Tool\2_Projektverwaltung\T2_Projektverwaltung.tbx\Projektverwaltung"""
    import os, arcpy, datetime

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""

        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters

        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""

            #Beginn des Betrachtungszeitraumes auf aktuelles Jahr setzen
            self.params[4].value = datetime.datetime.now().year
            self.params[5].value = 2050

            #Eingaben zu Beginn deaktiviere/füllen
            self.params[1].enabled = False
            self.params[2].enabled = False
            self.params[3].enabled = False
            self.params[4].enabled = False
            self.params[5].enabled = False
            self.params[1].value = " "
            self.params[1].filter.list = [" "]
            self.params[2].value = " "

            #Projektliste erzeugen

            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""

            # Eingaben in Abhängigkeit von Vorhaben aktivieren/deaktivieren
            if self.params[0].altered and not self.params[0].hasBeenValidated:

                tbx_path = __file__
                base_path = os.path.dirname(tbx_path)
                base_path = os.path.dirname(base_path)
                base_path = os.path.dirname(base_path)
                tablePfad = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
                try:
                    rows = arcpy.SearchCursor(tablePfad)
                    list = []
                    for row in rows:
                        list.append(row.Name)
                except:
                    list = []

                list = sorted(list)

                if self.params[0].value == "Neues Projekt anlegen":
                    self.params[1].enabled = False
                    self.params[2].enabled = True
                    self.params[3].enabled = True
                    self.params[4].enabled = True
                    self.params[5].enabled = True
                    self.params[1].value = " "
                    self.params[1].filter.list = [" "]
                    self.params[2].value = None
                    self.params[3].value = os.path.join(base_path,'3_Projekte','projektflaechen_template.shp')

                elif self.params[0].value == "Bestehendes Projekt kopieren":
                    self.params[1].enabled = True
                    self.params[2].enabled = True
                    self.params[3].enabled = False
                    self.params[4].enabled = False
                    self.params[5].enabled = False
                    self.params[1].value = None
                    self.params[1].filter.list = list
                    self.params[2].value = None
                    self.params[3].value = None


                else:
                    self.params[1].enabled = True
                    self.params[2].enabled = False
                    self.params[3].enabled = False
                    self.params[4].enabled = False
                    self.params[5].enabled = False
                    self.params[1].value = None
                    self.params[1].filter.list = list
                    self.params[2].value = " "
                    self.params[3].value = None

            #Ende des Betrachtungszeitraumes prüfen und ggf. auf ein Jahr nach Beginn setzen
            if self.params[5].value <= self.params[4].value:
                    self.params[5].value = self.params[4].value + 1


            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return

    def __init__(self):
        self.label = u'1 Projekte verwalten'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Was_möchten_Sie_tun_
        param_1 = arcpy.Parameter()
        param_1.name = u'Was_m\xf6chten_Sie_tun_'
        param_1.displayName = u'Was m\xf6chten Sie tun?'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'Neues Projekt anlegen', u'Bestehendes Projekt kopieren', u'Bestehendes Projekt l\xf6schen']

        # Bestehendes_Projekt_auswählen
        param_2 = arcpy.Parameter()
        param_2.name = u'Bestehendes_Projekt_ausw\xe4hlen'
        param_2.displayName = u'Bestehendes Projekt ausw\xe4hlen'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.value = u' '
        param_2.filter.list = [u' ']

        # Name_des_neuen_Projektes
        param_3 = arcpy.Parameter()
        param_3.name = u'Name_des_neuen_Projektes'
        param_3.displayName = u'Name des neuen Projektes'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'
        param_3.value = u' '

        # Shapefile_des_Plangebiets____shp_
        param_4 = arcpy.Parameter()
        param_4.name = u'Shapefile_des_Plangebiets____shp_'
        param_4.displayName = u'Shapefile des Plangebiets (*.shp)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Shapefile'

        # Beginn_des_Betrachtungszeitraumes
        param_5 = arcpy.Parameter()
        param_5.name = u'Beginn_des_Betrachtungszeitraumes'
        param_5.displayName = u'Beginn des Betrachtungszeitraumes'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'2016'

        # Ende_des_Betrachtungszeitraumes
        param_6 = arcpy.Parameter()
        param_6.name = u'Ende_des_Betrachtungszeitraumes'
        param_6.displayName = u'Ende des Betrachtungszeitraumes'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'2050'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6]

        self.ToolValidator(parameters).initializeParameters()
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
        projektVerwaltung.main(parameters)

def main():
    tbx = Toolbox()
    tool = Projektverwaltung()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()
