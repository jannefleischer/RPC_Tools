# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode


class EditMarkets(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def run(self):
        pass


class TbxEditMarkets(Tbx):

    @property
    def label(self):
        return encode(u'Märkte editieren')

    @property
    def Tool(self):
        return EditMarkets

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
    
        param = self.add_parameter('market')
        param.name = encode(u'Markt')
        param.displayName = encode(u'Markt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []

        return params
    
    def open(self):
        # ToDo: add markets
        pass

    def _updateParameters(self, params):

        return params


if __name__ == '__main__':
    t = TbxEditMarkets()
    t._getParameterInfo()
    t.set_active_project()
    t.execute()
