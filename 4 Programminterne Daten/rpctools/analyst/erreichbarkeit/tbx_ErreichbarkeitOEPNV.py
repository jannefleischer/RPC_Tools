# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.erreichbarkeit.T3_Erreichbarkeit_OEPNV import ErreichbarkeitOEPNV

class TbxErreichbarkeitOEPNV(Tbx):

    @property
    def label(self):
        return encode(u'Erreichbarkeit von OEPNV ermitteln')

    @property
    def Tool(self):
        return ErreichbarkeitOEPNV

    def _getParameterInfo(self):

		list_projects = project_lib.get_projects()
		list_projects = sorted(list_projects)
		#set project
		self.params[0].filter.list = list_projects

		#set Haltestellen
		self.params[1].filter.list = []
		self.params[2].filter.list = []
		self.params[3].filter.list = []

        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = []

        # Haltestelle1
        param_2 = arcpy.Parameter()
        param_2.name = u'Haltestelle1'
        param_2.displayName = u'Haltestelle1'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = language('string')

        # Haltestelle2
        param_3 = arcpy.Parameter()
        param_3.name = u'Haltestelle2'
        param_3.displayName = u'Haltestelle2'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = language('string')

        # Haltestelle3
        param_4 = arcpy.Parameter()
        param_4.name = u'Haltestelle3'
        param_4.displayName = u'Haltestelle3'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = language('string')

        parameters = [param_1, param_2, param_3, param_4]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()

        return parameters


    def _updateParameters(self, params):

		#Projekt ausw�hlen
		if self.params[0].altered and not self.params[0].hasBeenValidated:
			projectname = self.params[0].value
			self.params[1].value = ""
			self.params[2].value = ""
			self.params[3].value = ""
			path_Halte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Erreichbarkeit.gdb','OEPNV_Haltestellen')

			rows_Halte = arcpy.SearchCursor(path_Halte)
			list_Halte1 = []
			list_Halte2 = []
			list_Halte3 = []
			for row in rows_Halte:
				list_Halte1.append(row.Name + " | " + str(row.Distanz) + "m entfernt")
				list_Halte2.append(row.Name + " | " + str(row.Distanz) + "m entfernt")
				list_Halte3.append(row.Name + " | " + str(row.Distanz) + "m entfernt")

			list_Halte1 = sorted(list(set(list_Halte1)))
			list_Halte2 = sorted(list(set(list_Halte2)))
			list_Halte3 = sorted(list(set(list_Halte3)))

			self.params[1].filter.list = list_Halte1
			self.params[2].filter.list = list_Halte2
			self.params[3].filter.list = list_Halte3

		#Haltestellen ausw�hlen
		if self.params[1].altered and not self.params[1].hasBeenValidated:

			projectname = self.params[0].value
			Halte1 = (self.params[1].value)

		if self.params[2].altered and not self.params[2].hasBeenValidated:

			projectname = self.params[0].value
			Halte2 = (self.params[2].value)

		if self.params[3].altered and not self.params[3].hasBeenValidated:

			projectname = self.params[0].value
			Halte3 = (self.params[3].value)

		return
