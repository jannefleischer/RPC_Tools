# -*- coding: utf-8 -*-


import sys
from os.path import abspath, dirname, join
BASE_PATH = dirname(dirname(abspath(__file__)))
sys.path.append(join(BASE_PATH, '4_Intern'))

from rpctools.utils.params import Params
from rpctools.utils.project_lib import (get_projects,
                                        get_table,
                                        get_template_flaechen,
                                        encode)

from rpctools.definitions.projektverwaltung import (T1_Projektverwaltung,
                                                    teilflaecheBenennen)
import os
import sys
import argparse
import gc

import arcpy


class Toolbox(object):
    def __init__(self):
        self.label = u'Projektverwaltung'
        self.alias = ''
        self.tools = [TeilflaecheBenennen, ProjektVerwaltung]

# Tool implementation code

class TeilflaecheBenennen(object):
    """"""

    def __init__(self):
        self.label = u'2 Teilflaechen verwalten'
        reload(teilflaecheBenennen)
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Projekt
        list_projects = get_projects()
        params = Params()
        params.project = arcpy.Parameter()
        params.project.name = u'Projekt'
        params.project.displayName = u'Projekt'
        params.project.parameterType = 'Required'
        params.project.direction = 'Input'
        params.project.datatype = u'Zeichenfolge'
        params.project.value = u' '
        params.project.filter.list = list_projects

        # Teilfläche
        params.teilflaeche = arcpy.Parameter()
        params.teilflaeche.name = encode(u'Teilfläche')
        params.teilflaeche.displayName = encode(u'Teilfläche')
        params.teilflaeche.parameterType = 'Required'
        params.teilflaeche.direction = 'Input'
        params.teilflaeche.datatype = u'GPString'
        params.teilflaeche.filter.list = []

        # Name
        params.name = arcpy.Parameter()
        params.name.name = u'Name'
        params.name.displayName = u'Name'
        params.name.parameterType = 'Required'
        params.name.direction = 'Input'
        params.name.datatype = u'GPString'

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        #Projekt auswählen
        i=-1

        i+=1
        if params.project.altered and not params.project.hasBeenValidated:
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)
            params.project.filter.list = list_projects

        if params.project.altered and not params.project.hasBeenValidated:
            projectname = params.project.value
            params.teilflaeche.value = ''

            tablepath_teilflaechen = self.get_teilflaeche(projectname)

            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append('Nr. ' + str(row.OBJECTID) + " | "
                                         + str(round(row.Flaeche_ha,2))
                                         + " ha" + " | "+ row.NAME)

            list_teilflaechen = list(set(list_teilflaechen))
            list_teilflaechen = sorted(list_teilflaechen)

            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaeche:
                params.teilflaeche.value = list_teilflaechen[0]


        #Teilfläche auswählen
        if params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated:

            projectname = params.project.value
            flaechenname = params.teilflaeche.value
            flaechenname_id = flaechenname.split('|')[0].replace('Nr.','').strip()

        return

    def get_teilflaeche(self, projectname):
        tablepath_teilflaechen = get_table(projectname,
                                           'FGDB_Definition_Projekt.gdb',
                                           'Teilflaechen_Plangebiet')
        return tablepath_teilflaechen

    def updateMessages(self, params):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""


        if params.project.value != None and params.name.value != None:
            projectname= self.params[0].value
            tablepath_teilflaechen = self.get_teilflaeche(projectname)
            namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

            params.name.clearMessage()

            for row in namen_cursor:
                if params.name.value == row[0]:
                    params.name.setErrorMessage("Name wurde bereits vergeben.")
        return

    def execute(self, parameters, messages):
        teilflaecheBenennen.main(parameters, messages)


