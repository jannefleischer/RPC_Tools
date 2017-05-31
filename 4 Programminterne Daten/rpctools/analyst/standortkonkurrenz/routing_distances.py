from rpctools.utils.config import Folders
from rpctools.utils.spatial_lib import clip_raster
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point

import arcpy
import os
import shutil
import requests
import sys
import time


class RasterManagement(object):
    def __init__(self):
        self.raster_values = self.raster_origin = self.srid = None
        self.cellWidth = self.cellHeight = None
        # map point via id to a raster cell
        self.point_raster_map = {}
        
    def load(self, raster_file): 
        desc = arcpy.Describe(raster_file)
        e = desc.Extent
        self.srid = desc.spatialReference.factoryCode
        self.raster_origin = Point(e.XMin, e.YMax, epsg=self.srid)
        self.cellWidth = float(arcpy.GetRasterProperties_management(
            raster_file, 'CELLSIZEX').getOutput(0).replace(',', '.'))
        self.cellHeight = float(arcpy.GetRasterProperties_management(
            raster_file, 'CELLSIZEY').getOutput(0).replace(',', '.'))
        self.raster_values = arcpy.RasterToNumPyArray(raster_file)
        
    def register_points(self, points):
        if self.raster_values is None:
            raise Exception('A raster-file has to be loaded first!')
        for point in points:
            t = point.transform(self.srid) if point.epsg != self.srid \
                else point
            mapped_x = int(abs(t.x - self.raster_origin.x) / self.cellWidth)
            mapped_y = int(abs(t.y - self.raster_origin.y) / self.cellHeight)
            self.point_raster_map[point.id] = (mapped_x, mapped_y)
            
    def get_value(self, point):
        mapped_x, mapped_y = self.point_raster_map[point.id]
        return self.raster_values[mapped_y][mapped_x]

class DistanceRouting(object):
    URL = r'https://projektcheck.ggr-planung.de/otp/surfaces'
    ROUTER = 'deutschland'
    RASTER_FILE_PATTERN = 'raster_{id}.tif'
    
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
        
    def get_distances(self, origin, destinations, bbox=None):
        dist_raster = self._request_dist_raster(origin)
        if bbox is not None:
            fn, ext = os.path.splitext(dist_raster)
            clipped_raster = fn + '_clipped' + ext
            clip_raster(dist_raster, clipped_raster, bbox)
            dist_raster = clipped_raster
        raster = RasterManagement()
        raster.load(dist_raster)
        raster.register_points(destinations)
        start = time.time()
        distances = []
        for dest in destinations:
            distances.append(raster.get_value(dest))
        print('mapping {}s'.format(time.time() - start))
        return distances
        
    def _request_dist_raster(self, origin):
        t = origin.transform(self.epsg) if origin.epsg != self.epsg \
            else origin
        params = {
            'batch': True,
            'routerId': self.ROUTER,
            'fromPlace': "{},{}".format(t.y, t.x),
            'toPlace': "{},{}".format(t.y, t.x),
            'mode': 'CAR',
            'maxWalkDistance': 5000,
            'maxPreTransitTime': 1200,
            'cutoffMinutes': 20
        }
        start = time.time()
        r = requests.post(self.URL, params=params)
        print('request post {}s'.format(time.time() - start))
        id = r.json()['id']
        #url = '{url}/{id}/indicator?targets=Siedlungszellen_FeaturesToJS&detail=true'.format(url=self.URL, id=id)
        url = '{url}/{id}/raster'.format(url=self.URL, id=id)

        params = {   
            #'width': 5000,
            #'height': 3000,
            'resolution': 300, 
            'crs': 'EPSG:{}'.format('31467'),
        } 
        start = time.time()
        r = requests.get(url, stream=True, params=params)
        print('request get {}s'.format(time.time() - start))
        out_raster = os.path.join(
            self.tmp_folder,
            self.RASTER_FILE_PATTERN.format(id=origin.id))
        if r.status_code == 200:
            with open(out_raster, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        return out_raster
    