# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Änderung der Art der Nutzung
# Purpose:
#
# Author:      Basti
#
# Created:     20.10.2013
# Copyright:   (c) Basti 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#ToDO
# ArcGis erstellt unicode fehelr



import arcpy ,sys,os,gc
import xlsxwriter
gc.collect()


##################################################################################################################
#Flächennutzung
#Zuordnungs datein unklar - nur Prozent angabe vorhanden >100 % ....
def LeseDaten_Vornutzung(workspace_projekt_definition_projekt):

    arcpy.AddMessage('Lese Angaben ueber Vornutzung')
    Cur_Teilflaechen=arcpy.SearchCursor(workspace_projekt_definition_projekt+"/Teilflaechen_Plangebiet")
    Cur_Vornutzung_Details=arcpy.SearchCursor(workspace_projekt_definition_projekt+"/Vornutzungen_Details_Prozent")
    Daten_Vor=[]
    Flaechen=[]
    gesamtFlaeche=0.0

    array_Cur_Vornutzung_Details=[]
    for werte in Cur_Vornutzung_Details:
        array_Cur_Vornutzung_Details.append([werte.Vornutzungstyp,werte.Prozent_der_Flaeche,werte.Teilflaeche_Plangebiet])

    for werte in Cur_Teilflaechen:
        Flaechen.append([werte.Name,werte.Flaeche_ha])
        gesamtFlaeche+=werte.Flaeche_ha

    #Flaehcneberechnung
    for cc in array_Cur_Vornutzung_Details:
        for bb in Flaechen:
##            print "a ",cc[2]
##            print "b ",bb[0]
            if cc[2]==bb[0]:
                cc[1]= bb[1]*cc[1]/100



   # print array_Cur_Vornutzung_Details

    Daten_Vor.append([array_Cur_Vornutzung_Details[0][0],array_Cur_Vornutzung_Details[0][1],0,array_Cur_Vornutzung_Details[0][2]])
    for a in array_Cur_Vornutzung_Details[1:]:
        gefunden=0
        for b in Daten_Vor:
            if a[0] == b[0]:
               b[1]+=a[1]
               gefunden=1
        if gefunden==0:
            #Neuer Typus
            Daten_Vor.append([a[0],a[1],0,a[2]])


    for wert in Daten_Vor:
        wert[2]= wert[1]*100/gesamtFlaeche



##    zasd=0.
##    for jjjj in Daten_Vor:
##        zasd+=jjjj[2]
##    print zasd
    #Check ob Fläche komplett ist -> ok!
##    asdf=0.0
##    for v in Daten_Vor :
##        asdf+=v[1]
##    print gesamtFlaeche - asdf
    del Cur_Teilflaechen,Cur_Vornutzung_Details,array_Cur_Vornutzung_Details,gesamtFlaeche
    return Daten_Vor

##################################################################################################################
#Flächennutzung
def LeseDaten(workspace_projekt_definition_projekt):

    arcpy.AddMessage("Lese Angaben ueber geplante Flächennutzung")
    Cur_Flaechenbilanz_Planung_Prozent=arcpy.SearchCursor(workspace_projekt_definition_projekt+"/Flaechenbilanz_Planung_Prozent")
    Daten=[]
    gesamtFlaeche=0.0

    #flaechnungzung s2
    array_Cur_Flaechenbilanz_Planung_Prozent=[]
    for werte in Cur_Flaechenbilanz_Planung_Prozent:
        array_Cur_Flaechenbilanz_Planung_Prozent.append([werte.Flaechennutzung_S2,werte.Flaeche_ha])
        gesamtFlaeche+=werte.Flaeche_ha

    Daten.append([array_Cur_Flaechenbilanz_Planung_Prozent[0][0],array_Cur_Flaechenbilanz_Planung_Prozent[0][1],0])
    for a in array_Cur_Flaechenbilanz_Planung_Prozent[1:]:
        gefunden=0
        for b in Daten:
            if a[0] == b[0]:
               b[1]+=a[1]
               gefunden=1
        if gefunden==0:
            #Neuer Typus
            Daten.append([a[0],a[1],0])


    for wert in Daten:
        wert[2]= wert[1]*100/gesamtFlaeche
##    print Daten
    #Check ob Fläche komplett ist -> ok!
