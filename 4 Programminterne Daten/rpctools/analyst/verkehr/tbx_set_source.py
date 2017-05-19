# -*- coding: utf-8 -*-
#
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.verkehr.set_source import SetSource
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten \
     import TbxFlaechendefinition
from rpctools.utils.constants import Nutzungsart

#class TbxSetSource(TbxFlaechendefinition):
    #_nutzungsart = Nutzungsart.GEWERBE

    #@property
    #def Tool(self):
        #return SetSource

    #@property
    #def label(self):
        #return encode(u'Schritt 3: Startpunkte ändern')

class TbxSetSource(TbxFlaechendefinition):

    @property
    def label(self):
        return encode(u'Schritt 3: Startpunkte ändern')

    @property
    def Tool(self):
        return SetSource

    def _open(self, params):
        x, y = self.config.active_coord
        params.x_source.value = x
        params.y_source.value = y

    def _getParameterInfo(self):
        params = super(TbxSetSource, self)._getParameterInfo()

        # x coord
        p = self.add_parameter('x_source')
        p.name = u'x'
        p.displayName = u'X-Koordinate des Anbindungspunktes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPDouble'
        p.value = 0

        # y coord
        p = self.add_parameter('y_source')
        p.name = u'y'
        p.displayName = u'Y-Koordinate des Anbindungspunktes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPDouble'
        p.value = 0

        return self.par

    def _updateParameters(self, params):
        params = super(TbxSetSource, self)._updateParameters(params)
        return params

if __name__ == '__main__':
    tbx = TbxSetSource()
    p = tbx.getParameterInfo()
    print