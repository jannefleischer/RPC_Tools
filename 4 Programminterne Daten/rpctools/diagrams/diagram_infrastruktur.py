# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from rpctools.utils.diagrams import Diagram, show_diagram


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
            
        fig, ax = plt.subplots()
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, costs, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        
        #plt.rcdefaults()
        #fig, ax = plt.subplots()
    
        ## Example data
        #people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
        #y_pos = np.arange(len(people))
        #performance = 3 + 10 * np.random.rand(len(people))
        #error = np.random.rand(len(people))
    
        #ax.barh(y_pos, performance, xerr=error, align='center',
                #color='green', ecolor='black')
        #ax.set_yticks(y_pos)
        #ax.set_yticklabels(people)
        #ax.invert_yaxis()  # labels read top-to-bottom
        #ax.set_xlabel('Performance')
        #ax.set_title('How fast do you want to go today?')
        

if __name__ == "__main__":
    show_diagram(globals())
