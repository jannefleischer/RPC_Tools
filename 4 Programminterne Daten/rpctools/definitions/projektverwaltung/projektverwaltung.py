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
import numpy as np

from rpctools.utils.params import Tool
from rpctools.utils.spatial_lib import get_ags
from rpctools.utils.spatial_lib import get_gemeindetyp
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.encoding import encode

from rpctools.definitions.diagram_teilflaechen import DiaTeilflaechen


class Projektverwaltung(DiaTeilflaechen):

    _param_projectname = 'name'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def add_output_new_project(self):
        ## add Erschliessungsnetz
        fc = self.folders.get_table("Erschliessungsnetze_Linienelemente",
                                    workspace="FGDB_Kosten.gdb")
        layer = self.folders.get_layer("Erschließungsnetz")
        self.output.add_output("projektdefinition", layer, fc, zoom=False)
        
        ## add Erschliessungsnetz
        fc = self.folders.get_table("Erschliessungsnetze_Punktelemente",
                                    workspace="FGDB_Kosten.gdb")
        layer = self.folders.get_layer("Erschließungsnetz - "
                                       "punktuelle Maßnahmen")
        self.output.add_output("projektdefinition", layer, fc, zoom=False)

        # add Teilflächen
        fc = self.folders.get_table("Teilflaechen_Plangebiet")
        layer = self.folders.get_layer("Teilflächen des Plangebiets")
        self.output.add_output("projektdefinition", layer, fc)

        # add OpenStreetmap
        layer = self.folders.get_layer("OpenStreetMap")
        self.output.add_output("hintergrundkarten", layer,
                               zoom=False, in_project=False)


