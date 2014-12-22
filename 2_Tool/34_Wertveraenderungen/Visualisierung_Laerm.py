# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Basti
#
# Created:     20.10.2013
# Copyright:   (c) Basti 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#try catch hinzufügen sonst fertig

import arcpy,sys,os,gc
gc.collect()
def kopiere_file(workspace_projekt_Verkehrserzeugung,workspace_projekt_Wertveraenderungen):
    arcpy.AddMessage("Kopieren des Ergebnisses der Laermerzeugung.")
    try:
        arcpy.DeleteFeatures_management(workspace_projekt_Wertveraenderungen+"\ET_L15_Grid_Ergebnis")

    except:
        pass

    try:
        arcpy.CopyFeatures_management(workspace_projekt_Verkehrserzeugung+"\L15_Grid_Ergebnis", workspace_projekt_Wertveraenderungen+"\ET_L15_Grid_Ergebnis")
    except:
        arcpy.AddMessage("File konnte nicht kopiert werden - abbruch")
        return 1
    return 0


def Layerstyle_kopieren(workspace_projekt_Verkehrserzeugung,workspace_vorlagen,workspace_projekt_ergebnis):

    arcpy.env.workspace = workspace_projekt_Wertveraenderungen
    path=workspace_vorlagen+'\Leeremxd_laerm.mxd'
    path=path.replace("\\","\\\\")
##    print path
    arcpy.AddMessage("Laden der Styles.")
##    my_mxd = arcpy.mapping.MapDocument(r"C:\Users\Basti\Dropbox\RPC\00_Entwicklungsumgebung\3_Projekte\LKH_Bultweg\Ergebnisausgabe\Abbildungen\Leeremxd.mxd")
    my_mxd = arcpy.mapping.MapDocument(path)
    my_mxd.relaticePaths =True
    data_frame = arcpy.mapping.ListDataFrames(my_mxd)[0]
    # Switch to data view
    my_mxd.activeView = data_frame.name
    # Load standard layer with symbology, append to TOC in first data frame
    #alt
##    my_layer = arcpy.mapping.Layer(r'C:\Users\Basti\Dropbox\RPC\00_Entwicklungsumgebung\2_Tool\34_Wertveraenderungen\Wertveraenderungen_Wohnen\Laermbelaestigung\Laerm_Layer.lyr')
    #neu
##    my_layer = arcpy.mapping.Layer(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Laerm_Layer2.lyr')))
    my_layer= arcpy.mapping.ListLayers(my_mxd)[0]

    ##arcpy.mapping.AddLayer(data_frame, my_layer, 'TOP')
    # Loop through rasters in workspace, swap out layer's source with raster's
##    print str(arcpy.ListFeatureClasses())
    fcname = 'ET_L15_Grid_Ergebnis'    #arcpy.ListFeatureClasses()[0]
    my_layer2 = arcpy.mapping.Layer(os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap.lyr')))
##    print os.path.abspath(os.path.join(os.path.dirname(__file__), 'Basemap.lyr'))
##    print os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap.lyr'))

    # Set layer's source
    my_layer.replaceDataSource(os.path.join(arcpy.env.workspace), 'FILEGDB_WORKSPACE', fcname)

##    arcpy.mapping.AddLayer(data_frame, my_layer, 'TOP')
    arcpy.mapping.AddLayer(data_frame,my_layer2,'BOTTOM')
##    ext = my_layer.getExtent()
##    data_frame.extent=ext
##    my_mxd.updateItem()

    # Save to disk
    try:
      os.remove(workspace_projekt_ergebnis+ '\\32_Wertveraenderung.mxd')
      os.remove(workspace_projekt_ergebnis+ '\\Ergebnis_out_Laerm_Verkehr.jpg')
    except:
        arcpy.AddMessage(" ")
    try:
      my_mxd.saveACopy(os.path.abspath(os.path.join(workspace_projekt_ergebnis, '32_Wertveraenderung_Learm.mxd')),"10.0")

      arcpy.mapping.ExportToJPEG(my_mxd, os.path.abspath(os.path.join(workspace_projekt_ergebnis, 'Ergebnis_out_Laerm_Verkehr.jpg')), "PAGE_LAYOUT",
                           resolution=300)

      arcpy.AddMessage("Erstellung der 32_Wertveraenderung.mxd und Ergebnis_out_Laerm_Verkehr.jpg  ")
      arcpy.AddMessage("war erfolgreich. ")
    except:
        arcpy.AddMessage("Fehler beim Abspeichern. ")
    del path,my_mxd,data_frame,my_layer,fcname



#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

arcpy.env.overwriteOutput = True

#projektname="LKH_Tostedt"
##projektname=sys.argv[0]
# Variablen definieren
projektname = arcpy.GetParameterAsText(0)

arcpy.AddMessage("\n\nTool zur Laermmodellierung gestartet.")
arcpy.AddMessage("Visualisierung der Laermbelastung als Karte mit farblichen Abstufungen.")

workspace_vorlagen=os.path.join(base_path,'2_Tool','34_Wertveraenderungen','Style')
workspace_projekt_def = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_Verkehrserzeugung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_25_Verkehrserzeugung_'+projektname+'.gdb')
workspace_projekt_Wertveraenderungen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_34_Wertveraenderungen_'+projektname+'.gdb')
workspace_projekt_ergebnis = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen')

geklappt= kopiere_file(workspace_projekt_Verkehrserzeugung,workspace_projekt_Wertveraenderungen)


if geklappt==0:
    Layerstyle_kopieren(workspace_projekt_Verkehrserzeugung,workspace_vorlagen,workspace_projekt_ergebnis)
else:
    arcpy.AddMessage("Abbruch . ")
    print"Abbruch"
try:
    del projektname,workspace_vorlagen,workspace_projekt_def,workspace_projekt_Verkehrserzeugung,workspace_projekt_Wertveraenderungen,workspace_projekt_ergebnis
except:
    pass


gc.collect()

exit()