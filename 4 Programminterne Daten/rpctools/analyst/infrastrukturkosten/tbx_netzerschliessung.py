# -*- coding: utf-8 -*-
import arcpy
from rpctools.utils.params import Tbx
from rpctools.utils.params import Tool
from rpctools.utils.encoding import encode
from rpctools.utils.basetable_definitions import (Netzarten)


class NetzAnlegen(Tool):

    def run(self):
        pass

class TbxNetzAnlegenTbx(Tbx):
    @property
    def label(self):
        return encode(u'Schritt ?: Erschliessungsnetz anlegen')

    @property
    def Tool(self):
        return NetzAnlegen
    
    def __init__(self):
        super(TbxNetzAnlegenTbx, self).__init__()
        self.netzarten = Netzarten(self.folders)

    def _getParameterInfo(self):
        params = self.par
        
        # Was_wollen_Sie_tun_
        param = params.action = arcpy.Parameter()
        param.name = u'Was_wollen_Sie_tun_'
        param.displayName = u'Was wollen Sie tun?'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = self.netzarten.values()
        param.value = param.filter.list[0]

    def _updateParameters(self, params):
        return params