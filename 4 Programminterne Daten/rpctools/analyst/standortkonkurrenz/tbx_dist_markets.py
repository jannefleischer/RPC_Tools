# -*- coding: utf-8 -*-
import arcpy
import os
import pandas as pd

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_project_centroid
from rpctools.analyst.standortkonkurrenz.zensus import Zensus
from rpctools.analyst.standortkonkurrenz.routing_distances import DistanceRouting
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point


class DistMarkets(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def run(self):
        square_size = self.par.square_size.value * 1000
        zensus = Zensus()
        
        x, y = get_project_centroid(self.projectname)
        centroid = Point(x, y, epsg=self.parent_tbx.config.epsg)
        
        zensus_points = zensus.cutout_area(centroid, square_size)
        self.zensus_to_db(zensus_points)
        
        routing = DistanceRouting()
        
        fn = routing.request_dist_raster(centroid)
        print()
        
    def zensus_to_db(self, zensus_points):
        df = pd.DataFrame()
        epsg = self.parent_tbx.config.epsg
        shapes = []
        ews = []
        self.parent_tbx.delete_rows_in_table('Siedlungszellen')
        for point in zensus_points:
            if point.ew <= 0:
                continue
            t = point.transform(epsg)
            t.create_geom()
            shapes.append(t.geom)
            ews.append(point.ew)
            
        df['id'] = range(len(shapes))
        df['SHAPE'] = shapes
        df['ew'] = ews
        
        self.parent_tbx.insert_dataframe_in_table('Siedlungszellen', df)
        addLayer = arcpy.mapping.Layer(self.folders.get_table('Siedlungszellen'))
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        arcpy.mapping.AddLayer(df, addLayer)


class TbxDistMarkets(Tbx):

    @property
    def label(self):
        return encode(u'Entfernung zwischen Supermarkt und '
                      u'Rasterzellen berechnen')

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
    t.par.projectname.value = t.config.active_project
    t.execute()

    print 'done'