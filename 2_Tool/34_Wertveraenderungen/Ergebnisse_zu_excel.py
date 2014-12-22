# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Wertveraenderung_Einzelhandel
# Purpose:
#
# Author:      Sebastian Sieh
#
# Created:     09.04.2014
# Copyright:   (c) hoe023 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os, xlsxwriter, imp, csv, sys, datetime, math

# import sheet_lib as sl
sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

projektname = 'HCU_ZGB_OTLindenEZH' # haendische Ueberbrueckung bei manueller Scriptnutzung
##projektname = str(arcpy.GetParameterAsText(0))

base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_basis_daten_wert=os.path.join(base_path,'2_Tool',"34_Wertveraenderungen",'FGDB_34_Wertveraenderungen_Tool.gdb')
workspace_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_wertveraederung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_34_Wertveraenderungen_'+projektname+'.gdb')
workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
arcpy.env.workspace = workspace_projekt
arcpy.env.overwriteOutput = True


schrittmeldung = 'Datenexport in Excel-Datei  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung
#==================================================================================================================================================================================
#Kopiere Template.mxd
try:
    arcpy.DeleteFeatures_management(os.path.join(workspace_wertveraederung,"Teilflaechen_Plangebiet"))
except:
    pass
arcpy.Copy_management(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet"),os.path.join(workspace_wertveraederung,"Teilflaechen_Plangebiet"))

mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","34_Wertveraenderungen","34_Template_Kartenerzeugung","34_KK_Bindung_Template.mxd"))
mxdpfad = os.path.join(workspace_projekt_ergebnisse,'34_KK_Bindung.mxd')
mxd_template.saveACopy(mxdpfad)

# Ersetze Datenquelle
Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
templatepath = os.path.join(base_path,"2_Tool","34_Wertveraenderungen","34_Template_Kartenerzeugung","template.gdb")
resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_34_Wertveraenderungen_"+projektname+".gdb")
Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)

#==================================================================================================================================================================================
# Ersetze Datenquelle
Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
templatepath = os.path.join(base_path,"2_Tool","34_Wertveraenderungen","34_Template_Kartenerzeugung","template.gdb")
resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_34_Wertveraenderungen_"+projektname+".gdb")
Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
# Setze Viewport neu
df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Siedlungszahlendaten_planfall", df)[0]

##print gebietLayer
##arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
arcpy.SelectLayerByLocation_management(gebietLayer, "WITHIN_A_DISTANCE", os.path.join(workspace_wertveraederung,"Neuer_Markt"), "1 Kilometers", "NEW_SELECTION")
df.extent = gebietLayer.getSelectedExtent(False)
arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
df.scale = df.scale * 3.0

arcpy.RefreshActiveView()
Haltestellen_mxd.save()
del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

#Exportiere Ergebnis
arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "34_KK_Bindung.jpg"), "PAGE_LAYOUT",resolution=300)

schrittmeldung = 'Uebersichtskarte der KK-Bindung erstellt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

del Haltestellen_mxd

#==================================================================================================================================================================================
mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","34_Wertveraenderungen","34_Template_Kartenerzeugung","34_Bestand_Template.mxd"))
mxdpfad = os.path.join(workspace_projekt_ergebnisse,'34_Bestand.mxd')
mxd_template.saveACopy(mxdpfad)

# Ersetze Datenquelle
Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
templatepath = os.path.join(base_path,"2_Tool","34_Wertveraenderungen","34_Template_Kartenerzeugung","template.gdb")
resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_34_Wertveraenderungen_"+projektname+".gdb")
Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
# Setze Viewport neu
df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Einzelhandelstandorte", df)[0]

##print gebietLayer
##arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
arcpy.SelectLayerByLocation_management(gebietLayer, "WITHIN_A_DISTANCE", os.path.join(workspace_wertveraederung,"Teilflaechen_Plangebiet"), "1.5 Kilometers", "NEW_SELECTION")
df.extent = gebietLayer.getSelectedExtent(False)
arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
df.scale = df.scale * 3.0

arcpy.RefreshActiveView()
Haltestellen_mxd.save()
del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

#Exportiere Ergebnis
arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "34_Bestandregion.jpg"), "PAGE_LAYOUT",resolution=300)

schrittmeldung = 'Uebersichtskarte der Bestandregion erstellt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

del Haltestellen_mxd
#==================================================================================================================================================================================
#############################################################################################################
# 1. Dokument einrichten

