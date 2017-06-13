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
from rpctools.utils.params import Tool
# Import arcpy modules
import arcpy, os


class Flaechenbilanz(Tool):

    _workspace = 'FGDB_Definition_Projekt.gdb'

    def add_outputs(self): 
        pass

    @property
    def teilflaechen_table(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

    @property
    def flaechenbilanz(self):
        return self.folders.get_table('Flaechenbilanz')

    def run(self):
        arcpy.env.overwriteOutput = True

        #projektname = self.par.name.value
        teilflaeche = self.par.teilflaeche.value
        startjahr = self.par.startjahr.value
        ### 01_Generelle Flächenaufteilung ###
        ant_verkehrsfl = self.par.ant_verkehrsfl.value
        ant_gruenfl = self.par.ant_gruenfl.value
        ant_sonstige_fl = self.par.ant_sonstige_fl.value
        ant_nettobauland = self.par.ant_nettobauland.value
        ### 02_Aufteilung Nettobauland ###
        ant_gewerbefl = self.par.ant_gewerbefl.value
        ant_nettowohnbauland = self.par.ant_nettowohnbauland.value
        ### 03_Aufteilung Verkehrsfläche ###
        laermschutz = self.par.laermschutz.value
        privatwege = self.par.privatwege.value
        auessere_erschl = self.par.auessere_erschl.value
        innere_erschl = self.par.innere_erschl.value
        ### 04_Aufteilung Grünfläche ###
        spielplatz = self.par.spielplatz.value
        strassenbegleitgruen = self.par.strassenbegleitgruen.value
        ausgleich_ersatz = self.par.ausgleich_ersatz.value
        allg_gruen = self.par.allg_gruen.value

        #Pfade einrichten
        teilflaechen_table = self.teilflaechen_table
        flaechenbilanz = self.flaechenbilanz

        # Suche Größe der aktuellen Teilfläche heraus
        with arcpy.da.SearchCursor(teilflaechen_table, ['Name',
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



        # Nettobauland
        nettobauland = flaeche * ant_nettobauland / 100.

        ant = self.par.ant_nettowohnbauland.value
        cursor.insertRow((
            teilflaeche,
            startjahr,
            'Nettobauland',
            'Nettowohnbauland',
            ant_nettobauland,
            ant_nettowohnbauland,
            nettobauland * ant_nettowohnbauland / 100.))

        cursor.insertRow((
            teilflaeche,
            startjahr,
            'Nettobauland',
            'Gewerbeflaeche',
            ant_nettobauland,
            ant_gewerbefl,
            nettobauland * ant_gewerbefl / 100.))

        # Verkehrsfläche
        verkehrsflaeche = flaeche * ant_verkehrsfl / 100.

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Laermschutzanlagen',
                          ant_verkehrsfl,
                          laermschutz,
                          verkehrsflaeche * laermschutz / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Privat - Innere Erschliessung',
                          ant_verkehrsfl,
                          privatwege,
                          verkehrsflaeche * privatwege / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Oeffentlich - Aeussere Erschliessung',
                          ant_verkehrsfl,
                          auessere_erschl,
                          verkehrsflaeche * auessere_erschl / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Erschliessungsflaeche',
                          'Oeffentlich - Innere Erschliessung',
                          ant_verkehrsfl,
                          innere_erschl,
                          verkehrsflaeche * innere_erschl / 100.))

        # Grünfläche
        gruenflaeche = flaeche * ant_gruenfl / 100.

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Spielplaetze',
                          ant_gruenfl,
                          spielplatz,
                          gruenflaeche * spielplatz / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Strassenbegleitgruen',
                          ant_gruenfl,
                          strassenbegleitgruen,
                          gruenflaeche * strassenbegleitgruen / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Ausgleichs- und Ersatzflaechen',
                          ant_gruenfl,
                          ausgleich_ersatz,
                          gruenflaeche * ausgleich_ersatz / 100.))

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Gruenflaeche',
                          'Allgemeine Gruenflaechen',
                          ant_gruenfl,
                          allg_gruen,
                          gruenflaeche * allg_gruen / 100.))

        # Sonstige Flächen
        sonstige_fl = flaeche * ant_sonstige_fl / 100.

        cursor.insertRow((teilflaeche,
                          startjahr,
                          'Sonstige Flaechen',
                          'Sonstige Flaechen',
                          ant_sonstige_fl,
                          ant_sonstige_fl,
                          sonstige_fl))
