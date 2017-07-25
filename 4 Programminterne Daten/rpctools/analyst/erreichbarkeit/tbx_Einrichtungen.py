# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tool, Tbx
from rpctools.utils.spatial_lib import get_project_centroid, Point
from rpctools.utils.encoding import encode
from rpctools.analyst.erreichbarkeit.geoserver_query import GeoserverQuery


class Einrichtungen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Erreichbarkeit.gdb'
    cutoff = None

    modes = {
        'CAR': ('Auto', 15),
        'BICYCLE': ('Fahrrad', 10),
        'WALK': (u'zu Fuß', 3)
    }

    def add_outputs(self):
        pass

    def run(self):
        query = GeoserverQuery()
        categories = [u'Kita', u'ÖPNV_Haltestelle', u'Autobahnanschlussstelle']
        radius = self.par.radius.value * 1000
        x, y = get_project_centroid(self.par.projectname.value)
        centroid = Point(x, y, epsg=self.parent_tbx.config.epsg)
        target_epsg = self.parent_tbx.config.epsg
        features = query.get_features(centroid, radius, categories, target_epsg)


class TbxEinrichtungen(Tbx):
    @property
    def label(self):
        return encode(u'Einrichtungen anzeigen')

    @property
    def Tool(self):
        return Einrichtungen

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []

        param = self.add_parameter('radius')
        param.name = encode(u'radius')
        param.displayName = encode(u'Radius in Kilometern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [1, 20]
        param.value = 10

        return params

if __name__ == '__main__':
    t = TbxEinrichtungen()
    params = t.getParameterInfo()
    t.set_active_project()
    t.open()
    t.execute()