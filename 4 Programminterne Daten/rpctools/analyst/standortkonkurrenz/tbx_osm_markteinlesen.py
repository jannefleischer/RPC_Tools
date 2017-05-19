# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode


class OSMMarktEinlesen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte'
    
    def run(self):
        pass


class TbxOSMMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'Marktstandorte online aus OpenStreetMap abfragen')

    @property
    def Tool(self):
        return OSMMarktEinlesen

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = params.projectname = arcpy.Parameter()
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = []

        return params

    def _updateParameters(self, params):   

        return params


if __name__ == '__main__':
    t = TbxOSMMarktEinlesen()
    t._getParameterInfo()
    t.set_active_project()
    t.execute()
