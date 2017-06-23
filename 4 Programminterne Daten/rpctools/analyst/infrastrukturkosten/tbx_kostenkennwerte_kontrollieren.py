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
        regional_time_factor = time_factor * regional_factor.loc[:, 'BKI_Regionalfaktor']
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

    @property
    def label(self):
        return encode(u'Kostenkennwerte kontrollieren')

    @property
    def Tool(self):
        return KostenkennwerteKontrollieren

    def _open(self, params):
        pass

    def _updateParameters(self, params):

        pass

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

        return params


if __name__ == '__main__':
    t = TbxKostenkennwerteKontrollieren()
    t._getParameterInfo()
    t.par.project.value = t.config.active_project
    t._updateParameters(None)
    t.execute()
