# -*- coding: utf-8 -*-
import arcpy
import pandas as pd
import numpy as np

from rpctools.utils.params import Tbx, Tool
from rpctools.analyst.standortkonkurrenz.zensus import Zensus, ZensusCell
from rpctools.utils.spatial_lib import Point, extent_to_bbox, \
     get_extent, features_to_raster
from rpctools.utils.encoding import encode




class SetBoundaryConditions(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def add_outputs(self):
        self.output.add_layer('standortkonkurrenz',
                              'Maerkte_Puffer',
                              featureclass="Maerkte_Puffer",
                              template_folder="Standortkonkurrenz")
        self.output.add_layer('standortkonkurrenz',
                              'Siedlungszellen_Puffer',
                              featureclass="Siedlungszellen_Puffer",
                              template_folder="Standortkonkurrenz")
        pass

    def run(self):
        zensus = Zensus()
        settlement_radius = self.par.radius_settlement.value
        markets_radius = self.par.radius_markets.value

        community_extent = get_extent('Zentren', self._workspace,
                                      where='Auswahl<>{}'.format(0))
        bbox =  extent_to_bbox(self, community_extent,
                               epsg=self.parent_tbx.config.epsg,
                               boundary_size=settlement_radius)
        self.calculate_zensus(bbox,
                              settlement_buffer=settlement_radius,
                              markets_buffer=markets_radius)
        pass

    def calculate_zensus(self, bbox, settlement_buffer, markets_buffer):
        '''extract zensus points (incl. points for planned areas)
        and write them to the database'''
        zensus = Zensus()


        arcpy.AddMessage('Extrahiere Siedlungszellen aus Zensusdaten...')
        zensus_points, max_id = zensus.cutout_area(bbox,
                                                   epsg=self.parent_tbx.config.epsg,
                                                   settlement_buffer=settlement_buffer,
                                                   markets_buffer=markets_buffer)
        tfl_points = self.get_tfl_points(max_id + 1)
        # settlements = zensus centroids + teilflaeche centroids
        sz_points = zensus_points + tfl_points
        arcpy.AddMessage('Schreibe Siedlungszellen in Datenbank...')
        self.zensus_to_db(sz_points)
        project = self.parent_tbx.folders.projectname
        zensus.add_kk(sz_points, project)
        # TODO: Update instead of rewrite
        self.zensus_to_db(sz_points)


    def get_tfl_points(self, start_id):
        '''get the centroids of the planned areas as zensus points, start_id
        is the id the first point gets (further areas ascending)'''
        df_tfl = self.parent_tbx.table_to_dataframe(
            'Teilflaechen_Plangebiet', workspace='FGDB_Definition_Projekt.gdb')
        points = []
        i = 0
        for index, tfl in df_tfl.iterrows():
            point = ZensusCell(tfl['INSIDE_X'], tfl['INSIDE_Y'],
                               epsg=self.parent_tbx.config.epsg, ew=tfl['ew'],
                               id=start_id+i,
                               tfl_id=tfl['id_teilflaeche'])
            points.append(point)
            i += 1
        return points

    def zensus_to_db(self, zensus_points):
        df = pd.DataFrame()
        shapes = []
        ews = []
        kk_indices = []
        kks = []
        cell_ids = []
        tfl_ids = []
        self.parent_tbx.delete_rows_in_table('Siedlungszellen')
        for point in zensus_points:
            # ignore zensus points with no inhabitants
            # (but keep the planned ones)
            if point.ew <= 0 and point.tfl_id < 0:
                continue
            point.create_geom()
            shapes.append(point.geom)
            ews.append(point.ew)
            kk_indices.append(point.kk_index)
            kks.append(point.kk)
            cell_ids.append(point.id)
            tfl_ids.append(point.tfl_id)

        df['id'] = cell_ids
        df['SHAPE'] = shapes
        df['ew'] = ews
        df['kk_index'] = kk_indices
        df['kk'] = kks
        df['id_teilflaeche'] = tfl_ids

        self.parent_tbx.insert_dataframe_in_table('Siedlungszellen', df)

class TbxSetBoundaryConditions(Tbx):

    @property
    def label(self):
        return encode(u'Randbedingungen setzen')

    @property
    def Tool(self):
        return SetBoundaryConditions

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.value = self.config.active_project

        # settlement radius
        p = self.add_parameter('radius_settlement')
        p.name = u'radius_settlement'
        p.displayName = encode(u'Pufferzone für Siedlungszellen um gewählte'
                               u'Gemeinden festlegen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 5000]
        p.value = 3000
        p.enabled = False

        # markets radius
        p = self.add_parameter('radius_markets')
        p.name = u'radius_markets'
        p.displayName = encode(u'Pufferzone für Märkte um gewählte'
                               u'Gemeinden festlegen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 10000]
        p.value = 6000
        p.enabled = False

        return params

    def _updateParameters(self, params):
        pass


if __name__ == "__main__":
    t = TbxSetBoundaryConditions()
    t.getParameterInfo()
    t.set_active_project()
    #t.show_outputs()
    t.execute()

    print 'done'