import arcpy
import rpctools.utils.config

def Bewohner_referenz_plangebiet(projektname):

    we_tabelle = Folders.get_table(self, tablename= "Wohnen_WE_in_Gebaeudetypen", fgdb='FGDB_Definition_Projekt.gdb', project= projektname, check=True)
    fields = ["WE", "EW_je_WE"]
    einwohnerzahl = 0
    cursor = arcpy.SearchCursor(fields)
    for flaeche in cursor:
        einwohnerzahl += flaeche[0] * flaeche[1]

    return einwohnerzahl
