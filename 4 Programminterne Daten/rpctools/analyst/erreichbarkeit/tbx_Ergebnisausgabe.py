# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.erreichbarkeit.T5_Ergebnissammler import Ergebnisausgabe

class TbxErgebnisausgabe(Tbx):

    @property
    def label(self):
        return encode(u'Ergebnisse exportieren')

    @property
    def Tool(self):
        return Ergebnisausgabe

    def _getParameterInfo(self):

        params = self.par
    	projekte = self.folders.get_projects()


        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        return params

    def _updateParameters(self, params):
		return

