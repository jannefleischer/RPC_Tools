# -*- coding: utf-8 -*-

import os
import sys
import arcpy
import rpctools.utils.chronik as c
from rpctools.utils.params import Tool

class Wohnflaechendichte(Tool):
    """Wohnflaechendichte-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        self.output.delete_output("Gesamtsumme")

        gemeinde_werte = lib_einnahmen.get_values(["Summe_Einnahmenbilanz"], self.projectname)

        symbology = lib_einnahmen.get_symbology(gemeinde_werte, 1)

        self.output.add_layer(
            groupname = "einnahmen",
            featureclass = "Gemeindebilanzen",
            template_layer = symbology,
            template_folder = "einnahmen",
            name = "Gesamtsumme",
            disable_other = True,
            symbology = {'valueField': "Summe_Einnahmenbilanz"},
            label_replace = {'Einw_Saldo': 'Summe_Einnahmenbilanz'}
        )

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    def run(self):
        """run Wohnflaechendichte Tool"""

        par = self.par
        projektname = self.projectname
        tablepath_wohnflaeche = self.folders.get_table('Wohnflaechendichte', "FGDB_Flaeche_und_Oekologie.gdb")
        tablepath_de = self.folders.get_base_table("FGDB_Flaeche_und_Oekologie_Tool.gdb", 'GrundlagenDE')
        tablepath_wohngebaeude = self.folders.get_table('Wohnen_WE_in_Gebaeudetypen', "FGDB_Definition_Projekt.gdb")
        table_teilflaechen = self.folders.get_table("Teilflaechen_Plangebiet", "FGDB_Definition_Projekt.gdb")
        tablepath_rahmendaten = self.folders.get_table("Projektrahmendaten", "FGDB_Definition_Projekt.gdb")

        mean_wohnflaeche_efh = par.flaeche_efh.value
        mean_wohnflaeche_dh = par.flaeche_dh.value
        mean_wohnflaeche_rh = par.flaeche_rh.value
        mean_wohnflaeche_mfh = par.flaeche_mfh.value

        we_efh = 0
        we_dh = 0
        we_rh = 0
        we_mfh = 0

        cursor = arcpy.da.SearchCursor(tablepath_wohngebaeude, ["IDTeilflaeche", "IDGebaeudetyp", "WE"])
        for gebaeude in cursor:
            if gebaeude[0] == self.parent_tbx.id_teilflaeche:
                if gebaeude[1] == 1:
                    we_efh += gebaeude[2]
                if gebaeude[1] == 2:
                    we_efh += gebaeude[2]
                if gebaeude[1] == 3:
                    we_efh += gebaeude[2]
                if gebaeude[1] == 4:
                    we_efh += gebaeude[2]

        wohnflaeche_efh_qm = mean_wohnflaeche_efh * we_efh
        wohnflaeche_dh_qm = mean_wohnflaeche_dh * we_dh
        wohnflaeche_rh_qm = mean_wohnflaeche_rh * we_rh
        wohnflaeche_mfh_qm = mean_wohnflaeche_mfh * we_mfh

        wohnflaeche_gesamt_qm = wohnflaeche_efh_qm + wohnflaeche_dh_qm + wohnflaeche_rh_qm + wohnflaeche_mfh_qm

        teilflaeche_gesamt_qm = 0
        cursor = arcpy.da.SearchCursor(table_teilflaechen, ["id_teilflaeche", "Flaeche_ha"])
        for teilflaeche in cursor:
            if teilflaeche[0] == self.parent_tbx.id_teilflaeche:
                teilflaeche_gesamt_qm = teilflaeche[1] * 10000

        wohnflaechendichte_projekt = round((wohnflaeche_gesamt_qm / teilflaeche_gesamt_qm) * 100)
        self.wohnflaechendichte_projekt = int(wohnflaechendichte_projekt)

        ags_projekt = ""
        cursor = arcpy.da.SearchCursor(tablepath_rahmendaten, "AGS")
        for row in cursor:
            ags_projekt = row[0]
            ags_kreis = ags_projekt[0:5]

        wohnflaechendichte_kreis = 0
        kreistyp = 0
        fields = ["AGS", "Siedlungsstruktureller_Kreistyp", "Wohnflaeche_in_Wohngebaeuden_in_qm", "Gebaeude_und_Freiflaeche_Wohnen_in_ha"]
        where = '"AGS"' + "='" + ags_kreis  + "'"
        cursor = arcpy.da.SearchCursor(tablepath_de, fields, where)
        for kreis in cursor:
            kreistyp = kreis[1]
            wohnflaechendichte_kreis = round(kreis[2] / (kreis[3] * 10000) * 100)
        self.wohnflaechendichte_kreis = int(wohnflaechendichte_kreis)

        wohnflaechendichte_kreise = 0
        anzahl_kreise = 0
        where = '"Siedlungsstruktureller_Kreistyp"' + "=" + str(kreistyp)
        cursor = arcpy.da.SearchCursor(tablepath_de, fields, where)
        for kreis in cursor:
            wohnflaechendichte_kreise += kreis[2] / (kreis[3] * 10000) * 100
            anzahl_kreise += 1
        wohnflaechendichte_kreistyp = round(wohnflaechendichte_kreise / anzahl_kreise)
        self.wohnflaechendichte_kreistyp = int(wohnflaechendichte_kreistyp)

        arcpy.AddMessage("Projektflaeche: " + str(self.wohnflaechendichte_projekt))
        arcpy.AddMessage("Kreis: " + str(self.wohnflaechendichte_kreis))
        arcpy.AddMessage("Kreistyp: " + str(self.wohnflaechendichte_kreistyp))

