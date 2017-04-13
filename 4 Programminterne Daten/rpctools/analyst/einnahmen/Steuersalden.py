# -*- coding: utf-8 -*-

import arcpy, sys

import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell
from os.path import join, isdir, abspath, dirname, basename

from rpctools.utils.params import Tool

import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.population_lib as pop

class Steuersalden(Tool):

    _param_projectname = 'name'
    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):

        parameters = self.par
        projektname = self.par.name.value

    # Pruefen, ob Wanderungssalden-Tabelle existiert; falls ja, dann loeschen
        layer_pfad = self.folders.get_db("FGDB_Einnahmen.gdb", projektname)
        wanderungssalden_pfad = os.path.join(layer_pfad, "Wanderungssalden")
        layer_existiert = arcpy.Exists(wanderungssalden_pfad)

        if layer_existiert == 0:
            arcpy.AddMessage("Es wurden noch keine Wanderungssalden für das angegebene Projekt berechnet. Bitte zuerst 'Schritt 1: Wanderungssalden schätzen' durchführen.")
            sys.exit()

        #Löschen bisheriger Layer
        self.output.delete_output("Steuereinnahmesalden")


    # Layer "Steuereinnahmesalden" mit Gemeinden aus dem Layer "Wanderungssalden" erzeugen, vorhandenen Steuersaldo-Layer löschen

        if  arcpy.Exists("Wanderungssalden_lyr"):
            arcpy.Delete_management("Wanderungssalden_lyr")
        arcpy.MakeFeatureLayer_management(wanderungssalden_pfad, "Wanderungssalden_lyr")

        steuersalden_pfad = os.path.join(layer_pfad, "Steuersalden")
        if arcpy.Exists(steuersalden_pfad) == 1:
            arcpy.Delete_management(steuersalden_pfad)
        arcpy.CopyFeatures_management("Wanderungssalden_lyr", steuersalden_pfad)

        list_fields = []
        list_fieldobjects = arcpy.ListFields(steuersalden_pfad)
        list_fieldobjects
        for field in list_fieldobjects:
            if not field.required:
                list_fields.append(field.name)
        list_fields.remove("GEN")
        arcpy.DeleteField_management(steuersalden_pfad, list_fields)


    # Hinzufuegen leerer Spalten zu Steuersalden
        arcpy.AddField_management(steuersalden_pfad, "Grundsteuer", "LONG")
        arcpy.AddField_management(steuersalden_pfad, "Einkommensteuer", "LONG")
        arcpy.AddField_management(steuersalden_pfad, "Familienleistungsausgleich", "LONG")
        arcpy.AddField_management(steuersalden_pfad, "Gewerbesteuer", "LONG")
        arcpy.AddField_management(steuersalden_pfad, "Umsatzsteuer", "LONG")
        arcpy.AddField_management(steuersalden_pfad, "Summe_Saldo_Steuereinnahmen", "LONG")

    # Grundsteuer ermitteln
    # Dummy-Rechenweg
        grundsteuer = 999

        fields = ["Grundsteuer"]
        cursor = arcpy.da.UpdateCursor(steuersalden_pfad, fields)
        for gemeinde in cursor:
            gemeinde[0] = grundsteuer
            cursor.updateRow(gemeinde)

    # Einkommensteuer und Familienleistungsausgleich ermitteln
    # Dummy-Rechenweg
        einkommen = 888
        familienausgleich = 777

        fields = ["Einkommensteuer", "Familienleistungsausgleich"]
        cursor = arcpy.da.UpdateCursor(steuersalden_pfad, fields)
        for gemeinde in cursor:
            gemeinde[0] = einkommen
            gemeinde[1] = familienausgleich
            cursor.updateRow(gemeinde)


    # Gewerbesteuer und Umsatzsteuer ermitteln
    # Dummy-Rechenweg
        gewerbe = 666
        umsatz = 555

        fields = ["Gewerbesteuer", "Umsatzsteuer"]
        cursor = arcpy.da.UpdateCursor(steuersalden_pfad, fields)
        for gemeinde in cursor:
            gemeinde[0] = gewerbe
            gemeinde[1] = umsatz
            cursor.updateRow(gemeinde)


    # Aufsummieren der Steuereinnahmen

        fields = ["Grundsteuer", "Einkommensteuer", "Familienleistungsausgleich", "Gewerbesteuer", "Umsatzsteuer", "Summe_Saldo_Steuereinnahmen"]
        cursor = arcpy.da.UpdateCursor(steuersalden_pfad, fields)
        for gemeinde in cursor:
            gemeinde[5] = gemeinde[0] +  gemeinde[1] +  gemeinde[2] +  gemeinde[3] +  gemeinde[4]
            cursor.updateRow(gemeinde)


    # Anzeigen der Saldo-Layer

        #Grundsteuer
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Grundsteuersaldo", enhance = True, folder="einnahmen"),
                            subgroup = "Steuereinnahmesalden"
                                )
        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Grundsteuersaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )

        #Einkommensteuer
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Einkommensteuersaldo", enhance = True, folder="einnahmen"),
                            disable_other = False,
                            subgroup = "Steuereinnahmesalden"
                                )

        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Einkommensteuersaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )

        #Familienleistungsausgleich
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Familienleistungsausgleichssaldo", enhance = True, folder="einnahmen"),
                            disable_other = False,
                            subgroup = "Steuereinnahmesalden"
                                )

        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Familienleistungsausgleichssaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )

        #Gewerbesteuer
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Gewerbesteuersaldo", enhance = True, folder="einnahmen"),
                            disable_other = False,
                            subgroup = "Steuereinnahmesalden"
                                )

        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Gewerbesteuersaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )

        #Umsatzsteuer
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Umsatzsteuersaldo", enhance = True, folder="einnahmen"),
                            disable_other = False,
                            subgroup = "Steuereinnahmesalden"
                                )

        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Umsatzsteuersaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )


        #Gesamtsaldo
        self.output.add_output(group = self.output.module["einnahmen"],
                            featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                            template_layer = self.folders.get_layer(layername = "Positiver Gesamtsaldo", enhance = True, folder="einnahmen"),
                            disable_other = False,
                            subgroup = "Steuereinnahmesalden"
                                )

        self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project=projektname, tablename = "Steuersalden"),
                                template_layer = self.folders.get_layer(layername = "Negativer Gesamtsaldo", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Steuereinnahmesalden"
                                )



    #   Symbology anpassen
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        projekt_layer = self.output.get_projectlayer(projektname)
        if arcpy.mapping.ListLayers(mxd, "Negativer Grundsteuersaldo"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negativer Grundsteuersaldo")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(mxd, "Negativer Einkommensteuersaldo"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negativer Einkommensteuersaldo")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(mxd, "Negativer Familienleistungsausgleichssaldo"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negativer Familienleistungsausgleichssaldo")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(mxd, "Negativer Gewerbesteuersaldo"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negativer Gewerbesteuersaldo")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(projekt_layer, "Negativer Umsatzsteuersaldo"):
            lyr = arcpy.mapping.ListLayers(projekt_layer, "Negativer Umsatzsteuersaldo")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(mxd, "Negativer Gesamtsaldo"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negativer Gesamtsaldo")[0]
            lyr.symbology.reclassify()
        arcpy.RefreshTOC()
