# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Basti
#
# Created:     03.06.2013
# Copyright:   (c) Basti 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#Fertig nur noch abspeichern fehlt
#
import arcpy
import math,sys
import gc,os
from decimal import Decimal

def Betriebstyperstellen(shp_Standortdaten):
    #shp_Standortdaten

    Discounter=['Aktiv-Discount','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']
    try:
        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "Betreibstyp_bzw_Anbeiter", "String")
    except:
        print "error"
        exit(1)
        return
        pass
    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+shp_Standortdaten)

    for maerkte in cur_Standortdaten:

##        print maerkte.Betriebstyp

        if ([g for g in Discounter if str(maerkte.Betriebstyp.encode('utf-8')).lower().replace(' ','') in str(g).lower().replace(' ','')] and maerkte.Betriebstyp.lower()!="Edeka".lower()):
            #Ja ein Discounter
##            print maerkte.Betriebstyp
##            print "Ja ein Discounter"
##            if maerkte.Id==60:
##                print str(maerkte.Betriebstyp).lower()
##                print "netto" in str(maerkte.Betriebstyp).lower() and "edeka" in  str(maerkte.Name_postalisch).lower()
##                print "netto" in str(maerkte.Betriebstyp).lower()
##                print "netto(edeka)" ==  str(maerkte.Name_postalisch).lower()
##                print str(maerkte.Betriebstyp).lower()=="netto(edeka)"

            if "aktiv-discount" in str(maerkte.Betriebstyp).lower() or  "aktiv discount" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Aktiv-Discount"
            elif "diska" in str(maerkte.Betriebstyp).lower() :
                maerkte.Betreibstyp_bzw_Anbeiter="diska"
            elif "lidl" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Lidl"
            elif ("netto" in str(maerkte.Betriebstyp).lower() and "edeka" in  str(maerkte.Name_postalisch).lower() )or (str(maerkte.Betriebstyp).lower()=="netto(edeka)"):
                maerkte.Betreibstyp_bzw_Anbeiter="Netto(Edeka)"
            elif "netto" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Netto"
            elif "aldi" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Aldi"
            elif "penny" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Penny"
            elif "norma" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="Norma"
            elif "np" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="NP"
            elif "treff 3000" in str(maerkte.Betriebstyp).lower():
                maerkte.Betreibstyp_bzw_Anbeiter="treff 3000"
            else:
                #Nicht vorhanden der Betriebstyp
                arcpy.AddMessage("Discounter unbekannt")
                arcpy.AddMessage("Betriebstyp nicht vorhanden MarktId: " + str(maerkte.Id))

            cur_Standortdaten.updateRow(maerkte)
        else:
            #Ein SM
##            print "Ja ein SM"
            if maerkte.VKFL_Gesamt<=400:
                maerkte.Betreibstyp_bzw_Anbeiter="kl. Nahversorgungsmarkt"
                cur_Standortdaten.updateRow(maerkte)
            elif maerkte.VKFL_Gesamt<=800:
                #kl. SM Betreiber
                string="kl. SM "
                if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                elif "kaufland" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                elif "coma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                elif "combi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                elif "familia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                elif "globus" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                elif "migros" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                elif "hit" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                elif "jibi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                elif "markant" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                elif "rewe" in str(maerkte.Betriebstyp).lower() or  "nahkauf" in str(maerkte.Betriebstyp).lower() :
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                elif "tegut" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                elif "perfetto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                elif "v-markt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                elif "wasgau" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                elif "toom" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                elif "sky" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                elif "plaza" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                elif "real" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                elif "denns" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                elif "alnatura" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                elif "basic" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                elif "biocompany" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                elif "vitalia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                elif "viv" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                else:
                    try:
                        Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(maerkte.Name_postalisch)
                    maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                    print "Unbekannter Betreiber "+str(maerkte.Betriebstyp)+ " Zuteilung kl. SM nicht moeglich\n"
                    arcpy.AddMessage("Zuteilung kl. SM nicht moeglich")
                    arcpy.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                cur_Standortdaten.updateRow(maerkte)

            elif maerkte.VKFL_gesamt<=1500:
                #mttl SM Betreiber
                string="mittl. SM "
                if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                elif "kaufland" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                elif "coma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                elif "combi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                elif "familia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                elif "globus" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                elif "migros" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                elif "hit" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                elif "jibi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                elif "markant" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                elif "rewe" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                elif "tegut" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                elif "perfetto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                elif "v-markt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                elif "wasgau" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                elif "toom" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                elif "sky" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                elif "plaza" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                elif "real" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                elif "denns" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                elif "alnatura" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                elif "basic" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                elif "biocompany" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                elif "vitalia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                elif "viv" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                else:
                    try:
                        Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(maerkte.Name_postalisch)
                    maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                    arcpy.AddMessage("Zuteilung mittl. SM nicht moeglich")
                    arcpy.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                cur_Standortdaten.updateRow(maerkte)
            elif maerkte.VKFL_gesamt<=2500:
                #gr SM Betreiber
                string="gr. SM "
                if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                elif "kaufland" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                elif "coma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                elif "combi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                elif "familia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                elif "globus" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                elif "migros" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                elif "hit" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                elif "jibi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                elif "markant" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                elif "rewe" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                elif "tegut" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                elif "perfetto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                elif "v-markt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                elif "wasgau" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                elif "toom" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                elif "sky" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                elif "plaza" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                elif "real" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                elif "denns" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                elif "alnatura" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                elif "basic" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                elif "biocompany" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                elif "vitalia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                elif "viv" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                else:
                    try:
                        Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(maerkte.Name_postalisch)
                    maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                    arcpy.AddMessage("Zuteilung gr. SM nicht moeglich")
                    arcpy.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                cur_Standortdaten.updateRow(maerkte)
            elif maerkte.VKFL_gesamt<=5000:
                #V-Markt SM Betreiber
                string="V-Markt "
                if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                elif "kaufland" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                elif "coma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                elif "combi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                elif "familia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                elif "globus" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                elif "migros" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                elif "hit" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                elif "jibi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                elif "markant" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                elif "rewe" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                elif "tegut" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                elif "perfetto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                elif "v-markt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                elif "wasgau" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                elif "toom" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                elif "sky" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                elif "plaza" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                elif "real" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                elif "denns" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                elif "alnatura" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                elif "basic" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                elif "biocompany" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                elif "vitalia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                elif "viv" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                else:
                    try:
                        Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(maerkte.Name_postalisch)
                    maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                    arcpy.AddMessage("Zuteilung "+string+" nicht moeglich")
                    arcpy.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                cur_Standortdaten.updateRow(maerkte)
            elif maerkte.VKFL_gesamt>5000:
                #SBW SM Betreiber
                string="SBW "
                if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                elif "kaufland" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                elif "coma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                elif "combi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                elif "familia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                elif "globus" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                elif "migros" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                elif "hit" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                elif "jibi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                elif "markant" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                elif "rewe" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                elif "tegut" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                elif "perfetto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                elif "v-markt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                elif "wasgau" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                elif "toom" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                elif "sky" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                elif "plaza" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                elif "real" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                elif "denns" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                elif "alnatura" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                elif "basic" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                elif "biocompany" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                elif "vitalia" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                elif "viv" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                else:
                    try:
                        Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(maerkte.Name_postalisch)
                    maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                    arcpy.AddMessage("Zuteilung "+string+" nicht moeglich")
                    arcpy.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                cur_Standortdaten.updateRow(maerkte)



    del cur_Standortdaten,maerkte




# Sascha bereden - brauche zuteilung aller maerkte zu den typen - sind kl. Nahversorger alle unter 400 m² sofern keine Discounter!

def Einwohnerfinden(shp_Standortdaten):
    #Unbedingt aendern zugefaehrlich nur mit orten
    #shp_Standortdaten

    try:

        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "EW_Gemeindeverband", "LONG")
    except:
        pass

    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+shp_Standortdaten)
    cur_Gemeindezahlen=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Gemeindezahlen"))


    array_cur_Gemeindezahlen=[]
    for werte in cur_Gemeindezahlen:
        array_cur_Gemeindezahlen.append([werte.Name_des_Gemeindeverbandes,werte.Einwohner])
    del werte

    array_Datensammlung=[]
    # #### Hier muss was geändert werden todo

    for eintraege_stand in cur_Standortdaten:
        gefunden=0
        for eintraege_gemeindezahlen in array_cur_Gemeindezahlen:
            if [g for g in array_Datensammlung if eintraege_stand.Ort == g[0] ] :
                for sammlung in array_Datensammlung:
                    if eintraege_stand.Ort == sammlung[0]:
                        eintraege_stand.EW_Gemeindeverband=sammlung[1]
                        break
                del sammlung
                gefunden=1
                cur_Standortdaten.updateRow(eintraege_stand)
                break

            elif eintraege_stand.Ort == eintraege_gemeindezahlen[0]:
                eintraege_stand.EW_Gemeindeverband=eintraege_gemeindezahlen[1]
                array_Datensammlung.append([eintraege_stand.Ort,eintraege_gemeindezahlen[1]])
                gefunden=1
                cur_Standortdaten.updateRow(eintraege_stand)
                break

            elif eintraege_stand.Ort in eintraege_gemeindezahlen[0]:
                eintraege_stand.EW_Gemeindeverband=eintraege_gemeindezahlen[1]
                array_Datensammlung.append([eintraege_stand.Ort,eintraege_gemeindezahlen[1]])
                gefunden=1
                cur_Standortdaten.updateRow(eintraege_stand)
                break
        if gefunden==0:
            print "nicht gefunden"
            exit(1)

    del cur_Gemeindezahlen,cur_Standortdaten,eintraege_stand
