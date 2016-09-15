# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Erreichbarkeit_OEPNV.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import os
import sys
import math
import urllib
import re
import gc
import csv
import time
import operator

import arcpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import  FuncFormatter
import numpy as np


#---------------------------------------------------------------------------------------
# Unicode kram
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)



#--------------------------------------------------------------------------------------------------
# Abfahrt
class Verkehrsmittel:
    def __init__(self):
       self.verkehrsmittel=[]
       self.ziel =[]
       self.uhrzeit = []

def escape1(html):
    rueck=[]
    for usd in html:
        usd=usd.decode('ISO-8859-1')
        usd=usd.replace('\n','')
        usd= decode_unicode_references(usd)
        usd= usd.encode('utf-8')
        rueck.append(usd)

    return rueck
#----------------------------------------------------------------------------------------------------------------------------------------------
# Abfahrtfunktion für Barcode
def Abfahrt(base_path,projektname,Daten):

    workspace_projekt_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit_Projekt_'+projektname+'.gdb')

    fahrzeug_array_alle_Haltestellen=[]
    for z in Daten:

        str1='&gt;&gt;'
        str2='<span class="bold">'

        max="99999"
        evaID=str(z[0])
##        print z[0]
        f = urllib.urlopen("http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId="+evaID+"&bt=dep&max="+max+"&p=1111111111&start=1&time=00.00&time_end=23.59")
##        print("http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId="+evaID+"&bt=dep&max="+max+"&p=1111111111&start=1&time=00.00&time_end=23.59")
        uhrzeit_falsch=[]
        uhrzeit=[]
        verkehrsmittel=[]
        ziel=[]
        bla=[]

        uu=0
        for zeilen in f:
            if uu==1:
                ziel.append(zeilen)
                uu=0

            if zeilen.find(str1)==0:
                uu=1

            if zeilen.find(str2)==0:
                bla.append(zeilen)
                m = re.findall(r">[0-9][0-9]:[0-9][0-9]<",zeilen)
                if len(m)>0:
                    uhrzeit_falsch.append(m)
                    bla.remove(zeilen)
        f.close()

        for n in uhrzeit_falsch:
            uhrzeit.append(repr(n).replace('>',"").replace('<',""))

        for h in bla:
            test=h.replace('<span class="bold">',"").replace('</span>',"").replace('\n',"")
            if len(test)>2:
                verkehrsmittel.append(test)

        ziel = escape1(ziel)

        gefunden=0
        i=0
        fahrzeug_array= []
        fahrzeug = Verkehrsmittel()
        while(i<len(verkehrsmittel)):
            if (i==0):
                fahrzeug.verkehrsmittel.append(str(verkehrsmittel[0]))
                #decode es als utf-8 und excel geht wieder
                fahrzeug.ziel.append(str(ziel[0]).decode('String_Escape'))
                fahrzeug.uhrzeit.append(uhrzeit[0])
                fahrzeug_array.append(fahrzeug)
                gefunden=1

            else:
                for h in fahrzeug_array:

                    if(verkehrsmittel[i]==str(h.verkehrsmittel).replace("'","").replace("[","").replace("]","")) and (str(ziel[i]).decode('utf-8')==''.join(h.ziel)):
                        h.uhrzeit.append(uhrzeit[i])
                        gefunden=1

                if(gefunden==0):
                    fahrzeug = Verkehrsmittel()
                    fahrzeug.verkehrsmittel.append(verkehrsmittel[i])
                    fahrzeug.ziel.append(str(ziel[i]).decode('String_Escape'))
                    fahrzeug.uhrzeit.append(uhrzeit[i])
                    fahrzeug_array.append(fahrzeug)

            i=i+1
            gefunden=0

        del uhrzeit , uhrzeit_falsch,bla,ziel, i

        fahrzeug_array_alle_Haltestellen.append(fahrzeug_array)

    return fahrzeug_array_alle_Haltestellen
