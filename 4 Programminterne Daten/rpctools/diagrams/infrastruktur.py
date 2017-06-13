# -*- coding: utf-8 -*-

import numpy as np
from rpctools.utils.diagram import MatplotDiagram
import matplotlib.ticker as mticker


class Netzlaenge(MatplotDiagram):
    
    def _create(self, **kwargs):
        line_table = 'Erschliessungsnetze_Linienelemente'
        self.title = (u"{}: Länge der zusätzlichen Infrastrukturnetze "
                 u"(ohne punktuelle Maßnahmen)".format(
                     self.par.get_projectname()))
        x_label = u"Meter zusätzliche Netzlänge (ohne punktuelle Maßnahmen)"
        
        linien_df = self.table_to_dataframe(
            line_table, columns=['SHAPE_Length', 'IDNetz'],
            workspace='FGDB_Kosten.gdb'
        )
        base_df = self.table_to_dataframe(
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
            self.par.get_projectname())
        x_label = u"Kosten der punktuellen Maßnahmen"
        
        point_df = self.table_to_dataframe(
            point_table, workspace='FGDB_Kosten.gdb')
        base_df = self.table_to_dataframe(
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
            costs.append(grouped_df['Kosten_EH_EUR'].sum())
            
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

if __name__ == "__main__":
    netz_diagram = Netzlaenge()
    netz_diagram.create()
    netz_diagram.show()
    kosten_diagram = MassnahmenKosten()
    kosten_diagram.create()
    kosten_diagram.show()
