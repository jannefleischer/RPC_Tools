# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Definition_Zentren.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import gc
import os

import arcpy
def main(parameters, messages):
    gc.collect()
    projektname=parameters[0].valueAsText
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_projekt = join(base_path, '3_Projekte', projektname,'FGDB_Standortkonkurrenz_Supermaerkte_' + projektname + '.gdb')

    cur_checker= arcpy.SearchCursor(join(workspace_projekt,"Zentren"))
    array_checker=[]
    gefunden=0
    for rows in cur_checker:
        gefunden=0
        if len(array_checker)==0:
            array_checker.append([rows.Zentren, rows.Markt_1])

        for a in array_checker:
            if rows.Zentren== a[0]:
                a.append(rows.Markt_1)
                gefunden=1

        if gefunden==0:
            array_checker.append([rows.Zentren, rows.Markt_1])

    zuloesch=[]
    print array_checker
    for b in array_checker:
        if len(b)<4:
            zuloesch.append(b[0])
            messages.AddMessage("Das Zentrum "+str(b[0])+" wird geloescht, da weniger als drei Maerkte dem Zentrum zugeordnet wurden.")


    if len(zuloesch)>0:
        messages.AddMessage("Zum erneuten Erstellen der Zentren wiederholen Sie Tool 03 Definition von Zentren.")

    print zuloesch

    for c in zuloesch:
        query="\"Zentren\" =\'"+str(c).replace('u','',0).replace("'",'')+"\'"
        print query
        q=arcpy.MakeTableView_management(workspace_projekt+"\Zentren", "customer_view")
        e=arcpy.SelectLayerByAttribute_management("customer_view","NEW_SELECTION",query)
        w=arcpy.DeleteRows_management("customer_view")
        arcpy.Delete_management("customer_view")
        del q,e,w

    del cur_checker, zuloesch,array_checker
    gc.collect()
    messages.AddMessage("\n\nErfolgreich beendet und gespeichert!")
    print"done"