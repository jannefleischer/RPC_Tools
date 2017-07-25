# -*- coding: utf-8 -*-
import requests
import json
import arcpy


class GeoserverQuery(object):
    feature_url = ('https://geoserver.ggr-planung.de/geoserver/projektcheck/wfs')
    
    feature_params = {
        'service': 'WFS',
        'request': 'GetFeature',
        'version': '2.0.0',
        'typeNames': 'projektcheck:projektcheck_deutschland',
        'CQL_FILTER': '',
        'count': 10000,
        'outputFormat': 'application/json',
        'srsname': 'EPSG:4326'
    }
    
    def __init__(self):
        self.epsg = 3035


    def get_features(self, point, radius, categories, target_epsg):
        '''point has to be in epsg 31467!'''
        if point.epsg != self.epsg:
            point.transform(self.epsg)
        params = self.feature_params.copy()
        params['srsname'] = 'EPSG:{}'.format(target_epsg)
        categories = [u"'{}'".format(c) for c in categories]
        cql_filter = (u'projektcheck_category IN ({cat}) '
                      u'AND DWithin(geom,POINT({y} {x}), {radius}, meters)'
                      .format(cat=u','.join(categories),
                              x=point.x, y=point.y,
                              radius=radius))
        params['CQL_FILTER'] = cql_filter
        r = requests.get(self.feature_url, params=params)
        r.raise_for_status()
        return r
