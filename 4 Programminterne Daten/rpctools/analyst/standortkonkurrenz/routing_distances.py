from rpctools.utils.config import Folders

import arcpy
import os
import shutil
import requests
import sys


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
        
    def request_dist_raster(self, point):
        t = point.transform(self.epsg) if point.epsg != self.epsg \
            else point
        params = {
            'batch': True,
            'routerId': self.ROUTER,
            'fromPlace': "{},{}".format(t.y, t.x),
            'toPlace': "{},{}".format(t.y, t.x),
            'mode': 'CAR',
            'maxWalkDistance': 750,
            'maxPreTransitTime': 1200
        }
        r = requests.post(self.URL, params=params)
        id = r.json()['id']
        url = '{url}/{id}/raster'.format(url=self.URL, id=id)
        r = requests.get(url, stream=True)
        out_raster = os.path.join(
            self.tmp_folder,
            self.RASTER_FILE_PATTERN.format(id=point.id))
        if r.status_code == 200:
            with open(out_raster, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        return out_raster
    
    def apply_distances(self, points, raster):
        for point in points:
            t = point.transform(self.epsg) if point.epsg != self.epsg \
                else point
            res = arcpy.GetCellValue_management(raster,
                                                '{x} {y}'.format(x=t.x, y=t.y))
            point.distance = res.getOutput(0)
        return points