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
    

class ArbeitsplaetzeSchaetzen(object):
    """Implementation for rpc_tools.arbeitsplaetze_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class BeschreibungPunktuelleMassnahmeElektrizitaet(object):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_elektrizitaet (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class BeschreibungPunktuelleMassnahmeKanalisation(object):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_kanalisation (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class BeschreibungPunktuelleMassnahmeStrasseAeussere(object):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_auessere (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class BeschreibungPunktuelleMassnahmeStrasseInnere(object):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_innere (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class BeschreibungPunktuelleMassnahmeTrinkwasser(object):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_trinkwasser (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class ElektrizitaetKostenaufteilung(object):
    """Implementation for rpc_tools.elektrizitaet_kostenaufteilung (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class GesamtkostenErmitteln(object):
    """Implementation for rpc_tools.gesamtkosten_ermitteln (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class HebesaetzeGewerbesteuer(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class HebesaetzeGrundsteuerB(object):
    """Implementation for rpc_tools.hebesaetze_grundsteuer_b (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class InfrastrukturmengenBilanzieren(object):
    """Implementation for rpc_tools.infrastrukturmengen_bilanzieren (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class KanalisationKostenaufteilung(object):
    """Implementation for rpc_tools.kanalisation_kostenaufteilung (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class KostenNachKostentraegernAuswerten(object):
    """Implementation for rpc_tools.kosten_nach_kostentraegern_auswerten (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class KostenProWEBzwAPVergleichen(object):
    """Implementation for rpc_tools.kosten_pro_we_bzw_ap_vergleichen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class KostenkennwerteKontrollieren(object):
    """Implementation for rpc_tools.kostenkennwerte_kontrollieren (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class SkizzeBeenden(object):
    """Implementation for rpc_tools.skizze_beenden (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
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
        pass
    def onRectangle(self, rectangle_geometry):
        pass

class StrasseAeussereKostenaufteilung(object):
    """Implementation for rpc_tools.strasse_aeussere_kostenaufteilung (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class StrasseInnereKostenaufteilung(object):
    """Implementation for rpc_tools.strasse_innere_kostenaufteilung (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
    
class TrinkwasserKostenaufteilung(object):
    """Implementation for rpc_tools.trinkwasser_kostenaufteilung (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass


### PROJECT MANAGEMENT ###


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


### DRAWING TOOLS ###


class DrawingTool(object):
    # has to match the column 'IDNetzelement' of base-table 
    # Netze_und_Netzelemente (defined in subclasses)
    _id_netzelement = None
    
    def __init__(self):
        self.enabled = True
        netz_table = folders.get_base_table('FGDB_Kosten_Tool.gdb',
                                            'Netze_und_Netzelemente')
        self.netz_ids = {}
        cursor = arcpy.da.SearchCursor(netz_table, ['IDNetzelement', 'IDNetz'])
        self.netz_ids = dict([row for row in cursor])
        self.cursor = 3
        self.tbx = TbxInfrastruktur()
        self.tbx.getParameterInfo()
        
    def commit_geometry(self, table, shape, element_id):
        self.tbx.par.projectname.value = config.active_project
        if not self.tbx.tool.output.layer_exists(
            'Wirkungsbereich 5 - Infrastrukturfolgekosten'):
            self.tbx.tool.add_output()
        netz_id = self.netz_ids[element_id]
        project=config.active_project
        gdb = folders.get_table(table, 
                                workspace='FGDB_Kosten.gdb',
                                project=project)
        cursor = arcpy.da.InsertCursor(
            gdb, ["SHAPE@", 'IDNetzelement', 'IDNetz'])
        cursor.insertRow([shape, element_id, netz_id])
        del(cursor)
        arcpy.RefreshActiveView()    


class LineTool(DrawingTool):
    _id_netzelement = None
    table = 'Erschliessungsnetze_Linienelemente'
    
    def __init__(self):
        super(LineTool, self).__init__()
        self.shape = "Line"
        
    def onLine(self, line_geometry):
        self.commit_geometry(self.table, line_geometry, self._id_netzelement)


class PointTool(DrawingTool):
    _id_netzelement = None
    table = 'Erschliessungsnetze_Punktelemente'
    
    def __init__(self):
        super(PointTool, self).__init__()
        self.shape = "NONE"
        
    def onMouseDownMap(self, x, y, button, shift):
        point_geometry = arcpy.Point(x, y)
        self.commit_geometry(self.table, point_geometry, self._id_netzelement)


class AnliegerstrasseInnere(LineTool):
    """Implementation for rpc_tools.anliegerstrasse_innere (Tool)"""
    _id_netzelement = 11
    

class SammelstrasseInnere(LineTool):
    """Implementation for rpc_tools.sammelstrasse_innere (Tool)"""
    _id_netzelement = 12


class LagePunktuelleMassnahmeStrasseInnere(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_strasse_innere (Tool)"""
    _id_netzelement = 13


class AnliegerstrasseAeussere(LineTool):
    """Implementation for rpc_tools.anliegerstrasse_aeussere (Tool)"""
    _id_netzelement = 14


class SammelstrasseAeussere(LineTool):
    """Implementation for rpc_tools.sammelstrasse_aeussere (Tool)"""
    _id_netzelement = 15
    
    
class LagePunktuelleMassnahmeStrasseAeussere(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_strasse_aeussere (Tool)"""
    _id_netzelement = 16
    

class KanalTrennsystem(LineTool):
    """Implementation for rpc_tools.kanal_trennsystem (Tool)"""
    _id_netzelement = 21


class KanalMischsystem(LineTool):
    """Implementation for rpc_tools.kanal_mischsystem (Tool)"""
    _id_netzelement = 22


class KanalNurSchmutzwasser(LineTool):
    """Implementation for rpc_tools.kanal_nur_schmutzwasser (Tool)"""
    _id_netzelement = 23


class LagePunktuelleMassnahmeKanalisation(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_kanalisation (Tool)"""
    _id_netzelement = 24


class Trinkwasserleitung(LineTool):
    """Implementation for rpc_tools.trinkwasserleitung (Tool)"""
    _id_netzelement = 31


class LagePunktuelleMassnahmeTrinkwasser(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_trinkwasser (Tool)"""
    _id_netzelement = 32


class Stromleitung(LineTool):
    """Implementation for rpc_tools.stromleitung (Tool)"""
    _id_netzelement = 41


class LagePunktuelleMassnahmeElektrizitaet(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_elektrizitaet (Tool)"""
    _id_netzelement = 42


def delete_selected_elements(layer_name): 
    active = config.active_project
    layers = projekt_auswahl.tbx.tool.output.get_layers(
        layer_name, projectname=active)
    if not layers:
        return
    # ToDo: loop necessary?
    layer = layers[0]
    # check if anything is selected
    sth_selected = len(arcpy.Describe(layer).FIDset) > 0
    message = 'OK'
    if not sth_selected:
        message = pythonaddins.MessageBox(
            u'Es sind keine Elemente im Layer "{layer}" des Projektes "{proj}" '
            .format(layer=layer_name, proj=active) + 
            u'ausgewählt.\n\nSollen alle in diesem Layer '
            u'angelegten Elemente aus dem Projekt gelöscht werden?',
            'Achtung', 1)
    if message == 'OK':
        arcpy.DeleteFeatures_management(layer)


class NetzabschnittLoeschen(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        delete_selected_elements(u'Erschließungsnetz')


class PunktuelleMassnahmeLoeschen(object):
    """Implementation for rpc_tools.punktuelle_massnahme_loeschen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        delete_selected_elements(u'Erschließungsnetz - punktuelle Maßnahmen')


### NUTZUNGEN ###


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


### BEWOHNER ARBEISTPLAETZE ###


class BewohnerSchaetzen(object):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Bewohner_Arbeitsplaetze.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxBewohner')


### EINNAHMEN ###


class WanderungssaldenSchaetzen(object):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxWanderungssalden')


class Einwohnersalden(object):
    """Implementation for rpc_tools.einwohnersalden (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxEWSaldenbearbeiten')


class Beschaeftigtensalden(object):
    """Implementation for rpc_tools.beschaeftigtensalden (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxGewSaldenbearbeiten')


class EinnahmeverschiebungenSchaetzen(object):
    """Implementation for rpc_tools.einnahmeverschiebungen_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxSteuersalden')


if __name__ == "__main__":
    t = DrawingTool()
    t.commit_geometry(None, None, None)