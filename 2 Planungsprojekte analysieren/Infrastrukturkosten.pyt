# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.infrastrukturkosten import tbx_aufteilungsregeln
reload(tbx_aufteilungsregeln)
from rpctools.analyst.infrastrukturkosten import tbx_kostenermittlung
reload(tbx_kostenermittlung)
from rpctools.analyst.infrastrukturkosten import tbx_flaechenbilanz
reload(tbx_flaechenbilanz)
from rpctools.analyst.infrastrukturkosten import tbx_massnahme_beschreiben
reload(tbx_massnahme_beschreiben)

from rpctools.analyst.infrastrukturkosten.tbx_kostenermittlung import TbxInfrastrukturkostenermittlung
from rpctools.analyst.infrastrukturkosten.tbx_aufteilungsregeln import TbxKostenaufteilungsregeln
from rpctools.analyst.infrastrukturkosten.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.analyst.infrastrukturkosten.tbx_massnahme_beschreiben import TbxMassnahmeBeschreiben


class Toolbox(object):
    def __init__(self):
        self.label = u'Infrastrukturkosten'
        self.alias = ''
        self.tools = [TbxMassnahmeBeschreiben,
                      TbxFlaechenbilanz,
                      TbxInfrastrukturkostenermittlung,
                      TbxKostenaufteilungsregeln]