def betriebstyp_bestimmung(shp_Standortdaten):
    #shp_Standortdaten

    # Zusatzspalte mit Betriebstyp fuer Attraktivitaet
    try:
        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "Betriebstyp_Attraktivitaet", "TEXT",250)
        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "Gemeindeklasse", "LONG")
    except:
        pass
    #Cursor drauf
    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+shp_Standortdaten)
    cur_Attraktivitaet_Info=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))

    Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']



    array_Attraktivitaet_Info=[]
    for zeile in cur_Attraktivitaet_Info:
        array_Attraktivitaet_Info.append([zeile.Typ,zeile.ein_Markt_in_der_Naehe,zeile.zwei_Maerkte_in_der_Naehe,zeile.drei_Maerkte_in_der_Naehe,zeile.zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N])

    del zeile,cur_Attraktivitaet_Info
##=WENN(N4>=100000;1;WENN(N4>=50000;2;WENN(N4>=20000;3;WENN(N4>=10000;4;WENN(N4>=1;5;0)))))
    for row_standort in cur_Standortdaten:
        gefunden =0
        if row_standort.EW_Gemeindeverband>=100000:
            row_standort.Gemeindeklasse=1
        elif row_standort.EW_Gemeindeverband>=50000:
            row_standort.Gemeindeklasse=2
        elif row_standort.EW_Gemeindeverband>=20000:
            row_standort.Gemeindeklasse=3
        elif row_standort.EW_Gemeindeverband>=10000:
            row_standort.Gemeindeklasse=4
        elif row_standort.EW_Gemeindeverband>=1:
            row_standort.Gemeindeklasse=5
        else :
            row_standort.Gemeindeklasse=0

        #Variable SM kritisch
        for row_attraktiv in array_Attraktivitaet_Info:
            if row_standort.Betreibstyp_bzw_Anbeiter==row_attraktiv[0]  and "allg." not in row_standort.Betreibstyp_bzw_Anbeiter :
##                print "gefunden" , row_standort.Betreibstyp_bzw_Anbeiter
                gefunden =1
                row_standort.Betriebstyp_Attraktivitaet=row_standort.Betreibstyp_bzw_Anbeiter
                cur_Standortdaten.updateRow(row_standort)
                break
        del row_attraktiv

        if gefunden==0:
##            print "nicht gefunden"
##            print row_standort.Betreibstyp_bzw_Anbeiter
##            print len(row_standort.Betreibstyp_bzw_Anbeiter)
##            print row_standort.Betreibstyp_bzw_Anbeiter
##            print "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower()
##            print

            variable=0
            if "allg." in  str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                variable=1
                print row_standort.Betreibstyp_bzw_Anbeiter

        #Sascha fragen welche werrte Discounter bekommen
            if [f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() in f.lower() ] and [c for c in array_Attraktivitaet_Info if  str(row_standort.Betreibstyp_bzw_Anbeiter).lower() != c[0].lower()] and variable==0 :
                cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                row_cur_IAttraktivitaet_Info.setValue("Typ",str(row_standort.Betreibstyp_bzw_Anbeiter))
                row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.59)
                row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.59)
                row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.34)
                row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.06)
                row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.06)
                cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                del cur_IAttraktivitaet_Info
                array_Attraktivitaet_Info.append([str(row_standort.Betreibstyp_bzw_Anbeiter),1,0.59,0.59,0.34,0.06,0.06])
                row_standort.Betriebstyp_Attraktivitaet=str(row_standort.Betreibstyp_bzw_Anbeiter)
                cur_Standortdaten.updateRow(row_standort)
##                print row_standort.Betreibstyp_bzw_Anbeiter
            elif "kaufland" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Attraktivitaet="V-Markt-SBW-Kaufland"
                    cur_Standortdaten.updateRow(row_standort)



            elif "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() and "marktkauf" != row_standort.Name_postalisch.lower() :
                if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
##                    print "Zugeteilt zu kl. SM Edeka"
                    row_standort.Betriebstyp_Attraktivitaet="kl. SM Edeka"
                    cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>800:
##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                    row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Edeka"
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    print "Fehler zuordnung edeka"
            elif "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() and "marktkauf" == row_standort.Name_postalisch.lower():
                vorhanden =0
                if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
##                    print "Zugeteilt zu kl. SM Marktkauf edeka"
                    for schaunach in array_Attraktivitaet_Info:
                        if "kl. SM Marktkauf" == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet="kl. SM Marktkauf"
                            cur_Standortdaten.updateRow(row_standort)
                            break
                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                        row_cur_IAttraktivitaet_Info.setValue("Typ","kl. SM Marktkauf")
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.87)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.58)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.44)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.32)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.32)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["kl. SM Marktkauf",1,0.87,0.58,0.44,0.32,0.32])



                        row_standort.Betriebstyp_Attraktivitaet="kl. SM Marktkauf"
                        cur_Standortdaten.updateRow(row_standort)

                #gefaehrliche stelle
                elif row_standort.VKFL_Gesamt>800:
##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                    for schaunach in array_Attraktivitaet_Info:
                        if "gr.mittl.SM-V-Markt Marktkauf" == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt Marktkauf"
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                        row_cur_IAttraktivitaet_Info.setValue("Typ","gr.mittl.SM-V-Markt Marktkauf")
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["gr.mittl.SM-V-Markt Marktkauf",1,0.7,0.5,0.3,0.1,0.05])
                        row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt Marktkauf"
                        cur_Standortdaten.updateRow(row_standort)
                else:
                    print "Fehler zuordnung Marktkauf"

            elif "sky" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                if row_standort.VKFL_Gesamt>800:
##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                    row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM Sky"
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    print "Fehler zuordnung sky"

            elif "rewe" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
##                    print "Zugeteilt zu kl. SM Rewe"
                    row_standort.Betriebstyp_Attraktivitaet="kl. SM Rewe"
                    cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>800:
##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Rewe"
                    row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM Rewe"
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    print "Fehler zuordnung Rewe"

            elif "famila" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():

##                    print "Zugeteilt zu V-Markt-SBW-Famila"
                    row_standort.Betriebstyp_Attraktivitaet="gr. SM-V-Markt-SBW-Famila"
                    cur_Standortdaten.updateRow(row_standort)

##            elif "sbw" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
##                    vorhanden=0
##                    try:
##                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
##                    except:
####                        print "fehler namenmarkt"
##                        Name_Markt=str(row_standort.Name_postalisch)
##
##                    for schaunach in array_Attraktivitaet_Info:
##                        if "SBW "+ str(Name_Markt) == schaunach[0]:
##                            vorhanden=1
##                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
##                            cur_Standortdaten.updateRow(row_standort)
##                            break
##
##                    if vorhanden==0:
##                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
##                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
##
##                        row_cur_IAttraktivitaet_Info.setValue("Typ","SBW "+ str(Name_Markt))
##                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
##                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
##                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
##                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
##                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
##                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
##                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)
##
##                        del cur_IAttraktivitaet_Info
##                        array_Attraktivitaet_Info.append(["SBW "+row_standort.Betreibstyp_bzw_Anbeiter,1,0.7,0.5,0.3,0.1,0.05])
##
##
##
##                        row_standort.Betriebstyp_Attraktivitaet=str("SBW "+ str(Name_Markt))
##                        cur_Standortdaten.updateRow(row_standort)
            elif "v-markt" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() or "sbw" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    vorhanden=0
                    try:
                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                    except:
                        Name_Markt=str(row_standort.Name_postalisch)

                    for schaunach in array_Attraktivitaet_Info:
                        if "mittl.gr. SM-V-Markt-SBW "+ str(Name_Markt) == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                        row_cur_IAttraktivitaet_Info.setValue("Typ","mittl.gr. SM-V-Markt-SBW "+ str(Name_Markt))
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["mittl.gr. SM-V-Markt-SBW "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                        row_standort.Betriebstyp_Attraktivitaet="mittl.gr. SM-V-Markt-SBW "+ str(Name_Markt)
                        cur_Standortdaten.updateRow(row_standort)


            else:
                #Es sind somit SM
                if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
##                    print "Zugeteilt zu kl. SM allg."
                    vorhanden=0
                    try:
                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt " +row_standort.Name_postalisch
                        Name_Markt=str(row_standort.Name_postalisch)

                    for schaunach in array_Attraktivitaet_Info:
                        if "kl. SM "+ str(Name_Markt) == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                        row_cur_IAttraktivitaet_Info.setValue("Typ","kl. SM "+ str(Name_Markt))
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.87)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.58)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.44)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.32)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.32)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["kl. SM "+ str(Name_Markt),1,0.87,0.58,0.44,0.32,0.32])

                        row_standort.Betriebstyp_Attraktivitaet="kl. SM "+ str(Name_Markt)
                        cur_Standortdaten.updateRow(row_standort)

                elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<=1500:
##                    print "Zugeteilt zu mttl. SM allg"
                    vorhanden=0
                    try:
                            Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                    except:
