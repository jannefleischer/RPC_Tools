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

    def add_outputs(self):
        pass

    def run(self):
        self.kostenkennwerte()
        pass

    def kostenkennwerte(self):
        tbx = self.parent_tbx
        # check if table Kostenkennwerte_Linienelemente contains content
        df_costs_line_elements = tbx.table_to_dataframe(
            'Kostenkennwerte_Linienelemente', workspace='FGDB_Kosten.gdb')
        if len(df_costs_line_elements) != 0:
            return
        # calculate time factor
        current_year = int(time.strftime("%Y"))
        df_frame_data = tbx.table_to_dataframe('Rahmendaten',
                                            workspace='FGDB_Kosten_Tool.gdb',
                                            is_base_table=True)
        interest = df_frame_data['Zins']
        reference_year = df_frame_data['Stand_Kostenkennwerte']
        time_factor = (1 + interest) ** (current_year - reference_year)
        # get regional factor
        ags = tbx.query_table('Projektrahmendaten',
                              workspace='FGDB_Definition_Projekt.gdb',
                              columns=['AGS'])[0][0]
        regional_factor = tbx.table_to_dataframe(
            'bkg_gemeinden', workspace='FGDB_Basisdaten_deutschland.gdb',
            columns=['BKI_Regionalfaktor'], where="AGS='{}'".format(str(ags)),
            is_base_table=True)
        # fill table Kostenkennwerte_Linienelemente
        regional_time_factor = time_factor * \
            regional_factor.loc[:, 'BKI_Regionalfaktor']
        rounding_factor = 5
        df_networks = tbx.table_to_dataframe('Netze_und_Netzelemente',
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

        tbx.dataframe_to_table('Kostenkennwerte_Linienelemente', df_networks,
                               pkeys=['ID'], workspace='FGDB_Kosten.gdb',
                               upsert=True)
        return

    def round_df_to(self, df, rounding_factor):
        df = df / rounding_factor
        df = df.apply(pd.Series.round)
        df *= rounding_factor
        df = df.astype('int')
        return df

class TbxKostenkennwerteKontrollieren(Tbx):
    _opened_for_the_first_time = True
    @property
    def label(self):
        return encode(u'Kostenkennwerte kontrollieren')

    @property
    def Tool(self):
        return KostenkennwerteKontrollieren

    def _open(self, params):
        df_costs = self.table_to_dataframe('Kostenkennwerte_Linienelemente',
                                           workspace='FGDB_Kosten.gdb')
        self.df_costs = df_costs
        network_elements = list(self.df_costs.Netzelement)
        params.network.filter.list = network_elements
        params.network.value = network_elements[0]
        params.costs_EH.value = int(self.df_costs.Euro_EH[0])
        params.costs_BU.value = int(self.df_costs.Cent_BU[0])
        params.costs_EN.value = int(self.df_costs.Euro_EN[0])
        params.lifespan.value = int(self.df_costs.Lebensdauer[0])


    def _updateParameters(self, params):
        condition = params.network.value
        where= u"network = '{}'".format(condition)
        if self.par.changed('network'):
            costs_EH, costs_BU, costs_EN, lifespan = self.df_costs['Euro_EH', 'Cent_BU', 'Euro_EN', 'Lebensdauer'].where(where)
            params.costs_EH.value = costs_EH
            params.costs_BU.value = costs_BU
            params.costs_EN.value = costs_EN
            params.lifespan.value = lifespan
        return

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
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Kosten BU
        p = self.add_parameter('costs_BU')
        p.name = u'costs_BU'.encode('cp1252')
        p.displayName = u'Jährliche Kosten für Betrieb und Unterhaltung: Cent pro laufenden Meter und Jahr'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Kosten EN
        p = self.add_parameter('costs_EN')
        p.name = u'costs_EN'.encode('cp1252')
        p.displayName = u'Kosten der Erneuerung: Euro pro laufenden Meter und Erneuerungszyklus'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [0, 2000]
        # Lebensdauer
        p = self.add_parameter('lifespan')
        p.name = u'lifespan'.encode('cp1252')
        p.displayName = u'Lebensdauer: Jahre zwischen den Erneuerungszyklen'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'Long'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]



        return params


if __name__ == '__main__':
    t = TbxKostenkennwerteKontrollieren()
    t._getParameterInfo()
    t.par.project.value = t.config.active_project
    t._open(t.par)
    t._updateParameters(t.par)
    t.execute()