# Pfade setzen
logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
excelpfad = os.path.join(ausgabeordner,'34_Wertveraenderung_Versorgung.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblätter anlegen
wb = xlsxwriter.Workbook(excelpfad)
sl.infosheet(projektname, str("Wertveraenderung Versorgung").decode('utf-8'), wb)
ws2 = wb.add_worksheet('Beschreibung des Wirkungsfeldes')
ws2.set_column(1, 1, 120)
##ws2.set_column(2, 2, 30)
##ws2.set_column(3, 3, 25)
##ws2.set_column(4, 4, 22)
##ws2.set_column(5, 5, 50)


# Styles anlegen
head = wb.add_format({'bold': True, 'font_size': '24', 'align': 'left','valign': 'vcenter', 'bg_color': 'white', 'border': '0'})
normal = wb.add_format({'font_size': '14', 'bg_color': 'white', 'border': '0'})
rechts = wb.add_format({'font_size': '14', 'align' : 'right', 'bg_color': 'white', 'border': '0'})
bold = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0'})
bold_rechts = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0', 'align' : 'right'})

background = wb.add_format({'bg_color': 'white', 'border': '0'})

# Hintergrund weiss faerben
for x in range(0,200):
    for y in range(0,200):
        ws2.write(x,y,"", background)

#############################################################################################################
# 2.Beschreibung des Wirkungsfeldes
ws2.write(2, 1, "Beschreibung des Wirkungsfeldes".decode('utf-8'), bold)
ws2.write(3, 1, "Die Ergebnisse stellen die zu erwartenden Umsatzverdrängungen für den Bestand im Lebensmitteleinzelhandel dar, die ".decode('utf-8'))
ws2.write(4, 1, "durch ein neues Vorhaben in der Kommune und/oder der Region im Durchschnitt zu erwarten sind. Grundlage hierfür sind ".decode('utf-8'))
ws2.write(5, 1, "Änderungen des Einkaufsverhaltens (und damit der Kaufkraftströme), die sich durch einen neuen Lebensmittelmarkt ergeben.".decode('utf-8'))
ws2.write(6, 1, "Betrachtet werden (je nach Auswahl) vor allem tangierte Zentren, also Innenstädte, Stadtteil- und Nahversorgungszentren, ".decode('utf-8'))
ws2.write(7, 1, "einzelne Versorgungsstandorte innerhalb der Kommune und ggf. angrenzende Kommunen. Die Modellierung beruht auf einer".decode('utf-8'))
ws2.write(8, 1, "bundesweit durchgeführten, telefonischen Haushaltsbefragung von 4.026 Haushalten (10.468 Personen) zu insgesamt 6.122 ".decode('utf-8'))
ws2.write(9, 1, "Einkaufsvorgängen (erster und zweiter Haupteinkaufsort) in unterschiedlichen siedlungsstrukturellen Kontexten. Unter ".decode('utf-8'))
ws2.write(10, 1, "Berücksichtigung der jeweiligen Konkurrenzsituation in den Kommunen und der Region kann daraus in Abhängigkeit vom ".decode('utf-8'))
ws2.write(11, 1, "Betriebstyp, Stadt-/Gemeindegröße und der Entfernung zwischen Wohnort und Lebensmittelmarkt die Einkaufswahrscheinlichkeit ".decode('utf-8'))
ws2.write(12, 1, "eines Haushalts/einer Person zum jeweiligen Markt dargestellt werden – abgebildet als Exponentialfunktion. Die angewendeten ".decode('utf-8'))
ws2.write(13, 1, "Exponentialfunktionen für die Märkte innerhalb der Kommune, in der das Planvorhaben abgebildet wird, finden Sie in der ".decode('utf-8'))
ws2.write(14, 1, "Tabelle „Exponentialfunktion Standortkommune“.  ".decode('utf-8'))
ws2.write(15, 1, "Je nach Stadt-/Gemeindegröße und Anbieter sind dabei Modifizierungen vorgenommen worden. Bei den Berechnungen wurde ".decode('utf-8'))
ws2.write(16, 1, "zusätzlich ein Attraktivitätsfaktor einbezogen, der die Konkurrenzsituation von Märkten des gleichen Anbieters berücksichtigt. ".decode('utf-8'))

#####################################################################################################################################
ws3 = wb.add_worksheet('Expofunktion Standortkommune')
ws3.set_column(1, 1, 35)
ws3.set_column(2, 3, 20)
#Dichtesten SM zum untersuchungsgebiet finden -> Gemeindeklasse erhalten
##cur_Standorte_Search= arcpy.SearchCursor(workspace_wertveraederung+"\Standortdaten_planfall")
##cur_Centroid_RPC= arcpy.SearchCursor(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet_Centroide"))
##RPC_X=0;
##RPC_Y=0;
##for zeile in cur_Centroid_RPC:
##    RPC_X=zeile.POINT_X
##    RPC_Y=zeile.POINT_Y
##    break
##
##del zeile,cur_Centroid_RPC
##
##entfernung=9999999
##Gemeindeklasse=0
##for zeile in cur_Standorte_Search:
##
##    if (math.sqrt(math.pow( abs(zeile.Lon - RPC_X),2)+math.pow( abs(zeile.Lat - RPC_Y),2))<=entfernung):
##        #etwas dichteres gefunden
##        entfernung=math.sqrt(math.pow( abs(zeile.Lon - RPC_X),2)+math.pow( abs(zeile.Lat - RPC_Y),2))
##        Gemeindeklasse=zeile.Gemeindeklasse

##if gemeindeklasse==0:
## keine ahnung
Gemeindeklasse=2

##del zeile,cur_Standorte_Search

if Gemeindeklasse==1:
#Ueber_100kEW:
    expofunktion="Ueber_100kEW"
elif Gemeindeklasse==2:
#Zwischen_50k_100kEW
    expofunktion="Zwischen_50k_100kEW"
elif Gemeindeklasse==3:
#Zwischen_20k_50kEW:
    expofunktion="Zwischen_20k_50kEW"
elif Gemeindeklasse==4:
#Zwischen_10k_20kEW:
    expofunktion="Zwischen_10k_20kEW"
else:
    arcpy.AddMessage("Fehler bei den Gemeindeklassen")
    print "Fehler bei den Gemeindeklassen"

cur_Expo_Funktion = arcpy.SearchCursor(os.path.join(workspace_basis_daten_wert,expofunktion))
spaltennamen = [f.name for f in arcpy.ListFields(os.path.join(workspace_basis_daten_wert,expofunktion))]
spaltennamen=spaltennamen[1:]
for n, spalten in  enumerate( spaltennamen):
    if n==0:
        ws3.write(2,n+1,str(spalten),bold)
    else:
        ws3.write(2,n+1,str(spalten),bold_rechts)



for n, zeilen in enumerate( cur_Expo_Funktion):
    ws3.write(n+3,1,zeilen.Typ.decode('utf-8'))
    ws3.write(n+3,2,zeilen.Faktor_EXP)
    ws3.write(n+3,3,zeilen.Hochzahl)

del cur_Expo_Funktion ,spaltennamen

################################################################################################################
ws4 = wb.add_worksheet('Konkurrenzsituation der Maerkte')
ws4.set_column(1, 1, 120)

# 3.Beschreibung des Wirkungsfeldes
ws4.write(2, 1, "Darstellung der IST-Situation in der Region".decode('utf-8'), bold)
ws4.write(3, 1, "Die Berechnung der Konkurrenzsituation der Märkte zueinander basiert auf Routings von Siedlungszelle zum potentiellen ".decode('utf-8'))
ws4.write(4, 1, "Versorgungsstandort, dabei wurden Entfernungen zwischen Siedlungszelle und Markt von bis zu 20 km berücksichtigt. Grundlage ".decode('utf-8'))
ws4.write(5, 1, "der Ergebnisse sind Luftliniendistanzen unter Berücksichtigung eines Ungenauigkeitsfaktors.  ".decode('utf-8'))
ws4.write(6, 1, "Agglomerationsvorteile, die sich aus der direkten Lage der einzelnen Standorte zueinander ergeben (z. B. bei sogenannten ".decode('utf-8'))
ws4.write(7, 1, "Koppelstandorten), wurden bei den Berechnungen nicht berücksichtigt. Basis für die Berechnungen ist der Bestand an  ".decode('utf-8'))
ws4.write(8, 1, "Lebensmittelmärkten in der Region und dem Tabellenblatt „Bestand Region“ zu entnehmen. ".decode('utf-8'))
ws4.write(9, 1, "Bezieht man die vorhandene Kaufkraft vor Ort in die Berechnungen ein, kann daraus der anzunehmende Jahresumsatz in der ".decode('utf-8'))
ws4.write(10, 1, "Warengruppe Lebensmittel je Standort (d. h. je Lebensmittelmarkt) ermittelt werden. Die vorhandene Kaufkraft vor Ort ".decode('utf-8'))
ws4.write(11, 1, "ergibt sich aus den folgenden Parametern: ".decode('utf-8'))
ws4.write(12, 1, "     • Einwohnerzahl auf kommunaler Ebene ".decode('utf-8'))
ws4.write(13, 1, "     • anteilige Verteilung der Einwohner in den Kommunen auf Siedlungszellen (mit den Kantenlängen 250 mal 250 Meter) auf ".decode('utf-8'))
ws4.write(14, 1, "        Grundlage einer Auswertung der bestehenden Telefonanschlüsse (Disaggregierung)".decode('utf-8'))
ws4.write(15, 1, "     • Verbrauchsausgaben im periodischen Bedarfsbereich (d. h. Lebensmittel, Drogerieartikel (Körperpflege/Putzmittel),  ".decode('utf-8'))
ws4.write(16, 1, "        Tiernahrung, Zeitungen/Zeitschriften) Ø p. P.: 2.924,- € p. a., davon anteilig in Lebensmittelmärkten: 78,02 % ".decode('utf-8'))
ws4.write(17, 1, "        (Quelle: Statistisches Bundesamt (Hrsg.)(2009): Binnenhandel, Gastgewerbe, Tourismus – Fachserie 6, Reihe 4; ".decode('utf-8'))
ws4.write(18, 1, "        eigene Berechnungen und Aktualisierungen)".decode('utf-8'))
ws4.write(19, 1, "Aus der Delta-Betrachtung der anzunehmenden Jahresumsätze (brutto) für alle Standorte vor und nach Realisierung des Planvorhabens ".decode('utf-8'))
ws4.write(20, 1, "kann dann die zu erwartende Umsatzverdrängung auf den Bestand abgeleitet werden. ".decode('utf-8'))

################################################################################################################
ws5 = wb.add_worksheet('Bestand Region')
ws5.set_column(1, 1, 5)
ws5.set_column(2, 2, 30)
ws5.set_column(3, 3, 10)
ws5.set_column(4, 4, 30)
ws5.set_column(5, 6, 25)
ws5.set_column(7, 7, 7)
ws5.set_column(8, 8, 13)

ws5.write(2, 1, 'Bestand Lebensmittelmärkte in der Region'.decode('utf-8'), bold)
ws5.write(3, 1, "ID".decode('utf-8'), bold)
ws5.write(3, 2, "Name / Anbieter".decode('utf-8'), bold)
ws5.write(3, 3, "Postleitzahl".decode('utf-8'), bold)
ws5.write(3, 4, "Ort".decode('utf-8'), bold)
ws5.write(3, 5, "Ortsteil".decode('utf-8'), bold)
ws5.write(3, 6, "Strasse".decode('utf-8'), bold)
ws5.write(3, 7, "HNR".decode('utf-8'), bold)
ws5.write(3, 8, "VKFL gesamt".decode('utf-8'), bold)

cur_Standorten = arcpy.SearchCursor(workspace_wertveraederung+"\Standortdaten")
for n, zeile in enumerate( cur_Standorten):
    ws5.write(n+4,1,zeile.Id)
    ws5.write(n+4,2,zeile.Betriebstyp)
    ws5.write(n+4,3,zeile.PLZ)
    ws5.write(n+4,4,zeile.Ort)
    ws5.write(n+4,5,zeile.Ortsteil)
    ws5.write(n+4,6,zeile.Strasse)
    ws5.write(n+4,7,zeile.HNR)
    ws5.write(n+4,8,zeile.VKFL_gesamt)


ws5.write(3, 10, "Uebersichtskarte des Einzelhandels in der Region".decode('utf-8'), bold)
image = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "34_Bestandregion.jpg")
ws5.insert_image('K5', image, {'x_scale': 0.25, 'y_scale': 0.25})
del image


