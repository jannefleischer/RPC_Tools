# -*- coding: utf-8 -*-
#

import arcpy
import os
from rpctools.utils.params import Tool
from rpctools.analyst.verkehr.otp_router import Point, OTPRouter
from rpctools.outputs.verkehr import VerkehrOutput


class Routing(Tool):
    _workspace = 'FGDB_Verkehr.gdb'
    _param_projectname = 'project'
    
    @property
    def Output(self):
        return VerkehrOutput

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

        # get data from Teilflaechen_Plangebiet table
        columns = ['id_teilflaeche', 'SOURCE_X', 'SOURCE_Y', 'Wege_gesamt',
                   'Nutzungsart']
        cursor = arcpy.da.SearchCursor(tmp_table, columns)
        data_tfl = [row for row in cursor]
        del cursor
        arcpy.Delete_management(tmp_table)
        # get data from Wege_je_nutzung table
        data_wjn = toolbox.query_table('Wege_je_nutzung',
                                       columns=['Nutzungsart', 'Wege_gesamt',
                                                'PKW_Anteil'])

        def calc_trips(data_tfl, data_wjn):
            for i in range(len(data_wjn)):
                tou = data_wjn[i][0]  # type of use
                # trips * %cars
                trips_by_car = data_wjn[i][1] * data_wjn[i][2] / 100
                tfl_id_with_tou = []
                total_trips_for_tou = 0
                for j in range(len(data_tfl)):
                    source_id, x_coord, y_coord, trips, tfl_use = data_tfl[j]
                    if tou == tfl_use:
                        tfl_id_with_tou.append(j)
                        total_trips_for_tou += trips
                for tfl_id in tfl_id_with_tou:
                    source_id, x_coord, y_coord, trips, tfl_use = data_tfl[tfl_id]
                    trips = trips_by_car * trips / total_trips_for_tou
                    data_tfl[tfl_id] = (source_id, x_coord, y_coord, trips, tfl_use)
            return data_tfl

        data_tfl = calc_trips(data_tfl, data_wjn)

        # calculate routes
        workspace = self.folders.get_db()
        o = OTPRouter(workspace)
        r_id = 0
        for single_tfl in data_tfl:
            source_id, x_coord, y_coord, trips, tfl_use = single_tfl
            if not trips:
                continue
            o.areas.add_area(source_id, trips=trips)
            # ? lat = y lon = x
            source = Point.from_xy(y=y_coord, x=x_coord,
                                   srid_proj=o.p2, srid_geogr=o.p1)    # centroid

            # calculate segments around centroid
            destinations = o.create_circle(source, dist=outer_circle,
                                           n_segments=n_segments)
            # calculate the routes to the segments
            for (lon, lat) in destinations:
                destination = Point(lat, lon)
                arcpy.AddMessage('suche Routen {}'.format(r_id))
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
