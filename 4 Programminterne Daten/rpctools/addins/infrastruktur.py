# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os

from rpctools.addins.common import ToolboxButton, folders, config
from rpctools.addins.outputs import ErschliessungsnetzeAnzeigen

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
    "NetzabschnittLoeschen", "PunktuelleMassnahmeLoeschen",
    "InfrastrukturmengenBilanzieren", "ElektrizitaetKostenaufteilung", 
    "GesamtkostenErmitteln", "KanalisationKostenaufteilung",
    "KostenNachKostentraegernAuswerten", "KostenProWEBzwAPVergleichen",
    "KostenkennwerteKontrollieren", "StrasseAeussereKostenaufteilung",
    "StrasseInnereKostenaufteilung", "TrinkwasserKostenaufteilung"
]


class InfrastructureDrawingTool(object):
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
        self.output = ErschliessungsnetzeAnzeigen()
        
    def onClick(self):
        self.output.show()

    def commit_geometry(self, tablename, shape, element_id, additional_columns={}):
        """insert geometry with spec. id into given table """        
        netz_id = self.netz_ids[element_id]
        project=config.active_project
        table = folders.get_table(tablename,
                                  workspace='FGDB_Kosten.gdb',
                                  project=project)
        columns = (["SHAPE@", 'IDNetzelement', 'IDNetz'] +
                   additional_columns.keys())
        cursor = arcpy.da.InsertCursor(
            table, columns)
        cursor.insertRow([shape, element_id, netz_id] +
                         additional_columns.values())
        del(cursor)
        arcpy.RefreshActiveView()

    def get_ids(self, tablename):
        project=config.active_project
        table = folders.get_table(tablename,
                                  workspace='FGDB_Kosten.gdb',
                                  project=project)
        cursor = arcpy.da.SearchCursor(table, ['OBJECTID'])
        ids = [row[0] for row in cursor]
        del(cursor)
        return ids


class InfrastructureLineTool(InfrastructureDrawingTool):
    table = 'Erschliessungsnetze_Linienelemente'

    def __init__(self):
        super(InfrastructureLineTool, self).__init__()
        self.shape = "Line"

    def onLine(self, line_geometry):
        self.commit_geometry(self.table, line_geometry, self._id_netzelement)


class InfrastructurePointTool(InfrastructureDrawingTool):
    table = 'Erschliessungsnetze_Punktelemente'

    def __init__(self):
        super(InfrastructurePointTool, self).__init__()
        self.shape = "NONE"

    def onMouseDownMap(self, x, y, button, shift):
        point_geometry = arcpy.Point(x, y)
        ids = self.get_ids(self.table)
        max_id = max(ids) if ids else 0
        desc = u'Maßnahme {id} ({x}, {y})'.format(id=max_id, x=x, y=y)
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


class Beschreibung(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxMassnahmenBeschreiben'

    def onClick(self):
        # no way to directly tell the toolbox the id of the measure
        # -> take the Config-singleton as a container to pass it
        config.active_measure_id = self._id_netzelement
        super(Beschreibung, self).onClick()


class AnliegerstrasseInnere(InfrastructureLineTool):
    """Implementation for rpc_tools.anliegerstrasse_innere (Tool)"""
    _id_netzelement = 11


class SammelstrasseInnere(InfrastructureLineTool):
    """Implementation for rpc_tools.sammelstrasse_innere (Tool)"""
    _id_netzelement = 12


class LagePunktuelleMassnahmeStrasseInnere(InfrastructurePointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_strasse_innere (Tool)"""
    _id_netzelement = 13


class BeschreibungPunktuelleMassnahmeStrasseInnere(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_innere (Button)"""
    _id_netzelement = 13


class AnliegerstrasseAeussere(InfrastructureLineTool):
    """Implementation for rpc_tools.anliegerstrasse_aeussere (Tool)"""
    _id_netzelement = 14


class SammelstrasseAeussere(InfrastructureLineTool):
    """Implementation for rpc_tools.sammelstrasse_aeussere (Tool)"""
    _id_netzelement = 15


class LagePunktuelleMassnahmeStrasseAeussere(InfrastructurePointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_strasse_aeussere (Tool)"""
    _id_netzelement = 16


class BeschreibungPunktuelleMassnahmeStrasseAeussere(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_auessere (Button)"""
    _id_netzelement = 16


class KanalTrennsystem(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_trennsystem (Tool)"""
    _id_netzelement = 21


class KanalMischsystem(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_mischsystem (Tool)"""
    _id_netzelement = 22


class KanalNurSchmutzwasser(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_nur_schmutzwasser (Tool)"""
    _id_netzelement = 23


class LagePunktuelleMassnahmeKanalisation(InfrastructurePointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_kanalisation (Tool)"""
    _id_netzelement = 24


class BeschreibungPunktuelleMassnahmeKanalisation(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_kanalisation (Button)"""
    _id_netzelement = 24


class Trinkwasserleitung(InfrastructureLineTool):
    """Implementation for rpc_tools.trinkwasserleitung (Tool)"""
    _id_netzelement = 31


class LagePunktuelleMassnahmeTrinkwasser(InfrastructurePointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_trinkwasser (Tool)"""
    _id_netzelement = 32


class BeschreibungPunktuelleMassnahmeTrinkwasser(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_trinkwasser (Button)"""
    _id_netzelement = 32


class Stromleitung(InfrastructureLineTool):
    """Implementation for rpc_tools.stromleitung (Tool)"""
    _id_netzelement = 41


class LagePunktuelleMassnahmeElektrizitaet(InfrastructurePointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_elektrizitaet (Tool)"""
    _id_netzelement = 42


class BeschreibungPunktuelleMassnahmeElektrizitaet(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_elektrizitaet (Button)"""
    _id_netzelement = 42


def delete_selected_elements(layer_name):
    active = config.active_project
    output = ErschliessungsnetzeAnzeigen()
    layers = output.get_layers(layer_name)
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


class InfrastrukturmengenBilanzieren(ToolboxButton):
    """Implementation for rpc_tools.infrastrukturmengen_bilanzieren (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxInfrastrukturmengenBilanz'
    _do_show = False


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