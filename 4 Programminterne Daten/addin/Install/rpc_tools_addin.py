import arcpy
import pythonaddins
import os

from rpctools.utils.config import Folders, Config
from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl

folders = Folders()
config = Config()

class ButtonClass16(object):
    # Nutzungen auf Teilfl&#228;chen definieren
    """Implementation for rpc_tools.button_3 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projektverwaltung = os.path.join(folders.DEFINITION_PYT_PATH,
                                         'Projektdefinition.pyt')
        pythonaddins.GPToolDialog(projektverwaltung, 'TbxTeilflaecheVerwalten')

class ButtonClass17(object):
    """Implementation for rpc_tools.button_4 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class ButtonClass18(object):
    """Implementation for rpc_tools.button_5 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class ButtonClass19(object):
    """Implementation for rpc_tools.button_6 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class ProjektAnlegen(object):
    """Implementation for rpc_tools.neues_projekt (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projektverwaltung = os.path.join(folders.DEFINITION_PYT_PATH,
                                         'Projektverwaltung.pyt')
        pythonaddins.GPToolDialog(projektverwaltung, 'TbxProjektAnlegen')

class ProjektAuswahl(object):
    """Implementation for rpc_tools.projekt_auswahl (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.tbx = TbxProjektauswahl()
        self.tbx.getParameterInfo()
        config.on_change('active_project', lambda active: self.refresh())
        self.refresh()

    def onSelChange(self, selection):
        if selection != config.active_project:
            #config.active_project = selection
            #config.write()
            self.tbx.par.active_project.value = selection
            self.tbx.execute()
        self.value = selection

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        if focused:
            self.refresh()

    def onEnter(self):
        pass

    def refresh(self):
        projects = folders.get_projects()
        self.items = sorted(projects)
        active = config.active_project
        if active not in projects:
            active = ''
        self.value = active

class ProjektKopieren(object):
    """Implementation for rpc_tools.projekt_kopieren (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projektverwaltung = os.path.join(folders.DEFINITION_PYT_PATH,
                                         'Projektverwaltung.pyt')
        pythonaddins.GPToolDialog(projektverwaltung, 'TbxProjektKopieren')

class ProjektLoeschen(object):
    """Implementation for rpc_tools.projekt_loeschen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projektverwaltung = os.path.join(folders.DEFINITION_PYT_PATH,
                                         'Projektverwaltung.pyt')
        pythonaddins.GPToolDialog(projektverwaltung, 'TbxProjekteLoeschen')