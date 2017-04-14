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
from os.path import join, isdir
import os
import shutil
import gc
import arcpy

from rpctools.utils.params import Tool
from rpctools.utils.spatial_lib import get_ags
from rpctools.utils.spatial_lib import get_gemeindetyp
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.encoding import encode

from rpctools.definitions.diagram_teilflaechen import DiaTeilflaechen


class Projektverwaltung(DiaTeilflaechen):

    _param_projectname = 'name'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        # prevent eventual locks
        gc.collect()

        arcpy.AddMessage(self.par.action.value)
        self.output.define_projection()

        if self.par.action.value == "Neues Projekt anlegen":
            self.projekt_anlegen()
            self.add_output_new_project()
            self.add_diagramm()

        elif self.par.action.value == "Bestehendes Projekt kopieren":
            self.projekt_kopieren()
            self.add_output_new_project()

        else:
            self._param_projectname = 'existing_project'
            self.projekt_loeschen()
            self.remove_project_from_output()

    def add_output_new_project(self):
        # add Teilflächen
        fc = self.folders.get_table("Teilflaechen_Plangebiet")
        layer = self.folders.get_layer("Teilflächen des Plangebiets")
        self.output.add_output("projektdefinition", layer, fc)

        # add OpenStreetmap
        layer = self.folders.get_layer("OpenStreetMap")
        self.output.add_output("hintergrundkarten", layer,
                               zoom=False, in_project=False)

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
                arcpy.AddMessage("Projektordner gefunden \n")
                shutil.rmtree(projektPfad)
                arcpy.AddMessage("Projektordner gelöscht \n")
            else:
                arcpy.AddMessage("Projektordner " + projektName + " nicht gefunden \n")

            arcpy.AddMessage("*********************************************************************************")
            arcpy.AddMessage("Das Projekt " + projektName + " wurde erfolgreich entfernt \n")

        except Exception as e:
            arcpy.AddMessage(e)

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
            arcpy.AddMessage("Succesfully copied")
            arcpy.AddMessage("New Project registered at {}".format(project_path))
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

        # check if  a) all ags of teilflaechen are identical and
        #           b) maximal distance of teilflaechen smaller than x

        # to do (Stefaan)
        ags_projekt = '02000000' # wird nebenbei bestimmt
        gemeindename_projekt = "Hamburg"# nebenbei bestimmen


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

        # epsg-code or the
        config = self.parent_tbx.config
        sr = arcpy.SpatialReference(config.epsg)
        transform_method = config.transformation
        arcpy.Project_management(flaeche, tfl, sr, transform_method)

        gdbPfad = self.folders.get_db()
        arcpy.env.workspace = gdbPfad

        # Prepare Shapefile for use in RPC

        # delete unused fields
        fieldObjList = arcpy.ListFields(tfl)
        fieldNameList = []
        for field in fieldObjList:
            if not field.required:
                fieldNameList.append(field.name)

        if fieldNameList:
            arcpy.DeleteField_management(tfl, fieldNameList)

        # add needed fields
        arcpy.AddField_management(tfl, "id_teilflaeche", "LONG")
        arcpy.AddField_management(tfl, "Name", "TEXT")
        arcpy.AddField_management(tfl, "Beginn_Nutzung", "LONG")
        arcpy.AddField_management(tfl, "Aufsiedlungsdauer", "LONG")
        arcpy.AddField_management(tfl, "Flaeche_ha", "DOUBLE")
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
        arcpy.AddGeometryAttributes_management(
            Input_Features = tfl, Geometry_Properties="CENTROID_INSIDE")

        # Berechne Umfang der Flächen
        arcpy.CalculateField_management(tfl, "umfang_meter",
                                        "!shape.length@METER!", "PYTHON_9.3")

        cursor = arcpy.UpdateCursor(tfl)
        for i, row in enumerate(cursor):
            row.setValue("id_teilflaeche", i + 1)
            row.setValue("Nutzungsart", Nutzungsart.UNDEFINIERT)
            row.setValue("Name", "Flaeche_" + str(i + 1))
            row.setValue("Aufsiedlungsdauer", 1)
            row.setValue("validiert", 0)
            row.setValue("Beginn_Nutzung", beginn_betrachtung)
            row.setValue("ags_bkg", ags_projekt)
            row.setValue("gemeinde_name", gemeindename_projekt)
            cursor.updateRow(row)


        # add project-data to Projektrahmendaten
        gemeindetyp = get_gemeindetyp(ags_projekt)

        # loesche ggf. vorhandene zeilen in den Projektrahmendaten und fuege neue daten danach hinzu
        projektrahmendaten = self.folders.get_table(tablename="Projektrahmendaten",
                                                    project=project_name)
        arcpy.DeleteRows_management(projektrahmendaten)

        cursor = arcpy.InsertCursor(projektrahmendaten)
        row = cursor.newRow()
        row.BEGINN_BETRACHTUNGSZEITRAUM = beginn_betrachtung
        row.ENDE_BETRACHTUNGSZEITRAUM = ende_betrachtung
        row.GEMEINDENAME = gemeindename_projekt
        row.PROJEKTNAME = project_name
        row.AGS = ags_projekt
        row.GEMEINDETYP = gemeindetyp
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
