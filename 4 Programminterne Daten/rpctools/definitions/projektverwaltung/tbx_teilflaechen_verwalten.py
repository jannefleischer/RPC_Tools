# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from collections import OrderedDict
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import (
    TeilflaechenVerwalten)
from rpctools.utils.constants import Nutzungsart


class Teilflaeche(OrderedDict):
    """Teilfläche with some attributes"""
    def __init__(self, flaechen_id, name, ha, ags):
        """
        Parameters
        ----------
        flaechen_id : int
        name : str
        ha : float
        ags : str
        """
        super(Teilflaeche, self).__init__()
        self.flaechen_id = flaechen_id
        self.name = name
        self.ha = ha
        self.ags = ags
        # set the values as keys of the dict
        self.update(((v, k) for (k, v) in self.__dict__.iteritems()
                     if not k.startswith('_')))

    @property
    def where_clause(self):
        """"""
        where = '"id_teilflaeche" = {}'.format(self.flaechen_id)
        return where


class TbxFlaechendefinition(Tbx):
    # filters the available teilflaechen by the id of the nutzungsart
    # (None for access to all teilflaechen)
    _nutzungsart = None
    # the available teilflaechen are stored here
    _teilflaechen = None
    _nutzungsarten = None
    _recently_opened = True

    @property
    def teilflaechen_table(self):
        return self.folders.get_table('Teilflaechen_Plangebiet')

    def get_teilflaeche(self, name):
        # type: (str) -> Teilflaeche
        """
        return the teilflaeche

        Parameters
        ----------
        name : str

        Returns
        -------
        teilflaeche : Teilflaeche
        """
        if not self.teilflaechen or name not in self.teilflaechen:
            return None
        teilflaeche = self.teilflaechen[name]
        return teilflaeche

    @property
    def teilflaechen(self):
        # type: () -> List[Teilflaeche]
        """dict of key/value pairs of pretty names of teilflaechen as keys and
        (id, name, ha, ags) as values"""
        return self._teilflaechen
    
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
            del rows
        return self._nutzungsarten

    def _get_teilflaechen(self, nutzungsart=None):
        """
        get pretty names of all teilflaechen of current project along with
        their ids, stored names, hectars and ags,
        optionally filtered by nutzungsart

        Parameters
        ----------
        nutzungsart : int, optional
            the nutzungsart of the flaechen

        Returns
        -------
        teilflaechen : dict
            key/value pairs of pretty names as keys and (id, name, ha, ags) as
            values
        """

        columns = ['id_teilflaeche', 'Flaeche_ha', 'Name',
                   'gemeinde_name', 'Nutzungsart', 'ags_bkg']
        rows = self.query_table('Teilflaechen_Plangebiet', columns)
        teilflaechen = OrderedDict()
        inverted_nutzungsarten = {v: k for k, v in
                                  self.nutzungsarten.iteritems()}

        for flaechen_id, ha, name, gemeinde, nutzungsart_id, ags in rows:
            # ignore other nutzungsart_ids, if filtering is requested
            if nutzungsart is not None and nutzungsart != nutzungsart_id:
                continue
            n = inverted_nutzungsarten[nutzungsart_id]
            pretty = ' | '.join([
                'Nr. {}'.format(flaechen_id),
                name,
                str(gemeinde),
                '{} ha'.format(round(ha, 2)),
                'Nutzungsart: {}'.format(n)
            ])
            teilflaechen[pretty] = Teilflaeche(flaechen_id, name, ha, ags)

        return teilflaechen

    def get_nutzungsart_id(self, flaechen_id):
        """get the nutzungsart of the given flaeche (by id)"""
        row = self.query_table(
            'Teilflaechen_Plangebiet', ['Nutzungsart'],
            where = '"id_teilflaeche" = {}'.format(flaechen_id))[0]
        return row[0]

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        p = self.add_parameter('projectname')
        p.name = u'Projekt'
        p.displayName = u'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        projects = self.folders.get_projects()
        p.filter.list = projects
        p.value = '' if len(projects) == 0 else p.filter.list[0]

        # Teilfläche
        p = self.add_parameter('teilflaeche')
        p.name = encode(u'Teilfläche')
        p.displayName = encode(u'Teilfläche')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []

        self.update_teilflaechen(self._nutzungsart)

        self.add_temporary_management('FGDB_Definition_Projekt.gdb')

        return params
    
    def commit_tfl_changes(self):
        """Commit Teilflaechen Changes"""
        
    def _open(self, params):
        self.update_teilflaechen(self._nutzungsart)
        self._recently_opened = True

    def _updateParameters(self, params):
        if params.changed('projectname'):
            self._open(params)

        if params.changed('teilflaeche') and self.par.teilflaeche.filter.list:
            # don't commit after toolbox just opened (else the defaults overwrite
            # the actual settings)
            if not self._recently_opened:
                self.commit_tfl_changes()
            tfl = self.get_teilflaeche(params.teilflaeche.value)
            params._current_tfl = tfl
            self.update_teilflaechen_inputs(tfl.flaechen_id,
                                            tfl.name)
        self._recently_opened = False
        return params

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""


    def update_teilflaechen(self, nutzungsart=None):
        """update the parameter list of teilflaeche (opt. filter nutzungsart)"""
        # currently selected flaeche
        idx = self.par.selected_index('teilflaeche')
        
        if not self.par.projectname.value:
            list_teilflaechen = []
        else:
            self._teilflaechen = self._get_teilflaechen(nutzungsart=nutzungsart)
            list_teilflaechen = self.teilflaechen.keys()
        self.par.teilflaeche.filter.list = list_teilflaechen
        
        if not list_teilflaechen:
            flaeche = ''
            
        # a flaeche was selected and is in list, select it again
        elif idx >= 0:
            flaeche = self.par.teilflaeche.filter.list[idx]
        
        # flaeche not in list -> select first one
        else: 
            if list_teilflaechen:
                flaeche = list_teilflaechen[0]
                tfl = self.get_teilflaeche(flaeche)
                self.par._current_tfl = tfl
                self.par.teilflaeche.enabled = True
            else:
                flaeche = u'keine entsprechenden Flächen vorhanden'
                for param in self.par:
                    param.enabled = False
            
        self.par.teilflaeche.value = flaeche

