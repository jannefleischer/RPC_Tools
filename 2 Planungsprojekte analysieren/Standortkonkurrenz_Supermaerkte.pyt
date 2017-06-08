# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.standortkonkurrenz import tbx_osm_markteinlesen
reload(tbx_osm_markteinlesen)
from rpctools.analyst.standortkonkurrenz import tbx_dist_markets
reload(tbx_dist_markets)
from rpctools.analyst.standortkonkurrenz import tbx_edit_markets
reload(tbx_edit_markets)

from rpctools.analyst.standortkonkurrenz.tbx_osm_markteinlesen import TbxOSMMarktEinlesen
from rpctools.analyst.standortkonkurrenz.tbx_dist_markets import TbxDistMarkets
from rpctools.analyst.standortkonkurrenz.tbx_edit_markets import (
    TbxEditMarketsPlanfall, TbxEditMarketsNullfall)

class Toolbox(object):
    def __init__(self):
        self.label = u'standortkonkurrenz'
        self.alias = ''
        self.tools = [TbxOSMMarktEinlesen,
                      TbxDistMarkets,
                      TbxEditMarketsNullfall, 
                      TbxEditMarketsPlanfall]

















