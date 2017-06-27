# -*- coding: utf-8 -*-
import os
import arcpy
import webbrowser

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.analyst.erreichbarkeit.tbx_ZentraleOrteOEPNV import next_monday
from rpctools.analyst.erreichbarkeit.bahn_query import BahnQuery


class Fahrplaene(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Erreichbarkeit.gdb'
    
    def add_outputs(self):
        pass
    
    def run(self):
        query = BahnQuery(next_monday())
        idx = self.par.selected_index('stops')
        id = self.parent_tbx.df_stops['id'].values[idx]
        url = query.get_timetable_url(id)
        webbrowser.open(url, new=0, autoraise=True)

class TbxHaltestellen(Tbx):

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt auswählen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.value = self.config.active_project

        param = self.add_parameter('stops')
        param.name = encode(u'stops')
        param.displayName = encode(u'Name der Haltestelle')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
        
        self.df_stops = []

        return params
    
    def _open(self, params):
        
        self.df_stops = self.table_to_dataframe(
            'Haltestellen', where='flaechenzugehoerig=1')
        
        names = self.df_stops['name'].values
        param = params.stops
        param.filter.list = names.tolist()
        param.value = names[0]

class TbxFahrplaene(TbxHaltestellen):

    @property
    def label(self):
        return encode(u'Fahrpläne anzeigen')

    @property
    def Tool(self):
        return Fahrplaene
    
if __name__ == "__main__":
    t = TbxFahrplaene()
    t.getParameterInfo()
    t.set_active_project()
    t._open(t.par)
    t.execute()
