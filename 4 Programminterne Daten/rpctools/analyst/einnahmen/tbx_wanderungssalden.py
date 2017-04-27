# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.constants import Nutzungsart
from rpctools.analyst.einnahmen.Wanderungssalden import Wanderungssalden

class TbxWanderungssalden(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 1: Wanderungssalden schätzen'

    @property
    def Tool(self):
        return Wanderungssalden

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

        return par

    def _updateMessages(self, params):
        par = self.par
        
        where = 'Nutzungsart = {} or Nutzungsart = {}'.format(
            Nutzungsart.WOHNEN, Nutzungsart.GEWERBE)
        
        rows = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb', 
                                where=where)        

        if not rows:
            par.name.setErrorMessage(u'In diesem Projekt sind weder Wohn- '
                                     u'noch Gewerbeflächen definiert!')
            
if __name__ == '__main__':
    t = TbxWanderungssalden()
    t.getParameterInfo()
    t.open()