#----------------------------------------------------------------------------------------------------------------------------------------------
# Alte Abfahrt funktion
def Abfahrt2(base_path,projektname,Daten):

    workspace_projekt_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit_Projekt_'+projektname+'.gdb')
    workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
    myfile = open(workspace_projekt_ergebnisse+"/Informationen_Abfahrt.csv", "wb")
    writer = csv.writer(myfile,dialect='excel',delimiter=' ')
    trenn=[';']


    for z in Daten:

        str1='&gt;&gt;'
        str2='<span class="bold">'

        max="99999"
        evaID=str(z[0])
        writer.writerow((repr(z[2]).decode('String_Escape').replace("'",'').replace('u','',1) , str(z[0]).replace('"','')))

        f = urllib.urlopen("http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId="+evaID+"&bt=dep&max="+max+"&start=1&time=00.00&time_end=23.59&disableEquivs=yes")
##        print("http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId="+evaID+"&bt=dep&max="+max+"&start=1&time=00.00&time_end=23.59&disableEquivs=yes")
        uhrzeit_falsch=[]
        uhrzeit=[]
        verkehrsmittel=[]
        ziel=[]
        bla=[]

        uu=0
        for zeilen in f:
            if uu==1:
                ziel.append(zeilen)
                uu=0

            if zeilen.find(str1)==0:
                uu=1

            if zeilen.find(str2)==0:
                bla.append(zeilen)
                m = re.findall(r">[0-9][0-9]:[0-9][0-9]<",zeilen)
                if len(m)>0:
                    uhrzeit_falsch.append(m)
                    bla.remove(zeilen)
        f.close()

        for n in uhrzeit_falsch:
            uhrzeit.append(repr(n).replace('>',"").replace('<',""))

        for h in bla:
            test=h.replace('<span class="bold">',"").replace('</span>',"").replace('\n',"")
            if len(test)>2:
                verkehrsmittel.append(test)

        ziel = escape1(ziel)

        gefunden=0
        i=0
        fahrzeug_array= []
        fahrzeug = Verkehrsmittel()
        while(i<len(verkehrsmittel)):
            if (i==0):
                fahrzeug.verkehrsmittel.append(str(verkehrsmittel[0]))
                fahrzeug.ziel.append(str(ziel[0]).decode('utf-8'))

                fahrzeug.uhrzeit.append(uhrzeit[0])
                fahrzeug_array.append(fahrzeug)
                gefunden=1

            else:
                for h in fahrzeug_array:
                    if(verkehrsmittel[i]==str(h.verkehrsmittel).replace("'","").replace("[","").replace("]","")) and (str(ziel[i]).decode('utf-8')==''.join(h.ziel)):
                        h.uhrzeit.append(uhrzeit[i])
                        gefunden=1

                if(gefunden==0):
                    fahrzeug = Verkehrsmittel()
                    fahrzeug.verkehrsmittel.append(verkehrsmittel[i])
                    fahrzeug.ziel.append(str(ziel[i]).decode('utf-8'))
                    fahrzeug.uhrzeit.append(uhrzeit[i])
                    fahrzeug_array.append(fahrzeug)

            i=i+1
            gefunden=0

        for a in fahrzeug_array:
            ptime=""
            for b in a.uhrzeit:
                ptime+=str(b).replace('[','').replace(']','').replace("'",'').replace('"','')+str(trenn).replace('[','').replace(']','').replace("'",'')

            blib= list(str(a.ziel).decode('String_Escape').replace('[','').replace(']','').replace("'",'').replace('"','').replace("u",'',1))
            bla2 = a.verkehrsmittel + trenn
            bla2 = bla2 + blib
            bla2 = bla2 + trenn +list(ptime)

            writer.writerow(bla2)
            del ptime

        del uhrzeit , uhrzeit_falsch,verkehrsmittel,bla,ziel,fahrzeug_array,  i ,fahrzeug.uhrzeit,fahrzeug.verkehrsmittel,fahrzeug.ziel
        writer.writerow('')

    myfile.close()
    del writer,myfile
