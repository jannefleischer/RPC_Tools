# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.Steuersalden import Steuersalden

class TbxErgebnisinterpretation(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 2: Steuersalden schätzen'

    @property
    def Tool(self):
        return Steuersalden

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
        projects = self.folders.get_projects()
        projects_wohnen_gewerbe = []

        for project in projects:
            table_teilflaechen = self.folders.get_table(
                tablename='Teilflaechen_Plangebiet',
                workspace="FGDB_Definition_Projekt.gdb",
                project=project)
            fields = "Nutzungsart"
            cursor = arcpy.da.SearchCursor(table_teilflaechen, fields)
            wohnen_gewerbe_exists = False

            for flaeche in cursor:
                if flaeche[0] == 1 or flaeche[0] == 2:
                    wohnen_gewerbe_exists = True

            if wohnen_gewerbe_exists == True:
                projects_wohnen_gewerbe.append(project)

        par.name.filter.list = projects_wohnen_gewerbe
        if projects_wohnen_gewerbe:
            par.name.value = projects_wohnen_gewerbe[0]
        else:
            par.name.value = None
            par.name.filter.enabled = False