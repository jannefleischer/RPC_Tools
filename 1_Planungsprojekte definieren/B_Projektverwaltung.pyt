# -*- coding: utf-8 -*-

# reload
from rpctools.definitions.projektverwaltung import tbx_projektverwaltung
reload(tbx_projektverwaltung)
from rpctools.definitions.projektverwaltung import tbx_teilflaechen_benennen
reload(tbx_teilflaechen_benennen)

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung \
     import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_benennen \
     import TbxTeilflaecheBenennen


class Toolbox(object):
    def __init__(self):
        self.label = u'Projektverwaltung'
        self.alias = ''
        self.tools = [TbxTeilflaecheBenennen,
                      TbxProjektVerwaltung]
