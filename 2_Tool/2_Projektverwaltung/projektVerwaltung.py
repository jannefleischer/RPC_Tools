# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# projektVerwaltung.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH / HCU Hamburg / GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import arcpy, os, shutil, sys

def main(parameters):

    if parameters[0].valueAsText == "Neues Projekt anlegen":

        arcpy.env.overwriteOutput = True

        try:
        #get new Project input Data
            projectName = parameters[2].valueAsText
            flaeche = parameters[3].valueAsText
            beginn_betrachtung = parameters[4].valueAsText
            ende_betrachtung = parameters[5].valueAsText

        #get the working directory and split it for the upper level path
            #Pfad anlegen
            mainPath = str(sys.path[0]).split("2_Tool")[0]

            fcPfad = os.path.join(mainPath,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
            sql = "Name = '" + projectName +"'"
            x=0
            cursor = arcpy.SearchCursor(fcPfad,sql)
            for row in cursor:
                x = x+1
            if x > 0:
                print "Es scheint bereits ein Projekt mit diesem Namen zu existieren"
                messages.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
                print "Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox"
                messages.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
                sys.exit()

        #register new project in the database
        #Am Ende das erfolgreich angelegte Projekt in "FGDB_01_Basisdaten-deutschland.gdb/angelegteProjekte" registrieren
            #messages.AddMessage(fcPfad)
            cursor = arcpy.InsertCursor(fcPfad)
            row = cursor.newRow()
            row.Name = projectName
            cursor.insertRow(row)
            messages.AddMessage("Projekt wird in der Datenbank registriert \n")
            print "Projekt wird in der Datenbank registriert \n"
            del row, cursor

        #copy template folder
            #templatePath = os.path.join(mainPath,'3_Projekte','Template.gdb') #Fehler im Script - geandert durch AT
            templatePath = os.path.join(mainPath,'3_Projekte','Template')
            projectPath = os.path.join(mainPath,'3_Projekte', projectName)
            try:
                shutil.copytree(templatePath, projectPath)
            except Exception as e:
                messages.AddMessage(e)
                print e
                messages.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
                messages.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
                messages.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
                sys.exit()
        ##rename copied files
        #list all files in directory
            files = os.listdir(projectPath)
        #check if filenames contain "Template"
            messages.AddMessage("Erstelle Kopien der Basisdaten: ")
            print "Erstelle Kopien der Basisdaten: "
            for file in files:
                messages.AddMessage("    -" + file)
                if "Template" in file:
                    #split filename and add projectName as new filename
                    newName = file.replace("Template",projectName)
                    filePath = os.path.join(projectPath,file)
                    newFilePath = os.path.join(projectPath,newName)
                    os.rename(filePath,newFilePath)
        #If shapefile was uploaded, add to gdb
            if flaeche != "":
                gdbPfad = os.path.join(mainPath,'3_Projekte',projectName,'FGDB_Definition_Projekt_'+projectName+'.gdb')
                arcpy.FeatureClassToGeodatabase_conversion(flaeche, gdbPfad)

                dsc = arcpy.Describe(flaeche)
                filename = dsc.baseName
                filename = filename.replace(" ","_")
                filename = filename.replace("-","_")
                messages.AddMessage(filename)

                arcpy.env.workspace = gdbPfad
                fcs = arcpy.ListFeatureClasses()
                fcsPfad = os.path.join(gdbPfad,filename)
                try:
                    arcpy.Rename_management(fcsPfad,"Teilflaechen_Plangebiet")
                except:
                    messages.AddMessage("Fehler: Umbenennung nicht erfolgreich")
                fcs = arcpy.ListFeatureClasses()


        #   Prepare Shapefile for use in RPC
            teilfaechen_plangebiet = os.path.join(gdbPfad,"Teilflaechen_Plangebiet")

            #delete unused fields
            fieldObjList = arcpy.ListFields(teilfaechen_plangebiet)
            fieldNameList = []
            for field in fieldObjList:
                if not field.required:
                    fieldNameList.append(field.name)

            arcpy.DeleteField_management(teilfaechen_plangebiet, fieldNameList)

            #add needed fields
            arcpy.AddField_management(teilfaechen_plangebiet,"Name","TEXT")
            arcpy.AddField_management(teilfaechen_plangebiet,"Startjahr","LONG")
            arcpy.AddField_management(teilfaechen_plangebiet,"Beginn_Nutzung","LONG")
            arcpy.AddField_management(teilfaechen_plangebiet,"Aufsiedlungsdauer","LONG")
            arcpy.AddField_management(teilfaechen_plangebiet, "Flaeche_ha", "DOUBLE", "", "", "", "", "", "")
            arcpy.AddField_management(teilfaechen_plangebiet,"umfang_meter","FLOAT")
            #arcpy.AddField_management(teilfaechen_plangebiet,"Bilanzsumme","FLOAT")


            # Berechne ha der Teilflaechen
            arcpy.CalculateField_management(teilfaechen_plangebiet, "Flaeche_ha", "!SHAPE.AREA@HECTARES!", "PYTHON_9.3", "")

            # Berechne Umfang der Flächen
            arcpy.CalculateField_management(teilfaechen_plangebiet,"umfang_meter","!shape.length@METER!","PYTHON_9.3")

            #add year
            startjahr = int(beginn_betrachtung)

            cursor = arcpy.UpdateCursor(teilfaechen_plangebiet)
            i= 1
            for row in cursor:
                row.setValue("Startjahr", startjahr)
                row.setValue("Name", "Flaeche_"+str(i))
                row.setValue("Aufsiedlungsdauer", 5)
                #row.setValue("Bilanzsumme", 0)
                cursor.updateRow(row)
                i+= 1


        #add project-data to Projektrahmendaten

            #Den AGS aus der Lage der projektfläche im Raum ermitteln
            bkg = os.path.join(mainPath,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','bkg_gemeinden')
            workspace_projekt_definition = os.path.join(mainPath,'3_Projekte',projectName,'FGDB_Definition_Projekt_'+projectName+'.gdb')
            projektrahmendaten = os.path.join(workspace_projekt_definition,'Projektrahmendaten')
            projektFlaeche = os.path.join(workspace_projekt_definition,'Teilflaechen_Plangebiet')

            #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
            #1. Feature Layer aus den bkg-daten erstellen
            arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
            #2.Spatial Select wo Planfläche bkg_lyr intersected
            arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
            #Wenn Flaeche = 1, ags extrahieren
            n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
            if(int(n) > 1):
                messages.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
                ## TODO Dateien loeschen und Projektregistrierung loeschen

                sys.exit()
            if(int(n) == 1 ):
                gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
                for gemeinde in gemeindeCursor:
                    ags = gemeinde.AGS
                    gen = gemeinde.GEN

            #Setzen des Sonderkostenfaktors auf 1 =100% - Sonderkostenfaktor wird im Themenfeld Kosten durch nutzer eingegeben und in der Tabelle aktualisiert
            sonderkostenfaktor = 1

            #loesche ggf. vorhandene zeilen in den rojektrahmendaten und fuege neue daten danach hinzu
            arcpy.DeleteRows_management(projektrahmendaten)

            cursor = arcpy.InsertCursor(projektrahmendaten)
            row = cursor.newRow()
            row.BEGINN_BETRACHTUNGSZEITRAUM = beginn_betrachtung
            row.ENDE_BETRACHTUNGSZEITRAUM = ende_betrachtung
            row.GEMEINDENAME = gen
            row.PROJEKTSPEZIFISCHER_SONDERKOSTENFAKTOR = sonderkostenfaktor
            row.PROJEKTNAME = projectName
            row.AGS = ags
            cursor.insertRow(row)

            del cursor,row

        #Minimap erzeugen
            schrittmeldung = 'Erzeuge Uebersichtskarte \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung

            #Kopiere Template.mxd
            mxd_template = arcpy.mapping.MapDocument(os.path.join(mainPath, "2_Tool","2_Projektverwaltung","Style_Minimap","template.mxd"))
            ausgabeordner_img = os.path.join(mainPath,'3_Projekte',projectName,'Ergebnisausgabe','Abbildungen')
            mxdpfad = os.path.join(ausgabeordner_img,'Definition_Projekt.mxd')
            mxd_template.saveACopy(mxdpfad)

            # Ersetze Datenquelle
            minimap_mxd = arcpy.mapping.MapDocument(mxdpfad)
            templatepath = os.path.join(mainPath,"2_Tool","2_Projektverwaltung","Style_Minimap","template.gdb")
            resultpath = os.path.join(mainPath,'3_Projekte',projectName,'FGDB_Definition_Projekt_'+projectName+'.gdb')
            minimap_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)

            # Setze Viewport neu
            df = arcpy.mapping.ListDataFrames(minimap_mxd)[0]
            gebietLayer = arcpy.mapping.ListLayers(minimap_mxd, "Teilflaechen_Plangebiet", df)[0]
            arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
            df.extent = gebietLayer.getSelectedExtent(False)
            arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
            df.scale = df.scale * 1.4

            arcpy.RefreshActiveView()
            minimap_mxd.save()
            del mxd_template

            #Exportiere Ergebnis
            arcpy.mapping.ExportToJPEG(minimap_mxd, os.path.join(ausgabeordner_img, 'Minimap.jpg'), "PAGE_LAYOUT",resolution=150)
            minimap = os.path.join(os.path.join(mainPath,'3_Projekte',projectName,'Ergebnisausgabe','Abbildungen', 'Minimap.jpg'))

        #output information to user
            print("Basisdaten erfolgreich kopiert")
            messages.AddMessage("Basisdaten erfolgreich kopiert \n")
            #print("Neues Projekt angelegt im Ordner " + projectPath)
            messages.AddMessage("Neues Projekt angelegt im Ordner " + projectPath + '\n')
        except Exception as e:
            messages.AddMessage(e)
            print e



    elif parameters[0].valueAsText == "Bestehendes Projekt kopieren":

        try:
        #get new Project Name as input
            projectNameOld = parameters[1].valueAsText
            #projectNameOld = "Bultweg_Sued_fiktiv"
        #allow the upload of a shapefile containg the projektgebiet
            projectNameNew = parameters[2].valueAsText
            #projectNameNew = "test"
        #get the working directory and split it for the upper level path
            #Pfad anlegen
            mainPath = str(sys.path[0]).split("2_Tool")[0]

            fcPfad = os.path.join(mainPath,"1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","angelegteProjekte")
            sql = "Name = '" + projectNameNew +"'"
            x=0
            cursor = arcpy.SearchCursor(fcPfad,sql)
            for row in cursor:
                x = x+1
            if x > 0:
                print "Es scheint bereits ein Projekt mit diesem Namen zu existieren"
                messages.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
                print "Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox"
                messages.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
                sys.exit()

        #copy template folder
            templatePath = os.path.join(mainPath,"3_Projekte",projectNameOld)
            projectPath = os.path.join(mainPath,"3_Projekte",projectNameNew)

            try:
                shutil.copytree(templatePath, projectPath)
            except Exception as e:
                messages.AddMessage(e)
                messages.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
                messages.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
                messages.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
                sys.exit()
        ##rename copied files
        #list all files in directory
            files = os.listdir(projectPath)
        #check if filenames contain "Template"
            for file in files:
                messages.AddMessage(file)
                if projectNameOld in file:
                    #split filename and add projectName as new filename
                    newName = file.replace(projectNameOld,projectNameNew)
                    filePath = os.path.join(projectPath,file)
                    newFilePath = os.path.join(projectPath,newName)

                    os.rename(filePath,newFilePath)

        #register new project in the database
        #Am Ende das erfolgreich angelegte Projekt in "FGDB_Basisdaten-deutschland.gdb/angelegteProjekte" registrieren
            messages.AddMessage(fcPfad)
            cursor = arcpy.InsertCursor(fcPfad)
            row = cursor.newRow()
            row.Name = projectNameNew
            cursor.insertRow(row)
            messages.AddMessage("Inserting")
            del row, cursor

        #output information to user
            print("Succesfully copied")
            messages.AddMessage("Succesfully copied")
            print("New Project registered at " + projectPath)
            messages.AddMessage("New Project registered at " + projectPath)
        except Exception as e:
            messages.AddMessage(e)


    else:

        #Das zu löschende Projekt
        projektName = parameters[1].valueAsText

        #aktuelles Arbeitsverzeichnis bekommen
        pfad = str(sys.path[0]).split("2_Tool")[0]

        #Mit dem Projektnamen zum neuen Projektpfad zusammenführen"
        projektePfad = os.path.join(pfad,'3_Projekte')
        projektPfad= os.path.join(projektePfad,projektName)
        messages.AddMessage("Suche Ordner: " + projektPfad)

        #entferne alle aktuellen Layer aus dem TOC (Locks aufheben)
        messages.AddMessage("Loese aktive Layer aus MXD \n")
        mxd = arcpy.mapping.MapDocument("CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            for lyr in arcpy.mapping.ListLayers(mxd, "", df):
                arcpy.mapping.RemoveLayer(df, lyr)
        del mxd

        try:
            #Überprüfen, ob ein Eintrag in der Datenbank vorliegt
            fcPfad = os.path.join(pfad,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
            #messages.AddMessage(fcPfad)
            sql = "Name = '" + projektName +"'"
            x=0
            cursor = arcpy.UpdateCursor(fcPfad,sql)
            for row in cursor:
                #messages.AddMessage(row.Name)
                x = x+1
            del cursor, row

            #Überprüfen, ob der Projektordner existiert
            if(os.path.isdir(projektPfad)):
                print("Projektordner gefunden")
                messages.AddMessage("Projektordner gefunden \n")
                shutil.rmtree(projektPfad)
                print("Projektordner gelöscht")
                messages.AddMessage("Projektordner gelöscht \n")
            else:
                print("Projektordner "+ projektName + " nicht gefunden \n")
                messages.AddMessage("Projektordner "+ projektName + " nicht gefunden \n")

            if x == 1:
                print "Eintrag in der Datenbank gefunden"
                messages.AddMessage("Eintrag in der Datenbank gefunden \n")
                delcursor = arcpy.UpdateCursor(fcPfad,sql)
                try:
                    for fc in delcursor:
                        #messages.AddMessage("Loeschschleife")
                        #messages.AddMessage(fc.Name)
                        delcursor.deleteRow(fc)
                        print("Eintrag gelöscht")
                        messages.AddMessage("Eintrag gelöscht \n")
                except:
                    messages.AddMessage("Löschen fehlgeschlagen \n")

                del delcursor


            else:
                print("Projekt "+ projektName + " nicht gefunden")
                messages.AddMessage("Projekt "+ projektName + " nicht gefunden \n")


            messages.AddMessage("*********************************************************************************")
            messages.AddMessage("Das Projekt " + projektName + " wurde erfolgreich entfernt \n")

        except Exception as e:
            print(e)
            messages.AddMessage(e)
        finally:
            try:
                del cursor, delcursor
            except:
                print""

if __name__ == "__main__":
    main(sys.argv)
