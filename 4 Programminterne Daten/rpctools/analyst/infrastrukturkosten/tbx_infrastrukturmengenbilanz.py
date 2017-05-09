# -*- coding: utf-8 -*-

import datetime
import arcpy
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode


class InfrastrukturmengenBilanz(Tool):    
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Kosten.gdb'
    _group_layer = "infrastruktur"
    _line_layer = "Erschließungsnetz"
    _point_layer = "Erschließungsnetz - punktuelle Maßnahmen"    

    def add_output(self):
        # add Erschliessungsnetz
        fc = self.folders.get_table('Erschliessungsnetze_Linienelemente')
        layer = self.folders.get_layer(self._line_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
        fc = self.folders.get_table('Erschliessungsnetze_Punktelemente')
        layer = self.folders.get_layer(self._point_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
    def calculate_lengths(self):
        linien_df = self.parent_tbx.table_to_dataframe(
            "Erschliessungsnetze_Linienelemente",
            columns=['SHAPE_Length', 'IDNetz']
        )
        base_df = self.parent_tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'], 
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)
        joined = linien_df.merge(base_df, on='IDNetz')
        grouped = joined.groupby(by='IDNetz')
        self.parent_tbx.delete_rows_in_table(
            'Erschliessungsnetze_Linienlaengen')
        for id_netz, grouped_df in grouped:
            self.parent_tbx.insert_row_in_table(
                'Erschliessungsnetze_Linienlaengen',
                column_values={
                    'Laenge': grouped_df['SHAPE_Length'].sum(), 
                    'Netz': grouped_df['Netz'].unique()[0],
                    'IDNetz': id_netz
                }
            )
            
        
    def add_diagramm(self):
        # Erstelle Diagramm Teilflaechen nach Hektar
        project_name = self.projectname
        title = encode("{}: Länge der zusätzlichen Infrastrukturnetze "
                       "(ohne punktuelle Maßnahmen)".format(project_name))
        out_graph_name = ("{}: Länge der zusätzlichen Infrastrukturnetze "
                          "(ohne punktuelle Maßnahmen)".format(project_name))
        input_template = self.folders.get_diagram_template(
            'Erschliessungsnetz_Netzlaenge')
        input_data = self.folders.get_table('Erschliessungsnetze_Linienlaengen')
        # Create the graph
        graph = arcpy.Graph()
        mxd = arcpy.mapping.MapDocument("CURRENT")
        # Add a vertical bar series to the graph
        graph.addSeriesBarHorizontal(dataSrc=input_data,
                                     fieldX='Laenge')
        graph.graphPropsGeneral.title = title
        self.output.add_graph(input_template, graph, title)
    
    def run(self):
        self.calculate_lengths()
        self.add_output()
        self.add_diagramm()


class TbxInfrastrukturmengenBilanz(Tbx):
    """Toolbox Projekt loeschen"""
    @property
    def label(self):
        return u'Schritt ?: Infrastrukturmengen bilanzieren'

    @property
    def Tool(self):
        return InfrastrukturmengenBilanz

    def _getParameterInfo(self):
        projects = self.folders.get_projects()

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