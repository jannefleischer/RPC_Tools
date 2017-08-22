from rpctools.utils.config import Folders, Config
from rpctools.utils.params import DummyTbx
from rpctools.utils.spatial_lib import clip_raster, Point, points_within, \
     get_extent

import os
import shutil
import sys
import arcpy
import numpy as np
import time


class ZensusCell(Point):
    def __init__(self, x, y, epsg=4326, ew=0, id=None, kk_index=None,
                 kk=None, tfl_id=-1):
        super(ZensusCell, self).__init__(x, y, id=id, epsg=epsg)
        self.ew = ew
        self.kk_index = kk_index
        self.kk = kk
        # -1 if point is not correlated to a planned area
        self.tfl_id = tfl_id


class Zensus(object):
    _workspace = "FGDB_Standortkonkurrenz_Supermaerkte.gdb"
    _table = "Zentren"

    def __init__(self):
        self.folders = Folders()
        self.epsg = 4326
        self.tmp_folder = os.path.join(self.folders.TEMPORARY_GDB_PATH,
                                       'Zensus')
        if os.path.exists(self.tmp_folder):
            arcpy.Delete_management(self.tmp_folder)
        try:
            os.mkdir(self.tmp_folder)
        except:
            pass

    def cutout_area(self, bbox, epsg, settlement_buffer=3000, markets_buffer=6000):
        """
        return the centroids of the zensus cells as points inside the
        selected communities
        """
        tbx = DummyTbx()
        tbx.set_active_project()
        community_path =  tbx.folders.get_table(self._table,
                                                 workspace=self._workspace)
        zensus_points = []
        zensus_raster = self.folders.ZENSUS_RASTER_FILE
        # temporary paths
        out_raster = os.path.join(self.tmp_folder, 'zensus_cutout.tif')
        raster_points = os.path.join(self.tmp_folder,
                               'zensus_cutout.shp')
        raster_points_projected = os.path.join(self.tmp_folder,
                                         'zensus_cutout_projected.shp')
        raster_points_clipped = os.path.join(self.tmp_folder,
                                       'zensus_cutout_clipped.shp')
        out_raster = os.path.join(self.tmp_folder, 'zensus_cutout.tif')
        ws_tmp = tbx.folders.get_db(workspace=self._workspace)
        selected_communities = "Ausgewaehlte_Gemeinden"
        settlement_cells_buffer_feature = "Siedlungszellen_Puffer"
        markets_buffer_feature = "Maerkte_Puffer"
        selected_communities_path =  os.path.join(ws_tmp, selected_communities)
        settlement_cells_buffer_path =  os.path.join(ws_tmp, settlement_cells_buffer_feature)
        markets_buffer_path =  os.path.join(ws_tmp, markets_buffer_feature)
        # delete old tables
        arcpy.Delete_management(selected_communities_path)
        arcpy.Delete_management(settlement_cells_buffer_path)
        arcpy.Delete_management(markets_buffer_path)
        # clip minimum to rectangle shape that still contains all communities
        srid = clip_raster(zensus_raster, out_raster, bbox)
        # get raster points
        arcpy.RasterToPoint_conversion(out_raster, raster_points)
        start = time.time()
        with arcpy.da.UpdateCursor(raster_points, "GRID_CODE") as cursor:
            for row in cursor:
                if row[0] <= 0:
                    cursor.deleteRow()
        print(time.time() - start)
        # project raster points to gauss krueger
        out_cs = arcpy.SpatialReference(epsg)
        arcpy.Project_management(raster_points, raster_points_projected,
                                 out_cs)
        # make feature class for selected communities
        arcpy.FeatureClassToFeatureClass_conversion(
            community_path, ws_tmp, selected_communities,
            where_clause='Auswahl<>{}'.format(0))
        # create buffer area
        arcpy.Buffer_analysis(in_features=selected_communities_path,
                              out_feature_class=settlement_cells_buffer_path,
                              buffer_distance_or_field=settlement_buffer,
                              dissolve_option='ALL')
        arcpy.Buffer_analysis(in_features=selected_communities_path,
                              out_feature_class=markets_buffer_path,
                              buffer_distance_or_field=markets_buffer,
                              dissolve_option='ALL')
        # clip raster points to selected communities
        arcpy.Clip_analysis(raster_points_projected,
                            settlement_cells_buffer_path,
                            raster_points_clipped)
        # create list with zensus points for return
        rows = arcpy.da.SearchCursor(raster_points_clipped,
                                     ['SHAPE@XY', 'GRID_CODE'])
        zensus_points = []
        index = 0
        for ((x, y), value) in rows:
            if value <= 0:
                continue
            p = ZensusCell(x, y, id=index, epsg=srid, ew=value)
            zensus_points.append(p)
            index += 1
        # delete temporary files
        def del_tmp():
            for fn in [raster_points, raster_points_projected, out_raster,
                       raster_points_clipped]:
                arcpy.Delete_management(fn)
        del_tmp()
        return zensus_points, len(zensus_points)

    def add_kk(self, zensus_points, project):
        folders = Folders()
        default_table = folders.get_base_table(
            table='Grundeinstellungen',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb'
        )
        cursor = arcpy.da.SearchCursor(
            default_table, ['Wert'],
            where_clause="Info = 'KK je Einwohner default'")
        default_kk_index = cursor.next()[0]
        del(cursor)
        base_kk = 2280
        tmp_table = os.path.join(arcpy.env.scratchGDB, 'tmp_kk_join')
        kk_table = folders.get_base_table(
            workspace='FGDB_Basisdaten_deutschland.gdb',
            table='KK2015')
        zensus_table = folders.get_table(
            'Siedlungszellen',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte.gdb',
            project=project)

        if arcpy.Exists(tmp_table):
            arcpy.Delete_management(tmp_table)
        arcpy.SpatialJoin_analysis(zensus_table, kk_table, tmp_table,
                                   match_option='WITHIN')

        cursor = arcpy.da.SearchCursor(tmp_table, ['id', 'kk_ew_index'])
        kk_indices = {}
        for id_cell, kk_index in cursor:
            kk_indices[id_cell] = kk_index
        for zensus_cell in zensus_points:
            if not kk_indices.has_key(zensus_cell.id):
                continue
            kk_index = default_kk_index  #kk_indices[zensus_cell.id]
            if kk_index is None:
                kk_index = default_kk_index
            zensus_cell.kk_index = kk_index
            zensus_cell.kk = zensus_cell.ew * base_kk * kk_index / 100

        arcpy.Delete_management(tmp_table)