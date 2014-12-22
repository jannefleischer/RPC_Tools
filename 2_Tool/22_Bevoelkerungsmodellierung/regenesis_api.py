# -*- coding: cp1252 -*-
import urllib2, json, arcpy, sys,os
from pprint import pprint
#api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
#(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)




# Variablen definieren
projektname = "Bultweg_Sued_fiktiv"
ags = "03353040"
jahr = "2011"
geschlecht = "gesm"
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung")
#Check ob Tabelle  mit Inhalt (Checken ob Reihe in Tabelle vorhanden & jede Zelle mit Zahlen gefüllt ist.
#check = arcpy.SearchCursor(bevoelkerung_gemeinde_pfad)

#wenn nein, Abfrage ausführen
#wenn ja, überspringen
#Abfrage Bevölkerungszahlen
#Tabelle öffnen
bevoelkerung_gemeinde = arcpy.InsertCursor(bevoelkerung_gemeinde_pfad)
row = bevoelkerung_gemeinde.newRow()
url = "http://api.regenesis.pudo.org/cube/12411gj004/facts?" #<--Altersklassen Bevölkerung
#url = "http://api.regenesis.pudo.org/cube/12411rj005/facts?" #Altersjahre
parameter = "cut=gemein.name:" + str(ags)
query = url+parameter
print query
try:
    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)
except Exception as e:
    pprint(e)
#json Datensatz Filtern und die Werte auf die entsprechenden Zellen verteilen
for eintrag in data:
    
    jahr_filter = "31.12."+jahr
    geschlecht_filter = geschlecht
    #Jahr Filtern:
    if eintrag["stag.text"] == jahr_filter and eintrag["ges.name"] == geschlecht_filter:
        column = eintrag["altx20.name"]
        value = eintrag["bevstd"]
        row.setValue(column, value)
        row.ags = ags
        row.jahr = jahr
        row.geschlecht = geschlecht

#tabelle updaten
bevoelkerung_gemeinde.insertRow(row)
del row, bevoelkerung_gemeinde

#Abfrage Wanderungsdaten
#Tabelle öffnen
wanderung_gemeinde = arcpy.InsertCursor(wanderung_gemeinde_pfad)
row = wanderung_gemeinde.newRow()
url = "http://api.regenesis.pudo.org/cube/12711gj001/facts?" #<--Altersklassen Wanderungen
#url = "http://api.regenesis.pudo.org/cube/12411rj005/facts?" #Altersjahre
parameter = "cut=gemein.name:" + str(ags)
query = url+parameter
print query
try:
    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)
except Exception as e:
    pprint(e)
#json Datensatz Filtern und die Werte auf die entsprechenden Zellen verteilen
for eintrag in data:
   # pprint(eintrag)
    jahr_filter = jahr
    geschlecht_filter = geschlecht
    #Jahr Filtern:
    if eintrag["jahr.text"] == jahr_filter and eintrag["ges.name"] == geschlecht_filter:
        pprint(eintrag["altx01.name"])
        #column = eintrag["altx01.name"]
        #value = eintrag["bev081"]
        #row.setValue(column, value)
        #row.ags = ags
        #row.jahr = jahr
        #row.geschlecht = geschlecht

#tabelle updaten
#wanderung_gemeinde.insertRow(row)
del row, wanderung_gemeinde

