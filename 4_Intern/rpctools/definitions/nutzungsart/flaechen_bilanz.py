# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 10_Kostenmodell.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import sys
from os.path import abspath, dirname, join, isdir
BASE_PATH = dirname(dirname(abspath(__file__)))
sys.path.append(join(BASE_PATH, '4_Intern'))
from rpctools.utils.project_lib import (Folders)
from rpctools.utils.params import Tool
# Import arcpy modules
import arcpy, os


class Flaechenbilanz(Tool):

    _dbname = 'FGDB_Definition_Projekt.gdb'

    @property
    def teilflaechen(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

    @property
    def flaechenbilanz(self):
        return self.folders.get_table('Flaechenbilanz')

    def run(self):
        arcpy.env.overwriteOutput = True

        #Pfade einrichten
        teilflaechen = self.teilflaechen
        flaechenbilanz = self.flaechenbilanz

        # Suche Größe der aktuellen Teilfläche heraus
        with arcpy.da.SearchCursor(teilflaechen, ['Name',
                                                  'Flaeche_ha']) as cursor:
            for row in cursor:
                if row[0] == teilflaeche:
                    flaeche = float(row[1])

        # Lösche bisherige Eingaben für gewählte Teilfläche
        with arcpy.da.UpdateCursor(flaechenbilanz,
                                   "Teilflaeche_Plangebiet") as cursor:
            for row in cursor:
                if row[0] == teilflaeche:
                    cursor.deleteRow()

        # Füge neue Eingaben für gewählte Teilfläche ein
        fields = ['Teilflaeche_Plangebiet',
                  'Startjahr',
                  'Flaechennutzung_S1',
                  'Flaechennutzung_S2',
                  'Anteil_S1',
                  'Anteil_S2',
                  'Flaeche_ha']
        cursor = arcpy.da.InsertCursor(flaechenbilanz, fields)

        teilflaeche = self.par.teilflaeche.value
        startjahr = self.par.startjahr.value

        # Nettobauland
        ant_nettobauland = self.par.ant_nettobauland.value
        nettobauland = flaeche * nettobauland / 100.

        ant = self.par.ant_nettowohnbauland.value
        cursor.insertRow((
            teilflaeche,
            startjahr,
            'Nettobauland',
            'Nettowohnbauland',
            ant_nettobauland,
            ant,
            nettobauland * ant / 100.))

        ant = self.par.ant_gewerbefl.value
        cursor.insertRow((
            teilflaeche,
            startjahr,
            'Nettobauland',
            'Gewerbeflaeche',
            ant_nettobauland,
            ant,
            nettobauland * ant / 100.))

        # Verkehrsfläche
        ant_verkehrsflaeche = self.par.ant_verkehrsflaeche.value
        verkehrsflaeche = flaeche * ant_verkehrsflaeche / 100.

        ant = self.par.laermschutz.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Laermschutzanlagen',
                          ant_verkehrsflaeche,
                          ant,
                          verkehrsflaeche * ant / 100.))
        ant = self.par.privatwege.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Privat - Innere Erschliessung',
                          ant_verkehrsflaeche,
                          ant,
                          verkehrsflaeche * ant / 100.))
        ant = self.par.auessere_erschl.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Oeffentlich - Aeussere Erschliessung',
                          ant_verkehrsflaeche,
                          ant,
                          verkehrsflaeche * ant / 100.))
        ant = self.par.innere_erschl.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Oeffentlich - Innere Erschliessung',
                          ant_verkehrsflaeche,
                          ant,
                          verkehrsflaeche * ant / 100.))

        # Grünfläche
        ant_gruenfl = self.par.ant_gruenfl.value
        gruenflaeche = flaeche * ant_gruenfl / 100.

        ant = self.par.spielplatz.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Spielplaetze',
                          ant_gruenfl,
                          ant,
                          gruenflaeche * ant / 100.))

        ant = self.par.strassenbegleitgruen.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Strassenbegleitgruen',
                          ant_gruenfl,
                          ant,
                          gruenflaeche * ant / 100.))

        ant = self.par.ausgleich_ersatz.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Ausgleichs- und Ersatzflaechen',
                          ant_gruenfl,
                          ant,
                          gruenflaeche * ant / 100.))

        ant = self.par.allg_gruen.value
        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Allgemeine Gruenflaechen',
                          ant_gruenfl,
                          ant,
                          gruenflaeche * ant / 100.))

        # Sonstige Flächen
        ant_sonstige_fl = self.par.ant_sonstige_fl.value
        sonstige_fl = flaeche * ant_sonstige_fl / 100.

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Sonstige Flaechen',
                          'Sonstige Flaechen',
                          ant_sonstige_fl,
                          ant_sonstige_fl,
                          sonstige_fl))
