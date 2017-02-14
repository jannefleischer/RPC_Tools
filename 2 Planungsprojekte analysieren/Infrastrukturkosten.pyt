# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.infrastrukturkosten import tbx_aufteilungsregeln
reload(tbx_aufteilungsregeln)
from rpctools.analyst.infrastrukturkosten import tbx_kostenermittlung
reload(tbx_kostenermittlung)

from rpctools.analyst.infrastrukturkosten.tbx_kostenermittlung import TbxInfrastrukturkostenermittlung
from rpctools.analyst.infrastrukturkosten.tbx_aufteilungsregeln import TbxKostenaufteilungsregeln

class Toolbox(object):
    def __init__(self):
        self.label = u'Infrastrukturkosten'
        self.alias = ''
        self.tools = [TbxInfrastrukturkostenermittlung,
                      TbxKostenaufteilungsregeln]