# -*- coding: utf-8 -*-
# reload
import sys
#sys.dont_write_bytecode=True
#import wingdbstub

from rpctools.definitions.projektverwaltung import (tbx_projektverwaltung, 
                                                    tbx_projektauswahl)
reload(tbx_projektverwaltung)
reload(tbx_projektauswahl)

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung \
     import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_projektauswahl \
     import TbxProjektauswahl


class Toolbox(object):
    def __init__(self):
        self.label = u'Projekte verwalten'
        self.alias = ''
        self.tools = [TbxProjektauswahl, TbxProjektVerwaltung]