##                            print "fehler namenmarkt"
                            Name_Markt=str(row_standort.Name_postalisch)

                    for schaunach in array_Attraktivitaet_Info:
                        if "mittl. SM "+ str(Name_Markt) == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                        row_cur_IAttraktivitaet_Info.setValue("Typ","mittl. SM "+ str(Name_Markt))
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["mittl. SM "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                        row_standort.Betriebstyp_Attraktivitaet="mittl. SM "+ str(Name_Markt)
                        cur_Standortdaten.updateRow(row_standort)

                elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<=2500:
##                    print "Zugeteilt zu mttl. SM allg"
                    vorhanden=0
                    try:
                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                    except:
##                        print "fehler namenmarkt"
                        Name_Markt=str(row_standort.Name_postalisch)

                    for schaunach in array_Attraktivitaet_Info:
                        if "gr. SM "+ str(Name_Markt) == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                        row_cur_IAttraktivitaet_Info.setValue("Typ","gr. SM "+ str(Name_Markt))
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["gr. SM "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                        row_standort.Betriebstyp_Attraktivitaet="gr. SM "+ str(Name_Markt)
                        cur_Standortdaten.updateRow(row_standort)

                else:
                    print "Fehler zuordnung "
                    print row_standort.Id


    del cur_Standortdaten,row_standort,array_Attraktivitaet_Info

def betriebstyp_bestimmung_expF(shp_Standortdaten):
    #shp_Standortdaten
    try:

    # Zusatzspalte mit Betriebstyp fuer Attraktivitaet
        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "Betriebstyp_Funktion", "TEXT",250)
    except:
         pass
    #Cursor drauf
    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+shp_Standortdaten)


    cur_ueber100kEW=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Ueber_100kEW"))

    Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']

    array_ueber100kEw=[]
    for zeile in cur_ueber100kEW:
        array_ueber100kEw.append(zeile.Typ)

    del zeile,cur_ueber100kEW

    for row_standort in cur_Standortdaten:
        if row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Aldi'.lower():
            row_standort.Betriebstyp_Funktion='Aldi'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Lidl'.lower():
            row_standort.Betriebstyp_Funktion='Lidl'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Netto(Edeka)'.lower():
            row_standort.Betriebstyp_Funktion='Netto(Edeka)'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Penny'.lower() or row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Netto(dsk)'.lower() or row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Norma'.lower():
            row_standort.Betriebstyp_Funktion='Penny'
            cur_Standortdaten.updateRow(row_standort)
        elif  'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() or  'rewe' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():

            if row_standort.VKFL_Gesamt>400 and row_standort.VKFL_Gesamt<801:
                if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Funktion='kl. SM Edeka'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='kl. SM Rewe'
                    cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<1501:
                if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Funktion='mittl. SM Edeka'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='mittl. SM Rewe'
                    cur_Standortdaten.updateRow(row_standort)

            elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<2501:
                if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Funktion='gr. SM Edeka'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='gr. SM Rewe'
                    cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
                if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Funktion='V-Markt Edeka'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='V-Markt Rewe'
                    cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>5000 :
                if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Funktion='SBW Edeka'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='SBW-Rewe'
                    cur_Standortdaten.updateRow(row_standort)
        elif 'famila' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
            if row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
                row_standort.Betriebstyp_Funktion='V-Markt-Famila'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>5000:
                row_standort.Betriebstyp_Funktion='SBW-Famila'
                cur_Standortdaten.updateRow(row_standort)
            else:
                row_standort.Betriebstyp_Funktion='gr. SM Famila'
                cur_Standortdaten.updateRow(row_standort)

        elif  ([f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() == f.lower() ]):
            row_standort.Betriebstyp_Funktion=row_standort.Betreibstyp_bzw_Anbeiter
            cur_Standortdaten.updateRow(row_standort)

        elif  ([f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() != f.lower() ] and  row_standort.VKFL_Gesamt<401) or row_standort.Betreibstyp_bzw_Anbeiter == 'kl. Nahversorgungsmarkt' :
            row_standort.Betriebstyp_Funktion='kl. Nahversorgungsmarkt'
            cur_Standortdaten.updateRow(row_standort)

        elif  ([f for f in array_ueber100kEw if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() == f.lower() ]):
            row_standort.Betriebstyp_Funktion=row_standort.Betreibstyp_bzw_Anbeiter
            cur_Standortdaten.updateRow(row_standort)

        elif row_standort.VKFL_Gesamt>400 and row_standort.VKFL_Gesamt<801:
            row_standort.Betriebstyp_Funktion='kl. SM allg.'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<1501:
            row_standort.Betriebstyp_Funktion='mittl. SM allg.'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<2501:
            row_standort.Betriebstyp_Funktion='gr. SM allg.'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
            row_standort.Betriebstyp_Funktion='V-Markt allg.'
            cur_Standortdaten.updateRow(row_standort)
        elif row_standort.VKFL_Gesamt>5000 :
            row_standort.Betriebstyp_Funktion='SBW allg.'
            cur_Standortdaten.updateRow(row_standort)
        else:
            print "FEHLER"
            print row_standort.Betreibstyp_bzw_Anbeiter
            print

    del cur_Standortdaten,row_standort

def berechnung_siedlungsdaten(siedlung):
    #siedlung = Siedlungszahlendaten
    try:
        arcpy.AddField_management(workspace_projekt+siedlung, "Lebensmittel", "DOUBLE")
    except:
        print "Unexpected error1:", sys.exc_info()[0]


    cur_Siedlungszellendaten=arcpy.UpdateCursor(workspace_projekt+siedlung)
    cur_Grundeinstellungen=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Grundeinstellungen"))
    cur_KK_Kennziffer_LM=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"KK_Kennziffer_LM"))

    array_cur_Grundeinstellungen=[]
    for werte in cur_Grundeinstellungen:
        vs=[werte.Info,werte.Wert]
        array_cur_Grundeinstellungen.append(vs)

##    print array_cur_Grundeinstellungen[2][1]

    array_KK_Kennziffer_LM=[]
    for werte in cur_KK_Kennziffer_LM:
        vs=[werte.Ort,werte.Wert]
        array_KK_Kennziffer_LM.append(vs)


    #Berechnung Lebensmittel Siedlungszellendaten
    try:

        for zeile in cur_Siedlungszellendaten:
            betrachtung_Ort=zeile.GEN

            # KK Wert immer auf 100 nach neuster Entscheidung
            KK_Wert=100.
##            for suche in array_KK_Kennziffer_LM:
##    ##            print betrachtung_Ort + " vergleich mit " + suche.Ort
##    ##            print str(type(betrachtung_Ort)) + " vergleich mit " + str(type(suche.Ort))
##                if betrachtung_Ort==suche[0]:
##    ##                print "TREFFER"
##                    KK_Wert=suche[1]
##                    break
##    ##                print KK_Wert
##            del suche
##            if KK_Wert==0:
##                print "FEHLER"
##                print betrachtung_Ort
##            print zeile.SZ_Einwohner, array_cur_Grundeinstellungen[1][1] , array_cur_Grundeinstellungen[2][1] ,array_cur_Grundeinstellungen[1][1] * array_cur_Grundeinstellungen[2][1]
            g=(zeile.SZ_Einwohner*array_cur_Grundeinstellungen[1][1]*array_cur_Grundeinstellungen[2][1])
##            print g
            zeile.Lebensmittel=g    #*KK_Wert/100. #*array_cur_Grundeinstellungen[2][1]
            cur_Siedlungszellendaten.updateRow(zeile)
    except:
        print "Unexpected error:", sys.exc_info()[0]

    del cur_Grundeinstellungen,cur_KK_Kennziffer_LM,cur_Siedlungszellendaten

#------------------------------------------------------------------------------------------------------------
#KK-Anteile Wahrsch
def KK_Anteile_Wahrsch(shp_KK_Anteile_Wahrsch,shp_distanzmatrix,shp_standortdaten):
    #shp_KK_Anteile_Wahrsch=KK_Anteile_Wahrsch
    #shp_distanzmatrix=Distanzmatrix
    #shp_standortdaten=Standortdaten

    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,shp_KK_Anteile_Wahrsch))
    except:
        print "fehler beim löschen - "+shp_KK_Anteile_Wahrsch
    try:

        arcpy.CreateTable_management(arcpy.env.workspace,shp_KK_Anteile_Wahrsch,shp_distanzmatrix)
    except:
        print"a) Fehler beim erstellen der Tabelle"+str(shp_distanzmatrix)
        return 1



    cur_Siedlungszellendaten=arcpy.SearchCursor(os.path.join(workspace_projekt,"Siedlungszahlendaten"))
    cur_Standortdaten=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_standortdaten))

    #Neuer MarktID hier setzen
    neuerMarktID=600



##    cur_gesamt =arcpy.SearchCursor(shp+"/gesamt")
    #100.000 EW und mehr
    cur_Ueber_100kEW =arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Ueber_100kEW"))
    #50.000 bis 100.000 EW
    cur_Zwischen_50k_100kEW =arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Zwischen_50k_100kEW"))
    #20.000 bis 50.000 EW
    cur_Zwischen_20k_50kEW =arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Zwischen_20k_50kEW"))
    #10.000 bis 20.000 EW
    cur_Zwischen_10k_20kEW =arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Zwischen_10k_20kEW"))
    #unter 10.000 EW
    cur_Unter_10kEW =arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Unter_10kEW"))

    cur_Distanzmatrix=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_distanzmatrix))


##    array_gesamt=[]
##    for zeile in cur_gesamt:
##        vs=[zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl]
##        array_gesamt.append(vs)
##
##    del zeile,cur_gesamt

    array_Ueber_100kEW=[]
    for zeile in cur_Ueber_100kEW:
        array_Ueber_100kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])
    del zeile,cur_Ueber_100kEW

    array_Zwischen_50k_100kEW=[]
    for zeile in cur_Zwischen_50k_100kEW:
        array_Zwischen_50k_100kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

    del zeile,cur_Zwischen_50k_100kEW

    array_Zwischen_20k_50kEW=[]
    for zeile in cur_Zwischen_20k_50kEW:
        array_Zwischen_20k_50kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

    del zeile,cur_Zwischen_20k_50kEW

    array_Zwischen_10k_20kEW=[]
    for zeile in cur_Zwischen_10k_20kEW:
        array_Zwischen_10k_20kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

    del zeile,cur_Zwischen_10k_20kEW

    array_Unter_10kEW=[]
    for zeile in cur_Unter_10kEW:
        array_Unter_10kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

    del zeile,cur_Unter_10kEW

    fieldnames = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,shp_distanzmatrix))]

    cur_KK_Anteile_Wahrsch=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_KK_Anteile_Wahrsch))

    array_Siedlungszellendaten=[]
    for zeile in cur_Siedlungszellendaten:
        array_Siedlungszellendaten.append([zeile.SZ_ID,zeile.GEN,zeile.GEN,zeile.SZ_Einwohner,zeile.Lebensmittel])
    del zeile,cur_Siedlungszellendaten

    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Funktion,zeile.Gemeindeklasse,zeile.Bonifaktor])

    del zeile,cur_Standortdaten

    row_insert_KK_Anteile_Wahrsch=cur_KK_Anteile_Wahrsch.newRow()

    for zeile in cur_Distanzmatrix:
        for felder in fieldnames[2:]:
            MarktID= int(str(felder).replace('ID_',''))
            for standort_daten in array_Standortdaten:
                if MarktID==standort_daten[0]:
                    if zeile.getValue('ID_'+str(MarktID))!=0. :
                        row_insert_KK_Anteile_Wahrsch.Siedlungsid=zeile.Siedlungsid
                        gemeindeklasse=standort_daten[2]

                        aufschlag_neuer_Markt=1.
