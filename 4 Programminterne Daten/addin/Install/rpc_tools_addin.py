# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os
from collections import OrderedDict

from rpctools.utils.config import Folders, Config
from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl
from rpctools.utils.basetable_definitions import Netzarten

folders = Folders()
config = Config()
    

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
    
    
class NetzartAuswahl(object):
    """Implementation for rpc_tools.netzart_auswahl (ComboBox)"""
    def __init__(self):
        self.netzarten = Netzarten(folders)
        self._id_map = OrderedDict([(netzart.name, netzart.id)
                                    for netzart in self.netzarten.values()])
        self.items = self._id_map.keys()
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.value = self.items[0]
        
    def get_selected_id(self):
        return self._id_map[self.value]
    
    def onSelChange(self, selection):
        self.value = selection
        

class NetzlinieTool(object):
    """Implementation for rpc_tools.netzlinie_tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Line" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        print line_geometry    
        project=config.active_project
        gdb = folders.get_table('Erschliessungsnetz', 
                                workspace='FGDB_Kosten.gdb',
                                project=project)
        cursor = arcpy.da.InsertCursor(gdb, ["SHAPE@", 'netz_id'])
        selected_id = netzart_auswahl.get_selected_id()
        cursor.insertRow([line_geometry, selected_id])
        del(cursor)
        arcpy.RefreshActiveView()
        
    def onRectangle(self, rectangle_geometry):
        pass
    

class NetzlinieLoeschen(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        active = config.active_project
        layers = projekt_auswahl.tbx.tool.output.get_layers(
            u'Erschließungsnetz', projectname=active)
        if not layers:
            return
        # ToDo: loop necessary?
        layer = layers[0]
        # check if anything is selected
        sth_selected = len(arcpy.Describe(layer).FIDset) > 0
        message = 'OK'
        if not sth_selected:
            message = pythonaddins.MessageBox(
                u'Es sind keine Netzlinien im Projekt {} '.format(active) + 
                u'ausgewählt.\nSollen alle in diesem Projekt '
                u'angelegten Netzlinien gelöscht werden?',
                'Achtung', 1)
        if message == 'OK':
            arcpy.DeleteFeatures_management(layer)
    

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