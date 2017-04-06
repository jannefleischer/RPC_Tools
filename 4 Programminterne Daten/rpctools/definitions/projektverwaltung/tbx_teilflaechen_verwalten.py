# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from collections import OrderedDict
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import TeilflaechenVerwalten


class TbxFlaechendefinition(Tbx):

    @property
    def teilflaechen_table(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

    def get_teilflaechen(self, nutzungsart=None):
        """
        get pretty names of all teilflaechen of current project along with
        their ids and stored names,
        optionally filtered by nutzungsart

        Parameters
        ----------
        nutzungsart : int, optional
            the nutzungsart of the flaechen

        Returns
        -------
        teilflaechen : dict
            key/value pairs of pretty names as keys and (id, name) as values
        """

        columns = ['id_teilflaeche', 'Flaeche_ha', 'Name',
                   'gemeinde_name', 'Nutzungsart']
        rows = arcpy.da.SearchCursor(self.teilflaechen_table, columns)
        teilflaechen = OrderedDict()

        for flaechen_id, ha, name, gemeinde, nutzungsart_id in rows:
            # ignore other nutzungsart_ids, if filtering is requested
            if nutzungsart is not None and nutzungsart != nutzungsart_id:
                continue
            pretty = ' | '.join([
                'Nr. {}'.format(flaechen_id),
                name,
                str(gemeinde),
                '{} ha'.format(round(ha, 2))
            ])
            teilflaechen[pretty] = flaechen_id, name

        return teilflaechen

    def get_nutzungsart_id(self, flaechen_id):
        """get the nutzungsart of the given flaeche (by id)"""
        where = '"id_teilflaeche" = {}'.format(flaechen_id)
        row = arcpy.SearchCursor(self.teilflaechen_table, where).next()
        return row.Nutzungsart

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

        # Teilfläche
        p = params.teilflaeche = arcpy.Parameter()
        p.name = encode(u'Teilfläche')
        p.displayName = encode(u'Teilfläche')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []

        return params

    def update_teilflaechen_list(self, nutzungsart=None):
        """update the parameter list of teilflaeche (opt. filter nutzungsart)"""
        list_teilflaechen = self.get_teilflaechen(
            nutzungsart=nutzungsart).keys()
        self.par.teilflaeche.filter.list = list_teilflaechen

        if list_teilflaechen:
            flaeche = list_teilflaechen[0]
            self.par.teilflaeche.value = flaeche

class TbxTeilflaecheVerwalten(TbxFlaechendefinition):
    """Toolbox to name Teilflächen"""
    _nutzungsarten = None

    @property
    def label(self):
        return u'Schritt 2: Teilflächen verwalten'

    @property
    def Tool(self):
        return TeilflaechenVerwalten

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
        if params.changed('projectname'):
            params.teilflaeche.value = ''
            self.update_teilflaechen_list()

        flaeche = params.teilflaeche.value
        if flaeche:
            flaechen_id, flaechenname = self.get_teilflaechen()[flaeche]
            if params.changed('projectname', 'teilflaeche'):
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

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""
        self.par.name.value = flaechenname
        nutzungsart_id = self.get_nutzungsart_id(flaechen_id)
        nutzungsarten = self.nutzungsarten
        nutzungsart = nutzungsarten.keys()[
            nutzungsarten.values().index(nutzungsart_id)]
        self.par.nutzungsart.value = nutzungsart

    def _updateMessages(self, params):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        if params.projectname.value != None and params.name.value != None:
            projectname = params.projectname.value
            tablepath_teilflaechen = self.teilflaechen_table
            namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

            params.name.clearMessage()

            for row in namen_cursor:
                if params.name.value == row[0]:
                    params.name.setErrorMessage("Name wurde bereits vergeben.")


if __name__ == '__main__':

    t = TbxTeilflaecheVerwalten()
    params = t.getParameterInfo()
    t.get_teilflaechen()
    t.print_test_parameters()
    t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()