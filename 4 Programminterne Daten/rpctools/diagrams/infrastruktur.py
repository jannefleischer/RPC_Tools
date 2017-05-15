# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from rpctools.utils.diagrams import Diagram


class InfrastrukturBilanzKosten(Diagram):
    
    def _create(self):
        _point_table = 'Erschliessungsnetze_Punktelemente'
        
        point_df = self.table_to_dataframe(
            _point_table, workspace='FGDB_Kosten.gdb')
        base_df = self.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)

        joined = point_df.merge(base_df, on='IDNetz', how='right')
        joined.fillna(0, inplace=True)
        grouped = joined.groupby(by='IDNetz')
        columns = ['Netz', 'Kosten_EH_EUR']
        categories = []
        costs = []
        for id_netz, grouped_df in grouped:
            categories.append(grouped_df['Netz'].values[0])
            costs.append(grouped_df['Kosten_EH_EUR'].sum())
            
        figure, ax = plt.subplots()
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, costs, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        
        return figure
        

if __name__ == "__main__":
    diagram = InfrastrukturBilanzKosten()
    diagram.create(projectname='1')
    diagram.show()
