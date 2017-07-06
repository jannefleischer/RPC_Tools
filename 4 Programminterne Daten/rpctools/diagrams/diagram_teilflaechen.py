# -*- coding: utf-8 -*-

import arcpy
from rpctools.utils.encoding import encode
from rpctools.utils.diagram import ArcpyDiagram


class DiaTeilflaechen(ArcpyDiagram):
    _workspace = 'FGDB_Definition_Projekt.gdb'
    
    def _create(self, **kwargs):
        """
        Diagramm für Teilflächen
        """
        # Erstelle Diagramm Teilflaechen nach Hektar
        project_name = kwargs['project_name'] if 'project_name' in kwargs \
            else self.tbx.par.get_projectname()
        title = encode(
            "{}: Teilflächen des Plangebiets (Bruttofläche)"
            .format(project_name))
        input_template = self.tbx.folders.get_diagram_template(
            'Teilflaechen_Hektar')
        
        # Create the graph
        graph = arcpy.Graph()
        mxd = arcpy.mapping.MapDocument("CURRENT")
        project_layer = self.tbx.output.get_projectlayer()
        input_data = arcpy.mapping.ListLayers(project_layer,
                                              "Teilflaechen des Plangebiets",
                                              mxd.activeDataFrame)[0]
        # Add a vertical bar series to the graph
        graph.addSeriesBarVertical(dataSrc=input_data,
                                   fieldY="Flaeche_ha",
                                   fieldLabel="Name")
        graph.graphPropsGeneral.title = title
        return graph, input_template

    
if __name__ == "__main__":
    diagram = DiaTeilflaechen()
    diagram.create()
    diagram.show()