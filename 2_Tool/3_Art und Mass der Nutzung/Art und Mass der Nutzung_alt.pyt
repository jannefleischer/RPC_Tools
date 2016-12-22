# -*- coding: utf-8 -*-

import contextlib
import os
import sys
import datetime
import arcpy
import _flaechenbilanz, nutzungen
import argparse

# Export of toolbox C:\GGR\RPC_Tools\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung_alt.tbx


class Toolbox(object):
    def __init__(self):
        self.label = u'Art und Mass der Nutzung'
        self.alias = ''
        self.tools = [Flaechenbilanz, Nutzungen]

# Tool implementation code

class Flaechenbilanz(object):
    """C:\GGR\RPC_Tools\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung_alt.tbx\Flaechenbilanz"""
    # -*- coding: utf-8 -*-

    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(_flaechenbilanz)
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
      
            tbx_path = __file__
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
      
            list_teilflaechen = []
      
            i=-1
      
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
      
            #set point
            i+=1 ; self.params[i].filter.list = list_teilflaechen
      
            #Startjahr auf aktuelles Jahr setzen
            i+=1 ; self.params[i].value = datetime.datetime.now().year
      
            i = 2
            heading = "01_Generelle Fl\xe4chenaufteilung"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
      
            heading = "02_Aufteilung Nettobauland"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
      
            heading = "03_Aufteilung Verkehrsfl\xe4che"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
      
            heading = "04_Aufteilung Gr\xfcnfl\xe4che"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading
      
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
      
            def eingaben_auslesen():
                projectname = self.params[0].value
                teilflaeche = self.params[1].value
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                tablepath_flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Flaechenbilanz')
      
                # Oberkategorien
                queries_S1 = ((1,'Erschliessungsflaeche'),(2,'Gruenflaeche'),(3,'Sonstige Flaechen'),(4,'Nettobauland'))
                fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S1','Anteil_S1']
      
                for query in queries_S1:
                    where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S1" = ' + "'" + query[1] + "'"
                    rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                    value = 0
                    for row in rows:
                        value = row[2]
                    self.params[query[0]+2].value = value
      
      
                # Nettobauland
                queries_S2 = ((1,'Gewerbeflaeche'),(2,'Nettowohnbauland'))
                fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']
      
                for query in queries_S2:
                    where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                    rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                    value = 0
                    for row in rows:
                        value = row[2]
                    self.params[query[0]+6].value = value
      
      
                # Verkehr
                queries_S2 = ((1,'Laermschutzanlagen'),(2,'Privat - Innere Erschliessung'),(3,'Oeffentlich - Aeussere Erschliessung'),(4,'Oeffentlich - Innere Erschliessung'))
                fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']
      
                for query in queries_S2:
                    where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                    rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                    value = 0
                    for row in rows:
                        value = row[2]
                    self.params[query[0]+8].value = value
      
                # Gruenflaechen
                queries_S2 = ((1,'Spielplaetze'),(2,'Strassenbegleitgruen'),(3,'Ausgleichs- und Ersatzflaechen'),(4,'Allgemeine Gruenflaechen'))
                fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']
      
                for query in queries_S2:
                    where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                    rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                    value = 0
                    for row in rows:
                        value = row[2]
                    self.params[query[0]+10].value = value
      
                return
      
            def sliderSummenKontrolle(listeSliderID, zielwertSlidersumme):
                istsumme = 0
                for s in listeSliderID:
                    istsumme+=self.params[s].value
      
                if istsumme <> zielwertSlidersumme:
                    abweichung = zielwertSlidersumme - istsumme
                    for s in reversed(listeSliderID):
                        alterWert = self.params[s].value
                        neuerWert = self.params[s].value + abweichung
                        if neuerWert < 0:
                            neuerWert = 0
                        elif neuerWert > zielwertSlidersumme:
                            neuerWert = zielwertSlidersumme
                        abweichung = abweichung + alterWert - neuerWert
                        self.params[s].value = neuerWert
                return
      
            # Pfad zum Ordner, in dem Script liegt, erzeugen
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path)
      
            # Auswahl Teilfläche
            i = 0
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
      
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
                list_teilflaechen = []
                for row in rows_teilflaechen :
                    list_teilflaechen.append(row.Name)
                list_teilflaechen = sorted(set(list_teilflaechen))
                i+=1 ; self.params[i].filter.list = list_teilflaechen
      
                if len(list_teilflaechen) == 1:
                    self.params[i].value = list_teilflaechen[0]
                    eingaben_auslesen()
      
            # bestehende Eingaben (falls vorhanden) übernehmen
            i = 1
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                eingaben_auslesen()
      
            # Slider generieren
            i = 2
            # Oberkategorien
            listeSliderID = [i+1,i+2,i+3,i+4]
            zielwertSlidersumme = 100
      
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)
      
            # Nettobauland
            listeSliderID = [i+5,i+6]
      
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)
      
      
            # Verkehr
            listeSliderID = [i+7,i+8,i+9,i+10]
      
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)
      
            # Grünfläche
            listeSliderID = [i+11,i+12,i+13,i+14]
      
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)
      
      
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return

    def __init__(self):
        self.label = u'1 Fl\xe4chenbilanz eingeben'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Teilfläche
        param_2 = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Startjahr
        param_3 = arcpy.Parameter()
        param_3.name = u'Startjahr'
        param_3.displayName = u'Startjahr'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'2016'
        param_3.filter.type = 'Range'
        param_3.filter.list = [2010, 2050]

        # Verkehrsfläche____
        param_4 = arcpy.Parameter()
        param_4.name = u'Verkehrsfl\xe4che____'
        param_4.displayName = u'Verkehrsfl\xe4che (%)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'0'
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        # Grünfläche____
        param_5 = arcpy.Parameter()
        param_5.name = u'Gr\xfcnfl\xe4che____'
        param_5.displayName = u'Gr\xfcnfl\xe4che (%)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'0'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 100]

        # Sonstige_Flächen____
        param_6 = arcpy.Parameter()
        param_6.name = u'Sonstige_Fl\xe4chen____'
        param_6.displayName = u'Sonstige Fl\xe4chen (%)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'0'
        param_6.filter.type = 'Range'
        param_6.filter.list = [0, 100]

        # Nettobauland____
        param_7 = arcpy.Parameter()
        param_7.name = u'Nettobauland____'
        param_7.displayName = u'Nettobauland (%)'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Long'
        param_7.value = u'100'
        param_7.filter.type = 'Range'
        param_7.filter.list = [0, 100]

        # Gewerbeflaeche____
        param_8 = arcpy.Parameter()
        param_8.name = u'Gewerbeflaeche____'
        param_8.displayName = u'Gewerbeflaeche (%)'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Long'
        param_8.value = u'0'
        param_8.filter.type = 'Range'
        param_8.filter.list = [0, 100]

        # Nettowohnbauland____
        param_9 = arcpy.Parameter()
        param_9.name = u'Nettowohnbauland____'
        param_9.displayName = u'Nettowohnbauland (%)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Long'
        param_9.value = u'100'
        param_9.filter.type = 'Range'
        param_9.filter.list = [0, 100]

        # Flächen_für_Lärmschutz____
        param_10 = arcpy.Parameter()
        param_10.name = u'Fl\xe4chen_f\xfcr_L\xe4rmschutz____'
        param_10.displayName = u'Fl\xe4chen f\xfcr L\xe4rmschutz (%)'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = u'0'
        param_10.filter.type = 'Range'
        param_10.filter.list = [0, 100]

        # Privatwege____
        param_11 = arcpy.Parameter()
        param_11.name = u'Privatwege____'
        param_11.displayName = u'Privatwege (%)'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Long'
        param_11.value = u'0'
        param_11.filter.type = 'Range'
        param_11.filter.list = [0, 100]

        # Äußere_Erschließung____
        param_12 = arcpy.Parameter()
        param_12.name = u'\xc4u\xdfere_Erschlie\xdfung____'
        param_12.displayName = u'\xc4u\xdfere Erschlie\xdfung (%)'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Long'
        param_12.value = u'0'
        param_12.filter.type = 'Range'
        param_12.filter.list = [0, 100]

        # Innere_Erschließung____
        param_13 = arcpy.Parameter()
        param_13.name = u'Innere_Erschlie\xdfung____'
        param_13.displayName = u'Innere Erschlie\xdfung (%)'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'Long'
        param_13.value = u'100'
        param_13.filter.type = 'Range'
        param_13.filter.list = [0, 100]

        # Spielplatzfläche____
        param_14 = arcpy.Parameter()
        param_14.name = u'Spielplatzfl\xe4che____'
        param_14.displayName = u'Spielplatzfl\xe4che (%)'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'Long'
        param_14.value = u'0'
        param_14.filter.type = 'Range'
        param_14.filter.list = [0, 100]

        # Straßenbegleitgrün____
        param_15 = arcpy.Parameter()
        param_15.name = u'Stra\xdfenbegleitgr\xfcn____'
        param_15.displayName = u'Stra\xdfenbegleitgr\xfcn (%)'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'Long'
        param_15.value = u'0'
        param_15.filter.type = 'Range'
        param_15.filter.list = [0, 100]

        # Ausgleichs-_und_Ersatzflächen
        param_16 = arcpy.Parameter()
        param_16.name = u'Ausgleichs-_und_Ersatzfl\xe4chen'
        param_16.displayName = u'Ausgleichs- und Ersatzfl\xe4chen'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'Long'
        param_16.value = u'0'
        param_16.filter.type = 'Range'
        param_16.filter.list = [0, 100]

        # Allgemeine_Grünflächen
        param_17 = arcpy.Parameter()
        param_17.name = u'Allgemeine_Gr\xfcnfl\xe4chen'
        param_17.displayName = u'Allgemeine Gr\xfcnfl\xe4chen'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Long'
        param_17.value = u'100'
        param_17.filter.type = 'Range'
        param_17.filter.list = [0, 100]

        parameters= [param_1, param_2, param_3, param_4, param_5, param_6, 
                     param_7, param_8, param_9, param_10, param_11, param_12, 
                     param_13, param_14, param_15, param_16, param_17]
        
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            validator(parameters).initializeParameters()

        self.updateParameters(parameters)   
        
        return parameters
    
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
        _flaechenbilanz.main(parameters, messages)


