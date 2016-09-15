# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# projektKopieren.py
# 
# Description: 
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import os
import shutil
import sys

import arcpy

try:
#get new Project Name as input
    projectNameOld = arcpy.GetParameterAsText(0)
    #projectNameOld = "Bultweg_Sued_fiktiv"
#allow the upload of a shapefile containg the projektgebiet
    projectNameNew = arcpy.GetParameterAsText(1)
    #projectNameNew = "test"
#get the working directory and split it for the upper level path
    #Pfad anlegen
    mainPath = str(sys.path[0]).split("2_Tool")[0]

    fcPfad = os.path.join(mainPath,"1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","angelegteProjekte")
    sql = "Name = '" + projectNameNew +"'"
    x=0
    cursor = arcpy.SearchCursor(fcPfad,sql)
    for row in cursor:
        x = x+1
    if x > 0:
        print "Es scheint bereits ein Projekt mit diesem Namen zu existieren"
        arcpy.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
        print "Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox"
        arcpy.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
        sys.exit()

#copy template folder
    templatePath = os.path.join(mainPath,"3_Projekte",projectNameOld)
    projectPath = os.path.join(mainPath,"3_Projekte",projectNameNew)

    try:
        shutil.copytree(templatePath, projectPath)
    except Exception as e:
        arcpy.AddMessage(e)
        arcpy.AddMessage("Es ist ein Fehler beim Kopieren aufgetreten.")
        arcpy.AddMessage("Es scheint bereits ein Projekt mit diesem Namen zu existieren")
        arcpy.AddMessage("Bitte geben Sie einen anderen Namen ein oder nutzen Sie die 'Projekt löschen' Funktion in der Toolbox")
        sys.exit()
##rename copied files
#list all files in directory
    files = os.listdir(projectPath)
#check if filenames contain "Template"
    for file in files:
        arcpy.AddMessage(file)
        if projectNameOld in file:
            #split filename and add projectName as new filename
            newName = file.replace(projectNameOld,projectNameNew)
            filePath = os.path.join(projectPath,file)
            newFilePath = os.path.join(projectPath,newName)

            os.rename(filePath,newFilePath)

#register new project in the database
#Am Ende das erfolgreich angelegte Projekt in "FGDB_Basisdaten-deutschland.gdb/angelegteProjekte" registrieren
    arcpy.AddMessage(fcPfad)
    cursor = arcpy.InsertCursor(fcPfad)
    row = cursor.newRow()
    row.Name = projectNameNew
    cursor.insertRow(row)
    arcpy.AddMessage("Inserting")
    del row, cursor

#output information to user
    print("Succesfully copied")
    arcpy.AddMessage("Succesfully copied")
    print("New Project registered at " + projectPath)
    arcpy.AddMessage("New Project registered at " + projectPath)
except Exception as e:
    arcpy.AddMessage(e)