##                        if MarktID==neuerMarktID:
##                            aufschlag_neuer_Markt=1.47
                        if standort_daten[3]!=None and standort_daten[3]!="":
##                            print "boni faktor gesetzt " + str(MarktID)
                            aufschlag_neuer_Markt=standort_daten[3]


    ##                    if gemeindeklasse==0:
    ####                        print "GEsamt"
    ##                                    for werte in array_gesamt:
    ##                                        if standort_daten[1]==werte[0]:
    ##
    ##                                            Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ####                                            print Wert
    ##                                            row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        if gemeindeklasse==1:
    ##                        print "GEsamt"
                                        for werte in array_Ueber_100kEW:
                                            if standort_daten[1]==werte[0]:

                                                Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ##                                            print Wert
                                                row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        elif gemeindeklasse==2:
    ##                        print "GEsamt"
                                        for werte in array_Zwischen_50k_100kEW:
                                            if standort_daten[1]==werte[0]:

                                                Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ##                                            print Wert
                                                row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        elif gemeindeklasse==3:
    ##                                    print "GEsamt"
                                        for werte in array_Zwischen_20k_50kEW:
                                            if standort_daten[1]==werte[0]:
    ##                                            print float(werte[1])
    ##                                            print float(werte[2])
    ##                                            print float(zeile.getValue('ID_'+str(MarktID)))/1000
                                                Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ##                                            print Wert
                                                row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        elif gemeindeklasse==4:
    ##                        print "GEsamt"
                                        for werte in array_Zwischen_10k_20kEW:
                                            if standort_daten[1]==werte[0]:

                                                Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ##                                            print Wert
                                                row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        elif gemeindeklasse==5:
    ##                        print "GEsamt"
                                        for werte in array_Unter_10kEW:
                                            if standort_daten[1]==werte[0]:

                                                Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
    ##                                            print Wert
                                                row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                    else:
                        row_insert_KK_Anteile_Wahrsch.Siedlungsid=zeile.Siedlungsid
                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),0.)

        cur_KK_Anteile_Wahrsch.insertRow(row_insert_KK_Anteile_Wahrsch)

    del cur_KK_Anteile_Wahrsch,cur_Distanzmatrix



def Kleinste_Distanzen(shp_distanzmatrix,shp_Standortdaten,shp_Distanzmatrix_dichteste):
    #shp_distanzmatrix= Distanzmatrix
    #shp_Standortdaten= Standortdaten
    #shp_Distanzmatrix_dichteste=Distanzmatrix_dichteste

    cur_Distanzmatrix=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_distanzmatrix))
    cur_Standortdaten=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Standortdaten))

    fieldnamess = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,shp_distanzmatrix))]

    fieldnames= fieldnamess[2:]
##    print fieldnames

    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Attraktivitaet])

    del zeile,cur_Standortdaten


    array_betriebstyp_fieldid=[]
    for name in fieldnames:
        for zeile in array_Standortdaten:
            if int(str(name).replace('ID_',''))==zeile[0]:

                if (len(array_betriebstyp_fieldid)==0):
                    array_betriebstyp_fieldid.append([zeile[1],zeile[0]])
                else:
                    gefunden=0
                    for a in array_betriebstyp_fieldid:
                        if zeile[1]==a[0]:
                            a.append(zeile[0])
                            gefunden=1
                            break
                    if gefunden==0:
                        array_betriebstyp_fieldid.append([zeile[1],zeile[0]])
                    del a


##    print array_betriebstyp_fieldid

    try:
        arcpy.Delete_management("\\"+shp_Distanzmatrix_dichteste)
    except:
        print "fehler beim löschen - Distanzmatrix_dichteste"
    try:
        arcpy.CreateTable_management(workspace_projekt, shp_Distanzmatrix_dichteste)
    except:
        print "FEHLER beim erstellen - Distanzmatrix_dichteste"
        exit(1)


    #Hinzufuegen SiedlungsId Spalte
    arcpy.AddField_management(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste), fieldnamess[1], "LONG")


    #Tabelle vorbereiten
    for eintrag_machen in array_betriebstyp_fieldid:
        arcpy.AddField_management(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_1", "DOUBLE")
        arcpy.AddField_management(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_2", "DOUBLE")
        arcpy.AddField_management(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_3", "DOUBLE")

    #Cursor auf die Tabelle
    cur_Distanzmatrix_dichteste=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste))

    for zeile in cur_Distanzmatrix:
        array_betriebstyp_entfernung=[]
        for field in fieldnames:
            Wert = zeile.getValue(field)
            for a in array_betriebstyp_fieldid:
                zahl = int(str(field).replace('ID_',''))

                if [c for c in a[1:] if int(str(field).replace('ID_',''))==c]: #int(str(field).replace('ID_','')) in a[1]:

                    if len(array_betriebstyp_entfernung)==0:
                        array_betriebstyp_entfernung.append([a[0],Wert,0,0])

                    else:
                        gefunden=0
                        for b in array_betriebstyp_entfernung:
                            if a[0]==b[0]:
##                                if str(b[0])==u"gr. SM Edeka":
##                                    print Wert
##                                    print b[1]
##                                    print b[2]
##                                    print b[3]
##                                    print
                                    #Muellzahlen
                                if Wert ==0:
                                    gefunden=1
                                    break

                                if b[1]>Wert:   # > gewechselt
                                    zw1=b[1]
                                    zw2=b[2]

                                    b[1]=Wert
                                    b[2]=zw1
                                    b[3]=zw2

                                elif b[2]>Wert: # > gewechselt
                                    zw2=b[2]
                                    b[2]=Wert
                                    b[3]=zw2

                                elif b[3]>Wert: # > gewechselt
                                    b[3]=Wert

                                elif b[1]==0:
                                    b[1]=Wert

                                elif b[2]==0:
                                    b[2]=Wert

                                elif b[3]==0:
                                    b[3]=Wert


                                gefunden=1
                                break
                        del b
                        if gefunden==0:
                            array_betriebstyp_entfernung.append([a[0],Wert,0,0])

        try:

            row_Distanzmatrix_dichteste=cur_Distanzmatrix_dichteste.newRow()
    ##            print array_betriebstyp_entfernung
    ##            print
            for  eintraege in array_betriebstyp_entfernung:
                for x,  dreitraege in enumerate( eintraege[1:]):
    ##                print "asd"
    ##                    print eintraege[0]
                    feldername=str(eintraege[0]).replace(',','').replace('.','').replace('-',' ').replace('(','_').replace(')','').replace(' ','_')+"_"+str(x+1)
    ##                print feldername
                    row_Distanzmatrix_dichteste.setValue(str(feldername),dreitraege)
                    row_Distanzmatrix_dichteste.setValue(fieldnamess[1],zeile.getValue(fieldnamess[1]))
        except:
            print "Fehler "
            print fieldnamess[1]
        cur_Distanzmatrix_dichteste.insertRow(row_Distanzmatrix_dichteste)
        del array_betriebstyp_entfernung

    del cur_Distanzmatrix_dichteste,cur_Distanzmatrix,fieldnamess

def Attraktivitaet(shp_Standortdaten,shp_Distanzmatrix_dichteste,shp_Distanzmatrix_dichteste_gewichtung):
    #shp_Standortdaten
    #shp_Distanzmatrix_dichteste
    #shp_Distanzmatrix_dichteste_gewichtung

    Maximaler_AbstandZwMK=1.000 # 2Km

    cur_Standortdaten=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Standortdaten))
    cur_Distanzmatrix_dichteste=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste))
    cur_Attraktivitaet_Info=arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))

    fieldnames_infotabelle=[f.name for f in arcpy.ListFields(os.path.join(workspace_Basis_Daten,"Attraktivitaet_Info"))]

    try:
        arcpy.Delete_management(workspace_projekt+"\\"+shp_Distanzmatrix_dichteste_gewichtung)
    except:
        print "Fehler beim Löschen Distanzmatrix_dichteste_gewichtung"
    try:
        arcpy.CreateTable_management(workspace_projekt, shp_Distanzmatrix_dichteste_gewichtung,shp_Distanzmatrix_dichteste)
    except:
        print "FEHLER erstellen  - Distanzmatrix_dichteste_gewichtung"
        exit(1)
        pass


    fieldnamess = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste))]
    cur_Distanzmatrix_dichteste_gewichtung=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste_gewichtung))




    fieldnames=fieldnamess[2:]

    array_Attraktivitaet_Info=[]
    for zeile in cur_Attraktivitaet_Info:
        array_Attraktivitaet_Info.append([zeile.Typ,zeile.ein_Markt_in_der_Naehe,zeile.zwei_Maerkte_in_der_Naehe,zeile.drei_Maerkte_in_der_Naehe,zeile.zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N])

    del zeile,cur_Attraktivitaet_Info


    wert =[]


    for zeile in cur_Distanzmatrix_dichteste:
        row_Distanzmatrix_dichteste_gewichtung=cur_Distanzmatrix_dichteste_gewichtung.newRow()
        array_betriebstyp_gewichtung_zeile=[]
        for zeile1 in fieldnames:

            wert.append(zeile.getValue(str(zeile1)))
            if len(wert)==3:
