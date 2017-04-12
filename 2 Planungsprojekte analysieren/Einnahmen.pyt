# -*- coding: utf-8 -*-

from rpctools.analyst.einnahmen import (tbx_wanderungssalden, tbx_saldenbearbeiten, tbx_saldenbearbeiten2,
                                        tbx_steuersalden)
reload(tbx_wanderungssalden)
reload(tbx_saldenbearbeiten)
reload(tbx_saldenbearbeiten2)
reload(tbx_steuersalden)


from rpctools.analyst.einnahmen.tbx_wanderungssalden import TbxWanderungssalden
from rpctools.analyst.einnahmen.tbx_saldenbearbeiten import TbxSaldenbearbeiten
from rpctools.analyst.einnahmen.tbx_saldenbearbeiten2 import TbxSaldenbearbeiten2
from rpctools.analyst.einnahmen.tbx_steuersalden import TbxSteuersalden

class Toolbox(object):
    def __init__(self):
        self.label = u'Einnahmen'
        self.alias = ''
        self.tools = [TbxWanderungssalden,
                      TbxSaldenbearbeiten,
                      TbxSaldenbearbeiten2,
                      TbxSteuersalden,]
