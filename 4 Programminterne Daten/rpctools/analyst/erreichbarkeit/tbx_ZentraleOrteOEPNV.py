# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import pandas as pd

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_project_centroid, points_within, Point
from rpctools.analyst.erreichbarkeit.bahn_query import BahnQuery

import datetime

def next_monday():
    today = datetime.date.today()
    nextmonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    return nextmonday

class ZentraleOrte(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Erreichbarkeit.gdb'
    
    def add_outputs(self):
        
        group_layer = ("erreichbarkeit")
        fc = 'Haltestellen'
        layer_nullfall = 'Haltestellen'

        self.output.add_layer(group_layer, layer_nullfall, fc, zoom=False)
    
    def run(self):
        self.query = BahnQuery(date=next_monday())
        arcpy.AddMessage('Berechne die zentralen Orte und Haltestellen '
                         'in der Umgebung...')
        self.write_centers_stops()
        arcpy.AddMessage('Ermittle die Anzahl der Abfahrten je Haltestelle...')
        self.update_connections(projectarea_only=True)
        
    def write_centers_stops(self):
        '''get centers in radius around project centroid, write their closest
        stops and the stops near the project to the db
        '''
        # truncate tables, will be filled in progress
        self.parent_tbx.delete_rows_in_table('Zentrale_Orte')
        self.parent_tbx.delete_rows_in_table('Haltestellen')        
        
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
        oz_points, oz_within = points_within(centroid, oz_points, radius=70000)
        mz_points, mz_within = points_within(centroid, mz_points, radius=30000)
        df_oz_within = df_oz[oz_within]
        df_mz_within = df_mz[mz_within]
        
        def get_closest_stops(points):
            stops = []
            for point in points:
                t_p = Point(point[0], point[1],
                            epsg=self.parent_tbx.config.epsg)
                t_p.transform(4326)
                closest = self.query.stops_near(t_p, n=1)[0]
                stops.append(closest)
            return stops
            
        oz_stops = get_closest_stops(oz_points)
        mz_stops = get_closest_stops(mz_points)
        
        df_oz_within['id_haltestelle'] = [s.id for s in oz_stops]
        df_mz_within['id_haltestelle'] = [s.id for s in mz_stops]
                
        df_within = pd.concat([df_oz_within, df_mz_within])
        df_within['name'] = df_within['GEN']
        df_within['id_zentraler_ort'] = df_within['OBJECTID']
        df_within['distanz'] = 0
        
        self.parent_tbx.insert_dataframe_in_table('Zentrale_Orte', df_within)
        
        p_centroid = Point(centroid[0], centroid[1],
                           epsg=self.parent_tbx.config.epsg)
        p_centroid.transform(4326)
        tfl_stops = self.query.stops_near(p_centroid, n=10)
        
        self._stops_to_db(oz_stops)
        self._stops_to_db(mz_stops)
        self._stops_to_db(tfl_stops, is_project_stop=1)
        
    def update_connections(self, projectarea_only=False):
        '''update the db-column 'abfahrten' of the stops with the number
        of departures
        '''
        where = 'flaechenzugehoerig = 1' if projectarea_only else None
        df_stops = self.parent_tbx.table_to_dataframe('Haltestellen',
                                                      where=where)
        ids = df_stops['id'].values
        n_departures = self.query.n_departures(ids)
        df_stops['abfahrten'] = n_departures
        self.parent_tbx.dataframe_to_table('Haltestellen', df_stops, ['id'])
        
    def _stops_to_db(self, stops, is_project_stop=0):
        '''(warning: changes projection of point!)'''
        table = self.folders.get_table('Haltestellen')
        ids = []
        names = []
        shapes = []
        
        for stop in stops:
            stop.transform(self.parent_tbx.config.epsg)
            shapes.append(arcpy.Point(stop.x, stop.y))
            ids.append(stop.id)
            names.append(stop.name)
            
        column_values = {
            'SHAPE': shapes,
            'id': ids,
            'name': names,
            'flaechenzugehoerig': [is_project_stop] * len(stops), 
            'abfahrten': [0] * len(stops)
        }
        self.parent_tbx.insert_rows_in_table('Haltestellen',
                                             column_values=column_values)


class TbxZentraleOrteOEPNV(Tbx):

    @property
    def label(self):
        return encode(u'Haltestellen und Zentrale Orte '
                      u'in der Umgebung ermitteln')

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