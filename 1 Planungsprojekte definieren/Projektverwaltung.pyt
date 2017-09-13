# -*- coding: utf-8 -*-
# reload
import sys
#sys.dont_write_bytecode=True
#import wingdbstub

from rpctools.definitions.projektverwaltung import (tbx_projektverwaltung,
                                                    tbx_projektauswahl)
reload(tbx_projektverwaltung)
reload(tbx_projektauswahl)

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung import \
     TbxProjekteLoeschen, TbxProjektAnlegen, TbxProjektKopieren

from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl
from rpctools.definitions.projektpfad.tbx_projektpfad import TbxProjectFolder



class Toolbox(object):
    def __init__(self):
        self.label = u'Projekte verwalten'
        self.alias = ''
        self.tools = [TbxProjektAnlegen,
                      TbxProjektKopieren,
                      TbxProjekteLoeschen,
                      TbxProjektauswahl,
                      TbxProjectFolder,
                      ]