#--------------------------------------------------------------------------------------------------
# Ankunft
def Ankunft(base_path,projektname,Daten):

    workspace_projekt_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit_Projekt_'+projektname+'.gdb')

    myfile = open(workspace_projekt_ergebnisse+"/Informationen_Ankunft.csv", "wb")
    writer = csv.writer(myfile,dialect='excel',delimiter=' ')
    trenn=[';']


    for z in Daten:

        str1='&lt;&lt;'
        str2='<span class="bold">'

        max="99999"
        evaID=str(z[0])
        writer.writerow((repr(z[2]).decode('String_Escape').replace("'",'').replace('u','',1) , str(z[0]).replace('"','')))

        f = urllib.urlopen("http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId="+evaID+"&bt=arr&max="+max+"&start=1&time=00.00&time_end=23.59&disableEquivs=yes")
        uhrzeit_falsch=[]
        uhrzeit=[]
        verkehrsmittel=[]
        ziel=[]
        bla=[]

        uu=0
        for zeilen in f:
            if uu==1:
                ziel.append(zeilen)
                uu=0

            if zeilen.find(str1)==0:
                uu=1

            if zeilen.find(str2)==0:
                bla.append(zeilen)
                m = re.findall(r">[0-9][0-9]:[0-9][0-9]<",zeilen)
                if len(m)>0:
                    uhrzeit_falsch.append(m)
                    bla.remove(zeilen)

        f.close()

        for n in uhrzeit_falsch:
            uhrzeit.append(repr(n).replace('>',"").replace('<',""))

        for h in bla:
            test=h.replace('<span class="bold">',"").replace('</span>',"").replace('\n',"")
            if len(test)>2:
                verkehrsmittel.append(test)

        ziel = escape1(ziel)
        gefunden=0
        i=0
        fahrzeug_array= []
        fahrzeug = Verkehrsmittel()

        # Struktur Verkehrsmittel Ziel Uhrzeit Uhrzeit UhrzeitUhrzeitUhrzeit Uhrzeit

        while(i<len(verkehrsmittel)):
            if (i==0):
                fahrzeug.verkehrsmittel.append(str(verkehrsmittel[0]))
                fahrzeug.ziel.append(str(ziel[0]).decode('utf-8'))
##                fahrzeug.ziel.append(ziel[0])
                fahrzeug.uhrzeit.append(uhrzeit[0])
                fahrzeug_array.append(fahrzeug)
                gefunden=1
##                print str(fahrzeug.ziel).decode('String_Escape')

            else:
                for h in fahrzeug_array:

                    if(verkehrsmittel[i]==str(h.verkehrsmittel).replace("'","").replace("[","").replace("]","")) and (str(ziel[i]).decode('utf-8')==''.join(h.ziel)):
                        h.uhrzeit.append(uhrzeit[i])
                        gefunden=1

                if(gefunden==0):
                    fahrzeug = Verkehrsmittel()
                    fahrzeug.verkehrsmittel.append(verkehrsmittel[i])
                    fahrzeug.ziel.append(str(ziel[i]).decode('utf-8'))
                    fahrzeug.uhrzeit.append(uhrzeit[i])
                    fahrzeug_array.append(fahrzeug)
            i=i+1
            gefunden=0

        for a in fahrzeug_array:
            ptime=""
            for b in a.uhrzeit:
                ptime+=str(b).replace('[','').replace(']','').replace("'",'').replace('"','')+str(trenn).replace('[','').replace(']','').replace("'",'')

            blib= list(str(a.ziel).decode('String_Escape').replace('[','').replace(']','').replace("'",'').replace('"','').replace("u",'',1))
            bla2 = a.verkehrsmittel + trenn
            bla2 = bla2 + blib
            bla2 = bla2 + trenn +list(ptime)

            writer.writerow(bla2)
            del ptime

        del uhrzeit , uhrzeit_falsch,verkehrsmittel,bla,ziel,fahrzeug_array,  i ,fahrzeug.uhrzeit,fahrzeug.verkehrsmittel,fahrzeug.ziel
        writer.writerow('')


    myfile.close()
    del writer,myfile
