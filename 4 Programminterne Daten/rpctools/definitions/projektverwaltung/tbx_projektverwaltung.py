# -*- coding: utf-8 -*-

import sys

import arcpy
import datetime
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung import Projektverwaltung


class TbxProjektVerwaltung(Tbx):
    """Toolbox Projektverwaltung"""

    @property
    def label(self):
        return u'Schritt 1: Projekte verwalten'

    @property
    def Tool(self):
        return Projektverwaltung

    def _getParameterInfo(self):
        params = self.par

        # Was_möchten_Sie_tun_
        p = params.action = arcpy.Parameter()
        p.name = encode('Was_möchten_Sie_tun_')
        p.displayName = encode('Was möchten Sie tun?')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = language('string')
        p.filter.list = ['Neues Projekt anlegen',
                                     'Bestehendes Projekt kopieren',
                                     encode('Bestehendes Projekt löschen')]

        projects = self.folders.get_projects()

        # Bestehendes_Projekt_auswählen
        p = params.existing_project = arcpy.Parameter()
        p.name = encode('Bestehendes_Projekt_auswählen')
        p.displayName = encode('Bestehendes Projekt auswählen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = language('string')
        p.value = u' '
        p.filter.list = projects

        # Name_des_neuen_Projektes
        p = params.name = arcpy.Parameter()
        p.name = u'Name_des_neuen_Projektes'
        p.displayName = u'Name des neuen Projektes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = language('string')
        p.value = u' '

        # Shapefile_des_Plangebiets____shp_
        p = params.shapefile = arcpy.Parameter()
        p.name = u'Shapefile_des_Plangebiets____shp_'
        p.displayName = u'Shapefile des Plangebiets (*.shp)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Shapefile'
        p.value = self.folders.TEMPLATE_FLAECHEN

        # Beginn_des_Betrachtungszeitraumes
        p = params.begin = arcpy.Parameter()
        p.name = u'Beginn_des_Betrachtungszeitraumes'
        p.displayName = u'Beginn des Betrachtungszeitraumes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [2010, 2050]
        p.value = datetime.datetime.now().year

        # Ende_des_Betrachtungszeitraumes
        p = params.end = arcpy.Parameter()
        p.name = u'Ende_des_Betrachtungszeitraumes'
        p.displayName = u'Ende des Betrachtungszeitraumes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [2010, 2050]
        p.value = 2050


        #Eingaben zu Beginn deaktiviere/füllen
        params.existing_project.enabled = False
        params.name.enabled = False
        params.shapefile.enabled = False
        params.begin.enabled = False
        params.end.enabled = False
        params.existing_project.filter.list = [" "]

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
