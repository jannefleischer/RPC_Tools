# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.flaeche_oekologie.script_Ueberschneidungen import Ueberschneidungen
from rpctools.utils.constants import Nutzungsart
import rpctools.utils.lib_oekologie as lib_oeko
import os

class TbxUeberschneidungen(Tbx):
    """Toolbox Ueberschneidungen"""


    @property
    def label(self):
        return u'Ueberschneidungen anzeigen'

    @property
    def Tool(self):
        return Ueberschneidungen

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = params.name = arcpy.Parameter()
        param.name = u'Projektname'
        param.displayName = u'Projektname'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'


        heading = encode("Bodenbedeckung Nullfall")

        param = params.ueberbauteflaechen_alt = arcpy.Parameter()
        param.name = u'Anteil_an_ueberbauten_Flaechen_alt'
        param.displayName = u'Anteil an ueberbauten Flaechen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.wasser_alt = arcpy.Parameter()
        param.name = u'Anteil_an_natuerlichen_Wasserflaechen_alt'
        param.displayName = u'Anteil an natuerlichen Wasserflaechen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.platten_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Platten_alt'
        param.displayName = u'Anteil an Platten'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.baeume_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Baumen_und_Straeuchern_alt'
        param.displayName = u'Anteil an Baumen und Straeuchern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.rasengittersteine_alt = arcpy.Parameter()
        param.name = u'Anteil_an_wassergebundener_Decke_und_Rasengittersteinen_alt'
        param.displayName = u'Anteil an wassergebundener Decke und Rasengittersteinen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.stauden_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Stauden_alt'
        param.displayName = u'Anteil an Stauden'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.wiese_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Wiesen_alt'
        param.displayName = u'Anteil an Wiesen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.beton_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Asphalt_und_Beton_alt'
        param.displayName = u'Anteil an Asphalt und Beton'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.acker_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Acker_und_offenem_Boden_alt'
        param.displayName = u'Anteil an Acker und offenem Boden'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.kleinpflaster_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Kleinpflaster_alt'
        param.displayName = u'Anteil an Kleinpflaster'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.rasen_alt = arcpy.Parameter()
        param.name = u'Anteil_an_Rasen_alt'
        param.displayName = u'Anteil an Rasen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 100
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading


        heading = encode("Bodenbedeckung Planfall")

        param = params.ueberbauteflaechen_neu = arcpy.Parameter()
        param.name = u'Anteil_an_ueberbauten_Flaechen_neu'
        param.displayName = u'Anteil an ueberbauten Flaechen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.wasser_neu = arcpy.Parameter()
        param.name = u'Anteil_an_natuerlichen_Wasserflaechen_neu'
        param.displayName = u'Anteil an natuerlichen Wasserflaechen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.platten_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Platten_neu'
        param.displayName = u'Anteil an Platten'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.baeume_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Baumen_und_Straeuchern_neu'
        param.displayName = u'Anteil an Baumen und Straeuchern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.rasengittersteine_neu = arcpy.Parameter()
        param.name = u'Anteil_an_wassergebundener_Decke_und_Rasengittersteinen_neu'
        param.displayName = u'Anteil an wassergebundener Decke und Rasengittersteinen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.stauden_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Stauden_neu'
        param.displayName = u'Anteil an Stauden'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.wiese_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Wiesen_neu'
        param.displayName = u'Anteil an Wiesen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.beton_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Asphalt_und_Beton_neu'
        param.displayName = u'Anteil an Asphalt und Beton'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.acker_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Acker_und_offenem_Boden_neu'
        param.displayName = u'Anteil an Acker und offenem Boden'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.kleinpflaster_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Kleinpflaster_neu'
        param.displayName = u'Anteil an Kleinpflaster'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 0
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        param = params.rasen_neu = arcpy.Parameter()
        param.name = u'Anteil_an_Rasen_neu'
        param.displayName = u'Anteil an Rasen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 100
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        return params

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


    def eingaben_auslesen(self):
        params = self.par
        projektname = params.name.value

        workspace_projekt_oekologie = self.folders.get_db('FGDB_Flaeche_und_Oekologie.gdb', projektname)
        tabelle_boden_anteile = os.path.join(workspace_projekt_oekologie, "Bodenbedeckung_Anteile")

        if  not arcpy.Exists(tabelle_boden_anteile):
            lib_oeko.create_bodenbedeckung(projektname)


        fields = ["IDBodenbedeckung", "Planfall", "Bodenbedeckung_Anteil"]
        cursor = arcpy.da.SearchCursor(tabelle_boden_anteile, fields)
        for row in cursor:
            if row[1] == 0 and row[0] == 1:
                 params['ueberbauteflaechen_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 2:
                 params['wasser_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 3:
                 params['platten_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 4:
                 params['baeume_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 5:
                 params['rasengittersteine_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 6:
                 params['stauden_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 7:
                 params['wiese_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 8:
                 params['beton_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 9:
                 params['acker_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 10:
                 params['kleinpflaster_alt'].value = row[2]
            elif row[1] == 0 and row[0] == 11:
                 params['rasen_alt'].value = row[2]
            elif row[1] == 1 and row[0] == 1:
                 params['ueberbauteflaechen_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 2:
                 params['wasser_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 3:
                 params['platten_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 4:
                 params['baeume_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 5:
                 params['rasengittersteine_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 6:
                 params['stauden_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 7:
                 params['wiese_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 8:
                 params['beton_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 9:
                 params['acker_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 10:
                 params['kleinpflaster_neu'].value = row[2]
            elif row[1] == 1 and row[0] == 11:
                 params['rasen_neu'].value = row[2]


        return


    def _updateParameters(self, params):

        if params.name.altered and not params.name.hasBeenValidated:
                self.eingaben_auslesen()

        listeSliderID = ['ueberbauteflaechen_alt',
                         'wasser_alt',
                         'platten_alt',
                         'baeume_alt',
                         'rasengittersteine_alt',
                         'stauden_alt',
                         'wiese_alt',
                         'beton_alt',
                         'acker_alt',
                         'kleinpflaster_alt',
                         'rasen_alt']

        zielwertSlidersumme = 100

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)


        listeSliderID = ['ueberbauteflaechen_neu',
                         'wasser_neu',
                         'platten_neu',
                         'baeume_neu',
                         'rasengittersteine_neu',
                         'stauden_neu',
                         'wiese_neu',
                         'beton_neu',
                         'acker_neu',
                         'kleinpflaster_neu',
                         'rasen_neu']

        for r in listeSliderID:
            if params[r].altered:
                self.sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

		return


    def bodenbedeckung_eintragen(self, polygon, bodenbedeckung, planfall):
        column_values = {
            'IDBodenbedeckung': bodenbedeckung,
            'SHAPE@': polygon
        }

        if planfall:
            self.insert_rows_in_table('Bodenbedeckung_Planfall', column_values, "FGDB_Flaeche_und_Oekologie.gdb")
        else:
            self.insert_rows_in_table('Bodenbedeckung_Nullfall', column_values, "FGDB_Flaeche_und_Oekologie.gdb")