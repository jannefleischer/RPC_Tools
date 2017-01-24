# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.T5_Gewerbesteuer import Gewerbesteuer


class TbxGewerbesteuer(Tbx):
    """Toolbox Gewerbesteuer"""

    @property
    def label(self):
        return u'5 Gewerbesteuer'

    @property
    def Tool(self):
        return Gewerbesteuer

    def _getParameterInfo(self):

        params = self.par
        # Projektname
        param_1 = params.name = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Hebesatz_als_vH_Satz
        param_2 = params.hebesatz = arcpy.Parameter()
        param_2.name = u'Hebesatz_als_vH_Satz'
        param_2.displayName = u'Hebesatz als vH Satz'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        return params
