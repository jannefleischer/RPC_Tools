# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 10_Kostenmodell.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import arcpy, os, sys

def main():
    arcpy.env.overwriteOutput = True


    # Variablen definieren
    i=-1
    i+=1;projektname = arcpy.GetParameterAsText(i)
    i+=1;teilflaeche = arcpy.GetParameterAsText(i)
    i+=1;startjahr = arcpy.GetParameterAsText(i)

    i+=1;verkehrsflaeche = int(arcpy.GetParameterAsText(i))
    i+=1;gruenflaeche = int(arcpy.GetParameterAsText(i))
    i+=1;sonst_flaechen = int(arcpy.GetParameterAsText(i))
    i+=1;nettobauland = int(arcpy.GetParameterAsText(i))

    i+=1;gewerbeflaeche = int(arcpy.GetParameterAsText(i))
    i+=1;nettowohnbauland = int(arcpy.GetParameterAsText(i))

    i+=1;laermschutz = int(arcpy.GetParameterAsText(i))
    i+=1;privatwege = int(arcpy.GetParameterAsText(i))
    i+=1;aeussere_erschliessung = int(arcpy.GetParameterAsText(i))
    i+=1;innere_erschliessung = int(arcpy.GetParameterAsText(i))

    i+=1;spielplatz = int(arcpy.GetParameterAsText(i))
    i+=1;strassenbegleitgruen = int(arcpy.GetParameterAsText(i))
    i+=1;ausgleich = int(arcpy.GetParameterAsText(i))
    i+=1;allg_gruenflaeche = int(arcpy.GetParameterAsText(i))

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
    teilflaechen = os.path.join(workspace_projekt_definition,'Teilflaechen_Plangebiet')
    flaechenbilanz = os.path.join(workspace_projekt_definition,'Flaechenbilanz')

    # Suche Größe der aktuellen Teilfläche heraus
    with arcpy.da.SearchCursor(teilflaechen, ['Name', 'Flaeche_ha']) as cursor:
        for row in cursor:
            if row[0] == teilflaeche:
                flaeche = float(row[1])

    # Lösche bisherige Eingaben für gewählte Teilfläche
    with arcpy.da.UpdateCursor(flaechenbilanz, "Teilflaeche_Plangebiet") as cursor:
        for row in cursor:
            if row[0] == teilflaeche:
                cursor.deleteRow()

    # Füge neue Eingaben für gewählte Teilfläche ein
    fields = ['Teilflaeche_Plangebiet', 'Startjahr', 'Flaechennutzung_S1', 'Flaechennutzung_S2', 'Anteil_S1', 'Anteil_S2', 'Flaeche_ha']
    cursor = arcpy.da.InsertCursor(flaechenbilanz, fields)

    cursor.insertRow((teilflaeche,startjahr,'Nettobauland','Nettowohnbauland',nettobauland,nettowohnbauland, flaeche * nettobauland / 100 * nettowohnbauland / 100))
    cursor.insertRow((teilflaeche,startjahr,'Nettobauland','Gewerbeflaeche',nettobauland,gewerbeflaeche, flaeche * nettobauland / 100 * gewerbeflaeche / 100))

    cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Laermschutzanlagen',verkehrsflaeche,laermschutz,flaeche * verkehrsflaeche / 100 * laermschutz / 100))
    cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Privat - Innere Erschliessung',verkehrsflaeche,privatwege,flaeche * verkehrsflaeche / 100 * privatwege / 100))
    cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Oeffentlich - Aeussere Erschliessung',verkehrsflaeche,aeussere_erschliessung,flaeche * verkehrsflaeche / 100 * aeussere_erschliessung / 100))
    cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Oeffentlich - Innere Erschliessung',verkehrsflaeche,innere_erschliessung,flaeche * verkehrsflaeche / 100 * innere_erschliessung / 100))

    cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Spielplaetze',gruenflaeche,spielplatz,flaeche * gruenflaeche / 100 * spielplatz / 100))
    cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Strassenbegleitgruen',gruenflaeche,strassenbegleitgruen,flaeche * gruenflaeche / 100 * strassenbegleitgruen / 100))
    cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Ausgleichs- und Ersatzflaechen',gruenflaeche,ausgleich,flaeche * gruenflaeche / 100 * ausgleich / 100))
    cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Allgemeine Gruenflaechen',gruenflaeche,allg_gruenflaeche,flaeche * gruenflaeche / 100 * allg_gruenflaeche / 100))

    cursor.insertRow((teilflaeche,startjahr,'Sonstige Flaechen','Sonstige Flaechen',sonst_flaechen,sonst_flaechen,flaeche* sonst_flaechen / 100))

if __name__ == "__main__":
    main()
