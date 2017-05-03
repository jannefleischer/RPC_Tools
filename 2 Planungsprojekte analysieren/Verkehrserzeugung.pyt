# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.verkehr import tbx_Basisdatenbearbeiten
reload(tbx_Basisdatenbearbeiten)
from rpctools.analyst.verkehr import tbx_Routingsdurchfuehren
reload(tbx_Routingsdurchfuehren)
from rpctools.analyst.verkehr import tbx_VerkehrsmengenErmitteln
reload(tbx_VerkehrsmengenErmitteln)
from rpctools.analyst.verkehr import tbx_VerkehrsmengenErmitteln
reload(tbx_VerkehrsmengenErmitteln)
from rpctools.analyst.verkehr import tbx_routing
reload(tbx_routing)
from rpctools.analyst.verkehr import tbx_update_nodes
reload(tbx_update_nodes)

from rpctools.analyst.verkehr.tbx_Routingsdurchfuehren import TbxRoutingsdurchfuehren
from rpctools.analyst.verkehr.tbx_Basisdatenbearbeiten import TbxBasisdatenbearbeiten
from rpctools.analyst.verkehr.tbx_VerkehrsmengenErmitteln import TbxVerkehrsmengenErmitteln
from rpctools.analyst.verkehr.tbx_routing import TbxRouting
from rpctools.analyst.verkehr.tbx_update_nodes import TbxUpdateNodes


class Toolbox(object):
    def __init__(self):
        self.label = u'Verkehr'
        self.alias = ''
        self.tools = [TbxRouting,
                      TbxUpdateNodes,
                      TbxBasisdatenbearbeiten,
                      TbxVerkehrsmengenErmitteln,
                      TbxRoutingsdurchfuehren]