##                print "drei werte"
                wert1=wert[0]
                wert2=wert[1]
                wert3=wert[2]
                wert=[]
                ausspalte=[]

                #ueberpruefe wie viele Entfernungen du eigentlich hast
                #Nur ein Markt in der Gegend -> Abbruch
                #Besprechen mit Sascha!
                #veraendert nach email mit maengel von sachsa
##                if wert2==0 and wert3==0 and wert1==0 :
##                    ausspalte.append(None)
##                    ausspalte.append(None)
##                    ausspalte.append(None)
##                elif wert2==0 and wert3==0 :
##                    ausspalte.append(1)
##                    ausspalte.append(None)
##                    ausspalte.append(None)
##                else:
##                    if wert2==0.:
##                        wert2=1000
##                    if wert3==0.:
##                        wert3=1000

##                    print zeile1
##                    print wert1,wert2,wert3

                #Berechnung 1
                if wert1==0:
                    ausspalte.append(None)
                elif wert2==0 and wert3==0:
                    ausspalte.append(1)
                elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                    ausspalte.append(1)
                elif wert3==0:
                    ausspalte.append(2)
                elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                    ausspalte.append(3)
                else:
                    ausspalte.append(2)

                #was ist wenn der dritte wert 0 ist
                #Berechnung 2
                if wert2==0:
                    ausspalte.append(None)
                elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                    ausspalte.append(4)
                elif wert3==0:
                    ausspalte.append(2)
                elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                    ausspalte.append(3)
                else:
                    ausspalte.append(2)

                #Berechnung 3
                if wert3==0:
                    ausspalte.append(None)
                elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                    ausspalte.append(5)
                elif wert3==0:
                    ausspalte.append(2)
                elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                    ausspalte.append(3)
                elif abs(wert2-wert1)<Maximaler_AbstandZwMK:
                    ausspalte.append(6)


                else:
                    #Fehler
                    print " Fehler attraktivitaet"

##                if (zeile.Siedlungsid==1921 or zeile.Siedlungsid==1956 or zeile.Siedlungsid==1994) and (zeile1 == "gr_SM_V_Markt_SBW_Famila_1" or zeile1 == "gr_SM_V_Markt_SBW_Famila_2"or zeile1 == "gr_SM_V_Markt_SBW_Famila_3"):
##                    print ausspalte, zeile.Siedlungsid,wert1 , wert2, wert3
##                if zeile1 == "Penny_1" or zeile1 == "Penny_2"or zeile1 == "Penny_3":
##
##                     print ausspalte , zeile.Siedlungsid

                #Wert aus der Info tabelle fuer den Abstand holen
                gesuchtgefunden=0
                for abc in array_Attraktivitaet_Info:
##                    print
##                    print str(abc[0]).replace('.','').replace('(',' ').replace(')','').replace(',','').replace('_','').replace('-',' ').replace(' ','')
##                    print str(zeile1).replace('_3','').replace('_','')
                    if str(abc[0]).replace('.','').replace('(',' ').replace(')','').replace(',','').replace('_','').replace('-',' ').replace(' ','')==str(zeile1).replace('_3','').replace('_','').replace(' ',''):
##                        print "gefunden in Infotablee"
                        if ausspalte[0]== None:
                            array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),0,0,0])
                        elif ausspalte[1]== None:
                            array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],0,0])
                        elif ausspalte[2]== None:
                            array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],abc[ausspalte[1]],0])
                        else:
                            array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],abc[ausspalte[1]],abc[ausspalte[2]]])
                        gesuchtgefunden=1
                        break


                if gesuchtgefunden==0:
                    print "not found in Infotabelle"
                    print str(zeile1).replace('_3','').replace('_',' ').replace(' ','')

                del abc
                ausspalte=[]
##                print array_betriebstyp_gewichtung_zeile


##        print array_betriebstyp_gewichtung_zeile
        #vor weg nur Id setzen bzw kopieren
        row_Distanzmatrix_dichteste_gewichtung.setValue(str(fieldnamess[1]),zeile.getValue(str(fieldnamess[1])))
##        print array_betriebstyp_gewichtung_zeile
        for asd in array_betriebstyp_gewichtung_zeile:
            if asd[1]==None:
                asd[1]=0
            if asd[2]==None:
                asd[2]=0

            if asd[3]==None:
                asd[3]=0

            row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_1",asd[1])
            row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_2",asd[2])
            row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_3",asd[3])
        cur_Distanzmatrix_dichteste_gewichtung.insertRow(row_Distanzmatrix_dichteste_gewichtung)
##    print "done"


def asd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
    #shp_Siedlungszahlendaten
    #shp_Standortdaten
    #shp_Distanzmatrix
    #shp_Distanzmatrix_dichteste
    #shp_shp_Distanzmatrix_dichteste_gewichtung
    #shp_KK_Anteile_Wahrsch
    #shp_Verteilungsmasstab1
    #shp_Verteilungsmasstab2
    #shp_ET_Kaufkraft
    print os.path.join(workspace_projekt,shp_Siedlungszahlendaten)
    cur_Siedlungszellendaten=arcpy.UpdateCursor(os.path.join(workspace_projekt,shp_Siedlungszahlendaten))

    cur_Distanzmatrix_dichteste=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Distanzmatrix_dichteste))
    cur_Distanzmatrix_dichteste_gewichtung=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_shp_Distanzmatrix_dichteste_gewichtung))

    cur_Distanzmatrix=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Distanzmatrix))
    cur_Standortdaten=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_Standortdaten))
    cur_KK_Anteile_Wahrsch=arcpy.SearchCursor(os.path.join(workspace_projekt,shp_KK_Anteile_Wahrsch))




    fieldnamess = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,shp_Distanzmatrix))]

    fieldnames= fieldnamess[2:]
##    print fieldnames
##    print len (fieldnames)
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,shp_Verteilungsmasstab1))
        arcpy.Delete_management(os.path.join(workspace_projekt,shp_Verteilungsmasstab2))
        arcpy.Delete_management(os.path.join(workspace_projekt,shp_ET_Kaufkraft))
    except:
        print "fehler beim löschen - Verteilung"
    try:
        arcpy.CreateTable_management(workspace_projekt, shp_Verteilungsmasstab1,shp_Distanzmatrix)
        arcpy.CreateTable_management(workspace_projekt, shp_Verteilungsmasstab2,shp_Distanzmatrix)
        arcpy.CreateTable_management(workspace_projekt, shp_ET_Kaufkraft,shp_Distanzmatrix)
    except:
        exit(1)
        print "FEHLER beim Löschen - Verteilung"
        pass




    #curser drauf
    cur_Verteilungsmasstab1=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_Verteilungsmasstab1))
    cur_Verteilungsmasstab2=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_Verteilungsmasstab2))
    cur_Kaufkraft_ET=arcpy.InsertCursor(os.path.join(workspace_projekt,shp_ET_Kaufkraft))


    array_Siedlungszellendaten=[]
    for zeile in cur_Siedlungszellendaten:
        array_Siedlungszellendaten.append([zeile.SZ_ID,zeile.SZ_Einwohner,zeile.Lebensmittel])

    del zeile,cur_Siedlungszellendaten

##    print len(array_Siedlungszellendaten)

    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Attraktivitaet])

    del zeile,cur_Standortdaten

##    print len(array_Standortdaten)


    for distmatrix in cur_Distanzmatrix:

        for b in cur_KK_Anteile_Wahrsch:

            for a in cur_Distanzmatrix_dichteste_gewichtung:

                for abc in cur_Distanzmatrix_dichteste:

##                    print distmatrix.Siedlungsid
##                    print abc.Siedlungsid
##                    print a.Siedlungsid

                    array_irgendwas=[]
                    for name in fieldnames:
##                        print str(int(str(name).replace('ID_','')))
                        row_cur_Verteilungsmasstab1=cur_Verteilungsmasstab1.newRow()
                        for zeile in array_Standortdaten:
                            if int(str(name).replace('ID_',''))==zeile[0]:


    ##                            print zeile [1] # name
##                                print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1"

##                                print b.getValue(name)
##                                print
##                                print distmatrix.getValue(name)
##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1")
##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2")
##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_3")

##                                print str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_') + "_1"
##                                print abc.getValue(str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_') + "_1")
                                welchespalte=str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_').replace('(','_').replace(')','')
##                                print name
##                                print welchespalte
##                                print float(distmatrix.getValue(name))
##                                print float(abc.getValue(welchespalte + "_1"))
##                                print (abc.getValue(welchespalte + "_2"))
##                                print (abc.getValue(welchespalte + "_3"))
##                                print
                                if distmatrix.getValue(name) == (abc.getValue(welchespalte+ "_1")) and distmatrix.getValue(name)!=0.:
##                                    print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1"
##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1")
##                                    print welchespalte
##                                    print name
##                                    print (b.getValue(str(name))*100.)
##                                    print a.getValue(welchespalte+ "_1")
##                                    print

                                    array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte+ "_1"))

##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_1"))

                                elif distmatrix.getValue(name) == abc.getValue(welchespalte + "_2") and distmatrix.getValue(name)!=0.:
##                                    print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2"
##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2")
##                                    print "ID_"+str(distmatrix.Siedlungsid)
##                                    print welchespalte
##                                    print name
##                                    print (b.getValue(str(name))*100.)
##                                    print a.getValue(welchespalte+ "_1")
##                                    print
                                    array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte + "_2"))
##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_2"))


                                elif distmatrix.getValue(name) == abc.getValue(welchespalte+ "_3") and distmatrix.getValue(name)!=0.:
##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_3")
##                                    print welchespalte
##                                    print name
##                                    print (b.getValue(str(name))*100.)
##                                    print a.getValue(welchespalte+ "_1")
##                                    print
                                    array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte + "_3"))
