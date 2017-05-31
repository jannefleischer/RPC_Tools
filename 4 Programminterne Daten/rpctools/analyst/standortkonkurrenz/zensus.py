from rpctools.utils.config import Folders
from rpctools.utils.spatial_lib import clip_raster
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point

import os
import shutil
import sys
import arcpy


class ZensusCell(Point):
    def __init__(self, x, y, epsg=4326, ew=0, id=None):
        super(ZensusCell, self).__init__(x, y, id, epsg=epsg)
        self.ew = ew


class Zensus(object):
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

    def cutout_area(self, centroid, size):
        """return the centroids of the zensus cells as points in a square area 
        with the dimensions of distance x distance with the given centroid in 
        the middle
        """

        zensus_points = []
        zensus_raster = self.folders.ZENSUS_RASTER_FILE
        # p1 and p2 build square around centroid
        p1 = Point(centroid.x - size / 2,
                   centroid.y - size / 2,
                   epsg=centroid.epsg)
        p2 = Point(centroid.x + size / 2,
                   centroid.y + size / 2,
                   epsg=centroid.epsg)
        
        bbox = (p1, p2)
        
        out_raster = os.path.join(self.tmp_folder, 'zensus_cutout.tif')
        
        srid = clip_raster(zensus_raster, out_raster, bbox)
        
        out_shp = os.path.join(self.tmp_folder,
                               'zensus_cutout.shp')
        #cellsize = float(arcpy.GetRasterProperties_management(
            #zensus_file, 'CELLSIZEX').getOutput(0).replace(',', '.'))
        
        
        arcpy.RasterToPoint_conversion(out_raster, out_shp)
        
        desc = arcpy.Describe(out_shp)
        rows = arcpy.da.SearchCursor(out_shp, ['SHAPE@XY', 'GRID_CODE'])
        for (x, y), value in rows:
            p = ZensusCell(x, y, epsg=srid, ew=value)
            zensus_points.append(p)
            
        return zensus_points, bbox