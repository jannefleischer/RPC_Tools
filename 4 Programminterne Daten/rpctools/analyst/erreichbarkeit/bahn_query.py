# -*- coding: utf-8 -*-
import requests
import re
from HTMLParser import HTMLParser
from rpctools.utils.spatial_lib import Point
import datetime


class Stop(Point):
    def __init__(self, x, y, name, id=None, epsg=4326):
        super(Stop, self).__init__(x, y, id=id, epsg=epsg)
        self.name = name


class BahnQuery(object):
    reiseauskunft_url = 'http://reiseauskunft.bahn.de/bin/query.exe/dn' #?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&start=1"
    mobile_url = 'http://mobile.bahn.de/bin/mobil/query.exe/dox'
    timetable_url = 'http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn'#?ld=96242&country=DEU&rt=1&evaId=%s&bt=dep&time=24:00&maxJourneys=10000&date=%s&productsFilter=1111111111&max=10000&start=yes'
    
    routing_params = {
        'start': 1,
        'S': '',
        'Z': '',
        'date': '',
        'time': ''
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
    
    timetable_params = {
        'ld': 96242,
        'country': 'DEU',
        'rt': 1,
        'bt': 'dep',
        'start': 'yes',
        'productsFilter': 1111111111,
        'max': 10000,
        'maxJourneys': 10000,
        'time': '24:00',
        'date': '',
        'evaId': 0,        
    }
    
    date_pattern = '%d.%m.%Y'
    
    def __init__(self, date=None):
        self.html = HTMLParser()
        date = date or datetime.date.today()
        self.date = date.strftime(self.date_pattern)
        
    def _to_db_coord(self, c):
        return ("%.6f" % c).replace('.','')
    
    def _from_db_coord(self, c):
        return c / 1000000.
    
    def stops_near(self, point, max_distance=2000, stopclass=1023, n=5000):
        """get closest station to given point (tuple of x,y; epsg: 4326)
        ordered by distance (ascending)
        """
        # set url-parameters 
        params = self.station_params.copy()
        params['look_maxdist'] = max_distance
        params['look_stopclass'] = stopclass
        if point.epsg != 4326:
            raise ValueError('Point has to be in WGS84!')
        params['look_x'] = self._to_db_coord(point.x)
        params['look_y'] = self._to_db_coord(point.y)
        
        r = requests.get(self.mobile_url, params=params)
        # use regular expressions instead of parsing to xml, because html is
        # malformed and lxml is tough to install on all machines
        
        regex = '<a class="uLine"(.*?)</a>'
        rows = re.findall(regex, r.text)
        
        def parse_href_number(tag, href):
            regex = '{tag}=(\d+)!'.format(tag=tag)
            return re.search(regex, href).group(1)
        
        stops = []
        
        for row in rows:
            regex = '>(.*)'
            _name = re.search(regex, row).group(1)
            if not _name:
                continue
            _x = int(parse_href_number('X', row))
            _y = int(parse_href_number('Y', row))
            _id = int(parse_href_number('id', row))
            _dist = int(parse_href_number('dist', row))
            stop = Stop(self._from_db_coord(_x), self._from_db_coord(_y),
                        self.html.unescape(_name),
                        id=_id, epsg=4326)
            stop.dist = _dist
            stops.append(stop)
        
        # response should be sorted by distances in first place, 
        # but do it again because you can
        stops_sorted = sorted(stops, key=lambda x: x.dist)        
        if n < len(stops_sorted):
            stops_sorted[:n]
                
        return stops
    
    def routing(origin, destination, times):
        params = {}
        
    def n_departures(self, stop_ids, max_journeys=10000):
        '''stop_ids have to be hafas stuff'''
        # set url-parameters 
        params = self.timetable_params.copy()
        params['date'] = self.date
        params['maxJourneys'] = max_journeys
        regex = 'id="journeyRow_(\d+)"'
        n_departures = []
        
        for id in stop_ids:
            params['evaId'] = id
            r = requests.get(self.timetable_url, params=params)
            n_rows = len(re.findall(regex, r.text))
            n_departures.append(n_rows)
            #sleep(0.5)
            
        return n_departures