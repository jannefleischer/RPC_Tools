def main():
    pass

if __name__ == '__main__':
    main()
import arcpy,sys,os
arcpy.env.overwriteOutput = True
#Parameter
projekt = arcpy.GetParameterAsText(0)
inTable_male = arcpy.GetParameterAsText(1)
inTable_female = arcpy.GetParameterAsText(2)
#Pfade
BasisPfad = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
projektPfad = os.path.join(BasisPfad, '3_Projekte', projekt)
projektGDBPfad = os.path.join(BasisPfad,'3_Projekte',projekt,'FGDB_11_Definition_Projekt_'+projekt+'.gdb')


#Tabellen importieren
arcpy.TableToTable_conversion(inTable_male,projektGDBPfad,'RegionPrognose_m')
arcpy.TableToTable_conversion(inTable_female,projektGDBPfad,'RegionPrognose_f')

pfad_prognose_m = os.path.join(projektGDBPfad,'RegionPrognose_m')
pfad_prognose_f = os.path.join(projektGDBPfad,'RegionPrognose_f')
pfad_prognose_gesamt = os.path.join(projektGDBPfad,'RegionPrognose_gesamt')
#Beide Prognosen in eine Datei kombinieren
arcpy.Merge_management([pfad_prognose_f,pfad_prognose_m],pfad_prognose_gesamt)


arcpy.AddMessage("Tabellenimport erfolgreich")