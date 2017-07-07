# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool, Folders
from rpctools.utils.encoding import encode
from rpctools.analyst.infrastrukturkosten.kostenkennwerte_hilfsfunktionen \
     import kostenkennwerte
import numpy as np
import pandas as pd


class NetzKostenaufteilung(Tool):
    _workspace = 'FGDB_Kosten.gdb'
    _param_projectname = 'project'

    def add_outputs(self):
        pass
    def run(self):
        tbx = self.parent_tbx
        arcpy.AddMessage(tbx.df_results)
        return



class TbxNetzKostenaufteilung(Tbx):
    _workspace = 'FGDB_Kosten.gdb'
    _netztyp = None
    #_df_results.loc[:, 'owner'] = 100
    #_df_dummy_values = pd.DataFrame(index=['EH', 'BU', 'EN'],
                               #columns=['owner', 'community', 'users'],
                               #data=0, dtype='int')
    #_df_dummy_values.loc[:, 'owner'] = 100
    #_df_dummy_values = _df_dummy_values.astype(int, copy=False)

    @property
    def label(self):
        return encode(u'Kostenaufteilung festlegen')

    @property
    def Tool(self):
        return NetzKostenaufteilung

    def _open(self, params):
        params.default_EH.value = self.initial_settings[0]
        params.default_BU.value = self.initial_settings[0]
        params.default_EN.value = self.initial_settings[0]
        # set params:
        params.community_EH.value = self.df_results.loc['EH', 'Anteil_GEM']
        params.owner_EH.value = self.df_results.loc['EH', 'Anteil_GSB']
        params.users_EH.value = self.df_results.loc['EH', 'Anteil_ALL']
        params.community_BU.value = self.df_results.loc['BU', 'Anteil_GEM']
        params.owner_BU.value = self.df_results.loc['BU', 'Anteil_GSB']
        params.users_BU.value = self.df_results.loc['BU', 'Anteil_ALL']
        params.community_EN.value = self.df_results.loc['EN', 'Anteil_GEM']
        params.owner_EN.value = self.df_results.loc['EN', 'Anteil_GSB']
        params.users_EN.value = self.df_results.loc['EN', 'Anteil_ALL']


    def _updateParameters(self, params):
        # check if other default settings were choosen
        if self.par.changed('default_EH'):
            if params.default_EH.value != u"benutzerdefinierte Einstellungen":
                params.community_EH.value =  self._df_defaults.loc[params.default_EH.value, "Anteil_GEM"]
                params.owner_EH.value =  self._df_defaults.loc[params.default_EH.value, "Anteil_GSB"]
                params.users_EH.value =  self._df_defaults.loc[params.default_EH.value, "Anteil_ALL"]
        if self.par.changed('default_BU'):
            if params.default_BU.value != u"benutzerdefinierte Einstellungen":
                params.community_BU.value =  self._df_defaults.loc[params.default_BU.value, "Anteil_GEM"]
                params.owner_BU.value =  self._df_defaults.loc[params.default_BU.value, "Anteil_GSB"]
                params.users_BU.value =  self._df_defaults.loc[params.default_BU.value, "Anteil_ALL"]
        if self.par.changed('default_EN'):
            if params.default_EN.value != u"benutzerdefinierte Einstellungen":
                params.community_EN.value =  self._df_defaults.loc[params.default_EN.value, "Anteil_GEM"]
                params.owner_EN.value =  self._df_defaults.loc[params.default_EN.value, "Anteil_GSB"]
                params.users_EN.value =  self._df_defaults.loc[params.default_EN.value, "Anteil_ALL"]
        # check if range-filter has changed
        # EH

        self.df_results.loc['EH', 'Anteil_GEM'] = params.community_EH.value
        self.df_results.loc['EH', 'Anteil_GSB'] = params.owner_EH.value
        self.df_results.loc['EH', 'Anteil_ALL'] = params.users_EH.value
        if not self.par.changed('default_EH'):
            params.default_EH.value = u"benutzerdefinierte Einstellungen"
        # BU

        self.df_results.loc['BU', 'Anteil_GEM'] = params.community_BU.value
        self.df_results.loc['BU', 'Anteil_GSB'] = params.owner_BU.value
        self.df_results.loc['BU', 'Anteil_ALL'] = params.users_BU.value
        if not self.par.changed('default_BU'):
            params.default_BU.value = u"benutzerdefinierte Einstellungen"
        # EN

        self.df_results.loc['EN', 'Anteil_GEM'] = params.community_EN.value
        self.df_results.loc['EN', 'Anteil_GSB'] = params.owner_EN.value
        self.df_results.loc['EN', 'Anteil_ALL'] = params.users_EN.value
        if not self.par.changed('default_EN'):
            params.default_EN.value = u"benutzerdefinierte Einstellungen"

        return params

    def _getParameterInfo(self):
        params = self.par
        projekte = self.folders.get_projects()
        # get initial data
        self.initial_settings = [u"Investoren / Grundstücksbesitzer zahlen alles"] * 3
        self._df_defaults = self.table_to_dataframe('Aufteilungsregeln', columns=[],
                                                   workspace='FGDB_Kosten_Tool.gdb',
                                                   where=None,
                                                   pkey='',
                                                   project='',
                                                   is_base_table=True)
        self._df_defaults.index = self._df_defaults["Aufteilungsregel"]
        self._df_defaults.loc[:, ["Anteil_GSB", "Anteil_GEM", "Anteil_ALL"]] = \
            self._df_defaults.loc[:, ["Anteil_GSB", "Anteil_GEM", "Anteil_ALL"]].astype(int)
        self.df_results = self._df_defaults.loc[self.initial_settings,
                                                ["Anteil_GSB", "Anteil_GEM",
                                                 "Anteil_ALL"]].copy()
        self.df_results.index = ["EH", "BU", "EN"]
        self.df_results = self.df_results.astype(int)

        default_list = list(self._df_defaults.Aufteilungsregel)
        default_list.append(u"benutzerdefinierte Einstellungen")


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
        p.value = network[0]

        # category = EH
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_EH")
        p.name = u"default_EH".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = default_list
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
        self.add_dependency(['owner_EH', 'community_EH', 'users_EH'], 100)

        # category = BU
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_BU")
        p.name = u"default_BU".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = default_list
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
        self.add_dependency(['owner_BU', 'community_BU', 'users_BU'], 100)

        # category = EN
        # Nachfolgende Werte setzen auf
        p = self.add_parameter("default_EN")
        p.name = u"default_EN".encode("cp1252")
        p.displayName = u"Nachfolgende Werte setzen auf ...".encode("cp1252")
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = default_list
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
        self.add_dependency(['owner_EN', 'community_EN', 'users_EN'], 100)

        return params

class TbxNetzKostenaufteilungInnere(TbxNetzKostenaufteilung):
    _netztyp = 1

if __name__ == '__main__':
    t = TbxNetzKostenaufteilung()
    t._getParameterInfo()
    t.par.project.value = t.config.active_project
    t._open(t.par)
    t._updateParameters(t.par)
    t.execute()