##    asdf=0.0
##    for v in Daten :
##        asdf+=v[1]
##    print gesamtFlaeche - asdf
    del Cur_Flaechenbilanz_Planung_Prozent,array_Cur_Flaechenbilanz_Planung_Prozent,gesamtFlaeche
    return Daten


def ErstelleXls(Daten,Daten_Vor,workspace_projekt_ergebnis):

    arcpy.AddMessage("Erstelle Diagramme")

    excelpfad = os.path.join(workspace_projekt_ergebnis,'32_Wertveraenderung.xlsx')

    try:
        os.remove(excelpfad)
    except:
        pass

    # Workbook und Tabellenblätter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    ws1 = wb.add_worksheet('Info')
    ws2 = wb.add_worksheet('Rohdaten')
    ws3 = wb.add_worksheet('Auswertungen')
    ws4 = wb.add_worksheet('Grafiken')


    bold = wb.add_format({'bold': 1})

    # Add the ws4 data that the charts will refer to.
    headings1 = ['Laermintensives Gewerbe','','','Laermschutzanlagen',
                'Normales Gewerbe','Erschliessungsflaeche','Wenig stoerendes Gewerbe',
                'Gemeinbedarfsflaeche','Gewerbeflaeche (Versorgung)','Nettobauland','','Strassenbegleitgruen'
                ,'Spielplaetze','Gruenflaeche']
    headings2 = ['Laermintensives Gewerbe','Abbauflaeche','Landwirtschaftlicher Betrieb','Brachflaeche',
                'Normales Gewerbe','Erschliessungsflaeche','Wenig stoerendes Gewerbe',
                'Soziale Infrastruktur','Einzelhandel','Wohnen','Ackerflaeche','Wald'
                ,'Wiese','Oeffentliche Gruenflaeche']


##    headingss1 = ['Lärmintensives Gewerbe'.decode('utf-8'),'','','Lärmschutzanlagen'.decode('utf-8'),
##            'Normales Gewerbe','Erschließungsflächen'.decode('utf-8'),'Wenig störendes Gewerbe'.decode('utf-8'),
##            'Gemeinbedarfsfläche'.decode('utf-8'),'Gewerbefläche (Versorgung)'.decode('utf-8'),'Nettowohnbauland','','Strassenbegleitgrün'.decode('utf-8')
##            ,'Spielplätze'.decode('utf-8'),'Allgemeine Grünflächen'.decode('utf-8')]
##
##
##    headingss2 = ['Lärmintensives Gewerbe'.decode('utf-8'),'Abbaufläche'.decode('utf-8'),'Landwirtschaftlicher Betrieb','Brachfläche'.decode('utf-8'),
##            'Normales Gewerbe','Erschliessungsfläche'.decode('utf-8'),'Wenig störendes Gewerbe'.decode('utf-8'),
##            'Soziale Infrastruktur','Einzelhandel','Wohnen','Ackerfläche'.decode('utf-8'),'Wald'
##            ,'Wiese','Öffentliche Grünfläche'.decode('utf-8')]

    data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    data2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]


    wozusetzen=[]
    for row_Daten in Daten:
        gesetzt=0
        for zahl, row_Headings in enumerate( headings1):
##            print "a " ,row_Daten[0]
##            print "b " ,row_Headings
            if (row_Daten[0]==row_Headings):
                wozusetzen.append([zahl, row_Daten[2]])
                break

    for uu in wozusetzen:
        data[uu[0]]= round(uu[1])

##    print data

##    print Daten_Vor
    wozusetzen2=[]
    for row_Daten_Vor in Daten_Vor:
        gesetzt=0
        for zahl, row_Headings2 in enumerate( headings2):
##            print "a " ,row_Daten_Vor[0]
##            print "b " ,row_Headings2
            if (row_Daten_Vor[0]==row_Headings2):
                wozusetzen2.append([zahl, row_Daten_Vor[2]])
##                print "doppel abbruch"
                break

    for uu in wozusetzen2:
        data2[uu[0]]=round(uu[1])

##    print data2

    ws2.write_column('A1', headings2,bold)
    ws2.write_column('B1', data2)
    ws2.write_column('C1', headings1,bold)
    ws2.write_column('D1', data)

