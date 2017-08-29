# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from rpctools.utils.params import Tool
from rpctools.diagrams.diagram_oekologie import Dia_Integrationsgrad

class Integrationsgrad(Tool):
    """Integrationsgrad"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    aussengrenze = 0.0
    gemeinsame_grenze = 0.0

    def add_outputs(self):
        self.output.add_layer(groupname = "oekologie", featureclass = "Grenze_Siedlungskoerper", template_layer = "Grenze_Siedlungskoerper", template_folder="oekologie",  zoom=False, disable_other = True)

        diagram = Dia_Integrationsgrad(projectname=self.par.name.value)
        self.output.add_diagram(diagram)

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    def run(self):
        params = self.par
        projekt = self.projectname
        table_grenzlinie = self.folders.get_table("Grenze_Siedlungskoerper", "FGDB_Flaeche_und_Oekologie.gdb")
        cursor = arcpy.da.SearchCursor(table_grenzlinie, ["SHAPE_Length"])
        for row in cursor:
            self.gemeinsame_grenze += row[0]

        teilflaechen = self.folders.get_table("Teilflaechen_Plangebiet", "FGDB_Definition_Projekt.gdb")
        path_aussengrenze = os.path.join(self.folders.get_db("FGDB_Flaeche_und_Oekologie.gdb"),"Aussengrenze_Plangebiet")
        if arcpy.Exists(path_aussengrenze):
            arcpy.Delete_management(path_aussengrenze)
        arcpy.Dissolve_management(teilflaechen, path_aussengrenze)
        cursor = arcpy.da.SearchCursor(path_aussengrenze, ["SHAPE_Length"])
        for row in cursor:
            self.aussengrenze += row[0]
        arcpy.Delete_management(path_aussengrenze)

        table_integrationsgrad = self.folders.get_table("Integrationsgrad", "FGDB_Flaeche_und_Oekologie.gdb")
        cursor = arcpy.da.UpdateCursor(table_integrationsgrad, ["*"])
        for row in cursor:
            cursor.deleteRow()

        gemeinsame_grenze = round(self.gemeinsame_grenze / self.aussengrenze, 3) * 100
        neue_grenze = 100 - gemeinsame_grenze
        column_values = {"Grenze": [u"Überschneidung mit bestehender Siedlungsfläche", u"Grenze ohne Überschneidung mit Siedlungsfläche"],
                                "Umfang": [neue_grenze, gemeinsame_grenze]}
        self.parent_tbx.insert_rows_in_table("Integrationsgrad", column_values)

class Integrationsgrad_loeschen(Tool):
    """Integrationsgrad_loeschen"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        table_grenzlinie = self.folders.get_table("Grenze_Siedlungskoerper", "FGDB_Flaeche_und_Oekologie.gdb")

        cursor = arcpy.da.UpdateCursor(table_grenzlinie, ["*"])
        for row in cursor:
            cursor.deleteRow()

        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