################################################################################################################
ws6 = wb.add_worksheet('Darstellung der Teilergebnisse')
ws6.set_column(1, 1, 120)


ws6.write(2, 1, "Darstellung der Teilergebnisse I".decode('utf-8'), bold)
ws6.write(3, 1, "Für den neuen Lebensmittelmarkt ergibt sich daraus eine zu erwartende Kaufkraftbindung, wie sie auf dem Tabellenblatt ".decode('utf-8'))
ws6.write(4, 1, "„Kaufkraftbindung neuer Standort“ dargestellt ist. Grundlage hierfür sind die oben aufgeführten Annahmen zur Kaufkraftbindung ".decode('utf-8'))
ws6.write(5, 1, "in Abhängigkeit von der Einwohnerdichte, des Kaufkraftniveaus und der Konkurrenzsituation vor Ort. Der daraus abgeleitete  ".decode('utf-8'))
ws6.write(6, 1, "zu erwartende jährliche Gesamtumsatz sowie die Flächenproduktivität (Umsatz pro m² Verkaufsfläche) für den neuen ".decode('utf-8'))
ws6.write(7, 1, "Lebensmittelmarkt ist dem Tabellenblatt „Umsatz Planvorhaben“ zu entnehmen. Hierin enthalten sind alle Bruttoumsätze ".decode('utf-8'))
ws6.write(8, 1, "aus den Warengruppen des periodischen Bedarfsbereiches, d. h. Lebensmittel, Drogerieartikel (Körperpflege/Putzmittel),  ".decode('utf-8'))
ws6.write(9, 1, "Tiernahrung, Zeitungen/Zeitschriften. Sogenannte Nonfood II-Artikel wie Bekleidung, Schuhe, Multimedia-Artikel etc., die in vielen  ".decode('utf-8'))
ws6.write(10, 1, "Lebensmitteldiscountern und Supermärkten als Aktionsware angeboten werden, sind in den ausgewiesenen Umsätzen nicht enthalten.".decode('utf-8'))

