# -*- coding: utf-8 -*-
#

import requests

#import arcpy
import os
from collections import OrderedDict
#from rpctools.analyst.verkehr.otp_routing import Point
from pyproj import Proj, transform
import urllib
import re
import arcpy


class Point(object):
    """A Point object"""
    __slots__ = ['x', 'y', 'node_id', 'geom', 'epsg']
    def __init__(self, x, y, node_id=None, epsg=4326):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.geom = None
        self.epsg = Proj(init='epsg:{}'.format(epsg))

    def __repr__(self):
        return '{},{}'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def create_geom(self):
        """Create geometry from coordinates"""
        geom = arcpy.Point(self.x, self.y)
        self.geom = geom

    def transform(self, target_srid):
        target_srs = Proj(init='epsg:{}'.format(target_srid))
        x, y = transform(self.epsg, target_srs, self.x, self.y)
        return Point(x, y, epsg=target_srid)


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
    def __init__(self, epsg=31467):
        self.geoserver_epsg = 3035
        self.url = r'https://geoserver.ggr-planung.de/geoserver/projektcheck/wfs?'
        self.wfs_params = dict(service='WFS',
                               request='GetFeature',
                               version='2.0.0',
                               typeNames='projektcheck:supermaerkte',
                               outputFormat='application/json')
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
        transformed = point.transform(self.geoserver_epsg)
        srsname = 'EPSG:{}'.format(self.epsg)
        params = dict(CQL_FILTER=query.format(x=transformed.x,
                                              y=transformed.y,
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
        try:
            json = r.json()
        except ValueError:
            return []
        return self._decode_json(json)

    def _decode_json(self, json):
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


    def set_chains(self):
        """
        Assign chains to supermarkets

        """
        projectname = self.projectname
        ws_markets = self.folders.get_db('FGDB_Standortkonkurrenz_Supermaerkte.gdb', projectname)
        ws_chains = self.folders.get_basedb('FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb')
        
        table_markets = os.path.join(ws_markets, "Maerkte")
        fields = ["name", "id_kette", "id_betriebstyp_nullfall", "id_betriebstyp_planfall"]
        market_cursor = arcpy.da.UpdateCursor(table_markets, fields)
        
        table_chains = os.path.join(ws_chains, "Ketten_Zuordnung")
        fields = ["regex", "id_kette", "id_betriebstyp"]
        chain_cursor = arcpy.da.SearchCursor(table_chains, fields, sql_clause=(None, 'ORDER BY prioritaet')) 
               
        for market in market_cursor:
            match_found = False
            
            for chain in chain_cursor:
                chain_expression = re.compile(chain[0])
                if chain_expression.match(market[0]) not None:
                    match_found = True
                    market[1] = chain[1]
                    market[2] = chain[2]
                    market[3] = chain[2]
                    market_cursor.updateRow(market)
                    break
                
            if not match_found:
                market[1] = 0
                market[2] = 0
                market[3] = 0
                 
            

if __name__ == '__main__':
    o = OSMShopsReader()
    source = Point(54, 10, epsg=4326)
    #source = source.transform(3035)
    supermarkets = o.get_shops(source)
    o.create_supermarket_features(supermarkets)
    o.set_chains()




