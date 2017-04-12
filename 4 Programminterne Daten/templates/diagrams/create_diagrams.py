import arcpy

out_graph_name = "WE_angepasst"
out_graph_bmp = r"C:\Users\AK\Desktop\Templates Diagramme\WE_angepasst4.bmp"
input_template = r"C:\Users\AK\Desktop\Templates Diagramme\Wohneinheiten.grf"
input_data = r"C:\ProjektCheck\3 Benutzerdefinierte Projekte\Wir_wollen_Diagramme\FGDB_Definition_Projekt.gdb\Wohnen_WE_in_Gebaeudetypen"

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
arcpy.MakeGraph_management(input_template, graph, out_graph_name)
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
# Save the graph as an image
#arcpy.SaveGraph_management(out_graph_name, out_graph_bmp,
#                           "MAINTAIN_ASPECT_RATIO", 600, 375)
print('done')