################################################################################################################
ws7 = wb.add_worksheet('KK Bindung neuer Standort')


# Hintergrund weiss faerben
for x in range(0,200):
    for y in range(0,200):
        ws3.write(x,y,"", background)

ws7.write(2, 1, "Kaufkraftbindung durch den neuen bzw. erweiterten Markt".decode('utf-8'), bold)
image = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "34_KK_Bindung.jpg")
ws7.insert_image('B4', image, {'x_scale': 0.25, 'y_scale': 0.25})
del image

################################################################################################################
ws8 = wb.add_worksheet('Umsatz Planvorhabens')
ws8.set_column(1, 1, 30)
ws8.set_column(2, 2, 12)

ws8.write(2, 1, "Umsatz des Planvorhabens".decode('utf-8'), bold)

cur_statistik=arcpy.SearchCursor(workspace_wertveraederung+"\Statistik_planfall")
umsaetze=[]
for zeile in cur_statistik:
    umsaetze.append(zeile.SUM_ID_600)
    try:
        umsaetze.append(zeile.SUM_ID_601)
    except:
        #kein weiteren markt
        pass

del cur_statistik
ws8.write(3,1,"%.2f" % (umsaetze[0]/1000000))
ws8.write(3,2,"Mio € (brutto)".decode('utf-8'))

