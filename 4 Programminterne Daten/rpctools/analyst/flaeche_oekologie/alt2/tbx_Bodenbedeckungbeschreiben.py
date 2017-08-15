# -*- coding: utf-8 -*-
import os
import sys
import arcpy
from os.path import join
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.flaeche_oekologie.Bodenbedeckungbeschreiben import BodenbedeckungBeschreiben

class TbxBodenbedeckungbeschreiben(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 1: Bodenbedeckung beschreiben')

    @property
    def Tool(self):
        return BodenbedeckungBeschreiben

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = params.projectname = arcpy.Parameter()
        param.name = u'Projektname'
        param.displayName = u'Projekt'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'


        # Teilfl�che
        param = params.teilflaeche = arcpy.Parameter()
        param.name = u'Teilfl\xe4che'
        param.displayName = u'Teilfl\xe4che'
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
        return


    def _updateParameters(self, params):

        if params.projectname.altered and not params.projectname.hasBeenValidated:
            tablepath_teilflaechen = join(self.folders.get_db("FGDB_Definition_Projekt.gdb", self.par.projectname.value), "Teilflaechen_Plangebiet")
            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append(row.Name)
            list_teilflaechen = sorted(set(list_teilflaechen))
            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaechen:
                params.teilflaeche.value = list_teilflaechen[0]
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


