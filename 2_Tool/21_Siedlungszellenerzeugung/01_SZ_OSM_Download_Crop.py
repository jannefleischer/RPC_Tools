# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 01_SZ_Download.py
#
# Description: Erkenne Bundesland des Untersuchungsprojektes und lade entsprechende OSM-Dateien von der Geofabrik
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
# Import arcpy modules
import os
import shutil
import gc
import zipfile
import urllib
import sys

import arcpy


gc.collect()

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)
#projektname = 'Biesfeld-West' # haendische Ueberbrueckung bei manueller Scriptnutzung

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_basis = os.path.join(base_path, '1_Basisdaten', 'FGBD_01_Basisdaten_deutschland.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_11_Definition_Projekt_' + projektname + '.gdb')
workspace_siedlungszellen = os.path.join(base_path, '3_Projekte', projektname,
                                         'FGDB_21_Siedlungszellen_' + projektname + '.gdb')

#Aktuelles Verzeichnis bestimmen
wcd = os.path.dirname(os.path.realpath(__file__))

#############################################################################################################
# Schritt 1 - erkennen, in welchem Bundesland und Kreis das Projekt liegt
schrittmeldung = 'Ermittle Bundesland \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Variablen
gemeindelayer = os.path.join(workspace_basis, 'bkg_gemeinden')
teilflaechen_plangebiet = os.path.join(workspace_projekt, 'teilflaechen_plangebiet')
gemeinden_untersuchung = os.path.join(workspace_projekt, 'untersuchungsgemeinde')

arcpy.MakeFeatureLayer_management(gemeindelayer, "gemeindelayer_lyr")
arcpy.MakeFeatureLayer_management(teilflaechen_plangebiet, "teilflaechen_plangebiet_lyr")

# Process: Layer lagebezogen auswählen
arcpy.SelectLayerByLocation_management("gemeindelayer_lyr", "INTERSECT", "teilflaechen_plangebiet_lyr", "",
                                       "NEW_SELECTION")

# Process: Features kopieren
arcpy.CopyFeatures_management("gemeindelayer_lyr", gemeinden_untersuchung, "", "0", "0", "0")

# Landesschluessel auslesen
rows = arcpy.SearchCursor(gemeinden_untersuchung)

for row in rows:
    statecode = row.AGS[:2]

statelist = [('schleswig-holstein', '01'),
             ('hamburg', '02'),
             ('niedersachsen', '03'),
             ('bremen', '04'),
             ('nordrhein-westfalen', '05'),
             ('hessen', '06'),
             ('rheinland-pfalz', '07'),
             ('baden-wuerttemberg', '08'),
             ('bayern', '09'),
             ('saarland', '10'),
             ('berlin', '11'),
             ('brandenburg', '12'),
             ('mecklenburg-vorpommern', '13'),
             ('sachsen', '14'),
             ('sachsen-anhalt', '15'),
             ('thueringen', '16'),
]

for s in statelist:
    if s[1] == statecode:
        state = s[0]
        state_path = state.replace('-',
                                   '_')  #bundeslaender mit bindestrichen verursachen spaeter probleme bei der pfaderstellung
        county = ''
        city = ''

statusmeldung = 'Untersuchungsgebiet liegt in ' + state.capitalize() + '\n'
arcpy.AddMessage(statusmeldung)
print statusmeldung

#############################################################################################################
# Schritt 2 - Ueberpruefung, ob die Daten schon downgeloaded wurden
schrittmeldung = 'Ermittle, ob OSM-Daten bereits vorliegen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

filename_url = state + '-latest.shp.zip'
filename_rpc = state_path + '.zip'

try:
    directory = os.path.join(base_path, '1_Basisdaten', 'OSM_' + state_path)
    downloadpath = os.path.join(directory, filename_rpc)

    with open(downloadpath):
        statusmeldung = 'OSM-Daten sind bereits geladen\n'
        arcpy.AddMessage(statusmeldung)
        print statusmeldung

except IOError:
    statusmeldung = 'Download der Geodaten von OSM notwendig - Vorgang kann einige Minuten dauern \n'
    arcpy.AddMessage(statusmeldung)
    print statusmeldung

    baseurl = 'http://download.geofabrik.de/europe/germany/'

    try:
        directory = os.path.join(base_path, '1_Basisdaten', 'OSM_' + state_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

    except Exception as e:
        print e
        arcpy.AddMessage(e)

    downloadurl = baseurl + filename_url


    #generate Downloadpath
    downloadpath = os.path.join(directory, filename_rpc)

    try:
        urllib.urlretrieve(downloadurl, downloadpath)
    except Exception as e:
        arcpy.AddMessage(e)


#############################################################################################################
#Schritt 3 - Entzippen der Daten
schrittmeldung = 'Dateien werden entpackt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

fh = open(downloadpath, 'rb')
z = zipfile.ZipFile(fh)
extractpath = os.path.join(base_path, "1_Basisdaten", "OSM_" + state_path, "data")
z.extractall(path=extractpath)

#############################################################################################################
#Schritt 4 - Import der Shapefiles in FGBD_01_Basisdaten_deutschland.gdb
schrittmeldung = 'Import der Shapefiles in FGBD_01_Basisdaten_deutschland.gdb \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

roads_shp = os.path.join(base_path, "1_Basisdaten", "OSM_" + state_path, "data", "roads.shp")
railways_shp = os.path.join(base_path, "1_Basisdaten", "OSM_" + state_path, "data", "railways.shp")

importlist = [roads_shp, railways_shp]

for shp in importlist:
    exportname = shp.split('data')[1].replace('.shp', '').replace('\\', '')
    layername = ('OSM_' + state_path + '_' + exportname).replace('\\', '')
    exportpath = os.path.join(workspace_basis, layername)

    if arcpy.Exists(exportpath):
        print exportpath + ' existiert bereits und wird nicht neu angelegt'
        print "\n"
    else:
        arcpy.CopyFeatures_management(shp, exportpath, "", "0", "0", "0")


#############################################################################################################
#Schritt 5 - Zuschneiden der eingeladenen Daten auf Gemeinde + 10km Umring
schrittmeldung = 'Zuschneiden der eingeladenen Daten auf Gemeinde + 10km Umring und Import in Projektverzeichnis\n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

roads_gdb = os.path.join(workspace_basis, "OSM_" + state_path + "_roads")
railways_gdb = os.path.join(workspace_basis, "OSM_" + state_path + "_railways")

selectionlist = [roads_gdb, railways_gdb]

try:
    for shape in selectionlist:
        print shape
        import_lyr = arcpy.MakeFeatureLayer_management(shape, "import_lyr")

        featurename = shape.replace(workspace_basis, '').replace(state_path, '').replace('__', '_')
        exportfeature = workspace_siedlungszellen + featurename
        #print exportfeature
        arcpy.SelectLayerByLocation_management(import_lyr, "WITHIN_A_DISTANCE", teilflaechen_plangebiet,
                                               "20 Kilometers", "NEW_SELECTION")
        #print 'Selektion abgeschlossen'
        arcpy.CopyFeatures_management(import_lyr, exportfeature, "", "0", "0", "0")
        #print 'ausschnitt kopiert'

        del import_lyr, exportfeature, featurename
except Exception as e:
    schrittmeldung = e
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

#############################################################################################################
#Schritt 6 - loeschen der temporaeren OSM-Files
schrittmeldung = 'Loeschen der temporaeren OSM-Files \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

try:
    shutil.rmtree(os.path.join(base_path, "1_Basisdaten", 'OSM_' + state_path, 'data'))
except:
    pass

print 'fertig'
arcpy.AddMessage('fertig')