##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_3"))

                                else:
                                    array_irgendwas.append(0.0)
##                                    row_cur_Verteilungsmasstab1.setValue(str(name),0)


                        del zeile

##                    print array_irgendwas
                    row_cur_Verteilungsmasstab1.setValue(fieldnamess[1],distmatrix.Siedlungsid)
                    summe=0.0
                    for spaltenzahl, schreibe in enumerate( array_irgendwas):
                        row_cur_Verteilungsmasstab1.setValue(fieldnames[spaltenzahl],float(schreibe))
                        summe+=schreibe
                    cur_Verteilungsmasstab1.insertRow(row_cur_Verteilungsmasstab1)


##                    print len(array_irgendwas)
##                    print len(fieldnames)



##                    print summe
                    row_cur_Verteilungsmasstab2=cur_Verteilungsmasstab2.newRow()
                    row_cur_Kaufkraft_ET=cur_Kaufkraft_ET.newRow()
##                    test=0.0
##                    test1=0.0
                    nichtgefunden=0
                    for variable_array_Siedlungszellendaten in array_Siedlungszellendaten:

                        if variable_array_Siedlungszellendaten[0]==distmatrix.Siedlungsid:

                            for x, variable_array_irgendwas in enumerate( array_irgendwas):




        ##                            array_irgendwas[x]=(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[3]
                                if summe!=0 and variable_array_irgendwas!=0:

                                    row_cur_Verteilungsmasstab2.setValue(fieldnames[x],variable_array_irgendwas/summe)
                                    row_cur_Kaufkraft_ET.setValue(fieldnames[x],(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[2])
                                else:
                                    row_cur_Verteilungsmasstab2.setValue(fieldnames[x],0.)
                                    row_cur_Kaufkraft_ET.setValue(fieldnames[x],0.)
    ##                                test+=(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[3]
    ##                                test1+=variable_array_irgendwas/summe

                                row_cur_Verteilungsmasstab2.setValue(str(fieldnamess[1]),variable_array_Siedlungszellendaten[0])
                                row_cur_Kaufkraft_ET.setValue(str(fieldnamess[1]),variable_array_Siedlungszellendaten[0])

                            cur_Verteilungsmasstab2.insertRow(row_cur_Verteilungsmasstab2)
                            cur_Kaufkraft_ET.insertRow(row_cur_Kaufkraft_ET)
                            nichtgefunden=1
                            break
                    if nichtgefunden==0:
                        print " nicht gefunden FEHLER"
                        print distmatrix.Siedlungsid

##                    print test
##                    print test1
##                    print
##                        del variable_array_Siedlungszellendaten


##                    print array_irgendwas
                    del array_irgendwas
                    break

                break
            break


    try:
        del row_cur_Verteilungsmasstab2,row_cur_Verteilungsmasstab1
        del cur_Distanzmatrix,cur_Distanzmatrix_dichteste,cur_Distanzmatrix_dichteste_gewichtung,row_cur_Kaufkraft_ET,cur_Kaufkraft_ET,cur_KK_Anteile_Wahrsch,cur_Verteilungsmasstab1,cur_Verteilungsmasstab2
    except:
        print"fehler beim löschen"




def schreibe_KK(shp_Standortdaten,shp_ET_Kaufkraft,shp_Statistik):
    #shp_Standortdaten
    #shp_ET_Kaufkraft
    #shp_Statistik


    try:
        arcpy.AddField_management(workspace_projekt+shp_Standortdaten, "Kaufkraft", "DOUBLE")
    except:
        print "Unexpected error:", sys.exc_info()[0]

    fieldnamess = [f.name for f in arcpy.ListFields(workspace_projekt+shp_ET_Kaufkraft)]

    try:
        arcpy.Delete_management(shp_Statistik)
    except:
        print "fehler beim löschen - Statistik"

    g=[]
    for spalten in fieldnamess[2:]:
        g.append([str(spalten),"SUM"])
    arcpy.Statistics_analysis(workspace_projekt+shp_ET_Kaufkraft, workspace_projekt+shp_Statistik, g)

    fieldname = [f.name for f in arcpy.ListFields(workspace_projekt+shp_Statistik)]

    cur_Statistik= arcpy.SearchCursor(workspace_projekt+shp_Statistik)
    cur_Standortdaten= arcpy.UpdateCursor(workspace_projekt+shp_Standortdaten)

    for einezeile in cur_Statistik:
        for abc in fieldname[2:]:
            for zeile_standort in cur_Standortdaten:
                if int(abc.replace('SUM_ID_',''))==zeile_standort.Id:
                    zeile_standort.Kaufkraft=einezeile.getValue(abc)
                    cur_Standortdaten.updateRow(zeile_standort)
                    break

    del cur_Standortdaten,cur_Statistik,fieldname,fieldnamess

def bilde_gesamt(shp_Uebersicht,shp_Standortdaten):
    #shp_Uebersicht
    #shp_Standortdaten
    try:
        arcpy.Delete_management(shp_Uebersicht)
    except:
        print "fehler beim löschen - Uebersicht"
    try:
        arcpy.CreateTable_management(workspace_projekt,shp_Uebersicht.replace('/',''))
    except:
        print"Fehler beim erstellen der Tabelle"
        return
    try:
        arcpy.AddField_management(workspace_projekt+shp_Uebersicht, "Marke", "TEXT")
        arcpy.AddField_management(workspace_projekt+shp_Uebersicht, "Kaufkraft_ges", "DOUBLE")
    except:
        print "Unexpected error:", sys.exc_info()[0]


    cur_Standortdaten=arcpy.SearchCursor(workspace_projekt+shp_Standortdaten)

    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.Betriebstyp_Attraktivitaet,zeile.Kaufkraft,zeile.Id])

    del zeile,cur_Standortdaten

    neues_array=[]

    neues_array.append(array_Standortdaten[0])
    array_Standortdaten.pop(0)


    for inhalt_db in array_Standortdaten:
        gefundenn=0
        for inhalt_array in neues_array:
            if inhalt_db[0]==inhalt_array[0]: #and (int(inhalt_db[2])!=600 and int( inhalt_db[2])!=601) :
##                print inhalt_db[2]
                inhalt_array[1]+=inhalt_db[1]
                gefundenn=1
                break

        if gefundenn==0:
            neues_array.append([inhalt_db[0],inhalt_db[1]])


##    print neues_array
    cur_Uebersicht= arcpy.InsertCursor(workspace_projekt+shp_Uebersicht)

    for inhalt in neues_array:
##        print type(inhalt[1])
        row_cur_Uebersicht=cur_Uebersicht.newRow()
        row_cur_Uebersicht.Kaufkraft_ges=inhalt[1]
        row_cur_Uebersicht.setValue("Marke",str(inhalt[0]))

        cur_Uebersicht.insertRow(row_cur_Uebersicht)

    del cur_Uebersicht
    del neues_array,array_Standortdaten


def zentralitaet(shp_Zentralitaet,shp_Standortdaten):
    #shp_Zentralitaet
    #shp_Standortdaten
    try:
        arcpy.Delete_management(shp_Zentralitaet)
    except:
        print "fehler beim löschen - Zentralitaet"
    try:
        arcpy.CreateTable_management(workspace_projekt,shp_Zentralitaet.replace('/',''))
    except:
        print"Fehler beim erstellen der Tabelle"
        return
    try:
        arcpy.AddField_management(workspace_projekt+shp_Zentralitaet, "Region", "TEXT")
        arcpy.AddField_management(workspace_projekt+shp_Zentralitaet, "KK", "DOUBLE")
        arcpy.AddField_management(workspace_projekt+shp_Zentralitaet, "Umsatz", "DOUBLE")
        arcpy.AddField_management(workspace_projekt+shp_Zentralitaet, "Zentralitaet", "DOUBLE")
        arcpy.AddField_management(workspace_projekt+shp_Zentralitaet, "VKF_pro_EW", "DOUBLE")
    except:
        print "Unexpected error:", sys.exc_info()[0]


    cur_Standortdaten=arcpy.SearchCursor(workspace_projekt+shp_Standortdaten)
    cur_Siedlungszahlendaten=arcpy.SearchCursor(workspace_projekt+"/Siedlungszahlendaten")

    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.Ort,zeile.VKFL_Gesamt,zeile.EW_Gemeindeverband,zeile.Kaufkraft,zeile.Id])

    del zeile,cur_Standortdaten


    array_Siedlungszahlendaten=[]
    for zeile in cur_Siedlungszahlendaten:
        array_Siedlungszahlendaten.append([zeile.Gen,zeile.Lebensmittel,zeile.SZ_Einwohner])

    del zeile,cur_Siedlungszahlendaten

    neues_array1=[]
    neues_array1.append(array_Siedlungszahlendaten[0])
    array_Siedlungszahlendaten.pop(0)

    for inhalt_db in array_Siedlungszahlendaten:
        gefundenn=0
        for inhalt_array in neues_array1:
            if inhalt_db[0]==inhalt_array[0]:
                inhalt_array[1]+=inhalt_db[1]
                inhalt_array[2]+=inhalt_db[2]
                gefundenn=1
                break

        try:
            del inhalt_array
        except:
            pass

        if gefundenn==0:
            neues_array1.append([inhalt_db[0],inhalt_db[1],inhalt_db[2]])


##    print "neues array1"
##    print neues_array1

    neues_array2=[]
    neues_array2.append(array_Standortdaten[0])
    array_Standortdaten.pop(0)

    for inhalt_db in array_Standortdaten:
        gefundenn=0
        for inhalt_array in neues_array2:
            if inhalt_db[0]==inhalt_array[0]:
                inhalt_array[1]+=inhalt_db[1]
                inhalt_array[3]+=inhalt_db[3]

                gefundenn=1
                break

        if gefundenn==0:
            neues_array2.append([inhalt_db[0],inhalt_db[1],inhalt_db[2],inhalt_db[3]])
