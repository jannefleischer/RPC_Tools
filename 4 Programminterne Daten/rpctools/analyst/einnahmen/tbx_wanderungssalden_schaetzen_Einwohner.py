# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.constants import Nutzungsart
from rpctools.analyst.einnahmen.script_Wanderungssalden_schaetzen_Einwohner import Wanderungssalden1


class TbxWanderungssalden1(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 1: Wanderungssalden Einwohner schätzen'

    @property
    def Tool(self):
        return Wanderungssalden1

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

        where = 'Nutzungsart = {}'.format(
            Nutzungsart.WOHNEN)

        rows = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb',
                                where=where)

        if not rows:
            par.name.setErrorMessage(u'In diesem Projekt sind keine Wohnflächen definiert!')

if __name__ == '__main__':
    t = TbxWanderungssalden1()
    t.getParameterInfo()
    t.set_active_project()
    t.show_outputs()
    t.open()