##    ws4.write_column('C1', data[1])
#    #######################################################################
#   Chart1 Planung Chart2 Vornutzung
   # Create a new Chart object.
    chart1 = wb.add_chart({'type': 'column', 'subtype': 'stacked'})


    # Configure the first series.
    if data[0]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$1',
            'categories': '=Rohdaten!$E$1',
            'values':     '=Rohdaten!$D$1',
            'fill': {'color': '#f50018'},

            })
    if data[1]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$2',
            'categories': '=Rohdaten!$E$2',
            'values':     '=Rohdaten!$D$2',
            'fill': {'color': '#f50018'},

            })

    if data[2]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$3',
            'categories': '=Rohdaten!$E$3',
            'values':     '=Rohdaten!$D$3',
            'fill': {'color': '#f50018'},

        })

    if data[3]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$4',
            'categories': '=Rohdaten!$E$4',
            'values':     '=Rohdaten!$D$4',
            'fill': {'color': '#e05500'},

        })
    if data[4]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$5',
            'categories': '=Rohdaten!$E$5',
            'values':     '=Rohdaten!$D$5',
            'fill': {'color': '#ccad00'},

        })
    if data[5]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$6',
            'categories': '=Rohdaten!$E$6',
            'values':     '=Rohdaten!$D$6',
            'fill': {'color': '#ccad00'},

        })
    if data[6]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$7',
            'categories': '=Rohdaten!$E$7',
            'values':     '=Rohdaten!$D$7',
            'fill': {'color': '#7cb700'},

        })
    if data[7]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$8',
            'categories': '=Rohdaten!$E$8',
            'values':     '=Rohdaten!$D$8',
            'fill': {'color': '#7cb700'},
        })
    if data[8]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$9',
            'categories': '=Rohdaten!$E$9',
            'values':     '=Rohdaten!$D$9',
            'fill': {'color': '#7cb700'},

        })
    if data[9]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$10',
            'categories': '=Rohdaten!$E$10',
            'values':     '=Rohdaten!$D$10',
            'fill': {'color': '#20a300'},

        })
    if data[10]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$11',
            'categories': '=Rohdaten!$E$11',
            'values':     '=Rohdaten!$D$11',
            'fill': {'color': '#20a300'},

        })
    if data[11]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$12',
            'categories': '=Rohdaten!$E$12',
            'values':     '=Rohdaten!$D$12',
            'fill': {'color': '#008e27'},

        })
    if data[12]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$13',
            'categories': '=Rohdaten!$E$13',
            'values':     '=Rohdaten!$D$13',
            'fill': {'color': '#008e27'},
        })

    if data[13]>0:
        chart1.add_series({
            'name':       '=Rohdaten!$C$14',
            'categories': '=Rohdaten!$E$14',
            'values':     '=Rohdaten!$D$14',
            'fill': {'color': '#008e27'},
        })

