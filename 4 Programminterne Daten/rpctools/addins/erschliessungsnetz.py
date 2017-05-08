# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os

from rpctools.utils.config import Folders, Config
from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl
from rpctools.analyst.infrastrukturkosten.tbx_infrastruktur import \
     TbxInfrastruktur

folders = Folders()
config = Config()

__all__ = [
    "AnliegerstrasseInnere", "AnliegerstrasseAeussere",
    "SammelstrasseAeussere", "SammelstrasseInnere", 
    "KanalMischsystem", "KanalNurSchmutzwasser", "KanalTrennsystem",
    "LagePunktuelleMassnahmeElektrizitaet",
    "LagePunktuelleMassnahmeKanalisation",
    "LagePunktuelleMassnahmeStrasseAeussere",
    "LagePunktuelleMassnahmeStrasseInnere",
    "LagePunktuelleMassnahmeTrinkwasser",
    "Trinkwasserleitung", "Stromleitung", 
    "NetzabschnittLoeschen", "PunktuelleMassnahmeLoeschen"
]

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
        
    def commit_geometry(self, table, shape, element_id, additional_columns={}):
        """insert geometry with spec. id into given table """
        self.tbx.par.projectname.value = config.active_project
        if not self.tbx.tool.output.layer_exists(
            'Wirkungsbereich 5 - Infrastrukturfolgekosten'):
            self.tbx.tool.add_output()
        netz_id = self.netz_ids[element_id]
        project = config.active_project
        gdb = folders.get_table(table, 
                                workspace='FGDB_Kosten.gdb',
                                project=project)
        columns = (["SHAPE@", 'IDNetzelement', 'IDNetz'] +
                   additional_columns.keys())
        cursor = arcpy.da.InsertCursor(
            gdb, columns)
        cursor.insertRow([shape, element_id, netz_id] +
                         additional_columns.values())
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
        desc = u'unbenannt @({x}, {y})'.format(x=x, y=y)
        self.commit_geometry(
            self.table, point_geometry, self._id_netzelement,
            additional_columns={
                'Kosten_EH_EUR': 0,
                'Kosten_BU_EUR': 0,
                'Kosten_EN_EUR': 0,
                'Lebensdauer': 20,
                'Bezeichnung': desc,
                }
        )


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