##    print "neues_array2"
##    print neues_array2
    cur_Uebersicht= arcpy.InsertCursor(workspace_projekt+shp_Zentralitaet)



    for inhalt1 in neues_array2:
        gefunden=0
        for inhalt in neues_array1:
            if (inhalt1[0]==inhalt[0]):

                row_cur_Uebersicht=cur_Uebersicht.newRow()
                row_cur_Uebersicht.setValue("Region",(inhalt[0]))
                row_cur_Uebersicht.KK=inhalt1[3]
                row_cur_Uebersicht.Umsatz=inhalt1[3]
                row_cur_Uebersicht.Zentralitaet=(inhalt1[3]/inhalt[1])*100
                row_cur_Uebersicht.VKF_pro_EW=(inhalt1[2]/inhalt1[3])*100

                gefunden=1


                cur_Uebersicht.insertRow(row_cur_Uebersicht)
                break
        try:
            del inhalt
        except:
            pass

        if gefunden ==0:
            print "keine Uebereinstimmung"
            print(inhalt1[0])

    del cur_Uebersicht
    del neues_array1,neues_array2,array_Standortdaten,array_Siedlungszahlendaten


def kaufkraft_inSied(shp_siedlungszellendaten,shp_kaufkraft):
    #shp_siedlungszellendaten
    #shp_kaufkraft
    try:
        arcpy.DeleteField_management(workspace_projekt+shp_siedlungszellendaten,"KK_Neu")
    except:
        pass

    try:
        arcpy.AddField_management(workspace_projekt+shp_siedlungszellendaten, "KK_Neu", "DOUBLE")


    except:
        print"error"
        return

    cur_Update_sied = arcpy.UpdateCursor(workspace_projekt+shp_siedlungszellendaten)
    cur_Update_etkk=arcpy.UpdateCursor(workspace_projekt+shp_kaufkraft)

    for a in cur_Update_sied:
        for b in cur_Update_etkk:
            if a.SZ_ID == b.Siedlungsid:
                a.KK_neu=b.getValue("ID_600")*100./a.getValue("Lebensmittel")
                cur_Update_sied.updateRow(a)
                break


    try:
        arcpy.DeleteField_management(workspace_projekt+shp_siedlungszellendaten,"KK_Neu_2")
    except:
        pass

    try:
        arcpy.AddField_management(workspace_projekt+shp_siedlungszellendaten, "KK_Neu_2", "DOUBLE")
    except:
        print"error"
        return

    for a in cur_Update_sied:
        for b in cur_Update_etkk:
            if a.SZ_ID == b.Siedlungsid:
                try:
                    a.KK_neu_2=b.getValue("ID_601")*100./a.getValue("Lebensmittel")
                except:
                    print "markt 601 nicht vorhanden ->keine kk anhaengen an siedlungszellen"
                    return

                cur_Update_sied.updateRow(a)
                break

    del cur_Update_etkk,cur_Update_sied


def verlustrechnung(shp_standortdaten):


    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+"/Standortdaten")
    cur_Zentren= arcpy.UpdateCursor(workspace_projekt+"/Zentren")

    try:
        arcpy.Delete_management(workspace_projekt+"/Verlustrechnung")
    except:
        pass


    try:

        arcpy.CreateTable_management(arcpy.env.workspace,"Verlustrechnung")
    except:
        print"a) Fehler beim erstellen der Tabelle"+str("Verlustrechnung")
        return 1

    try:
        arcpy.AddField_management(workspace_projekt+"/Verlustrechnung","Kommune","TEXT")
        arcpy.AddField_management(workspace_projekt+"/Verlustrechnung","Umsatz_vorher","DOUBLE")
        arcpy.AddField_management(workspace_projekt+"/Verlustrechnung","Umsatz_nachher","DOUBLE")
        arcpy.AddField_management(workspace_projekt+"/Verlustrechnung","Differenz","DOUBLE")
        arcpy.AddField_management(workspace_projekt+"/Verlustrechnung","Differenz_Proz","DOUBLE")
    except:
        pass

    cur_Ins_Verlust=arcpy.InsertCursor(workspace_projekt+"/Verlustrechnung")


    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.Id,zeile.Ort,zeile.Kaufkraft])

    del zeile,cur_Standortdaten

    array_Standortdaten_Orte=[]
    for zeilen_st in array_Standortdaten:
        gefunde=0
        for zeile_orte in array_Standortdaten_Orte:
            if zeile_orte[0]==zeilen_st[1]:
                zeile_orte[1]+=zeilen_st[2]
                gefunde=1
                break

        try:
            del zeile_orte
        except:
            pass

        if gefunde==0:
            array_Standortdaten_Orte.append([zeilen_st[1],zeilen_st[2]])


##    print array_Standortdaten_Orte

    array_Zentren=[]
    for zeilen in cur_Zentren:
        gefunden2=0
        for inhalt_array in array_Zentren:
            if zeilen.Zentren==inhalt_array[0]:
              inhalt_array.append(zeilen.Markt_1)
              gefunden2=1
        try:
            del inhalt_array
        except:
            pass
        if gefunden2==0:
            array_Zentren.append([str(zeilen.Zentren),zeilen.Markt_1])

##    print array_Zentren
##    print len( array_Zentren)


    for zeile_array in array_Zentren:
##        print zeile_array
##        print len(zeile_array)
        summe=0
        for z in xrange(len(zeile_array)):
            if z!=0:
                for zeile_array_st in array_Standortdaten:
                    if zeile_array_st[0]==zeile_array[z]:
                        summe+=zeile_array_st[2]
##                        print zeile_array_st[2]
##                        print zeile_array[z]


        zeile_array.append(summe)


    for x in xrange(len(array_Zentren)):
        for zeilen_array_st in array_Standortdaten:
            if array_Zentren[x][1]==zeilen_array_st[0]:
                array_Zentren[x].append(zeilen_array_st[1])
                break

    print array_Standortdaten_Orte
    print len (array_Standortdaten_Orte)
    for array_zent in array_Zentren:
        for i, array_orte in enumerate( array_Standortdaten_Orte):
##            print array_zent[len(array_zent)-1]
            if array_zent[len(array_zent)-1]== array_orte[0]:
                array_orte[1]-=array_zent[len(array_zent)-2]
                array_Standortdaten_Orte.insert(i+1,[array_zent[0],array_zent[len(array_zent)-2]])
##                neues_array = array_Standortdaten_Orte[:i]
##                neues_array.append([array_zent[0],array_zent[len(array_zent)-2]])
##                neues_array.append( array_Standortdaten_Orte[i:].replace('[[','[').replace(']]]',']'))
##                print
##                print neues_array
##                print
##                array_Standortdaten_Orte=neues_array
                break

        del i , array_orte


    for blabla in array_Standortdaten_Orte:
        row = cur_Ins_Verlust.newRow()
        row.setValue("Kommune",blabla[0])
        row.setValue("Umsatz_vorher",blabla[1])

        cur_Ins_Verlust.insertRow(row)

    del cur_Ins_Verlust, cur_Zentren,row,array_Standortdaten,array_Standortdaten_Orte,array_zent,array_Zentren

    cur_Standortdaten=arcpy.UpdateCursor(workspace_projekt+"/Standortdaten_planfall")
    cur_Zentren= arcpy.UpdateCursor(workspace_projekt+"/Zentren")
    cur_up_Verlust=arcpy.UpdateCursor(workspace_projekt+"/Verlustrechnung")


    array_Standortdaten=[]
    for zeile in cur_Standortdaten:
        array_Standortdaten.append([zeile.Id,zeile.Ort,zeile.Kaufkraft])

    del zeile,cur_Standortdaten

    array_Standortdaten_Orte=[]
    for zeilen_st in array_Standortdaten:
        gefunde=0
        if zeilen_st[0] != 600 and zeilen_st[0]!= 601:
            for zeile_orte in array_Standortdaten_Orte:
                if zeile_orte[0]==zeilen_st[1]:
                    zeile_orte[1]+=zeilen_st[2]
                    gefunde=1
                    break

            try:
                del zeile_orte
            except:
                pass

            if gefunde==0:
                array_Standortdaten_Orte.append([zeilen_st[1],zeilen_st[2]])


##    print array_Standortdaten_Orte

    array_Zentren=[]
    for zeilen in cur_Zentren:
        gefunden2=0
        for inhalt_array in array_Zentren:
            if zeilen.Zentren==inhalt_array[0]:
              inhalt_array.append(zeilen.Markt_1)
              gefunden2=1
        try:
            del inhalt_array
        except:
            pass
        if gefunden2==0:
            array_Zentren.append([str(zeilen.Zentren),zeilen.Markt_1])

##    print array_Zentren
##    print len( array_Zentren)


    for zeile_array in array_Zentren:
##        print zeile_array
##        print len(zeile_array)
        summe=0
        for z in xrange(len(zeile_array)):
            if z!=0:
                for zeile_array_st in array_Standortdaten:
                    if zeile_array_st[0]==zeile_array[z]:
                        summe+=zeile_array_st[2]
##                        print zeile_array_st[2]
##                        print zeile_array[z]


        zeile_array.append(summe)


    for x in xrange(len(array_Zentren)):
        for zeilen_array_st in array_Standortdaten:
            if array_Zentren[x][1]==zeilen_array_st[0]:
                array_Zentren[x].append(zeilen_array_st[1])
                break

##    print array_Standortdaten_Orte
##    print len (array_Standortdaten_Orte)
    for array_zent in array_Zentren:
        for i, array_orte in enumerate( array_Standortdaten_Orte):
##            print array_zent[len(array_zent)-1]
            if array_zent[len(array_zent)-1]== array_orte[0]:
                array_orte[1]-=array_zent[len(array_zent)-2]
                array_Standortdaten_Orte.insert(i+1,[array_zent[0],array_zent[len(array_zent)-2]])
