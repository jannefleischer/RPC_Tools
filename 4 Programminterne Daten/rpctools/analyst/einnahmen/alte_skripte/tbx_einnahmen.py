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
    """
    Toolbox mit nur dem Parameter *name*
    """

    def _getParameterInfo(self):
        # Projektname
        params = self.par
        projekte = self.folders.get_projects()

        param_1 = params.name = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        return params


class TbxEinkommenssteuer(_TbxEinnahmen):
    """Toolbox Einkommenssteuer"""

    @property
    def label(self):
        return u'Schritt 2: Einkommensteuer'

    @property
    def Tool(self):
        return Einkommenssteuer


class TbxFamilienleistungsausgleich(_TbxEinnahmen):
    """Toolbox Familienleistungsausgleich"""

    @property
    def label(self):
        return u'Schritt 5: Familienleistungsausgleich'

    @property
    def Tool(self):
        return Familienleistungsausgleich


class TbxKFA(_TbxEinnahmen):
    """Toolbox Kommunaler Finanzausgleich"""

    @property
    def label(self):
        return u'Schritt 6: Kommunaler Finanzausgleich'

    @property
    def Tool(self):
        return KFA


class TbxKRU(_TbxEinnahmen):
    """Toolbox Kreisumlage"""

    @property
    def label(self):
        return u'Schritt 7: Kreisumlage'

    @property
    def Tool(self):
        return KRU
