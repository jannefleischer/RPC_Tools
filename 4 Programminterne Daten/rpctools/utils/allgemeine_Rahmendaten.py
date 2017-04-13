import arcpy
import rpctools.utils.config

def Bewohner_referenz_plangebiet(self, projektname):

    we_tabelle = Folders.get_table(self, tablename= "Wohnen_WE_in_Gebaeudetypen", workspace='FGDB_Definition_Projekt.gdb', project= projektname, check=True)
    fields = ["WE", "EW_je_WE"]
    einwohnerzahl = 0
    cursor = arcpy.SearchCursor(fields)
    for flaeche in cursor:
        einwohnerzahl += flaeche[0] * flaeche[1]

    return einwohnerzahl


def Erwerbstaetige_referenz_plangebiet(self, projektname):

    erwerbstaetige = 0
    pfad_rahmendaten = self.folders.get_table(
        tablename='Projektrahmendaten',
        workspace="FGDB_Definition_Projekt.gdb",
        project=projektname)
    cursor = arcpy.da.SearchCursor(pfad_rahmendaten, ["AGS", "Gemeindetyp"])
    for projekt in cursor:
        ags_projekt = projekt[0]
        gemeindetyp = projekt[1]

    table_teilflaechen = self.folders.get_table(
        tablename='Teilflaechen_Plangebiet',
        workspace="FGDB_Definition_Projekt.gdb",
        project=projektname)
    pfad_flaechenanteile_branchen = self.folders.get_table(tablename='Gewerbe_Flaechenanteile_Branchen', workspace="FGDB_Definition_Projekt.gdb", project=projektname)
    pfad_dichtekennwerte = self.folders.get_base_table(tablename = "Dichtekennwerte_Gewerbe", workspace="FGDB_Definition_Projekt_Tool.gdb")

    cursor_teilflaechen = arcpy.da.SearchCursor(table_teilflaechen, ["id_teilflaeche", "Nutzungsart", "Flaeche_ha"])
    for flaeche in cursor_teilflaechen:
        if flaeche[1] == 2:
            cursor_branchenanteile = arcpy.da.SearchCursor(pfad_flaechenanteile_branchen, ["IDTeilflaeche", "IDBranche", "Flaechenanteil"])
            for eintrag in cursor_branchenanteile:
                if flaeche[0] == eintrag[0]:
                    cursor_dichtekennwerte = arcpy.da.SearchCursor(pfad_dichtekennwerte, ["ID_Branche_ProjektCheck", "Gemeindetyp_ProjektCheck", "AP_pro_ha_brutto"])
                    for dichtekennwert in cursor_dichtekennwerte:
                        if dichtekennwert[0] == eintrag[1] and dichtekennwert[1] == gemeindetyp:
                            erwerbstaetige += dichtekennwert[2] * flaeche[2] * eintrag[2] / 100

    return erwerbstaetige



