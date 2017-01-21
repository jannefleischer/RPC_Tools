# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.T2_Einkommensteuer import Einkommenssteuer
from rpctools.analyst.einnahmen.T3_Familienleistungsausgleich \
     import Familienleistungsausgleich
from rpctools.analyst.einnahmen.T6_KFA import KFA
from rpctools.analyst.einnahmen.T7_KRU import KRU


class _TbxEinnahmen(Tbx):
    """Toolbox to name Teilflächen"""

    def getParameterInfo(self):
        # Projektname
        params = self.par
        projekte = self.folders.get_projects()

        param_1 = params.name = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        return params


class TbxEinkommenssteuer(_TbxEinnahmen):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'2 Einkommensteuer'

    @property
    def Tool(self):
        return Einkommenssteuer


class TbxFamilienleistungsausgleich(_TbxEinnahmen):
    @property
    def label(self):
        return u'3 Familienleistungsausgleich'

    @property
    def Tool(self):
        return Familienleistungsausgleich


class TbxKFA(_TbxEinnahmen):
    @property
    def label(self):
        return u'6 Kommunaler Finanzausgleich'

    @property
    def Tool(self):
        return KFA


class TbxKRU(_TbxEinnahmen):
    @property
    def label(self):
        return u'7 Kreisumlage'

    @property
    def Tool(self):
        return KRU
