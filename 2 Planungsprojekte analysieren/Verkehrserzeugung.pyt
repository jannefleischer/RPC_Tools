# -*- coding: utf-8 -*-

from rpctools.analyst.verkehr.tbx_routing import TbxRouting
from rpctools.analyst.verkehr.tbx_update_nodes import TbxUpdateNodes
from rpctools.analyst.verkehr.tbx_settings import TbxSettings
from rpctools.analyst.verkehr.tbx_set_source import TbxSetSource


class Toolbox(object):
    def __init__(self):
        self.label = u'Verkehr'
        self.alias = ''
        self.tools = [TbxRouting,
                      TbxUpdateNodes,
                      TbxSettings,
                      TbxSetSource]







