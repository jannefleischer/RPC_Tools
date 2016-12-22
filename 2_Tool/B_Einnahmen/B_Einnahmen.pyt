# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy

def set_parameter_as_text(params, index, val):
    if (hasattr(params[index].value, 'value')):
        params[index].value.value = val
    else:
        params[index].value = val

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx

class Toolbox(object):
    def __init__(self):
        self.label = u'32_Einnahmen'
        self.alias = ''
        self.tools = [Tool30b41bb0, KFA, Einkommensteuer, Familienleistungsausgleich, Grundsteuer, Gewerbesteuer, KRU]

# Tool implementation code

class Tool30b41bb0(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\AuswirkungsabschätzungUmland"""
    import arcpy
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
    
        i=0
    
        heading1 = "01 Nettozuzugsquoten (in %)"
        i+=1 ; self.params[i].category = heading1 
        i+=1 ; self.params[i].category = heading1 
    
        heading2 = "02 Einzugsbereich (in km)"
        i+=1 ; self.params[i].category = heading2 
        i+=1 ; self.params[i].category = heading2 
    
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'1 Vorberechnungen'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        # Nettozuzugsquote_Einwohner
        param_2 = arcpy.Parameter()
        param_2.name = u'Nettozuzugsquote_Einwohner'
        param_2.displayName = u'Nettozuzugsquote Einwohner'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'50'

        # Nettozuzugsquote_Arbeitsplätze
        param_3 = arcpy.Parameter()
        param_3.name = u'Nettozuzugsquote_Arbeitspl\xe4tze'
        param_3.displayName = u'Nettozuzugsquote Arbeitspl\xe4tze'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'50'

        # Einzugsbereich_Einwohner
        param_4 = arcpy.Parameter()
        param_4.name = u'Einzugsbereich_Einwohner'
        param_4.displayName = u'Einzugsbereich Einwohner'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'25'

        # Einzugsbereich_Arbeitsplätze
        param_5 = arcpy.Parameter()
        param_5.name = u'Einzugsbereich_Arbeitspl\xe4tze'
        param_5.displayName = u'Einzugsbereich Arbeitspl\xe4tze'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'25'

        return [param_1, param_2, param_3, param_4, param_5]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\1_Vorberechnungen.py'):
            # -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 01_Auswirkung_Umland.py
            #
            # Description: Erstellung der regionalen Auswirkungsabschätzung für das zu untersuchende Projekt
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            #############################################################################################################
            #
            # Funktionen
            #
            #############################################################################################################
            
            def getAGS(projektname):
                import arcpy,sys,os
                base_path = str(sys.path[0]).split("2_Tool")[0]
                projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
                bkg_gemeinden = os.path.join( base_path, "1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","bkg_gemeinden")
                #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
                #1. Feature Layer aus den bkg-daten erstellen
                try:
                    arcpy.Delete_management("bkg_gemeinden_lyr")
                except:
                    print""
                arcpy.MakeFeatureLayer_management(bkg_gemeinden,"bkg_gemeinden_lyr")
                #2.Spatial Select wo Planfläche vgm_lyr intersected
                arcpy.SelectLayerByLocation_management("bkg_gemeinden_lyr", "INTERSECT", projektFlaeche)
                #Wenn Flaeche = 1, ags extrahieren
                n = arcpy.GetCount_management("bkg_gemeinden_lyr").getOutput(0)
                print n
            
                if(int(n) == 1 ):
                    gemeindeCursor = arcpy.SearchCursor("bkg_gemeinden_lyr")
                    for gemeinde in gemeindeCursor:
                        verbandsgemeinde = gemeinde.BEMERK
                        ags = gemeinde.AGS
                        RS = gemeinde.RS
            
                else:
                    messages.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
                    ## TODO Dateien loeschen und Projektregistrierung loeschen)
                    sys.exit()
            
                #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
                if verbandsgemeinde[0:3] != "gem":
                    ags_vg = ""
                    ags_regenesis = ags
            
                elif ags[0:2] == "03": #Niedersachsen
                    print "NS"
                    ags_vg = RS[0:5] + RS[9:]
                    ags_regenesis = RS[0:5] + RS[6] + RS[7:]
                    messages.AddMessage(ags_vg)
            
            
                elif ags[0:2] == "07": #Rheinland-Pfalz
                    print "RP"
                    ags_vg = RS[0:5] + RS[7:9]
                    ags_regenesis = RS[0:5] + RS[7:]
                    messages.AddMessage(ags_vg)
            
                return ags, ags_vg, ags_regenesis
            
            
            def getReGenesisAGS(ags_input):
                #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_input + "'"
            
                ags_vg = ""
                ags_regenesis = ags
            
                #Rheinland-Pfalz
                if ags[0:2] == "07":
            
                    if verbandsgemeinde[0:3] == "kre":
                        ags_vg = ""
                        ags_regenesis = ags
            
                    elif verbandsgemeinde[0:3] == "gem":
                        rows = arcpy.SearchCursor(VG250, where)
                        for row in rows:
                            ags_vg = row.SN_L + row.SN_R + row.SN_K + row.SN_V2
                            ags_regenesis = ags_vg
            
                    else:
                        rows = arcpy.SearchCursor(VG250, where)
                        for row in rows:
                            ags_vg = row.SN_L + row.SN_R + row.SN_K + "00" + row.SN_G
                            ags_regenesis = ags_vg
            
                #Niedersachsen
                elif ags[0:2] == "03":
            
                    if verbandsgemeinde[0:3] == "kre":
                        ags_vg = ""
                        ags_regenesis = ags
            
                    elif verbandsgemeinde[0:3] == "gem":
                        rows = arcpy.SearchCursor(VG250, where)
                        for row in rows:
                            ags_vg = RS[0:5] + RS[6] + RS[7:9]
                            ags_regenesis = ags_vg
            
                    else:
                        ags_vg = ""
                        ags_regenesis = ags
            
                return ags_input, ags_vg, ags_regenesis
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import modules
            import os
            import gc
            import sys
            import imp
            
            import arcpy
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            poplibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','population_lib.py'))
            pop = imp.load_source('population_lib', poplibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            nettoZuzugsQuote_EW = parameters[1].valueAsText
            nettoZuzugsQuote_AP = parameters[2].valueAsText
            einzugsbereich_EW = parameters[3].valueAsText
            einzugsbereich_AP = parameters[4].valueAsText
            
            # Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            #############################################################################################################
            #
            # Durchlauf Auswirkungen im Umland
            #
            #############################################################################################################
            beginmeldung = '\nDurchlauf Auswirkungen im Umland \n'
            messages.AddMessage(beginmeldung)
            print beginmeldung
            
            #############################################################################################################
            # Einwohnerzahl erzeugen
            pop.recalcPopulation(projektname)
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Ermittle AGS der Kommune \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            ags_eigen = getAGS(projektname)[0]
            ags_vg_eigen = getAGS(projektname)[1]
            ags_regenesis_eigen = getAGS(projektname)[2]
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Ermittle Kommunen im definierten Umkreis \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            inputGemeinden = os.path.join(workspace_basisdaten, 'bkg_gemeinden')
            gemeindenAuswirkungenAP = os.path.join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumAP')
            gemeindenAuswirkungenEW = os.path.join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumEW')
            projektflaechen = os.path.join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
            
            arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")
            arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")
            
            # Process: Layer lagebezogen auswählen
            arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")
            arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")
            
            umkreis_km = str(einzugsbereich_EW) + " Kilometers"
            arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
            arcpy.CopyFeatures_management("gemeinden_lyr", gemeindenAuswirkungenEW)
            
            # Process: Layer lagebezogen auswählen
            arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")
            arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")
            
            umkreis_km = str(einzugsbereich_AP) + " Kilometers"
            arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
            arcpy.CopyFeatures_management("gemeinden_lyr", gemeindenAuswirkungenAP)
            
            
            #############################################################################################################
            # Schritt 2
            schrittmeldung = 'Punktlayer aus Planflaechen erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Create Centroid Layer
            try:
                arcpy.DeleteFeatures_management(Teilflaechen_Plangebiet_Centroide)
            except Exception as e:
                print e
            
            arcpy.env.overwriteOutput = True
            arcpy.CreateFeatureclass_management(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide", "POINT", "", "DISABLED", "DISABLED", projektflaechen, "", "0", "0", "0")
            
            # Create search cursor
            polygon_rows = arcpy.SearchCursor(projektflaechen)
            shapeName = arcpy.Describe(projektflaechen).shapeFieldName
            
            centroid_rows = arcpy.InsertCursor(Teilflaechen_Plangebiet_Centroide)
            
            for polygon_row in polygon_rows:
                feat = polygon_row.getValue(shapeName)
            
                latValue = str(feat.trueCentroid).split(' ')[1]
                lonValue = str(feat.trueCentroid).split(' ')[0]
            
                #print latValue, lonValue
            
                vertex = arcpy.CreateObject("Point")
                vertex.X = lonValue
                vertex.Y = latValue
            
                feature = centroid_rows.newRow()
                feature.shape = vertex
                centroid_rows.insertRow(feature)
            
            del centroid_rows
            del polygon_row
            del polygon_rows
            
            try:
                arcpy.DeleteFeatures_management(Teilflaechen_Plangebiet_CentroideGK3)
            except Exception as e:
                print e
            
            arcpy.Project_management(Teilflaechen_Plangebiet_Centroide, Teilflaechen_Plangebiet_CentroideGK3, "PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "DHDN_To_WGS_1984_5x", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
            arcpy.AddXY_management(Teilflaechen_Plangebiet_CentroideGK3)
            
            # Mittelpunkt der Teilflaechen ermitteln
            mw_y = []
            mw_x = []
            
            polygon_rows = arcpy.SearchCursor(Teilflaechen_Plangebiet_CentroideGK3)
            
            for polygon_row in polygon_rows:
                mw_x.append(polygon_row.POINT_X)
                mw_y.append(polygon_row.POINT_Y)
            
            mw_x = sum(mw_x)/len(mw_x)
            mw_y = sum(mw_y)/len(mw_y)
            
            
            #############################################################################################################
            # Schritt 3
            schrittmeldung = 'Punktlayer aus Umkreiskommunen (EW) erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Process: Feature-Class erstellen
            try:
                arcpy.DeleteFeatures_management(gemeindenWirkraumEW_Centroide)
            except Exception as e:
                print e
            
            gemeindenWirkraumEW = os.path.join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumEW')
            arcpy.CreateFeatureclass_management(workspace_projekt_definition, "gemeindenWirkraumEW_Centroide", "POINT", "", "DISABLED", "DISABLED", gemeindenWirkraumEW, "", "0", "0", "0")
            
            # Add new fields
            fieldName = "AGS"
            fieldAlias = "AGS"
            arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            fieldName = "AGS_VG"
            fieldAlias = "AGS_VG"
            arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            fieldName = "AGS_Regenesis"
            fieldAlias = "AGS_Regenesis"
            arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            # Create search cursor
            polygon_rows = arcpy.SearchCursor(gemeindenWirkraumEW)
            shapeName = arcpy.Describe(gemeindenWirkraumEW).shapeFieldName
            
            centroid_rows = arcpy.InsertCursor(gemeindenWirkraumEW_Centroide)
            
            for polygon_row in polygon_rows:
                feat = polygon_row.getValue(shapeName)
                ags = polygon_row.AGS
                verbandsgemeinde = polygon_row.BEMERK
                RS = polygon_row.RS
            
                ags_vg = getReGenesisAGS(ags)[1]
                ags_regenesis = getReGenesisAGS(ags)[2]
            
                messages.AddMessage(ags)
                messages.AddMessage(ags_regenesis)
            
                latValue = str(feat.trueCentroid).split(' ')[1]
                lonValue = str(feat.trueCentroid).split(' ')[0]
            
                #print latValue, lonValue
            
                vertex = arcpy.CreateObject("Point")
                vertex.X = lonValue
                vertex.Y = latValue
            
                feature = centroid_rows.newRow()
                feature.shape = vertex
                feature.AGS = ags
                feature.AGS_VG = ags_vg
                feature.AGS_Regenesis = ags_regenesis
                centroid_rows.insertRow(feature)
            
            del centroid_rows
            del polygon_row
            del polygon_rows
            
            arcpy.AddXY_management(gemeindenWirkraumEW_Centroide)
            
            schrittmeldung = '\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Punktlayer aus Umkreiskommunen (AP) erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Process: Feature-Class erstellen
            try:
                arcpy.DeleteFeatures_management(gemeindenWirkraumAP_Centroide)
            except Exception as e:
                print e
            
            gemeindenWirkraumAP = os.path.join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumAP')
            arcpy.CreateFeatureclass_management(workspace_projekt_definition, "gemeindenWirkraumAP_Centroide", "POINT", "", "DISABLED", "DISABLED", gemeindenWirkraumAP, "", "0", "0", "0")
            
            # Add new fields
            fieldName = "AGS"
            fieldAlias = "AGS"
            arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            fieldName = "AGS_VG"
            fieldAlias = "AGS_VG"
            arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            fieldName = "AGS_Regenesis"
            fieldAlias = "AGS_Regenesis"
            arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
            arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")
            
            # Create search cursor
            polygon_rows = arcpy.SearchCursor(gemeindenWirkraumAP)
            shapeName = arcpy.Describe(gemeindenWirkraumAP).shapeFieldName
            
            centroid_rows = arcpy.InsertCursor(gemeindenWirkraumAP_Centroide)
            
            for polygon_row in polygon_rows:
                feat = polygon_row.getValue(shapeName)
                ags = polygon_row.AGS
                verbandsgemeinde = polygon_row.BEMERK
                RS = polygon_row.RS
            
                ags_vg = getReGenesisAGS(ags)[1]
                ags_regenesis = getReGenesisAGS(ags)[2]
            
                messages.AddMessage(ags)
                messages.AddMessage(ags_regenesis)
            
                latValue = str(feat.trueCentroid).split(' ')[1]
                lonValue = str(feat.trueCentroid).split(' ')[0]
            
                #print latValue, lonValue
            
                vertex = arcpy.CreateObject("Point")
                vertex.X = lonValue
                vertex.Y = latValue
            
                feature = centroid_rows.newRow()
                feature.shape = vertex
                feature.AGS = ags
                feature.AGS_VG = ags_vg
                feature.AGS_Regenesis = ags_regenesis
                centroid_rows.insertRow(feature)
            
            del centroid_rows
            del polygon_row
            del polygon_rows
            
            arcpy.AddXY_management(gemeindenWirkraumAP_Centroide)
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = '\nErzeuge Entfernungstabelle Einwohner \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_definition,'gemeindenWirkraumEW_Centroide'),
                (workspace_projekt_einnahmen,'AWU_gemeindenWirkraumEW')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_DistanzenEW')
            
            sql = """SELECT gemeindenWirkraumEW_Centroide.AGS, gemeindenWirkraumEW_Centroide.AGS_VG, gemeindenWirkraumEW_Centroide.AGS_Regenesis, (([POINT_X]-mw_x)^2+([point_Y]-mw_y)^2)^(1/2) AS distanz, AWU_gemeindenWirkraumEW.EWZ INTO AWU_DistanzenEW
            FROM gemeindenWirkraumEW_Centroide INNER JOIN AWU_gemeindenWirkraumEW ON gemeindenWirkraumEW_Centroide.AGS = AWU_gemeindenWirkraumEW.AGS
            WHERE (((gemeindenWirkraumEW_Centroide.AGS)<>'AGSVALUE'));
            """
            
            sql = sql.replace("mw_x",str(mw_x)).replace("mw_y",str(mw_y)).replace("AGSVALUE",str(ags_eigen))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 3
            schrittmeldung = 'Erzeuge Entfernungstabelle Arbeitsplaetze \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_definition,'gemeindenWirkraumAP_Centroide'),
                (workspace_projekt_einnahmen,'AWU_gemeindenWirkraumAP')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_DistanzenAP')
            
            sql = """
            SELECT gemeindenWirkraumAP_Centroide.AGS, gemeindenWirkraumAP_Centroide.AGS_VG, gemeindenWirkraumAP_Centroide.AGS_Regenesis, (([POINT_X]-mw_x)^2+([point_Y]-mw_y)^2)^(1/2) AS distanz, AWU_gemeindenWirkraumAP.EWZ INTO AWU_DistanzenAP
            FROM gemeindenWirkraumAP_Centroide INNER JOIN AWU_gemeindenWirkraumAP ON gemeindenWirkraumAP_Centroide.AGS = AWU_gemeindenWirkraumAP.AGS
            WHERE (((gemeindenWirkraumAP_Centroide.AGS)<>'AGSVALUE'));
            """
            
            sql = sql.replace("mw_x",str(mw_x)).replace("mw_y",str(mw_y)).replace("AGSVALUE",str(ags_eigen))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Berechne EW-Anteile entsprechend der Einwohnerzahl \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Maximale Distanz EW ermitteln
            maxlist = []
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'AWU_DistanzenEW')
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                maxlist.append(row.distanz)
            
            try:
                distEW_max = max(maxlist)
            except:
                distEW_max = 0
            
            # EWgewichtet erzeugen
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_DistanzenEW')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_EWgewichtet')
            
            sql = """SELECT AWU_DistanzenEW.AGS, AWU_DistanzenEW.AGS_VG, AWU_DistanzenEW.AGS_Regenesis, AWU_DistanzenEW.distanz, AWU_DistanzenEW.EWZ, 1-[distanz]/distEW_max AS Faktor, (1-[distanz]/distEW_max)*[EWZ] AS AWU_EWgewichtet INTO AWU_EWgewichtet
            FROM AWU_DistanzenEW;
            """
            
            sql = sql.replace("distEW_max",str(distEW_max))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Summe EW ermitteln
            sumlist = []
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'AWU_EWgewichtet')
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                sumlist.append(row.AWU_EWgewichtet)
            sumEW = sum(sumlist)
            
            # Erzeuge Wanderungsfaktor
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_EWgewichtet')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
            
            nettoZuzugsQuote_EW = str(float(nettoZuzugsQuote_EW)/100)
            
            sql = """SELECT AWU_EWgewichtet.AGS, AWU_EWgewichtet.AGS_VG, AWU_EWgewichtet.AGS_Regenesis, ([AWU_EWgewichtet]/sumEW)*(nettoZuzugsQuote_EW) AS AWU_Wanderungsfaktor INTO AWU_WanderungsfaktorEW
            FROM AWU_EWgewichtet;
            """
            
            sql = sql.replace("sumEW",str(sumEW)).replace("nettoZuzugsQuote_EW",str(nettoZuzugsQuote_EW))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Ergaenze AGS der eigenen Kommune
            input = os.path.join(workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
            rows = arcpy.InsertCursor(input)
            row = rows.newRow()
            row.AGS = ags_eigen
            row.AGS_VG = ags_vg_eigen
            row.AGS_Regenesis = ags_regenesis_eigen
            row.AWU_Wanderungsfaktor = float(nettoZuzugsQuote_EW)
            rows.insertRow(row)
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Berechne AP-Anteile entsprechend der Arbeitsplatzverteilung \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Maximale Distanz AP ermitteln
            maxlist = []
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'AWU_DistanzenAP')
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                maxlist.append(row.distanz)
            
            try:
                distAP_max = max(maxlist)
            except:
                distAP_max = 0
            
            # EWgewichtet erzeugen
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_DistanzenAP')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_APgewichtet')
            
            sql = """SELECT AWU_DistanzenAP.AGS, AWU_DistanzenAP.AGS_VG, AWU_DistanzenAP.AGS_Regenesis, AWU_DistanzenAP.distanz, AWU_DistanzenAP.EWZ, 1-[distanz]/distAP_max AS Faktor, (1-[distanz]/distAP_max)*[EWZ] AS AWU_APgewichtet INTO AWU_APgewichtet
            FROM AWU_DistanzenAP;
            """
            
            sql = sql.replace("distAP_max",str(distAP_max))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Summe EW ermitteln
            sumlist = []
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'AWU_APgewichtet')
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                sumlist.append(row.AWU_APgewichtet)
            sumAP = sum(sumlist)
            
            # Erzeuge Wanderungsfaktor
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_APgewichtet')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
            
            nettoZuzugsQuote_AP = str(float(nettoZuzugsQuote_AP)/100)
            
            sql = """SELECT AWU_APgewichtet.AGS, AWU_APgewichtet.AGS_VG, AWU_APgewichtet.AGS_Regenesis, ([AWU_APgewichtet]/sumAP)*(nettoZuzugsQuote_AP) AS AWU_Wanderungsfaktor INTO AWU_WanderungsfaktorAP
            FROM AWU_APgewichtet;
            """
            
            sql = sql.replace("sumAP",str(sumAP)).replace("nettoZuzugsQuote_AP",str(nettoZuzugsQuote_AP))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Ergaenze AGS der eigenen Kommune
            input = os.path.join(workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
            rows = arcpy.InsertCursor(input)
            row = rows.newRow()
            row.AGS = ags_eigen
            row.AGS_VG = ags_vg_eigen
            row.AGS_Regenesis = ags_regenesis_eigen
            row.AWU_Wanderungsfaktor = float(nettoZuzugsQuote_AP)
            rows.insertRow(row)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Verteilung der EW auf Gemeinden \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW'),
                (workspace_projekt_definition,'Einwohnerzahl')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsergebnisEW')
            
            sql = """SELECT AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr, Sum([Einwohnerzahl]*[AWU_Wanderungsfaktor]) AS EW INTO AWU_WanderungsergebnisEW
            FROM Einwohnerzahl, AWU_WanderungsfaktorEW
            GROUP BY AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr
            ORDER BY AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Verteilung der AP auf Gemeinden \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP'),
                (workspace_projekt_definition,'Gewerbe_Beschaeftigte')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsergebnisAP')
            
            sql = """SELECT AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche, Sum([Anzahl]*[AWU_Wanderungsfaktor]) AS AP INTO AWU_WanderungsergebnisAP
            FROM Gewerbe_Beschaeftigte, AWU_WanderungsfaktorAP
            GROUP BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche
            ORDER BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList_a = ['gemeindenWirkraumAP','gemeindenWirkraumEW','gemeindenWirkraumAP_Centroide','gemeindenWirkraumEW_Centroide','Teilflaechen_Plangebiet_CentroideGK3']
            deleteList_b = ['AWU_APgewichtet','AWU_EWgewichtet','AWU_DistanzenAP','AWU_DistanzenEW']
            
            for e in deleteList_a:
                f = os.path.join(workspace_projekt_definition,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            for e in deleteList_b:
                f = os.path.join(workspace_projekt_einnahmen,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('01_Auswirkung_Umland abgeschlossen')

class KFA(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\KFA"""
    import arcpy
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'6 Kommunaler Finanzausgleich'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        return [param_1]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\6_KFA.py'):
            ﻿# -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 32_KFA_01.py
            #
            # Description: Berechnung des Kommunalen Finanzausgleichs für das zu untersuchende Projekt
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # ILS / GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            
            # Import arcpy modules
            import os
            import gc
            import sys
            import imp
            import arcpy
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            #projektname = 'HCU_LKH_Brackel'
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            
            projektRahmendaten = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Projektrahmendaten")
            projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
            kfa_01_jaehrlich = os.path.join(workspace_projekt_einnahmen, "KFA_01_Jahresdaten")
            kfa_02_statisch = os.path.join(workspace_projekt_einnahmen, "KFA_02_Statische_Daten")
            projektBevoelkerung = os.path.join(projektRahmendaten, "Einwohnerzahl")
            
            
            
            #############################################################################################################
            #Funktionen
            
            def getAGS(projektname):
                import arcpy,sys,os
                base_path = str(sys.path[0]).split("2_Tool")[0]
                projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
                bkg_gemeinden = os.path.join( base_path, "1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","bkg_gemeinden")
                #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
                #1. Feature Layer aus den bkg-daten erstellen
                try:
                    arcpy.Delete_management("bkg_gemeinden_lyr")
                except:
                    print""
                arcpy.MakeFeatureLayer_management(bkg_gemeinden,"bkg_gemeinden_lyr")
                #2.Spatial Select wo Planfläche vgm_lyr intersected
                arcpy.SelectLayerByLocation_management("bkg_gemeinden_lyr", "INTERSECT", projektFlaeche)
                #Wenn Flaeche = 1, ags extrahieren
                n = arcpy.GetCount_management("bkg_gemeinden_lyr").getOutput(0)
                print n
            
                if(int(n) == 1 ):
                    gemeindeCursor = arcpy.SearchCursor("bkg_gemeinden_lyr")
                    for gemeinde in gemeindeCursor:
                        verbandsgemeinde = gemeinde.BEMERK
                        ags = gemeinde.AGS
                        RS = gemeinde.RS
            
                else:
                    messages.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
                    ## TODO Dateien loeschen und Projektregistrierung loeschen)
                    sys.exit()
            
                #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
                if verbandsgemeinde[0:3] != "gem":
                    ags_vg = ""
                    ags_regenesis = ags
            
                elif ags[0:2] == "03": #Niedersachsen
                    print "NS"
                    ags_vg = RS[0:5] + RS[9:]
                    ags_regenesis = RS[0:5] + RS[6] + RS[7:]
                    messages.AddMessage(ags_vg)
            
            
                elif ags[0:2] == "07": #Rheinland-Pfalz
                    print "RP"
                    ags_vg = RS[0:5] + RS[7:9]
                    ags_regenesis = RS[0:5] + RS[7:]
                    messages.AddMessage(ags_vg)
            
                return ags, ags_vg, ags_regenesis
            
            def ags_samtgemeinde(ags_in):
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_in + "'"
            
                rows = arcpy.SearchCursor(VG250, fields, where)
            
                for row in rows:
                    ags_out = row.SN_L + row.SN_R + row.SN_K + row.SN_V1[1] + row.SN_V2 + row.SN_G
            
                return ags_out
            
            
            def getKreisfrei(ags):
                #kreisfrei = "ja" wenn die letzten drei Stellen der AGS Nullen sind
                if ags[-3:] == '000':
                    kreisfrei = "1"
                else:
                    kreisfrei = "0"
            
                return(kreisfrei)
            
            
            def getEWZ(ags_input):
                query = "http://www.statistik-portal.de/Statistik-Portal/gemeindeverz.asp?G="+ags_input
                try:
                    queryresult = urllib2.urlopen(query).read()
                    time.sleep(1)
                    AnzHH = queryresult.split('<tr><th>Einwohner</th><td>')[1].split("</td></tr>")[0].replace('.','')
                except:
                    AnzHH = 1
            
                time.sleep(0.2)
                return(AnzHH)
            
            
            def getAnzHH(ags_input):
                #TODO: Haushalte, nicht Einwohner!
            
                query = "http://www.statistik-portal.de/Statistik-Portal/gemeindeverz.asp?G="+ags_input
                try:
                    queryresult = urllib2.urlopen(query).read()
                    time.sleep(1)
                    AnzHH = queryresult.split('<tr><th>Einwohner</th><td>')[1].split("</td></tr>")[0].replace('.','')
                except:
                    AnzHH = 1
            
                time.sleep(0.2)
                return(AnzHH)
            
            
            def getHebesatzGrStA(ags_input):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if data == []:
            
                    ags = ags_samtgemeinde(ags_input)
            
                    print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
            
                    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
            
                HebesatzGrStA = data[0][u'stenw1']
            
                return(HebesatzGrStA)
            
            
            def getHebesatzGrStB(ags_input):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if data == []:
                    ags = ags_samtgemeinde(ags_input)
            
                    print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
            
                    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
                HebesatzGrStB = data[0][u'stenw2']
            
                return(HebesatzGrStB)
            
            
            def getHebesatzGewSt(ags_input):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if data == []:
                    ags = ags_samtgemeinde(ags_input)
            
                    print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
            
                    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
                HebesatzGewSt = data[0][u'stenw3']
            
                return(HebesatzGewSt)
            
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import arcpy modules
            import arcpy, os, gc, sys, xlsxwriter, imp, urllib2, json
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            #############################################################################################################
            # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune
            
            schrittmeldung = 'Vereinigungsmenge aus Umland erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge KFA_01_Wirkraum_temp
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
            
            sql = """SELECT AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis INTO KFA_01_Wirkraum_temp
            FROM AWU_WanderungsfaktorAP
            GROUP BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            # Fuege Werte an  KFA_01_Wirkraum_temp an
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp'),
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
            
            sql = """INSERT INTO KFA_01_Wirkraum_temp ( AGS, AGS_VG, AGS_Regenesis )
            SELECT AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis
            FROM AWU_WanderungsfaktorEW;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Fuege Werte an  KFA_01_Wirkraum_temp an
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum')
            
            sql = """SELECT KFA_01_Wirkraum_temp.AGS, KFA_01_Wirkraum_temp.AGS_VG, KFA_01_Wirkraum_temp.AGS_Regenesis INTO KFA_01_Wirkraum
            FROM KFA_01_Wirkraum_temp
            GROUP BY KFA_01_Wirkraum_temp.AGS,KFA_01_Wirkraum_temp.AGS_VG, KFA_01_Wirkraum_temp.AGS_Regenesis
            ORDER BY KFA_01_Wirkraum_temp.AGS;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Erzeuge Tabelle KRU_01_Kreisumlagesaetze_Wirkraum
            
            #TODO: Tabelle KRU_01_Kreisumlagesaetze_Wirkraum
            #Spalte 1 AGS5 gruppieren und Filtern über kreisfrei anhand von Nullen der AGS
            #Spalte 2 "0" rein schreiben - Name der Spalte "Umlagensatz_in_vH" Double
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_01_Wirkraum')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
            
            sql = """SELECT Left([AGS],5) AS AGS5 INTO KRU_01_Kreisumlagesaetze_Wirkraum FROM KFA_01_Wirkraum GROUP BY Left([AGS],5);"""
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            # Kreisfreie Kommunen entfernen durch Filterung auf 000 hinten in der AGS
            KRU_01_Kreisumlagesaetze_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
            arcpy.AddField_management(KRU_01_Kreisumlagesaetze_Wirkraum, "Umlagensatz_in_vH", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
            fields = "AGS5"
            rows = arcpy.da.UpdateCursor(KRU_01_Kreisumlagesaetze_Wirkraum, fields)
            for row in rows:
                AGS5 = row[0]
                if AGS5[-3:] == "000":
                    rows.deleteRow()
            del rows
            
            
            #############################################################################################################
            # Schritt 2
            schrittmeldung = 'Tabelle KFA_02 erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            kfa_02_statisch = os.path.join(workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
            
            #Tabelle leeren
            arcpy.TruncateTable_management(kfa_02_statisch)
            
            KFA_01_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KFA_01_Wirkraum')
            rows = arcpy.SearchCursor(KFA_01_Wirkraum)
            
            for row in rows:
                ags = row.AGS
                ags_vg = row.AGS_VG
                ags_regenesis = row.AGS_Regenesis
            
                messages.AddMessage(ags_regenesis)
            
                EWZ = getEWZ(ags)
                print "EWZ: " + str(EWZ)
            
                kreisfrei = getKreisfrei(ags) # zur Bestimmung der Kreisfreiheit wird die Original-AGS verwendet
                print "Kreisfrei: " + str(kreisfrei)
            
                HebesatzGrStA = getHebesatzGrStA(ags_regenesis)
                print "HebesatzGrStA: " + str(HebesatzGrStA)
            
                HebesatzGrStB = getHebesatzGrStB(ags_regenesis)
                print "HebesatzGrStB: " + str(HebesatzGrStB)
            
                HebesatzGewSt = getHebesatzGewSt(ags_regenesis)
                print "HebesatzGewSt: " + str(HebesatzGewSt)
            
                #Insert Values into Table "kfa_02_statisch"
                rows1 = arcpy.InsertCursor(kfa_02_statisch)
                row1 = rows1.newRow()
                row1.AGS = ags
                row1.AGS_VG = ags_vg
                row1.AGS_Regenesis = ags_regenesis
                row1.EW = int(EWZ)
                row1.HebGrStA = int(HebesatzGrStA)
                row1.HebGrStB = int(HebesatzGrStB)
                row1.HebGewSt = int(HebesatzGewSt)
                row1.Kreisfrei = int(kreisfrei)
                rows1.insertRow(row1)
            
                del row1, rows1
            
            del row, rows
            
            
            
            #############################################################################################################
            # Schritt 2
            schrittmeldung = '\nTabelle KFA_03_Jahresdaten erzeugen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            KFA_03_Jahresdaten = os.path.join(workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
            KFA_01_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KFA_01_Wirkraum')
            
            #Tabelle leeren
            arcpy.TruncateTable_management(KFA_03_Jahresdaten)
            
            # Betrachtungszeitraum ermitteln
            rows = arcpy.SearchCursor(projektRahmendaten)
            for row in rows:
                beginnZeitraum = int(row.Beginn_Betrachtungszeitraum)
                endeZeitraum = int(row.Ende_Betrachtungszeitraum)
            del row, rows
            
            # Iteration ueber Betrachtungszeitraum und fuellen der Tabelle mit Nullwerten
            jahre = endeZeitraum - beginnZeitraum
            rows_out = arcpy.InsertCursor(KFA_03_Jahresdaten)
            
            for i in range(0,jahre+1):
            
                rows_in = arcpy.SearchCursor(KFA_01_Wirkraum)
            
                for gemeinde in rows_in:
            
                    ags = gemeinde.AGS
                    ags_vg = gemeinde.AGS_VG
                    ags_regenesis = gemeinde.AGS_Regenesis
            
                    row_out = rows_out.newRow()
                    row_out.Jahr = i + beginnZeitraum
                    row_out.AGS = ags
                    row_out.AGS_VG = ags_vg
                    row_out.AGS_Regenesis = ags_regenesis
            
                    row_out.DeltaEW = 0
                    row_out.DeltaGrSt = 0
                    row_out.DeltaGewSt = 0
                    row_out.DeltaUmsSt = 0
                    row_out.DeltaEinkSt = 0
                    row_out.DeltaFaLeiA = 0
            
                    rows_out.insertRow(row_out)
                    del row_out
            
            del rows_out
            
            
            #####################################################################
            schrittmeldung = ' - Delta Einwohner'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW'),
                (workspace_projekt_definition,'Einwohnerzahl'),
                (workspace_projekt_einnahmen,'KFA_03_Jahresdaten'),
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Jahresdaten_temp')
            
            sql = """SELECT KFA_03_Jahresdaten.Jahr, KFA_03_Jahresdaten.AGS, KFA_03_Jahresdaten.AGS_VG, KFA_03_Jahresdaten.AGS_Regenesis,  ([Einwohnerzahl]*[AWU_Wanderungsfaktor])*-1 AS DeltaEW, KFA_03_Jahresdaten.DeltaGrSt, KFA_03_Jahresdaten.DeltaGewSt, KFA_03_Jahresdaten.DeltaUmsSt, KFA_03_Jahresdaten.DeltaEinkSt, KFA_03_Jahresdaten.DeltaFaLeiA INTO KFA_03_Jahresdaten_temp
            FROM (KFA_03_Jahresdaten LEFT JOIN AWU_WanderungsfaktorEW ON KFA_03_Jahresdaten.AGS = AWU_WanderungsfaktorEW.AGS) LEFT JOIN Einwohnerzahl ON KFA_03_Jahresdaten.Jahr = Einwohnerzahl.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #DeltwEinwohner aufsummieren
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_03_Jahresdaten_temp')
                ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
            
            sql = """SELECT KFA_03_Jahresdaten_temp.Jahr, KFA_03_Jahresdaten_temp.AGS, KFA_03_Jahresdaten_temp.AGS_VG, KFA_03_Jahresdaten_temp.AGS_Regenesis, Sum(KFA_03_Jahresdaten_temp.DeltaEW) AS DeltaEW, Sum(KFA_03_Jahresdaten_temp.DeltaGrSt) AS DeltaGrSt, Sum(KFA_03_Jahresdaten_temp.DeltaGewSt) AS DeltaGewSt, Sum(KFA_03_Jahresdaten_temp.DeltaUmsSt) AS DeltaUmsSt, Sum(KFA_03_Jahresdaten_temp.DeltaEinkSt) AS DeltaEinkSt, Sum(KFA_03_Jahresdaten_temp.DeltaFaLeiA) AS DeltaFaLeiA INTO KFA_03_Jahresdaten
            FROM KFA_03_Jahresdaten_temp
            GROUP BY KFA_03_Jahresdaten_temp.Jahr, KFA_03_Jahresdaten_temp.AGS, KFA_03_Jahresdaten_temp.AGS_VG, KFA_03_Jahresdaten_temp.AGS_Regenesis;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #Nullwerte von Delta-Einwohner auf 0 setzen
            
            KFA_03_Jahresdaten = os.path.join(workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
            where_clause = '"DeltaEW" IS NULL'
            cur = arcpy.UpdateCursor(KFA_03_Jahresdaten, where_clause)
            
            for row in cur:
                row.DeltaEW = 0
                cur.updateRow(row)
            
            try:
                del row, cur
            except:
                pass
            
            #DeltaEinwohner eigene Kommune addieren
            ags = getAGS(projektname)[0]
            
            eingangstabellen = [(workspace_projekt_definition,'Einwohnerzahl')]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_Bevoelkerung_temp')
            
            sql = """SELECT Einwohnerzahl.Jahr, Sum(Einwohnerzahl.Einwohnerzahl) AS EW INTO KFA_Bevoelkerung_temp
            FROM Einwohnerzahl
            GROUP BY Einwohnerzahl.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            KFA_Bevoelkerung_temp = os.path.join(workspace_projekt_einnahmen,'KFA_Bevoelkerung_temp')
            
            fields = ['EW','Jahr']
            cursor = arcpy.da.SearchCursor(KFA_Bevoelkerung_temp, fields)
            for row in cursor:
                ew = row[0]
                jahr = row[1]
            
                where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
            
                rows_update = arcpy.UpdateCursor(KFA_03_Jahresdaten,where_clause)
                for row_update in rows_update:
                    row_update.setValue("DeltaEW", row_update.getValue("DeltaEW") + ew)
                    rows_update.updateRow(row_update)
            
                try:
                    del rows_update, row_update, where_clause
                except:
                    pass
            
            del cursor, row
            
            
            ##rows_bev = arcpy.SearchCursor(KFA_Bevoelkerung_temp)
            ##
            ##for row_bev in rows_bev:
            ##    ew = row_bev.EW
            ##    jahr = row_bev.Jahr
            ##
            ##    where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
            ##
            ##    rows_update = arcpy.UpdateCursor(KFA_03_Jahresdaten,where_clause)
            ##    for row_update in rows_update:
            ##        row_update.setValue("DeltaEW", row_update.getValue("DeltaEW") + ew)
            ##        rows_update.updateRow(row_update)
            ##try:
            ##    del rows_update, row_update, rows_bev, row_bev
            ##except:
            ##    pass
            
            
            #####################################################################
            schrittmeldung = ' - Delta Grundsteuer'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            GRST_Grundsteuereinnahmen = os.path.join(workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')
            
            fields = ['GrStEinnahmen','Jahr']
            cursor = arcpy.da.SearchCursor(GRST_Grundsteuereinnahmen, fields)
            for row in cursor:
                GrStEinnahmen = row[0]
                jahr = row[1]
            
                updateFields = ['DeltaGrSt']
                where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
                updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause)
                for updateRow in updateCursor:
                    updateRow[0] = GrStEinnahmen
                    updateCursor.updateRow(updateRow)
            
            
            #####################################################################
            schrittmeldung = ' - Delta Gewerbesteuer'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            GWST_06_Bilanz = os.path.join(workspace_projekt_einnahmen,'GWST_06_Bilanz')
            
            fields = ['SummevonGWST_EUR','Jahr', 'AGS']
            cursor = arcpy.da.SearchCursor(GWST_06_Bilanz, fields)
            for row in cursor:
                GWST = row[0]
                jahr = row[1]
                ags = row[2]
            
                updateFields = ['DeltaGewSt']
                where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
                updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause)
                for updateRow in updateCursor:
                    updateRow[0] = GWST
                    updateCursor.updateRow(updateRow)
            
            
            #####################################################################
            schrittmeldung = ' - Delta Einkommensteuer'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            EKST_06_Bilanz = os.path.join(workspace_projekt_einnahmen,'EKST_06_Bilanz')
            
            fields = ['Bilanz_EST_EUR','Betrachtungsjahr','AGS']
            cursor = arcpy.da.SearchCursor(EKST_06_Bilanz, fields)
            for row in cursor:
                EKST = row[0]
                jahr = row[1]
                ags = row[2]
            
                updateFields = ['DeltaEinkSt']
                where_clause_update = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
                updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause_update)
            
                for updateRow in updateCursor:
                    updateRow[0] = EKST
                    updateCursor.updateRow(updateRow)
            
            
            #####################################################################
            schrittmeldung = ' - Delta Familienleistungsausgleich \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            FLA_01_Ergebnis = os.path.join(workspace_projekt_einnahmen,'FLA_01_Ergebnis')
            
            fields = ['FLA_Euro','Betrachtungsjahr','AGS']
            cursor = arcpy.da.SearchCursor(FLA_01_Ergebnis, fields)
            for row in cursor:
                FLA = row[0]
                jahr = row[1]
                ags = row[2]
            
                updateFields = ['DeltaFaLeiA']
                where_clause_update = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
                updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause_update)
            
                for updateRow in updateCursor:
                    updateRow[0] = FLA
                    updateCursor.updateRow(updateRow)
            
            #####################################################################
            schrittmeldung = 'Berechne Steuerkraftmesszahl \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            #Erstelle leere Tabelle KFA_03_Jahresdaten
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_03_Jahresdaten'),
                (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl')
            
            sql = """SELECT KFA_03_Jahresdaten.AGS, KFA_03_Jahresdaten.AGS_VG, KFA_03_Jahresdaten.AGS_Regenesis, KFA_03_Jahresdaten.Jahr, KFA_02_Statische_Daten.EW AS EW_Referenz, KFA_02_Statische_Daten.HebGrStA, KFA_02_Statische_Daten.HebGrStB, KFA_02_Statische_Daten.HebGewSt, KFA_03_Jahresdaten.DeltaEW, KFA_03_Jahresdaten.DeltaGrST, KFA_03_Jahresdaten.DeltaGewSt, KFA_03_Jahresdaten.DeltaUmsSt, KFA_03_Jahresdaten.DeltaEinkSt, KFA_03_Jahresdaten.DeltaFaLeiA, KFA_02_Statische_Daten.Kreisfrei INTO KFA_03_Steuerkraftmesszahl
            FROM KFA_03_Jahresdaten INNER JOIN KFA_02_Statische_Daten ON KFA_03_Jahresdaten.AGS = KFA_02_Statische_Daten.AGs;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            KFA_03_Steuerkraftmesszahl = os.path.join(workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl')
            
            arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "deltaSKMZ", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
            arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Ausgleichsfaktor", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
            arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Grundbetrag", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
            arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Faktor_Zuweisungen_KU", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
            
            
            fields = ['AGS','Jahr','EW_Referenz','Kreisfrei','HebGrStA','HebGrStB','HebGewSt','DeltaGrST','DeltaGewSt','DeltaUmsSt','DeltaEinkSt','DeltaFaLeiA']
            cursor = arcpy.da.SearchCursor(KFA_03_Steuerkraftmesszahl, fields)
            for row in cursor:
                ags = row[0]
                jahr = row[1]
                EW_Referenz = row[2]
                kreisfrei = row[3]
                HebGrStA = row[4]
                HebGrStB = row[5]
                HebGewSt = row[6]
                DeltaGrST = row[7]
                DeltaGewSt = row[8]
                DeltaUmsSt = row[9]
                DeltaEinkSt = row[10]
                DeltaFaLeiA = row[11]
            
                KFA_Rahmendaten = os.path.join(workspace_tool_einnahmen,'KFA_Rahmendaten')
            
                if kreisfrei == 1:
                    where_clause = '"Kreisfrei"= 1 AND "AGS_Land" = ' + "'" + ags[:2] + "' AND "+ '"Einwohner_von" <=' + str(EW_Referenz)+ " AND "+ '"Einwohner_bis" >='+str(EW_Referenz)
                else:
                    where_clause = '"Kreisangehoerig"= 1 AND "AGS_Land" = ' + "'" + ags[:2] + "' AND "+ '"Einwohner_von" <=' + str(EW_Referenz)+ " AND "+ '"Einwohner_bis" >='+str(EW_Referenz)
            
                fields = [
                'Grundbetrag','Ausgleichsfaktor','Nivellierter_Hebesatz_GrSt_B','Faktor_Grundsteuer_B',
                'Nivellierter_Hebesatz_GewSt_netto','Faktor_Gewerbesteuer','Faktor_Umsatzsteuer',
                'Faktor_Anteil_Einkommensteuer','Faktor_Familienleistungsausgleich',
                'Faktor_Zuweisungen_in_Kreisumlage']
            
                cursor = arcpy.da.SearchCursor(KFA_Rahmendaten, fields, where_clause)
                for row in cursor:
                    grundbetrag = row[0]
                    ausgleichsfaktor = row[1]
                    Nivellierter_Hebesatz_GrSt_B = row[2]
                    Faktor_Grundsteuer_B = row[3]
                    Nivellierter_Hebesatz_GewSt_netto = row[4]
                    Faktor_Gewerbesteuer = row[5]
                    Faktor_Umsatzsteuer = row[6]
                    Faktor_Anteil_Einkommensteuer = row[7]
                    Faktor_Familienleistungsausgleich = row[8]
                    Faktor_Zuweisungen_in_Kreisumlage = row[9]
            
                deltaSKMZ = DeltaGrST/HebGrStB*Nivellierter_Hebesatz_GrSt_B*Faktor_Grundsteuer_B+DeltaGewSt/HebGewSt*Nivellierter_Hebesatz_GewSt_netto*Faktor_Gewerbesteuer+DeltaUmsSt*Faktor_Umsatzsteuer+DeltaEinkSt*Faktor_Anteil_Einkommensteuer+DeltaFaLeiA*Faktor_Familienleistungsausgleich
            
                updateFields = ['deltaSKMZ','Grundbetrag','Ausgleichsfaktor','Faktor_Zuweisungen_KU']
                where_clause_update = '"AGS"= '+"'"+ ags +"'"+' AND "Jahr" = '+str(jahr)
                updateCursor = arcpy.da.UpdateCursor(KFA_03_Steuerkraftmesszahl, updateFields, where_clause_update)
            
                for updateRow in updateCursor:
                    updateRow[0] = deltaSKMZ
                    updateRow[1] = grundbetrag
                    updateRow[2] = ausgleichsfaktor
                    updateRow[3] = Faktor_Zuweisungen_in_Kreisumlage
                    updateCursor.updateRow(updateRow)
            
            #####################################################################
            schrittmeldung = 'Berechne Veredelungsfaktor je Gemeinde \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_tool_einnahmen,'KFA_Veredelungsfaktor'),
                (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_Veredelung_temp')
            
            sql = """SELECT Left([AGs],2) AS AGS_2, KFA_02_Statische_Daten.AGS, KFA_02_Statische_Daten.AGS_VG, KFA_02_Statische_Daten.AGS_Regenesis, KFA_02_Statische_Daten.EW, KFA_02_Statische_Daten.Kreisfrei INTO KFA_Veredelung_temp
            FROM KFA_02_Statische_Daten;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #Veredelungsfaktor je Gemeinde erzeugen
            KFA_04_VeredelungsfaktorenGemeinden = os.path.join(workspace_projekt_einnahmen,'KFA_04_VeredelungsfaktorenGemeinden')
            arcpy.TruncateTable_management(KFA_04_VeredelungsfaktorenGemeinden)
            
            KFA_02_Statische_Daten = os.path.join(workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
            
            fields = ['AGS','AGS_VG','EW']
            cursor = arcpy.da.SearchCursor(KFA_02_Statische_Daten, fields)
            for row in cursor:
                ags = row[0]
                ags_vg = row[1]
                ewz = int(row[2])
            
                dataset = []
            
                fields1 = ['Stuetzwert_EWZ','Stuetzwert_Veredelungsfaktor']
                table = os.path.join(workspace_tool_einnahmen,'KFA_Veredelungsfaktor')
                where = '"AGS_Land"'+" ='"+ ags[:2] + "'"
            
                cursor2 = arcpy.da.SearchCursor(table, fields1, where)
                for row2 in cursor2:
                    ew = row2[0]
                    vf = row2[1]
                    werte = (ew, vf)
                    dataset.append(werte)
            
                #Werte nach Einwohnerzahl aufsteigend sortieren
                dataset.sort(key=lambda x: x[0])
            
                #nächsten Wert zur aktuellen Einwohnerzahl finden
                closest_value = min(dataset, key=lambda x:abs(x[0]-ewz))
                index = dataset.index(closest_value)
            
                #Steigung berechnen
                if closest_value[0]<ewz:
                    index_min = index
                    index_max = index+1
                else:
                    index_min = index-1
                    index_max = index
            
                p1 = dataset[index_min]
                p2 = dataset[index_max]
            
                s = (p2[1]-p1[1])/(p2[0]-p1[0])
            
                #Veredelungsfaktor berechnen
                vf = p1[1]+(ewz-p1[0])*s
            
                cur_vf = arcpy.InsertCursor(KFA_04_VeredelungsfaktorenGemeinden)
                row = cur_vf.newRow()
                row.AGS = str(ags)
                row.AGS_VG = str(ags_vg)
                row.EWZ = int(ewz)
                row.VeredelungsFaktor = float(vf)
                cur_vf.insertRow(row)
            
            
            #####################################################################
            schrittmeldung = 'Berechne KFA_05_Zuweisungen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl'),
                (workspace_projekt_einnahmen,'KFA_04_VeredelungsfaktorenGemeinden')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KFA_05_Zuweisungen')
            
            sql = """SELECT KFA_03_Steuerkraftmesszahl.AGS, KFA_03_Steuerkraftmesszahl.AGS_VG, KFA_03_Steuerkraftmesszahl.AGS_Regenesis, KFA_03_Steuerkraftmesszahl.Jahr, [DeltaEW]*[VeredelungsFaktor]*[Grundbetrag] AS deltaBedarf, KFA_03_Steuerkraftmesszahl.deltaSKMZ, [DeltaEW]*[VeredelungsFaktor]*[Grundbetrag]-[deltaSKMZ] AS deltaBedarf_minus_deltaSteuerkraft, ([deltaEW]*[Veredelungsfaktor]*[Grundbetrag]-[deltaSKMZ])*[Ausgleichsfaktor] AS Zuweisungen, KFA_03_Steuerkraftmesszahl.Faktor_Zuweisungen_KU INTO KFA_05_Zuweisungen
            FROM KFA_03_Steuerkraftmesszahl INNER JOIN KFA_04_VeredelungsfaktorenGemeinden ON KFA_03_Steuerkraftmesszahl.AGS = KFA_04_VeredelungsfaktorenGemeinden.AGS
            ORDER BY KFA_03_Steuerkraftmesszahl.AGS, KFA_03_Steuerkraftmesszahl.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Kommunaler_Finanzausgleich.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Kommunaler Finanzausgleich").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws2 = wb.add_worksheet('Auswertungen')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_KFA')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Charts anlegen
            
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws2.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'KFA_05_Zuweisungen')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            rows = arcpy.SearchCursor(ausgabetabelle)
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row.getValue(fieldname)
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9, normal)
            ws4.set_column('B:B', 9, normal)
            ws4.set_column('C:C', 16, normal)
            ws4.set_column('D:D', 12, money)
            ws4.set_column('E:E', 12, money)
            ws4.set_column('F:F', 35, money)
            ws4.set_column('G:G', 12, money)
            ws4.set_column('G:G', 25, money)
            ws4.set_column('H:H', 16, normal)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_06_KFA.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Auswertungen formatieren
            
            #Ueberschrift
            ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)
            
            AGSListe = []
            JahrListe = []
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                AGSListe.append(row.getValue("AGS"))
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                JahrListe.append(row.getValue("Jahr"))
            
            AGSListe = sorted(set(AGSListe))
            JahrListe = sorted(set(JahrListe))
            
            print JahrListe
            print AGSListe
            
            #schreibe Jahre
            i = 0
            for j in JahrListe:
                ws2.write(3,i+2,j,bold)
                i+=1
            
            #schreibe AGS
            i = 0
            for a in AGSListe:
                ws2.write(i+4,1,a,bold)
                i+=1
            
            #schreibe Werte
            i=0
            f=0
            alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
            ]
            for j in JahrListe:
                for a in AGSListe:
                    try:
                        formula = "=SUMIFS(Rohdaten_KFA!$I:$I,Rohdaten_KFA!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_KFA!$E:$E,Auswertungen!"+alphabet[f+2]+"4)"
                        ws2.write_formula(i+4, f+2, formula, money)
                        i+=1
                    except Exception as e:
                        print e
                i=0
                f+=1
            
            #Schreibe AGS als Ueberschrift
            ws2.write(3,1,"AGS",bold)
            
            ################################
            #Grafiken einfuegen
            
            print len(JahrListe)
            print len(AGSListe)
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Kommunaler Finanzausgleich in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            i=0
            
            for ags in AGSListe:
            
                i+=1
            
                chart.add_series({
                        'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                        'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)+1],
                        'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)+1], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                    })
            
            ws3.insert_chart('B2', chart)
            
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except Exception as r:
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
                messages.AddMessage(e)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = ['KFA_01_Wirkraum_temp','KFA_03_Jahresdaten_temp','KFA_Bevoelkerung_temp','KFA_Veredelung_temp','KFA_01_Wirkraum_temp','KFA_03_Jahresdaten_temp','KRU_01_Kreisumlagesaetze_Wirkraum_temp']
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_einnahmen,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('06_Kommunaler Finanzausgleich abgeschlossen')

class Einkommensteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Einkommensteuer"""
    import arcpy
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
    
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'2 Einkommensteuer'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        return [param_1]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\2_Einkommensteuer.py'):
            # -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 02_Einkommensteuer.py
            #
            # Description: Erstellung der Einkommensteuerberechnung
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            #############################################################################################################
            #
            # Funktionen
            #
            #############################################################################################################
            
            def getRS(ags_in):
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_in + "'"
                fields = "RS"
                rows = arcpy.da.SearchCursor(VG250, fields, where)
            
                for row in rows:
                    regionalschluessel = row[0]
            
                if regionalschluessel[2:] == "0000000000":
                    regionalschluessel = regionalschluessel[0:2]
            
                return regionalschluessel
            
            def getRS_VG(ags_in):
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_in + "'"
                fields = ["SN_L","SN_R","SN_K","SN_V1","SN_V2"]
                rows = arcpy.da.SearchCursor(VG250, fields, where)
            
                for row in rows:
                    regionalschluessel = row[0] + row[1] + row[2] + row[3] + row[4]
            
                return regionalschluessel
            
            
            def getAnteilEKS(ags_input,jahr):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)
            
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                AnteilEKS = int(data[0][u'steu08'])
                time.sleep(0.5)
                return(AnteilEKS)
            
            
            def getAnzHH(ags_input):
                query = "https://ergebnisse.zensus2011.de/auswertungsdb/download?csv="+ags_input+"&tableId=GWZ_4_1_0&locale=DE"
            
                queryresult = urllib2.urlopen(query).read()
                time.sleep(1)
                AnzHH = queryresult.split('Insgesamt;')[3].split(";")[0]
            
                time.sleep(0.5)
                return(AnzHH)
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import arcpy modules
            import os
            import gc
            import sys
            import imp
            import urllib2
            import json
            import time
            import arcpy
            import xlsxwriter
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_BevModellierung_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')
            
            #############################################################################################################
            #
            # Durchlauf Auswirkungen im Umland
            #
            #############################################################################################################
            beginmeldung = 'Durchlauf Einkommensteuer \n'
            messages.AddMessage(beginmeldung)
            print beginmeldung
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Ermittle kommunalen Anteil an Einkommensteuer und Anzahl Haushalte \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            EKST_01_Basisdaten = os.path.join(workspace_projekt_einnahmen,'EKST_01_Basisdaten')
            arcpy.TruncateTable_management(EKST_01_Basisdaten)
            
            umlandtabelle = os.path.join(workspace_projekt_einnahmen, "AWU_WanderungsfaktorEW")
            
            #Data Access Cursor
            fields = ['AGS', 'AGS_VG', 'AGS_Regenesis']
            cursor = arcpy.da.SearchCursor(umlandtabelle, fields)
            for row in cursor:
                ags = row[0]
                ags_vg = row[1]
                ags_regenesis = row[2]
            
            ##rows = arcpy.SearchCursor(umlandtabelle)
            ##
            ##for row in rows:
            ##    ags = row.AGS
            ##    ags_vg = row.AGS_VG
            ##    ags_regenesis = row.AGS_Regenesis
            
                try:
                    i = 0
                    try:
                        AnteilEKS10 = getAnteilEKS(ags_regenesis, 2010)*1000
                        i+=1
                    except:
                        AnteilEKS10 = 0
                    try:
                        AnteilEKS11 = getAnteilEKS(ags_regenesis, 2011)*1000
                        i+=1
                    except:
                        AnteilEKS11 = 0
                    try:
                        AnteilEKS12 = getAnteilEKS(ags_regenesis, 2012)*1000
                        i+=1
                    except:
                        AnteilEKS12 = 0
            
                    AnteilEKS = (AnteilEKS10+AnteilEKS11+AnteilEKS12)/i
                    if AnteilEKS == 0:
                        AnteilEKS = 2
            
                    try:
                        if ags_vg == "":
                            AnzHH = getAnzHH(getRS(ags)).replace("(","").replace(")","")
            
                        else:
                            AnzHH = getAnzHH(getRS_VG(ags)).replace("(","").replace(")","")
                    except:
                        AnzHH = str(1)
                        message = "Keine Haushalte fuer AGS " + ags + "gefunden. Wert wird auf 1 gesetzt."
                        messages.AddMessage(message)
            
                    #Using data access cursor for improved speed
                    fields = ['AGS', 'KAEST3Jahre', 'HH2011']
                    cursor = arcpy.da.InsertCursor(EKST_01_Basisdaten, fields)
                    cursor.insertRow((ags, AnteilEKS, AnzHH))
                    del fields, cursor
            
                    #regular Cursor
            ##        rows_insert = arcpy.InsertCursor(EKST_01_Basisdaten)
            ##        row_in = rows_insert.newRow()
            ##        row_in.AGS = ags
            ##        row_in.KAEST3Jahre = AnteilEKS
            ##        row_in.HH2011 = AnzHH
            ##        rows_insert.insertRow(row_in)
            
                    message = "Daten fuer AGS: "+ags_regenesis+" wurden ermittelt: HH:" + str(AnzHH) +" EKS:"+ str(AnteilEKS)
                    messages.AddMessage(message)
            
                except Exception as e:
                    message = "Daten fuer AGS: "+ags_regenesis+" koennen nicht ermittelt werden: " + str(e)
                    messages.AddMessage(message)
                    sys.exit()
            
            messages.AddMessage("\n")
            
            #############################################################################################################
            # Schritt Aufsummieren der Einkommensteuer pro Haushalt
            schrittmeldung = 'Aufsummieren der Einkommensteuer pro Haushalt \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge EKST_02_ESTproHHRefZiel
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_01_Basisdaten'),
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefZiel')
            
            sql = """SELECT EKST_01_Basisdaten.AGS, ([KAEST3Jahre]/[HH2011])*[AWU_Wanderungsfaktor] AS ESTProHHReferenz INTO EKST_02_ESTproHHRefZiel
            FROM EKST_01_Basisdaten INNER JOIN AWU_WanderungsfaktorEW ON EKST_01_Basisdaten.AGS = AWU_WanderungsfaktorEW.AGS;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Ermittle Summe ueber Tabelle
            EKST_02_ESTproHH = os.path.join(workspace_projekt_einnahmen,'EKST_02_ESTproHHRefZiel')
            EStProHHReferenzZielort = 0
            
            #Data Access Cursor
            cursor = arcpy.da.SearchCursor(EKST_02_ESTproHH, 'ESTproHHReferenz')
            for row in cursor:
                EStProHHReferenzZielort = EStProHHReferenzZielort + row[0]
            del cursor, row
            
            #regular Cursor
            ##rows = arcpy.SearchCursor(EKST_02_ESTproHH)
            ##for row in rows:
            ##    EStProHHReferenzZielort = EStProHHReferenzZielort + row.ESTproHHReferenz
            
            # Erzeuge EKST_02_ESTproHHRefHerkunft
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_01_Basisdaten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefHerkunft')
            
            sql = """SELECT EKST_01_Basisdaten.AGS, [KAEST3Jahre]/[HH2011] AS EStProHHRefHerkunft INTO EKST_02_ESTproHHRefHerkunft
            FROM EKST_01_Basisdaten;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt Erzeuge Wohneinheitenuebersicht
            schrittmeldung = 'Erzeuge Wohneinheitenuebersicht \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Ermittle Betrachtungszeitraum
            projektrahmendaten = os.path.join(workspace_projekt_definition,'Projektrahmendaten')
            rows = arcpy.SearchCursor(projektrahmendaten)
            for row in rows:
                beginn = row.Beginn_Betrachtungszeitraum
                ende = row.Ende_Betrachtungszeitraum
            
            del row, rows
            
            EKST_03_WE_NBG = os.path.join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')
            arcpy.TruncateTable_management(EKST_03_WE_NBG)
            
            #Iteriere ueber Jahre
            gebaeudetypenliste = []
            gebaeudetypen = os.path.join(workspace_projekt_definition,'Wohneinheiten_Details')
            fields = "Gebaeudetyp"
            rows = arcpy.da.SearchCursor(gebaeudetypen, fields)
            for row in rows:
                gebaeudetypenliste.append(row[0])
            
            gebaeudetypenliste = set(gebaeudetypenliste)
            
            for gebaeudetyp in gebaeudetypenliste:
                try:
                    message = "Berechne fuer: " + gebaeudetyp
                    messages.AddMessage(message)
            
                    #Iteriere ueber Eigentum / Miete
                    miete_eigentum = ["Miete","Eigentum"]
                    for e in miete_eigentum:
            
                        Anzahl_WE = 0
                        #Iteriere ueber Jahre
                        for jahr in range(beginn,ende+1):
            
                            Wohneinheiten_Details = os.path.join(workspace_projekt_definition,'Wohneinheiten_Details')
            
                            where = '"Gebaeudetyp"'+" ='"+ gebaeudetyp + "' AND " + '"Miete_Eigentum"'+" ='"+ e + "' AND " + '"Jahr"'+" =" + str(jahr)
                            cursor = arcpy.SearchCursor(Wohneinheiten_Details, where)
                            for row in cursor:
                                Anzahl_WE = Anzahl_WE + row.Anzahl_WE
            
                            fields = ['Jahr', 'Gebaeudetyp', 'Miete_Eigentum', 'Anzahl_WE']
                            cursor = arcpy.da.InsertCursor(EKST_03_WE_NBG, fields)
                            cursor.insertRow((jahr, gebaeudetyp, e, Anzahl_WE))
                            del fields, cursor
            
                except Exception as r:
                    messages.AddMessage(r)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = '\nErzeuge EKST_04_Zuwachs \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge EKST_04_Zuwachs
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
                (workspace_tool_einnahmen,'EKST_Korrekturfaktor_NBG')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_04_Zuwachs')
            
            sql = """SELECT 'AAAA' AS AGS, [Jahr]+7 AS Betrachtungsjahr, Sum([Anzahl_WE]*[KorrekturfaktorNBG]*EStProHHReferenzZielort) AS EST_EUR INTO EKST_04_Zuwachs
            FROM EKST_03_WE_NBG INNER JOIN EKST_Korrekturfaktor_NBG ON (EKST_03_WE_NBG.Miete_Eigentum = EKST_Korrekturfaktor_NBG.Miete_Eigentum) AND (EKST_03_WE_NBG.Gebaeudetyp = EKST_Korrekturfaktor_NBG.Gebaeudetyp)
            GROUP BY 'AAAA', [Jahr]+7
            HAVING ((([Jahr]+7)<=EndeBetrachtungszeitraum))
            ORDER BY [Jahr]+7, Sum([Anzahl_WE]*[KorrekturfaktorNBG]*EStProHHReferenzZielort);
            """
            
            sql = sql.replace("EStProHHReferenzZielort",str(EStProHHReferenzZielort)).replace("AAAA",ags).replace("EndeBetrachtungszeitraum",str(ende))
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Erzeuge EKST_05_Verlust \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge EKST_05_Verlust
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
                (workspace_tool_einnahmen,'EKST_Korrekturfaktor_NBG'),
                (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefHerkunft'),
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
            
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_05_Verlust')
            
            sql = """
            SELECT [Jahr]+7 AS Betrachtungsjahr, EKST_02_ESTproHHRefHerkunft.AGS, Sum([Anzahl_WE]*[EStProHHRefHerkunft]*[KorrekturfaktorNBG]*[AWU_Wanderungsfaktor]*-1) AS EST_EUR INTO EKST_05_Verlust
            FROM EKST_03_WE_NBG INNER JOIN EKST_Korrekturfaktor_NBG ON (EKST_03_WE_NBG.Miete_Eigentum = EKST_Korrekturfaktor_NBG.Miete_Eigentum) AND (EKST_03_WE_NBG.Gebaeudetyp = EKST_Korrekturfaktor_NBG.Gebaeudetyp), EKST_02_ESTproHHRefHerkunft INNER JOIN AWU_WanderungsfaktorEW ON EKST_02_ESTproHHRefHerkunft.AGS = AWU_WanderungsfaktorEW.AGS
            GROUP BY [Jahr]+7, EKST_02_ESTproHHRefHerkunft.AGS
            HAVING ((([Jahr]+7)<=EndeBetrachtungszeitraum))
            ORDER BY [Jahr]+7, EKST_02_ESTproHHRefHerkunft.AGS;
            """
            
            sql = sql.replace("EndeBetrachtungszeitraum",str(ende))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # INSERT EKST_05_Verlust
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_04_Zuwachs'),
                (workspace_projekt_einnahmen,'EKST_05_Verlust')
            
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_04_Zuwachs')
            
            sql = """
            INSERT INTO EKST_04_Zuwachs ( Betrachtungsjahr, AGS, EST_EUR )
            SELECT EKST_05_Verlust.Betrachtungsjahr, EKST_05_Verlust.AGS, EKST_05_Verlust.EST_EUR
            FROM EKST_05_Verlust;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Erzeuge EKST_06_Summen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge EKST_04_Zuwachs
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_04_Zuwachs')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'EKST_06_Bilanz')
            
            sql = """SELECT EKST_04_Zuwachs.AGS, EKST_04_Zuwachs.Betrachtungsjahr, Sum(EKST_04_Zuwachs.EST_EUR) AS Bilanz_EST_EUR INTO EKST_06_Bilanz
            FROM EKST_04_Zuwachs
            GROUP BY EKST_04_Zuwachs.AGS, EKST_04_Zuwachs.Betrachtungsjahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Einkommensteuer.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Einkommensteuer").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws2 = wb.add_worksheet('Auswertungen')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_Einkommensteuer')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Charts anlegen
            
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws2.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'EKST_06_Bilanz')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            rows = arcpy.SearchCursor(ausgabetabelle)
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row.getValue(fieldname)
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9,normal)
            ws4.set_column('B:B', 9,normal)
            ws4.set_column('C:C', 16,normal)
            ws4.set_column('D:D', 18, money)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_02_Einkommensteuer.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Auswertungen formatieren
            
            #Ueberschrift
            ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)
            
            AGSListe = []
            JahrListe = []
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                AGSListe.append(row.getValue("AGS"))
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                JahrListe.append(row.getValue("Betrachtungsjahr"))
            
            AGSListe = sorted(set(AGSListe))
            JahrListe = sorted(set(JahrListe))
            
            #schreibe Jahre
            i = 0
            for j in JahrListe:
                ws2.write(3,i+2,j,bold)
                i+=1
            
            #schreibe AGS
            i = 0
            for a in AGSListe:
                ws2.write(i+4,1,a,bold)
                i+=1
            
            #schreibe Werte
            i=0
            f=0
            alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
            ]
            for j in JahrListe:
                for a in AGSListe:
                    formula = "=SUMIFS(Rohdaten_Einkommensteuer!$D:$D,Rohdaten_Einkommensteuer!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_Einkommensteuer!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
                    ws2.write_formula(i+4, f+2, formula, money)
                    i+=1
                i=0
                f+=1
            
            #Schreibe AGS als Ueberschrift
            ws2.write(3,1,"AGS",bold)
            
            
            ################################
            #Grafiken einfuegen
            
            print len(JahrListe)
            print len(AGSListe)
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Einkommensteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            
            i=0
            for ags in AGSListe:
            
                i+=1
            
                chart.add_series({
                        'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                        'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)],
                        'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                    })
            
            ws3.insert_chart('B2', chart)
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except:
                print "Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?"
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = []
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_definition,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('02_Einkommensteuer abgeschlossen')

