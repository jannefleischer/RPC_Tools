# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.standortkonkurrenz import tbx_definitionZentren
reload(tbx_definitionZentren)
from rpctools.analyst.standortkonkurrenz import tbx_marktEinlesen
reload(tbx_marktEinlesen)
from rpctools.analyst.standortkonkurrenz import tbx_marktHinzufuegen
reload(tbx_marktHinzufuegen)
from rpctools.analyst.standortkonkurrenz import tbx_standortkonkurrenz
reload(tbx_standortkonkurrenz)
from rpctools.analyst.standortkonkurrenz import tbx_zentrenBearbeiten
reload(tbx_zentrenBearbeiten)

from rpctools.analyst.standortkonkurrenz.tbx_definitionZentren import TbxDefinitionZentren
from rpctools.analyst.standortkonkurrenz.tbx_marktEinlesen import TbxMarktEinlesen
from rpctools.analyst.standortkonkurrenz.tbx_marktHinzufuegen import TbxMarktHinzufuegen
from rpctools.analyst.standortkonkurrenz.tbx_standortkonkurrenz import TbxStandortkonkurrenz
from rpctools.analyst.standortkonkurrenz.tbx_zentrenBearbeiten import TbxZentrenBearbeitenn

class Toolbox(object):
    def __init__(self):
        self.label = u'standortkonkurrenz'
        self.alias = ''
        self.tools = [TbxMarktEinlesen,
                      TbxMarktHinzufuegen,
					  TbxDefinitionZentren,
					  TbxZentrenBearbeitenn,
					  TbxStandortkonkurrenz]
















