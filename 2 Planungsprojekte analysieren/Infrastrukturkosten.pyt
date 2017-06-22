# -*- coding: utf-8 -*-

from rpctools.analyst.infrastrukturkosten.tbx_kostenermittlung import \
     TbxInfrastrukturkostenermittlung
from rpctools.analyst.infrastrukturkosten.tbx_aufteilungsregeln import \
     TbxKostenaufteilungsregeln
from rpctools.analyst.infrastrukturkosten.tbx_flaechenbilanz import \
     TbxFlaechenbilanz
from rpctools.analyst.infrastrukturkosten.tbx_massnahmen_beschreiben import \
     TbxMassnahmenBeschreiben
from rpctools.analyst.infrastrukturkosten.tbx_infrastrukturmengenbilanz import \
     TbxInfrastrukturmengenBilanz


class Toolbox(object):
    def __init__(self):
        self.label = u'Infrastrukturkosten'
        self.alias = ''
        self.tools = [TbxMassnahmenBeschreiben,
                      TbxInfrastrukturmengenBilanz, 
                      TbxFlaechenbilanz,
                      TbxInfrastrukturkostenermittlung,
                      TbxKostenaufteilungsregeln]