# -*- coding: utf-8 -*-

import sys

import arcpy
import datetime
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.projektauswahl import \
     Projektauswahl


class TbxProjektauswahl(Tbx):
    """Toolbox Projektauswahl"""

    @property
    def label(self):
        return u'aktives Projekt wählen'

    @property
    def Tool(self):
        return Projektauswahl

    def __init__(self):
        super(TbxProjektauswahl, self).__init__()
        self.update_projects = False

    def _getParameterInfo(self):
        params = self.par
        # Bestehendes_Projekt_auswählen
        p = params.active_project = arcpy.Parameter()
        p.name = encode('aktives Projekt')
        p.displayName = encode('aktives Projekt auswählen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if self.recently_opened:
            params.active_project.filter.list = self.folders.get_projects()
            if self.config.active_project:
                params.active_project.value = self.config.active_project
        