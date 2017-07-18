# -*- coding: utf-8 -*-
# reload

from rpctools.analyst.erreichbarkeit.tbx_ErreichbarkeitOEPNV import TbxErreichbarkeitOEPNV
from rpctools.analyst.erreichbarkeit.tbx_HaltestellenZentraleOrte import TbxHaltestellenZentraleOrte
from rpctools.analyst.erreichbarkeit.tbx_Fahrplaene import TbxFahrplaene

class Toolbox(object):
    def __init__(self):
        self.label = u'Erreichbarkeit'
        self.alias = ''
        self.tools = [TbxHaltestellenZentraleOrte,
                      TbxFahrplaene, 
                      TbxErreichbarkeitOEPNV]


