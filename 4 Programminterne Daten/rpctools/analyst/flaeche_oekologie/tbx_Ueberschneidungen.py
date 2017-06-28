# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.flaeche_oekologie.script_Ueberschneidungen import Ueberschneidungen
from rpctools.utils.constants import Nutzungsart

class TbxUeberschneidungen(Tbx):
    """Toolbox Ueberschneidungen"""

    @property
    def label(self):
        return u'Ueberschneidungen anzeigen'

    @property
    def Tool(self):
        return Ueberschneidungen

    def _getParameterInfo(self):

        par = self.par

        # Projektname
        par.name = arcpy.Parameter()
        par.name.name = u'Projektname'
        par.name.displayName = u'Projektname'
        par.name.parameterType = 'Required'
        par.name.direction = 'Input'
        par.name.datatype = u'GPString'
        par.name.filter.list = []

        par.label = arcpy.Parameter()
        par.label.name = u'Label'
        par.label.displayName = u'Label'
        par.label.parameterType = 'Required'
        par.label.direction = 'Input'
        par.label.datatype = u'Double'
        par.label.value = 0


        return par

    def _updateParameters(self, params):
        par = self.par


class TbxLayerWald(TbxUeberschneidungen):

    def _updateParameters(self, params):
        par = self.par
        if par.name.altered and not par.name.hasBeenValidated:
            par.label.value = 1

class TbxLayerNatur(TbxUeberschneidungen):

    def _updateParameters(self, params):
        par = self.par
        if par.name.altered and not par.name.hasBeenValidated:
            par.label.value = 2

class TbxLayerLandschaft(TbxUeberschneidungen):

    def _updateParameters(self, params):
        par = self.par
        if par.name.altered and not par.name.hasBeenValidated:
            par.label.value = 3

class TbxLayerWasser(TbxUeberschneidungen):

    def _updateParameters(self, params):
        par = self.par
        if par.name.altered and not par.name.hasBeenValidated:
            par.label.value = 4