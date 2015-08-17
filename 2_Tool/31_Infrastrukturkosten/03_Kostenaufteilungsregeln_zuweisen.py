# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Kostenaufteilungsregeln_zuweisen.py
# 
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import arcpy, os, inspect, pyodbc, shutil, gc

arcpy.env.overwriteOutput = True

#Pfade einrichten und Variablen uebergeben

i=-1

i+=1 ; projektname = arcpy.GetParameterAsText(i)

heading = "01 Planungskosten"
i+=1 ; KB1_KP1 = arcpy.GetParameterAsText(i)

heading = "02 Grün-, Ausgleichs- und Ersatzflächen"
i+=1 ; KB2_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB2_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB2_KP3 = arcpy.GetParameterAsText(i)

heading = "03 Innere Verkehrserschliessung"
i+=1 ; KB3_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB3_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB3_KP3 = arcpy.GetParameterAsText(i)

heading = "04 Äußere Verkehrserschliessung"
i+=1 ; KB4_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB4_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB4_KP3 = arcpy.GetParameterAsText(i)

heading = "05 Wasserversorgung"
i+=1 ; KB5_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB5_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB5_KP3 = arcpy.GetParameterAsText(i)

heading = "06 Abwasserentsorgung"
i+=1 ; KB6_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB6_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB6_KP3 = arcpy.GetParameterAsText(i)

heading = "07 Lärmschutz"
i+=1 ; KB7_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB7_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB7_KP3 = arcpy.GetParameterAsText(i)

heading = "08 - Zusatzkosten"
i+=1 ; KB8_KP1 = arcpy.GetParameterAsText(i)
i+=1 ; KB8_KP2 = arcpy.GetParameterAsText(i)
i+=1 ; KB8_KP3 = arcpy.GetParameterAsText(i)

base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
kosten_tool = os.path.join(base_path,'2_Tool',"31_Kosten","FGDB_31_Kosten_Tool.gdb")
kosten_projekt = os.path.join(base_path,'3_Projekte',projektname,"FGDB_31_Kosten_"+projektname+".gdb")

tablepath_costrules_project = os.path.join(kosten_projekt,'Projektspez_Kostenauft')

kostenbereiche = [('01 - Planungsaufwand',1),('02 - Gruen-, Ausgleichs- und Ersatzflaechen',2),('03 - Innere Verkehrserschliessung',3),('04 - Aeussere Verkehrserschliessung',4),('05 - Wasserversorgung',5),('06 - Abwasserentsorgung',6),('07 - Laermschutz',7),('08 - Zusatzkosten',8)]
kostenphasen = [('1 - Erstmalige Herstellung',1),('2 - Betrieb und Unterhaltung',2),('3 - Erneuerung',3)]

for kostenbereich in kostenbereiche:

    kb_name = kostenbereich[0]
    kb = kostenbereich[1]

    for kostenphase in kostenphasen:

        try:

            kp_name = kostenphase[0]
            kp = kostenphase[1]

            rows = arcpy.UpdateCursor(tablepath_costrules_project, "", "", "","")

            for row in rows:
                if row.Kostenbereich == kb_name and row.Kostenphase == kp_name:
                    ziel = "KB"+str(kb)+"_"+"KP"+str(kp)
                    ziel_value = eval(ziel)

                    arcpy.AddMessage(ziel_value)

                    row.Kostenaufteilungsregel = ziel_value
                    rows.updateRow(row)

            del rows, row
        except Exception as e:
            arcpy.AddMessage(e)


# Endmeldung
message = 'Regel zugewiesen'
print message
arcpy.AddMessage(message)