#-----------------------------------------------------------------------------------------------------------------------------------------------
#Zeichne Barcode
def zeichne(timeline,lines,halte):

    workspace_projekt_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit_Projekt_'+projektname+'.gdb')
    workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
##    print halte
    halte= halte.replace("(",'').replace(")",'').replace(",",'').replace("/",'').replace(" ",'').replace(unichr(228),'ae').replace(unichr(246),'oe').replace(unichr(252),'ue').replace(unichr(223),'ss')
##    print halte
    fig=plt.figure()

##    print len (timeline)
    ax=fig.add_subplot(611,axisbg='w')

    p1=[]

    Farben=["#E41a1c", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", "#FFFF33", "#A65628", "#F781BF"] # Using color brewer color scheme: http://colorbrewer2.org/?type=qualitative&scheme=Set1&n=8
    for x, a in enumerate(timeline):

            Datenarray = a
            N = len(Datenarray)
            ind = np.arange(N)      # the x locations for the groups
            width = 1               # the width of the bars: can also be len(x) sequence
            p1.append(ax.bar(ind, Datenarray, width,linewidth=0 ,color=Farben[x],label=unicode(str(lines[x]).replace("'",'').replace('[','').replace(']','').decode('String_escape').decode('utf-8'))))

    handles, labels = ax.get_legend_handles_labels()

    fontP = FontProperties()
    fontP.set_size('small')
    ax.legend(handles[::-1], labels[::-1],loc='upper center', bbox_to_anchor=(0.5, -0.3), prop = fontP, fancybox=True, shadow=True, ncol=3)

    ax.get_yaxis().set_visible(False)
    ax.set_xlim(0,N)
    ax.set_xticks([0, 24, 48, 72,96,120,144,168,192,216,240,264,288])
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, pos: (str(int(x)*5/60)+':'+str(str(0))+str(0) ) ))

    fig.savefig(workspace_projekt_ergebnisse+"/"+halte+".png",pad_inches=1,dpi=464,facecolor='w', edgecolor='w', bbox_inches='tight')

    plt.clf()
    fig.clf()
    plt.close()
    del fig, ax , p1
    gc.collect()


