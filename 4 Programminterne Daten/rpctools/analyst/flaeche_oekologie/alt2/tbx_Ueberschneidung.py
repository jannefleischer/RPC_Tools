# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.flaeche_oekologie.schutzwuerdigeBoedenTesten import Ueberschneidung

class TbxUeberschneidung(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 2: Auf Überschneidungen testen')

    @property
    def Tool(self):
        return Ueberschneidung

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        return params


    def _updateParameters(self, params):
		return

