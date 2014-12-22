# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Basti
#
# Created:     16.12.2013
# Copyright:   (c) Basti 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import system modules
import arcpy,os,sys,gc
from arcpy import env

gc.collect()

def buffern(workspace_projekt_def,workspace_projekt_Wertveraenderungen):
    cur_Flaechenbilanz_Planung=arcpy.SearchCursor(workspace_projekt_def+'\Flaechenbilanz_Planung')
    arcpy.AddMessage("Suchen nach Gemeinbedarfsflaechen.")
    Ja=False
    for zeile in cur_Flaechenbilanz_Planung:
##        print zeile.Flaechennutzung_S2
        if zeile.Flaechennutzung_S2=="Gemeinbedarfsflaeche":
            Ja=True


    if Ja==True:
##        print "sachen einzeichnen bzw checken was wo wie"
        cur_Infrastruktur_Schulen=arcpy.SearchCursor(workspace_projekt_Wertveraenderungen+'\Infrastruktur_Schulen')

        keinEintrag = True
        for zeil in cur_Infrastruktur_Schulen:
            keinEintrag=False



        if keinEintrag==True:
            arcpy.AddMessage("Kein Punkt in Point Feature - Abbruch")
##            print "Kein Punkt in Point Feature"
            return 1
        else:
        #Buffern
            arcpy.AddMessage("Buffern der Schulen.")

            # Set local variables
            inFeatures = "Infrastruktur_Schulen"
            outFeatureClass = workspace_projekt_Wertveraenderungen+"/Einzugsgebiet"
            distances = [5,10,15,20,25,30,40,50,75,100,125,150,175,200,250,300,350,400,450,500]
            bufferUnit = "meters"

            # Execute MultipleRingBuffer
            arcpy.MultipleRingBuffer_analysis(inFeatures, outFeatureClass, distances, bufferUnit, "", "ALL")

    return 0
def Layerstyle_kopieren(workspace_vorlagen,workspace_projekt_ergebnis):

    path=workspace_vorlagen+'\Leeremxd_Infra.mxd'
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
    fcname = 'Einzugsgebiet'    #arcpy.ListFeatureClasses()[0]
    my_layer2 = arcpy.mapping.Layer(os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap_topo.lyr')))
##    print os.path.abspath(os.path.join(os.path.dirname(__file__), 'Basemap.lyr'))
##    print os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap.lyr'))

    # Set layer's source
    my_layer.replaceDataSource(os.path.join(arcpy.env.workspace), 'FILEGDB_WORKSPACE', fcname)

##    arcpy.mapping.AddLayer(data_frame, my_layer, 'TOP')
    arcpy.mapping.AddLayer(data_frame,my_layer2,'BOTTOM')

    ext = my_layer.getExtent()
    data_frame.extent=ext
##    my_mxd.updateItem()

    # Save to disk
    try:
      os.remove(workspace_projekt_ergebnis+ '\\32_Wertveraenderung_Einzugsgebiet_Schulen.mxd')
      os.remove(workspace_projekt_ergebnis+ '\\32_Ergebnis_out_Einzugsgebiet_Schulen.jpg')
    except:
        arcpy.AddMessage("  ")
    try:
      my_mxd.saveACopy(os.path.abspath(os.path.join(workspace_projekt_ergebnis, '32_Wertveraenderung_Einzugsgebiet_Schulen.mxd')),"10.0")

      arcpy.mapping.ExportToJPEG(my_mxd, os.path.abspath(os.path.join(workspace_projekt_ergebnis, '32_Ergebnis_out_Einzugsgebiet_Schulen.jpg')), "PAGE_LAYOUT",
                           resolution=300)

      arcpy.AddMessage("Erstellung der 32_Wertveraenderung_Einzugsgebiet_Schulen.mxd und 32_Ergebnis_out_Einzugsgebiet_Schulen.jpg ")
      arcpy.AddMessage("war erfolgreich. ")
    except:
        arcpy.AddMessage("Fehler beim Abspeichern. ")
    del path,my_mxd,data_frame,my_layer,fcname


#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

arcpy.env.overwriteOutput = True

projektname = arcpy.GetParameterAsText(0)
##projektname="LKH_Bultweg"

workspace_vorlagen=os.path.join(base_path,'2_Tool','34_Wertveraenderungen','Style')
workspace_projekt_def = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_Wertveraenderungen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_34_Wertveraenderungen_'+projektname+'.gdb')
workspace_projekt_ergebnis = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen')

# Set environment settings
env.workspace = workspace_projekt_Wertveraenderungen


geklappt=buffern(workspace_projekt_def,workspace_projekt_Wertveraenderungen)
if geklappt==0:
    Layerstyle_kopieren(workspace_vorlagen,workspace_projekt_ergebnis)
try:
    del projektname,workspace_vorlagen,workspace_projekt_def,workspace_projekt_Wertveraenderungen,workspace_projekt_ergebnis
except:
    pass

gc.collect()