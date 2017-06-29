# -*- coding: utf-8 -*-
import os
import arcpy
import webbrowser

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.analyst.erreichbarkeit.tbx_HaltestellenZentraleOrte import next_working_day
from rpctools.analyst.erreichbarkeit.bahn_query import BahnQuery


class Gesamtkosten(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Kosten.gdb'
    
    def add_outputs(self):
        pass
    
    def run(self):
        self.calculate()
    
    def calculate(self):
        print()


class TbxGesamtkosten(Tbx):

    @property
    def label(self):
        return encode(u'Gesamtkosten berechnen')

    @property
    def Tool(self):
        return Gesamtkosten
    
    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt auswählen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.value = self.config.active_project
        return params
    
    def validate_inputs(self):
        return True, ''
        
    def _open(self, params):
        pass
    
if __name__ == "__main__":
    t = TbxGesamtkosten()
    t.getParameterInfo()
    t.set_active_project()
    t.open()
    t.execute()
