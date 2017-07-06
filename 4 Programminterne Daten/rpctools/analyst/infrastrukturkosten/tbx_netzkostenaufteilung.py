# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool, Folders
from rpctools.utils.encoding import encode
from rpctools.analyst.infrastrukturkosten.kostenkennwerte_hilfsfunktionen \
     import kostenkennwerte
import numpy as np
import pandas as pd


class NetzKostenaufteilung(Tool):
    def add_outputs(self):
        pass
    def run(self):
        pass



class TbxNetzKostenaufteilung(Tbx):
    _workspace = 'FGDB_Kosten.gdb'
    @property
    def label(self):
        return encode(u'Kostenaufteilung festlegen')

    @property
    def Tool(self):
        return NetzKostenaufteilung

    def _open(self, params):
        pass

    def _updateParameters(self, params):
        return params

    def _getParameterInfo(self):
        df_defaults = ["benutzerdefinierte Aufteilung"]  # existiert noch nicht: self.table_to_dataframe('Aufteilungsregeln', _workspace)
        params = self.par
        projekte = self.folders.get_projects()
        category_EH = "Einmalige Herstellung"
        category_BU = "Betrieb und Unterhaltung"
        category_EN = "Erneuerung"
        # Projekt_auswählen
        p = self.add_parameter('project')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt auswählen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = projekte
        if projekte:
            p.value = projekte[0]
        # Netz
        p = self.add_parameter('network')
        p.name = u'network'.encode('cp1252')
        p.displayName = u'Netz'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        network = ["Straße (innere Erschließung)",
                   "Straße (äußere Erschließung)", "Kanalisation",
                   "Trinkwasser", "Elektrizität"]
        p.filter.list = network

        # category = EH
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_EH")
        p.name = u"default_EH".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = df_defaults
        p.value = df_defaults[0]
        p.category = category_EH
        # Grundstücksbesitzer
        p = self.add_parameter("owner_EH")
        p.name = u"owner_EH".encode("cp1252")
        p.displayName = u"Kostenanteil der GrundstücksbesitzerInnen (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EH
        # Gemeinde
        p = self.add_parameter("community_EH")
        p.name = u"community_EH".encode("cp1252")
        p.displayName = u"Kostenanteil der Gemeinde (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EH
        # Nutzer
        p = self.add_parameter("users_EH")
        p.name = u"users_EH".encode("cp1252")
        p.displayName = u"Kostenanteil der Allgemeinheit der Netznutzer und Tarifkunden (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EH

        # category = BU
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_BU")
        p.name = u"default_BU".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = df_defaults
        p.value = df_defaults[0]
        p.category = category_BU
        # Grundstücksbesitzer
        p = self.add_parameter("owner_BU")
        p.name = u"owner_BU".encode("cp1252")
        p.displayName = u"Kostenanteil der GrundstücksbesitzerInnen (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_BU
        # Gemeinde
        p = self.add_parameter("community_BU")
        p.name = u"community_BU".encode("cp1252")
        p.displayName = u"Kostenanteil der Gemeinde (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_BU
        # Nutzer
        p = self.add_parameter("users_BU")
        p.name = u"users_BU".encode("cp1252")
        p.displayName = u"Kostenanteil der Allgemeinheit der Netznutzer und Tarifkunden (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_BU

        # category = EN
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_EN")
        p.name = u"default_EN".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = df_defaults
        p.value = df_defaults[0]
        p.category = category_EN
        # Grundstücksbesitzer
        p = self.add_parameter("owner_EN")
        p.name = u"owner_EN".encode("cp1252")
        p.displayName = u"Kostenanteil der GrundstücksbesitzerInnen (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EN
        # Gemeinde
        p = self.add_parameter("community_EN")
        p.name = u"community_EN".encode("cp1252")
        p.displayName = u"Kostenanteil der Gemeinde (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EN
        # Nutzer
        p = self.add_parameter("users_EN")
        p.name = u"users_EN".encode("cp1252")
        p.displayName = u"Kostenanteil der Allgemeinheit der Netznutzer und Tarifkunden (in Prozent)".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = "Range"
        p.filter.list = [0, 100]
        p.category = category_EN

        return params
