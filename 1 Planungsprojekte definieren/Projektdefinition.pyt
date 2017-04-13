# -*- coding: utf-8 -*-
# reload
import sys
#sys.dont_write_bytecode=True
#import wingdbstub

from rpctools.definitions.projektverwaltung import tbx_teilflaechen_verwalten
reload(tbx_teilflaechen_verwalten)


from rpctools.definitions.nutzungsart import (tbx_flaechenbilanz,
                                              tbx_nutzungen)
reload(tbx_flaechenbilanz)
reload(tbx_nutzungen)

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten \
     import TbxTeilflaecheVerwalten

#from rpctools.definitions.nutzungsart.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.definitions.nutzungsart.tbx_nutzungen import (
    TbxNutzungenWohnen, TbxNutzungenGewerbe, TbxNutzungenEinzelhandel)


class Toolbox(object):
    def __init__(self):
        self.label = u'Projekte definieren'
        self.alias = ''
        self.tools = [TbxTeilflaecheVerwalten,
                      #TbxFlaechenbilanz,
                      TbxNutzungenWohnen,
                      TbxNutzungenGewerbe,
                      TbxNutzungenEinzelhandel]