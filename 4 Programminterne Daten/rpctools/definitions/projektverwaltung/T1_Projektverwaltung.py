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

import sys
from os.path import abspath, dirname, join, isdir
from rpctools.utils.params import Tool
from rpctools.utils.spatial_lib import get_ags
from rpctools.utils.constants import Nutzungsart
import arcpy
import os, shutil, gc


class Projektverwaltung(Tool):

    _param_projectname = 'name'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        # prevent eventual locks
        gc.collect()

        arcpy.AddMessage(self.par.action.value)

        if self.par.action.value == "Neues Projekt anlegen":
            self.projekt_anlegen()
            self.add_output_new_project()
            self.add_diagramm()

        elif self.par.action.value == "Bestehendes Projekt kopieren":
            self.projekt_kopieren()
            self.add_output_new_project()

        else:
            _param_projectname = 'existing_project'
            self.projekt_loeschen()
            self.remove_project_from_output()

    def add_output_new_project(self):
        group = self.output.module["projektdefinition"]
        name = self.par.name.value
        fc = self.folders.get_table(project = name, tablename = "Teilflaechen_Plangebiet")
        layer = self.folders.get_layer("Teilflächen des Plangebiets")
        self.output.add_output(group, fc, layer)

    def add_diagramm(self):
        # Erstelle Diagramm Teilflaechen nach Hektar
        project_name = self.par.name.value
        out_graph_name = project_name + ": Teilflaechen nach Hektar"
        input_template = r"C:\ProjektCheck\4 Programminterne Daten\templates\diagrams\Teilflaechen_Hektar.grf"
        input_data = self.folders.get_table('Teilflaechen_Plangebiet', project=project_name, check=False)
        # Create the graph
        graph = arcpy.Graph()
        input_data = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"), "Teilflaechen_Plangebiet",
                                                arcpy.mapping.MapDocument("CURRENT").activeDataFrame)[0]
        # Add a vertical bar series to the graph
        graph.addSeriesBarVertical(dataSrc = input_data, fieldY = "Flaeche_ha", fieldLabel = "Name")
        graph.graphPropsGeneral.title = project_name + ": Teilflaechen des Plangebiets (Bruttoflaeche)"
        arcpy.env.addOutputsToMap = True
        arcpy.MakeGraph_management(input_template, graph, out_graph_name)
        arcpy.env.addOutputsToMap = False
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

    def remove_project_from_output(self):
        """ToDo"""

    def projekt_loeschen(self):
        projektName = self.par.existing_project.value
        arcpy.AddMessage("Projektname: " + projektName)
        # Mit dem Projektnamen zum neuen Projektpfad zusammenführen"
        projektPfad = self.folders.get_projectpath(projektName)
        arcpy.AddMessage("Suche Ordner: " + projektPfad)

        # entferne alle aktuellen Layer aus dem TOC (Locks aufheben)
        arcpy.AddMessage("Loese aktive Layer aus MXD \n")
        mxd = arcpy.mapping.MapDocument("CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            for lyr in arcpy.mapping.ListLayers(mxd, "", df):
                arcpy.mapping.RemoveLayer(df, lyr)
        del mxd

        try:

            # Überprüfen, ob der Projektordner existiert
            if(isdir(projektPfad)):
                print("Projektordner gefunden")
                arcpy.AddMessage("Projektordner gefunden \n")
                shutil.rmtree(projektPfad)
                print("Projektordner gelöscht")
                arcpy.AddMessage("Projektordner gelöscht \n")
            else:
                print("Projektordner " + projektName + " nicht gefunden \n")
                arcpy.AddMessage("Projektordner " + projektName + " nicht gefunden \n")

            arcpy.AddMessage("*********************************************************************************")
            arcpy.AddMessage("Das Projekt " + projektName + " wurde erfolgreich entfernt \n")

        except Exception as e:
            print(e)
            arcpy.AddMessage(e)
        finally:
            try:
                del cursor, delcursor
            except:
                print("")

    def projekt_kopieren(self):
        try:
            # get new Project Name as input
            projectNameOld = self.par.existing_project.value
            # allow the upload of a shapefile containg the projektgebiet
            project_name = self.par.name.value

            # copy template folder
            template_path = self.folders.get_projectpath()
            project_path = join(self.folders.PROJECT_BASE_PATH, project_name)

            try:
                shutil.copytree(template_path, project_path)
            except Exception as e:
                arcpy.AddMessage(e)
                arcpy.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
                arcpy.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
                arcpy.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
                sys.exit()

            # output information to user
            print("Succesfully copied")
            arcpy.AddMessage("Succesfully copied")
            print("New Project registered at " + project_path)
            arcpy.AddMessage("New Project registered at " + project_path)
        except Exception as e:
            arcpy.AddMessage(e)

    def projekt_anlegen(self):
        arcpy.env.overwriteOutput = True

        # get new Project input Data
        project_name = self.par.name.value
        flaeche = self.par.shapefile.value
        beginn_betrachtung = self.par.begin.value
        ende_betrachtung = self.par.end.value
        project_path = join(self.folders.PROJECT_BASE_PATH, project_name)

        # copy template folder
        try:
            shutil.copytree(self.folders.PROJECT_TEMPLATE, project_path)
        except Exception as e:
            arcpy.AddMessage(e)
            print e
            arcpy.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
            arcpy.AddMessage("Es scheint bereits ein Projekt mit diesem " +
                             "Namen zu existieren")
            arcpy.AddMessage("Bitte geben Sie einen anderen Namen ein oder " +
                             "nutzen Sie die 'Projekt löschen' Funktion in " +
                             "der Toolbox")
            sys.exit()

        # add layer teilflächen to gdb
        tfl = self.folders.get_table('Teilflaechen_Plangebiet',
        project=project_name, check=False)
        if arcpy.Exists(tfl):
            arcpy.Delete_management(tfl)
        espgcode_gk3 = 31467
        sr = arcpy.SpatialReference(espgcode_gk3)
        arcpy.Project_management(flaeche, tfl, sr)

        gdbPfad = self.folders.get_db()
        arcpy.env.workspace = gdbPfad

        # Prepare Shapefile for use in RPC

        # delete unused fields
        fieldObjList = arcpy.ListFields(tfl)
        fieldNameList = []
        for field in fieldObjList:
            if not field.required:
                fieldNameList.append(field.name)

        arcpy.DeleteField_management(tfl, fieldNameList)

        # add needed fields
        arcpy.AddField_management(tfl, "id_teilflaeche", "LONG")
        arcpy.AddField_management(tfl, "Name", "TEXT")
        arcpy.AddField_management(tfl, "Beginn_Nutzung", "LONG")
        arcpy.AddField_management(tfl, "Aufsiedlungsdauer", "LONG")
        arcpy.AddField_management(tfl, "Flaeche_ha", "DOUBLE", "", "", "", "", "", "")
        arcpy.AddField_management(tfl, "umfang_meter", "FLOAT")
        arcpy.AddField_management(tfl, "Nutzungsart", "SHORT")
        arcpy.AddField_management(tfl, "ags_bkg", "TEXT")
        arcpy.AddField_management(tfl, "gemeinde_name", "TEXT")
        arcpy.AddField_management(tfl, "validiert", "SHORT")
        #arcpy.AddField_management(teilfaechen_plangebiet, "Bilanzsumme", "FLOAT")

        # Berechne ha der Teilflaechen
        arcpy.CalculateField_management(tfl,
                                        "Flaeche_ha",
                                        "!SHAPE.AREA@HECTARES!",
                                        "PYTHON_9.3", "")

        # Berechne Gauß-Krüger-Koordinaten
        arcpy.AddGeometryAttributes_management(Input_Features = tfl,
                                                Geometry_Properties = "CENTROID_INSIDE")

        # Berechne Umfang der Flächen
        arcpy.CalculateField_management(tfl, "umfang_meter", "!shape.length@METER!", "PYTHON_9.3")

        cursor = arcpy.UpdateCursor(tfl)
        for i, row in enumerate(cursor):
            row.setValue("id_teilflaeche", i + 1)
            row.setValue("Nutzungsart", Nutzungsart.UNDEFINIERT)
            row.setValue("Name", "Flaeche_" + str(i + 1))
            row.setValue("Aufsiedlungsdauer", 1)
            row.setValue("validiert", 0)
            row.setValue("Beginn_Nutzung", beginn_betrachtung)
            cursor.updateRow(row)

        flaechen_ags = get_ags(tfl, 'id_teilflaeche')
        cursor = arcpy.UpdateCursor(tfl)
        for row in cursor:
            flaechen_id = row.id_teilflaeche
            if flaechen_id not in flaechen_ags:
                raise ValueError(
                    u'AGS für Fläche {} konnte nicht ermittelt werden'
                    .format(flaechen_id))
            ags, gen = flaechen_ags[flaechen_id]
            row.setValue('ags_bkg', ags)
            row.setValue('gemeinde_name', gen)
            cursor.updateRow(row)

        # add project-data to Projektrahmendaten

        # Den AGS aus der Lage der projektfläche im Raum ermitteln
        bkg = self.folders.get_base_table('FGDB_Basisdaten_deutschland.gdb',
                                          'bkg_gemeinden')
        workspace_projekt_definition = gdbPfad
        projektrahmendaten = join(workspace_projekt_definition,
                                  'Projektrahmendaten')
        projektFlaeche = join(workspace_projekt_definition,
                              'Teilflaechen_Plangebiet')

        arcpy.AddMessage(bkg)

        # ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
        # 1. Feature Layer aus den bkg-daten erstellen
        arcpy.MakeFeatureLayer_management(bkg, "bkg_lyr")
        # 2.Spatial Select wo Planfläche bkg_lyr intersected
        arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT",
                                               projektFlaeche)

        # Setzen des Sonderkostenfaktors auf 1 =100% - Sonderkostenfaktor wird im Themenfeld Kosten durch nutzer eingegeben und in der Tabelle aktualisiert
        sonderkostenfaktor = 1

        # loesche ggf. vorhandene zeilen in den rojektrahmendaten und fuege neue daten danach hinzu
        arcpy.DeleteRows_management(projektrahmendaten)

        cursor = arcpy.InsertCursor(projektrahmendaten)
        row = cursor.newRow()
        row.BEGINN_BETRACHTUNGSZEITRAUM = beginn_betrachtung
        row.ENDE_BETRACHTUNGSZEITRAUM = ende_betrachtung
        row.GEMEINDENAME = gen
        row.PROJEKTSPEZIFISCHER_SONDERKOSTENFAKTOR = sonderkostenfaktor
        row.PROJEKTNAME = project_name
        row.AGS = ags
        cursor.insertRow(row)

        del cursor, row

        # Minimap erzeugen
        schrittmeldung = 'Erzeuge Uebersichtskarte \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Kopiere Template.mxd
        template_folder = join(self.folders.MXDS, "Style_Minimap")
        template = join(template_folder, "template.mxd")
        mxd_template = arcpy.mapping.MapDocument(template)
        ausgabeordner_img = join(project_path,
                                 self.folders._AUSGABE_PATH, 'Abbildungen')
        os.makedirs(ausgabeordner_img)
        mxdpfad = join(ausgabeordner_img, 'Definition_Projekt.mxd')
        mxd_template.saveACopy(mxdpfad)

        # Ersetze Datenquelle
        minimap_mxd = arcpy.mapping.MapDocument(mxdpfad)
        templatepath = join(template_folder, "template.gdb")
        resultpath = gdbPfad
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

        # Exportiere Ergebnis
        minimap = join(ausgabeordner_img, 'Minimap.jpg')
        arcpy.mapping.ExportToJPEG(
            minimap_mxd,
            minimap,
            "PAGE_LAYOUT",
            resolution=150)


    # output information to user
        print("Basisdaten erfolgreich kopiert")
        arcpy.AddMessage("Basisdaten erfolgreich kopiert \n")
        # print("Neues Projekt angelegt im Ordner " + projectPath)

        arcpy.AddMessage("Neues Projekt angelegt im Ordner {}\n".format(
            project_path))

