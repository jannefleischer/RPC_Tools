# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode

from rpctools.analyst.standortkonkurrenz.dist_markets import DistMarkets

class TbxDistMarkets(Tbx):

    @property
    def label(self):
        return encode(u'Entfernung zwischen Supermarkt und Rasterzellen berechnen')

    @property
    def Tool(self):
        return DistMarkets

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
        p.value = self.config.active_project
        p.enabled = False

        # set square size
        p = self.add_parameter('square_size')
        p.name = u'sqare_size'.encode('cp1252')
        p.displayName = u'Größe des Bereichs wählen (km)'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.value = 20

        return params

    def _updateParameters(self, params):
        pass



if __name__ == "__main__":
    t = TbxDistMarkets()
    t.getParameterInfo()
    t.par.project.value = t.config.active_project
    t.execute()

    print 'done'