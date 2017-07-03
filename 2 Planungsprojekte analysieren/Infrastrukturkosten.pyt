# -*- coding: utf-8 -*-

from rpctools.analyst.infrastrukturkosten.tbx_kostenermittlung import \
     TbxInfrastrukturkostenermittlung
from rpctools.analyst.infrastrukturkosten.tbx_aufteilungsregeln import \
     TbxKostenaufteilungsregeln
from rpctools.analyst.infrastrukturkosten.tbx_flaechenbilanz import \
     TbxFlaechenbilanz
from rpctools.analyst.infrastrukturkosten.tbx_massnahmen_editieren import \
     TbxMassnahmenEditieren
from rpctools.analyst.infrastrukturkosten.tbx_infrastrukturmengenbilanz import \
     TbxInfrastrukturmengenBilanz
from rpctools.analyst.infrastrukturkosten.tbx_kostenkennwerte_kontrollieren \
     import TbxKostenkennwerteKontrollieren


class Toolbox(object):
    def __init__(self):
        self.label = u'Infrastrukturkosten'
        self.alias = ''
        self.tools = [TbxMassnahmenEditieren,
                      TbxInfrastrukturmengenBilanz,
                      TbxFlaechenbilanz,
                      TbxInfrastrukturkostenermittlung,
                      TbxKostenaufteilungsregeln,
                      TbxKostenkennwerteKontrollieren]