class Familienleistungsausgleich(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Familienleistungsausgleich"""
    import arcpy
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
    
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'3 Familienleistungsausgleich'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        return [param_1]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\3_Familienleistungsausgleich.py'):
            ﻿# -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 03_Familienleistungsausgleich.py
            #
            # Description: Erstellung der Einkommensteuerberechnung
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import arcpy modules
            import os
            import gc
            import sys
            import imp
            
            import arcpy
            import xlsxwriter
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_BevModellierung_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')
            
            #############################################################################################################
            #
            # Durchlauf Auswirkungen im Umland
            #
            #############################################################################################################
            beginmeldung = 'Durchlauf Familienleistungsausgleich \n'
            messages.AddMessage(beginmeldung)
            print beginmeldung
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Ermittle Familienleistungsausgleich \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge FLA_Zwischentabelle
            eingangstabellen = [
                (workspace_projekt_einnahmen,'EKST_06_Bilanz'),
                (workspace_tool_einnahmen,'FLA_Landesfaktoren')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'FLA_Zwischentabelle')
            
            sql = """SELECT EKST_06_Bilanz.AGS, Left([AGS],2) AS AGS_Land, EKST_06_Bilanz.Betrachtungsjahr, EKST_06_Bilanz.Bilanz_EST_EUR AS EST_EUR INTO FLA_Zwischentabelle
            FROM EKST_06_Bilanz;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Erzeuge FLA_Ergebnis
            eingangstabellen = [
                (workspace_projekt_einnahmen,'FLA_Zwischentabelle'),
                (workspace_tool_einnahmen,'FLA_Landesfaktoren')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'FLA_01_Ergebnis')
            
            sql = """SELECT FLA_Zwischentabelle.AGS, FLA_Zwischentabelle.Betrachtungsjahr, [EST_EUR]*[FLA_Faktor] AS FLA_EURO INTO FLA_01_Ergebnis
            FROM FLA_Landesfaktoren INNER JOIN FLA_Zwischentabelle ON FLA_Landesfaktoren.AGS_Land = FLA_Zwischentabelle.AGS_Land;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Familienleistungsausgleich.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Familienleistungsausgleich").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws2 = wb.add_worksheet('Auswertungen')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_FLA')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Charts anlegen
            
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws2.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'FLA_01_Ergebnis')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            rows = arcpy.da.SearchCursor(ausgabetabelle, fieldnames)
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row[i]
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9,normal)
            ws4.set_column('B:B', 9,normal)
            ws4.set_column('C:C', 16,normal)
            ws4.set_column('D:D', 18, money)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_03_Familienleistungsausgleich.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Auswertungen formatieren
            
            #Ueberschrift
            ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)
            
            AGSListe = []
            JahrListe = []
            
            fields = "AGS"
            rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
            for row in rows:
                AGSListe.append(row[0])
            
            fields = "Betrachtungsjahr"
            rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
            for row in rows:
                JahrListe.append(row[0])
            
            AGSListe = sorted(set(AGSListe))
            JahrListe = sorted(set(JahrListe))
            
            print JahrListe
            print AGSListe
            
            #schreibe Jahre
            i = 0
            for j in JahrListe:
                ws2.write(3,i+2,j,bold)
                i+=1
            
            #schreibe AGS
            i = 0
            for a in AGSListe:
                ws2.write(i+4,1,a,bold)
                i+=1
            
            #schreibe Werte
            i=0
            f=0
            alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
            ]
            for j in JahrListe:
                for a in AGSListe:
                    formula = "=SUMIFS(Rohdaten_FLA!$D:$D,Rohdaten_FLA!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_FLA!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
                    ws2.write_formula(i+4, f+2, formula, money)
                    i+=1
                i=0
                f+=1
            
            
            #Schreibe AGS als Ueberschrift
            ws2.write(3,1,"AGS",bold)
            
            
            ################################
            #Grafiken einfuegen
            
            print len(JahrListe)
            print len(AGSListe)
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Familienleistungsausgleich in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            
            i=0
            
            for ags in AGSListe:
            
                i+=1
            
                chart.add_series({
                        'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                        'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)+1],
                        'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)+1], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                    })
            
            ws3.insert_chart('B2', chart)
            
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except Exception as r:
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
                messages.AddMessage(r)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = ['FLA_Zwischentabelle']
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_einnahmen,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('03_Familienleistungsausgleich abgeschlossen')

class Grundsteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Grundsteuer"""
    import arcpy
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
        i=2
    
        heading1 = "01 Monatsrohmieten (in €)"
        i+=1 ; self.params[i].category = heading1 
        i+=1 ; self.params[i].category = heading1
        i+=1 ; self.params[i].category = heading1
        i+=1 ; self.params[i].category = heading1
    
        heading2 = "02 Jahresrohmieten (in €)"
        i+=1 ; self.params[i].category = heading2
        i+=1 ; self.params[i].category = heading2
    
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'4 Grundsteuer'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        # Gemeindegrössenklasse_1964
        param_2 = arcpy.Parameter()
        param_2.name = u'Gemeindegr\xf6ssenklasse_1964'
        param_2.displayName = u'Gemeindegr\xf6ssenklasse 1964'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.filter.list = [u'unter 2000 EW', u'2000 bis 5000 EW', u'5000 bis 10000 EW', u'10000 bis 50000 EW', u'50000 bis 500000 EW', u'\xfcber 500000 EW']

        # Grundsteuerhebesatz_als_vH_Satz
        param_3 = arcpy.Parameter()
        param_3.name = u'Grundsteuerhebesatz_als_vH_Satz'
        param_3.displayName = u'Grundsteuerhebesatz als vH Satz'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'

        # Einfamilienhaus__Monatsrohmiete__in_€_m²_
        param_4 = arcpy.Parameter()
        param_4.name = u'Einfamilienhaus__Monatsrohmiete__in_\u20ac_m\xb2_'
        param_4.displayName = u'Einfamilienhaus: Monatsrohmiete (in \u20ac/m\xb2)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Zeichenfolge'

        # Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_€_m²_
        param_5 = arcpy.Parameter()
        param_5.name = u'Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_\u20ac_m\xb2_'
        param_5.displayName = u'Zweifamilien- oder Doppelhaus: Monatsrohmiete (in \u20ac/m\xb2)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Zeichenfolge'

        # Reihenhaus__Monatsrohmiete__in_€_m²_
        param_6 = arcpy.Parameter()
        param_6.name = u'Reihenhaus__Monatsrohmiete__in_\u20ac_m\xb2_'
        param_6.displayName = u'Reihenhaus: Monatsrohmiete (in \u20ac/m\xb2)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'

        # Mehrfamilienhaus__Monatsrohmiete__in_€_m²_
        param_7 = arcpy.Parameter()
        param_7.name = u'Mehrfamilienhaus__Monatsrohmiete__in_\u20ac_m\xb2_'
        param_7.displayName = u'Mehrfamilienhaus: Monatsrohmiete (in \u20ac/m\xb2)'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Zeichenfolge'

        # Jahresrohmiete_Garagen___pro_Garage_
        param_8 = arcpy.Parameter()
        param_8.name = u'Jahresrohmiete_Garagen___pro_Garage_'
        param_8.displayName = u'Jahresrohmiete Garagen  (pro Garage)'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Zeichenfolge'

        # Jahresrohmiete_Carports___pro_Garage_
        param_9 = arcpy.Parameter()
        param_9.name = u'Jahresrohmiete_Carports___pro_Garage_'
        param_9.displayName = u'Jahresrohmiete Carports  (pro Garage)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Zeichenfolge'

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\4_Grundsteuer.py'):
            ﻿# -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 02_Einkommensteuer.py
            #
            # Description: Erstellung der Einkommensteuerberechnung
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import modules
            import os
            import gc
            import sys
            import imp
            
            import arcpy
            import xlsxwriter
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            gemeindegroessenklasse64 = parameters[1].valueAsText
            grundsteuerhebesatz = parameters[2].valueAsText
            
            monatsrohmiete_EFH = float(parameters[3].valueAsText.replace(",","."))
            monatsrohmiete_DHH = float(parameters[4].valueAsText.replace(",","."))
            monatsrohmiete_RH = float(parameters[5].valueAsText.replace(",","."))
            monatsrohmieteMFH = float(parameters[6].valueAsText.replace(",","."))
            monatsrohmieteMFH_G = float(parameters[6].valueAsText.replace(",","."))
            
            jahresrohmiete_garage = float(parameters[7].valueAsText.replace(",","."))
            jahresrohmiete_carport = float(parameters[8].valueAsText.replace(",","."))
            
            #projektname = "HCU_LKH_Bultweg"
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_BevModellierung_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')
            
            #############################################################################################################
            #
            # Durchlauf Auswirkungen im Umland
            #
            #############################################################################################################
            beginmeldung = 'Durchlauf Grundsteuer \n'
            messages.AddMessage(beginmeldung)
            print beginmeldung
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Einlesen Eingangstabellen\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            #Einlesen der Tabellen
            #Jahr I Gebäudetyp I Miete/Eigentum I Anzahl WE
            #Gebäudetyp I Wohnfläche_m²_proWE I Anzahl_Garagen_proWE I Anzahl_Carports_proWE
            
            #Pruefe, ob Tabellen aus EKS-Berechnung vorhanden sind
            EKST_03_WE_NBG = os.path.join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')
            rowcount = arcpy.GetCount_management(EKST_03_WE_NBG)
            if rowcount == 0:
                messages.AddMessage("Das Modul Einkommensteuer wurde noch nicht vollstaendig ausgefuehrt.\rDie fuer das Modul Grundsteuer benoetigten Tabellen sind daher noch nicht vorhanden.")
                sys.exit("")
            
            
            EKST_03_WE_NBG = os.path.join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')
            
            #############################################################################################################
            # Schritt 2
            schrittmeldung = 'Ermittle Jahresrohmieten\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            #Ubertrage Nutzereingaben in GRST_Rohmieten
            
            
            GRST_Rohmieten = os.path.join(workspace_projekt_einnahmen,'GRST_Rohmieten')
            
            arcpy.TruncateTable_management(GRST_Rohmieten)
            in_cur = arcpy.InsertCursor(GRST_Rohmieten)
            row = in_cur.newRow()
            row.Gebaeudetyp = 'Einfamilienhaus'
            row.Rohmiete = float(monatsrohmiete_EFH) * 12
            in_cur.insertRow(row)
            
            row = in_cur.newRow()
            row.Gebaeudetyp = 'Zweifamilien- oder Doppelhaus'
            row.Rohmiete = float(monatsrohmiete_DHH) * 12
            in_cur.insertRow(row)
            
            row = in_cur.newRow()
            row.Gebaeudetyp = 'Reihenhaus'
            row.Rohmiete = float(monatsrohmiete_RH) * 12
            in_cur.insertRow(row)
            
            row = in_cur.newRow()
            row.Gebaeudetyp = 'Mehrfamilienhaus'
            row.Rohmiete = float(monatsrohmieteMFH) * 12
            in_cur.insertRow(row)
            
            row = in_cur.newRow()
            row.Gebaeudetyp = 'Mehrfamilienhaus mit Gewerbeeinheiten'
            row.Rohmiete = float(monatsrohmieteMFH) * 12
            in_cur.insertRow(row)
            
            ##row = in_cur.newRow()
            ##row.Gebaeudetyp = 'Bürogebäude'
            ##row.Jahresrohmiete = 0
            ##in_cur.insertRow(row)
            ##
            ##row = in_cur.newRow()
            ##row.Gebaeudetyp = 'Gewerbegebäude'
            ##row.Jahresrohmiete = 0
            ##in_cur.insertRow(row)
            ##
            ##row = in_cur.newRow()
            ##row.Gebaeudetyp = 'Einzelhandelsgebäude'
            ##row.Jahresrohmiete = 0
            ##in_cur.insertRow(row)
            
            
            # erzeuge Tabelle Gebäudetyp I Jahresrohmiete = Wohnfläche * Monatsrohmiete *12 + Anzahl_Garagen * Jahresrohmiete_Garagen + Anzahl_Carports * Jahresrohmiete_Carports
            
            # Fixe Tabelle Gebäudetyp I Gemeindegrößenklasse64 I Vervielfältiger (als double)
            
            eingangstabellen = [
                (workspace_tool_definition,'Gebaeudetyp'),
                (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
                (workspace_projekt_einnahmen,'GRST_Rohmieten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Jahresrohmiete')
            
            sql = """SELECT Gebaeudetyp.Gebaeudetyp, [Wohnfl_m2_pro_WE]*[Rohmiete]+[Garagen_pro_WE]*jahresrohmiete_garage+[Carport_pro_WE]*jahresrohmiete_carport AS Jahresrohmiete INTO GRST_Jahresrohmiete
            FROM GRST_Rohmieten RIGHT JOIN Gebaeudetyp ON GRST_Rohmieten.Gebaeudetyp = Gebaeudetyp.Gebaeudetyp;"""
            
            sql = sql.replace("jahresrohmiete_garage",str(jahresrohmiete_garage)).replace("jahresrohmiete_carport",str(jahresrohmiete_carport))
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 3
            schrittmeldung = 'Einheitswert\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # erzeuge Tabelle Gebäudetyp I Einheitswert_bis38346_EUR I Einheitswert_ab38346_EUR
            # Einheitswert = Jahresrohmiete (aus Nr. 2) * Vervielfältiger je Gebäudetyp
            # Achtung! Ergebnisse BIS 38346 gehen komplett in diese Spalte. Liegt das Ergebnis darüber gehen 38346 in die Spalte und der Restbetrag in die Spalte Einheitswert_ab38346_EUR
            # Beispiel: 90000 = 1 * 38346_EUR in Spalte Einheitswert_bis38346_EUR und 90000-38346 in Einheitswert_ab38346_EUR
            
            # Fixe Tabelle Gebäudetyp I Steuermesszahl_bis38346_EUR I Steuermesszahl_ueber38346_EUR
            
            #Erstelle temporaere Zwischentabelle
            eingangstabellen = [
                (workspace_tool_einnahmen,'GRST_Vervielfaeltiger'),
                (workspace_projekt_einnahmen,'GRST_Jahresrohmiete'),
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Einheitswert_temp')
            
            sql = """
            SELECT GRST_Jahresrohmiete.Gebaeudetyp, [Jahresrohmiete]*[Vervielfaeltiger] AS Einheitswert INTO GRST_Einheitswert_temp
            FROM GRST_Jahresrohmiete INNER JOIN GRST_Vervielfaeltiger ON GRST_Jahresrohmiete.Gebaeudetyp = GRST_Vervielfaeltiger.Gebaeudetyp
            WHERE (((GRST_Vervielfaeltiger.Gemeindegroessenklasse64)='2000 bis 5000 EW'))
            GROUP BY GRST_Jahresrohmiete.Gebaeudetyp, [Jahresrohmiete]*[Vervielfaeltiger];
            """
            
            sql = sql.replace("2000 bis 5000 EW",str(gemeindegroessenklasse64))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #Erstelle leere Tabelle GRST_Einheitswert
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GRST_Einheitswert_temp')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Einheitswert')
            
            sql = """
            SELECT GRST_Einheitswert_temp.Gebaeudetyp, Round([Einheitswert],0) AS Einheitswert_Summe, 1 AS Einheitswert_bis38346_EUR, 1 AS Einheitswert_ueber38346_EUR INTO GRST_Einheitswert
            FROM GRST_Einheitswert_temp;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #Fuelle Werte in Einheitswerttabelle aus
            
            einheitswert = os.path.join(workspace_projekt_einnahmen,'GRST_Einheitswert')
            fields = ["Einheitswert_Summe", "Gebaeudetyp"]
            rows1 = arcpy.da.SearchCursor(einheitswert, fields)
            for row1 in rows1:
                einheitswert_value = row1[0]
                gebauedetyp = row1[1]
            
                if int(einheitswert_value) <= 38346:
                    Steuermesszahl_bis38346_EUR = einheitswert_value
                    Steuermesszahl_ueber38346_EUR = 0
            
                if int(einheitswert_value) > 38346:
                    Steuermesszahl_bis38346_EUR = 38346
                    Steuermesszahl_ueber38346_EUR = einheitswert_value - 38346
            
                where = '"Gebaeudetyp" = '+ "'"+gebauedetyp+"'"
                fields = ["Einheitswert_bis38346_EUR","Einheitswert_ueber38346_EUR"]
                rows2 = arcpy.da.UpdateCursor(einheitswert, fields, where)
                for row2 in rows2:
                    row2[0] = Steuermesszahl_bis38346_EUR
                    row2[1] = Steuermesszahl_ueber38346_EUR
                    rows2.updateRow(row2)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Steuermessbetrag und Steuerschuld\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            #erzeuge Tabelle Gebäudetyp I Steuerschuld_Jahr = (Einheitswert_bis38346_EUR * Steuermesszahl_bis38346_EUR + Einheitswert_ab38346_EUR * Steuermesszahl_ueber38346_EUR) * Hebesatz / 100
            
            #Erstelle Tabelle Steuermessbetrag
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GRST_Einheitswert'),
                (workspace_tool_einnahmen,'GRST_Steuermesszahlen')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Steuermessbetrag')
            
            sql = """SELECT GRST_Einheitswert.Gebaeudetyp, ([Einheitswert_bis38346_EUR]*[Steuermesszahl_bis_38346_EUR]+[Einheitswert_ueber38346_EUR]*[Steuermesszahl_ab_38346_EUR])*HEBESATZ/100 AS Steuerschuld_pro_Jahr INTO GRST_Steuermessbetrag
            FROM GRST_Einheitswert INNER JOIN GRST_Steuermesszahlen ON GRST_Einheitswert.Gebaeudetyp = GRST_Steuermesszahlen.Gebaeudetyp;
            """
            
            sql = sql.replace("HEBESATZ",str(grundsteuerhebesatz))
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 5
            schrittmeldung = 'Grundsteuereinnahmen\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # erzeuge Tabelle Jahr I Grundsteuereinnahmen = (Anzahl_WE je Gebäudetyp aus Tabelle im Schrit 1 * Steuerschuld aus voriger Tabelle )
            
            #Erstelle Tabelle GRST_Grundsteuereinnahmen_temp
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GRST_Steuermessbetrag'),
                (workspace_projekt_einnahmen,'EKST_03_WE_NBG')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen_temp')
            
            sql = """SELECT EKST_03_WE_NBG.Jahr, EKST_03_WE_NBG.Gebaeudetyp, Sum([Anzahl_WE]*[Steuerschuld_pro_Jahr]) AS GrStEinnahmen INTO GRST_Grundsteuereinnahmen_temp
            FROM EKST_03_WE_NBG INNER JOIN GRST_Steuermessbetrag ON EKST_03_WE_NBG.Gebaeudetyp = GRST_Steuermessbetrag.Gebaeudetyp
            GROUP BY EKST_03_WE_NBG.Jahr, EKST_03_WE_NBG.Gebaeudetyp
            ORDER BY EKST_03_WE_NBG.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #Erstelle Tabelle GRST_Grundsteuereinnahmen
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen_temp')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')
            
            sql = """SELECT GRST_Grundsteuereinnahmen_temp.Jahr, Sum(GRST_Grundsteuereinnahmen_temp.GrStEinnahmen) AS GrStEinnahmen INTO GRST_Grundsteuereinnahmen
            FROM GRST_Grundsteuereinnahmen_temp
            GROUP BY GRST_Grundsteuereinnahmen_temp.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Grundsteuer.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Grundsteuer").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_Grundsteuer')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Charts anlegen
            
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            rows = arcpy.da.SearchCursor(ausgabetabelle, fieldnames)
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row[i]
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9, normal)
            ws4.set_column('B:B', 9, normal)
            ws4.set_column('C:C', 18, money)
            
            ################################
            #Grafiken einfuegen
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Grundsteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            
            jahre = 0
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                jahre +=1
            
            chart.add_series({
                    'name': 'Grundsteuer',
                    'categories': ['Rohdaten_Grundsteuer', 1, 1, jahre+1, 1],
                    'values':     ['Rohdaten_Grundsteuer', 1, 2, jahre+1, 2], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                })
            
            ws3.insert_chart('B2', chart)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_04_Grundsteuer.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except Exception as e:
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
                messages.AddMessage(e)
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = ['GRST_Einheitswert_temp', 'GRST_Grundsteuereinnahmen_temp']
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_einnahmen,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('04_Grundsteuer abgeschlossen')

class Gewerbesteuer(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\Gewerbesteuer"""
    import arcpy
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
    
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'5 Gewerbesteuer'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        # Hebesatz_als_vH_Satz
        param_2 = arcpy.Parameter()
        param_2.name = u'Hebesatz_als_vH_Satz'
        param_2.displayName = u'Hebesatz als vH Satz'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        return [param_1, param_2]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\5_Gewerbesteuer.py'):
            ﻿# -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 05Gewerbesteuer.py
            #
            # Description: Erstellung der Einkommensteuerberechnung
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            #############################################################################################################
            #
            # Funktionen
            #
            #############################################################################################################
            
            def ags_samtgemeinde(ags_in):
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_in + "'"
            
                rows = arcpy.SearchCursor(VG250, where)
            
                for row in rows:
                    # Weiche für Bundesländer
                    if ags_in[0:2] == "03":
                        ags_sg = row.SN_L + row.SN_R + row.SN_K + row.SN_V1[1] + row.SN_V2 + row.SN_G
            
                    elif ags_in[0:2] == "07":
                        ags_sg = row.SN_L + row.SN_R + row.SN_K + row.SN_V2
            
                    else:
                        messages.AddMessage("Es trat ein Fehler in der Ermittlung der AGS der Samtgemeinde auf. Das Programm musste abgebrochen werden.")
                        sys.exit()
            
                message = "AGS_SG ermittelt: " + ags_sg
                messages.AddMessage(message)
                return ags_sg
            
            
            def ags_regionalschluessel(ags_in):
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            
                VG250 = os.path.join(workspace_basisdaten,'VG250')
                where = '"AGS"'+" ='"+ ags_in + "'"
                fields = "RS"
                rows = arcpy.da.SearchCursor(VG250, fields, where)
            
                for row in rows:
                    regionalschluessel = row[0]
            
                if regionalschluessel[2:] == "0000000000":
                    regionalschluessel = regionalschluessel[0:2]
            
                return regionalschluessel
            
            
            def getAnteilGWS(ags_input,jahr):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)
            
                #messages.AddMessage(query)
            
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if len(data) == 0:
            
                    ags_sg = ags_samtgemeinde(ags_input)
                    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_sg+"|jahr.text:"+str(jahr)
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
                AnteilGWS = int(data[0][u'stenw5'])
                return(AnteilGWS)
            
            
            def getHebesatzGWS(ags_input,jahr):
                query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)
            
                #messages.AddMessage(query)
            
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if len(data) == 0:
            
                    ags_sg = ags_samtgemeinde(ags_input)
                    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_sg+"|jahr.text:"+str(jahr)
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
                HebesatzGWS = int(data[0][u'stenw3'])
            
                return(HebesatzGWS)
            
            
            def getAnzAP(ags_input):
                query = "http://api.regenesis.pudo.org/cube/13111gj001/facts?cut=gemein.name:"+str(ags_input)
            
                #messages.AddMessage(query)
                print query
            
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                data = json.loads(jsonContent)
            
                if len(data) == 0:
                    ags_sg = ags_samtgemeinde(ags_input)
                    query = "http://api.regenesis.pudo.org/cube/13111gj001/facts?cut=gemein.name:"+str(ags_sg)
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
            
                AnzAP = data[3][u'erw032']
                return(AnzAP)
            
            
            #############################################################################################################
            #
            # Beginne Hauptteil
            #
            #############################################################################################################
            
            # Import arcpy modules
            import os
            import gc
            import sys
            import imp
            import urllib2
            import json
            
            import arcpy
            import xlsxwriter
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            hebesatzProjektkommune = parameters[1].valueAsText
            #projektname = "HCU_LKH_Bultweg"
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            
            workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_BevModellierung_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_32_Einnahmen_Tool.gdb")
            
            Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
            Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
            gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
            gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
            
            input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')
            
            #############################################################################################################
            #
            # Durchlauf Auswirkungen im Umland
            #
            #############################################################################################################
            beginmeldung = 'Durchlauf Gewerbesteuer \n'
            messages.AddMessage(beginmeldung)
            print beginmeldung
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Ermittle Gewerbesteuer und Anzahl Arbeitsplaetze \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            
            GWST_01_Basisdaten = os.path.join(workspace_projekt_einnahmen,'GWST_01_Basisdaten')
            arcpy.TruncateTable_management(GWST_01_Basisdaten)
            
            umlandtabelle = os.path.join(workspace_projekt_einnahmen, "AWU_WanderungsfaktorAP")
            fields = ["AGS", "AGS_VG", "AGS_Regenesis"]
            rows = arcpy.da.SearchCursor(umlandtabelle, fields)
            for row in rows:
                ags = row[0]
                ags_vg = row[1]
                ags_regenesis = row[2]
            
                messages.AddMessage(ags_regenesis)
            
                try:
                    i = 0
                    try:
                        AnteilGWS10 = getAnteilGWS(ags_regenesis, 2010)*1000
                        i+=1
                    except:
                        AnteilGWS10 = 0
                    try:
                        AnteilGWS11 = getAnteilGWS(ags_regenesis, 2011)*1000
                        i+=1
                    except:
                        AnteilGWS11 = 0
                    try:
                        AnteilGWS12 = getAnteilGWS(ags_regenesis, 2012)*1000
                        i+=1
                    except:
                        AnteilGWS12 = 0
            
                    try:
                        AnteilGWS = (AnteilGWS10+AnteilGWS11+AnteilGWS12)/i
            
                    except Exception as r:
                        message = "\n Die zur Abfrage der Gewerbesteuer notwendige Webseite 'http://api.regenesis.pudo.org/' liefert derzeit keine Werte zurueck. Die Berechnung wird daher unterbrochen. Bitte probieren Sie es spaeter noch einmal. \n"
                        print message
                        messages.AddMessage(message)
                        messages.AddMessage(r)
                        sys.exit()
            
                    i = 0
                    try:
                        HebeSGWS10 = getHebesatzGWS(ags_regenesis, 2010)
                        i+=1
                    except:
                        HebeSGWS10 = 0
                    try:
                        HebeSGWS11 = getHebesatzGWS(ags_regenesis, 2011)
                        i+=1
                    except:
                        HebeSGWS11 = 0
                    try:
                        HebeSGWS12 = getHebesatzGWS(ags_regenesis, 2012)
                        i+=1
                    except:
                        HebeSGWS12 = 0
            
                    HebeSGWS = (HebeSGWS10+HebeSGWS11+HebeSGWS12)/i
            
                    try:
                        AnzAP = getAnzAP(ags_regenesis)
            
                    except Exception as r:
                        AnzAP = 1
                        messages.AddMessage(r)
            
                    rows_insert = arcpy.InsertCursor(GWST_01_Basisdaten)
                    row_in = rows_insert.newRow()
                    row_in.AGS = ags
                    row_in.KAGWST3Jahre = AnteilGWS
                    row_in.AP2011 = AnzAP
                    row_in.GWSTHebesatz = HebeSGWS
                    rows_insert.insertRow(row_in)
            
                except Exception as e:
                    message = "Gewerbesteuer fuer AGS: "+ags_regenesis+" kann nicht ermittelt werden: " + str(e)
                    messages.AddMessage(message)
                    sys.exit()
            
            messages.AddMessage("\n")
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Aufsummieren der Gewerbesteuer pro Arbeitsplatz \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge GWST_02_GWSTproAPRefZiel
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_01_Basisdaten'),
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefZiel')
            
            sql = """SELECT GWST_01_Basisdaten.AGS, GWST_01_Basisdaten.AGS_Regenesis, ([KAGWST3Jahre]/[AP2011]/[GWSTHebesatz]*100)*[AWU_Wanderungsfaktor] AS GWSTGrundbetragProAPReferenz INTO GWST_02_GWSTproAPRefZiel
            FROM GWST_01_Basisdaten INNER JOIN AWU_WanderungsfaktorAP ON GWST_01_Basisdaten.AGS = AWU_WanderungsfaktorAP.AGS;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # Ermittle Summe ueber Tabelle
            GWST_02_GWSTproAP = os.path.join(workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefZiel')
            
            GWSTGrundbetragProAPReferenzZielort = 0
            rows = arcpy.SearchCursor(GWST_02_GWSTproAP)
            for row in rows:
                GWSTGrundbetragProAPReferenzZielort = GWSTGrundbetragProAPReferenzZielort + row.GWSTGrundbetragProAPReferenz
            
            # Erzeuge GWST_02_GWSTproAPRefHerkunft
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_01_Basisdaten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefHerkunft')
            
            sql = """SELECT GWST_01_Basisdaten.AGS, GWST_01_Basisdaten.AGS_Regenesis, [KAGWST3Jahre]/[AP2011]/[GWSTHebesatz]*100 AS GWSTGrundbetragProAPRefHerkunft INTO GWST_02_GWSTproAPRefHerkunft
            FROM GWST_01_Basisdaten;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 1
            schrittmeldung = 'Erzeuge Arbeitsplatzuebersicht \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge GWST_03_AP_NBG
            eingangstabellen = [
                (workspace_projekt_definition,'Gewerbe_Beschaeftigte')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_03_AP_NBG')
            
            sql = """SELECT Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche, Sum(Gewerbe_Beschaeftigte.Anzahl) AS SummevonAnzahl INTO GWST_03_AP_NBG
            FROM Gewerbe_Beschaeftigte
            GROUP BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche
            ORDER BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Erzeuge GWST_04_Zuwachs \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge GWST_04_Zuwachs
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_03_AP_NBG')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_04_Zuwachs')
            
            sql = """
            SELECT GWST_03_AP_NBG.Jahr, 'AAAA' AS AGS, Sum([SummevonAnzahl]*GWSTGrundbetragProAPReferenzZielort*hebesatzProjektkommune/100) AS GWST_EUR INTO GWST_04_Zuwachs
            FROM GWST_03_AP_NBG
            GROUP BY GWST_03_AP_NBG.Jahr, 'AAAA'
            ORDER BY GWST_03_AP_NBG.Jahr;
            """
            
            sql = sql.replace("GWSTGrundbetragProAPReferenzZielort",str(GWSTGrundbetragProAPReferenzZielort)).replace("AAAA",ags).replace("hebesatzProjektkommune",hebesatzProjektkommune)
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Erzeuge GWST_05_Verlust \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge GWST_05_Verlust
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_01_Basisdaten'),
                (workspace_projekt_einnahmen,'GWST_03_AP_NBG'),
                (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
            
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_05_Verlust')
            
            sql = """
            SELECT GWST_03_AP_NBG.Jahr, AWU_WanderungsfaktorAP.AGS, Sum(([SummevonAnzahl]*[AWU_Wanderungsfaktor]*[KAGWST3Jahre]/[AP2011])*-1) AS GWST_EUR INTO GWST_05_Verlust
            FROM GWST_03_AP_NBG, AWU_WanderungsfaktorAP INNER JOIN GWST_01_Basisdaten ON AWU_WanderungsfaktorAP.AGS = GWST_01_Basisdaten.AGS
            GROUP BY GWST_03_AP_NBG.Jahr, AWU_WanderungsfaktorAP.AGS;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            # INSERT GWST_05_Verlust into GWST_04_Zuwachs
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_04_Zuwachs'),
                (workspace_projekt_einnahmen,'GWST_05_Verlust')
            
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_04_Zuwachs')
            
            sql = """
            INSERT INTO GWST_04_Zuwachs ( Jahr, AGS, GWST_EUR )
            SELECT GWST_05_Verlust.Jahr, GWST_05_Verlust.AGS, GWST_05_Verlust.GWST_EUR
            FROM GWST_05_Verlust;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'Erzeuge GWST_06_Summen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge GWST_06_Summen
            eingangstabellen = [
                (workspace_projekt_einnahmen,'GWST_04_Zuwachs')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'GWST_06_Bilanz')
            
            sql = """SELECT GWST_04_Zuwachs.AGS, GWST_04_Zuwachs.Jahr, Sum(GWST_04_Zuwachs.GWST_EUR) AS SummevonGWST_EUR INTO GWST_06_Bilanz
            FROM GWST_04_Zuwachs
            GROUP BY GWST_04_Zuwachs.AGS, GWST_04_Zuwachs.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Gewerbesteuer.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Gewerbesteuer").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws2 = wb.add_worksheet('Auswertungen')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_Gewerbesteuer')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Charts anlegen
            
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws2.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'GWST_06_Bilanz')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            rows = arcpy.da.SearchCursor(ausgabetabelle, fieldnames)
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row[i]
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9,normal)
            ws4.set_column('B:B', 9,normal)
            ws4.set_column('C:C', 16,normal)
            ws4.set_column('D:D', 18, money)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_05_Gewerbesteuer.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Auswertungen formatieren
            
            #Ueberschrift
            ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)
            
            AGSListe = []
            JahrListe = []
            fields = ["AGS", "Jahr"]
            rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
            for row in rows:
                AGSListe.append(row[0])
            
            rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
            for row in rows:
                JahrListe.append(row[1])
            
            AGSListe = sorted(set(AGSListe))
            JahrListe = sorted(set(JahrListe))
            
            print JahrListe
            print AGSListe
            
            #schreibe Jahre
            i = 0
            for j in JahrListe:
                ws2.write(3,i+2,j,bold)
                i+=1
            
            #schreibe AGS
            i = 0
            for a in AGSListe:
                ws2.write(i+4,1,a,bold)
                i+=1
            
            #schreibe Werte
            i=0
            f=0
            alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
            ]
            for j in JahrListe:
                for a in AGSListe:
                    try:
                        formula = "=SUMIFS(Rohdaten_Gewerbesteuer!$D:$D,Rohdaten_Gewerbesteuer!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_Gewerbesteuer!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
                        ws2.write_formula(i+4, f+2, formula, money)
                        i+=1
                    except Exception as e:
                        print e
                i=0
                f+=1
            
            
            #Schreibe AGS als Ueberschrift
            ws2.write(3,1,"AGS",bold)
            
            ################################
            #Grafiken einfuegen
            
            print len(JahrListe)
            print len(AGSListe)
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Gewerbesteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            i=0
            
            for ags in AGSListe:
            
                i+=1
            
                chart.add_series({
                        'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                        'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)+1],
                        'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)+1], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                    })
            
            ws3.insert_chart('B2', chart)
            
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except Exception as r:
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
                messages.AddMessage(r)
            
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = []
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_definition,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('05_Gewerbesteuer abgeschlossen')

