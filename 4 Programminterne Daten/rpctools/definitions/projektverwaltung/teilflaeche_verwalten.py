# -*- coding: utf-8 -*-

import arcpy
import os
from collections import OrderedDict

from rpctools.utils.params import Tool
from rpctools.diagrams.diagram_teilflaechen import DiaTeilflaechen
from rpctools.utils.constants import Nutzungsart


class TeilflaechenVerwalten(Tool):

    _param_projectname = 'projectname'
    _workspace = 'FGDB_Definition_Projekt.gdb'
    
    def add_outputs(self):
        fc = "Teilflaechen_Plangebiet"
        layer = "Teilflächen des Plangebiets"
        self.output.add_layer("projektdefinition", layer, fc)
        self.output.add_diagram(DiaTeilflaechen())

    def run(self):
        df_areas = self.parent_tbx.df_areas
        
        # delete rows not corresponding to set type of use wohnen/gewerbe/einzelhandel
        for index, area in df_areas.iterrows():
            tou_id = area['Nutzungsart']
            area_id = area['id_teilflaeche']
            
            if tou_id != Nutzungsart.WOHNEN:
                tables = ['Wohnen_WE_in_Gebaeudetypen',
                          'Wohnen_Struktur_und_Alterung_WE']
                for table in tables:
                    self.parent_tbx.delete_rows_in_table(
                        table, pkey=dict(IDTeilflaeche=area_id))
            if tou_id != Nutzungsart.GEWERBE:
                tables = ['Gewerbe_Anteile', 'Gewerbe_Arbeitsplaetze']
                for table in tables:
                    self.parent_tbx.delete_rows_in_table(
                        table, pkey=dict(IDTeilflaeche=area_id))
            if tou_id != Nutzungsart.EINZELHANDEL:
                table = 'Einzelhandel_Verkaufsflaechen'
                self.parent_tbx.delete_rows_in_table(
                    table, pkey=dict(IDTeilflaeche=area_id))
        
        self.parent_tbx.dataframe_to_table('Teilflaechen_Plangebiet',
                                           df_areas, ['id_teilflaeche'],
                                           upsert=False)