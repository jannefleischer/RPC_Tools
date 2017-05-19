# -*- coding: utf-8 -*-
#

import requests

#import arcpy
import os
from collections import OrderedDict
#from rpctools.analyst.verkehr.otp_routing import Point
from pyproj import Proj, transform
import urllib
import arcpy
from rpctools.utils.config import Config 

config = Config()

class Point(object):
    """A Point object"""
    __slots__ = ['lat', 'lon', 'x', 'y', 'node_id', 'geom', 'epsg']
    def __init__(self, lat, lon, node_id=None, x=None, y=None, epsg=4326):
        self.lat = lat
        self.lon = lon
        self.node_id = node_id
        self.x = x
        self.y = y
        self.geom = None
        self.epsg = Proj(init='epsg:{}'.format(epsg))

    def __repr__(self):
        return '{},{}'.format(self.lat, self.lon)

    def __hash__(self):
        return hash((self.lat, self.lon))

    def create_geom(self):
        """Create geometry from coordinates"""
        geom = arcpy.Point(self.x, self.y)
        self.geom = geom

    def transform(self, target_srid):
        target_srs = Proj(init='epsg:{}'.format(target_srid))
        self.x, self.y = transform(self.epsg, target_srs, self.lon, self.lat)


class Supermarket(Point):
    """A Supermarket"""
    __slots__ = ['id_markt', 'x', 'y', 'name', 'kette', 'shop', 'typ', 'geom']
    def __init__(self, id_markt, x, y, name, kette, shop, typ, **kwargs):
        self.id_markt = id_markt
        self.x = x
        self.y = y
        self.name = name
        self.kette = kette
        self.shop = shop
        self.typ = typ
        self.geom = None

    def __repr__(self):
        return u'{},{}'.format(self.kette, self.name)


class OSMShopsReader(object):
    def __init__(self, workspace, epsg=31467):

        self.url = r'https://geoserver.ggr-planung.de/geoserver/projektcheck/wfs?'
        self.wfs_params = dict(service='WFS',
                               request='GetFeature',
                               version='2.0.0',
                               typeNames='projektcheck:supermaerkte',
                               outputFormat='application/json')

        self.ws = workspace
        self.epsg = epsg

    def get_shops(self, point, distance=20000, count=1000):
        """
        get shops from osm

        Parameters
        ----------
        source : Point
        distance : float
            the distance in meters

        Returns
        -------
        json
        """
        query = 'DWithin(geom,POINT({y} {x}),{m},meters)'
        srsname = 'EPSG:{}'.format(config.epsg)
        params = dict(CQL_FILTER=query.format(x=point.x,
                                              y=point.y,
                                              m=distance),
                      srsname=srsname,
                      count=str(count))
        params.update(self.wfs_params)
        new_params = []
        for (k, v) in params.items():
            param = '='.join([urllib.quote(k), urllib.quote(v)])
            new_params.append(param)
        param_str = '&'.join(new_params)
        r = requests.get(self.url, params=param_str)
        return r.json()

    def decode_json(self, json):
        """
        Parse the geometry from a json

        Parameters
        ----------
        json : json-instance

        route_id : int

        source_id : int, optional(default=0)

        Returns
        -------
        supermarkets : list
            a list with all supermarkets found
        """
        try:
            features = json['features']
        except KeyError:
            return
        n_features = len(features)
        supermarkets = []
        id_markt = 0
        for feature in features:
            id_markt += 1
            x, y = feature['geometry']['coordinates']
            properties = feature['properties']
            supermarket = Supermarket(id_markt, x, y, **properties)
            supermarkets.append(supermarket)
        return supermarkets

    def truncate(self, fc):
        """
        Truncate the table

        Parameters
        ----------
        fc : str
            the table to truncate
        """
        arcpy.TruncateTable_management(in_table=fc)

    def create_supermarket_features(self,
                                    supermarkets,
                                    name_fc='supermaerkte'):
        """Create the point-features for supermarkets"""
        sr = arcpy.SpatialReference(self.epsg)
        fields = ['id_markt',
                  'name',
                  'kette',
                  'shop',
                  'typ',
                  'SHAPE@']
        fc = os.path.join(self.ws, name_fc)
        self.truncate(fc)
        with arcpy.da.InsertCursor(fc, fields) as rows:
            for markt in supermarkets:
                markt.create_geom()
                if markt.geom:
                    rows.insertRow((markt.node_id,
                                    markt.name,
                                    markt.kette,
                                    markt.shop,
                                    markt.typ,
                                    markt.geom))




#class Routing(Tool):
    #_dbname = 'FGDB_Standortkonkurrenz.gdb'


    #def run(self):
        #toolbox = self.parent_tbx
        ## tbx settings



if __name__ == '__main__':
    o = OSMShopsReader(workspace='')
    source = Point(lat=54, lon=10)
    source.transform(3035)
    json = o.get_shops(source)
    supermarkets = o.decode_json(json)
    o.create_supermarket_features(supermarkets)




