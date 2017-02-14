# -*- coding: utf-8 -*-
# reload
from rpctools.definitions.projektverwaltung import tbx_projektverwaltung
reload(tbx_projektverwaltung)
from rpctools.definitions.projektverwaltung import tbx_teilflaechen_benennen
reload(tbx_teilflaechen_benennen)

from rpctools.utils.encoding import encode

from rpctools.definitions.nutzungsart import (tbx_flaechenbilanz,
                                              tbx_nutzungen)
reload(tbx_flaechenbilanz)
reload(tbx_nutzungen)

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung \
     import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_benennen \
     import TbxTeilflaecheBenennen

from rpctools.definitions.nutzungsart.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.definitions.nutzungsart.tbx_nutzungen import TbxNutzungen


class Toolbox(object):
    def __init__(self):
        self.label = u'Projekte definieren'
        self.alias = ''
        self.tools = [TbxProjektVerwaltung,
                      TbxTeilflaecheBenennen,
                      TbxFlaechenbilanz,
                      TbxNutzungen]
