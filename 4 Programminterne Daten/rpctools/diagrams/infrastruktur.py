# -*- coding: utf-8 -*-

import numpy as np
from rpctools.utils.diagram import MatplotDiagram
import matplotlib.ticker as mticker


class Netzlaenge(MatplotDiagram):
    
    def _create(self, **kwargs):
        line_table = 'Erschliessungsnetze_Linienelemente'
        self.title = (u"{}: Länge der zusätzlichen Infrastrukturnetze "
                 u"(ohne punktuelle Maßnahmen)".format(
                     self.tbx.par.get_projectname()))
        x_label = u"Meter zusätzliche Netzlänge (ohne punktuelle Maßnahmen)"
        
        linien_df = self.tbx.table_to_dataframe(
            line_table, columns=['SHAPE_Length', 'IDNetz'],
            workspace='FGDB_Kosten.gdb'
        )
        base_df = self.tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)
        joined = linien_df.merge(base_df, on='IDNetz', how='right')
        joined.fillna(0, inplace=True)
        grouped = joined.groupby(by='IDNetz')
        categories = []
        lengths = []
        for id_netz, grouped_df in grouped:
            categories.append(grouped_df['Netz'].values[0])
            lengths.append(grouped_df['SHAPE_Length'].sum())
            
        figure, ax = self.plt.subplots(figsize=(8, 4))
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, lengths, height=0.3, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.grid(True, which='major')
        
        return ax
    

class MassnahmenKosten(MatplotDiagram):
    
    def _create(self, **kwargs):
        point_table = 'Erschliessungsnetze_Punktelemente'
        self.title = u"{}: Kosten der punktuellen Maßnahmen".format(
            self.tbx.par.get_projectname())
        x_label = u"Kosten der punktuellen Maßnahmen"
        
        point_df = self.tbx.table_to_dataframe(
            point_table, workspace='FGDB_Kosten.gdb')
        base_df = self.tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)

        joined = point_df.merge(base_df, on='IDNetz', how='right')
        joined.fillna(0, inplace=True)
        grouped = joined.groupby(by='IDNetz')
        categories = []
        costs = []
        for id_netz, grouped_df in grouped:
            categories.append(grouped_df['Netz'].values[0])
            costs.append(grouped_df['Euro_EH'].sum())
            
        figure, ax = self.plt.subplots(figsize=(8, 4))
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, costs, height=0.3, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')
        
        return ax


class GesamtkostenDiagramm(MatplotDiagram):
    
    def _create(self, **kwargs):
        workspace = 'FGDB_Kosten.gdb'
        table = 'Gesamtkosten'
        self.title = u"{}: Gesamtkosten der infrastrukturellen Maßnahmen".format(
            self.tbx.par.get_projectname())
        x_label = u"Kosten für Netzerweiterungen und punktuelle Maßnahmen"
        
        df_costs = self.tbx.table_to_dataframe(
            table, workspace=workspace
        )
        
        u, u_idx = np.unique(df_costs['Netz'], return_index=True)
        categories = df_costs['Netz'][np.sort(u_idx)]
        
        pos_idx = np.arange(len(categories))
        
        bar_width = 0.2
        
        figure, ax = self.plt.subplots(figsize=(8, 4))
        grouped = df_costs.groupby(by='IDKostenphase')
        phase_names = []
        for i, (phase_id, group) in enumerate(grouped):
            costs = group['Euro']
            ax.barh(pos_idx + i * bar_width, costs, height=bar_width,
                    align='center')
            phase_names.append(group['Kostenphase'].values[0])
            
        ax.set_yticks(pos_idx + bar_width / 3)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')
        
        ax.legend(phase_names, loc='upper right')
        return ax


if __name__ == "__main__":
    kosten_diagram = GesamtkostenDiagramm()
    kosten_diagram.create()
    kosten_diagram.show()