if len(umsaetze)>1:
    ws8.write(3,3,"MarktID 600")
    ws8.write(4,1,"%.2f" % (umsaetze[1]/1000000))
    ws8.write(4,2,"-Mio € (brutto)".decode('utf-8'))
    ws8.write(4,3,"MarktID 601")
del umsaetze

################################################################################################################
ws9 = wb.add_worksheet('Darstellung der Teilergebnisse2')
ws9.set_column(1, 1, 120)


ws9.write(2, 1, "Darstellung der Teilergebnisse II".decode('utf-8'), bold)
ws9.write(3, 1, "Das Verfahren zur Berechnung der Kaufkraftbindung wird in diesem Wirkungsfeld auf sämtliche Standorte von Lebensmittelmärkten ".decode('utf-8'))
ws9.write(4, 1, "in der Region angewendet. Aus der Gegenüberstellung zwischen den errechneten Umsätzen vor der (geplanten) Ansiedlung des ".decode('utf-8'))
ws9.write(5, 1, "Lebensmittelmarktes und nach Realisierung des Marktes ergibt sich ein Delta, d. h. eine Differenz der zu erwartenden Umsätze im ".decode('utf-8'))
ws9.write(6, 1, "Lebensmittelbereich. Hieraus wird dann die zu erwartende durchschnittliche Umsatzverdrängung für den Bestand abgeleitet, die ".decode('utf-8'))
ws9.write(7, 1, "Ergebnisse sind im Tabellenblatt „Umsatzveränderung für den Bestand“ dargestellt. Die Darstellung beschränkt sich somit  ".decode('utf-8'))
ws9.write(8, 1, "ausschließlich auf die zu erwartenden „negativen“ Effekte und soll erste Anhaltspunkte geben, welche Bereiche innerhalb einer ".decode('utf-8'))
ws9.write(9, 1, "Kommune oder welche Kommune durch zu erwartende Umsatzverdrängung nach einer ersten allgemeinen Betrachtung besonders negativ ".decode('utf-8'))
ws9.write(10, 1, "von dem geplanten Vorhaben beeinflusst werden. Positive Effekte für direkt angrenzende Märkte, die sich ggf. durch  ".decode('utf-8'))
ws9.write(11, 1, "Agglomerationseffekte (z. B. in bestehenden Zentren) ergeben, sind in der Darstellung nicht enthalten. Die überschlägig  ".decode('utf-8'))
ws9.write(12, 1, "ermittelten Verdrängungseffekte stellen eine erste durchschnittliche Einschätzung zu den zu erwartenden Auswirkungen ".decode('utf-8'))
ws9.write(13, 1, "des neuen Marktes/der neuen Märkte dar. Sie ersetzen jedoch nicht eine detaillierte Einzelfallprüfung, wie sie auf ".decode('utf-8'))
ws9.write(14, 1, "Basis der Regelungen des § 11 Abs. 3 BauNVO bzw. des § 34 Abs. 3 BauGB erstellt werden.".decode('utf-8'))

################################################################################################################
ws10 = wb.add_worksheet('Umsatzveraenderung Bestand')
ws10.set_column(1, 1, 30)
ws10.set_column(2, 3, 19)
ws10.set_column(4, 4, 15)
ws10.set_column(5, 5, 20)
ws10.write(2, 1, "Umsatzveränderung Bestand".decode('utf-8'), bold)
ws10.write(3, 2, "Umsatz Nullfall".decode('utf-8'), bold)
ws10.write(3, 3, "Umsatz Planfall".decode('utf-8'), bold)
ws10.write(3, 4, "Verlust in %".decode('utf-8'), bold)
ws10.write(3, 5, "Verlust (absolut)".decode('utf-8'), bold)
cur_verlustrech_sear= arcpy.SearchCursor(workspace_wertveraederung+"\Verlustrechnung")

for n, zeile in enumerate( cur_verlustrech_sear):
    ws10.write(n+4,1,zeile.Kommune)
    ws10.write(n+4,2,"%.2f" % (zeile.Umsatz_vorher/1000000))
    ws10.write(n+4,3,"%.2f" % (zeile.Umsatz_nachher/1000000))
    ws10.write(n+4,4,"%.2f" % zeile.Differenz_Proz)
    ws10.write(n+4,5,"%.2f" % (zeile.Differenz/1000000))