class ProjektAnlegen(Projektverwaltung):
    """Projet neu anlegen"""

    def run(self):
        """"""
        gc.collect()
        #self.output.define_projection()
        prject_anlegen_successful = self.projekt_anlegen()
        # test if self.projekt_anlegen() was successful
        # if not: AddMessage and delete project again
        if prject_anlegen_successful:
            self.parent_tbx.config.active_project = self.projectname
            self.add_output_new_project()
            self.add_diagramm()
        else:
            arcpy.AddMessage("Fehlerhaftes Projekt wird wieder entfernt...")
            arcpy.Delete_management(self.folders.get_projectpath(check=False))

    def projekt_anlegen(self):
        """Projekt anlegen"""
        arcpy.env.overwriteOutput = True

        # get new Project input Data
        project_name = self.projectname

        flaeche = self.par.shapefile.value
        beginn_betrachtung = self.par.begin.value
        ende_betrachtung = self.par.end.value
        project_path = self.folders.get_projectpath(check=False)

        self.copy_template(project_path)

        tfl, gdbPfad = self.copy_teilflaechen_to_gdb(project_name, flaeche)
        toolbox = self.parent_tbx
        max_dist = toolbox.config.max_area_distance
        ags_projekt, gemeindename_projekt, get_gemeinde_success = \
            self.get_gemeinde(tfl, 'OBJECTID', max_dist)

        if not get_gemeinde_success:
            return False
        self.calculate_teilflaechen_attributes(tfl,
                                               beginn_betrachtung,
                                               ags_projekt,
                                               gemeindename_projekt)


        self.set_projektrahmendaten(ags_projekt,
                                    project_name,
                                    beginn_betrachtung,
                                    ende_betrachtung,
                                    gemeindename_projekt)

        self.add_minimap(project_path, gdbPfad)


        # output information to user
        arcpy.AddMessage("Basisdaten erfolgreich kopiert \n")

        arcpy.AddMessage("Neues Projekt angelegt im Ordner {}\n".format(
            project_path))

        return True

    def set_projektrahmendaten(self,
                               ags_projekt,
                               project_name,
                               beginn_betrachtung,
                               ende_betrachtung,
                               gemeindename_projekt):
        """add project-data to Projektrahmendaten"""
        arcpy.SetProgressorLabel('Projektrahmendaten berechnen')
        arcpy.SetProgressorPosition(50)

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

    def calculate_teilflaechen_attributes(self,
                                          tfl,
                                          beginn_betrachtung,
                                          ags_projekt,
                                          gemeindename_projekt):
        """Attribute berechnen"""
        arcpy.SetProgressorLabel('Teilflächen-Attribute berechnen')
        arcpy.SetProgressorPosition(40)

        # Berechne ha der Teilflaechen
        arcpy.CalculateField_management(tfl,
                                        "Flaeche_ha",
                                        "!SHAPE.AREA@HECTARES!",
                                        "PYTHON_9.3", "")


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
            row.setValue("WE_gesamt", 0)
            row.setValue("AP_gesamt", 0)
            row.setValue("VF_gesamt", 0)
            row.setValue("Wege_gesamt", 0)
            row.setValue("Wege_MIV", 0)
            cursor.updateRow(row)

    def copy_teilflaechen_to_gdb(self, project_name, flaeche):
        """add layer teilflächen to gdb"""
        arcpy.SetProgressorLabel('Teilflächen laden')
        arcpy.SetProgressorPosition(30)

        tfl = self.folders.get_table('Teilflaechen_Plangebiet',
                                     project=project_name, check=False)
        if arcpy.Exists(tfl):
            arcpy.Delete_management(tfl)

        # epsg-code or the
        config = self.parent_tbx.config
        sr1 = arcpy.Describe(flaeche).spatialReference
        sr2 = arcpy.SpatialReference(config.epsg)
        possible_transformations = arcpy.ListTransformations(sr1, sr2)
        if not possible_transformations:
            temp_path = self.folders.get_temporary_projectpath()
            temp_shapefile = os.path.join(temp_path, 'tempfile.shp')
            sr0 = arcpy.SpatialReference(4326)
            possible_transformations = arcpy.ListTransformations(sr1, sr0)
            transform_method = possible_transformations[0]
            arcpy.Project_management(flaeche, temp_shapefile, sr0, transform_method)
            possible_transformations = arcpy.ListTransformations(sr0, sr2)
            transform_method = possible_transformations[0]
            arcpy.Project_management(temp_shapefile, tfl, sr2, transform_method)
            arcpy.Delete_management(temp_shapefile)
        else:
            transform_method = possible_transformations[0]
            arcpy.Project_management(flaeche, tfl, sr2, transform_method)

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
        arcpy.AddField_management(tfl, "WE_gesamt", "LONG")
        arcpy.AddField_management(tfl, "AP_gesamt", "LONG")
        arcpy.AddField_management(tfl, "VF_gesamt", "LONG")
        arcpy.AddField_management(tfl, "Wege_gesamt", "LONG")
        arcpy.AddField_management(tfl, "Wege_MIV", "LONG")
        #arcpy.AddField_management(teilfaechen_plangebiet, "Bilanzsumme", "FLOAT")
        return tfl, gdbPfad

    def copy_template(self, project_path):
        """copy template folder"""
        arcpy.SetProgressorLabel('Kopiere Template-Ordner')
        arcpy.SetProgressorPosition(20)

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

    def add_minimap(self, project_path, gdbPfad):
        """Minimap erzeugen"""
        arcpy.SetProgressorLabel('Minimap erzeugen')
        arcpy.SetProgressorPosition(60)

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

        arcpy.SetProgressorPosition(70)

        # Ersetze Datenquelle
        minimap_mxd = arcpy.mapping.MapDocument(mxdpfad)
        templatepath = join(template_folder, "template.gdb")
        resultpath = gdbPfad
        minimap_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)

        arcpy.SetProgressorPosition(80)

        # Setze Viewport neu
        df = arcpy.mapping.ListDataFrames(minimap_mxd)[0]
        gebietLayer = arcpy.mapping.ListLayers(
            minimap_mxd, "Teilflaechen_Plangebiet", df)[0]
        arcpy.SelectLayerByAttribute_management(
            gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
        df.extent = gebietLayer.getSelectedExtent(False)
        arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
        df.scale = df.scale * 1.4

        arcpy.RefreshActiveView()
        minimap_mxd.save()
        del mxd_template

        arcpy.SetProgressorPosition(90)

        # Exportiere Ergebnis
        minimap = join(ausgabeordner_img, 'Minimap.jpg')
        arcpy.mapping.ExportToJPEG(
            minimap_mxd,
            minimap,
            "PAGE_LAYOUT",
            resolution=150)

    def get_gemeinde(self, tfl, id_column, max_dist):
        """Verschneide Teilflächen mit Gemeinde"""
        # to do (Stefaan)
        success = True
        arcpy.SetProgressorLabel('Verschneide Teilflächen mit Gemeinde')
        arcpy.SetProgressorPosition(10)

        # calculate Gauß-Krüger-Coordinates and append them to tfl
        arcpy.AddGeometryAttributes_management(
            Input_Features=tfl, Geometry_Properties="CENTROID_INSIDE")

        # Check if the distances between the centroids is smaller than max_dist
        toolbox = self.parent_tbx
        XY_INSIDE = toolbox.query_table("Teilflaechen_Plangebiet",
                                        ['INSIDE_X', 'INSIDE_Y'])
        distances = []
        for i in range(len(XY_INSIDE)):
            for j in range(i):
                dist = np.linalg.norm(np.subtract(XY_INSIDE[i], XY_INSIDE[j]))
                distances.append(dist)
        if max(distances) > max_dist:
            arcpy.AddError("Der Abstand zwischen den Schwerpunkten der "
                           "Teilflächen darf nicht größer "
                           "als {} sein".format(max_dist))
            success = False

        # get AGS and Gemeindename and check if AGS is unique
        ags_gen = get_ags(tfl, id_column)
        ags_project = [ID[0] for ID in ags_gen.values()]
        gen_project =  [ID[1] for ID in ags_gen.values()]
        if len(np.unique(ags_project)) != 1:
            arcpy.AddError("Die Teilflächen müssen in der selben Gemeinde"
                             "liegen")
            success = False

        return ags_project[0], gen_project[0], success


class ProjektKopieren(Projektverwaltung):
    _param_projectname = 'name'

    def run(self):
        """"""
        self.output.define_projection()
        self.projekt_kopieren()
        self.add_output_new_project()
        self.add_diagramm()

    def projekt_kopieren(self):
        """"""
        arcpy.SetProgressorLabel('Kopiere Projekt')
        arcpy.SetProgressorPosition(10)

        # get new Project Name as input
        projectNameOld = self.par.existing_project.value

        # copy template folder
        template_path = self.folders.get_projectpath(projectNameOld)
        project_path = self.folders.get_projectpath(check=False)

        try:
            def ignore_locks(path, filenames):
                return [f for f in filenames if f.endswith('.lock')]
            shutil.copytree(template_path, project_path, ignore=ignore_locks)
        except Exception as e:
            arcpy.AddMessage(e)
            arcpy.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
            arcpy.AddMessage("Es scheint bereits ein Projekt "
                             "mit diesem Namen zu existieren")
            arcpy.AddMessage("Bitte geben Sie einen anderen Namen ein "
                             "oder nutzen Sie die 'Projekt löschen' Funktion "
                             "in der Toolbox")
            sys.exit()

        arcpy.SetProgressorPosition(70)

        # output information to user
        arcpy.AddMessage("Succesfully copied")
        arcpy.AddMessage("New Project registered at {}".format(project_path))


class ProjektLoeschen(Tool):

    def run(self):
        # prevent eventual locks
        gc.collect()

        arcpy.AddMessage(encode('Lösche Projekte'))

        projects_to_delete = self.par.projekte.values
        step = 100 / len(projects_to_delete)
        pos = 0
        for project in projects_to_delete:
            pos += step
            arcpy.SetProgressorPosition(pos)
            arcpy.SetProgressorLabel(
                encode('Lösche Projekt {}'.format(project)))
            self.compact_gdbs(project)
            self.remove_project_from_output(project)
            self.projekt_loeschen(project)
        config = self.parent_tbx.config
        # change active project, if it was deleted
        if config.active_project in projects_to_delete:
            projects = self.folders.get_projects()
            config.active_project = projects[0] if len(projects) > 0 else ''

    def compact_gdbs(self, project):
        """
        compact all filegeodatabases to remove locks
        """
        projektPfad = self.folders.get_projectpath(project)
        for root, dirs, files in os.walk(projektPfad):
            for folder in dirs:
                if folder.endswith(".gdb"):
                    gdb = join(root, folder)
                    arcpy.AddMessage('Compact {}'.format(gdb))
                    try:
                        res = arcpy.Compact_management(gdb)
                        # del res could help to avoid schema locks
                        del res
                        gc.collect()
                        arcpy.AddMessage('Delete {}'.format(gdb))
                        res = arcpy.Delete_management(gdb)
                        del res
                    except arcpy.ExecuteError:
                        # .gdb-folder is no valid fgdb
                        # try with shutil.rmtree instead
                        shutil.rmtree(gdb, ignore_errors=True)

    def remove_project_from_output(self, project):
        """Remove Layers under Project GroupLayer"""
        # entferne alle aktuellen Layer aus dem TOC (Locks aufheben)
        arcpy.AddMessage("Loese aktive Layer aus MXD \n")
        mxd = arcpy.mapping.MapDocument("CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            project_layer = self.output.get_projectlayer(project)
            for lyr in arcpy.mapping.ListLayers(project_layer, "", df):
                arcpy.mapping.RemoveLayer(df, lyr)
        del mxd

    def projekt_loeschen(self, project_name):
        arcpy.AddMessage("Projektname: " + project_name)
        # Mit dem Projektnamen zum neuen Projektpfad zusammenführen"
        projektPfad = self.folders.get_projectpath(project_name)
        arcpy.AddMessage("Suche Ordner: " + projektPfad)

        # Überprüfen, ob der Projektordner existiert
        if isdir(projektPfad):
            arcpy.AddMessage("Projektordner gefunden \n")
            shutil.rmtree(projektPfad, ignore_errors=True)
            try:
                arcpy.Delete_management(projektPfad)
            except:
                pass
            arcpy.AddMessage("Projektordner gelöscht \n")
        else:
            arcpy.AddMessage("Projektordner " + project_name + " nicht gefunden \n")

        arcpy.AddMessage("*********************************************************************************")
        arcpy.AddMessage("Das Projekt " + project_name + " wurde erfolgreich entfernt \n")
