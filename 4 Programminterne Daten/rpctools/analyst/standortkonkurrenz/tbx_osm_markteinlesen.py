# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode

from rpctools.analyst.standortkonkurrenz.T1_Lebensmittelmaerkte_einlesen \
     import MarktEinlesen

class OSMMarktEinlesen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte'

class TbxOSMMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 1: Märkte einlesen')

    @property
    def Tool(self):
        return MarktEinlesen

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


