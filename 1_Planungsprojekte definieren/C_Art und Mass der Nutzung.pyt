# -*- coding: utf-8 -*-

from rpctools.utils.encoding import encode

from rpctools.definitions.nutzungsart import (tbx_flaechenbilanz,
                                              tbx_nutzungen)  
reload(tbx_flaechenbilanz)
reload(tbx_nutzungen)

from rpctools.definitions.nutzungsart.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.definitions.nutzungsart.tbx_nutzungen import TbxNutzungen


class Toolbox(object):
    def __init__(self):
        self.label = encode(u'Art und Maß der Nutzung')
        self.alias = ''
        self.tools = [TbxFlaechenbilanz, TbxNutzungen]
