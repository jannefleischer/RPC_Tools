import arcpy
import math
import rpctools.utils.config as config
import os

def get_symbology(gemeindewerte, vorzeichen):

    gemeinde_values = gemeindewerte
    anzahl_gemeinden = len(gemeindewerte)
    x = int(math.floor((anzahl_gemeinden -1) / 7))

    if vorzeichen == 1:
        gemeinde_values.sort(reverse = True)
    else:
        gemeinde_values.sort()
    arcpy.AddMessage(str(gemeinde_values))
    ref_value = gemeinde_values[x]
    folders = config.Folders()
    if vorzeichen == 1:
        symbology_path = folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "Symbologien_VZ_ProjGem_pos")
    else:
        symbology_path = folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "Symbologien_VZ_ProjGem_neg")

    cursor = arcpy.da.SearchCursor(symbology_path, ["Name_lyr_Vorlage", "Erster_Unterbrechungswert"])
    symbology_layer = None
    arcpy.AddMessage("ref: " + str(ref_value))
    if vorzeichen == 1:
        for symbology in cursor:
            arcpy.AddMessage(str(symbology[1]))
            if symbology_layer is None and symbology[1] >= ref_value:
                symbology_layer = symbology[0]
        if symbology_layer == None:
            symbology_layer = "Skala_minus_10"
    else:
        for symbology in cursor:
            if symbology[1] <= ref_value:
                symbology_layer = symbology[0]
    return str(symbology_layer)

def create_gemeindebilanzen(self, projektname):

    # Pruefen, ob Gemeindebilanzen-Tabelle existiert; falls ja, dann loeschen
        folders = config.Folders()
        layer_pfad = folders.get_db("FGDB_Einnahmen.gdb", projektname)
        wanderungssalden_pfad = os.path.join(layer_pfad, "Gemeindebilanzen")
        layer_existiert = arcpy.Exists(wanderungssalden_pfad)

        if layer_existiert == 1:
            return
        else:
        # Gemeinden im Umkreis ermitteln und speichern
            km = 20
            umkreis_km = str(km) + " Kilometers"

            workspace_basisdaten = folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')
            inputGemeinden = os.path.join(workspace_basisdaten, 'bkg_gemeinden')
            if  arcpy.Exists("gemeinden_lyr"):
                arcpy.Delete_management("gemeinden_lyr")
            arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")

            workspace_projekt_definition = folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
            projektflaechen = os.path.join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
            if  arcpy.Exists("projektflaechen_lyr"):
                arcpy.Delete_management("projektflaechen_lyr")
            arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

            workspace_projekt_einnahmen = folders.get_db('FGDB_Einnahmen.gdb', projektname)
            gemeindebilanzen = os.path.join(workspace_projekt_einnahmen, 'Gemeindebilanzen')
            arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
            arcpy.CopyFeatures_management("gemeinden_lyr", gemeindebilanzen)

            columns_kept = ["OBJECTID", "Shape", "RS", "AGS", "GEN", "BEZ", "IBZ", "BEM", "Einwohner", "SvB", "SvB_pro_Ew", "Shape_Length", "Shape_Area", "GK3_X", "GK3_Y"]
            fields = arcpy.ListFields(gemeindebilanzen)
            for field in fields:
                if not field.name in columns_kept:
                    arcpy.DeleteField_management(gemeindebilanzen, field.name)



        # Hinzuf?gen leerer Spalten zu Gemeindebilanzen
            arcpy.AddField_management(gemeindebilanzen, "Gewichtete_Ew", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "Gewichtete_SvB", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "Wanderungsanteil_Ew", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "Wanderungsanteil_SvB", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "Einw_Zuzug", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "Einw_Fortzug", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "Einw_Saldo", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "SvB_Zuzug", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "SvB_Fortzug", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "SvB_Saldo", "LONG")
            arcpy.AddField_management(gemeindebilanzen, "GrSt", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "ESt", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "FamLeistAusgl", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "GewSt", "DOUBLE")
            arcpy.AddField_management(gemeindebilanzen, "USt", "DOUBLE")



