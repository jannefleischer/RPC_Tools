# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool, Folders
from rpctools.utils.encoding import encode
import numpy as np
import pandas as pd
import time


class KostenkennwerteKontrollieren(Tool):
    _workspace = 'FGDB_Kosten.gdb'
    _param_projectname = 'project'
    _table = 'Kostenkennwerte_Linienelemente'

    def add_outputs(self):
        pass

    def run(self):
        tbx = self.parent_tbx
        tbx.dataframe_to_table(self._table, tbx.df_costs,
                               pkeys=['ID'], workspace=self._workspace)
        return


class TbxKostenkennwerteKontrollieren(Tbx):
    _table = 'Kostenkennwerte_Linienelemente'
    @property
    def label(self):
        return encode(u'Kostenkennwerte kontrollieren')

    @property
    def Tool(self):
        return KostenkennwerteKontrollieren

    def _open(self, params):
        # if Kostenkennwerte_Linienelemente does not exist, create the table
        # initially
        self.kostenkennwerte()
        df_costs = self.table_to_dataframe(self._table,
                                           workspace='FGDB_Kosten.gdb')
        self.df_costs = df_costs
        network_elements = list(self.df_costs.Netzelement)
        params.network.filter.list = network_elements
        params.network.value = network_elements[0]
        params.costs_EH.value = int(self.df_costs.Euro_EH[0])
        params.costs_BU.value = int(self.df_costs.Cent_BU[0])
        params.costs_EN.value = int(self.df_costs.Euro_EN[0])
        params.lifespan.value = int(self.df_costs.Lebensdauer[0])

    def get_from_df(self, df, columns, df_id):
        df_selected = df.loc[df_id, (columns)]
        return df_selected


    def _updateParameters(self, params):
        condition = params.network.value
        df_id = self.df_costs[self.df_costs.Netzelement == condition].index
        if self.par.changed('network'):
            # set tbx parameters initially
            df_selected = self.get_from_df(self.df_costs,
                                         ['Euro_EH', 'Cent_BU',
                                          'Euro_EN', 'Lebensdauer'], df_id)
            params.costs_EH.value = int(df_selected.Euro_EH)
            params.costs_BU.value = int(df_selected.Cent_BU)
            params.costs_EN.value = int(df_selected.Euro_EN)
            params.lifespan.value = int(df_selected.Lebensdauer)
            return params
        # update df_costs, if tbx parameters have changed
        if self.par.changed('costs_EH'):
            self.df_costs.loc[df_id, ('Euro_EH')] = self.par.costs_EH.value
        if self.par.changed('costs_BU'):
            self.df_costs.loc[df_id, ('Cent_BU')] = self.par.costs_BU.value
        if self.par.changed('costs_EN'):
            self.df_costs.loc[df_id, ('Euro_EN')] = self.par.costs_EN.value
        if self.par.changed('lifespan'):
            self.df_costs.loc[df_id, ('Lebensdauer')] = self.par.lifespan.value
        return params

    def _getParameterInfo(self):
        params = self.par
        projekte = self.folders.get_projects()

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
        # Netzelement
        p = self.add_parameter('network')
        p.name = u'network'.encode('cp1252')
        p.displayName = u'Netzelement'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        # Kosten EH
        p = self.add_parameter('costs_EH')
        p.name = u'costs_EH'.encode('cp1252')
        p.displayName = u'Kosten der erstmaligen Herstellung: EUR pro laufenen Meter'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Kosten BU
        p = self.add_parameter('costs_BU')
        p.name = u'costs_BU'.encode('cp1252')
        p.displayName = u'Jährliche Kosten für Betrieb und Unterhaltung: Cent pro laufenden Meter und Jahr'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Kosten EN
        p = self.add_parameter('costs_EN')
        p.name = u'costs_EN'.encode('cp1252')
        p.displayName = u'Kosten der Erneuerung: Euro pro laufenden Meter und Erneuerungszyklus'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Lebensdauer
        p = self.add_parameter('lifespan')
        p.name = u'lifespan'.encode('cp1252')
        p.displayName = u'Lebensdauer: Jahre zwischen den Erneuerungszyklen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]

        return params

    def kostenkennwerte(self):
        # check if table Kostenkennwerte_Linienelemente contains content
        df_costs_line_elements = self.table_to_dataframe(
            self._table, workspace='FGDB_Kosten.gdb')
        if len(df_costs_line_elements) != 0:
            return
        # calculate time factor
        current_year = int(time.strftime("%Y"))
        df_frame_data = self.table_to_dataframe('Rahmendaten',
                                            workspace='FGDB_Kosten_Tool.gdb',
                                            is_base_table=True)
        interest = df_frame_data['Zins']
        reference_year = df_frame_data['Stand_Kostenkennwerte']
        time_factor = (1 + interest) ** (current_year - reference_year)
        # get regional factor
        ags = self.query_table('Projektrahmendaten',
                              workspace='FGDB_Definition_Projekt.gdb',
                              columns=['AGS'])[0][0]
        regional_factor = self.table_to_dataframe(
            'bkg_gemeinden', workspace='FGDB_Basisdaten_deutschland.gdb',
            columns=['BKI_Regionalfaktor'], where="AGS='{}'".format(str(ags)),
            is_base_table=True)
        # fill table Kostenkennwerte_Linienelemente
        regional_time_factor = time_factor * \
            regional_factor.loc[:, 'BKI_Regionalfaktor']
        rounding_factor = 5
        df_networks = self.table_to_dataframe('Netze_und_Netzelemente',
                                             workspace='FGDB_Kosten_Tool.gdb',
                                             where="Typ='{}'".format('Linie'),
                                             is_base_table=True)
        # multiply with factors
        df_networks.loc[:, ['Euro_EH', 'Cent_BU', 'Euro_EN']] *= \
            regional_time_factor[0]
        # round to 5
        df_networks.loc[:, ['Euro_EH', 'Cent_BU', 'Euro_EN']] = \
            self.round_df_to(
                df_networks.loc[:, ['Euro_EH', 'Cent_BU', 'Euro_EN']],
                rounding_factor)

        self.dataframe_to_table(self._table, df_networks,
                               pkeys=['ID'], workspace='FGDB_Kosten.gdb',
                               upsert=True)
        return

    def round_df_to(self, df, rounding_factor):
        df = df / rounding_factor
        df = df.apply(pd.Series.round)
        df *= rounding_factor
        df = df.astype('int')
        return df

if __name__ == '__main__':
    t = TbxKostenkennwerteKontrollieren()
    t._getParameterInfo()
    t.par.project.value = t.config.active_project
    t._open(t.par)
    t._updateParameters(t.par)
    t.execute()
