# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.analyst.bewohner_arbeitsplaetze.bewohner import Bewohner
from rpctools.utils.constants import Nutzungsart


class TbxBewohner(TbxFlaechendefinition):
    _nutzungsart = Nutzungsart.WOHNEN
    
    @property
    def Tool(self):
        return Bewohner

    @property
    def label(self):
        return u'Bewohnerzahl schätzen'
    
if __name__ == '__main__':
    t = TbxBewohner()
    params = t.getParameterInfo()
    t.par.projectname.value = t.config.active_project
    t.tool.main(t.par, None)