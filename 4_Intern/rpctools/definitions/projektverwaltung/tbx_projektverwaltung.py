# -*- coding: utf-8 -*-

import sys

import arcpy
import datetime
from rpctools.utils.params import Tbx
reload(sys.modules[Tbx.__module__])
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung import Projektverwaltung

from rpctools.utils.params import Params


class TbxProjektVerwaltung(Tbx):
    """Toolbox Projektverwaltung"""

    @property
    def label(self):
        return u'1 Projekte verwalten'

    @property
    def Tool(self):
        return Projektverwaltung

    def _getParameterInfo(self):
        params = self.par

        # Was_möchten_Sie_tun_
        params.action = arcpy.Parameter()
        params.action.name = encode('Was_möchten_Sie_tun_')
        params.action.displayName = encode('Was möchten Sie tun?')
        params.action.parameterType = 'Required'
        params.action.direction = 'Input'
        params.action.datatype = u'Zeichenfolge'
        params.action.filter.list = ['Neues Projekt anlegen',
                                     'Bestehendes Projekt kopieren',
                                     encode('Bestehendes Projekt löschen')]

        projects = self.folders.get_projects()

        # Bestehendes_Projekt_auswählen
        params.existing_project = arcpy.Parameter()
        params.existing_project.name = encode('Bestehendes_Projekt_auswählen')
        params.existing_project.displayName = encode('Bestehendes Projekt auswählen')
        params.existing_project.parameterType = 'Required'
        params.existing_project.direction = 'Input'
        params.existing_project.datatype = u'Zeichenfolge'
        params.existing_project.value = u' '
        params.existing_project.filter.list = projects

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
        params.shapefile.value = self.folders.TEMPLATE_FLAECHEN

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
        params.existing_project.filter.list = [" "]
        
        #return [params.existing_project, params.begin, params.name]
        #raise Exception(self.par)
        self.xyt.append('Hallo')

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Eingaben in Abhängigkeit von Vorhaben aktivieren/deaktivieren
        if params.action.altered and not params.action.hasBeenValidated:

            projects = self.folders.get_projects()

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
                if projects:
                    params.existing_project.value = projects[0]
                params.existing_project.filter.list = projects
                params.name.value = None

            # Löschen
            else:
                params.existing_project.enabled = True
                params.name.enabled = False
                params.shapefile.enabled = False
                params.begin.enabled = False
                params.end.enabled = False
                if projects:
                    params.existing_project.value = projects[0]
                params.existing_project.filter.list = projects
                params.name.value = " "

        # Ende des Betrachtungszeitraumes prüfen
        # und ggf. auf ein Jahr nach Beginn setzen
        if params.end.value <= params.begin.value:
            params.end.value = params.begin.value + 1
