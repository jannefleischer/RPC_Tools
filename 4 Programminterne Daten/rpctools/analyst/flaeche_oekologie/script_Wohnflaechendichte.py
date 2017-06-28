# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.script_Gewerbesteuer_kontrollieren import HebesaetzeKontrolle
from rpctools.utils.constants import Nutzungsart

class TbxWohnflaeche(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Wohnflächendichte vergleichen'

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

        par.hebesatz = arcpy.Parameter()
        par.hebesatz.name = u'Hebesatz'
        par.hebesatz.displayName = u'Hebesatz für die Gewerbesteuer (von-Hundert-Satz)'
        par.hebesatz.parameterType = 'Required'
        par.hebesatz.direction = 'Input'
        par.hebesatz.datatype = u'GPLong'
        par.hebesatz.filter.type = 'Range'
        par.hebesatz.filter.list = [100, 600]
        par.hebesatz.value = 250

        return par

    def _updateParameters(self, params):
        par = self.par

        cursor = self.query_table(table_name = 'Chronik_Nutzung',
                                columns = ['Arbeitsschritt', 'Letzte_Nutzung'],
                                workspace='FGDB_Einnahmen.gdb')
        for row in cursor:
            if row[0] == u"Wanderung Beschäftigte" and row[1] is None:
                par.name.setErrorMessage(u'Es wurden noch keine Wanderungssalden für Beschäftigte berechnet!')

        where = 'Nutzungsart = {} or Nutzungsart = {}'.format(Nutzungsart.WOHNEN, Nutzungsart.EINZELHANDEL)
        if par.changed('name'):
            where = 'Nutzungsart = {} or Nutzungsart = {}'.format(Nutzungsart.WOHNEN, Nutzungsart.EINZELHANDEL)
            rows = self.query_table('Teilflaechen_Plangebiet',
                                    ['Nutzungsart'],
                                    workspace='FGDB_Definition_Projekt.gdb',
                                    where=where)
            if not rows:
                par.name.setErrorMessage(u'In diesem Projekt sind keine Gewerbe- oder Einzelhandelsflächen definiert!')
                par.gemeinde.enabled = False
                par.gemeinde.filter.list = []
                par.gemeinde.value = (u'Projekt enthält keine Flächen mit der '
                                      u'benötigten Nutzungsart')
            else:
                par.gemeinde.enabled = True
                gemeinden = []
                fields = ["GEN", "Hebesatz_GewSt"]
                rows = self.query_table('Gemeindebilanzen', fields,
                                        workspace='FGDB_Einnahmen.gdb')
                for gem_name, hebesteuer in rows:
                    gemeinden.append(u"{} || Hebesatz: {}".format(
                        gem_name, hebesteuer))
                par.gemeinde.filter.list = sorted(gemeinden)