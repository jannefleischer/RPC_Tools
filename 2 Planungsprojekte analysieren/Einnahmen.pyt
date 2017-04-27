# -*- coding: utf-8 -*-

from rpctools.analyst.einnahmen import (tbx_wanderungssalden,
                                        tbx_saldenbearbeiten,
                                        tbx_steuersalden)
reload(tbx_wanderungssalden)
reload(tbx_saldenbearbeiten)
reload(tbx_steuersalden)

from rpctools.analyst.einnahmen.tbx_wanderungssalden import TbxWanderungssalden
from rpctools.analyst.einnahmen.tbx_saldenbearbeiten import (
    TbxEWSaldenbearbeiten, TbxGewSaldenbearbeiten)
from rpctools.analyst.einnahmen.tbx_steuersalden import TbxSteuersalden


class Toolbox(object):
    def __init__(self):
        self.label = u'Einnahmen'
        self.alias = ''
        self.tools = [TbxWanderungssalden,
                      TbxEWSaldenbearbeiten,
                      TbxGewSaldenbearbeiten, 
                      TbxSteuersalden,]
