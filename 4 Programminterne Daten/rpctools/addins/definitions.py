from rpctools.utils.config import Folders
import os

folders = Folders()

__all__ = ["NutzungenDefinieren", "Wohnen", "Gewerbe", "Einzelhandel"]


class NutzungenDefinieren(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektdefinition.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxTeilflaecheVerwalten')


class Wohnen(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektdefinition.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxNutzungenWohnen')


class Gewerbe(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektdefinition.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxNutzungenGewerbe')


class Einzelhandel(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektdefinition.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxNutzungenEinzelhandel')
