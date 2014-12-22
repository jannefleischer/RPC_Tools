import arcpy, sys, os
import Einnahmen_lib as k

projektname = arcpy.GetParameterAsText(0)
#Startjahr und Endjahr aus der Tabelle 'Projektrahmendaten extrahieren
#Solange der vervielfaeltiger_gewerbesteuer nur bis 2030 vorliegt (siehe todo) wird nur bis 2030 prognostiziert
base_path = str(sys.path[0]).split("2_Tool")[0]
projektrahmendaten_pfad = os.path.join(base_path,"3_Projekte",projektname,"FGDB_11_Definition_Projekt_"+ projektname+".gdb","Projektrahmendaten")
projektrahmendaten_tabelle = arcpy.SearchCursor(projektrahmendaten_pfad)
for row in projektrahmendaten_tabelle:
    startjahr = row.Beginn_Betrachtungszeitraum
    endjahr = row.Ende_Betrachtungszeitraum
del projektrahmendaten_tabelle
try:
    del row
except:
    print ("")
if endjahr > 2030:
    endjahr=2030
dauer = endjahr-startjahr
#gewerbesteuer berechnen fuer jedes Jahr im zeitraum
jahr = startjahr
counter = 1
arcpy.AddMessage("Start: " + str(startjahr))
arcpy.AddMessage("Ende: " + str(endjahr))
#Todo Wirtschaftsabschnitt flexibel gestalten
while jahr <= endjahr:
    aufsiedlungsstand = counter/dauer * 100
    k.gewerbesteuer(projektname,jahr,aufsiedlungsstand)
    arcpy.AddMessage("Berechnung fuer das Jahr "+str(jahr))
    jahr+=1
    counter+=1






