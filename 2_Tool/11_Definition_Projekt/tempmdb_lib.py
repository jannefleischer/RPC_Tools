# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 01_Mengenermittlung.py
#
# Description:
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

def temp_mdb(eingangstabellen,sql,ausgabetabelle):
    # funktionsweise: kopiere tabellen aus einer gegebenen liste in eine temporäre PGDB, fuere sql-code auf diesen tabellen aus und kopiere das ergebnis zurueck

    import arcpy
    import inspect
    import pyodbc
    import shutil
    import gc
    import os
    import sys
    gc.collect()

    arcpy.env.overwriteOutput = True

    # Create Temp Folder
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    wirkungsfeld_path = os.path.join(base_path,'2_Tool',"11_Definition_Projekt") # Pfad zur temporaeren mdb
    #wirkungsfeld_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt'))
    out_folder_path = os.path.join(base_path,'2_Tool',"11_Definition_Projekt","temp") # Pfad zur temporaeren mdb inkl.
    temp_mdb_path =  os.path.join(out_folder_path,"PGDB_Temp.mdb")


    if not os.path.exists(out_folder_path):
        arcpy.CreateFolder_management(wirkungsfeld_path, "temp")

    # Create Temp MDB File
    out_name = "PGDB_Temp.mdb"
    out_version = "10.0"
    try:
        arcpy.CreatePersonalGDB_management (out_folder_path, out_name, out_version)
    except:
        shutil.rmtree(out_folder_path)
        if not os.path.exists(out_folder_path): os.makedirs(out_folder_path)

    # Copy given tables to Temporary MDB File
    for eingangstabelle in eingangstabellen:
        eingangstabelle_pfad = os.path.join(eingangstabelle[0], eingangstabelle[1])
        temptabelle_pfad = os.path.join(temp_mdb_path, eingangstabelle[1].replace(' ','_'))

        arcpy.CopyRows_management(eingangstabelle_pfad, temptabelle_pfad, "")

        kopiermessage = "Tabelle: "+eingangstabelle[1] + " kopiert \n"
        #print kopiermessage
        #arcpy.AddMessage(kopiermessage)

    # run SQL code on imported tables in PGDB
    connectionstring = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+temp_mdb_path # create connection string

    conn = pyodbc.connect(connectionstring)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        #arcpy.AddMessage("Befehl ausgefuehrt \n")
    except Exception as e:
        print sql
        print e
        print "sql-fehlerhaft"
        arcpy.AddMessage("sql-fehlerhaft \n")
        arcpy.AddMessage(sql)
    conn.commit()
    conn.close()

    # Copy resulting table to FGDB
    fgdb_eingangstabelle_pfad = os.path.join(temp_mdb_path, ausgabetabelle[1])
    fgdb_ausgabetabelle_pfad = os.path.join(ausgabetabelle[0], ausgabetabelle[1])

    arcpy.CopyRows_management(fgdb_eingangstabelle_pfad, fgdb_ausgabetabelle_pfad, "")

    # Delete Temp Folder
    shutil.rmtree(out_folder_path)

    # Collect Garbage
    gc.collect()