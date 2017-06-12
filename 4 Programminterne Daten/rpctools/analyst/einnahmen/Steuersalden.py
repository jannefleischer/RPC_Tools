# -*- coding: utf-8 -*-

import os
import sys

import arcpy

from rpctools.utils.params import Tool


class Steuersalden(Tool):
    """Steuersalden-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def run(self):
        """run Steuersalden Tool"""

        subgroup = "Steuereinnahmesalden"

    # Pruefen, ob Wanderungssalden-Tabelle existiert; falls ja, dann loeschen
        layer_pfad = self.folders.get_db("FGDB_Einnahmen.gdb")
        wanderungssalden_pfad = os.path.join(layer_pfad, "Wanderungssalden")
        layer_existiert = arcpy.Exists(wanderungssalden_pfad)

        if layer_existiert == 0:
            arcpy.AddMessage(
                "Es wurden noch keine Wanderungssalden für das angegebene "
                "Projekt berechnet. Bitte zuerst "
                "'Schritt 1: Wanderungssalden schätzen' durchführen.")
            sys.exit()

        # Löschen bisheriger Layer
        self.output.delete_output(subgroup)

    # Layer "Steuereinnahmesalden" mit Gemeinden
    # aus dem Layer "Wanderungssalden" erzeugen,
    # vorhandenen Steuersaldo-Layer löschen

        if arcpy.Exists("Wanderungssalden_lyr"):
            arcpy.Delete_management("Wanderungssalden_lyr")
        arcpy.MakeFeatureLayer_management(wanderungssalden_pfad,
                                          "Wanderungssalden_lyr")

        steuersalden_pfad = os.path.join(layer_pfad, "Steuersalden")
        if arcpy.Exists(steuersalden_pfad) == 1:
            arcpy.Delete_management(steuersalden_pfad)
        arcpy.CopyFeatures_management("Wanderungssalden_lyr",
                                      steuersalden_pfad)

        list_fields = []
        list_fieldobjects = arcpy.ListFields(steuersalden_pfad)

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

        fields = ["Grundsteuer", "Einkommensteuer",
                  "Familienleistungsausgleich", "Gewerbesteuer",
                  "Umsatzsteuer", "Summe_Saldo_Steuereinnahmen"]
        cursor = arcpy.da.UpdateCursor(steuersalden_pfad, fields)
        for gemeinde in cursor:
            gemeinde[5] = gemeinde[0] + gemeinde[1] + gemeinde[2] + gemeinde[3] + gemeinde[4]
            cursor.updateRow(gemeinde)

    # Anzeigen der Saldo-Layer

        tbl_steuersalden = "Steuersalden"
        groupname = "einnahmen"
        folder = "einnahmen"

        saldos = [
            "Positiver Grundsteuersaldo",
            "Negativer Grundsteuersaldo",
            "Positiver Einkommensteuersaldo",
            "Negativer Einkommensteuersaldo",
            "Positiver Familienleistungsausgleichssaldo",
            "Negativer Familienleistungsausgleichssaldo",
            "Positiver Gewerbesteuersaldo",
            "Negativer Gewerbesteuersaldo",
            "Positiver Umsatzsteuersaldo",
            "Negativer Umsatzsteuersaldo",
            "Positiver Gesamtsaldo"
            "Negativer Gesamtsaldo"
        ]
        for layername in saldos:
            self.output.add_layer(
                groupname=groupname,
                template_layer=layername,
                template_folder=folder,
                featureclass=tbl_steuersalden,
                disable_other=False,
                subgroup=subgroup,
            )

    #   Symbology anpassen
        mxd = arcpy.mapping.MapDocument("CURRENT")
        negative_saldos = [
            "Negativer Grundsteuersaldo",
            "Negativer Einkommensteuersaldo",
            "Negativer Familienleistungsausgleichssaldo",
            "Negativer Gewerbesteuersaldo",
            "Negativer Umsatzsteuersaldo",
            "Negativer Gesamtsaldo"
        ]
        for lyrname in negative_saldos:
            # ToDo: check if to reclassify in mxd or only in project_layer
            self.output.reclassify_layer(mxd, lyrname)
        arcpy.RefreshTOC()


