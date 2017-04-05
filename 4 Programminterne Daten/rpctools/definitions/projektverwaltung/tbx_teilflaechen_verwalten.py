# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from collections import OrderedDict
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import TeilflaechenVerwalten


class TbxFlaechendefinition(Tbx):
    _nutzungsarten = None

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        p = params.project = arcpy.Parameter()
        p.name = u'Projekt'
        p.displayName = u'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        projects = self.folders.get_projects()
        p.filter.list = projects
        p.value = '' if len(projects) == 0 else p.filter.list[0]

        # Teilfläche
        p = params.teilflaeche = arcpy.Parameter()
        p.name = encode(u'Teilfläche')
        p.displayName = encode(u'Teilfläche')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []

        return params

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
            representation = ' | '.join([
                'Nr. {}'.format(row.OBJECTID),
                '{} ha'.format(round(row.Flaeche_ha, 2)),
                row.NAME
            ])
            teilflaechen[representation] = row.OBJECTID, row.Name
        return teilflaechen

    def get_nutzungsart_id(self, flaechen_id):
        where = '"OBJECTID" = {}'.format(flaechen_id)
        row = arcpy.SearchCursor(self.teilflaechen_table, where).next()
        return row.Nutzungsart


class TbxTeilflaecheVerwalten(TbxFlaechendefinition):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'Schritt 2: Teilflaechen verwalten'

    @property
    def Tool(self):
        return TeilflaechenVerwalten

    def _getParameterInfo(self):
        params = super(TbxTeilflaecheVerwalten, self)._getParameterInfo()
        # Name
        p = params.name = arcpy.Parameter()
        p.name = u'Name'
        p.displayName = u'Name'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'

        # Nutzungsart
        p = params.nutzungsart = arcpy.Parameter()
        p.name = encode(u'Nutzungsart')
        p.displayName = encode(u'Nutzungsart')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = self.nutzungsarten.keys()

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if params.changed('project'):
            params.teilflaeche.value = ''
            self.update_teilflaechen_list()

        flaeche = params.teilflaeche.value
        if flaeche:
            flaechen_id, flaechenname = self.teilflaechen[flaeche]
            if params.changed('project', 'teilflaeche'):
                self.update_teilflaechen_inputs(flaechen_id, flaechenname)

            if params.changed('name'):
                self.folders.update_table(
                    'Teilflaechen_Plangebiet',
                    {'Name': params.name.value},
                    where='id_teilflaeche={}'.format(flaechen_id))
                # update teilflaechen but keep selected index
                idx = self.par.selected_index('teilflaeche')
                self.update_teilflaechen_list()
                params.teilflaeche.value = params.teilflaeche.filter.list[idx]

            if params.changed('nutzungsart'):
                nutzungsart_id = self.nutzungsarten[params.nutzungsart.value]
                self.folders.update_table(
                    'Teilflaechen_Plangebiet',
                    {'Nutzungsart': nutzungsart_id},
                    where='id_teilflaeche={}'.format(flaechen_id))

        return params


    def update_teilflaechen_list(self):
        list_teilflaechen = self.tool.teilflaechen.keys()
        self.par.teilflaeche.filter.list = list_teilflaechen

        if list_teilflaechen:
            flaeche = list_teilflaechen[0]
            self.par.teilflaeche.value = flaeche

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        self.par.name.value = flaechenname
        nutzungsart_id = self.get_nutzungsart_id(flaechen_id)
        nutzungsarten = self.nutzungsarten
        nutzungsart = nutzungsarten.keys()[
            nutzungsarten.values().index(nutzungsart_id)]
        self.par.nutzungsart.value = nutzungsart

    def _updateMessages(self, params):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        if params.project.value != None and params.name.value != None:
            projectname = params.project.value
            tablepath_teilflaechen = self.tool.teilflaechen_table
            namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

            params.name.clearMessage()

            for row in namen_cursor:
                if params.name.value == row[0]:
                    params.name.setErrorMessage("Name wurde bereits vergeben.")


if __name__ == '__main__':

    t = TbxTeilflaecheVerwalten()
    params = t.getParameterInfo()
    t.print_test_parameters()
    t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()