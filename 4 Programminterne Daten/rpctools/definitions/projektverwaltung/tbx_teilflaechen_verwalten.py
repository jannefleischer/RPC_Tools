# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from collections import OrderedDict
import arcpy
import numpy as np

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import (
    TeilflaechenVerwalten)
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.config import Config

config = Config()


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
        p = self.add_parameter('area')
        p.name = encode(u'Teilfläche')
        p.displayName = encode(u'Teilfläche')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []
        
        self.df_types_of_use = self.table_to_dataframe(
            'Nutzungsarten', workspace='FGDB_Definition_Projekt_Tool.gdb',
            is_base_table=True
        )

        return params

    def get_areas(self, nutzungsart=None):
        where = 'Nutzungsart = {}'.format(nutzungsart) if nutzungsart else None
        df_areas = self.table_to_dataframe('Teilflaechen_Plangebiet',
                                           where=where)
        return df_areas
        
    def _open(self, params):
        self.df_areas = self.get_areas(self._nutzungsart)
        pretty_names = [self.get_pretty_area_name(area) for
                        idx, area in self.df_areas.iterrows()]
        self.df_areas['pretty'] = pretty_names
        self.update_area_list()
        self.set_selected_area()
    
    def get_selected_area(self):
        '''return the currently selected area as a Series and 
        it's index in the list of areas
        '''
        area_idx = self.df_areas['pretty'] == self.par.area.value
        idx = np.where(area_idx==True)[0][0]
        area = self.df_areas.iloc[idx]
        return area, idx
        
    def set_selected_area(self):
        '''set the inputs for the currently selected area '''
        raise NotImplementedError

    def get_pretty_area_name(self, area):
        '''assemble a meaningful name for the area incl. name and additional
        informations'''
        idx = self.df_types_of_use['id'] == area['Nutzungsart']
        type_of_use = self.df_types_of_use['nutzungsart'][idx].values[0]
        pretty = u'"{name}" ({id}) | {gemeinde} | {ha} ha | {tou}'.format(
            id=area['id_teilflaeche'],
            name=area['Name'],
            ha=round(area['Flaeche_ha'], 2), 
            gemeinde=area['gemeinde_name'], 
            tou=type_of_use
        )
        return pretty
    
    def update_area_list(self, idx=None):
        """update the list of areas and select the area with index if given"""
        if idx is None:
            idx = self.par.area.filter.list.index(
                self.par.area.value) if self.par.area.value else 0
        pretty = self.df_areas['pretty'].values.tolist()
        self.par.area.filter.list = pretty
        self.par.area.value = pretty[idx]

    def _updateParameters(self, params):
        if params.changed('projectname'):
            self._open(params)

        elif params.changed('area'):
            self.set_selected_area()

        return params
    
    def validate_inputs(self):
        df_areas = self.get_areas()
        if len(df_areas) == 0:
            msg = (u'Es sind keine Flächen definiert!')
            return False, msg
        return True, ''

    def _updateMessages(self, params):
        valid, msg = self.validate_inputs()
        if not valid:
            self.par.projectname.setErrorMessage(msg)

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
        p = self.add_parameter('type_of_use')
        p.name = encode(u'Nutzungsart')
        p.displayName = encode(u'Nutzungsart')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = self.df_types_of_use['nutzungsart'].values.tolist()

        return params

    def _updateParameters(self, params):
        params = super(TbxTeilflaecheVerwalten, self)._updateParameters(params)

        area, idx = self.get_selected_area()

        #if params.changed('area') and self.par.area.filter.list:
            #selected, idx = self.get_selected_area()
            #pretty = self.get_pretty_area_name(selected)
            #self.df_areas.loc[idx, 'pretty'] = pretty
            #self.update_area_list()

        if params.changed('name'):
            self.df_areas.loc[idx, 'Name'] = self.par.name.value

        elif params.changed('type_of_use'):
            tou_idx = (self.df_types_of_use['nutzungsart'] ==
                       self.par.type_of_use.value)
            tou_id = self.df_types_of_use[tou_idx]['id'].values[0]
            self.df_areas.loc[idx, 'Nutzungsart'] = tou_id
            
            # set fixed duration (as defined in config)
            # except 'Einzelhandel' opens instantly
            duration = (1 if tou_id == Nutzungsart.EINZELHANDEL
                        else config.aufsiedlungsdauer)
            self.df_areas.loc[idx, 'Aufsiedlungsdauer'] = duration
        
        if params.changed('name') or params.changed('type_of_use'):
            # get area again because Series is just a copy of the row of Dataframe
            # which was changed
            area = self.df_areas.loc[idx]
            # something changed -> update pretty representation of selected area 
            # and update list as well (to show new pretty repr.)
            pretty = self.get_pretty_area_name(area)
            self.df_areas.loc[idx, 'pretty'] = pretty
            self.update_area_list()

        return params

    def set_selected_area(self):
        '''set the inputs for the currently selected area '''
        area, i = self.get_selected_area()
        tou_idx = self.df_types_of_use['id'] == area['Nutzungsart']
        type_of_use = self.df_types_of_use.loc[tou_idx]['nutzungsart'].values[0]
        self.par.name.value = area['Name']
        self.par.type_of_use.value = type_of_use

    def _updateMessages(self, params):
        valid, msg = self.validate_inputs()
        if not valid:
            self.par.projectname.setErrorMessage(msg)

if __name__ == '__main__':

    t = TbxTeilflaecheVerwalten()
    t.getParameterInfo()
    t.open()
    t._updateParameters(t.par)
    t.execute()