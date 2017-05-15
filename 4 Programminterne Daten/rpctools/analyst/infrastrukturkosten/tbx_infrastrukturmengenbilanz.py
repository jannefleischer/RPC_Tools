# -*- coding: utf-8 -*-
import sys
import datetime
import arcpy
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from rpctools.diagrams.infrastruktur import Netzlaenge, MassnahmenKosten


class InfrastrukturmengenBilanz(Tool):    
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Kosten.gdb'
    _group_layer = "infrastruktur"
    _line_layer = "Erschließungsnetz"
    _point_layer = "Erschließungsnetz - punktuelle Maßnahmen" 
    _line_table = 'Erschliessungsnetze_Linienelemente'
    _point_table = 'Erschliessungsnetze_Punktelemente'    
    _length_table = 'Erschliessungsnetze_Linienlaengen'
    _cost_table = 'Erschliessungsnetze_Punktkosten'
    
    def add_output(self):
        # add Erschliessungsnetz
        fc = self.folders.get_table(self._line_table)
        layer = self.folders.get_layer(self._line_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
        fc = self.folders.get_table(self._point_table)
        layer = self.folders.get_layer(self._point_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
    def calculate_lengths(self):
        linien_df = self.parent_tbx.table_to_dataframe(
            self._line_table, columns=['SHAPE_Length', 'IDNetz']
        )
        base_df = self.parent_tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)
        joined = linien_df.merge(base_df, on='IDNetz')
        grouped = joined.groupby(by='IDNetz')
        self.parent_tbx.delete_rows_in_table(self._length_table)
        for id_netz, grouped_df in grouped:
            self.parent_tbx.insert_row_in_table(
                self._length_table,
                column_values={
                    'Laenge': grouped_df['SHAPE_Length'].sum(), 
                    'Netz': grouped_df['Netz'].unique()[0],
                    'IDNetz': id_netz
                }
            )
            
        
    def calculate_costs(self): 
        point_df = self.parent_tbx.table_to_dataframe(self._point_table)
        base_df = self.parent_tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)

        joined = point_df.merge(base_df, on='IDNetz')
        grouped = joined.groupby(by='IDNetz')
        columns = ['Netz', 'Kosten_EH_EUR']
        categories = []
        costs = []
        for id_netz, grouped_df in grouped:
            categories.append(id_netz)
            costs.append(grouped_df['Kosten_EH_EUR'].sum())
            
        fig, ax = plt.subplots()
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, costs, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        plt.show(block=False)
        

    def add_diagramms(self):
        project_name = self.projectname
        
        # net lengths
        title = encode("{}: Länge der zusätzlichen Infrastrukturnetze "
                       "(ohne punktuelle Maßnahmen)".format(project_name))
        input_template = self.folders.get_diagram_template(
            'Erschliessungsnetz_Netzlaenge')
        input_data = self.folders.get_table(self._length_table)
        graph = arcpy.Graph()
        graph.addSeriesBarHorizontal(dataSrc=input_data,
                                     fieldX='Laenge')
        graph.graphPropsGeneral.title = title
        self.output.add_graph(input_template, graph, title)
        
        # costs
        title = encode("{}: Kosten der punktuellen Maßnahmen"
                       .format(project_name))
        input_template = self.folders.get_diagram_template(
            'Kosten_punktuelle_Massnahmen')
        input_data = self.folders.get_table(self._cost_table)
        graph = arcpy.Graph()
        graph.addSeriesBarHorizontal(dataSrc=input_data,
                                     fieldX='Kosten')
        graph.graphPropsGeneral.title = title
        self.output.add_graph(input_template, graph, title)
        
    
    def run(self):
        #self.calculate_lengths()
        #self.calculate_costs()
        #self.add_output()
        #self.add_diagramms()
        netz_diagram = Netzlaenge()
        netz_diagram.create()        
        kosten_diagram = MassnahmenKosten()
        kosten_diagram.create()
        netz_diagram.show()
        kosten_diagram.show()


class TbxInfrastrukturmengenBilanz(Tbx):
    """Toolbox Projekt loeschen"""
    @property
    def label(self):
        return u'Schritt ?: Infrastrukturmengen bilanzieren'

    @property
    def Tool(self):
        return InfrastrukturmengenBilanz

    def _getParameterInfo(self):

        # Bestehendes_Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = encode('Projekt')
        p.displayName = encode('Projekt')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.filter.list = []

        return self.par

    def _updateParameters(self, params):
        pass
    
if __name__ == "__main__":
    t = TbxInfrastrukturmengenBilanz()
    t.getParameterInfo()
    t.par.projectname.value = t.config.active_project
    t.execute()