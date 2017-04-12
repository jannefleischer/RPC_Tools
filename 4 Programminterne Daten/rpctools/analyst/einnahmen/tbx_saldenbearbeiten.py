# -*- coding: utf-8 -*-

import arcpy
import os
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.Salden_bearbeiten import Salden_bearbeiten

class TbxSaldenbearbeiten(Tbx):
    """Toolbox Wanderungssalden für Einnahmen"""

    @property
    def label(self):
        return u'Schritt 1a: Einwohner-Salden bearbeiten'

    @property
    def Tool(self):
        return Salden_bearbeiten

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
        projects_wohnen = []

        for project in projects:
            table_teilflaechen = self.folders.get_table(tablename= 'Teilflaechen_Plangebiet', fgdb = "FGDB_Definition_Projekt.gdb", project = project)
            fields = "Nutzungsart"
            cursor = arcpy.da.SearchCursor(table_teilflaechen, fields)
            wohnen_exists = False

            for flaeche in cursor:
               if flaeche[0] == 1:
                     wohnen_exists = True

            if wohnen_exists == True:
                projects_wohnen.append(project)

        par.name.filter.list = projects_wohnen
        if projects_wohnen:
            par.name.value = projects_wohnen[0]
        else:
            par.name.filter.enabled = False
            par.name.value = None

        if par.name.altered and not par.name.hasBeenValidated:
            projektname = self.par.name.value
            gemeinden = []
            workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
            wanderungssalden = os.path.join(workspace_projekt_einnahmen, 'Wanderungssalden')
            fields = ["GEN", "Einw_Saldo"]
            cursor = arcpy.da.SearchCursor(wanderungssalden, fields)
            for gemeinde in cursor:
                gemeinden.append(gemeinde[0] + "  ||  EW-Saldo: " + str(gemeinde[1]))
            par.gemeinde.filter.list = sorted(gemeinden)
