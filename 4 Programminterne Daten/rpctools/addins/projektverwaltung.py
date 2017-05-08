# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os
from collections import OrderedDict

from rpctools.utils.config import Folders, Config
from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl
from rpctools.analyst.infrastrukturkosten.tbx_infrastruktur import \
     TbxInfrastruktur

folders = Folders()
config = Config()

__all__ = ["ProjektAnlegen", "ProjektAuswahl", "ProjektKopieren",
           "ProjektLoeschen", "RefreshLayers"]


class ProjektAnlegen(object):
    """Implementation for rpc_tools.neues_projekt (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektverwaltung.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxProjektAnlegen')
        

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
            self.activate_project(project=selection)
        self.value = selection
        
    def activate_project(self, project=None):
        if project is None:
            project = self.value
        self.tbx.par.active_project.value = project
        self.tbx.execute()

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
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektverwaltung.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxProjektKopieren')
        

class ProjektLoeschen(object):
    """Implementation for rpc_tools.projekt_loeschen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.DEFINITION_PYT_PATH,
                                 'Projektverwaltung.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxProjekteLoeschen')


class RefreshLayers(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projekt_auswahl.activate_project()
