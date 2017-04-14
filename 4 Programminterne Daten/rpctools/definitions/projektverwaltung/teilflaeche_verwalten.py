# -*- coding: utf-8 -*-

import arcpy
import os
from collections import OrderedDict

from rpctools.utils.params import Tool


class TeilflaechenVerwalten(Tool):

    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'


    def run(self):
        # atm there is nothing to do here, setting db is already done in toolbox
        # ToDo: add output layer
        pass