# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.standortkonkurrenz import tbx_osm_markteinlesen
reload(tbx_osm_markteinlesen)
from rpctools.analyst.standortkonkurrenz import tbx_projektwirkung
reload(tbx_projektwirkung)
from rpctools.analyst.standortkonkurrenz import tbx_edit_markets
reload(tbx_edit_markets)

from rpctools.analyst.standortkonkurrenz.tbx_osm_markteinlesen import TbxOSMMarktEinlesen
from rpctools.analyst.standortkonkurrenz.tbx_projektwirkung import TbxProjektwirkungMarkets
from rpctools.analyst.standortkonkurrenz.tbx_edit_markets import (
    TbxEditMarketsPlanfall, TbxEditMarketsNullfall)

class Toolbox(object):
    def __init__(self):
        self.label = u'standortkonkurrenz'
        self.alias = ''
        self.tools = [TbxOSMMarktEinlesen,
                      TbxProjektwirkungMarkets,
                      TbxEditMarketsNullfall, 
                      TbxEditMarketsPlanfall]

