del cur_verlustrech_sear

################################################################################################################
ws11 = wb.add_worksheet('Darstellung der Teilergebnisse3')
ws11.set_column(1, 1, 120)


ws11.write(2, 1, "Darstellung der Teilergebnisse III".decode('utf-8'), bold)
ws11.write(3, 1, " Zur Bewertung der überschlägig ermittelten Verdrängungswirkung durch das neue Vorhaben ist unter anderem von Bedeutung, wie gut ".decode('utf-8'))
ws11.write(4, 1, "oder schlecht die derzeitige Versorgungssituation in der Region ist. Auf Basis des angegebenen Bestands an Lebensmittelmärkten  ".decode('utf-8'))
ws11.write(5, 1, "in der Region und der durchschnittlichen Kaufkraftbindung je Markt ergeben sich je Kommune die Ausstattungskennziffern  ".decode('utf-8'))
ws11.write(6, 1, "Verkaufsflächendichte und Handelszentralität vor der Ansiedlung des geplanten Marktes (siehe Tabellenblatt „Ausstattungskennziffern“). ".decode('utf-8'))
ws11.write(7, 1, " ".decode('utf-8'))
ws11.write(8, 1, "Dabei gibt die Kennziffer Verkaufsflächendichte im periodischen Bedarfsbereich (qm Verkaufsfläche pro Einwohner) das Verhältnis der  ".decode('utf-8'))
ws11.write(9, 1, "gesamten Verkaufsfläche der Lebensmittelmärkte zur Einwohnerzahl wider. Je höher der Wert, desto besser ist die Ausstattung im jeweiligen   ".decode('utf-8'))
ws11.write(10, 1, "Betrachtungsraum. Die Kennziffer Handelszentralität gibt das Verhältnis zwischen am Ort erwirtschaftetem Umsatz (brutto) und vorhandener ".decode('utf-8'))
ws11.write(11, 1, "Kaufkraft wider. Bei Werten unter 100 % existieren saldierte Kaufkraftabflüsse, bei Werten über 100 % ist der jeweilige Ort durch   ".decode('utf-8'))
ws11.write(12, 1, "saldierte Kaufkraftzuflüsse im jeweiligen Bedarfsbereich gekennzeichnet.".decode('utf-8'))
ws11.write(13, 1, " ".decode('utf-8'))
ws11.write(14, 1, "Die Daten beziehen sich jeweils auf den gesamten periodischen Bedarfsbereich (also auf Lebensmittel, Drogerieartikel   ".decode('utf-8'))
ws11.write(15, 1, "(Körperpflege/Putzmittel), Tiernahrung, Zeitungen/Zeitschriften), die Flächen und Umsätzen beziehen sich jedoch ausschließlich ".decode('utf-8'))
ws11.write(16, 1, "auf Lebensmittelmärkte (unabhängig von deren Größe), Drogeriemärkte, Tankstellenshops und Getränkemärkte sind in der Darstellung ".decode('utf-8'))
ws11.write(17, 1, "nicht enthalten und könn(t)en die Ausstattungskennziffern ggf. noch deutlich erhöhen. ".decode('utf-8'))
ws11.write(18, 1, "Die zu erwartenden Änderungen der Ausstattungskennziffern durch das geplanten Vorhaben sind dem Tabellenblatt „Delta-Ausstattungskennziffern“ zu entnehmen.  ".decode('utf-8'))

################################################################################################################
ws12 = wb.add_worksheet('Delta-Ausstattungskennziffern')
ws12.write(2, 1, "Ausstattungskennziffern".decode('utf-8'), bold)

