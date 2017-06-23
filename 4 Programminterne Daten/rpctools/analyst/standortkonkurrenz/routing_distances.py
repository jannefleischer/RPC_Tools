from rpctools.utils.config import Folders
from rpctools.utils.spatial_lib import clip_raster
from rpctools.utils.spatial_lib import Point

import arcpy
import os
import shutil
import requests
import sys
import time
import numpy as np
from scipy.ndimage import filters

def filter_raster(array, threshold=120):
    y_dim, x_dim = np.shape(array)
    new_array = np.copy(array)
    for x in range(1, x_dim - 1):
        for y in range(1, y_dim -1):
            if array[y][x] < threshold:
                continue
            neighbours = [array[y - 1][x - 1], array[y][x - 1],
                          array[y + 1][x - 1], array[y - 1][x],
                          array[y + 1][x], array[y - 1][x + 1],
                          array[y][x + 1], array[y + 1][x + 1]]
            new_array[y][x] = np.sum(neighbours) / len(neighbours)
    return new_array

def dilate_raster(array, kernel_size=3, threshold=120):
    '''smooth the borders of areas exceeding the given threshold,
    so that these areas shrink by half the kernel-size along their borders'''
    thresh_exceeded = array >= threshold
    ret = np.where(thresh_exceeded, np.nan, array)
    o = kernel_size // 2
    filtered = filters.generic_filter(
        ret, np.nanmedian, (kernel_size, kernel_size), origin=(o, o),
        mode='reflect')
    a = array.copy()
    thresh_exceeded_and_not_nan = thresh_exceeded & ~ np.isnan(filtered) 
    fill_values = filtered[thresh_exceeded]
    a[thresh_exceeded_and_not_nan] = filtered[thresh_exceeded_and_not_nan]
    return a

class RasterManagement(object):
    def __init__(self):
        self.raster_values = self.raster_origin = self.srid = None
        self.cellWidth = self.cellHeight = None
        # map point via id to a raster cell
        self.point_raster_map = {}

    def load(self, raster_file, unreachable=120):
        desc = arcpy.Describe(raster_file)
        e = desc.Extent
        self.srid = desc.spatialReference.factoryCode
        self.raster_origin = Point(e.XMin, e.YMax, epsg=self.srid)
        self.cellWidth = float(arcpy.GetRasterProperties_management(
            raster_file, 'CELLSIZEX').getOutput(0).replace(',', '.'))
        self.cellHeight = float(arcpy.GetRasterProperties_management(
            raster_file, 'CELLSIZEY').getOutput(0).replace(',', '.'))
        
        self.raster_values = dilate_raster(
            arcpy.RasterToNumPyArray(raster_file),
            threshold=unreachable
        )

    def register_points(self, points):
        if self.raster_values is None:
            raise Exception('A raster-file has to be loaded first!')
        for point in points:
            if point.epsg != self.srid:
                point.transform(self.srid) 
            mapped_x = int(abs(point.x - self.raster_origin.x) / self.cellWidth)
            mapped_y = int(abs(point.y - self.raster_origin.y) / self.cellHeight)
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

    def add_bbox_edge(self, bbox, rel_edge=0.1):
        """
        Change the size of the bbox to avoid rounding errors

        Parameters
        ----------
        bbox : tuple of points
            p1 and p2 define the upper right and the lower left corner of the
            box
        rel_edge : float opt
            relative factor for enlargement

        Returns
        -------
        bbox : tuple of points
            bigger bbox
        """
        p1, p2 = bbox
        bbox_size = abs(p1.x-p2.x)
        edge = bbox_size * rel_edge
        p1_new = Point(p1.x - edge, p1.y - edge, epsg=p1.epsg)
        p2_new = Point(p2.x + edge, p2.y + edge, epsg=p2.epsg)
        ret = (p1_new, p2_new)

        return ret

    def get_distances(self, origin, destinations, bbox=None):
        distances = np.ones(len(destinations), dtype=int)
        distances *= np.iinfo(distances.dtype).max
        dist_raster = self._request_dist_raster(origin)
        if dist_raster is None:
            return distances
        if bbox is not None:
            bbox = self.add_bbox_edge(bbox)
            fn, ext = os.path.splitext(dist_raster)
            clipped_raster = fn + '_clipped' + ext
            clip_raster(dist_raster, clipped_raster, bbox)
            arcpy.Delete_management(dist_raster)
            dist_raster = clipped_raster
        start = time.time()
        raster = RasterManagement()
        raster.load(dist_raster)
        print('filtering raster {}s'.format(time.time() - start))        
        start = time.time()
        raster.register_points(destinations)
        for i, dest in enumerate(destinations):
            distances[i] = raster.get_value(dest)
        print('mapping {}s'.format(time.time() - start))
    
        arcpy.Delete_management(dist_raster)
        return distances

    def _request_dist_raster(self, origin):
        err = 'Fehler bei der Anfrage. Liegt der Punkt innerhalb Deutschlands?'
        if origin.epsg != self.epsg:
            origin.transform(self.epsg) 
        params = {
            'batch': True,
            'routerId': self.ROUTER,
            'fromPlace': "{},{}".format(origin.y, origin.x),
            'toPlace': "{},{}".format(origin.y, origin.x),
            'mode': 'CAR',
            'maxWalkDistance': 5000,
            'maxPreTransitTime': 1200,
            'cutoffMinutes': 20
        }
        start = time.time()
        r = requests.post(self.URL, params=params)
        print('request post {}s'.format(time.time() - start))
        try: 
            id = r.json()['id']
        except:
            arcpy.AddError(err)
            return None
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
        else:
            arcpy.AddError(err)
            return None
        return out_raster

if __name__ == "__main__":
    for i in range(100):
        start = time.time()
        array = np.ones((100, 100))
        dilate_raster(array)
        print('{}s'.format(time.time() - start))