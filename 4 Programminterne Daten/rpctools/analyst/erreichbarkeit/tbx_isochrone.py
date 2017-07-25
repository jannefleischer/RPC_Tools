# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tool, Tbx
from rpctools.utils.spatial_lib import get_project_centroid, Point
from rpctools.utils.encoding import encode
from rpctools.analyst.erreichbarkeit.routing_query import RoutingQuery


class Isochrone(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Erreichbarkeit.gdb'

    modes = {
        'CAR': ('Auto', 15),
        'BICYCLE': ('Fahrrad', 10),
        'WALK': (u'zu Fuß', 3)
    }

    def add_outputs(self):
        group_layer = ("erreichbarkeit")
        layers = ['Isochrone zu Fuß',
                  'Isochrone Fahrrad',
                  'Isochrone Auto']
        fc = u'Isochrone'
        for layer in layers:
            self.output.add_layer(group_layer, layer, fc,
                                  template_folder='Erreichbarkeit',
                                  zoom=False)

    def run(self):
        table = 'Isochrone'
        column_values = {'modus': [], 'SHAPE@': []}

        self.parent_tbx.delete_rows_in_table(table)
        x, y = get_project_centroid(self.par.projectname.value)
        centroid = Point(x, y, epsg=self.parent_tbx.config.epsg)
        cutoff_sec = self.par.cutoff.value * 60
        query = RoutingQuery()
        target_epsg = self.parent_tbx.config.epsg
        for mode, (name, speed) in self.modes.iteritems():
            iso_poly = query.get_isochrone(centroid, target_epsg,
                                           mode, cutoff_sec, speed)
            column_values['modus'].append(name)
            column_values['SHAPE@'].append(iso_poly)
        self.parent_tbx.insert_rows_in_table(table, column_values)



class TbxIsochrone(Tbx):
    @property
    def label(self):
        return encode(u'Isochrone anzeigen')

    @property
    def Tool(self):
        return Isochrone

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

        param = self.add_parameter('cutoff')
        param.name = encode(u'Erreichbarkeit')
        param.displayName = encode(u'Erreichbarkeit in x Minuten')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [5, 60]
        param.value = 10

        return params

if __name__ == '__main__':
    t = TbxIsochrone()
    params = t.getParameterInfo()
    t.set_active_project()
    t.open()
    t.execute()