#    #######################################################################
##
   # Create a new Chart object.
    chart2 = wb.add_chart({'type': 'column', 'subtype': 'stacked'})


    # Configure the first series.
    if data2[0]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$1',
            'categories': '=Rohdaten!$E$1',
            'values':     '=Rohdaten!$B$1',
            'fill': {'color': '#f50018'},

            })
    if data2[1]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$2',
            'categories': '=Rohdaten!$E$2',
            'values':     '=Rohdaten!$B$2',
            'fill': {'color': '#f50018'},

            })

    if data2[2]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$3',
            'categories': '=Rohdaten!$E$3',
            'values':     '=Rohdaten!$B$3',
            'fill': {'color': '#f50018'},

        })

    if data2[3]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$4',
            'categories': '=Rohdaten!$E$4',
            'values':     '=Rohdaten!$B$4',
            'fill': {'color': '#e05500'},

        })
    if data2[4]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$5',
            'categories': '=Rohdaten!$E$5',
            'values':     '=Rohdaten!$B$5',
            'fill': {'color': '#ccad00'},

        })
    if data2[5]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$6',
            'categories': '=Rohdaten!$E$6',
            'values':     '=Rohdaten!$B$6',
            'fill': {'color': '#ccad00'},

        })
    if data2[6]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$7',
            'categories': '=Rohdaten!$E$7',
            'values':     '=Rohdaten!$B$7',
            'fill': {'color': '#7cb700'},

        })
    if data2[7]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$8',
            'categories': '=Rohdaten!$E$8',
            'values':     '=Rohdaten!$B$8',
            'fill': {'color': '#7cb700'},
        })
    if data2[8]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$9',
            'categories': '=Rohdaten!$E$9',
            'values':     '=Rohdaten!$B$9',
            'fill': {'color': '#7cb700'},

        })
    if data2[9]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$10',
            'categories': '=Rohdaten!$E$10',
            'values':     '=Rohdaten!$B$10',
            'fill': {'color': '#20a300'},

        })
    if data2[10]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$11',
            'categories': '=Rohdaten!$E$11',
            'values':     '=Rohdaten!$B$11',
            'fill': {'color': '#20a300'},

        })
    if data2[11]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$12',
            'categories': '=Rohdaten!$E$12',
            'values':     '=Rohdaten!$B$12',
            'fill': {'color': '#008e27'},

        })
    if data2[12]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$13',
            'categories': '=Rohdaten!$E$13',
            'values':     '=Rohdaten!$B$13',
            'fill': {'color': '#008e27'},
        })

    if data2[13]>0:
        chart2.add_series({
            'name':       '=Rohdaten!$A$14',
            'categories': '=Rohdaten!$E$14',
            'values':     '=Rohdaten!$B$14',
            'fill': {'color': '#008e27'},
        })

    # Add a chart title and some axis labels.
    chart2.set_title ({'name': 'Prozentualer Anteil der verschiedenen Flaechennutzungen (Bestand), sortiert nach ihrer Wertigkeit fuer die umliegenden Wohngebiete'.decode('utf-8')})
    chart1.set_title ({'name': 'Prozentualer Anteil der verschiedenen Flaechennutzungen (neu), sortiert nach ihrer Wertigkeit fuer die umliegenden Wohngebiete'.decode('utf-8')})

    # Set an Excel chart style.
    chart1.set_style(10)
    chart1.set_size({'width': 500, 'height': 400})
    chart1.set_y_axis({'min': 0, 'max': 101})
    # Set an Excel chart style.
    chart2.set_style(10)
    chart2.set_size({'width': 500, 'height': 400})
    chart2.set_y_axis({'min': 0, 'max': 101})
    # Insert the chart into the ws4 (with an offset).
##    ws4.insert_chart('A30', chart1, {'x_offset': 25, 'y_offset': 10})
##   # ws4.insert_chart('H30', chart2, {'x_offset': 25, 'y_offset': 10})
    ws4.insert_chart('A1', chart2)
    ws4.insert_chart('I1', chart1)


    ################################
    #Beschreibungsblatt einfuegen
    now = datetime.datetime.now()

    Beschreibungstext = """Wertveraenderung Wohnen. Sie finden die Werte im naechsten Tabellenblatt"""

    ws1.write(6, 1, 'REGIOPROJEKTCHECK', bold)
    ws1.write(7, 1, 'Folgeabschaetzung von Bauprojekten')

    ws1.write(9, 1, 'Untersuchtes Projekt:', bold)
    ws1.write(9, 2, projektname)
    ws1.write(10, 1, 'Wirkungsfeld:', bold)
    ws1.write(10, 2, 'Wertveraenderung Wohnen'.decode('utf-8'))
    ws1.write(11, 1, 'Exportdatum:', bold)
    ws1.write(11, 2, now.strftime("%Y-%m-%d %H:%M"))

    ws1.write(13, 1, 'Inhalt:', bold)
    ws1.write(13, 2, Beschreibungstext)



    wb.close()

    arcpy.AddMessage("Erfolgreich erstellt.")
    arcpy.AddMessage("Diagramm in \Ergebnisausgabe\Excel\32_Wertveraenderung.xls zu finden.")


#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)
##projektname="LKH_Bultweg"

workspace_projekt_ergebnis = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
workspace_projekt_definition_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_34_Wertveraenderungen_'+projektname+'.gdb')

Daten_Vor=LeseDaten_Vornutzung(workspace_projekt_definition_projekt)
Daten=LeseDaten(workspace_projekt_definition_projekt)
ErstelleXls(Daten,Daten_Vor,workspace_projekt_ergebnis)


##sys.argv = [projektname]
##execfile(str(sys.path[0])+'\Visualisierung_Laerm.py')


gc.collect()

del workspace_projekt_ergebnis,workspace_projekt_definition_projekt,workspace_projekt_wertveraenderung,Daten,Daten_Vor