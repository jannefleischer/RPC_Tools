# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode

from rpctools.analyst.verkehr.routing import Routing


class TbxRouting(Tbx):

    @property
    def label(self):
        return encode(u'Routing')

    @property
    def Tool(self):
        return Routing

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        p = self.add_parameter('project')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt auswählen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'

        p.filter.list = projekte
        if projekte:
            p.value = projekte[0]


        # outer radius
        p = self.add_parameter('outer')
        p.name = u'outer_circle'
        p.displayName = u'Radius des äußeren Kreises'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 4000]
        p.value = 3000

        # inner radius
        p = self.add_parameter('inner')
        p.name = u'inner_circle'
        p.displayName = u'Radius des inneren Kreises'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 1500]
        p.value = 1000

        # number of destinations
        p = self.add_parameter('dests')
        p.name = u'destinations'
        p.displayName = u'Anzahl der Ziele auf dem äußeren Kreis'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 360]
        p.value = 18

        return params


    def _updateParameters(self, params):
        return


if __name__ == "__main__":
    t = TbxRouting()
    t.getParameterInfo()
    t.par.project.value = t.config.active_project
    t.execute()

    print 'done'