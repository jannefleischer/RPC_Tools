# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os
from collections import OrderedDict
from abc import ABCMeta, abstractproperty
from imp import load_source

from rpctools.utils.config import Folders, Config
from rpctools.definitions.projektverwaltung.tbx_projektauswahl import \
     TbxProjektauswahl
from rpctools.analyst.infrastrukturkosten.tbx_infrastrukturmengenbilanz import \
     TbxInfrastrukturmengenBilanz

folders = Folders()
config = Config()

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


class ToolboxButton(object):
    """super class for buttons calling toolboxes on click"""
    __metaclass__ = ABCMeta
    # path to pyt file
    _path = None
    # the pyt importing the required toolbox
    _pyt_file = None
    # the class name of the toolbox (as imported in the pyt file)
    _toolbox_name = None
    # show the toolbox on click (if False, just execute the Tool)
    _do_show = True

    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(self._path, self._pyt_file)
        self._tbx = None

    @property
    def tbx(self):
        """the instanciated toolbox (load on demand only)"""
        if not self._tbx:
            tbx_module = load_source(self._toolbox_name, self.path)
            self._tbx = getattr(tbx_module, self._toolbox_name)()
            self._tbx.getParameterInfo()
        return self._tbx

    def onClick(self):
        """call toolbox on click"""
        # validate active project
        self.tbx.set_active_project()
        valid, msg = self.tbx.validate_inputs()
        # call toolbox
        if valid:
            # let the GUI build an instance of the toolbox to show it
            # (regular call of updateParameters etc. included)
            if self._do_show:
                pythonaddins.GPToolDialog(self.path, self._toolbox_name)
            # execute main function of Tool only (no updates etc. possible)
            else:
                self.tbx.execute()
        else:
            pythonaddins.MessageBox(msg, 'Fehler', 0)


### PROJECT MANAGEMENT ###


class ProjektAnlegen(ToolboxButton):
    """Implementation for rpc_tools.neues_projekt (Button)"""
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektverwaltung.pyt'
    _toolbox_name = 'TbxProjektAnlegen'


class ProjektAuswahl(object):
    """Implementation for rpc_tools.projekt_auswahl (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.tbx = TbxProjektauswahl()
        self.tbx.getParameterInfo()
        # connect the change of the active project to a refresh of the project-
        # list (esp. to auto. select the active project)
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

    def onFocus(self, focused):
        if focused:
            self.refresh()

    def refresh(self):
        """refresh the list of available projects and select the active one"""
        projects = folders.get_projects()
        self.items = sorted(projects)
        active = config.active_project
        if active not in projects:
            active = ''
        self.value = active


class ProjektKopieren(ToolboxButton):
    """Implementation for rpc_tools.projekt_kopieren (Button)"""
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektverwaltung.pyt'
    _toolbox_name = 'TbxProjektKopieren'


class ProjektLoeschen(ToolboxButton):
    """Implementation for rpc_tools.projekt_loeschen (Button)"""
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektverwaltung.pyt'
    _toolbox_name = 'TbxProjekteLoeschen'


class RefreshLayers(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        projekt_auswahl.activate_project()


### NETZERSCHLIESSUNG / INFRASTRUKTUR ###


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

    def commit_geometry(self, tablename, shape, element_id, additional_columns={}):
        """insert geometry with spec. id into given table """
        self.show_output()
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

    def show_output(self, redraw=False):
        infrastrukturmengen_bilanzieren.show_output(redraw=False)

    def get_ids(self, tablename):
        project=config.active_project
        table = folders.get_table(tablename,
                                  workspace='FGDB_Kosten.gdb',
                                  project=project)
        cursor = arcpy.da.SearchCursor(table, ['OBJECTID'])
        ids = [row[0] for row in cursor]
        del(cursor)
        return ids


class LineTool(DrawingTool):
    table = 'Erschliessungsnetze_Linienelemente'

    def __init__(self):
        super(LineTool, self).__init__()
        self.shape = "Line"

    def onLine(self, line_geometry):
        self.commit_geometry(self.table, line_geometry, self._id_netzelement)


class PointTool(DrawingTool):
    table = 'Erschliessungsnetze_Punktelemente'

    def __init__(self):
        super(PointTool, self).__init__()
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


class AnliegerstrasseInnere(LineTool):
    """Implementation for rpc_tools.anliegerstrasse_innere (Tool)"""
    _id_netzelement = 11


class SammelstrasseInnere(LineTool):
    """Implementation for rpc_tools.sammelstrasse_innere (Tool)"""
    _id_netzelement = 12


class LagePunktuelleMassnahmeStrasseInnere(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_strasse_innere (Tool)"""
    _id_netzelement = 13


