# -*- coding: utf-8 -*-
import requests
import re

class BahnQuery(object):
    reiseauskunft_url = 'http://reiseauskunft.bahn.de/bin/query.exe/dn' #?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&start=1"
    mobile_url = 'http://mobile.bahn.de/bin/mobil/query.exe/dox'
    
    routing_params = {
        'S': '',
        'Z': '',
    }
    
    station_params = {
        'Id': 9627,
        'n': 1,
        'rt': 1,
        'use_realtime_filter': 1,
        'performLocating': 2, 
        'tpl': 'stopsnear',
        'look_maxdist': 2000,
        'look_stopclass': 1023,
        'look_x': 0,
        'look_y': 0
    }
    
    def __init__(self):
        pass
    
    def closest_station(self, point, max_distance=2000, stopclass=1023):
        """get closest station to given point (tuple of x,y; epsg: 4326)"""
        # set url-parameters 
        params = self.station_params.copy()
        params['look_maxdist'] = max_distance
        params['look_stopclass'] = stopclass
        x, y = point
        params['look_x'] = ("%.6f" % x).replace('.','')
        params['look_y'] = ("%.6f" % y).replace('.','')
        
        r = requests.get(self.mobile_url, params=params)
        # use regular expressions instead of parsing to xml, because html is
        # malformed and lxml is tough to install on all machines
        regex = '<a class="uLine" .*>(.*?)</a>'
        stops = re.findall(regex, r.text)
        # ToDo: sort distances or do sth else with them? 
        # (stations are already sorted ascending)
        regex = '<div style="float:right">\\n(.*?) m\\n</div>'
        distances = re.findall(regex, r.text)
        
        return stops[0].decode('utf8')
    
    def routing(origin, destination, times):
        params = {}