# -*- coding: utf-8 -*-

import arcpy
import os
from collections import OrderedDict

from rpctools.utils.params import Tool


class TeilflaechenVerwalten(Tool):

    _param_projectname = 'project'
    _dbname = 'FGDB_Definition_Projekt.gdb'
    _nutzungsarten = None
    _seperator = ' | '

    @property
    def teilflaechen_table(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

    @property
    def nutzungsart_table(self):
        return self.folders.get_table('Nutzungsart')

    @property
    def nutzungsarten(self):
        # only fetch once, won't change because it's a base definition
        if self._nutzungsarten is None:
            table = self.folders.get_base_table(
                'FGDB_Definition_Projekt_Tool.gdb', 'Nutzungsarten')
            fields = ['nutzungsart', 'id']
            rows = arcpy.da.SearchCursor(table, fields)
            self._nutzungsarten = OrderedDict([r for r in rows])
        return self._nutzungsarten

    @property
    def teilflaechen(self):
        rows = arcpy.SearchCursor(self.teilflaechen_table)
        teilflaechen = OrderedDict()
        for row in rows:
            representation = self._seperator.join([
                'Nr. {}'.format(row.OBJECTID),
                '{} ha'.format(round(row.Flaeche_ha, 2)),
                row.NAME
            ])
            teilflaechen[representation] = row.OBJECTID
        return teilflaechen

    def get_flaechenname(self, representation):
        return representation.split(self._seperator)[-1]

    def get_nutzungsart_id(self, flaechen_id):
        where = '"OBJECTID" = {}'.format(flaechen_id)
        row = arcpy.SearchCursor(self.teilflaechen_table, where).next()
        return row.Nutzungsart

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