class BeschreibungPunktuelleMassnahmeStrasseInnere(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_innere (Button)"""
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


class BeschreibungPunktuelleMassnahmeStrasseAeussere(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_strasse_auessere (Button)"""
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


class BeschreibungPunktuelleMassnahmeKanalisation(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_kanalisation (Button)"""
    _id_netzelement = 24


class Trinkwasserleitung(LineTool):
    """Implementation for rpc_tools.trinkwasserleitung (Tool)"""
    _id_netzelement = 31


class LagePunktuelleMassnahmeTrinkwasser(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_trinkwasser (Tool)"""
    _id_netzelement = 32


class BeschreibungPunktuelleMassnahmeTrinkwasser(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_trinkwasser (Button)"""
    _id_netzelement = 32


class Stromleitung(LineTool):
    """Implementation for rpc_tools.stromleitung (Tool)"""
    _id_netzelement = 41


class LagePunktuelleMassnahmeElektrizitaet(PointTool):
    """Implementation for rpc_tools.lage_punktuelle_massnahme_elektrizitaet (Tool)"""
    _id_netzelement = 42


class BeschreibungPunktuelleMassnahmeElektrizitaet(Beschreibung):
    """Implementation for rpc_tools.beschreibung_punktuelle_massnahme_elektrizitaet (Button)"""
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


class InfrastrukturmengenBilanzieren(ToolboxButton):
    """Implementation for rpc_tools.infrastrukturmengen_bilanzieren (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxInfrastrukturmengenBilanz'
    _do_show = False

    def show_output(self, redraw=False):
        self.tbx.set_active_project()
        if redraw or not self.tbx.tool.output.layer_exists(
            'Wirkungsbereich 5 - Infrastrukturfolgekosten'):
            self.tbx.tool.add_output()


class ErschliessungsnetzeAnzeigen(object):
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        infrastrukturmengen_bilanzieren.show_output(redraw=True)


### NUTZUNGEN ###


class NutzungenDefinieren(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxTeilflaecheVerwalten'


class Wohnen(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenWohnen'


class Gewerbe(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenGewerbe'


class Einzelhandel(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenEinzelhandel'


### BEWOHNER ARBEISTPLAETZE ###


class BewohnerSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Bewohner_Arbeitsplaetze.pyt'
    _toolbox_name = 'TbxBewohner'


class ArbeitsplaetzeSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.arbeitsplaetze_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Bewohner_Arbeitsplaetze.pyt'
    _toolbox_name = 'TbxArbeitsplaetze'


### EINNAHMEN ###


class WanderungssaldenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxWanderungssalden'


class Einwohnersalden(ToolboxButton):
    """Implementation for rpc_tools.einwohnersalden (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxEWSaldenbearbeiten'


class Beschaeftigtensalden(ToolboxButton):
    """Implementation for rpc_tools.beschaeftigtensalden (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxGewSaldenbearbeiten'


class EinnahmeverschiebungenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.einnahmeverschiebungen_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxSteuersalden'
    
    
### VERKEHR ###
    
class InitialRouting(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxRouting'


class RoutingSettings(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxSettings'


class WeightedRouting(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxUpdateNodes'


class Anbindungspunkt(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxSetSource'

    def __init__(self):
        super(Anbindungspunkt, self).__init__()
        self.enabled = True
        self.shape = 'NONE'
        self.cursor = 3

    def onMouseDownMap(self, x, y, button, shift):
        config.active_coord = (x, y)
        self.onClick()
        
        
### Standortkonkurrenz ###
        
        
class BestandOSMEinlesen(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxStandortkonkurrenz'
    _do_show = False

    
class BestandEinlesen(object):
    pass


class BestandMarktHinzu(object):
    pass


class BestandMarktEntfernen(object):
    pass


class BestandMarktBearbeiten(object):
    pass


class PlanfallMarktErweitern(object):
    pass


class PlanfallMarktHinzu(object):
    pass


class PlanfallMarktEntfernen(object):
    pass


class PlanfallMarktBearbeiten(object):
    pass

if __name__ == "__main__":
    t = PointTool()
    t.get_ids(t.table)