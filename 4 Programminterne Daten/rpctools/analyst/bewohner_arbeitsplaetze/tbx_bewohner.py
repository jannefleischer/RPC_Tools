# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.utils.params import Tool
from rpctools.utils.constants import Nutzungsart
from rpctools.diagrams.bewohner_arbeitsplaetze import BewohnerEntwicklung
import pandas as pd
import arcpy


class Bewohner(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
    
    def add_outputs(self):
        tfl = self.parent_tbx.get_teilflaeche(self.par.teilflaeche.value)
        diagram = BewohnerEntwicklung()
        diagram.create(flaechen_id=tfl.flaechen_id,
                       flaechen_name=tfl.name)
        self.output.add_diagram(diagram)

    def run(self):
        pass


class TbxBewohner(TbxFlaechendefinition):
    _nutzungsart = Nutzungsart.WOHNEN
    
    @property
    def Tool(self):
        return Bewohner

    @property
    def label(self):
        return u'Bewohnerzahl schätzen'
    
    def _getParameterInfo(self):
        params = super(TbxBewohner, self)._getParameterInfo()
        # TbxFlaechendefinition adds workspace to temp. management, not required
        # here (no settings are made)
        self.remove_temporary_management()
        return params    
    
if __name__ == '__main__':
    t = TbxBewohner()
    params = t.getParameterInfo()
    t.set_active_project()
    t.update_teilflaechen(nutzungsart=1)
    t.show_outputs(show_layers=False)