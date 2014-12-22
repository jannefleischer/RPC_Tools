# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 01_Uebergabepunkte_bearbeiten.py
#
# Description:
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
# Import arcpy modules
import arcpy, os, gc, sys
import verkehr_lib as v

arcpy.env.overwriteOutput = True

#Pfade einrichten

i=-1

i+=1 ; projektname = arcpy.GetParameterAsText(i)
i+=1 ; punkt_name = arcpy.GetParameterAsText(i)
i+=1 ; qp_wohnen = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; qp_versorgung = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; qp_gewerbe = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; qp_schulen = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; zp_wohnen = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; zp_versorgung = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; zp_gewerbe = float(arcpy.GetParameterAsText(i).replace(',','.'))
i+=1 ; zp_schulen = float(arcpy.GetParameterAsText(i).replace(',','.'))

base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_verkehr = os.path.join(base_path,'3_Projekte',projektname,'FGDB_33_Verkehr_'+projektname+'.gdb')
workspace_tool_verkehr = os.path.join(base_path,"2_Tool","33_Verkehr","33_Verkehr_Tool.gdb")


#############################################################################################################
#
# Durchlauf Berechnung
#
#############################################################################################################
beginmeldung = 'Starte Ueberarbeitung Uebergabepunkte \n'
arcpy.AddMessage(beginmeldung)
print beginmeldung
#############################################################################################################
# Schritt 1 - Ueberarbeite Uebergabepunkt
schrittmeldung = 'Ueberarbeite Uebergabepunkt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

v.uebergabepunkt_bearbeiten(projektname,punkt_name,qp_wohnen,qp_versorgung,qp_gewerbe,qp_schulen,zp_wohnen,zp_versorgung,zp_gewerbe,zp_schulen)

# Endmeldung
gc.collect()
message = 'Script abgeschlossen'
print message
arcpy.AddMessage(message)