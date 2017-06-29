# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.erreichbarkeit import tbx_Einrichtungen
reload(tbx_Einrichtungen)
from rpctools.analyst.erreichbarkeit import tbx_Ergebnisausgabe
reload(tbx_Ergebnisausgabe)

from rpctools.analyst.erreichbarkeit.tbx_Einrichtungen import TbxEinrichtungen
from rpctools.analyst.erreichbarkeit.tbx_Ergebnisausgabe import TbxErgebnisausgabe
from rpctools.analyst.erreichbarkeit.tbx_ErreichbarkeitOEPNV import TbxErreichbarkeitOEPNV
from rpctools.analyst.erreichbarkeit.tbx_HaltestellenZentraleOrte import TbxHaltestellenZentraleOrte
from rpctools.analyst.erreichbarkeit.tbx_fahrplaene import TbxFahrplaene

class Toolbox(object):
    def __init__(self):
        self.label = u'Erreichbarkeit'
        self.alias = ''
        self.tools = [TbxEinrichtungen,
                      TbxHaltestellenZentraleOrte,
                      TbxFahrplaene, 
                      TbxErreichbarkeitOEPNV,
                      TbxErgebnisausgabe]