##                neues_array = array_Standortdaten_Orte[:i]
##                neues_array.append([array_zent[0],array_zent[len(array_zent)-2]])
##                neues_array.append( array_Standortdaten_Orte[i:].replace('[[','[').replace(']]]',']'))
##                print
##                print neues_array
##                print
##                array_Standortdaten_Orte=neues_array
                break

        del i , array_orte

##    print len (array_Standortdaten_Orte)
    for blabla in array_Standortdaten_Orte:
        for azu in cur_up_Verlust:
            if azu.Kommune== blabla[0]:
                azu.setValue("Umsatz_nachher",blabla[1])
                azu.setValue("Differenz",blabla[1]-azu.getValue("Umsatz_vorher"))
                azu.setValue("Differenz_proz",azu.getValue("Differenz")*100./azu.getValue("Umsatz_vorher"))
                cur_up_Verlust.updateRow(azu)
                break

    del cur_up_Verlust, cur_Zentren,azu,array_Standortdaten,array_Standortdaten_Orte,array_zent,array_Zentren,blabla


def Umsatz_dif():

    cur_Statistik=arcpy.UpdateCursor(workspace_projekt+"/Statistik")
    cur_Statistik_plan= arcpy.UpdateCursor(workspace_projekt+"/Statistik_planfall")

    try:
        arcpy.Delete_management(workspace_projekt+"/Diff_Umsatz")
    except:
        pass


    try:

        arcpy.CreateTable_management(arcpy.env.workspace,"Diff_Umsatz","Statistik_planfall")
    except:
        print"a) Fehler beim erstellen der Tabelle"+str("Diff_Umsatz")
        return 1

    fieldnames = [f.name for f in arcpy.ListFields(workspace_projekt+"/Statistik_planfall")]
    fieldnames=fieldnames[2:]
##    print fieldnames
    array=[]
    for c in cur_Statistik_plan:
        for a in cur_Statistik:
            for b in fieldnames:
                try:
                    if (b=="SUM_ID_600" or b=="SUM_ID_601" ):
                        array.append([b,c.getValue(b)])
                    else:
                        dif=a.getValue(b)-c.getValue(b)
                        array.append([b,dif])

                except:
##                    array.append([b,0])
                    pass

    print array

    cur_ins = arcpy.InsertCursor(workspace_projekt+"\Diff_Umsatz")
    zeile = cur_ins.newRow()
    for zu in range(len(array)):
        zeile.setValue(str(array[zu][0]),array[zu][1])

    cur_ins.insertRow(zeile)

    del cur_ins,cur_Statistik,cur_Statistik_plan

    fieldnames = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,"Diff_Umsatz"))]
    fieldnames=fieldnames[2:]
    loeschfield=[]
    upd_cur_diif_um=arcpy.UpdateCursor(os.path.join(workspace_projekt,"Diff_Umsatz"))
    for a in upd_cur_diif_um:
        for spaltenchecker in fieldnames:
##            print spaltenchecker, a.getValue(spaltenchecker)
            if (a.getValue(spaltenchecker)==None):
                loeschfield.append(str(spaltenchecker))

##    print loeschfield
    del upd_cur_diif_um ,a
    for zz in loeschfield:
##        print zz
        arcpy.DeleteField_management (os.path.join(workspace_projekt,"Diff_Umsatz"), str(zz))

gc.collect()

projektname = arcpy.GetParameterAsText(0)
matrixdirectory = arcpy.GetParameterAsText(1)
siedlungszellendirectory = arcpy.GetParameterAsText(2)
maerktedirectory = arcpy.GetParameterAsText(3)
neuemaerkteid1 = arcpy.GetParameterAsText(4)
neuemaerkteid2 = arcpy.GetParameterAsText(5)
neuemaerkteid3 = arcpy.GetParameterAsText(6)
verbindenemaerkte1 = arcpy.GetParameterAsText(7)
verbindenemaerkte2 = arcpy.GetParameterAsText(8)
verbindenemaerkte3 = arcpy.GetParameterAsText(9)




##shp="P:/RegionProjektCheck/Wertveraenderung_gewerbe/AllesNeu/NeusterStand.gdb"
##shp=r"C:\Users\Basti\Dropbox\RPC\00_Entwicklungsumgebung\3_Projekte\LKH_Tostedt\FGDB_34_Wertveraenderungen_LKH_Tostedt.gdb"

projektname="HCU_ZGB_OTLindenEZH"
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_Basis_Daten = os.path.join(base_path, '2_Tool', '34_Wertveraenderungen','FGDB_34_Wertveraenderungen_Tool.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Wertveraenderungen_' + projektname + '.gdb')


arcpy.env.workspace=workspace_projekt
arcpy.env.overwriteOutput = True





#Ablauf
#standortdaten
#neuer markt
#vorhanden
##arcpy.AddMessage("Beziehe notwendige Daten aus der Datenbank")
##Betriebstyperstellen("/Standortdaten")
####Einwohnerfinden("/Standortdaten") # TODO  einwohner irgendwo anders herholen wieder rein
##betriebstyp_bestimmung("/Standortdaten")
##betriebstyp_bestimmung_expF("/Standortdaten")
#######Neuer Markt
##Betriebstyperstellen("/Neuer_Markt")
####Einwohnerfinden("/Neuer_Markt")
##betriebstyp_bestimmung("/Neuer_Markt")
##betriebstyp_bestimmung_expF("/Neuer_Markt")
###Standortdatenplanfall erstellen
##arcpy.AddMessage("Erstelle Standortdatenplanfall")
##arcpy.Merge_management([workspace_projekt+"/Standortdaten",workspace_projekt+"/Neuer_Markt"],workspace_projekt+"/Standortdaten_planfall")
####
##if arcpy.Exists("/Siedlungszahlendaten_planfall"):
###Siedlungszellen kopieren bzw planfall erstellen
##    arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszahlendaten_planfall"))
##arcpy.Copy_management(os.path.join(workspace_projekt,"Siedlungszahlendaten"),"Siedlungszahlendaten_planfall")

##
##
###Umschreiben
###arcpy.Copy_management(variable eingabe toolbox,workspace_projekt+"/Distanzmatrix_planfall")
##
##if arcpy.Exists("/Distanzmatrix_planfall"):
##    arcpy.AddMessage("Distanzmatrix gefunden")
##    arcpy.AddMessage("Erstelle Distanzmatrix Nullfall")
##    try:
##        arcpy.Delete_management("/Distanzmatrix")
##    except:
##        pass
##
##    arcpy.Copy_management(workspace_projekt+"/Distanzmatrix_planfall",workspace_projekt+"/Distanzmatrix")
##    try:
##        arcpy.DeleteField_management (workspace_projekt+"/Distanzmatrix", "ID_600")
##    except:
##        arcpy.AddMessage("Distanzmatrix konnte nicht vorbereitet werden - bitte starten Sie ArcGis erneut und starten Sie die Toolbox erneut")
##        print "exit 1"
##        exit(1)
####        return
##    try:
##        arcpy.DeleteField_management (workspace_projekt+"/Distanzmatrix", "ID_601")
##    except:
##        pass
##arcpy.AddMessage("Distanzmatrix vorbereitet")
##
##
##berechnung_siedlungsdaten("/Siedlungszahlendaten")
##if KK_Anteile_Wahrsch("KK_Anteile_Wahrsch","Distanzmatrix","Standortdaten")==1:
##    print "Fehler in KK_Anteile_Wahrsch"
##    exit(1)
##
##
##Kleinste_Distanzen("Distanzmatrix","Standortdaten","Distanzmatrix_dichteste")
##Attraktivitaet("Standortdaten","Distanzmatrix_dichteste","Distanzmatrix_dichteste_gewi")
##
###sd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
##asd("Siedlungszahlendaten","Standortdaten","Distanzmatrix","KK_Anteile_Wahrsch","Distanzmatrix_dichteste","Distanzmatrix_dichteste_gewi","Verteilungsmas_1","Verteilungsmas_2","ET_Kaufkraft")
##schreibe_KK("/Standortdaten","/ET_Kaufkraft","/Statistik")
##bilde_gesamt("/Uebersicht","/Standortdaten")
##zentralitaet("/Zentralitaet","/Standortdaten")

####
###------------------------------------------------------------------Berechnung Nullfall beendet
arcpy.AddMessage("Planfall berechnung starten")

arcpy.AddMessage("Distanzmatrixplanfall verwenden")


berechnung_siedlungsdaten("/Siedlungszahlendaten_planfall")
if KK_Anteile_Wahrsch("KK_Anteile_Wahrsch_planfall","Distanzmatrix_planfall","Standortdaten_planfall")==1:
    print "Fehler in KK_Anteile_Wahrsch_planfall"
    exit(1)

Kleinste_Distanzen("Distanzmatrix_planfall","Standortdaten_planfall","Distanzmatrix_dichteste_planfall")
Attraktivitaet("Standortdaten_planfall","Distanzmatrix_dichteste_planfall","Distanzmatrix_dichteste_gewi_planfall")

#sd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
asd("Siedlungszahlendaten_planfall","Standortdaten_planfall","Distanzmatrix_planfall","KK_Anteile_Wahrsch_planfall","Distanzmatrix_dichteste_planfall","Distanzmatrix_dichteste_gewi_planfall","Verteilungsmas_1_planfall","Verteilungsmas_2_planfall","ET_Kaufkraft_planfall")
schreibe_KK("/Standortdaten_planfall","/ET_Kaufkraft_planfall","/Statistik_planfall")
bilde_gesamt("/Uebersicht_planfall","/Standortdaten_planfall")
zentralitaet("/Zentralitaet_planfall","/Standortdaten_planfall")
verlustrechnung("/Standortdaten_planfall")
kaufkraft_inSied("/Siedlungszahlendaten_planfall","/ET_Kaufkraft_planfall")
Umsatz_dif()


gc.collect()
print "done"
