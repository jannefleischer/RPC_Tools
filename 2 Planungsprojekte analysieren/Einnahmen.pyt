# -*- coding: utf-8 -*-

from rpctools.analyst.einnahmen import (tbx_vorberechnungen, tbx_einnahmen,
                                        tbx_grundsteuer, tbx_gewerbesteuer)  
reload(tbx_vorberechnungen)
reload(tbx_einnahmen)
reload(tbx_grundsteuer)
reload(tbx_gewerbesteuer)

from rpctools.analyst.einnahmen.tbx_vorberechnungen import TbxVorberechnungen
from rpctools.analyst.einnahmen.tbx_einnahmen import (
    TbxEinkommenssteuer,
    TbxFamilienleistungsausgleich,
    TbxKFA,
    TbxKRU,
    TbxTest)
from rpctools.analyst.einnahmen.tbx_grundsteuer import TbxGrundsteuer
from rpctools.analyst.einnahmen.tbx_gewerbesteuer import TbxGewerbesteuer

class Toolbox(object):
    def __init__(self):
        self.label = u'Einnahmen'
        self.alias = ''
        self.tools = [TbxVorberechnungen,
                      TbxEinkommenssteuer,
                      TbxFamilienleistungsausgleich,
                      TbxGrundsteuer,
                      TbxGewerbesteuer,
                      TbxKFA,
                      TbxKRU,
                      TbxTest]
