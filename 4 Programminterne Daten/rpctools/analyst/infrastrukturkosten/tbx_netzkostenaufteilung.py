# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool, Folders
from rpctools.utils.encoding import encode
from rpctools.analyst.infrastrukturkosten.kostenkennwerte_hilfsfunktionen \
     import kostenaufteilung_startwerte
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
    _netztyp = 1
    _has_been_opened = False

    @property
    def label(self):
        return encode(u'Kostenaufteilung festlegen')

    @property
    def Tool(self):
        return NetzKostenaufteilung

    def update_df(self, params, id_kostenphase):
        """
        update df_results with toolbox values
        id_kostenphase : list
        """

        for id_to_set in id_kostenphase:
            if id_to_set == 1:
                params_to_set = [params.owner_EH.value, params.community_EH.value, params.users_EH.value]
            elif id_to_set == 2:
                params_to_set = [params.owner_BU.value, params.community_BU.value, params.users_BU.value]
            elif id_to_set == 3:
                params_to_set = [params.owner_EN.value, params.community_EN.value, params.users_EN.value]
            self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == id_to_set), ["Anteil_GSB", "Anteil_GEM", "Anteil_ALL"]] = params_to_set



    def set_params(self, params, id_kostenphase):
        """
        sets the toolbox values for EH:1, BU:2 or EN:3
        params : params
        id_kostenphase : list
        """
        for id_to_set in id_kostenphase:
            if id_to_set == 1:
                params_to_set = [params.owner_EH, params.community_EH, params.users_EH]
            elif id_to_set == 2:
                params_to_set = [params.owner_BU, params.community_BU, params.users_BU]
            elif id_to_set == 3:
                params_to_set = [params.owner_EN, params.community_EN, params.users_EN]

            owner, community, users = params_to_set
            owner.value = int(self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == id_to_set), 'Anteil_GSB'])
            community.value = int(self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == id_to_set), 'Anteil_GEM'])
            users.value = int(self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == id_to_set), 'Anteil_ALL'])


    def _open(self, params):
        # get initial data
        kostenaufteilung_startwerte(self.par.get_projectname())
        self.df_results = self.table_to_dataframe('Kostenaufteilung', workspace=self._workspace)
        self.df_results = self.df_results.astype(int)
        self.df_results = pd.merge(self.df_results, self._df_defaults.loc[:, ['IDKostenregel', 'Aufteilungsregel']], on='IDKostenregel')
        params.default_EH.value = self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 1), 'Aufteilungsregel'].values[0]
        params.default_BU.value = self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 2), 'Aufteilungsregel'].values[0]
        params.default_EN.value = self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 3), 'Aufteilungsregel'].values[0]
        # set params:
        self.set_params(params, [1, 2, 3])


    def _updateParameters(self, params):
        if not self._has_been_opened:
            self._has_been_opened = True
            return params
        # check if other default settings were choosen
        if self.par.changed('default_EH'):
            if params.default_EH.value != u"benutzerdefinierte Einstellungen":
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 1), 'Aufteilungsregel'] = params.default_EH.value
                id_kostenregel = self._df_defaults.loc[self._df_defaults["Aufteilungsregel"] == params.default_EH.value, 'IDKostenregel'].values[0]
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 1), 'IDKostenregel'] = id_kostenregel
                # xxx Here is the problem!
                self.set_params(params, [1])
                self.update_df(params, [1])
        if self.par.changed('default_BU'):
            if params.default_BU.value != u"benutzerdefinierte Einstellungen":
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 2), 'Aufteilungsregel'] = params.default_BU.value
                id_kostenregel = self._df_defaults.loc[self._df_defaults["Aufteilungsregel"] == params.default_BU.value, 'IDKostenregel'].values[0]
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 2), 'IDKostenregel'] = id_kostenregel
                self.set_params(params, [2])
                self.update_df(params, [2])
        if self.par.changed('default_EN'):
            if params.default_EN.value != u"benutzerdefinierte Einstellungen":
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 3), 'Aufteilungsregel'] = params.default_EN.value
                id_kostenregel = self._df_defaults.loc[self._df_defaults["Aufteilungsregel"] == params.default_EN.value, 'IDKostenregel'].values[0]
                self.df_results.loc[(self.df_results["IDNetz"] == self._netztyp) & (self.df_results["IDKostenphase"] == 3), 'IDKostenregel'] = id_kostenregel
                self.set_params(params, [3])
                self.update_df(params, [3])
        # check if range-filter has changed
        # EH
        if self.par.changed('community_EH', 'owner_EH', 'users_EH'):
            self.update_df(params, [1])
            params.default_EH.value = u"benutzerdefinierte Einstellungen"
        # BU
        if self.par.changed('community_BU', 'owner_BU', 'users_BU'):
            self.update_df(params, [2])
            params.default_BU.value = u"benutzerdefinierte Einstellungen"
        # EN
        if self.par.changed('community_EN', 'owner_EN', 'users_EN'):
            self.update_df(params, [3])
            params.default_EN.value = u"benutzerdefinierte Einstellungen"
        return params

    def _getParameterInfo(self):
        params = self.par
        projekte = self.folders.get_projects()
        self._df_defaults = self.table_to_dataframe('Aufteilungsregeln', columns=[],
                                                   workspace='FGDB_Kosten_Tool.gdb',
                                                   where=None,
                                                   pkey='',
                                                   project='',
                                                   is_base_table=True)
        self._df_defaults.rename(columns={'IDAufteilungsregel': 'IDKostenregel',}, inplace=True)
        self._df_defaults.index = self._df_defaults["Aufteilungsregel"]
        self._df_defaults.loc[:, ["Anteil_GSB", "Anteil_GEM", "Anteil_ALL"]] = \
            self._df_defaults.loc[:, ["Anteil_GSB", "Anteil_GEM", "Anteil_ALL"]].astype(int)
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
