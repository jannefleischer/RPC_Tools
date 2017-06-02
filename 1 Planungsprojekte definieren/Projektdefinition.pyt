# -*- coding: utf-8 -*-
# reload
import sys

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten \
     import TbxTeilflaecheVerwalten

from rpctools.definitions.nutzungsart.tbx_nutzungen import (
    TbxNutzungenWohnen, TbxNutzungenGewerbe, TbxNutzungenEinzelhandel)


class Toolbox(object):
    def __init__(self):
        self.label = u'Projekte definieren'
        self.alias = ''
        self.tools = [TbxTeilflaecheVerwalten,
                      TbxNutzungenWohnen,
                      TbxNutzungenGewerbe,
                      TbxNutzungenEinzelhandel]