class TbxTeilflaecheVerwalten(TbxFlaechendefinition):
    """Toolbox to name Teilflächen and define their 'nutzungen'"""

    @property
    def label(self):
        return u'Schritt 2: Teilflächen verwalten'

    @property
    def Tool(self):
        return TeilflaechenVerwalten

    def _getParameterInfo(self):
        params = super(TbxTeilflaecheVerwalten, self)._getParameterInfo()
        # Name
        p = self.add_parameter('name')
        p.name = u'Name'
        p.displayName = u'Name'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'

        # Nutzungsart
        p = self.add_parameter('nutzungsart')
        p.name = encode(u'Nutzungsart')
        p.displayName = encode(u'Nutzungsart')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = self.nutzungsarten.keys()

        return params

    def _updateParameters(self, params):
        params = super(TbxTeilflaecheVerwalten, self)._updateParameters(params)

        flaeche = params.teilflaeche.value
        tfl = self.get_teilflaeche(params.teilflaeche.value)
        if tfl:
            where_tfl = 'id_teilflaeche={}'.format(tfl.flaechen_id)

            if params.changed('name'):
                self.update_table('Teilflaechen_Plangebiet',
                                  {'Name': params.name.value},
                                  where=where_tfl)
                self.update_teilflaechen()

            if params.changed('nutzungsart'):
                nutzungsart_id = self.nutzungsarten[params.nutzungsart.value]
                # set nutzungsart in gdb and clear sums
                self.update_table('Teilflaechen_Plangebiet',
                                  {'Nutzungsart': nutzungsart_id,
                                   'WE_gesamt': 0,
                                   'AP_gesamt': 0,
                                   'VF_gesamt': 0},
                                  where=where_tfl)

                # delete corresponding rows wohnen/gewerbe/einzelhandel
                if nutzungsart_id != Nutzungsart.WOHNEN:
                    table = 'Wohnen_WE_in_Gebaeudetypen'
                    self.delete_rows_in_table(
                        table, pkey=dict(IDTeilflaeche=tfl.flaechen_id,))
                if nutzungsart_id != Nutzungsart.GEWERBE:
                    tables = ['Gewerbe_Anteile', 'Gewerbe_Arbeitsplaetze']
                    for table in tables:
                        self.delete_rows_in_table(
                            table, pkey=dict(IDTeilflaeche=tfl.flaechen_id))
                if nutzungsart_id != Nutzungsart.EINZELHANDEL:
                    table = 'Einzelhandel_Verkaufsflaechen'
                    self.delete_rows_in_table(
                        table, pkey=dict(IDTeilflaeche=tfl.flaechen_id,))
                
                self.update_teilflaechen()


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
    t.update_table('Teilflaechen_Plangebiet', {'Nutzungsart': 1})
    print(t.query_table('Teilflaechen_Plangebiet', ['Nutzungsart']))
    t._commit_temporaries()
    t._get_teilflaechen()
    t.print_test_parameters()
    t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()