import arcpy
from rpctools.utils.params import Tool


out_graph_name = "WE_angepasst"
out_graph_bmp = r"C:\Users\AK\Desktop\Templates Diagramme\WE_angepasst4.bmp"
input_template = r"C:\Users\AK\Desktop\Templates Diagramme\Wohneinheiten.grf"
input_data = r"C:\ProjektCheck\3 Benutzerdefinierte Projekte\Wir_wollen_Diagramme\FGDB_Definition_Projekt.gdb\Wohnen_WE_in_Gebaeudetypen"

class TestTool(Tool):

    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):
        parameters = self.par

        arcpy.env.overwriteOutput = True

        # Variablen definieren
        projektname = self.par.name.value

        # Create the graph
        graph = arcpy.Graph()
        
        # Add a vertical bar series to the graph
        graph.addSeriesBarVertical(input_data, "WE", "Gebaeudetyp")
        
        # Specify the title of the left axis
        #graph.graphAxis[0].title = "Rainfall"
        
        # Specify the title of the bottom axis
        #graph.graphAxis[2].title = "Days"
        
        # Specify the title of the Graph
        #graph.graphPropsGeneral.title = "Amount of Rainfall"
        
        # Output a graph, which is created in-memory
        arcpy.env.addOutputsToMap = True
        arcpy.MakeGraph_management(input_template, graph, out_graph_name)
        arcpy.env.addOutputsToMap = False
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        
        # Save the graph as an image
        arcpy.SaveGraph_management(out_graph_name, out_graph_bmp,
                                  "MAINTAIN_ASPECT_RATIO", 600, 375)
        print('done')