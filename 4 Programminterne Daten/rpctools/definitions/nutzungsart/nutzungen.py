# -*- coding: utf-8 -*-

from rpctools.utils.params import Tool
import arcpy


class Nutzungen(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        """"""