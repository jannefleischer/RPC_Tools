#-------------------------------------------------------------------------------
# Name:        module1
# -*- coding: utf-8 -*-
# Purpose:
#
# Author:      rieffel
#
# Created:     05.03.2013
# Copyright:   (c) rieffel 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import arcpy, gc, time, os

#Variablen definieren
projektname = arcpy.GetParameterAsText(0)

#aktueller Pfad
rootPfad = str(sys.path[0]).split("2_Tool")[0]
#Pfad zur Ergebnistabelle


ergebnisTabelle = os.path.join(rootPfad,'3_Projekte',projektname,'FGDB_36_Flaeche_und_Oekologie_Projekt_'+projektname+'.gdb','Ergebnisse_oekologischeWertigkeit')
#ergebnisTabelle = rootPfad + "\\3_Projekte\\" + projektname + "\\FGDB_36_Flaeche_und_Oekologie_Projekt_" + projektname + ".gdb\\Ergebnisse_oekologischeWertigkeit"

workspace_basis = os.path.join(rootPfad,"1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb")
#workspace_basis = rootPfad+'\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\'

workspace_projekt = os.path.join(rootPfad,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
#workspace_projekt = rootPfad+'\\3_Projekte\\'+projektname+'\\FGDB_11_Definition_Projekt_'+projektname+'.gdb\\'

workspace_ergebnisse = os.path.join(rootPfad,'3_Projekte',projektname,'FGDB_36_Flaeche_und_Oekologie_Projekt_'+projektname+'.gdb')
#workspace_ergebnisse = rootPfad +'\\3_Projekte\\'+projektname+'\\FGDB_36_Flaeche_und_Oekologie_Projekt_'+projektname+'.gdb\\'

arcpy.env.overwriteOutput = True
##Daten für den Projektraum zusammenstellen
#AGS aus den Grundlagendaten extrahieren
#Wohnfläche und Nettobauland aus den Grundlagendaten extrahieren
#Wohnflaeche gesamt berechenen
Wohneinheiten_Details = os.path.join(workspace_projekt, 'Wohneinheiten_Details')
wohnflaeche_gesamt = 0
cursor = arcpy.SearchCursor(Wohneinheiten_Details)
for row in cursor:
    wohnflaecheTemp = row.Wohnflaeche_qm
    wohnflaeche_gesamt = wohnflaeche_gesamt + wohnflaecheTemp

#Nettobaulang gesamt berechnen
#Flaechenbilanz_Planung = os.path.join(workspace_projekt,'Flaechenbilanz_Planung_gruppiert')
#nettobauland_gesamt = 0
#sql = "Flaechennutzung_S1 = 'Nettobauland'"
#cursor = arcpy.SearchCursor(Flaechenbilanz_Planung,sql)

#for row in cursor:
#    print "Drin"
#    nettobauland_temp = row.Flaeche_ha
#    nettobauland_gesamt = nettobauland_gesamt + nettobauland_temp
#Änderung: Gesamtprojektfläche anstelle von nettobauland verwenden
pfad_flaeche = os.path.join(workspace_projekt,"Teilflaechen_Plangebiet")
arcpy.AddField_management(pfad_flaeche,"area_hektares","FLOAT")
arcpy.CalculateField_management(pfad_flaeche,"area_hektares","!shape.area@HECTARES!","PYTHON_9.3")

flaechengroesse = 0
cursor = arcpy.SearchCursor(pfad_flaeche)
for flaeche in cursor:
    flaechengroesse = flaechengroesse + flaeche.area_hektares
flaechengroesse = str(flaechengroesse).replace(",",".")
#Übernahme der alten Vairable damit nicht zu viel im Folgenden geändert werden muss
nettobauland_gesamt = flaechengroesse
nettobauland_gesamt = float(nettobauland_gesamt)
#Den AGS aus der Lage der projektfläche im Raum ermitteln
projektFlaeche = rootPfad + "\\3_Projekte\\" + projektname + "\\FGDB_11_Definition_Projekt_" + projektname + ".gdb\\Teilflaechen_Plangebiet"
bkg = rootPfad + "\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\bkg_gemeinden"
#ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
#1. Feature Layer aus den bkg-daten erstellen
arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
#2.Spatial Select wo Planfläche bkg_lyr intersected
arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
#Wenn Flaeche = 1, ags extrahieren
n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
if(int(n) ==1 ):
    gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
    for gemeinde in gemeindeCursor:
        ags = gemeinde.AGS
#der AGS muss noch angepasst werden, da zur bestimmung des Kreises nur die ersten 5 Stellen gebraucht werden
lenAGS = len(ags)
if (lenAGS >5):
    ags = str(ags)
    ags = ags[0:5]
    print(ags)

#Mittelwerte der einzelnen Kreistypen berechnen
#Zur schnelleren Bearbeitung wird Grundlagentabelle komplett in den Arbeitsspeicher geladen
table1 = "in_memory//GrundlagenDE"
fc = rootPfad + "\\2_Tool\\36_Flaeche_und_Oekologie\\FGDB_36_Flaeche_und_Oekologie_Tool.gdb\\GrundlagenDE"
arcpy.CopyRows_management(fc, table1)
#Erstellung einer weiteren in_memory Tabelle für die Ergebnisse der Mittelwertsberechnungen für die Kreistypen
kreise =arcpy.CreateTable_management("in_memory", "kreise" )
arcpy.AddField_management(kreise, "Kreistyp","SHORT")
arcpy.AddField_management(kreise, "Mittelwert_Wohnflaechendichte","DOUBLE")
#Die einzelnen Kreistypen werden selected und der Mittelwert für die Wohnflächendichte wird berechnet
i=1
while(i <= 9):
    sql = "Siedlungsstruktureller_Kreistyp = " + str(i)
    cursor = arcpy.SearchCursor(table1,sql)
    anzahl = 0
    wohnflaechendichte = 0
    for row in cursor:
        temp = row.Wohnflaeche_in_Wohngebaeuden_in_qm / row.Gebaeude_und_Freiflaeche_Wohnen_in_ha
        wohnflaechendichte = wohnflaechendichte + temp
        anzahl = anzahl +1
    average = wohnflaechendichte / anzahl
#Durschnittswerte der einzelnen Kreistypen in einer in_memory Tabelle ablegen
    cursor2 = arcpy.InsertCursor(kreise)
    row = cursor2.newRow()
    row.Kreistyp = i
    row.Mittelwert_Wohnflaechendichte = average
    cursor2.insertRow(row)
    i= i+1

##Zusammenstellung der Vergleichswerte
#Für das Projektgebiet
projektWohnflaechenDichte = wohnflaeche_gesamt / nettobauland_gesamt

#Für den Kreis
#Kreisdaten aus den Basisdaten Deutschland  anhand des AGS extrahieren
fc = rootPfad + "\\2_Tool\\36_Flaeche_und_Oekologie\\FGDB_36_Flaeche_und_Oekologie_Tool.gdb\\GrundlagenDE"
sql = "AGS LIKE '%" +ags +"%'"
cursor = arcpy.SearchCursor(fc,sql)
for row in cursor:
    kreistyp = row.Siedlungsstruktureller_Kreistyp
    wohnflaeche = row.Wohnflaeche_in_Wohngebaeuden_in_qm
    freiflaeche = row.Gebaeude_und_Freiflaeche_Wohnen_in_ha
    kreisName = row.Kreis_kreisfreie_Stadt
kreisWohnflaechendichte = wohnflaeche/freiflaeche
#kreisWohnflaechendichte = 0.26

#Durchschnitt fuer den Kreistyp
sql = "Kreistyp = " + str(kreistyp)
cursor3 = arcpy.SearchCursor(kreise,sql)
for row in cursor3:
    kreistypWohnflaechendichte = row.Mittelwert_Wohnflaechendichte

print("Wohnflaechendichte Projekt : " + str(projektWohnflaechenDichte))
print("Wohnflaechendichte Kreis   : " + str(kreisWohnflaechendichte))
print("Wohnflaechendichte Kreistyp: " + str(kreistypWohnflaechendichte))

##Abweichungen berechnen und Graphiken erstellen
#Abweichung Projektgebiet - Kreis
abweichung = projektWohnflaechenDichte / kreisWohnflaechendichte -1
print("Abweichung vom Kreisdurchschnitt: " + str(abweichung))
#Abweichung bewerten
if(abweichung >= 0.05):
    bewertung = 5
elif(abweichung >= 0) and (abweichung<= 0.05):
    bewertung = 4
elif(abweichung >= -0.05) and (abweichung <= 0):
    bewertung = 3
elif(abweichung >= -0.10) and (abweichung<=-0.05):
    bewertung = 2
elif(abweichung <= -0.10):
    bewertung = 1
print("Bewertung: "+str(bewertung))

#Ergebnisse in Ergebnisstabelle ablegen
#table = workspace_ergebnisse + "Ergebnisse_Wohnflaechendichte"
table= os.path.join(workspace_ergebnisse,'Ergebnisse_Wohnflaechendichte')
ergebnisse = arcpy.InsertCursor(table)
row = ergebnisse.newRow()

row.Name = projektname
row.Bewertung = bewertung
row.WohnflaechendichteProjektraum = projektWohnflaechenDichte
row.WohnflaechendichteProjektKreis = kreisWohnflaechendichte
row.WohnflaechendichteProjektKreistyp = kreistypWohnflaechendichte
lt = time.localtime()
year, monat, tag, stunde, minute = lt[0:5]
row.timestamp =  str(tag) + "." + str(monat) + "." + str(year) + " - " + str(stunde) + ":" + str(minute)
row.abweichungVonKreis = abweichung
ergebnisse.insertRow(row)
#Daten in die temp-Tabelle zur Diagrammerstellung schreiben
table = os.path.join(workspace_ergebnisse,"temp")
#table= r'C:\Users\rieffel\Dropbox\RPC\00_Entwicklungsumgebung\3_Projekte\Duesseldorf\FGDB_36_Flaeche_und_Oekologie_Projekt_Duesseldorf.gdb\temp'
#Temp-Tabelle leeren
arcpy.DeleteRows_management(table)
#Daten in die  Temp Tabelle schreiben
temp = arcpy.InsertCursor(table)
row = temp.newRow()
row.Name = projektname
row.Wohnflaechendichte_in_qm = projektWohnflaechenDichte
temp.insertRow(row)
row = temp.newRow()
row.Name = kreisName
row.Wohnflaechendichte_in_qm = kreisWohnflaechendichte
temp.insertRow(row)
row = temp.newRow()
#Bezeichung des Kreistyps aus der RaumTypen Tabelle extrahieren
#table = workspace_basis + "RaumTypen"
table2 = rootPfad+"\\2_Tool\\36_Flaeche_und_Oekologie\\FGDB_36_Flaeche_und_Oekologie_Tool.gdb\\RaumTypen"
sql = ("ID = " + str(kreistyp))
cursor4 = arcpy.SearchCursor(table2, sql)
for row1 in cursor4:
    typName = row1.Name
row.Name = typName
row.Wohnflaechendichte_in_qm = kreistypWohnflaechendichte
temp.insertRow(row)
#Diagramm erstellen
graph = arcpy.Graph()
graph.addSeriesBarVertical(table, 'Wohnflaechendichte_in_qm', fieldLabel='Name')
arcpy.MakeGraph_management("diagramm.tee", graph, "Diagramm")
output = rootPfad + "\\3_Projekte\\"+projektname + "\\Ergebnisausgabe\\Abbildungen\\36_Bewertung_Wohnflaeachendichte.png"
arcpy.SaveGraph_management("Diagramm", output, image_width=800, image_height=600)

#Image.open(output).show()


del cursor,cursor2,cursor3, cursor4, table1,kreise, ergebnisse, table, temp, row1, table2
gc.collect()