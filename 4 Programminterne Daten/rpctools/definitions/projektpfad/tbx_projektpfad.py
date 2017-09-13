# -*- coding: utf-8 -*-
import arcpy
import os

from rpctools.utils.config import Config
from rpctools.utils.params import Tbx, Tool


class ProjectFolder(Tool):

    def run(self):
        config = Config()
        tbx = self.parent_tbx
        config.project_folder = str(tbx.par.folderpath.value)


    def add_outputs(self):
        pass


class TbxProjectFolder(Tbx):

    @property
    def label(self):
        return encode(u'Projektpfad setzen')

    @property
    def Tool(self):
        return ProjectFolder

    def _getParameterInfo(self):
        params = self.par

        p = self.add_parameter('folderpath')
        p.name = u'folderpath'
        p.displayName = u'Pfad zu den benutzerdefinierten Projekten'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'DEFolder'

        return params
