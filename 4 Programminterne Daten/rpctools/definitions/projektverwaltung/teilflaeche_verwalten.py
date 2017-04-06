# -*- coding: utf-8 -*-

import arcpy
import os
from collections import OrderedDict

from rpctools.utils.params import Tool


class TeilflaechenVerwalten(Tool):

    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        # Teilfläche speichern
        flaechenname = self.par.teilflaeche.value
        alter_name = flaechenname.split('|')[2].strip()
        neuer_name = self.par.name.value

        flaechen_id = self.teilflaechen[flaechenname]
        where = '"OBJECTID" = {}'.format(flaechen_id)

        nutzungsart_id = self.nutzungsarten[self.par.nutzungsart.value]

        rows = arcpy.UpdateCursor(self.teilflaechen_table, where)
        for row in rows:
            row.NAME = neuer_name  #self.par.name.valueAsText
            row.Nutzungsart = nutzungsart_id
            rows.updateRow(row)

        del rows


        # Name der Teilfläche in anderen Tabellen aktualisieren

        path_definition = self.db

        tables = [
            ('Flaechenbilanz', 'Teilflaeche_Plangebiet'),
            ('Gebaeude_Details', 'Teilflaeche_Plangebiet'),
            ('Gewerbe_Anteile', 'teilflaeche'),
            ('Gewerbe_Beschaeftigte', 'Teilflaeche_Plangebiet'),
            ('Gewerbe_Betriebsflaechen', 'teilflaeche'),
            ('Gewerbe_Betriebsstruktur', 'teilflaeche'),
            ('Gewerbe_Teilflaechen', 'teilflaeche'),
            ('Grundlagen', 'Name'),
            ('Versorgung_Verkaufsflaechen', 'Teilflaeche_Plangebiet'),
            ('Wohneinheiten_Details', 'Teilflaeche_Plangebiet'),
        ]
        for tablename, attr in tables:
            self.rename_flaeche(path_definition, tablename, attr,
                                alter_name, neuer_name)

        path_oekologie = self.folders.get_db('FGDB_Flaeche_und_Oekologie.gdb')
        tables = [
            ('Bodenbedeckung', 'Teilflaeche'),
        ]
        for tablename, attr in tables:
            self.rename_flaeche(path_oekologie, tablename, attr,
                                alter_name, neuer_name)

    @staticmethod
    def rename_flaeche(path_definition, tablename,
                       attr, alter_name, neuer_name):
        table = os.path.join(path_definition, tablename)
        rows = arcpy.UpdateCursor(table)
        for row in rows:
            if getattr(row, attr) == alter_name:
                setattr(row, attr, neuer_name)
                rows.updateRow(row)
