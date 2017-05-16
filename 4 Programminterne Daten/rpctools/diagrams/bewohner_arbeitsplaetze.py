# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from rpctools.utils.diagrams import Diagram
import matplotlib.ticker as mticker
import pandas as pd


class BewohnerEntwicklung(Diagram):
    def _create(self, **kwargs):
        self.title = (u"{}: Geschätzte Einwohnerentwicklung".format(
            self.par._get_projectname()))
        
        flaechen_id = kwargs['flaechen_id']
        
        table = 'Bewohner_nach_Altersgruppe_und_Jahr'
        workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
        table_df = self.table_to_dataframe(
            table, workspace=workspace,
            where='IDTeilflaeche={}'.format(flaechen_id))
        groups = table_df['Altersklasse'].unique()
        colors = plt.cm.viridis_r(np.linspace(0, 1, len(groups)))
        transformed = pd.DataFrame(columns=groups)
        
        grouped = table_df.groupby(by='Altersklasse')
        for name, group_data in grouped:
            group_data.sort('Jahr', inplace=True)
            transformed[name] = group_data['Bewohner'].values
        xticks = table_df['Jahr'].unique()
        xticks.sort()
        ax = transformed.plot(kind='bar', stacked=True, figsize=(15, 8),
                              color=colors, title=self.title)
        ax.set_xticklabels(xticks, rotation=45)
        return ax.figure


if __name__ == "__main__":
    diagram = BewohnerEntwicklung()
    diagram.create(projectname='1', flaechen_id=1)
    diagram.show()