# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from collections import OrderedDict
import arcpy

from rpctools.utils.params import Tbx
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import TeilflaechenVerwalten


class TbxTeilflaechenMultiTest(Tbx):
    """Toolbox to name Teilflächen"""
    _nutzungsarten = None

    @property
    def label(self):
        return u'Schritt 2 Test: Multivalue'

    @property
    def Tool(self):
        return TeilflaechenVerwalten

    @property
    def nutzungsart_table(self):
        return self.folders.get_table('Nutzungsart')

    @property
    def teilflaechen_table(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

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

    def get_teilflaechen(self, nutzungsart=None):

        columns = ['id_teilflaeche', 'Name', 'Flaeche_ha', 'Nutzungsart']
        rows = arcpy.da.SearchCursor(self.teilflaechen_table, columns)
        teilflaechen = OrderedDict()

        for flaechen_id, name, ha, nutzungsart_id in rows:
            teilflaechen[flaechen_id] = (name, ha, nutzungsart_id)

        return teilflaechen

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        p = params.projectname = arcpy.Parameter()
        p.name = u'Projekt'
        p.displayName = u'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        projects = self.folders.get_projects()
        p.filter.list = projects
        p.value = '' if len(projects) == 0 else p.filter.list[0]

        p = params.flaechen_table = arcpy.Parameter()
        p.displayName='Teilflächen'
        p.name='flaechen_table'
        p.datatype='GPValueTable'
        p.direction='Input'
        p.parameterType='Required'
        p.parameterDependencies = [params.projectname.name]
        p.columns = [
            ['GPLong', u'id'],
            ['GPString', u'Name'],
            ['GPLong', u'Hektar'],
            ['GPString', u'Nutzungsart']
        ]
        p.filters[2].type = 'Range'
        p.filters[2].list = [0, 10000]
        p.filters[3].type = 'ValueList'
        p.filters[3].list = self.nutzungsarten.keys()
        self.update_table()

        return params

    def update_table(self):
        table = self.par.flaechen_table
        teilflaechen = self.get_teilflaechen()
        rows = []
        for flaechen_id, (name, ha, nutzungsart_id) in teilflaechen.iteritems():
            nutzungsart = self.nutzungsarten.keys()[
                self.nutzungsarten.values().index(nutzungsart_id)]
            rows.append([flaechen_id, name, ha, nutzungsart])

        n_rows = len(teilflaechen.keys())
        #table.filters[0].list = teilflaechen.keys()
        table.values = rows[:n_rows]

    def _updateParameters(self, params):
        if params.changed('projectname'):
            self.update_table()
        if params.changed('flaechen_table'):
            self.update_table()
        return params


    def _updateMessages(self, params):
        pass

if __name__ == '__main__':
    t = TbxTeilflaechenMultiTest()
    t._getParameterInfo()