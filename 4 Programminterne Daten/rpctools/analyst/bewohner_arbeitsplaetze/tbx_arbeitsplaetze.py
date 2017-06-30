# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.utils.params import Tool
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.spatial_lib import get_gemeindetyp
from rpctools.diagrams.bewohner_arbeitsplaetze import (ArbeitsplatzEntwicklung,
                                                       BranchenAnteile)
import pandas as pd
import arcpy


class Arbeitsplaetze(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
    
    def add_outputs(self):
        tfl = self.parent_tbx.get_teilflaeche(self.par.teilflaeche.value)
        diagram = ArbeitsplatzEntwicklung()
        diagram.create(flaechen_id=tfl.flaechen_id,
                       flaechen_name=tfl.name)
        self.output.add_diagram(diagram)
        
        diagram.show()
        diagram = BranchenAnteile()
        diagram.create(flaechen_id=tfl.flaechen_id,
                       flaechen_name=tfl.name)
        self.output.add_diagram(diagram)

    def run(self):
        pass


class TbxArbeitsplaetze(TbxFlaechendefinition):
    _nutzungsart = Nutzungsart.GEWERBE

    @property
    def Tool(self):
        return Arbeitsplaetze

    @property
    def label(self):
        return u'Arbeitsplätze schätzen'

if __name__ == '__main__':
    t = TbxArbeitsplaetze()
    params = t.getParameterInfo()
    t.par.projectname.value = t.config.active_project
    t.tool.main(t.par, None)