__author__ = 'Rieffel'
import  sys, os, arcpy
import komponentenmodell_lib as k


projektname = arcpy.GetParameterAsText(0)
#projektname = "Testlauf_1"

ags = k.ags_extrahieren(projektname)
#ags = '03353005'
jahr = "2011"
geschlecht = "gesm"
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Download der Bevoelkerungsdaten")
ags = k.bevdaten_download(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Download der Wanderungsdaten")
k.wanderungsdaten_download(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Dissagregation der Wanderungsdaten")
k.wanderungsdaten_dissaggegieren(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Berechnung der Wanderungsraten")
k.wanderungsraten_berechnen(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Berechung der Bevoelkerungsprognose")
endjahr = int(jahr)+40
startjahr = int(jahr)
arcpy.AddMessage( "Start:" + str(startjahr) + "| Ende: " + str(endjahr))
while startjahr <= endjahr:
    arcpy.AddMessage( startjahr)
    k.bevoelkerungsprognose(projektname, ags, startjahr, geschlecht)
    k.prognoseEinrechnen(projektname,ags, geschlecht,startjahr)
    #ToDo: Salden Fuer Planfall einberechnen
    startjahr = int(startjahr)+1

#
geschlecht = "gesw"
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Download der Bevoelkerungsdaten")
k.bevdaten_download(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Download der Wanderungsdaten")
k.wanderungsdaten_download(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Dissagregation der Wanderungsdaten")
k.wanderungsdaten_dissaggegieren(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Berechnung der Wanderungsraten")
k.wanderungsraten_berechnen(projektname,ags,jahr,geschlecht)
arcpy.AddMessage("*******************************************************************")
arcpy.AddMessage( "Berechung der Bevoelkerungsprognose")
endjahr = int(jahr) + 40
startjahr = int(jahr)
arcpy.AddMessage( "Start:" + str(startjahr) + "| Ende: " + str(endjahr))
while startjahr <= endjahr:
    arcpy.AddMessage( startjahr)
    k.bevoelkerungsprognose(projektname, ags, startjahr, geschlecht)
    k.prognoseEinrechnen(projektname,ags, geschlecht,startjahr)
    startjahr = int(startjahr) +1


