# -*- coding: utf-8 -*-
import numpy as np
from rpctools.utils.diagram import Diagram
import matplotlib.ticker as mticker
import pandas as pd


class BewohnerEntwicklung(Diagram):
    def _create(self, **kwargs):
        flaechen_id = kwargs['flaechen_id']
        flaechen_name = kwargs['flaechen_name']
        self.title = (u"{} - {}: Geschätzte Einwohnerentwicklung".format(
            self.par.get_projectname(), flaechen_name))
        
        table = 'Bewohner_nach_Altersgruppe_und_Jahr'
        workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
        table_df = self.table_to_dataframe(
            table, workspace=workspace,
            where='IDTeilflaeche={}'.format(flaechen_id))
        groups = table_df['Altersklasse'].unique()
        colors = self.plt.cm.viridis_r(np.linspace(0, 1, len(groups)))
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
        return ax


class ArbeitsplatzEntwicklung(Diagram):
    def _create(self, **kwargs):
        flaechen_id = kwargs['flaechen_id']
        flaechen_name = kwargs['flaechen_name']
        self.title = (u"{} - {}: Geschätzte Anzahl Arbeitsplätze "
                      u"(Orientierungswerte)".format(
                          self.par.get_projectname(), flaechen_name))
        
        flaechen_id = kwargs['flaechen_id']
        
        table = 'AP_nach_Jahr'
        workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
        table_df = self.table_to_dataframe(
            table, workspace=workspace,
            columns=['Jahr', 'AP'], 
            where='IDTeilflaeche={}'.format(flaechen_id))
        table_df.sort('Jahr', inplace=True)
        ax = table_df.plot(x='Jahr', y='AP', kind='line', title=self.title,
                           color='r', legend=False, figsize=(10, 5), grid=False)
        ax.set_ylabel(u'Arbeitsplätze (Orientierungswerte)')
        ax.set_ylim(bottom=0)
        ax.yaxis.grid(True, which='major')
        
        return ax


class BranchenAnteile(Diagram):
    def _create(self, **kwargs):
        flaechen_id = kwargs['flaechen_id']
        flaechen_name = kwargs['flaechen_name']
        self.title = (u"{} - {}: Geschätzte Branchenanteile an den "
                      u"Arbeitsplätzen".format(
                          self.par.get_projectname(), flaechen_name))
        
        flaechen_id = kwargs['flaechen_id']
        
        table = 'Branchenanteile'
        branche_table = 'Gewerbe_Branchen'
        workspace = 'FGDB_Bewohner_Arbeitsplaetze.gdb'
        table_df = self.table_to_dataframe(
            table, workspace=workspace,
            columns=['IDBranche', 'Anteil'], 
            where='IDTeilflaeche={}'.format(flaechen_id))
        branche_table_df = self.table_to_dataframe(
            branche_table, workspace='FGDB_Definition_Projekt_Tool.gdb',
            columns=['ID_Branche_Projektcheck', 'Name_Branche_Projektcheck'],
            is_base_table=True
        )
        branche_table_df.rename(
            columns={'ID_Branche_Projektcheck': 'IDBranche'}, inplace=True)
        joined = table_df.merge(branche_table_df, on='IDBranche')
        joined['Anteil'] *= 100
        
        colors = self.plt.cm.Accent(np.linspace(0, 1, len(joined)))
        ax = joined['Anteil'].plot(kind='pie', labels=[''] * 6, autopct='%.2f',
                                   figsize=(8, 8), title=self.title,
                                   colors=colors)
        ax.set_ylabel('')
        ax.legend(joined['Name_Branche_Projektcheck'], loc='upper center',
                  bbox_to_anchor=(0.5, 0.1))
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])        
        
        return ax

if __name__ == "__main__":
    #diagram = BewohnerEntwicklung()
    #diagram.create(projectname='1', flaechen_id=1, flaechen_name=u'Testfläche')
    #diagram.show()
    diagram = ArbeitsplatzEntwicklung()
    diagram.create(projectname='Test2', flaechen_id=1, flaechen_name=u'Testfläche')
    diagram.show()
    #diagram = BranchenAnteile()
    #diagram.create(projectname='Test', flaechen_id=2, flaechen_name=u'Testfläche')
    #diagram.show()