# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.flaeche_oekologie.script_Integrationsgrad import Integrationsgrad
from rpctools.analyst.flaeche_oekologie.script_Integrationsgrad import Integrationsgrad_loeschen
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.output import Output

class TbxIntegrationsgrad(Tbx):
    """Toolbox Integrationsgrad"""

    @property
    def label(self):
        return u' Integrationsgrad berechnen'

    @property
    def Tool(self):
        return Integrationsgrad

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

    def _updateParameters(self, params):
        par = self.par

    def grenzlinie_eintragen(self, polyline):

        table = self.folders.get_table("Grenze_Siedlungskoerper", "FGDB_Flaeche_und_Oekologie.gdb")
        cursor = arcpy.da.InsertCursor(table, ['SHAPE@'])
        cursor.insertRow([polyline])


class TbxIntegrationsgrad_loeschen(Tbx):
    """Toolbox TbxIntegrationsgrad_loeschen"""

    @property
    def label(self):
        return u' Integrationsgrad löschen'

    @property
    def Tool(self):
        return Integrationsgrad_loeschen

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

    def _updateParameters(self, params):
        par = self.par