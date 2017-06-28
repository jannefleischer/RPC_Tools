# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.flaeche_oekologie.oekologische_folgen import OekologischeFolgen

class TbxOekologischeFolgen(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 4: Ökologische Folgen berechnen')

    @property
    def Tool(self):
        return OekologischeFolgen

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



        return params



    def _updateParameters(self, params):

        i=0

        return


