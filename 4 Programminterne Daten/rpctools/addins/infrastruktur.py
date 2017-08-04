# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os

from rpctools.addins.common import ToolboxButton, folders, config
from rpctools.addins.outputs import ErschliessungsnetzeAnzeigen
from rpctools.utils.output import ArcpyEnv

__all__ = [
    "AnliegerstrasseInnere", "AnliegerstrasseAeussere",
    "SammelstrasseAeussere", "SammelstrasseInnere",
    "KanalMischsystem", "KanalNurSchmutzwasser", "KanalTrennsystem",
    "Trinkwasserleitung", "Stromleitung",
    "NetzabschnittLoeschen",
    "InfrastrukturmengenBilanzieren", "GesamtkostenErmitteln", 
    "KostenNachKostentraegernAuswerten", "KostenProWEBzwAPVergleichen",
    "KostenkennwerteKontrollieren", "Kostenaufteilung",
    "PunktMassnahmeHinzu", "PunktMassnahmeBearbeiten"
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
        columns = (['id', "SHAPE@", 'IDNetzelement', 'IDNetz'] +
                   additional_columns.keys())
        cursor = arcpy.da.SearchCursor(table, ['id'])
        ids = [row[0] for row in cursor]
        id = 1 if not ids else max(ids) + 1
        cursor = arcpy.da.InsertCursor(
            table, columns)
        try:
            cursor.insertRow([id, shape, element_id, netz_id] +
                             additional_columns.values())
        except Exception as e:
            print(e)
        finally:
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


class Beschreibung(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxMassnahmenBeschreiben'

    def onClick(self):
        config.active_coord = None
        self._open()

    def _open(self):
        # no way to directly tell the toolbox the id of the measure
        # -> take the Config-singleton as a container to pass it
        config.active_measure_id = self._id_netzelement
        super(Beschreibung, self).onClick()


class InfrastructurePointTool(InfrastructureDrawingTool, Beschreibung):
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
        config.active_coord = (x, y)
        self._open()

    def onClick(self):
        pass


class AnliegerstrasseInnere(InfrastructureLineTool):
    """Implementation for rpc_tools.anliegerstrasse_innere (Tool)"""
    _id_netzelement = 11


class SammelstrasseInnere(InfrastructureLineTool):
    """Implementation for rpc_tools.sammelstrasse_innere (Tool)"""
    _id_netzelement = 12


class AnliegerstrasseAeussere(InfrastructureLineTool):
    """Implementation for rpc_tools.anliegerstrasse_aeussere (Tool)"""
    _id_netzelement = 21


class SammelstrasseAeussere(InfrastructureLineTool):
    """Implementation for rpc_tools.sammelstrasse_aeussere (Tool)"""
    _id_netzelement = 22


class KanalTrennsystem(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_trennsystem (Tool)"""
    _id_netzelement = 31


class KanalMischsystem(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_mischsystem (Tool)"""
    _id_netzelement = 32


class KanalNurSchmutzwasser(InfrastructureLineTool):
    """Implementation for rpc_tools.kanal_nur_schmutzwasser (Tool)"""
    _id_netzelement = 33


class Trinkwasserleitung(InfrastructureLineTool):
    """Implementation for rpc_tools.trinkwasserleitung (Tool)"""
    _id_netzelement = 41


class Stromleitung(InfrastructureLineTool):
    """Implementation for rpc_tools.stromleitung (Tool)"""
    _id_netzelement = 51


class PunktMassnahmeBearbeiten(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxMassnahmenEditieren'

    def __init__(self):
        super(PunktMassnahmeBearbeiten, self).__init__()
        self.enabled = True
        self.shape = 'NONE'
        self.cursor = 3
        self.output = ErschliessungsnetzeAnzeigen()

    def onClick(self, coord=None):
        self.output.show()

    def onMouseDownMap(self, x, y, button, shift):
        config.active_coord = (x, y)
        super(PunktMassnahmeBearbeiten, self).onClick()


class PunktMassnahmeHinzu(PunktMassnahmeBearbeiten):

    def onMouseDownMap(self, x, y, button, shift):
        tbx = self.tbx
        tbx.set_active_project()
        tbx.add_measure_to_db(u'unbenannte Maßnahme', (x, y))
        arcpy.RefreshActiveView()
        super(PunktMassnahmeHinzu, self).onMouseDownMap(x, y, button, shift)


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


class NetzabschnittLoeschen(InfrastructureDrawingTool):
    def __init__(self):
        super(NetzabschnittLoeschen, self).__init__()
        self.shape = "Rectangle"

    def onRectangle(self, rectangle):
        xmin, ymin = rectangle.XMin, rectangle.YMin
        xmax, ymax = rectangle.XMax, rectangle.YMax
        project=config.active_project
        lines = folders.get_table('Erschliessungsnetze_Linienelemente',
                                  workspace='FGDB_Kosten.gdb',
                                  project=project)
        fc_bbox = 'in_memory/rectangle'
        fc_clipped = 'in_memory/clipped_lines'
        poly_points = arcpy.Array([
            arcpy.Point(xmin, ymin),
            arcpy.Point(xmin, ymax),
            arcpy.Point(xmax, ymax),
            arcpy.Point(xmax, ymin),
            arcpy.Point(xmin, ymin)
        ])
        bbox_poly = arcpy.Polygon(poly_points)
        with ArcpyEnv(addOutputsToMap=False):
            arcpy.CopyFeatures_management([bbox_poly], fc_bbox)
            arcpy.Clip_analysis(lines, fc_bbox, fc_clipped)
        cursor = arcpy.da.SearchCursor(fc_clipped, ['id', 'IDNetzelement'])
        del_ids = [id for id, element in cursor]
        del(cursor)
        cursor = arcpy.da.UpdateCursor(lines, 'id')
        for row in cursor:
            if row[0] in del_ids:
                cursor.deleteRow()
        del(cursor)
        arcpy.Delete_management(fc_bbox)
        arcpy.Delete_management(fc_clipped)
        arcpy.RefreshActiveView()


class InfrastrukturmengenBilanzieren(ToolboxButton):
    """Implementation for rpc_tools.infrastrukturmengen_bilanzieren (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxInfrastrukturmengenBilanz'
    _do_show = False


class KostenkennwerteKontrollieren(ToolboxButton):
    """Implementation for rpc_tools.kostenkennwerte_kontrollieren (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxKostenkennwerteKontrollieren'


class GesamtkostenErmitteln(ToolboxButton):
    """Implementation for rpc_tools.gesamtkosten_ermitteln (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxGesamtkosten'


class KostenNachKostentraegernAuswerten(ToolboxButton):
    """Implementation for rpc_tools.kosten_nach_kostentraegern_auswerten (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxKostentraegerAuswerten'


class KostenProWEBzwAPVergleichen(ToolboxButton):
    """Implementation for rpc_tools.kosten_pro_we_bzw_ap_vergleichen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxKostenVergleichen'


class Kostenaufteilung(ToolboxButton):
    """Implementation for rpc_tools.kostenaufteilung (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxNetzKostenaufteilungInnere'