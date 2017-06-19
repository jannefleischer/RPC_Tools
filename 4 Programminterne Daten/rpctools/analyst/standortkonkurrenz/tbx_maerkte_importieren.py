# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil
import re

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.analyst.standortkonkurrenz.market_templates import MarketTemplate
from rpctools.analyst.standortkonkurrenz.tbx_osm_markteinlesen import MarktEinlesen


class MaerkteImportieren(MarktEinlesen):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
    
    def run(self):
        path, filename = os.path.split(self.par.filepath)
        name, ext = os.path.splitext(filename) 
        idx = MarketTemplate.template_types.values().index(ext)
        template_type = MarketTemplate.template_types.keys()[idx]
        template = MarketTemplate(template_type, path, filename=filename,
                                  epsg=self.parent_tbx.config.epsg)
        markets = template.get_markets()
        self.markets_to_db(markets)
        print()


class TbxMaerkteImportieren(Tbx):

    @property
    def label(self):
        return encode(u'Marktstandorte aus Datei importieren')

    @property
    def Tool(self):
        return MaerkteImportieren

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []

        param = self.add_parameter('filepath')
        param.name = encode(u'Datei')
        param.displayName = encode(u'Datei')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'DEFile'
        #param.filter.type = 'File'
        param.filter.list = MarketTemplate.template_types.values()
        #param.value = 1000

        return params

    def _updateParameters(self, params):

        return params


if __name__ == '__main__':
    t = TbxMaerkteImportieren()
    t._getParameterInfo()
    t.par.filepath = r'C:\Users\ggr\Desktop\maerkte.csv'
    t.set_active_project()
    t.execute()
