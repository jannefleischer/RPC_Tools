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
import arcpy,os,sys,gc
from arcpy import env

gc.collect()

def CheckVonNeuenMaerkten(workspace_projekt_Wertveraenderungen,workspace_projekt_def):

        cur_Infrastruktur_NeueMaerkte=arcpy.SearchCursor(workspace_projekt_Wertveraenderungen+'\Infrastruktur_NeueMaerkte')

        keinEintrag = True
        for zeil in cur_Infrastruktur_NeueMaerkte:
            keinEintrag=False

        if keinEintrag==True:
                cur_Flaechenbilanz_Planung=arcpy.SearchCursor(workspace_projekt_def+'\Flaechenbilanz_Planung')
                Ja=False
                for zeile in cur_Flaechenbilanz_Planung:
            ##        print zeile.Flaechennutzung_S2
                    if zeile.Flaechennutzung_S2=="Gewerbeflaeche (Versorgung)":
                        Ja=True


                if Ja==True:

                    arcpy.AddMessage("Kein neuer Markt in Infrastruktur_NeueMaerkte eingetragen,")
                    arcpy.AddMessage("obwohl Gewerbeflaeche (Versorgung) in der Planung angegeben ist .")
                    arcpy.AddMessage("Bitte Point Feature in Infrastruktur_NeueMaerkte setzen.")
                    arcpy.AddMessage("Anschließend dieses Tool erneut starten.")
                    print "Kein Punkt in Point Feature"
                    del cur_Infrastruktur_NeueMaerkte,cur_Flaechenbilanz_Planung
                    return 1

                print "Kein neuer Markt geplant - Darstellung nicht möglich."
                arcpy.AddMessage("Kein neuer Markt geplant - Darstellung nicht möglich.")
        else:
            #Eintrage von Sascha vorhanden

            arcpy.AddMessage("Kopieren des Point Features Infrastruktur_NeueMaerkte.")
            try:
                arcpy.DeleteFeatures_management(workspace_projekt_Wertveraenderungen+"\ET_Infrastruktur_NeueMaerkte")

            except:
                pass

            try:
                arcpy.CopyFeatures_management(workspace_projekt_Wertveraenderungen+"\Infrastruktur_NeueMaerkte", workspace_projekt_Wertveraenderungen+"\ET_Infrastruktur_NeueMaerkte")
            except:
                arcpy.AddMessage("File konnte nicht kopiert werden - abbruch")
                del cur_Infrastruktur_NeueMaerkte,cur_Flaechenbilanz_Planung
                return 1

            arcpy.AddMessage("Buffern der Versorgungseinrichtungen.")

            # Set local variables
            inFeatures = "ET_Infrastruktur_NeueMaerkte"
            outFeatureClass = workspace_projekt_Wertveraenderungen+"/ET_Infrastruktur_NeueMaerkte_buffered"
            distances = [5,10,15,20,25,30,40,50,75,100,125,150,175,200,250,300,350,400,450,500]
            bufferUnit = "meters"

            # Execute MultipleRingBuffer
            arcpy.MultipleRingBuffer_analysis(inFeatures, outFeatureClass, distances, bufferUnit, "", "ALL")

            del inFeatures,outFeatureClass,distances,bufferUnit
        del cur_Infrastruktur_NeueMaerkte
        return 0


def Layerstyle_kopieren(workspace_vorlagen,workspace_projekt_ergebnis):

    path=workspace_vorlagen+'\Leeremxd_Nahversorgung.mxd'
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
    fcname = 'ET_Infrastruktur_NeueMaerkte_buffered'    #arcpy.ListFeatureClasses()[0]
    my_layer2 = arcpy.mapping.Layer(os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap_topo.lyr')))
##    print os.path.abspath(os.path.join(os.path.dirname(__file__), 'Basemap.lyr'))
##    print os.path.abspath(os.path.join(workspace_vorlagen, 'Basemap.lyr'))

    # Set layer's source
    my_layer.replaceDataSource(os.path.join(arcpy.env.workspace), 'FILEGDB_WORKSPACE', fcname)

##    arcpy.mapping.AddLayer(data_frame, my_layer, 'TOP')
    arcpy.mapping.AddLayer(data_frame,my_layer2,'BOTTOM')

    ext = my_layer.getExtent()
    data_frame.extent=ext
##    arcpy.mapping.DataFrame.extent=ext

    # Save to disk
    try:
      os.remove(workspace_projekt_ergebnis+ '\\32_Wertveraenderung_Einzugsgebiet_Gewerbe.mxd')
      os.remove(workspace_projekt_ergebnis+ '\\32_Ergebnis_out_Einzugsgebiet_Gewerbe.jpg')
    except:
        arcpy.AddMessage("Fehler beim Loeschen. ")
        print "Fehler beim Loeschen. "
    try:
      my_mxd.saveACopy(os.path.abspath(os.path.join(workspace_projekt_ergebnis, '32_Wertveraenderung_Einzugsgebiet_Gewerbe.mxd')),"10.0")

      arcpy.mapping.ExportToJPEG(my_mxd, os.path.abspath(os.path.join(workspace_projekt_ergebnis, '32_Ergebnis_out_Einzugsgebiet_Gewerbe.jpg')), "PAGE_LAYOUT",
                           resolution=300)

      arcpy.AddMessage("Erstellung der 32_Wertveraenderung_Einzugsgebiet_Gewerbe.mxd und 32_Ergebnis_out_Einzugsgebiet_Gewerbe.jpg ")
      arcpy.AddMessage("war erfolgreich. ")
      print "erfolgreich"
    except:
        arcpy.AddMessage("Fehler beim Abspeichern. ")
        print "Abspeichern"
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


geklappt=CheckVonNeuenMaerkten(workspace_projekt_Wertveraenderungen,workspace_projekt_def)

if geklappt==0:
    Layerstyle_kopieren(workspace_vorlagen,workspace_projekt_ergebnis)
try:
    del projektname,workspace_vorlagen,workspace_projekt_def,workspace_projekt_Wertveraenderungen,workspace_projekt_ergebnis,geklappt
except:
    pass

gc.collect()