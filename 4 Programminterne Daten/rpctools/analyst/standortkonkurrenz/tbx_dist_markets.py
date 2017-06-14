# -*- coding: utf-8 -*-
import arcpy
import os
import pandas as pd
import json
import numpy as np

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_project_centroid
from rpctools.analyst.standortkonkurrenz.zensus import Zensus
from rpctools.analyst.standortkonkurrenz.routing_distances import DistanceRouting
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point
from rpctools.utils.config import Folders
from rpctools.analyst.standortkonkurrenz.sales import Sales


class DistMarkets(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
    # ToDo: set this in toolbox?
    recalculate = False
    
    def add_outputs(self):
        # Add Layers
        group_layer = ("standortkonkurrenz")
        fc = 'Maerkte'
        layer = 'Umsatzveränderung Planfall'
    
        self.output.add_layer(group_layer, layer, fc, zoom=False)
    
        fc = 'Maerkte'
        layer = 'Kaufkraftbindung'
        betriebstyp_col = 'id_betriebstyp_nullfall'
        df_markets = self.parent_tbx.table_to_dataframe('Maerkte')
        id_nullfall = df_markets['id_betriebstyp_nullfall']
        id_planfall = df_markets['id_betriebstyp_planfall']
        planfall_idx = (id_nullfall != id_planfall) & (id_planfall > 0)
        
        for index, plan_market in df_markets[planfall_idx].iterrows():
            layer_name = '{n} {m} ({i})'.format(n=layer,
                                                m=plan_market['name'],
                                                i=plan_market['id'])
            self.output.add_layer(group_layer, layer, fc,
                                  query='id_markt={}'.format(
                                      plan_market['id']),
                                  name=layer_name, 
                                  zoom=False)
    
    def run(self):
        folders = Folders(self.par)
        tbx = self.parent_tbx
        square_size = self.par.square_size.value * 1000
        zensus = Zensus()

        x, y = get_project_centroid(self.projectname)
        centroid = Point(x, y, epsg=self.parent_tbx.config.epsg)
        
        if self.recalculate or len(tbx.query_table('Siedlungszellen')) == 0:            
            arcpy.AddMessage('Extrahiere Siedlungszellen aus Zensusdaten...')
            zensus_points, bbox = zensus.cutout_area(centroid, square_size)
            arcpy.AddMessage('Schreibe Siedlungszellen in Datenbank...')
            self.zensus_to_db(zensus_points)
            active_project = self.parent_tbx.config.active_project
            zensus.add_kk(zensus_points, active_project)
            # TODO: Update instead of rewrite
            self.zensus_to_db(zensus_points)
        else:
            bbox = zensus.get_bbox(centroid, square_size)
            arcpy.AddMessage('Siedlungszellen bereits vorhanden, '
                             'Neuberechnung wird übersprungen')
        arcpy.AddMessage(u'Berechne Entfernungen der Märkte '
                         u'zu den Siedlungszellen...')
        
        markets = self.parent_tbx.table_to_dataframe('Maerkte')
        epsg = self.parent_tbx.config.epsg

        routing = DistanceRouting()
        destinations = self.get_cells()
        dest_ids = [d.id for d in destinations]
        already_calculated = np.unique(tbx.table_to_dataframe(
            'Beziehungen_Maerkte_Zellen', columns=['id_markt'])['id_markt'])
        for index, market in markets.iterrows():
            arcpy.AddMessage(' - {}'.format(market['name']))
            if self.recalculate or market['id'] not in already_calculated:
                arcpy.AddMessage('   wird berechnet')
                market_id = market['id']
                x, y = market['SHAPE']
                origin = Point(x, y, id=market_id, epsg=epsg)
                distances = routing.get_distances(origin, destinations, bbox)
                self.distances_to_db(market_id, destinations, distances)
            else:
                arcpy.AddMessage(u'   bereits berechnet, wird übersprungen')

        df_markets = tbx.table_to_dataframe('Maerkte')
        df_zensus = self.parent_tbx.table_to_dataframe('Siedlungszellen')
        df_distances = self.parent_tbx.table_to_dataframe(
            'Beziehungen_Maerkte_Zellen', 
            columns=['id_markt', 'id_siedlungszelle', 'distanz'])
        sales = Sales(df_distances, df_markets, df_zensus)
        arcpy.AddMessage('Berechne Nullfall...')
        kk_nullfall = sales.calculate_nullfall()
        arcpy.AddMessage('Berechne Planfall...')
        kk_planfall = sales.calculate_planfall()
        arcpy.AddMessage(u'Berechne Kenngrößen...')
        self.sales_to_db(kk_nullfall, kk_planfall)

    def sales_to_db(self, kk_nullfall, kk_planfall):
        # sum up sales join them on index to dataframe, replace missing entries
        # (e.g. no entries for planned markets in nullfall -> sales = 0)
        sales_nullfall = kk_nullfall.sum(axis=1)
        sales_planfall = kk_planfall.sum(axis=1)
        df_sales_null = pd.DataFrame(sales_nullfall, columns=['umsatz_nullfall'])
        df_sales_plan = pd.DataFrame(sales_planfall, columns=['umsatz_planfall'])
        df_sales = df_sales_null.join(df_sales_plan, how='outer')
        df_sales.fillna(0, inplace=True)
        df_sales['id'] = df_sales.index
        df_sales['umsatz_differenz'] = ((df_sales['umsatz_planfall'] /
                                         df_sales['umsatz_nullfall']) * 100 - 100)
        
        self.parent_tbx.dataframe_to_table('Maerkte', df_sales, pkeys=['id'])
        
        # invert the pivoted tables
        kk_nullfall['id_markt'] = kk_nullfall.index
        kk_planfall['id_markt'] = kk_planfall.index
        df_nullfall = pd.melt(kk_nullfall,
                              value_name='kk_strom_nullfall',
                              id_vars='id_markt')
        df_planfall = pd.melt(kk_planfall,
                              value_name='kk_strom_planfall',
                              id_vars='id_markt')
        
        # join the results to the cell table
        cells = self.parent_tbx.table_to_dataframe('Beziehungen_Maerkte_Zellen')
        del cells['kk_strom_nullfall']
        del cells['kk_strom_planfall']
        cells = cells.merge(df_nullfall,
                            on=['id_siedlungszelle', 'id_markt'], how='left')
        cells = cells.merge(df_planfall,
                            on=['id_siedlungszelle', 'id_markt'], how='left')
        cells.fillna(0, inplace=True)
        cells.sort(['id_markt', 'id_siedlungszelle'], inplace=True)
        
        
        # should be identical, but take both anyway
        sum_null = cells.groupby('id_siedlungszelle',
                                 as_index=False)['kk_strom_nullfall'].sum()
        sum_plan = cells.groupby('id_siedlungszelle',
                                 as_index=False)['kk_strom_planfall'].sum()
        cells = cells.merge(sum_null, on=['id_siedlungszelle'],
                            suffixes=('', '_sum'))
        cells = cells.merge(sum_plan, on=['id_siedlungszelle'], 
                            suffixes=('', '_sum'))
        cells['kk_bindung_nullfall'] = cells['kk_strom_nullfall'] * 100 / cells['kk_strom_nullfall_sum']
        cells['kk_bindung_planfall'] = cells['kk_strom_planfall'] * 100 / cells['kk_strom_planfall_sum']

        # deletion of old entries and inserting is faster than updating
        self.parent_tbx.delete_rows_in_table('Beziehungen_Maerkte_Zellen')
        #column_values = {}
        #for col in cells.columns:
            #column_values[col] = cells[col].values
        arcpy.AddMessage(u'Schreibe Kenngrößen in Datenbank...')
        self.parent_tbx.insert_dataframe_in_table('Beziehungen_Maerkte_Zellen',
                                                  cells)

    def distances_to_db(self, market_id, destinations, distances):
        self.parent_tbx.delete_rows_in_table(
            'Beziehungen_Maerkte_Zellen', where='id_markt={}'.format(market_id))
        column_values = {}
        shapes = []
        ids = []
        for dest in destinations:
            ids.append(dest.id)
            shapes.append(arcpy.Point(dest.x, dest.y))
        column_values['distanz'] = distances
        column_values['id_siedlungszelle'] = ids
        column_values['SHAPE'] = shapes
        column_values['id_markt'] = [market_id] * len(destinations)
        self.parent_tbx.insert_rows_in_table('Beziehungen_Maerkte_Zellen',
                                             column_values)

    def get_cells(self):
        cells = []
        epsg = self.parent_tbx.config.epsg
        df = self.parent_tbx.table_to_dataframe('Siedlungszellen')
        for id, cell in df.iterrows():
            x, y = cell['SHAPE']
            dest = Point(x, y, id=cell['id'], epsg=epsg)
            cells.append(dest)
        return cells

    def zensus_to_db(self, zensus_points):
        df = pd.DataFrame()
        epsg = self.parent_tbx.config.epsg
        shapes = []
        ews = []
        kk_indices = []
        kks = []
        cell_ids = []
        self.parent_tbx.delete_rows_in_table('Siedlungszellen')
        for point in zensus_points:
            if point.ew <= 0:
                continue
            t = point.transform(epsg)
            t.create_geom()
            shapes.append(t.geom)
            ews.append(point.ew)
            kk_indices.append(point.kk_index)
            kks.append(point.kk)
            cell_ids.append(point.id)

        df['id'] = cell_ids
        df['SHAPE'] = shapes
        df['ew'] = ews
        df['kk_index'] = kk_indices
        df['kk'] = kks

        self.parent_tbx.insert_dataframe_in_table('Siedlungszellen', df)


class TbxDistMarkets(Tbx):

    @property
    def label(self):
        return encode(u'Projektwirkung schätzen')

    @property
    def Tool(self):
        return DistMarkets

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
        p.enabled = False

        # set square size
        p = self.add_parameter('square_size')
        p.name = u'sqare_size'.encode('cp1252')
        p.displayName = u'Größe des Bereichs wählen (km)'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.value = 20

        return params

    def _updateParameters(self, params):
        pass

if __name__ == "__main__":
    t = TbxDistMarkets()
    t.getParameterInfo()
    t.set_active_project()
    t.show_outputs()
    t.execute()

    print 'done'