class ProjektVerwaltung(object):
    """"""

    def __init__(self):
        self.label = u'1 Projekte verwalten'
        self.canRunInBackground = False
        reload(T1_Projektverwaltung)

    def getParameterInfo(self):
        # Was_möchten_Sie_tun_
        params.action = arcpy.Parameter()
        params.action.name = encode('Was_möchten_Sie_tun_')
        params.action.displayName = encode('Was möchten Sie tun?')
        params.action.parameterType = 'Required'
        params.action.direction = 'Input'
        params.action.datatype = u'Zeichenfolge'
        params.action.filter.list = [u'Neues Projekt anlegen',
                                     u'Bestehendes Projekt kopieren',
                                     encode('Bestehendes Projekt löschen')]

        list_projects = get_projects()

        # Bestehendes_Projekt_auswählen
        params.existing_project = arcpy.Parameter()
        params.existing_project.name = encode('Bestehendes_Projekt_auswählen')
        params.existing_project.displayName = encode('Bestehendes Projekt auswählen')
        params.existing_project.parameterType = 'Required'
        params.existing_project.direction = 'Input'
        params.existing_project.datatype = u'Zeichenfolge'
        params.existing_project.value = u' '
        params.existing_project.filter.list = list_projects

        # Name_des_neuen_Projektes
        params.name = arcpy.Parameter()
        params.name.name = u'Name_des_neuen_Projektes'
        params.name.displayName = u'Name des neuen Projektes'
        params.name.parameterType = 'Required'
        params.name.direction = 'Input'
        params.name.datatype = u'Zeichenfolge'
        params.name.value = u' '

        # Shapefile_des_Plangebiets____shp_
        params.shapefile = arcpy.Parameter()
        params.shapefile.name = u'Shapefile_des_Plangebiets____shp_'
        params.shapefile.displayName = u'Shapefile des Plangebiets (*.shp)'
        params.shapefile.parameterType = 'Required'
        params.shapefile.direction = 'Input'
        params.shapefile.datatype = u'Shapefile'
        params.shapefile.value = get_template_flaechen()

        # Beginn_des_Betrachtungszeitraumes
        params.begin = arcpy.Parameter()
        params.begin.name = u'Beginn_des_Betrachtungszeitraumes'
        params.begin.displayName = u'Beginn des Betrachtungszeitraumes'
        params.begin.parameterType = 'Required'
        params.begin.direction = 'Input'
        params.begin.datatype = u'Long'

        # Ende_des_Betrachtungszeitraumes
        params.end = arcpy.Parameter()
        params.end.name = u'Ende_des_Betrachtungszeitraumes'
        params.end.displayName = u'Ende des Betrachtungszeitraumes'
        params.end.parameterType = 'Required'
        params.end.direction = 'Input'
        params.end.datatype = u'Long'

        #Beginn des Betrachtungszeitraumes auf aktuelles Jahr setzen
        params.begin.value = datetime.datetime.now().year
        params.end.value = 2050

        #Eingaben zu Beginn deaktiviere/füllen
        params.existing_project.enabled = False
        params.name.enabled = False
        params.shapefile.enabled = False
        params.begin.enabled = False
        params.end.enabled = False
        params.existing_project.value = " "
        params.existing_project.filter.list = [" "]
        params.name.value = " "

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Eingaben in Abhängigkeit von Vorhaben aktivieren/deaktivieren
        if params.action.altered and not params.action.hasBeenValidated:

            list_projects = get_projects()

            if params.action.value == "Neues Projekt anlegen":
                params.existing_project.enabled = False
                params.name.enabled = True
                params.shapefile.enabled = True
                params.begin.enabled = True
                params.end.enabled = True
                params.existing_project.value = " "
                params.existing_project.filter.list = [" "]
                params.name.value = None

            elif params.action.value == "Bestehendes Projekt kopieren":
                params.existing_project.enabled = True
                params.name.enabled = True
                params.shapefile.enabled = False
                params.begin.enabled = False
                params.end.enabled = False
                params.existing_project.value = None
                params.existing_project.filter.list = list_projects
                params.name.value = None

            else:
                params.existing_project.enabled = True
                params.name.enabled = False
                params.shapefile.enabled = False
                params.begin.enabled = False
                params.end.enabled = False
                params.existing_project.value = None
                params.existing_project.filter.list = list_projects
                params.name.value = " "

        # Ende des Betrachtungszeitraumes prüfen
        # und ggf. auf ein Jahr nach Beginn setzen
        if params.end.value <= params.begin.value:
                params.end.value = params.begin.value + 1
        return

    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def isLicensed(self):
        return True

    def execute(self, parameters, messages):
        T1_Projektverwaltung.main(parameters, messages)

def main():
    tbx = Toolbox()
    tool = ProjektVerwaltung()
    tool.execute(tool.getParameterInfo(), None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()
