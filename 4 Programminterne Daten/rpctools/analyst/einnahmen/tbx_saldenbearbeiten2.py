# -*- coding: utf-8 -*-

import arcpy
import os
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.Salden_bearbeiten2 import Salden_bearbeiten2

class TbxSaldenbearbeiten2(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 1b: Erwerbstätige-Salden bearbeiten'

    @property
    def Tool(self):
        return Salden_bearbeiten2

    def _getParameterInfo(self):

        par = self.par
        projects = self.folders.get_projects()

        # Projektname
        par.name = arcpy.Parameter()
        par.name.name = u'Projektname'
        par.name.displayName = u'Projektname'
        par.name.parameterType = 'Required'
        par.name.direction = 'Input'
        par.name.datatype = u'GPString'
        par.name.filter.list = projects

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

        projects = self.folders.get_projects()
        projects_gewerbe = []

        for project in projects:
            table_teilflaechen = self.folders.get_table(
                tablename='Teilflaechen_Plangebiet',
                workspace="FGDB_Definition_Projekt.gdb",
                project=project)
            fields = "Nutzungsart"
            cursor = arcpy.da.SearchCursor(table_teilflaechen, fields)
            gewerbe_exists = False

            for flaeche in cursor:
                if flaeche[0] == 2:
                    gewerbe_exists = True

            if gewerbe_exists == True:
                projects_gewerbe.append(project)

        par.name.filter.list = projects_gewerbe
        if projects_gewerbe:
            par.name.value = projects_gewerbe[0]
        else:
            par.name.filter.enabled = False
            par.name.value = None


        if par.name.altered and not par.name.hasBeenValidated:
            projektname = self.par.name.value
            gemeinden = []
            workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
            wanderungssalden = os.path.join(workspace_projekt_einnahmen, 'Wanderungssalden')
            fields = ["GEN", "SvB_Saldo"]
            cursor = arcpy.da.SearchCursor(wanderungssalden, fields)
            for gemeinde in cursor:
                gemeinden.append(gemeinde[0] + "  ||  EW-Saldo: " + str(gemeinde[1]))
            par.gemeinde.filter.list = sorted(gemeinden)
