# -*- coding: utf-8 -*-
#

import arcpy

from rpctools.utils.params import Tool

class SetSource(Tool):
    _dbname = 'FGDB_Verkehr.gdb'
    _param_projectname = 'projectname'

    def run(self):
        pass