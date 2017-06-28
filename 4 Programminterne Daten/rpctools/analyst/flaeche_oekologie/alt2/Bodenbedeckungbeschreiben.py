# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# Bodenbedeckungbeschreiben.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
import os
import arcpy
import sys
from os.path import join
from rpctools.utils.params import Tool

class BodenbedeckungBeschreiben(Tool):

    param_projectname = 'projectname'
    _dbname = 'FGDB_Flaeche_und_Oekologie.gdb'

    def run(self):
        parameters = self.par
        teilflaeche = self.par.teilflaeche.value

        ws_oekologie = self.folders.get_db("FGDB_Flaeche_und_Oekologie.gdb")
        workspace_projekt = self.folders.get_db("FGDB_Definition_Projekt.gdb")
        path_nullfall = join(ws_oekologie, "Bodenbedeckung_Nullfall")
        path_planfall = join(ws_oekologie, "Bodenbedeckung_Planfall")

        cursor = arcpy.da.UpdateCursor(path_nullfall, ["Teilflaeche"])
        for flaeche in cursor:
            if flaeche[0] == teilflaeche:
                cursor.deleteRow()

        fields = ["NF_ueberbauteFlaechen", "NF_AsphaltBeton", "NF_Platten", "NF_Kleinpflaster", "NF_Rasengitter",
                    "NF_Acker", "NF_Rasen", "NF_BaeumeStraeucher", "NF_Stauden", "NF_Wiese", "NF_Wasserflaeche",
                    "Teilflaeche"]
        cursor = arcpy.da.InsertCursor(path_nullfall, fields)
        cursor.insertRow((self.par.ueberbauteflaechen_alt.value,
                        self.par.beton_alt.value,
                        self.par.platten_alt.value,
                        self.par.kleinpflaster_alt.value,
                        self.par.rasengittersteine_alt.value,
                        self.par.acker_alt.value,
                        self.par.rasen_alt.value,
                        self.par.baeume_alt.value,
                        self.par.stauden_alt.value,
                        self.par.wiese_alt.value,
                        self.par.wasser_alt.value,
                        teilflaeche
        ))



        fields = ["PF_ueberbauteFlaechen", "PF_AsphaltBeton", "PF_Platten", "PF_Kleinpflaster", "PF_Rasengitter",
                    "PF_Acker", "PF_Rasen", "PF_BaeumeStraeucher", "PF_Stauden", "PF_Wiese", "PF_Wasserflaeche", "Teilflaeche"]
        cursor = arcpy.da.UpdateCursor(path_planfall, fields)
        for flaeche in cursor:
            if flaeche[0] == teilflaeche:
                cursor.deleteRow()

        cursor = arcpy.da.InsertCursor(path_planfall, fields)
        cursor.insertRow((self.par.ueberbauteflaechen_neu.value,
                        self.par.beton_neu.value,
                        self.par.platten_neu.value,
                        self.par.kleinpflaster_neu.value,
                        self.par.rasengittersteine_neu.value,
                        self.par.acker_neu.value,
                        self.par.rasen_neu.value,
                        self.par.baeume_neu.value,
                        self.par.stauden_neu.value,
                        self.par.wiese_neu.value,
                        self.par.wasser_neu.value,
                        teilflaeche
        ))

        return



