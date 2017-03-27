# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.erreichbarkeit.T2_Zentrale_Orte_OEPNV_Abfrage import ZentraleOrteOEPNV

class TbxZentraleOrteOEPNV(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 3: Zentrale Orte ÖPNV')

    @property
    def Tool(self):
        return ZentraleOrteOEPNV

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()


        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        # Ziel_1
        param_2 = params.ziel1 = arcpy.Parameter()
        param_2.name = u'Ziel_1'
        param_2.displayName = u'Ziel 1'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'
        param_2.filter.list = []


        # Ziel_2
        param_3 = params.ziel2 = arcpy.Parameter()
        param_3.name = u'Ziel_2'
        param_3.displayName = u'Ziel 2'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = u'GPString'
        param_3.filter.list = []

        # Ziel_3
        param_4 = params.ziel4 = arcpy.Parameter()
        param_4.name = u'Ziel_3'
        param_4.displayName = u'Ziel 3'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'GPString'
        param_4.filter.list = []

        return params


    def _updateParameters(self, params):

		#Projekt ausw�hlen
		if self.params[0].altered and not self.params[0].hasBeenValidated:
			projectname = self.params[0].value
			self.params[1].value = ""
			self.params[2].value = ""
			self.params[3].value = ""
			path_Orte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,
									 'FGDB_Erreichbarkeit.gdb',
									 'Zentrale_Orte_75km')

			rows_Orte = arcpy.SearchCursor(path_Orte)
			list_Ort1 = []
			list_Ort2 = []
			list_Ort3 = []
			for row in rows_Orte :
				list_Ort1.append(row.Name)
				list_Ort2.append(row.Name)
				list_Ort3.append(row.Name)

			list_Ort1 = sorted(list(set(list_Ort1)))
			list_Ort2 = sorted(list(set(list_Ort2)))
			list_Ort3 = sorted(list(set(list_Ort3)))

			self.params[1].filter.list = list_Ort1
			self.params[2].filter.list = list_Ort2
			self.params[3].filter.list = list_Ort3

		#Orte ausw�hlen
		if self.params[1].altered and not self.params[1].hasBeenValidated:

			projectname = self.params[0].value
			Ort1 = self.params[1].value

		if self.params[2].altered and not self.params[2].hasBeenValidated:

			projectname = self.params[0].value
			Ort2 = self.params[2].value

		if self.params[3].altered and not self.params[3].hasBeenValidated:

			projectname = self.params[0].value
			Ort3 = self.params[3].value

		return

