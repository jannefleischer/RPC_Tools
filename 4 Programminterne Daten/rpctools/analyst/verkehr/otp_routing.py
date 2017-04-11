# -*- coding: utf-8 -*-
#

import requests



class Point(object):
    """A Point object"""
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '{},{})'.format(self.lat, self.lon)


class OTPRouter(object):
    def __init__(self):
        self.url = r'https://rpcrouting.ggr-planung.de/otp/routers/hvv_car/plan'
        self.router = 'hvv_car'

    def get_routing_request(self, source, destination, mode='CAR'):
        """
        get a routing requset for route from source to destination

        Parameters
        ----------
        source : Point
        destination : Point
        mode : str, optional (default='CAR')
        """
        params = dict(routerId=self.router,
                      fromPlace=source,
                      toPlace=destination,
                      mode=mode)
        r = requests.get(self.url, params=params)
        return r.json()



if __name__ == '__main__':
    o = OTPRouter()
    s = Point(lat=53.58598, lon=9.49219)
    d = Point(lat=53.65034, lon=9.79843)
    j = o.get_routing_request(s, d)
    print(j)
