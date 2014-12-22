#-------------------------------------------------------------------------------
# Name:        Integrationsgrad
# Purpose:
#
# Author:      rieffel/mayr
#
# Created:     02.08.2013
# Copyright:   (c) ILS - Institut für Landes- und Stadtentwicklungsforschung gGmbH 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import lib_oekologischeFolgen as f, arcpy, os
projekt = arcpy.GetParameterAsText(0)
GrenzeSiedlung = arcpy.GetParameterAsText(1)
GrenzeGesamt =  arcpy.GetParameterAsText(2)

wcd = os.getcwd()
rootPfad = str(sys.path[0]).split("2_Tool")[0]

flaechenPlangebiet = os.path.join(rootPfad,"3_Projekte",projekt,"FGDB_11_Definition_Projekt_" + projekt + ".gdb\Teilflaechen_Plangebiet")

ergebnis = f.IntegrationsGrad(GrenzeSiedlung,GrenzeGesamt)

integrationsgrad = ergebnis[0]
bewertung = ergebnis[1]

arcpy.AddMessage( "Integrationsgrad = " + str(integrationsgrad))
arcpy.AddMessage( "Bewertung = " + str(bewertung))

ergebnisTabelle = os.path.join(rootPfad,"3_Projekte",projekt,"FGDB_36_Flaeche_und_Oekologie_Projekt_" + projekt + ".gdb","Ergebnisse_Integrationsgrad")
#ergebnisTabelle = rootPfad + "\\3_Projekte\\" + projekt + "\\FGDB_36_Flaeche_und_Oekologie_Projekt_" + projekt + ".gdb\\Ergebnisse_Integrationsgrad"

#insert Cursor für die Ergebnistabelle erstellen
ergebnisCursor = arcpy.InsertCursor(ergebnisTabelle)
ergebnisZeile = ergebnisCursor.newRow()
ergebnisZeile.Projektname = projekt
ergebnisZeile.Integrationsgrad = integrationsgrad
ergebnisZeile.Bewertung = bewertung
ergebnisCursor.insertRow(ergebnisZeile)