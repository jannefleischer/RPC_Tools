# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.T1_Vorberechnungen import Vorberechnungen


class TbxVorberechnungen(Tbx):
    """Toolbox Vorberechnungen für Einnahmen"""

    @property
    def label(self):
        return u'1 Vorberechnungen'

    @property
    def Tool(self):
        return Vorberechnungen

    def _getParameterInfo(self):
         
        par = self.par
        # Projektname
        par.name = arcpy.Parameter()
        par.name.name = u'Projektname'
        par.name.displayName = u'Projektname'
        par.name.parameterType = 'Required'
        par.name.direction = 'Input'
        par.name.datatype = u'Zeichenfolge'
        par.name.filter.list = []

        heading = "01 Nettozuzugsquoten (in %)"

        # Nettozuzugsquote_Einwohner
        par.nettozuzugquote_ew = arcpy.Parameter()
        par.nettozuzugquote_ew.name = u'Nettozuzugsquote_Einwohner'
        par.nettozuzugquote_ew.displayName = u'Nettozuzugsquote Einwohner'
        par.nettozuzugquote_ew.parameterType = 'Required'
        par.nettozuzugquote_ew.direction = 'Input'
        par.nettozuzugquote_ew.datatype = u'Long'
        par.nettozuzugquote_ew.value = 50
        par.nettozuzugquote_ew.filter.type = 'Range'
        par.nettozuzugquote_ew.filter.list = [0, 100]
        par.nettozuzugquote_ew.category = heading

        # Nettozuzugsquote_Arbeitsplätze
        par.nettozuzugquote_jobs = arcpy.Parameter()
        par.nettozuzugquote_jobs.name = encode(u'Nettozuzugsquote_Arbeitsplätze')
        par.nettozuzugquote_jobs.displayName = encode(u'Nettozuzugsquote Arbeitsplätze')
        par.nettozuzugquote_jobs.parameterType = 'Required'
        par.nettozuzugquote_jobs.direction = 'Input'
        par.nettozuzugquote_jobs.datatype = u'Long'
        par.nettozuzugquote_jobs.value = 50
        par.nettozuzugquote_jobs.filter.type = 'Range'
        par.nettozuzugquote_jobs.filter.list = [0, 100]
        par.nettozuzugquote_jobs.category = heading

        heading = "02 Einzugsbereich (in km)"

        # Einzugsbereich_Einwohner
        par.einzugsbereich_ew = arcpy.Parameter()
        par.einzugsbereich_ew.name = u'Einzugsbereich_Einwohner'
        par.einzugsbereich_ew.displayName = u'Einzugsbereich Einwohner'
        par.einzugsbereich_ew.parameterType = 'Required'
        par.einzugsbereich_ew.direction = 'Input'
        par.einzugsbereich_ew.datatype = u'Long'
        par.einzugsbereich_ew.value = 25
        par.einzugsbereich_ew.filter.type = 'Range'
        par.einzugsbereich_ew.filter.list = [0, 50]
        par.einzugsbereich_ew.category = heading

        # Einzugsbereich_Arbeitsplätze
        par.einzugsbereich_jobs = arcpy.Parameter()
        par.einzugsbereich_jobs.name = encode(u'Einzugsbereich_Arbeitsplätze')
        par.einzugsbereich_jobs.displayName = encode(u'Einzugsbereich Arbeitsplätze')
        par.einzugsbereich_jobs.parameterType = 'Required'
        par.einzugsbereich_jobs.direction = 'Input'
        par.einzugsbereich_jobs.datatype = u'Long'
        par.einzugsbereich_jobs.value = 25
        par.einzugsbereich_jobs.filter.type = 'Range'
        par.einzugsbereich_jobs.filter.list = [0, 50]
        par.einzugsbereich_jobs.category = heading

        return par
