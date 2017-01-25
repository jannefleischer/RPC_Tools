# -*- coding: utf-8 -*-

import sys
import arcpy
from os.path import abspath, dirname, join
import datetime

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.nutzungsart.flaechenbilanz import Flaechenbilanz


class TbxFlaechenbilanz(Tbx):
    """Toolbox zur Flächenbilanz"""

    @property
    def label(self):
        return encode(u'1 Flächenbilanz eingeben')

    @property
    def Tool(self):
        return Flaechenbilanz

    def _getParameterInfo(self):
        # Projektname
        params = self.par
        projekte = self.folders.get_projects()
        p = params.projectname = arcpy.Parameter()
        p.name = u'Projektname'
        p.displayName = u'Projektname'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Zeichenfolge'
        p.filter.list = projekte
        if projekte:
            p.value = projekte[0]

        # Teilfläche
        p = params.teilflaeche = arcpy.Parameter()
        p.name = u'Teilfl\xe4che'
        p.displayName = u'Teilfl\xe4che'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Zeichenfolge'
        p.filter.list = []

        # Startjahr
        p = params.startjahr = arcpy.Parameter()
        p.name = u'Startjahr'
        p.displayName = u'Startjahr'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = datetime.datetime.now().year
        p.filter.type = 'Range'
        p.filter.list = [2010, 2050]

        heading = encode("01_Generelle Flächenaufteilung")

        # Verkehrsfläche____
        p = params.ant_verkehrsfl = arcpy.Parameter()
        p.name = u'Verkehrsfl\xe4che____'
        p.displayName = u'Verkehrsfl\xe4che (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Grünfläche____
        p = params.ant_gruenfl = arcpy.Parameter()
        p.name = u'Gr\xfcnfl\xe4che____'
        p.displayName = u'Gr\xfcnfl\xe4che (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Sonstige_Flächen____
        p = params.ant_sonstige_fl = arcpy.Parameter()
        p.name = u'Sonstige_Fl\xe4chen____'
        p.displayName = u'Sonstige Fl\xe4chen (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Nettobauland____
        p = params.ant_nettobauland = arcpy.Parameter()
        p.name = u'Nettobauland____'
        p.displayName = u'Nettobauland (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'100'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        heading = "02_Aufteilung Nettobauland"

        # Gewerbeflaeche____
        p = params.ant_gewerbefl = arcpy.Parameter()
        p.name = u'Gewerbeflaeche____'
        p.displayName = u'Gewerbeflaeche (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Nettowohnbauland____
        p = params.ant_nettowohnbauland = arcpy.Parameter()
        p.name = u'Nettowohnbauland____'
        p.displayName = u'Nettowohnbauland (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'100'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        heading = encode("03_Aufteilung Verkehrsfläche")

        # Flächen_für_Lärmschutz____
        p = params.laermschutz = arcpy.Parameter()
        p.name = u'Fl\xe4chen_f\xfcr_L\xe4rmschutz____'
        p.displayName = u'Fl\xe4chen f\xfcr L\xe4rmschutz (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Privatwege____
        p = params.privatwege = arcpy.Parameter()
        p.name = u'Privatwege____'
        p.displayName = u'Privatwege (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Äußere_Erschließung____
        p = params.auessere_erschl = arcpy.Parameter()
        p.name = u'\xc4u\xdfere_Erschlie\xdfung____'
        p.displayName = u'\xc4u\xdfere Erschlie\xdfung (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Innere_Erschließung____
        p = params.innere_erschl = arcpy.Parameter()
        p.name = u'Innere_Erschlie\xdfung____'
        p.displayName = u'Innere Erschlie\xdfung (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'100'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        heading = encode("04_Aufteilung Grünfläche")

        # Spielplatzfläche____
        p = params.spielplatz = arcpy.Parameter()
        p.name = u'Spielplatzfl\xe4che____'
        p.displayName = u'Spielplatzfl\xe4che (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Straßenbegleitgrün____
        p = params.strassenbegleitgruen = arcpy.Parameter()
        p.name = u'Stra\xdfenbegleitgr\xfcn____'
        p.displayName = u'Stra\xdfenbegleitgr\xfcn (%)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Ausgleichs-_und_Ersatzflächen
        p = params.ausgleich_ersatz = arcpy.Parameter()
        p.name = u'Ausgleichs-_und_Ersatzfl\xe4chen'
        p.displayName = u'Ausgleichs- und Ersatzfl\xe4chen'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'0'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        # Allgemeine_Grünflächen
        p = params.allg_gruen = arcpy.Parameter()
        p.name = u'Allgemeine_Gr\xfcnfl\xe4chen'
        p.displayName = u'Allgemeine Gr\xfcnfl\xe4chen'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.value = u'100'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]
        p.category = heading

        return params

    def eingaben_auslesen(self):
        params = self.par
        projectname = params.projectname.value
        teilflaeche = params.teilflaeche.value
        tablepath_teilflaechen = self.tool.teilflaechen
        tablepath_flaechenbilanz = self.tool.flaechenbilanz

        # Oberkategorien
        queries_S1 = ((1, 'Erschliessungsflaeche'),
                      (2, 'Gruenflaeche'),
                      (3, 'Sonstige Flaechen'),
                      (4, 'Nettobauland'))
        fields = ['Teilflaeche_Plangebiet', 'Flaechennutzung_S1', 'Anteil_S1']

        for query in queries_S1:
            where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S1" = ' + "'" + query[1] + "'"
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
            value = 0
            for row in rows:
                value = row[2]
            params[query[0]+2].value = value


        # Nettobauland
        queries_S2 = ((1,'Gewerbeflaeche'),(2,'Nettowohnbauland'))
        fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

        for query in queries_S2:
            where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
            value = 0
            for row in rows:
                value = row[2]
            params[query[0]+6].value = value


        # Verkehr
        queries_S2 = ((1,'Laermschutzanlagen'),(2,'Privat - Innere Erschliessung'),(3,'Oeffentlich - Aeussere Erschliessung'),(4,'Oeffentlich - Innere Erschliessung'))
        fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

        for query in queries_S2:
            where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
            value = 0
            for row in rows:
                value = row[2]
            params[query[0]+8].value = value

        # Gruenflaechen
        queries_S2 = ((1,'Spielplaetze'),(2,'Strassenbegleitgruen'),(3,'Ausgleichs- und Ersatzflaechen'),(4,'Allgemeine Gruenflaechen'))
        fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

        for query in queries_S2:
            where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
            value = 0
            for row in rows:
                value = row[2]
            params[query[0]+10].value = value

        return

    def sliderSummenKontrolle(self, listeSliderID, zielwertSlidersumme):
        params = self.par
        istsumme = 0
        for s in listeSliderID:
            istsumme+=params[s].value

        if istsumme <> zielwertSlidersumme:
            abweichung = zielwertSlidersumme - istsumme
            for s in reversed(listeSliderID):
                alterWert = params[s].value
                neuerWert = params[s].value + abweichung
                if neuerWert < 0:
                    neuerWert = 0
                elif neuerWert > zielwertSlidersumme:
                    neuerWert = zielwertSlidersumme
                abweichung = abweichung + alterWert - neuerWert
                params[s].value = neuerWert
        return

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Auswahl Teilfläche
        if params.projectname.altered and not params.projectname.hasBeenValidated:
            #projectname = params.name.value
            #self.folders.project = projectname

            tablepath_teilflaechen = self.tool.teilflaechen
            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append(row.Name)
            list_teilflaechen = sorted(set(list_teilflaechen))
            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaechen:
                params.teilflaeche.value = list_teilflaechen[0]
                self.eingaben_auslesen()

        # bestehende Eingaben (falls vorhanden) übernehmen
        if params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated:
            self.eingaben_auslesen()

        # Slider generieren
        i = 2
        # Oberkategorien
        listeSliderID = ['ant_verkehrsfl',
                         'ant_gruenfl',
                         'ant_sonstige_fl',
                         'ant_nettobauland']
        zielwertSlidersumme = 100

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        # Nettobauland
        listeSliderID = ['ant_gewerbefl',
                         'ant_nettowohnbauland']

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)


        # Verkehr
        listeSliderID = ['laermschutz',
                         'privatwege',
                         'auessere_erschl',
                         'innere_erschl']

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        # Grünfläche
        listeSliderID = ['spielplatz',
                         'strassenbegleitgruen',
                         'ausgleich_ersatz',
                         'allg_gruen']

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

