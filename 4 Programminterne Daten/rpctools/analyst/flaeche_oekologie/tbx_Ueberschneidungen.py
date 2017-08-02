# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.flaeche_oekologie.script_Ueberschneidungen import Ueberschneidungen
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.params import Tool

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

        # Projektname
        par.layer_number = arcpy.Parameter()
        par.layer_number.name = u'layer_number'
        par.layer_number.displayName = u'layer_number'
        par.layer_number.parameterType = 'Required'
        par.layer_number.datatype = u'GPLong'
        par.layer_number.value = 0

        return par


class TbxLayerWald(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerWald, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 1
        return par

class TbxLayerNatur(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerNatur, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 2
        return par

class TbxLayerLandschaft(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerLandschaft, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 3
        return par

class TbxLayerWasser(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerWasser, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 4
        return par

class TbxLayerFreiraum(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerFreiraum, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 5
        return par

class TbxLayerBodenversiegelung(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerBodenversiegelung, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 6
        return par

class TbxLayerHochspannung(TbxUeberschneidungen):

    def _getParameterInfo(self):
        super(TbxLayerHochspannung, self)._getParameterInfo()
        par = self.par
        par.layer_number.value = 7
        return par