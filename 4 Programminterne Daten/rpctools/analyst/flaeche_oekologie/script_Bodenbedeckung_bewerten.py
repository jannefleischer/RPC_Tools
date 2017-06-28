# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from rpctools.utils.params import Tool

class BodenbedeckungBewertung(Tool):
    """BodenbedeckungBewertung"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        path_bodenbedeckung = self.folders.get_table('Bodenbedeckung_Anteile', "FGDB_Flaeche_und_Oekologie.gdb", projekt)

        boden_anteile_alt = [0,0,0,0,0,0,0,0,0,0,0]
        boden_anteile_neu = [0,0,0,0,0,0,0,0,0,0,0]

        fields = ["IDBodenbedeckung", "Planfall", "Bodenbedeckung_Anteil"]
        cursor = arcpy.da.SearchCursor(path_bodenbedeckung, fields)
        for row in cursor:
            if row[1] == 0 and row[0] == 1:
                 boden_anteile_alt[0] = row[2]
            elif row[1] == 0 and row[0] == 2:
                 boden_anteile_alt[1] = row[2]
            elif row[1] == 0 and row[0] == 3:
                 boden_anteile_alt[2] = row[2]
            elif row[1] == 0 and row[0] == 4:
                 boden_anteile_alt[3] = row[2]
            elif row[1] == 0 and row[0] == 5:
                 boden_anteile_alt[4] = row[2]
            elif row[1] == 0 and row[0] == 6:
                 boden_anteile_alt[5] = row[2]
            elif row[1] == 0 and row[0] == 7:
                 boden_anteile_alt[6] = row[2]
            elif row[1] == 0 and row[0] == 8:
                 boden_anteile_alt[7] = row[2]
            elif row[1] == 0 and row[0] == 9:
                 boden_anteile_alt[8] = row[2]
            elif row[1] == 0 and row[0] == 10:
                 boden_anteile_alt[9] = row[2]
            elif row[1] == 0 and row[0] == 11:
                 boden_anteile_alt[10] = row[2]
            elif row[1] == 1 and row[0] == 1:
                 boden_anteile_neu[0] = row[2]
            elif row[1] == 1 and row[0] == 2:
                 boden_anteile_neu[1] = row[2]
            elif row[1] == 1 and row[0] == 3:
                 boden_anteile_neu[2] = row[2]
            elif row[1] == 1 and row[0] == 4:
                 boden_anteile_neu[3] = row[2]
            elif row[1] == 1 and row[0] == 5:
                 boden_anteile_neu[4] = row[2]
            elif row[1] == 1 and row[0] == 6:
                 boden_anteile_neu[5] = row[2]
            elif row[1] == 1 and row[0] == 7:
                 boden_anteile_neu[6] = row[2]
            elif row[1] == 1 and row[0] == 8:
                 boden_anteile_neu[7] = row[2]
            elif row[1] == 1 and row[0] == 9:
                 boden_anteile_neu[8] = row[2]
            elif row[1] == 1 and row[0] == 10:
                 boden_anteile_neu[9] = row[2]
            elif row[1] == 1 and row[0] == 11:
                 boden_anteile_neu[10] = row[2]

        plangebiet_ha = 0
        path_teilflaechen = self.folders.get_table('Teilflaechen_Plangebiet', "FGDB_Definition_Projekt.gdb", projekt)
        fields = ["SHAPE_Area"]
        cursor = arcpy.da.SearchCursor(path_teilflaechen, fields)
        for row in cursor:
            plangebiet_ha += row[0]

        boden_ha_absolut_nullfall = [0,0,0,0,0,0,0,0,0,0,0]
        boden_ha_absolut_planfall = [0,0,0,0,0,0,0,0,0,0,0]

        for x in xrange(11):
            boden_absolut_alt[x] = boden_anteile_alt[x] * plangebiet_ha
            boden_absolut_neu[x] = boden_anteile_neu[x] * plangebiet_ha

        #Klima
        waermespeicherung_multiplikator = [0,0,0.1,0.2,0.3,0.3,1,0.8,0.9,1,1]
        staubbindevermoegen_multiplikator = [0,0,0,0.1,0.1,0.1,0.2,0.8,0.4,0.4,1]
        #Boden
        schadstoffrueckhaltung_multiplikator = [0,0,0.2,0.3,0.4,0.5,0.8,0.8,0.8,0.8,0]
        durchlaessigkeit_multiplikator = [0,0.1,0.2,0.4,0.6,1,0.8,1,1,1,1]
        bodenueberformung_multiplikator = [0,0,0,0,0,0.8,0.8,0.8,0.8,1,1]
        #Wasser
        oberflaechenabfluss_multiplikator = [0,0.1,0.4,0.7,0.6,1,0.8,1,1,1,0]
        grundwasserneubildung_multiplikator = [0,0,0.3,0.5,0.8,1,0.5,0.4,0.5,0.5,1]
        regenwasserversickerung_multiplikator = [0,0.1,0.4,0.5,0.5,1,0.8,0.9,0.9,1,1]
        biotopausbildungsvermoegen_multiplikator = [0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.9,0.9,1,1]

        # 0 = Überbaute Fläche
        # 1 = Asphalt / Beton
        # 2 = Platten
        # 3 = Kleinpflaster
        # 4 = wassergeb. Decke / Rasengittersteine
        # 5 = offener Boden / Acker
        # 6 = Rasen
        # 7 = Bäume / Sträucher
        # 9 = Stauden
        # 10 = Wiese
        # 11 = natürliche Wasserflächen

        faktor_waermespeicherung_nullfall = []
        faktor_waermespeicherung_planfall = []

        faktor_staubbindevermoegen_nullfall = []
        faktor_staubbindevermoegen_planfall = []

        faktor_schadstoffrueckhaltung_nullfall = []
        faktor_schadstoffrueckhaltung_planfall = []

        faktor_durchlaessigkeit_nullfall = []
        faktor_durchlaessigkeit_planfall = []

        faktor_bodenueberformung_nullfall = []
        faktor_bodenueberformung_planfall = []

        faktor_oberflaechenabfluss_nullfall = []
        faktor_oberflaechenabfluss_planfall = []

        faktor_grundwasserneubildung_nullfall = []
        faktor_grundwasserneubildung_planfall = []

        faktor_regenwasserversickerung_nullfall = []
        faktor_regenwasserversickerung_planfall = []

        faktor_biotopausbildungsvermoegen_nullfall = []
        faktor_biotopausbildungsvermoegen_planfall = []


        for x in xrange(11):
            faktor_waermespeicherung_nullfall.append(boden_anteile_alt[x] * waermespeicherung_multiplikator[x])
            faktor_waermespeicherung_planfall.append(boden_anteile_neu[x] * waermespeicherung_multiplikator[x])

            faktor_staubbindevermoegen_nullfall.append(boden_anteile_alt[x] * staubbindevermoegen_multiplikator[x])
            faktor_staubbindevermoegen_planfall.append(boden_anteile_neu[x] * staubbindevermoegen_multiplikator[x])

            faktor_schadstoffrueckhaltung_nullfall.append(boden_anteile_alt[x] * schadstoffrueckhaltung_multiplikator[x])
            faktor_schadstoffrueckhaltung_planfall.append(boden_anteile_neu[x] * schadstoffrueckhaltung_multiplikator[x])

            faktor_durchlaessigkeit_nullfall.append(boden_anteile_alt[x] * durchlaessigkeit_multiplikator[x])
            faktor_durchlaessigkeit_planfall.append(boden_anteile_neu[x] * durchlaessigkeit_multiplikator[x])

            faktor_bodenueberformung_nullfall.append(boden_anteile_alt[x] * bodenueberformung_multiplikator[x])
            faktor_bodenueberformung_planfall.append(boden_anteile_neu[x] * bodenueberformung_multiplikator[x])

            faktor_oberflaechenabfluss_nullfall.append(boden_anteile_alt[x] * oberflaechenabfluss_multiplikator[x])
            faktor_oberflaechenabfluss_planfall.append(boden_anteile_neu[x] * oberflaechenabfluss_multiplikator[x])

            faktor_grundwasserneubildung_nullfall.append(boden_anteile_alt[x] * grundwasserneubildung_multiplikator[x])
            faktor_grundwasserneubildung_planfall.append(boden_anteile_neu[x] * grundwasserneubildung_multiplikator[x])

            faktor_regenwasserversickerung_nullfall.append(boden_anteile_alt[x] * regenwasserversickerung_multiplikator[x])
            faktor_regenwasserversickerung_planfall.append(boden_anteile_neu[x] * regenwasserversickerung_multiplikator[x])

            faktor_biotopausbildungsvermoegen_nullfall.append(boden_anteile_alt[x] * biotopausbildungsvermoegen_multiplikator[x])
            faktor_biotopausbildungsvermoegen_planfall.append(boden_anteile_neu[x] * biotopausbildungsvermoegen_multiplikator[x])



        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_staubbindevermoegen_nullfall = sum(faktor_staubbindevermoegen_nullfall) / 11
        quotient_staubbindevermoegen_planfall = sum(faktor_staubbindevermoegen_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        quotient_waermespeicherung_nullfall = sum(faktor_waermespeicherung_nullfall) / 11
        quotient_waermespeicherung_planfall = sum(faktor_waermespeicherung_planfall) / 11

        arcpy.AddMessage()