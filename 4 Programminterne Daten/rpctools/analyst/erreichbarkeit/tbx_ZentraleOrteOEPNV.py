# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import pandas as pd

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_project_centroid, points_within


class ZentraleOrte(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Erreichbarkeit.gdb'
    
    def add_outputs(self):
        pass
    
    def run(self):
        centroid = get_project_centroid(self.par.projectname.value)
        df_central = self.parent_tbx.table_to_dataframe(
            'Zentrale_Orte_Neu', 
            workspace='FGDB_Basisdaten_deutschland.gdb',
            columns=['SHAPE', 'OBJECTID', 'GEN', 'OZ'], 
            is_base_table=True
        )
        df_oz = df_central[df_central['OZ'] == 1]
        df_mz = df_central[df_central['OZ'] == 0]
        
        oz_points = df_oz['SHAPE'].values
        mz_points = df_mz['SHAPE'].values
        points, oz_within = points_within(centroid, oz_points, radius=70000)
        points, mz_within = points_within(centroid, mz_points, radius=30000)
        
        df_within = pd.concat([df_oz[oz_within], df_mz[mz_within]])
        df_within['name'] = df_within['GEN']
        df_within['id_zentraler_ort'] = df_within['OBJECTID']
        df_within['distanz'] = 0
            
        self.parent_tbx.delete_rows_in_table('Zentrale_Orte')
        self.parent_tbx.insert_dataframe_in_table('Zentrale_Orte', df_within)        
        
        

class TbxZentraleOrteOEPNV(Tbx):

    @property
    def label(self):
        return encode(u'Zentrale Orte ÖPNV')

    @property
    def Tool(self):
        return ZentraleOrte

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

        return params

if __name__ == "__main__":
    t = TbxZentraleOrteOEPNV()
    t.getParameterInfo()
    t.set_active_project()
    t.execute()