class KRU(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\B_Einnahmen\B_Einnahmen.tbx\KRU"""
    import arcpy
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self, parameters):
        """Setup arcpy and the list of tool parameters."""
        self.params = parameters
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        import os, arcpy
    
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
    
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []
    
        list_projects =[]
    
        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)
    
        #set parameters
        self.params[0].filter.list = list_projects 
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def __init__(self):
        self.label = u'7 Kreisumlage'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        return [param_1]
    def isLicensed(self):
        return True
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()
    def execute(self, parameters, messages):
        with script_run_as(u'F:\\ggr Projekte\\RPC_Tools\\2_Tool\\B_Einnahmen\\7_KRU.py'):
            # -*- coding: utf-8 -*-
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 32_KFA_01.py
            #
            # Description: Berechnung des Kommunalen Finanzausgleichs für das zu untersuchende Projekt
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # ILS / GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------
            
            
            # Import arcpy modules
            import os
            import gc
            import sys
            import imp
            import arcpy
            import xlsxwriter
            
            sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
            sl = imp.load_source('sheet_lib', sheetlibpath)
            
            mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
            mdb = imp.load_source('tempmdb_lib', mdblibpath)
            
            gc.collect()
            
            arcpy.env.overwriteOutput = True
            
            # Variablen definieren
            projektname = parameters[0].valueAsText
            
            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
            workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
            workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
            
            #############################################################################################################
            # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune
            
            schrittmeldung = 'Zwischentabelle AGS8 zu AGS5 erzeugen\n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge KRU_AGS5_zu_AGS8_temp
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KRU_AGS5_zu_AGS8_temp')
            
            sql = """SELECT KFA_02_Statische_Daten.AGs AS AGS8, Left([AGs],5) AS AGS5 INTO KRU_AGS5_zu_AGS8_temp
            FROM KFA_02_Statische_Daten
            GROUP BY KFA_02_Statische_Daten.AGs, KFA_02_Statische_Daten.Kreisfrei
            HAVING (((KFA_02_Statische_Daten.Kreisfrei)=0));
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            
            #############################################################################################################
            # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune
            
            schrittmeldung = 'KRU_02_delta_Kreisumlage \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Erzeuge KRU_02_delta_Kreisumlage
            eingangstabellen = [
                (workspace_projekt_einnahmen,'KFA_05_Zuweisungen'),
                (workspace_projekt_einnahmen,'KRU_AGS5_zu_AGS8_temp'),
                (workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
            ]
            
            ausgabetabelle = (workspace_projekt_einnahmen,'KRU_02_delta_Kreisumlage')
            
            sql = """SELECT KFA_05_Zuweisungen.AGS, KFA_05_Zuweisungen.AGS_VG, KFA_05_Zuweisungen.AGS_Regenesis, KFA_05_Zuweisungen.Jahr, ([deltaSKMZ]+[Zuweisungen]*[Faktor_Zuweisungen_KU])*[Umlagensatz_in_vH]/100 *-1 AS deltaKreisumlage INTO KRU_02_delta_Kreisumlage
            FROM (KFA_05_Zuweisungen INNER JOIN KRU_AGS5_zu_AGS8_temp ON KFA_05_Zuweisungen.AGS = KRU_AGS5_zu_AGS8_temp.AGS8) INNER JOIN KRU_01_Kreisumlagesaetze_Wirkraum ON KRU_AGS5_zu_AGS8_temp.AGS5 = KRU_01_Kreisumlagesaetze_Wirkraum.AGS5
            ORDER BY KFA_05_Zuweisungen.AGS, KFA_05_Zuweisungen.AGS_VG, KFA_05_Zuweisungen.AGS_Regenesis, KFA_05_Zuweisungen.Jahr;
            """
            
            mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
            
            #############################################################################################################
            # Schritt 6 - Datenexport in Excel-Datei
            schrittmeldung = 'Datenexport in Excel-Datei  \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            # Pfade setzen
            logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
            ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
            excelpfad = os.path.join(ausgabeordner,'Einnahmen_Kreisumlage.xlsx')
            
            try:
                os.remove(excelpfad)
            except:
                pass
            
            # Workbook und Tabellenblätter anlegen
            wb = xlsxwriter.Workbook(excelpfad)
            sl.infosheet(projektname, str("Kreisumlage").decode('utf-8'), wb)
            ws1 = wb.add_worksheet('Methodik')
            ws2 = wb.add_worksheet('Auswertungen')
            ws3 = wb.add_worksheet('Grafiken')
            ws4 = wb.add_worksheet('Rohdaten_KRU')
            ws5 = wb.add_worksheet('Haftungsausschluss')
            
            #Styles anlegen
            bold = wb.add_format({'bold': True})
            bold.set_bg_color('white')
            bold.set_border(0)
            
            normal = wb.add_format()
            normal.set_bg_color('white')
            normal.set_border(0)
            
            money = wb.add_format()
            money.set_num_format('#,##0')
            money.set_bg_color('white')
            money.set_border(0)
            
            #Hintergrund weiss faerben
            format = wb.add_format()
            format.set_bg_color('white')
            format.set_border(0)
            
            for x in range(0,400):
                for y in range(0,400):
                    ws1.write(x,y,"", format)
                    ws2.write(x,y,"", format)
                    ws3.write(x,y,"", format)
                    ws4.write(x,y,"", format)
                    ws5.write(x,y,"", format)
            
            ################################
            #Werteblatt 1 einfuegen
            
            ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'KRU_02_delta_Kreisumlage')
            
            #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
            rows = arcpy.SearchCursor(ausgabetabelle)
            fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
            j = 1
            for row in rows:
                i = 0
                for fieldname in fieldnames:
                    wert = row.getValue(fieldname)
                    ws4.write(j, i, wert)
                    i = i+1
            
                j = j+1
            
            #Felder als Header in Worksheet einfuegen
            i = 0
            for fieldname in fieldnames:
                column_with = len(fieldname)+2
                ws4.set_column(i, i, column_with)
                ws4.write(0, i, fieldname, bold)
                i = i+1
            
            #Eurobetrag formatieren
            ws4.set_column('A:A', 9,normal)
            ws4.set_column('B:B', 9,normal)
            ws4.set_column('C:C', 16,normal)
            ws4.set_column('D:D', 22, money)
            
            ################################
            #Methodikblatt einfuegen
            methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_07_KRU.png")
            ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Haftungsausschluss einfuegen
            haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
            ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt
            
            ################################
            #Auswertungen formatieren
            
            #Ueberschrift
            ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)
            
            AGSListe = []
            JahrListe = []
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                AGSListe.append(row.getValue("AGS"))
            
            rows = arcpy.SearchCursor(ausgabetabelle)
            for row in rows:
                JahrListe.append(row.getValue("Jahr"))
            
            AGSListe = sorted(set(AGSListe))
            JahrListe = sorted(set(JahrListe))
            
            print JahrListe
            print AGSListe
            
            #schreibe Jahre
            i = 0
            for j in JahrListe:
                ws2.write(3,i+2,j,bold)
                i+=1
            
            #schreibe AGS
            i = 0
            for a in AGSListe:
                ws2.write(i+4,1,a,bold)
                i+=1
            
            #schreibe Werte
            i=0
            f=0
            alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
            ]
            for j in JahrListe:
                for a in AGSListe:
                    try:
                        formula = "=SUMIFS(Rohdaten_KRU!$F:$F,Rohdaten_KRU!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_KRU!$E:$E,Auswertungen!"+alphabet[f+2]+"4)"
                        ws2.write_formula(i+4, f+2, formula, money)
                        i+=1
                    except Exception as e:
                        print e
                i=0
                f+=1
            
            ################################
            #Grafiken einfuegen
            
            print len(JahrListe)
            print len(AGSListe)
            
            chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
            chart.set_style(40)
            chart.set_size({'width': 800, 'height': 600})
            chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': 'Kreisumlage in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
            
            i=0
            
            for ags in AGSListe:
            
                i+=1
            
                chart.add_series({
                        'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                        'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)+1],
                        'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)+1], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                    })
            
            ws3.insert_chart('B2', chart)
            
            ################################
            #Workbook speichern
            try:
                wb.close()
            except Exception as r:
                messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
                messages.AddMessage(e)
            
            #############################################################################################################
            # Schritt 4
            schrittmeldung = 'temporaere Tabellen loeschen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung
            
            deleteList = ['KRU_AGS5_zu_AGS8_temp']
            
            for e in deleteList:
                f = os.path.join(workspace_projekt_einnahmen,e)
                try:
                    arcpy.Delete_management(f)
                except:
                    pass
            
            gc.collect()
            print "fertig"
            messages.AddMessage('06_Kommunaler Finanzausgleich abgeschlossen')