class Nutzungen(object):
    """C:\GGR\RPC_Tools\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung_alt.tbx\Nutzungen"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
  
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            reload(nutzungen)
  
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
    
            tbx_path = __file__
    
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
            tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
            try:
                rows_projects = arcpy.SearchCursor(tablepath_projects)
                message = "jep"
            except:
                rows_projects  = []
                message = "nope"
    
            list_projects =[]
    
            for row in rows_projects:
                list_projects.append(row.Name)
            list_projects = list(set(list_projects))
            list_projects = sorted(list_projects)
    
    
            list_teilflaechen = []
    
            list_EwProWE = []
            for i in range(1,5):
                for j in range(0,10):
                    list_EwProWE.append(str(i)+","+str(j)+" Bewohner pro Wohneinheit")
    
            i=-1
    
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
    
            #set point
            i+=1 ; self.params[i].filter.list = list_teilflaechen
    
            heading = "1) Aufsiedlungszeitraum"
            i+=1 ; self.params[i].category = heading # Startjahr
            i+=1 ; self.params[i].category = heading # Aufsiedlungsdauer
    
            heading = "2) Wohnen - Anzahl Wohneinheiten nach Gebäudetypen"
            i+=1 ; self.params[i].category = heading # Anzahl WE in Einfamilienhäusern
            i+=1 ; self.params[i].category = heading # Anzahl WE in Doppelhäusern
            i+=1 ; self.params[i].category = heading # Anzahl WE in Reihenhäusern
            i+=1 ; self.params[i].category = heading # Anzahl WE in Mehrfamilienhäusern
    
            heading = "3) Wohnen - Anteile Eigentum und Miete"
            i+=1 ; self.params[i].category = heading # Anteil Eigentum in Einfamilienhäusern
            i+=1 ; self.params[i].category = heading # Anteil Eigentum in Doppelhäusern
            i+=1 ; self.params[i].category = heading # Anteil Eigentum in Reihenhäusern
            i+=1 ; self.params[i].category = heading # Anteil Eigentum in Mehrfamilienhäusern
    
            heading = "4) Wohnen - Einwohner pro Wohneinheit"
            i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Einfamilienhäusern
            i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Doppelhäusern
            i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Reihenhäusern
            i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Mehrfamilienhäusern
    
            heading = "5) Wohnen - Zuzugsquote"
            i+=1 ; self.params[i].category = heading # Zuzugsquote Wohnen
    
            heading = "6) Gewerbe - Gebietstyp und Brachenstruktur"
            i+=1 ; self.params[i].category = heading # Gebietstyp Gewerbe
            i+=1 ; self.params[i].category = heading # Anteil Verarbeitendes Gewerbe
            i+=1 ; self.params[i].category = heading # Anteil Baugewerbe
            i+=1 ; self.params[i].category = heading # Anteil Handel und Kfz
            i+=1 ; self.params[i].category = heading # Anteil Verkehr und Lagerei
            i+=1 ; self.params[i].category = heading # Anteil Freiberufl. ... Dienstleistungen
            i+=1 ; self.params[i].category = heading # Anteil Sonstige Dienstleistungen
    
            heading = "7) Gewerbe - Zuzugs- und Eigentumsquote"
            i+=1 ; self.params[i].category = heading # Zuzugsquote Gewerbe
            i+=1 ; self.params[i].category = heading # Anteil Eigentum Gewerbe
    
            heading = "8) Einzelhandel (nur Lebensmitteleinzelhandel)"
            i+=1 ; self.params[i].category = heading # Verkaufsfläche
    
            # Vorgabewerte für Aufsiedelung setzen
            self.params[2].value = datetime.datetime.now().year + 1
            self.params[3].value = 5
    
            return
  
  
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
    
            def eingaben_auslesen():
    
                projectname = self.params[0].value
                teilflaeche = self.params[1].value
    
                tablepath_flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Wohneinheiten_Details')
                tabelle_gebaude = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gebaeude_Details')
                tabelle_Versorgung_Verkaufsflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Versorgung_Verkaufsflaechen')
                flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Flaechenbilanz')
                plangebiet = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                tabelle_gewerbeanteile = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Anteile')
    
                #Startjahr und Aufsiedlungsdauer
                fields = ['Beginn_Nutzung', 'Aufsiedlungsdauer', 'Name', 'Startjahr']
                rows = arcpy.da.SearchCursor(plangebiet,fields)
                for row in rows:
                    if row[2] == teilflaeche:
                        self.params[3].value = row[1]
                        if row[0] != None:
                            self.params[2].value = row[0]
                        else:
                            self.params[2].value = row[3]
    
                # Wohnen - Anzahl Wohneinheiten nach Gebäudetypen
                fields = ['Gebaeudetyp', 'Anzahl_Gebaeude', 'Teilflaeche_Plangebiet']
                rows = arcpy.da.SearchCursor(tabelle_gebaude,fields)
    
                efh = 0
                zfh = 0
                rh = 0
                mfh = 0
    
                for row in rows:
                    if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                        efh += row[1]
                    if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                        zfh += row[1]
                    if row[2] == teilflaeche and row[0] == "Reihenhaus":
                        rh += row[1]
                    if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                        mfh += row[1]
    
                self.params[4].value = efh
                self.params[5].value = zfh
                self.params[6].value = rh
                self.params[7].value = mfh
    
                #Wohnen - Anteile Eigentum und Miete
                fields = ['Gebaeudetyp', 'Ant_Eigentuemer', 'Teilflaeche_Plangebiet']
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
                for row in rows:
                    if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                        self.params[8].value = row[1]
                    if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                        self.params[9].value = row[1]
                    if row[2] == teilflaeche and row[0] == "Reihenhaus":
                        self.params[10].value = row[1]
                    if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                        self.params[11].value = row[1]
    
                #Wohnen - Einwohner pro Wohneinheit
                fields = ['Gebaeudetyp', 'EW_je_WE', 'Teilflaeche_Plangebiet']
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
                for row in rows:
                    if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                        self.params[12].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                    if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                        self.params[13].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                    if row[2] == teilflaeche and row[0] == "Reihenhaus":
                        self.params[14].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                    if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                        self.params[15].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
    
                #Gewerbe
                rows = arcpy.da.SearchCursor(tabelle_gewerbeanteile, ["teilflaeche", "branche", "Anteil_A", "Anteil_B" , "Anteil_C" , "Anteil_D" , "Anteil_E", "Anteil_F", "Anteil_Zuzug", "Anteil_Eigentum"])
                for row in rows:
                    if row[0] == teilflaeche:
                        self.params[17].value = row[1]
                        self.params[18].value = row[2]
                        self.params[19].value = row[3]
                        self.params[20].value = row[4]
                        self.params[21].value = row[5]
                        self.params[22].value = row[6]
                        self.params[23].value = row[7]
                        self.params[24].value = row[8]
                        self.params[25].value = row[9]
    
    
                #Einzelhandel (nur Lebensmitteleinzelhandel)
                fields = ['Verkaufsflaeche', 'Teilflaeche_Plangebiet']
                rows = arcpy.da.SearchCursor(tabelle_Versorgung_Verkaufsflaechen,fields)
                for row in rows:
                    if row[1] == teilflaeche:
                        self.params[26].value = row[0]
    
                return
    
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
        # Gebietstyp auswählen
            i=17
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                gebtyp = self.params[i].value
                tablepath_gebietstyp = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebietstypen')
    
                rows = arcpy.SearchCursor(tablepath_gebietstyp)
    
                for row in rows:
                    if gebtyp == row.Gebietstyp:
                        self.params[i+1].value = row.Ant_VerarbGew
                        self.params[i+2].value = row.Ant_BauGew
                        self.params[i+3].value = row.Ant_HanKfZ
                        self.params[i+4].value = row.Ant_VerLag
                        self.params[i+5].value = row.Ant_FrWiTeDi
                        self.params[i+6].value = row.Ant_SoDi
    
        # Automatische Anpassung der Slider
            def sliderSummenKontrolle(listeSliderID, zielwertSlidersumme):
                istsumme = 0
                for s in listeSliderID:
                    istsumme+=self.params[s].value
    
                if istsumme <> zielwertSlidersumme:
                    abweichung = zielwertSlidersumme - istsumme
                    for s in reversed(listeSliderID):
                        alterWert = self.params[s].value
                        neuerWert = self.params[s].value + abweichung
                        if neuerWert < 0:
                            neuerWert = 0
                        elif neuerWert > zielwertSlidersumme:
                            neuerWert = zielwertSlidersumme
                        abweichung = abweichung + alterWert - neuerWert
                        self.params[s].value = neuerWert
                return
    
            # Pfad zum Ordner, in dem Script liegt, erzeugen
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path)
    
            # Auswahl Teilfläche
            i = 0
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
    
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
                list_teilflaechen = []
                for row in rows_teilflaechen :
                    list_teilflaechen.append(row.Name)
                list_teilflaechen = sorted(set(list_teilflaechen))
                i+=1 ; self.params[i].filter.list = list_teilflaechen
    
                if len(list_teilflaechen) == 1:
                    self.params[i].value = list_teilflaechen[0]
                    eingaben_auslesen()
    
    
            # bestehende Eingaben (falls vorhanden) übernehmen
            i = 1
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                eingaben_auslesen()
    
    
            # Slider für Anteile an Arbeitsplätzen nach Gewerbetyp generieren
            listeSliderID = [18, 19, 20, 21,22, 23]
            zielwertSlidersumme = 100
    
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)
    
            return
  
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'2 Nutzungen eingeben'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projekt
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Teilfläche
        param_2 = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Beginn_der_Aufsiedlung__Jahreszahl_
        param_3 = arcpy.Parameter()
        param_3.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param_3.displayName = u'Beginn der Aufsiedlung (Jahreszahl)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'2017'
        param_3.filter.type = 'Range'
        param_3.filter.list = [2010, 2050]

        # Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_
        param_4 = arcpy.Parameter()
        param_4.name = u'Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_'
        param_4.displayName = u'Dauer der Aufsiedlung (Jahre, 1 = Aufsiedlung wird noch im Jahr des Aufsiedlungsbeginns abgeschlossen)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'5'
        param_4.filter.type = 'Range'
        param_4.filter.list = [1, 20]

        # Anzahl_WE_in_Ein-_und_Zweifamilienhäusern
        param_5 = arcpy.Parameter()
        param_5.name = u'Anzahl_WE_in_Ein-_und_Zweifamilienh\xe4usern'
        param_5.displayName = u'Anzahl WE in Ein- und Zweifamilienh\xe4usern'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'0'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 500]

        # Anzahl_WE_in_Doppelhäusern
        param_6 = arcpy.Parameter()
        param_6.name = u'Anzahl_WE_in_Doppelh\xe4usern'
        param_6.displayName = u'Anzahl WE in Doppelh\xe4usern'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'0'
        param_6.filter.type = 'Range'
        param_6.filter.list = [0, 500]

        # Anzahl_WE_in_Reihenhäusern
        param_7 = arcpy.Parameter()
        param_7.name = u'Anzahl_WE_in_Reihenh\xe4usern'
        param_7.displayName = u'Anzahl WE in Reihenh\xe4usern'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Long'
        param_7.value = u'0'
        param_7.filter.type = 'Range'
        param_7.filter.list = [0, 500]

        # Anzahl_WE_in_Mehrfamilienhäusern
        param_8 = arcpy.Parameter()
        param_8.name = u'Anzahl_WE_in_Mehrfamilienh\xe4usern'
        param_8.displayName = u'Anzahl WE in Mehrfamilienh\xe4usern'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Long'
        param_8.value = u'0'
        param_8.filter.type = 'Range'
        param_8.filter.list = [0, 500]

        # Anteil_Eigentümernutzung_in_Ein-_und_Zweifamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_9 = arcpy.Parameter()
        param_9.name = u'Anteil_Eigent\xfcmernutzung_in_Ein-_und_Zweifamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_9.displayName = u'Anteil Eigent\xfcmernutzung in Ein- und Zweifamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Long'
        param_9.value = u'90'
        param_9.filter.type = 'Range'
        param_9.filter.list = [0, 100]

        # Anteil_Eigentümernutzung_in_Doppelhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_10 = arcpy.Parameter()
        param_10.name = u'Anteil_Eigent\xfcmernutzung_in_Doppelh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_10.displayName = u'Anteil Eigent\xfcmernutzung in Doppelh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = u'80'
        param_10.filter.type = 'Range'
        param_10.filter.list = [0, 100]

        # Anteil_Eigentümernutzung_in_Reihenhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_11 = arcpy.Parameter()
        param_11.name = u'Anteil_Eigent\xfcmernutzung_in_Reihenh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_11.displayName = u'Anteil Eigent\xfcmernutzung in Reihenh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Long'
        param_11.value = u'70'
        param_11.filter.type = 'Range'
        param_11.filter.list = [0, 100]

        # Anteil_Eigentümernutzung_in_Mehrfamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_12 = arcpy.Parameter()
        param_12.name = u'Anteil_Eigent\xfcmernutzung_in_Mehrfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_12.displayName = u'Anteil Eigent\xfcmernutzung in Mehrfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Long'
        param_12.value = u'20'
        param_12.filter.type = 'Range'
        param_12.filter.list = [0, 100]

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienhäusern__kurz_nach_dem_Bezug_
        param_13 = arcpy.Parameter()
        param_13.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_13.displayName = u'Mittlere Anzahl Einwohner pro WE in Einfamilienh\xe4usern (kurz nach dem Bezug)'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'Zeichenfolge'
        param_13.value = u'3,2 Bewohner pro Wohneinheit'
        param_13.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelhäusern__kurz_nach_dem_Bezug_
        param_14 = arcpy.Parameter()
        param_14.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelh\xe4usern__kurz_nach_dem_Bezug_'
        param_14.displayName = u'Mittlere Anzahl Einwohner pro WE in Doppelh\xe4usern (kurz nach dem Bezug)'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'Zeichenfolge'
        param_14.value = u'3,0 Bewohner pro Wohneinheit'
        param_14.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenhäusern__kurz_nach_dem_Bezug_
        param_15 = arcpy.Parameter()
        param_15.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenh\xe4usern__kurz_nach_dem_Bezug_'
        param_15.displayName = u'Mittlere Anzahl Einwohner pro WE in Reihenh\xe4usern (kurz nach dem Bezug)'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'Zeichenfolge'
        param_15.value = u'3,0 Bewohner pro Wohneinheit'
        param_15.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienhäusern__kurz_nach_dem_Bezug_
        param_16 = arcpy.Parameter()
        param_16.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_16.displayName = u'Mittlere Anzahl Einwohner pro WE in Mehrfamilienh\xe4usern (kurz nach dem Bezug)'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'Zeichenfolge'
        param_16.value = u'2,1 Bewohner pro Wohneinheit'
        param_16.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_
        param_17 = arcpy.Parameter()
        param_17.name = u'Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_'
        param_17.displayName = u'Wie viel Prozent der Bewohner der neuen Wohnungen werden neu in die Gemeinde ziehen?'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Long'
        param_17.value = u'80'
        param_17.filter.type = 'Range'
        param_17.filter.list = [0, 100]

        # Gebietstyp_auswählen
        param_18 = arcpy.Parameter()
        param_18.name = u'Gebietstyp_ausw\xe4hlen'
        param_18.displayName = u'Gebietstyp ausw\xe4hlen'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'Zeichenfolge'
        param_18.value = u'<kein Gewerbegebiet vorhanden>'
        param_18.filter.list = [u'Industriegebiet', u'Logistikgebiet', u'Klassisches Gewerbegebiet', u'Kleinteiliges Gewerbegebiet', u'Hoeherwertiges Gewerbegebiet', u'Technologiepark, Wissenschaftspark', u'<kein Gewerbegebiet vorhanden>']

        # Anteil_der_Arbeitsplätze_im_verarbeitenden_Gewerbe__in_Prozent_
        param_19 = arcpy.Parameter()
        param_19.name = u'Anteil_der_Arbeitspl\xe4tze_im_verarbeitenden_Gewerbe__in_Prozent_'
        param_19.displayName = u'Anteil der Arbeitspl\xe4tze im verarbeitenden Gewerbe (in Prozent)'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'Long'
        param_19.value = u'40'
        param_19.filter.type = 'Range'
        param_19.filter.list = [0, 100]

        # Anteil_der_Arbeitsplätze_im_Baugewerbe__in_Prozent_
        param_20 = arcpy.Parameter()
        param_20.name = u'Anteil_der_Arbeitspl\xe4tze_im_Baugewerbe__in_Prozent_'
        param_20.displayName = u'Anteil der Arbeitspl\xe4tze im Baugewerbe (in Prozent)'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'Long'
        param_20.value = u'6'
        param_20.filter.type = 'Range'
        param_20.filter.list = [0, 100]

        # Anteil_der_Arbeitsplätze_im_Handel__inkl__Kfz___in_Prozent_
        param_21 = arcpy.Parameter()
        param_21.name = u'Anteil_der_Arbeitspl\xe4tze_im_Handel__inkl__Kfz___in_Prozent_'
        param_21.displayName = u'Anteil der Arbeitspl\xe4tze im Handel (inkl. Kfz) (in Prozent)'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'Long'
        param_21.value = u'17'
        param_21.filter.type = 'Range'
        param_21.filter.list = [0, 100]

        # Anteil_der_Arbeitsplätze_im_Verkehrs-_und_Lagereibereich___in_Prozent_
        param_22 = arcpy.Parameter()
        param_22.name = u'Anteil_der_Arbeitspl\xe4tze_im_Verkehrs-_und_Lagereibereich___in_Prozent_'
        param_22.displayName = u'Anteil der Arbeitspl\xe4tze im Verkehrs- und Lagereibereich  (in Prozent)'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'Long'
        param_22.value = u'10'
        param_22.filter.type = 'Range'
        param_22.filter.list = [0, 100]

        # Anteil_der_Arbeitsplätze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_
        param_23 = arcpy.Parameter()
        param_23.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_'
        param_23.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich der freiberuflichen, wissenschaftl. bzw. techn. Dienstleistungen (in Prozent)'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'Long'
        param_23.value = u'14'
        param_23.filter.type = 'Range'
        param_23.filter.list = [0, 100]

        # Anteil_der_Arbeitsplätze_im_Bereich_sonstiger_Diensteistungen
        param_24 = arcpy.Parameter()
        param_24.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_sonstiger_Diensteistungen'
        param_24.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich sonstiger Diensteistungen'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'Long'
        param_24.value = u'13'
        param_24.filter.type = 'Range'
        param_24.filter.list = [0, 100]

        # Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_
        param_25 = arcpy.Parameter()
        param_25.name = u'Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_'
        param_25.displayName = u'Wie viel Prozent der Unternehmen werden neu in die Gemeinde ziehen?'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'Long'
        param_25.value = u'80'
        param_25.filter.type = 'Range'
        param_25.filter.list = [0, 100]

        # Welcher_Anteil_der_Gebäude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_
        param_26 = arcpy.Parameter()
        param_26.name = u'Welcher_Anteil_der_Geb\xe4ude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_'
        param_26.displayName = u'Welcher Anteil der Geb\xe4ude ist voraussichtlich im Eigentum der Unternehmen?'
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'Long'
        param_26.value = u'100'
        param_26.filter.type = 'Range'
        param_26.filter.list = [0, 100]

        # Verkaufsfläche__in_Quadratmetern_
        param_27 = arcpy.Parameter()
        param_27.name = u'Verkaufsfl\xe4che__in_Quadratmetern_'
        param_27.displayName = u'Verkaufsfl\xe4che (in Quadratmetern)'
        param_27.parameterType = 'Required'
        param_27.direction = 'Input'
        param_27.datatype = u'Long'
        param_27.value = u'0'
        param_27.filter.type = 'Range'
        param_27.filter.list = [0, 20000]
    
        parameters= [param_1, param_2, param_3, param_4, param_5, param_6, 
                     param_7, param_8, param_9, param_10, param_11, param_12, 
                     param_13, param_14, param_15, param_16, param_17, 
                     param_18, param_19, param_20, param_21, param_22, 
                     param_23, param_24, param_25, param_26, param_27]
        
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            validator(parameters).initializeParameters()

        self.updateParameters(parameters)   
        
        return parameters    
    
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
        nutzungen.main(parameters, messages)
        
def main():
    tbx = Toolbox()
    tool = Flaechenbilanz()
    tool.execute(tool.getParameterInfo(), None)
    tool = Nutzungen()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()