#-----------------------------------------------------------------------------------------------------------------------------------------------
#Eerstellen der Barcodes bzw vorher entscheidung welches Diagramm erstellt werden soll
def erstellen_der_timelines(fahrzeug_array_b,Daten):

    Kategorie1_Verkehrsmittel=["ALT","AST","BSV","BUS","BYB","BZB","CAT","DZ","EXB"
                                ,"FAE","KAT","KD","KTB","LEO","LT","MBB","MEL","MSB"
                                ,"OBU","PRE","RFB","SB","SCH","SDG","SOE","UBU","UEF"
                                ,"WKD","ZRB"]
    Kategorie2_Verkehrsmittel=["HSB","RNV","STR","SWB"]
    Kategorie3_Verkehrsmittel=["ABR","ag","AKN","ALX","ANB","ARR","AVG","BLB","BOB","BRB"
                                ,"BSB","CAN","CB","DAB","DBG","DPN","DWE","EB","Ebx"
                                ,"EB/Ebx","ERB","erixx","EVB","HEX","HLB","HTB","HzL"
                                ,"IP","KM","ME","MEr","MR","MRB","N","NBE","NEB","NEG"
                                ,"NOB","NWB","OE","OLA","OS","OSB","PEG","R","R84","RAB"
                                ,"RB","RB/RE","RE","RER","REX","RSB","RT","RTB","S","S28"
                                ,"SBS","SHB","SKM","SKW","STB","T84","U","UBB","VBG","VEC"
                                ,"VIA","WFB"]
    Kategorie4_Verkehrsmittel=["AIR","ALS","ARC","ARN","ARZ","AS","ATB","ATR","AVE","AZ"
                                ,"CNL","D","DB","DNZ","DPF","E","EC","ECB","ECW","EE","EIC"
                                ,"EM","EN","ES","EST","EX","EZ","FB","FYR","HKX","HOT","IC"
                                ,"ICB","ICE","ICN","ICR","ICT","ICX","INT","INZ","IR","IRE","IRN"
                                ,"IRX","IXB","IXK","LYN","NEX","NZ","OEC","OIC","OZ","PCC","RHI"
                                ,"RHT","RJ","RR","RRI","RRT","S2","S84","SBB","SC","SP","TGD"
                                ,"TGV","THA","TLG","TLK","U70","UEX","UUU","VX","X","X2","X70","ZR"
                                ,"ZUG"]


    for welche, fahrzeug_array in enumerate( fahrzeug_array_b):
        #verkehrstraeger


        time5lines_verkehrstraeger=[]
        verkehr=[]
        nichtchecken=[]

        for x, a in enumerate( fahrzeug_array):
            if x not in  [ii for ii in nichtchecken] or x==0 :
                time5line=[]

                for uu in range(288):
                    time5line.append(0)
                wogefunden=[]


                mittel=str(a.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",'')

                if len([s for s in Kategorie1_Verkehrsmittel if s.lower() in str(mittel).lower()])>0  :
                    mittel="Bus"
                elif len([s for s in Kategorie2_Verkehrsmittel if s.lower() in str(mittel).lower()])>0 :
                    mittel="Strassen- bzw. Stadtbahn"
                elif len([s for s in Kategorie3_Verkehrsmittel if s.lower() in str(mittel).lower()])>0 :
                    mittel="U , S - Bahn"
                elif len([s for s in Kategorie4_Verkehrsmittel if s.lower() in str(mittel).lower()])>0 :
                    mittel="Fernbahn"

                gfind=0
                for y, b in enumerate( fahrzeug_array):
                    mittel2=str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",'')
                    if len([s for s in Kategorie1_Verkehrsmittel if s.lower() in str(mittel2).lower()])>0  :
                        mittel2="Bus"
                    elif len([s for s in Kategorie2_Verkehrsmittel if s.lower() in str(mittel2).lower()])>0 :
                        mittel2="Strassen- bzw. Stadtbahn"
                    elif len([s for s in Kategorie3_Verkehrsmittel if s.lower() in str(mittel2).lower()])>0 :
                        mittel2="U , S - Bahn"
                    elif len([s for s in Kategorie4_Verkehrsmittel if s.lower() in str(mittel2).lower()])>0 :
                        mittel2="Fernbahn"

                    if  mittel==mittel2 and x!=y:
                        drinn=0
                        for zz in verkehr:
                            if mittel ==zz:
                                drinn=1
                        if drinn ==0:
                            verkehr.append(mittel)
                        wogefunden.append(y)
                        nichtchecken.append(y)
                        gfind=1
                if gfind==0:
                 verkehr.append(mittel)
                ptime=""
                for woo in wogefunden:
                    for bk in fahrzeug_array[woo].uhrzeit:
                        ptime=str(bk).replace('[','').replace(']','').replace("'",'').replace('"','')
                        split = ptime.split(':')
                        time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1
                for bl in a.uhrzeit:
                        ptime=str(bl).replace('[','').replace(']','').replace("'",'').replace('"','')
                        split = ptime.split(':')
                        time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1

                time5lines_verkehrstraeger.append(time5line)

        time5lines_ziel=[]
        ziele=[]
        nichtchecken=[]

        for x, a in enumerate( fahrzeug_array):

            if x not in  [ii for ii in nichtchecken] or x==0 :
                time5line=[]

                for uu in range(288):
                    time5line.append(0)
                wogefunden=[]


                for y, b in enumerate( fahrzeug_array):
                    if a.ziel == b.ziel and x!=y:
                        wogefunden.append(y)
                        nichtchecken.append(y)

                ptime=""
                for woo in wogefunden:
                    for bk in fahrzeug_array[woo].uhrzeit:
                        ptime=str(bk).replace('[','').replace(']','').replace("'",'').replace('"','')
                        split = ptime.split(':')
                        time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1
                for bl in a.uhrzeit:

                        ptime=str(bl).replace('[','').replace(']','').replace("'",'').replace('"','')
                        split = ptime.split(':')
                        time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1
                ziele.append(str(a.ziel).replace('[','').replace(']','').replace("'",'').replace('"',''))
                time5lines_ziel.append(time5line)

        print "Ziel ", ziele

        #Linie

        time5lines_linie=[]
        lines=[]
        nichtchecken=[]
        for x, a in enumerate( fahrzeug_array):
            if x not in  [ii for ii in nichtchecken] or x==0 :
                time5line=[]

                for uu in range(288):
                    time5line.append(0)
                wogefunden=[]


                mittel=str(a.verkehrsmittel).replace('[','').replace(']','').replace("'",'')
                if 'MEr' in mittel:
                    mittel='Fernzug'
                elif 'CNL' in mittel:
                    mittel='Fernzug'
                elif 'IC' in mittel:
                    mittel='Fernzug'
                elif 'ICE' in mittel:
                    mittel='Fernzug'
                elif 'EC' in mittel:
                    mittel='Fernzug'
                elif 'HKX' in mittel:
                    mittel='Fernzug'
                elif 'EN' in mittel:
                    mittel='Fernzug'
                elif 'E' in mittel:
                    mittel='Fernzug'
                elif 'D' in mittel:
                    mittel='Fernzug'

                gfind=0
                for y, b in enumerate( fahrzeug_array):
                    mittel2=""
                    if 'MEr' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'CNL' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'IC' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'ICE' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'EC' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'HKX' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'EN' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'E' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if 'D' in str(b.verkehrsmittel).split(' ')[0].replace('[','').replace(']','').replace("'",''):
                        mittel2='Fernzug'
                    if (a.verkehrsmittel == b.verkehrsmittel or mittel==mittel2) and x!=y:
                        drinn=0
                        for zz in lines:
                            if mittel ==zz or a.verkehrsmittel==zz:
                                drinn=1
                        if drinn ==0:
                            if 'MEr' in a.verkehrsmittel or 'CNL' in a.verkehrsmittel or 'IC' in str(a.verkehrsmittel)or 'ICE' in str(a.verkehrsmittel)or 'EC' in str(a.verkehrsmittel)or 'HKX' in str(a.verkehrsmittel) or 'EN' in str(a.verkehrsmittel)or 'E' in str(a.verkehrsmittel)or'D' in str(a.verkehrsmittel):
                              lines.append(mittel)
                            else:
                                lines.append(a.verkehrsmittel)
                        wogefunden.append(y)
                        nichtchecken.append(y)
                        gfind=1

                if gfind==0:
                 lines.append(a.verkehrsmittel)

                ptime=""
                for woo in wogefunden:
                    for bk in fahrzeug_array[woo].uhrzeit:
                        ptime=str(bk).replace('[','').replace(']','').replace("'",'').replace('"','')
                        split = ptime.split(':')

                        time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1
                for bl in a.uhrzeit:
                    ptime=str(bl).replace('[','').replace(']','').replace("'",'').replace('"','')
                    split = ptime.split(':')
                    time5line[((int(split[0])*60)/5)+int(math.ceil(int(split[1])/5))]=1
                time5lines_linie.append(time5line)


        haeufigkeit=time5lines_linie[0].count(1)
        haufigstelinie=0
        print haeufigkeit
        for zahl, haeufig in enumerate( time5lines_linie):
##            print haeufig.count(1)
            if int(haeufigkeit)<int(haeufig.count(1)):
                haeufigkeit=int(haeufig.count(1))
                haufigstelinie=zahl


        time5lines_linie2=[]
        lines2=[]

        time5lines_linie2.append(time5lines_linie[haufigstelinie])
        time5lines_linie.pop(haufigstelinie)
        lines2.append(lines[haufigstelinie])
        lines2.append("Bus")

        uui=[]
        for k, aaaa in enumerate( time5lines_linie):
            if k==0:
                uui=aaaa
            else:
                uui= map(operator.add, uui, aaaa)

        for zahle, einzel in enumerate( uui):
            if einzel>1:
                uui[zahle]=1

        time5lines_linie2.append(uui)

        if (len(verkehr)>1):
            print "1. Ja"
            print "Unterschiedliche Verkehrstrager"
            style = 1
            zeichne(time5lines_verkehrstraeger,verkehr,Daten[welche][2])
        elif len(ziele)<7:
            print "2. 6 Ziele Ja"
            print "unterschieden nach Fahrtziel"
            style = 2
            zeichne(time5lines_ziel,ziele,Daten[welche][2])
        elif len(lines)<7:
            print "3. max 6 Linien"
            print "Unterscheidung nach Linie"
            style = 3
            zeichne(time5lines_linie,lines,Daten[welche][2])
        else:
            print "Nein, mehr Linien"
            print "Alle Linien und die stärkste in anderer Farbe"
            style = 4
            zeichne(time5lines_linie2,lines2,Daten[welche][2])

        name = Daten[welche][2].replace("(",'').replace(")",'').replace(",",'').replace("/",'').replace(" ",'').replace(unichr(228),'ae').replace(unichr(246),'oe').replace(unichr(252),'ue').replace(unichr(223),'ss')
        results.append([name, style, time.strftime("%x"), Daten[welche][2]])




# Variablen definieren

projektname = str(arcpy.GetParameterAsText(0))
haltestellen = []
if arcpy.GetParameterAsText(1) != "":
    haltestellen.append(arcpy.GetParameterAsText(1).split(" | ")[0])
if arcpy.GetParameterAsText(2) != "":
    haltestellen.append(arcpy.GetParameterAsText(2).split(" | ")[0])
if arcpy.GetParameterAsText(3) != "":
    haltestellen.append(arcpy.GetParameterAsText(3).split(" | ")[0])

base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
workspace_erreichbarkeit = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit_Projekt_'+projektname+'.gdb')
workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
arcpy.env.workspace = workspace_projekt
arcpy.env.overwriteOutput = True


# Daten aus Skript 01 einlesen und in entsprechende Struktur bringen
Daten = []
rows = arcpy.SearchCursor(os.path.join(workspace_erreichbarkeit,"OEPNV_Haltestellen"))
i = 1
for row in rows:
    Daten.append([row.IBNR,row.Distanz,row.Name,row.lon, row.lat, i])
    i+=1
del i
results = [] #Variable zum Sammeln und später dann Speichern der Zwischenergebnisse


#Funktionen:

Abfahrt2(base_path,projektname,Daten)
haltestellen = [Daten[0][2], Daten[1][2], Daten[2][2]]
Daten_temp = []
for n in haltestellen:
    b = 0
    for i in Daten:
##        print i[2]
##        print n
        if i[2] == n:
            Daten_temp.append(Daten[b])
        b+=1
del b

fahrzeug_array_b=Abfahrt(base_path,projektname, Daten_temp)
erstellen_der_timelines(fahrzeug_array_b,Daten_temp)



#############################################################################################################
# Schritt X - Datenexport in temporäre .csv zur späteren Abholung durch den Ergebnissammler
ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen')
with open(ausgabeordner+"\Haltestellen.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile)
    i = 0
    maxa = len(results)
    while i < maxa:
        writer.writerow([results[i][0].encode('latin1'),results[i][1],results[i][2], results[i][3].encode('latin1')])
        i +=1
    del writer, csvfile

print "done"