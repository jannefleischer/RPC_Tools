# -*- coding: utf-8 -*-
from rpctools.analyst.verkehr import tbx_routing
reload(tbx_routing)
from rpctools.analyst.verkehr import tbx_update_nodes
reload(tbx_update_nodes)
from rpctools.analyst.verkehr import tbx_settings
reload(tbx_settings)

from rpctools.analyst.verkehr.tbx_routing import TbxRouting
from rpctools.analyst.verkehr.tbx_update_nodes import TbxUpdateNodes
from rpctools.analyst.verkehr.tbx_settings import TbxSettings


class Toolbox(object):
    def __init__(self):
        self.label = u'Verkehr'
        self.alias = ''
        self.tools = [TbxRouting,
                      TbxUpdateNodes,
                      TbxSettings]







