# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.standortkonkurrenz.T5_StandortkonkurrenzSupermaerkteTool import Standortkonkurrenz

class TbxStandortkonkurrenz(Tbx):

    @property
    def label(self):
        return encode(u'Standortkonkurrenz berechnen')

    @property
    def Tool(self):
        return Standortkonkurrenz

    def _getParameterInfo(self):

    	list_projects = project_lib.get_projects()
    	list_projects = sorted(list_projects)

    	i = 0
    	self.params[i].filter.list = list_projects
    	self.Projekt= i
    	i+=1
    	self.Maerkteshp = i
    	i+=1
    	self.Siedlungsshp = i

        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = []

        parameters = [param_1]

        validator = getattr(self, 'ToolValidator', None)
        if validator:
            validator(parameters).initializeParameters()

        self.updateParameters(parameters)

        return parameters


    def _updateParameters(self, params):
		return