################################################################################################################
ws13 = wb.add_worksheet('Erlaeuterungen zur Bewertung')
ws13.set_column(1, 1, 120)
ws13.write(2, 1, "Erläuterungen zur Bewertung der Teilergebnisse".decode('utf-8'), bold)
ws13.write(3,1,"• Umsatzveränderung für den Bestand:".decode('utf-8'),bold)
ws13.write(4,1,"Die Umsatzveränderung für den Bestand (auch Verdrängungsquote, Umsatzumverteilung, Kaufkraftabschöpfungsquote genannt) wird  ".decode('utf-8'))
ws13.write(5,1,"in Deutschland i. d. R. im Rahmen des B-Plan-Verfahrens nach § 11 Abs. 3 BauNVO oder bei einer Beurteilung nach § 34 Abs. 3 BauGB  ".decode('utf-8'))
ws13.write(6,1,"(unbeplanter Innenbereich) verwendet und sehr häufig kontrovers diskutiert. Auf Grundlage dieser Quote wird im Bebauungsplanverfahren ".decode('utf-8'))
ws13.write(7,1,"und/oder in entsprechenden Gutachten in der Regel abgeleitet, ob das neue Vorhaben zu städtebaulichen, raumordnerischen und/oder ".decode('utf-8'))
ws13.write(8,1,"schädlichen Auswirkungen führt. Unter negativen oder schädlichen Auswirkungen wird in der Regel eine starke ökonomische Schwächung  ".decode('utf-8'))
ws13.write(9,1,"(Umsatzverlust) bestehender Versorgungstandorte (vor allem in Zentren) verstanden, in deren Folge städtebauliche Missstände, ".decode('utf-8'))
ws13.write(10,1,"d. h. bedeutende (großflächige) Leerstände zu erwarten sind, die die Vitalität bestehender Zentren und die wohnortnahe  ".decode('utf-8'))
ws13.write(11,1,"Grundversorgung (mit Lebensmitteln) gefährden. In diesem Zusammenhang wird immer wieder diskutiert, ab wie viel Prozent ".decode('utf-8'))
ws13.write(12,1," Umsatzverdrängung von städtebaulich negativen und/oder schädlichen Auswirkungen auszugehen ist. In der Rechtsprechung   ".decode('utf-8'))
ws13.write(13,1," hat sich durchgesetzt, dass es keinen pauschalen Wert gibt, ab dem von städtebaulichen und/oder schädlichen städtebaulichen  ".decode('utf-8'))
ws13.write(14,1,"Auswirkungen auszugehen ist. Vielmehr ist auf die jeweilige spezifische Situation abzustellen (u. a. BVerwG, Urteil vom   ".decode('utf-8'))
ws13.write(15,1,"17. Dez. 2009 – 4 C 1.08). Die Gerichte machen hier deutlich, dass die konkrete Ausgangslage von besonderer Relevanz ist. Das ".decode('utf-8'))
ws13.write(16,1,"heißt, bei der Bewertung sollte unter anderem der Abstand zwischen geplantem Betrieb und dem Zentrum Berücksichtigung finden, zudem ".decode('utf-8'))
ws13.write(17,1,"sollte beachtet werden, ob das Zentrum bereits durch sichtbare „trading down“-Tendenzen gekennzeichnet ist oder ob ggf. ein  ".decode('utf-8'))
ws13.write(18,1,"strukturprägender Ankerbetrieb durch das neue Planvorhaben besonders betroffen ist und dadurch die Funktionsfähigkeit des ".decode('utf-8'))
ws13.write(19,1,"Zentrums besonders in Frage gestellt werden muss (BVerwG, Urteil vom 11. Okt.2007, 4 C 7.07). In der Praxis hat sich ".decode('utf-8'))
ws13.write(20,1,"(allen Beteuerungen zum Trotz)  jedoch als „magische“ Grenze die 10 %-Schwelle Umsatzverdrängung durchgesetzt (so wenig empirisch  ".decode('utf-8'))
ws13.write(21,1,"belastbar diese Grenze auch sein mag), ab der mögliche Umsatzumverteilungen sehr detailliert in die Abwägung im Laufe  ".decode('utf-8'))
ws13.write(22,1,"des Bauleitplanverfahrens einbezogen werden sollten. Die Untergrenze, ab der von einer Relevanz dieser Verdrängung auszugehen ist, ".decode('utf-8'))
ws13.write(23,1,"wird in der Rechtsprechung bzw. den Kommentierungen dazu niedriger angesetzt. Fickert/Fieseler (2008: 842) nennen einen Wert ".decode('utf-8'))
ws13.write(24,1,"ab rd. 5 %. Städtebauliche Auswirkungen gewichtiger Art sind demnach erst bei einem Schwellenwert von 15 bis 20 % Umsatzverlust ".decode('utf-8'))
ws13.write(25,1,"des innenstadtrelevanten Einzelhandels anzunehmen nach (Fickert/Fieseler 2008: 844). Vielfach wird bei Werten ab ".decode('utf-8'))
ws13.write(26,1,"20 % Verdrängung von einer Abwägungsresistenz gesprochen, d. h. ab 20 % Umsatzverdrängung ist auf jeden Fall von städtebaulich ".decode('utf-8'))
ws13.write(27,1,"negativen/schädlichen Auswirkungen auszugehen (vgl. Vogels/Holl/Birk (1998); Kuschnerus (2007). In der Rechtsprechung ".decode('utf-8'))
ws13.write(28,1,"werden allerdings teilweise auch deutlich höhere Werte genannt (Fickert/Fieseler (2008: 844).".decode('utf-8'))
ws13.write(29,1,"".decode('utf-8'))
ws13.write(30,1,"• Verkaufsflächendichte:".decode('utf-8'),bold)
ws13.write(31,1,"Die Verkaufsflächendichte (qm Verkaufsfläche/Einwohner) ist ein auf Gemeindeebene darstellbarer, verhältnismäßig einfach zu  ".decode('utf-8'))
ws13.write(32,1,"errechnender Wert, der gut dazu verwendet werden kann, die Versorgungssituation im Lebensmittelbereich abzubilden und ".decode('utf-8'))
ws13.write(33,1,"die Ausstattungskennziffern der einzelnen Kommunen miteinander zu vergleichen. In der Regel korreliert dieser Wert mit ".decode('utf-8'))
ws13.write(34,1,"der Einzelhandelszentralität. ".decode('utf-8'))
ws13.write(35,1,"".decode('utf-8'))
ws13.write(36,1,"• Einzelhandelszentralität:".decode('utf-8'),bold)
ws13.write(37,1,"Die Einzelhandelszentralität stellt das Verhältnis von erwirtschaftetem Umsatz (brutto) in einer Branche (hier: periodischer ".decode('utf-8'))
ws13.write(38,1,"Bedarfsbereich durch Lebensmittelmärkte) zu vorhandener Kaufkraft in einem Betrachtungsraum (hier: Kommune bzw. Betrachtungsregion) ".decode('utf-8'))
ws13.write(39,1,"dar. Grundlage für die Berechnungen zu den Jahresumsätzen im Bereich Lebensmittel sind die angenommenen maximalen ".decode('utf-8'))
ws13.write(40,1,"Kaufkraftbindungsquoten auf der einen Seite und die Einwohnerzahlen, deren Kaufkraftniveau und Verbrauchsausgaben im periodischen ".decode('utf-8'))
ws13.write(41,1,"Bedarfsbereich auf der anderen Seite. Bei Werten über 100 % weist der Betrachtungsraum (hier: Kommune/Betrachtungsregion) ".decode('utf-8'))
ws13.write(42,1,"saldierte Kaufkraftzuflüsse auf, bei Werten unterhalb von 100 % sind in der Kommune/Betrachtungsregion saldierte Kaufkraftabflüsse ".decode('utf-8'))
ws13.write(43,1,"festzustellen. Das bedeutet, dass bei einem Wert von 100 % in einer Kommune/Betrachtungsregion (rein rechnerisch) eine ausreichende".decode('utf-8'))
ws13.write(44,1,"Versorgung gewährleistet ist, d. h. sich die eigene Bevölkerung innerhalb der jeweiligen Grenzen ausreichend mit den Gütern aus der".decode('utf-8'))
ws13.write(45,1,"jeweiligen Branche versorgen kann. In der Regel weisen größere Kommunen Zentralitäten von über 100 % auf. Sie versorgen also die ".decode('utf-8'))
ws13.write(46,1,"Bevölkerung in kleineren Kommunen (zumindest in Teilen) mit. Kleinere Kommunen haben entsprechend meist Werte unter 100 %. Zu ".decode('utf-8'))
ws13.write(47,1,"beachten ist bei dieser Kennziffer, dass es sich um einen relativen Wert handelt, d. h. bei gleicher Kennziffer (z. B. 107 %) ist ".decode('utf-8'))
ws13.write(48,1,"der absolute Kaufkraftzufluss umso höher, je größer die Stadt bzw. die Einwohnerzahl/absolute Kaufkraft vor Ort ist.".decode('utf-8'))
ws13.write(49,1,"".decode('utf-8'))
ws13.write(50,1,"Literatur".decode('utf-8'),bold)
ws13.write(51,1,"Fickert, H. C./Fieseler, H. (2008): Baunutzungsverordnung – Kommentar unter besonderer Berücksichtigung des deutschen und ".decode('utf-8'))
ws13.write(52,1,"gemeinschaftlichen Umweltschutzes mit ergänzenden Rechts-  und Verwaltungsvorschriften. S. 842-844.".decode('utf-8'))
ws13.write(53,1,"".decode('utf-8'))
ws13.write(54,1,"Kuschnerus, U. (2007): Der standortgerechte Einzelhandel. S. 168-171.".decode('utf-8'))
ws13.write(55,1,"".decode('utf-8'))
ws13.write(56,1,"Vogels, K.-H./Holl, S./Birk, H.-J. (1998): Auswirkungen großflächiger Einzelhandelsbetriebe.".decode('utf-8'))
ws13.write(57,1,"".decode('utf-8'))
ws13.write(58,1,"Rechtsprechungen".decode('utf-8'),bold)
ws13.write(59,1,"BVerwG, Urteil vom 11. Okt.2007, 4 C 7.07".decode('utf-8'))
ws13.write(60,1,"BVerwG, Urteil vom 17. Dez. 2009 – 4 C 1.08".decode('utf-8'))

#Workbook speichern
wb.close()

##try:
##	wb.close()
##except IOError:
##	schrittmeldung = 'ACHTUNG \nDie Ergebnisstabelle konnte nicht gespreichert werden, da eine ältere Version der Datei momentan in Excel geöffnet ist. Bitte schließen Sie diese Tabelle und führen Sie den Arbeitsschritt erneut aus. \n'
##	arcpy.AddMessage(schrittmeldung)
##	print schrittmeldung

# Endmeldung
print 'Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert \n'
arcpy.AddMessage('Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert')