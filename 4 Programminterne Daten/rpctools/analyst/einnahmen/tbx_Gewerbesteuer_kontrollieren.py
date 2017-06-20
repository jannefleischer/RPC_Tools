# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.script_Gewerbesteuer_kontrollieren import HebesaetzeKontrolle
from rpctools.utils.constants import Nutzungsart

class TbxKontrolleGewerbesteuer(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 6: Hebesätze kontrollieren'

    @property
    def Tool(self):
        return HebesaetzeKontrolle

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

        par.gemeinde = arcpy.Parameter()
        par.gemeinde.name = u'Gemeinde'
        par.gemeinde.displayName = u'Gemeinden'
        par.gemeinde.parameterType = 'Required'
        par.gemeinde.direction = 'Input'
        par.gemeinde.datatype = u'GPString'
        par.gemeinde.filter.list = []

        par.saldo = arcpy.Parameter()
        par.saldo.name = u'Saldo'
        par.saldo.displayName = u'Saldo'
        par.saldo.parameterType = 'Required'
        par.saldo.direction = 'Input'
        par.saldo.datatype = u'GPLong'

        return par

    def _updateParameters(self, params):
        par = self.par
        if par.changed('name'):
            where = 'Nutzungsart = {}'.format(self._nutzungsart)
            rows = self.query_table('Teilflaechen_Plangebiet',
                                    ['Nutzungsart'],
                                    workspace='FGDB_Definition_Projekt.gdb',
                                    where=where)
            if not rows:
                par.gemeinde.enabled = False
                par.gemeinde.filter.list = []
                par.gemeinde.value = (u'Projekt enthält keine Flächen mit der '
                                      u'benötigten Nutzungsart')
            else:
                par.gemeinde.enabled = True
                gemeinden = []
                fields = ["GEN", self._saldo_field]
                rows = self.query_table('Gemeindebilanzen', fields,
                                        workspace='FGDB_Einnahmen.gdb')
                for gem_name, saldo in rows:
                    gemeinden.append(u"{} || Saldo: {}".format(
                        gem_name, saldo))
                par.gemeinde.filter.list = sorted(gemeinden)
