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
        arcpy.AddMessage(tbx._df_results)
        return



class TbxNetzKostenaufteilung(Tbx):
    _workspace = 'FGDB_Kosten.gdb'
    _df_results = pd.DataFrame(index=['EH', 'BU', 'EN'],
                               columns=['owner', 'community', 'users'],
                               data=0, dtype='int')

    _df_results.loc[:, 'owner'] = 100
    _df_dummy_values = pd.DataFrame(index=['EH', 'BU', 'EN'],
                               columns=['owner', 'community', 'users'],
                               data=0, dtype='int')
    _df_dummy_values.loc[:, 'owner'] = 100
    _df_dummy_values = _df_dummy_values.astype(int, copy=False)

    @property
    def label(self):
        return encode(u'Kostenaufteilung festlegen')

    @property
    def Tool(self):
        return NetzKostenaufteilung

    def _open(self, params):
        params.default_EH.value = self._df_defaults[0]
        # set params:
        params.community_EH.value = self._df_dummy_values.loc['EH', 'community']
        params.owner_EH.value = self._df_dummy_values.loc['EH', 'owner']
        params.users_EH.value = self._df_dummy_values.loc['EH', 'users']
        params.community_BU.value = self._df_dummy_values.loc['BU', 'community']
        params.owner_BU.value = self._df_dummy_values.loc['BU', 'owner']
        params.users_BU.value = self._df_dummy_values.loc['BU', 'users']
        params.community_EN.value = self._df_dummy_values.loc['EN', 'community']
        params.owner_EN.value = self._df_dummy_values.loc['EN', 'owner']
        params.users_EN.value = self._df_dummy_values.loc['EN', 'users']


    def _updateParameters(self, params):
        # EH
        if self.par.changed('community_EH', 'owner_EH', 'users_EH'):
            self._df_results.loc['EH', 'community'] = params.community_EH.value
            self._df_results.loc['EH', 'owner'] = params.owner_EH.value
            self._df_results.loc['EH', 'users'] = params.users_EH.value
        # BU
        if self.par.changed('community_BU', 'owner_BU', 'users_BU'):
            self._df_results.loc['BU', 'community'] = params.community_BU.value
            self._df_results.loc['BU', 'owner'] = params.owner_BU.value
            self._df_results.loc['BU', 'users'] = params.users_BU.value
        # EN
        if self.par.changed('community_EN', 'owner_EN', 'users_EN'):
            self._df_results.loc['EN', 'community'] = params.community_EN.value
            self._df_results.loc['EN', 'owner'] = params.owner_EN.value
            self._df_results.loc['EN', 'users'] = params.users_EN.value
        return params

    def _getParameterInfo(self):
        params = self.par
        projekte = self.folders.get_projects()
        self.df_defaults = self.table_to_dataframe(
            'Aufteilungsregeln', workspace='FGDB_Kosten_Tool.gdb',
            is_base_table=True)


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
        p.filter.list = self._df_defaults
        p.value = self._df_defaults[0]
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
        p.filter.list = self._df_defaults
        p.value = self._df_defaults[0]
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
        p.filter.list = self._df_defaults
        p.value = self._df_defaults[0]
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


if __name__ == '__main__':
    t = TbxNetzKostenaufteilung()
    t._getParameterInfo()
    t.par.project.value = t.config.active_project
    t._open(t.par)
    t._updateParameters(t.par)
    t.execute()
