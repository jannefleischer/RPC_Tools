# -*- coding: utf-8 -*-
#

import arcpy
import os
from rpctools.utils.params import Tool
from rpctools.analyst.verkehr.otp_router import Point, OTPRouter


class Routing(Tool):
    _dbname = 'FGDB_Verkehr.gdb'
    _param_projectname = 'project'

    def run(self):
        toolbox = self.parent_tbx
        # tbx settings
        outer_circle = toolbox.par.outer.value
        inner_circle = toolbox.par.inner.value
        n_segments = toolbox.par.dests.value

        # create tmp_table for transforming from gauss-krüger to 4326
        tfl = self.folders.get_table("Teilflaechen_Plangebiet",
                                     workspace='FGDB_Definition_Projekt.gdb')
        tmp_table = os.path.join(arcpy.env.scratchGDB,
                                 "Teilflaechen_Plangebiet")
        if arcpy.Exists(tmp_table):
            arcpy.Delete_management(tmp_table)
        arcpy.Copy_management(tfl, tmp_table)   # create tmp table
        arcpy.AddGeometryAttributes_management(
            Input_Features=tmp_table, Geometry_Properties="CENTROID_INSIDE",
            Coordinate_System=4326)

        # get centroid coordinates
        columns = ['id_teilflaeche', 'INSIDE_X', 'INSIDE_Y']
        cursor = arcpy.da.SearchCursor(tmp_table, columns)
        XY_INSIDE = [row for row in cursor]
        del cursor
        arcpy.Delete_management(tmp_table)

        # calculate routes
        workspace = self.folders.get_db()
        o = OTPRouter(workspace)
        r_id = 0
        for centroid in XY_INSIDE:
            source_id, x_coord, y_coord = centroid
            # ? lat = y lon = x
            source = Point(lat=y_coord, lon=x_coord)    # centroid
            # calculate segments around centroid
            destinations = o.create_circle(source, dist=outer_circle,
                                           n_segments=n_segments)
            # calculate the routes to the segments
            for (lon, lat) in destinations:
                destination = Point(lat, lon)
                print r_id,
                json = o.get_routing_request(source, destination)
                o.decode_coords(json, route_id=r_id, source_id=source_id)
                r_id += 1

        o.nodes.transform()
        o.nodes_to_graph(meters=inner_circle)

        o.transfer_nodes.calc_initial_weight()
        o.calc_vertex_weights()
        o.create_polyline_features()
        o.create_node_features()
        print o.transfer_nodes.keys()
        o.create_transfer_node_features()
        
        o.dump(self.folders.get_otp_pickle_filename(check=False))

        # Empty column for manual changes of weigths
        nodes_path = self.folders.get_table('Zielpunkte', workspace='', project='',
                                   check=True)
        arcpy.AddField_management(nodes_path, 'Manuelle_Gewichtung')
        arcpy.AddField_management(nodes_path, 'Neue_Gewichte',
                                  field_type='DOUBLE')

        # Add Layers
        lyr_zielpunkte = self.folders.get_layer('Zielpunkte', 'Verkehr')
        fc_zielpunkte = self.folders.get_table('Zielpunkte')
        self.output.add_output('verkehr', lyr_zielpunkte, fc_zielpunkte)

        #lyr_nodes = self.folders.get_layer('nodes', 'Verkehr')
        #fc_nodes = self.folders.get_table('nodes')
        #self.output.add_output('verkehr', lyr_nodes, fc_nodes)

        lyr_links = self.folders.get_layer('links', 'Verkehr')
        fc_links = self.folders.get_table('links')
        self.output.add_output('verkehr', lyr_links, fc_links)


if __name__ == '__main__':
    o = OTPRouter(r'C:\ggr Projekte\RPC_Tools\3 Benutzerdefinierte Projekte\Test Verkehr\FGDB_Verkehr.gdb')
    source = Point(lat=53.5, lon=9.589)
    source_id = 0
    destinations = o.create_circle(source, dist=1000, n_segments=12)
    for d, (lon, lat) in enumerate(destinations):
        destination = Point(lat, lon)
        print d,
        json = o.get_routing_request(source, destination)
        o.decode_coords(json, route_id=d, source_id=source_id)

    max_d = d
    source = Point(lat=53.502, lon=9.587)
    source_id = 1
    for d, (lon, lat) in enumerate(destinations):
        destination = Point(lat, lon)
        json = o.get_routing_request(source, destination)
        o.decode_coords(json, route_id=d+max_d, source_id=source_id)

    o.nodes.transform()
    o.nodes_to_graph()
    o.transfer_nodes.calc_initial_weight()
    o.calc_vertex_weights()
    o.create_polyline_features()
    o.create_node_features()
    o.create_transfer_node_features()
