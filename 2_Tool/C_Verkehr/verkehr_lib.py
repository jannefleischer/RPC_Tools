# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# verkehr_lib.py
#
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


#
# Allgemeine Funktionen
#

def uebergabepunkt_bearbeiten(projektname,punkt_name,qp_wohnen,qp_versorgung,qp_gewerbe,qp_schulen,zp_wohnen,zp_versorgung,zp_gewerbe,zp_schulen):
    import sys, os, arcpy
    print "bearbeiten"
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    workspace_projekt_verkehr = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Verkehr_'+projektname+'.gdb')
    workspace_tool_verkehr = os.path.join(base_path,"2_Tool","C_Verkehr","33_Verkehr_Tool.gdb")

    uebergabepunkt_tabelle = os.path.join(workspace_projekt_verkehr,'L01_Uebergabepunkte')

    rows = arcpy.UpdateCursor(uebergabepunkt_tabelle)

    # Update the field used in buffer so the distance is based on the road
    # type. Road type is either 1, 2, 3 or 4. Distance is in meters.
    #
    for row in rows:
        # Fields from the table can be dynamically accessed from the row object.
        #   Here fields named BUFFER_DISTANCE and ROAD_TYPE are used
        if row.Punkt_Name == punkt_name:
                row.QP_Wohnen = qp_wohnen
                row.QP_Versorgung = qp_versorgung
                row.QP_Gewerbe = qp_gewerbe
                row.QP_Schulen = qp_schulen

                row.ZP_Wohnen = zp_wohnen
                row.ZP_Versorgung = zp_versorgung
                row.ZP_Gewerbe = zp_gewerbe
                row.ZP_Schulen = zp_schulen
                rows.updateRow(row)

    # Delete cursor and row objects to remove locks on the data
    del row, rows

def get_mapquest_route(route_id,lat_start,lon_start,lat_end,lon_end,mapquest_key):

    import urllib2
    import xml.dom.minidom as dom

    try:

        mode = 'fastest' # types available: fastest, shortest, pedestrian, bicycle

        origin = str(lat_start)+','+str(lon_start)
        destination = str(lat_end)+','+str(lon_end)

        query = 'http://open.mapquestapi.com/directions/v1/route?outFormat=xml&from='+origin+'&to='+destination+'+&callback=renderNarrative&routeType='+mode+'&unit=k&shapeFormat=raw&generalize=0&key='+mapquest_key
        #arcpy.AddMessage(query)

        xml = urllib2.urlopen(query)

        baum = dom.parse(xml)

        waypoints = []

        for node in baum.getElementsByTagName('shapePoints'):

            for coordnote in node.getElementsByTagName('latLng'):
                #extract lat from end_location
                for latnode in coordnote.getElementsByTagName('lat'):
                    lat =  latnode.toxml()
                    lat = lat.replace('<lat>','')
                    lat = lat.replace('</lat>','')
                    lat = float(lat)

                for lngnode in coordnote.getElementsByTagName('lng'):
                    #extract lng from end_location
                    lon =  lngnode.toxml()
                    lon = lon.replace('<lng>','')
                    lon = lon.replace('</lng>','')
                    lon = float(lon)

                werte = (route_id,lat,lon)

                waypoints.append(werte)

    except Exception as e:
        waypoints = []

    message = "Route von Punkt "+origin+" nach "+destination

    #arcpy.AddMessage(message)

    return(waypoints)


def verkehrserzeugung_einwohner(EW,Wege_EW,MIV_Anteil,Pers_KFZ,Anteil_Besucherfahrten,WF_Fahrten_je_EW):
    fahrten_ew_tag = int((float(EW)*float(Wege_EW)*float(MIV_Anteil)*float(Pers_KFZ)))
    fahrten_besucher_tag = int((float(fahrten_ew_tag)*float(Anteil_Besucherfahrten)))
    fahrten_wf_tag = int((float(EW)*float(WF_Fahrten_je_EW)))

    return(fahrten_ew_tag,fahrten_besucher_tag,fahrten_wf_tag)

def verkehrserzeugung_einzelhandel(BGF,BGF_Beschaeftigter,Anwesenheit,Wege_Beschaeftigter,MIV_Anteil,Pers_KFZ,Besucher_Tag,Lieferwege_100m2):
    fahrten_beschaeftigte_tag = int(((float(BGF)/float(BGF_Beschaeftigter))*float(Anwesenheit)*float(Wege_Beschaeftigter)*float(MIV_Anteil))/float(Pers_KFZ))
    fahrten_kunden_tag = int(((((BGF*float(Besucher_Tag))*float(MIV_Anteil))/float(Pers_KFZ))*2))
    fahrten_wf_tag =int((BGF/100)*float(Lieferwege_100m2))

    return(fahrten_beschaeftigte_tag,fahrten_kunden_tag,fahrten_wf_tag)

def verkehrserzeugung_gewerbe(Beschaeftigte,Anwesenheit,Wege_Beschaeftigter,MIV_Anteil,Pers_KFZ,Anteil_Besucherfahrten,Lieferwege_Beschaeftigte):
    fahrten_beschaeftigte_tag = int((float(Beschaeftigte)*float(Anwesenheit)*float(Wege_Beschaeftigter)*float(MIV_Anteil)/float(Pers_KFZ)))
    fahrten_besucher_tag = int((fahrten_beschaeftigte_tag)*float(Anteil_Besucherfahrten))
    fahrten_wf_tag = int((float(Beschaeftigte)*float(Lieferwege_Beschaeftigte)))

    return(fahrten_beschaeftigte_tag,fahrten_besucher_tag,fahrten_wf_tag)

def verkehrserzeugung_schulen(Schueler,Wege_Schueler,MIV_Anteil,Schueler_KFZ,Schueler_je_Lehrer,Wege_Lehrer,Pers_KFZ,Lieferwege_Schueler):
    fahrten_schueler_tag = int((float(Schueler)*float(Wege_Schueler)*float(MIV_Anteil))/float(Schueler_KFZ))
    fahrten_lehrer_tag = int(((float(Schueler)/float(Schueler_je_Lehrer))*float(Wege_Lehrer)*float(MIV_Anteil)/float(Pers_KFZ)))
    fahrten_wf_tag = int((float(Schueler)*float(Lieferwege_Schueler)))

    return(fahrten_schueler_tag,fahrten_lehrer_tag,fahrten_wf_tag)