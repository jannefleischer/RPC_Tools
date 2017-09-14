# -*- coding: utf-8 -*-
import arcpy
import os

from rpctools.utils.config import Config
from rpctools.utils.params import Tbx, Tool


class ProjectFolder(Tool):

    def run(self):
        config = Config()
        tbx = self.parent_tbx
        if not tbx._writeable:
            arcpy.AddError("Für den von Ihnen angegebenen Dateipfad besitzen "
                           "Sie keine Schreibrechte. Bitte geben Sie einen "
                           "anderen Pfad an!")
            return
        config.active_project = ""
        config.project_folder = str(tbx.par.folderpath.value)


    def add_outputs(self):
        pass


class TbxProjectFolder(Tbx):
    _writeable = True
    @property
    def label(self):
        return encode(u'Projektpfad setzen')

    @property
    def Tool(self):
        return ProjectFolder

    def validate_active_project(self):
        return True, ''

    def _open(self, params):
        p = params.folderpath
        config = Config()
        project_folder = config.project_folder
        p.value = project_folder

    def _getParameterInfo(self):
        self.requires_existing_project_path = False
        self.requires_existing_project = False
        params = self.par
        config = Config()
        p = self.add_parameter('folderpath')
        p.name = u'folderpath'
        p.displayName = u'Pfad zu den benutzerdefinierten Projekten'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'DEFolder'

        p = self.add_parameter('dummy')
        p.direction = 'Input'
        p.parameterType = 'Optional'
        p.enabled = False

        return params

    def _updateMessages(self, params):

        par = self.par
        if par.changed('folderpath'):
            try:
                test_path = str(par.folderpath.value) + \
                    r'\writability_test.txt'
                testfile = open(test_path, 'w+')
                testfile.close()
                os.remove(test_path)
                self._writeable = True
            except:
                self._writeable = False
                arcpy.AddMessage(str(par.folderpath.value))
                par.folderpath.setErrorMessage(u'Sie besitzen keine '
                                               u'Schreibrechte für diesen '
                                               u'Pfad!')