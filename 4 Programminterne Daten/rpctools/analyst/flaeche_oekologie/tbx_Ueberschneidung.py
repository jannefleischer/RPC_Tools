# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.flaeche_oekologie.schutzwuerdigeBoedenTesten import Ueberschneidung

class TbxUeberschneidung(Tbx):

    @property
    def label(self):
        return encode(u'Auf Überschneidungen testen')

    @property
    def Tool(self):
        return Ueberschneidung

    def _getParameterInfo(self):

    	list_projects = project_lib.get_projects()
    	list_projects = sorted(list_projects)

    	i=-1

    	#set project
    	i+=1 ; self.params[i].filter.list = list_projects

        # Projekt
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = []

        parameters = [param_1]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()
        return parameters


    def _updateParameters(self, params):
		return

