# -*- coding: utf-8 -*-

import contextlib
import os
import sys
import arcpy

import bewertung_wohnflaechendichte, Bodenbedeckungbeschreiben
import schutzwuerdigeBoedenTesten, oekologische_folgen

class Toolbox(object):
    def __init__(self):
        self.label = u'11_Definition_Projekt_Tool'
        self.alias = ''
        self.tools = [wohnflaechendichte, BodenbedeckungPlanfall, Ueberschneidung, Vornutzungbeschreiben, OekologischeFolgen]

# Tool implementation code

class wohnflaechendichte(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\F_Flaeche_und_Oekologie\F_Fläche und Ökologie.tbx\wohnflaechendichte"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
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
        
            i=-1
        
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
        
            heading = "Durchschnittliche überbaute Fläche nach Gebäudetyp"
            self.params[1].category = heading
            self.params[2].category = heading
            self.params[3].category = heading
            self.params[4].category = heading
        
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
        self.label = u'3 Bewertung der Wohnfl\xe4chendichte'
        self.canRunInBackground = False
        reload(bewertung_wohnflaechendichte)
        
    def getParameterInfo(self):
        # Name_des_Projektes
        param_1 = arcpy.Parameter()
        param_1.name = u'Name_des_Projektes'
        param_1.displayName = u'Name des Projektes'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Durchschnittliche_überbaute_Fläche_je_Wohneinheit_in_Ein-_und_Zweifamilienhäusern__qm_
        param_2 = arcpy.Parameter()
        param_2.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Ein-_und_Zweifamilienh\xe4usern__qm_'
        param_2.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Ein- und Zweifamilienh\xe4usern (qm)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'100'

        # Durchschnittliche_überbaute_Fläche_je_Wohneinheit_in_Doppelhäusern__qm_
        param_3 = arcpy.Parameter()
        param_3.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Doppelh\xe4usern__qm_'
        param_3.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Doppelh\xe4usern (qm)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'100'

        # Durchschnittliche_überbaute_Fläche_je_Wohneinheit_in_Reihenhäusern__qm_
        param_4 = arcpy.Parameter()
        param_4.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Reihenh\xe4usern__qm_'
        param_4.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Reihenh\xe4usern (qm)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'100'

        # Durchschnittliche_überbaute_Fläche_je_Wohneinheit_in_Mehrfamilienhäusern__qm_
        param_5 = arcpy.Parameter()
        param_5.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Mehrfamilienh\xe4usern__qm_'
        param_5.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Mehrfamilienh\xe4usern (qm)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'100'

        parameters = [param_1, param_2, param_3, param_4, param_5]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
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
        bewertung_wohnflaechendichte.main(parameters, messages)
            

class BodenbedeckungPlanfall(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\F_Flaeche_und_Oekologie\F_Fläche und Ökologie.tbx\BodenbedeckungPlanfall"""
    #Diese Datei muss in der Toolbox als Validator fUer das Projekt löschen Skript eingefUegt werden,
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
            list_projects = sorted(list_projects)
        
            list_teilflaechen = []
        
            i=-1
        
            #Filterliste fUer Bedeckungsarten
            bodenbedeckungListe =["Ueberbaute Flaechen","Asphalt, Beton","Platten","Kleinpflaster","Wassergebundene Decke, Rasengittersteine","Offener Boden, Acker","Rasen","Baeume, Straeucher","Stauden","Wiese","Natuerliche Wasserflaeche"]
            bodenbedeckungListe.sort()
            bodenbedeckungListe = list(set(bodenbedeckungListe))
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
        
            #set point
            i+=1 ; self.params[i].filter.list = list_teilflaechen
        
            heading = "01_Bodenbedeckung"
            i+=1 ; self.params[i].category = heading
            self.params[i].filter.list = bodenbedeckungListe
            i+=1 ; self.params[i].category = heading
            #i+=1 ; self.params[i].category = heading
            #self.params[i].filter.list = bodenbedeckungListe
            #i+=1 ; self.params[i].category = heading;self.params[i].enabled = 1
        
            heading = "02_Speichern"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading ;self.params[i].enabled = 0
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
        #Projekt auswaehlen
            i=-1
            i+=1
        
            self.params[5].value = "Bitte waehlen Sie das Projekt aus"
        
        #Wert i==0
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
        
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
        
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
                list_teilflaechen = []
                for row in rows_teilflaechen :
                    list_teilflaechen.append(row.Name)
                list_teilflaechen = list(set(list_teilflaechen))
        
        
                i+=1 ; self.params[i].filter.list = list_teilflaechen
                self.params[5].value = "Bitte waehlen Sie die zu bearbeitende Teilflaeche aus"
        ###UeberprUefen ob Vornutzungsfelder vorhanden, ansonsten hinzufUegen
        ###Eventuell die Spalten definieren lassen?
        ##        vornutzung1Vorhanden = False
        ##        anteil1Vorhanden = False
        ##        vornutzung2Vorhanden = False
        ##        anteil2Vorhanden = False
        ##        vornutzung3Vorhanden = False
        ##        anteil3Vorhanden = False
        ##        spalten = arcpy.ListFields(tablepath_teilflaechen)
        ##        for spalte in spalten:
        ##            if(spalte.name == "Vornutzung1"):
        ##                vornutzung1Vorhanden = True
        ##            if(spalte.name == "Anteil1"):
        ##                anteil1Vorhanden = True
        ##
        ##            if(spalte.name == "Vornutzung2"):
        ##                vornutzung2Vorhanden = True
        ##            if(spalte.name == "Anteil2"):
        ##                anteil2Vorhanden = True
        ##
        ##            if(spalte.name == "Vornutzung3"):
        ##                vornutzung3Vorhanden = True
        ##            if(spalte.name == "Anteil3"):
        ##                anteil3Vorhanden = True
        ##    #Felder anlegen
        ##        if(vornutzung1Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung1","TEXT")
        ##        if(vornutzung2Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung2","TEXT")
        ##        if(vornutzung3Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung3","TEXT")
        ##
        ##        if(anteil1Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil1","FLOAT")
        ##        if(anteil2Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil2","FLOAT")
        ##        if(anteil3Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil3","FLOAT")
        
        
        #Teilflaeche auswaehlen
            i=1
            if self.params[i].altered and not self.params[i].hasBeenValidated:
        
                projectname = self.params[i-1].value
                flaechenname = self.params[i].value
        
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                sql = "Name ='"+self.params[1].value +"'"
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen,sql)
        ##        try:
        ##            for row in rows_teilflaechen:
        ##                vornutzung1 = row.Vornutzung1
        ##                anteil1 = row.Anteil1
        ##                vornutzung2 = row.Vornutzung2
        ##                anteil2 = row.Anteil2
        ##                vornutzung3 = row.Vornutzung3
        ##                anteil3 = row.Anteil3
        ##
        ##
        ##        except:
        ##            vornutzung1 = 0.0
        ##            anteil1 = 0.0
        ##            vornutzung2 = 0.0
        ##            anteil2 = 0.0
        ##            vornutzung3 = 0.0
        ##            anteil3 = 0.0
        ##
        ##        i+=1 ; self.params[i].value = vornutzung1
        ##        i+=1 ; self.params[i].value = anteil1
        ##        i+=1 ; self.params[i].value = vornutzung2
        ##        i+=1 ; self.params[i].value = anteil2
        ##        i+=1 ; self.params[i].value = vornutzung3
        ##        i+=1 ; self.params[i].value = anteil3
                self.params[5].value = "Zum Speichern bitte das Kaestchen anklicken"
        
            if self.params[4].value == True and not self.params[4].hasBeenValidated:
                #val = win32ui.MessageBox(r"Werte gespeichert, bitte den naechsten Punkt auswaehlen oder die Eingabe mit Klick auf 'OK' beenden","Werte gespeichert")
                #sql = "Name ='"+self.params[1].value +"'"
                #EinzufUegende Werte festlegen
                if self.params[2].value == "Ueberbaute Flaechen":
                    NF_Spalte = "NF_ueberbauteFlaechen"
                if self.params[2].value == "Asphalt, Beton":
                    NF_Spalte = "NF_AsphaltBeton"
                if self.params[2].value =="Platten":
                    NF_Spalte ="NF_Platten"
                if self.params[2].value =="Kleinpflaster":
                    NF_Spalte ="NF_Kleinpflaster"
                if self.params[2].value =="Wassergebundene Decke, Rasengittersteine":
                    NF_Spalte ="NF_Rasengitter"
                if self.params[2].value =="Offener Boden, Acker":
                    NF_Spalte ="NF_Acker"
                if self.params[2].value =="Rasen":
                    NF_Spalte ="NF_Rasen"
                if self.params[2].value =="Baeume, Straeucher":
                    NF_Spalte ="NF_BaeumeStraeucher"
                if self.params[2].value =="Stauden":
                    NF_Spalte ="NF_Stauden"
                if self.params[2].value =="Wiese":
                    NF_Spalte ="NF_Wiese"
                if self.params[2].value =="Natuerliche Wasserflaeche":
                    NF_Spalte ="NF_Wasserflaeche"
        #Flächengröße der Teilflächen ermitteln um aus den Anteilen absolute Werte zu machen
                tbx_path = __file__
                base_path = os.path.dirname(tbx_path)
                base_path = os.path.dirname(base_path)
                base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
                #Projektname
                projekt = self.params[0].value
                gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
                pfad_flaeche = os.path.join(base_path,'3_Projekte',projekt,gdb,"Teilflaechen_Plangebiet")
        ##        try:
        ##            arcpy.AddField_management(pfad_flaeche,"area_hektares","FLOAT")
        ##        except:
        ##            messages.AddMessage("")
        
        ##        arcpy.CalculateField_management(pfad_flaeche,"area_hektares","!shape.area@HECTARES!","PYTHON_9.3")
        
                sql = "Name = '"+ self.params[1].value +"'"
                cursor = arcpy.SearchCursor(pfad_flaeche,sql)
                for row in cursor:
                    teilflaeche = row.Flaeche_ha
        
                NF_Anteil = self.params[3].value
                #PF_Anteil = self.params[5].value
                NF_Absolut = teilflaeche * (float(NF_Anteil)/100)
                #PF_Absolut = teilflaeche * (float(PF_Anteil)/100)
        
                projectname = self.params[0].value
                tabelle_bodenbedeckung = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Flaeche_und_Oekologie_Projekt_'+projectname+'.gdb','Bodenbedeckung')
                Insert = arcpy.InsertCursor(tabelle_bodenbedeckung)
                row = Insert.newRow()
                row.Teilflaeche = self.params[1].value
                row.setValue(NF_Spalte, NF_Absolut)
                #row.setValue(PF_Spalte,PF_Absolut)
                Insert.insertRow(row)
                #Die gespeicherten Werte sind Hektar, berechnet durch den angegebeben Anteil
        
                self.params[5].value ="Die Eingaben fuer die Teilflaeche " + str(self.params[1].value) + " wurden gespeichert. Waehlen Sie die naechste Bodenbedeckung dieser Teilflaeche aus, waehlen Sie eine weitere Teilflaeche oder beenden Sie die Eingabe mit 'OK'"
                self.params[4].value = False
        
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'1 Bodenbedeckung Nullfall beschreiben'
        self.canRunInBackground = False
        reload(Bodenbedeckungbeschreiben)
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

        # Bodenbedeckung_auf_der_Teilfläche
        param_3 = arcpy.Parameter()
        param_3.name = u'Bodenbedeckung_auf_der_Teilfl\xe4che'
        param_3.displayName = u'Bodenbedeckung auf der Teilfl\xe4che'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'
        param_3.filter.list = [u'Ueberbaute Flaechen', u'Natuerliche Wasserflaeche', u'Platten', u'Baeume, Straeucher', u'Wassergebundene Decke, Rasengittersteine', u'Stauden', u'Wiese', u'Asphalt, Beton', u'Offener Boden, Acker', u'Kleinpflaster', u'Rasen']

        # Anteil_an_der_Teilfläche____
        param_4 = arcpy.Parameter()
        param_4.name = u'Anteil_an_der_Teilfl\xe4che____'
        param_4.displayName = u'Anteil an der Teilfl\xe4che (%)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = 0
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        # Speichern
        param_5 = arcpy.Parameter()
        param_5.name = u'Speichern'
        param_5.displayName = u'Speichern'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'Boolesch'
        param_5.filter.list = [u'true', u'false']

        # Status
        param_6 = arcpy.Parameter()
        param_6.name = u'Status'
        param_6.displayName = u'Status'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'
    
        parameters = [param_1, param_2, param_3, param_4, param_5, param_6]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
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
        Bodenbedeckungbeschreiben.main(parameters, messages)

class Ueberschneidung(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\F_Flaeche_und_Oekologie\F_Fläche und Ökologie.tbx\04Uberschneidung"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
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
        
            i=-1
        
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
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
        self.label = u'4 Auf \xdcberschneidungen testen'
        self.canRunInBackground = False
        reload(schutzwuerdigeBoedenTesten)
        
    def getParameterInfo(self):
        # Projekt
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []
    
        parameters = [param_1]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
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
        schutzwuerdigeBoedenTesten.main(parameters, messages)

class Vornutzungbeschreiben(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\F_Flaeche_und_Oekologie\F_Fläche und Ökologie.tbx\Vornutzungbeschreiben222"""
    #Diese Datei muss in der Toolbox als Validator fUer das Projekt löschen Skript eingefUegt werden,
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
        
            i=-1
        
            #Filterliste fUer Bedeckungsarten
            bodenbedeckungListe =["Ueberbaute Flaechen","Asphalt, Beton","Platten","Kleinpflaster","Wassergebundene Decke, Rasengittersteine","Offener Boden, Acker","Rasen","Baeume, Straeucher","Stauden","Wiese","Natuerliche Wasserflaeche"]
            bodenbedeckungListe.sort()
            bodenbedeckungListe = list(set(bodenbedeckungListe))
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
        
            #set point
            i+=1 ; self.params[i].filter.list = list_teilflaechen
        
            heading = "01_Bodenbedeckung"
            i+=1 ; self.params[i].category = heading
            self.params[i].filter.list = bodenbedeckungListe
            i+=1 ; self.params[i].category = heading
            #i+=1 ; self.params[i].category = heading
            #self.params[i].filter.list = bodenbedeckungListe
            #i+=1 ; self.params[i].category = heading;self.params[i].enabled = 1
        
            heading = "02_Speichern"
            i+=1 ; self.params[i].category = heading
            i+=1 ; self.params[i].category = heading ;self.params[i].enabled = 0
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""        
            tbx_path = __file__
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
        #Projekt auswaehlen
            i=-1
            i+=1
        
            self.params[5].value = "Bitte waehlen Sie das Projekt aus"
        
        #Wert i==0
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
        
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
        
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
                list_teilflaechen = []
                for row in rows_teilflaechen :
                    list_teilflaechen.append(row.Name)
                list_teilflaechen = list(set(list_teilflaechen))
        
        
                i+=1 ; self.params[i].filter.list = list_teilflaechen
                self.params[5].value = "Bitte waehlen Sie die zu bearbeitende Teilflaeche aus"
        ###UeberprUefen ob Vornutzungsfelder vorhanden, ansonsten hinzufUegen
        ###Eventuell die Spalten definieren lassen?
        ##        vornutzung1Vorhanden = False
        ##        anteil1Vorhanden = False
        ##        vornutzung2Vorhanden = False
        ##        anteil2Vorhanden = False
        ##        vornutzung3Vorhanden = False
        ##        anteil3Vorhanden = False
        ##        spalten = arcpy.ListFields(tablepath_teilflaechen)
        ##        for spalte in spalten:
        ##            if(spalte.name == "Vornutzung1"):
        ##                vornutzung1Vorhanden = True
        ##            if(spalte.name == "Anteil1"):
        ##                anteil1Vorhanden = True
        ##
        ##            if(spalte.name == "Vornutzung2"):
        ##                vornutzung2Vorhanden = True
        ##            if(spalte.name == "Anteil2"):
        ##                anteil2Vorhanden = True
        ##
        ##            if(spalte.name == "Vornutzung3"):
        ##                vornutzung3Vorhanden = True
        ##            if(spalte.name == "Anteil3"):
        ##                anteil3Vorhanden = True
        ##    #Felder anlegen
        ##        if(vornutzung1Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung1","TEXT")
        ##        if(vornutzung2Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung2","TEXT")
        ##        if(vornutzung3Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Vornutzung3","TEXT")
        ##
        ##        if(anteil1Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil1","FLOAT")
        ##        if(anteil2Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil2","FLOAT")
        ##        if(anteil3Vorhanden==False):
        ##            arcpy.AddField_management(tablepath_teilflaechen,"Anteil3","FLOAT")
        
        
        #Teilflaeche auswaehlen
            i=1
            if self.params[i].altered and not self.params[i].hasBeenValidated:
        
                projectname = self.params[i-1].value
                flaechenname = self.params[i].value
        
                tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
                sql = "Name ='"+self.params[1].value +"'"
                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen,sql)
        ##        try:
        ##            for row in rows_teilflaechen:
        ##                vornutzung1 = row.Vornutzung1
        ##                anteil1 = row.Anteil1
        ##                vornutzung2 = row.Vornutzung2
        ##                anteil2 = row.Anteil2
        ##                vornutzung3 = row.Vornutzung3
        ##                anteil3 = row.Anteil3
        ##
        ##
        ##        except:
        ##            vornutzung1 = 0.0
        ##            anteil1 = 0.0
        ##            vornutzung2 = 0.0
        ##            anteil2 = 0.0
        ##            vornutzung3 = 0.0
        ##            anteil3 = 0.0
        ##
        ##        i+=1 ; self.params[i].value = vornutzung1
        ##        i+=1 ; self.params[i].value = anteil1
        ##        i+=1 ; self.params[i].value = vornutzung2
        ##        i+=1 ; self.params[i].value = anteil2
        ##        i+=1 ; self.params[i].value = vornutzung3
        ##        i+=1 ; self.params[i].value = anteil3
                self.params[5].value = "Zum Speichern bitte das Kaestchen anklicken"
        
            if self.params[4].value == True and not self.params[4].hasBeenValidated:
                #val = win32ui.MessageBox(r"Werte gespeichert, bitte den naechsten Punkt auswaehlen oder die Eingabe mit Klick auf 'OK' beenden","Werte gespeichert")
                #sql = "Name ='"+self.params[1].value +"'"
                #EinzufUegende Werte festlegen
                if self.params[2].value == "Ueberbaute Flaechen":
                    PF_Spalte = "PF_ueberbauteFlaechen"
                if self.params[2].value == "Asphalt, Beton":
                    PF_Spalte = "PF_AsphaltBeton"
                if self.params[2].value =="Platten":
                    PF_Spalte ="PF_Platten"
                if self.params[2].value =="Kleinpflaster":
                    PF_Spalte ="PF_Kleinpflaster"
                if self.params[2].value =="Wassergebundene Decke, Rasengittersteine":
                    PF_Spalte ="PF_Rasengitter"
                if self.params[2].value =="Offener Boden, Acker":
                    PF_Spalte ="PF_Acker"
                if self.params[2].value =="Rasen":
                    PF_Spalte ="PF_Rasen"
                if self.params[2].value =="Baeume, Straeucher":
                    PF_Spalte ="PF_BaeumeStraeucher"
                if self.params[2].value =="Stauden":
                    PF_Spalte ="PF_Stauden"
                if self.params[2].value =="Wiese":
                    PF_Spalte ="PF_Wiese"
                if self.params[2].value =="Natuerliche Wasserflaeche":
                    PF_Spalte ="PF_Wasserflaeche"
        #Flächengröße der Teilflächen ermitteln um aus den Anteilen absolute Werte zu machen
                tbx_path = __file__
                base_path = os.path.dirname(tbx_path)
                base_path = os.path.dirname(base_path)
                base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
                #Projektname
                projekt = self.params[0].value
                gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
                pfad_flaeche = os.path.join(base_path,'3_Projekte',projekt,gdb,"Teilflaechen_Plangebiet")
        
                sql = "Name = '"+ self.params[1].value +"'"
                cursor = arcpy.SearchCursor(pfad_flaeche,sql)
                for row in cursor:
                    teilflaeche = row.Flaeche_ha
        
                #NF_Anteil = self.params[3].value
                PF_Anteil = self.params[3].value
                #NF_Absolut = teilflaeche * (float(NF_Anteil)/100)
                PF_Absolut = teilflaeche * (float(PF_Anteil)/100)
        
                projectname = self.params[0].value
                tabelle_bodenbedeckung = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Flaeche_und_Oekologie_Projekt_'+projectname+'.gdb','Bodenbedeckung')
                Insert = arcpy.InsertCursor(tabelle_bodenbedeckung)
                row = Insert.newRow()
                row.Teilflaeche = self.params[1].value
                #row.setValue(NF_Spalte,NF_Absolut)
                row.setValue(PF_Spalte,PF_Absolut)
                Insert.insertRow(row)
                #Die gespeicherten Werte sind Hektar, berechnet durch den angegebeben Anteil
        
                self.params[5].value ="Die Eingaben fuer die Teilflaeche " + str(self.params[1].value) + " wurden gespeichert. Waehlen Sie die naechste Bodenbedeckung dieser Teilflaeche aus, waehlen Sie eine weitere Teilflaeche oder beenden Sie die Eingabe mit 'OK'"
                self.params[4].value = False
        
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'2 Bodenbedeckung Planfall beschreiben'
        self.canRunInBackground = False
        #reload(Bodenbedeckungbeschreiben)
        
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

        # geplante_Bodenbedeckung_auf_der_Teilfläche
        param_3 = arcpy.Parameter()
        param_3.name = u'geplante_Bodenbedeckung_auf_der_Teilfl\xe4che'
        param_3.displayName = u'geplante Bodenbedeckung auf der Teilfl\xe4che'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'
        param_3.filter.list = [u'Ueberbaute Flaechen', u'Natuerliche Wasserflaeche', u'Platten', u'Baeume, Straeucher', u'Wassergebundene Decke, Rasengittersteine', u'Stauden', u'Wiese', u'Asphalt, Beton', u'Offener Boden, Acker', u'Kleinpflaster', u'Rasen']

        # geplanter_Anteil_an_der_Teilfläche____
        param_4 = arcpy.Parameter()
        param_4.name = u'geplanter_Anteil_an_der_Teilfl\xe4che____'
        param_4.displayName = u'geplanter Anteil an der Teilfl\xe4che (%)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = 0
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        # Speichern
        param_5 = arcpy.Parameter()
        param_5.name = u'Speichern'
        param_5.displayName = u'Speichern'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'Boolesch'

        # Status
        param_6 = arcpy.Parameter()
        param_6.name = u'Status'
        param_6.displayName = u'Status'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
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
        Bodenbedeckungbeschreiben.main(parameters, messages)

class OekologischeFolgen(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\F_Flaeche_und_Oekologie\F_Fläche und Ökologie.tbx\OekologischeFolgen"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            tbx_path = __file__    
            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    
            tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
            tablepath_teilflaeche = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    
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
    
            i=-1
    
            #set project
            i+=1 ; self.params[i].filter.list = list_projects
    
            return
    
        def updateParameters(self):
            i=0
    #        if self.params[i].altered and not self.params[i].hasBeenValidated:
    #            tbx_path, tool_method = __file__.split('#')
    #            toolname = tool_method.split('.')[0]
    #
    #            base_path = os.path.dirname(tbx_path)
    #            base_path = os.path.dirname(base_path)
    #            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
    #            #Projektname
    #            projekt = self.params[i].value
    #            gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
    #            pfad_flaeche = os.path.join(base_path,'3_Projekte',projekt,gdb,"Teilflaechen_Plangebiet")
    
    #            arcpy.AddField_management(pfad_flaeche,"area_hektares","FLOAT")
    #            arcpy.CalculateField_management(pfad_flaeche,"area_hektares","!shape.area@HECTARES!","PYTHON_9.3")
    
    #            flaechengroesse = 0
    #            cursor = arcpy.SearchCursor(pfad_flaeche)
    #            for flaeche in cursor:
    #                flaechengroesse = flaechengroesse + flaeche.area_hektares
    #            flaechengroesse = str(flaechengroesse).replace(",",".")
    #            self.params[4].value = flaechengroesse
    
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                tbx_path = __file__
                base_path = os.path.dirname(tbx_path)
                base_path = os.path.dirname(base_path)
                base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt
                #Projektname
                projekt = self.params[i].value
                gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
                pfad_umfang = os.path.join(base_path,'3_Projekte',projekt,gdb,"Teilflaechen_Plangebiet")
    
    
            #try:
                #arcpy.CalculateField_management(pfad_umfang,"umfang_meter","!shape.length@METER!","PYTHON_9.3")
            #except:
            #pass
    
                flaechenumfang = 0
                cursor = arcpy.SearchCursor(pfad_umfang)
                for umfang in cursor:
                    flaechenumfang = flaechenumfang + umfang.umfang_meter
    
            flaechenumfang = round(flaechenumfang)
            flaechenumfang = str(flaechenumfang)
            self.params[3].value = flaechenumfang
    
    
    
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    
    
    def __init__(self):
        self.label = u'5 \xd6kologische Folgen berechnen'
        self.canRunInBackground = False
        reload(oekologische_folgen)
        
    def getParameterInfo(self):
        # Projekt_auswählen
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'04-10-16', u'test']

        # Region_auswählen
        param_2 = arcpy.Parameter()
        param_2.name = u'Region_ausw\xe4hlen'
        param_2.displayName = u'Region ausw\xe4hlen'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.filter.list = [u'Braunschweig-Salzgitter-Wolfenbuettel', u'In und um Duesseldorf', u'Kreis Euskirchen', u'Kreis Unna', u'Landkreis Harburg', u'Landkreis Wolfenbuettel', u'Rheinisch-Bergischer Kreis']

        # Länge_der_gemeinsamen_Grenze_Planfläche_Gemeinde__m_
        param_3 = arcpy.Parameter()
        param_3.name = u'L\xe4nge_der_gemeinsamen_Grenze_Planfl\xe4che_Gemeinde__m_'
        param_3.displayName = u'L\xe4nge der gemeinsamen Grenze Planfl\xe4che|Gemeinde (m)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Double'

        # Länge_der_gesamten_Grenze_der_Planfläche__m_
        param_4 = arcpy.Parameter()
        param_4.name = u'L\xe4nge_der_gesamten_Grenze_der_Planfl\xe4che__m_'
        param_4.displayName = u'L\xe4nge der gesamten Grenze der Planfl\xe4che (m)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Double'

        # Was_wird_hauptsächlich_auf_der_Projektfläche_errichtet_
        param_5 = arcpy.Parameter()
        param_5.name = u'Was_wird_haupts\xe4chlich_auf_der_Projektfl\xe4che_errichtet_'
        param_5.displayName = u'Was wird haupts\xe4chlich auf der Projektfl\xe4che errichtet?'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Zeichenfolge'
        param_5.filter.list = [u'Wohnen', u'Gewerbe', u'Einzelhandel']

        # Sind_schutzwürdige_Böden_betroffen_
        param_6 = arcpy.Parameter()
        param_6.name = u'Sind_schutzw\xfcrdige_B\xf6den_betroffen_'
        param_6.displayName = u'Sind schutzw\xfcrdige B\xf6den betroffen?'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'
        param_6.filter.list = [u'Ja', u'Nein']

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()    
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
        oekologische_folgen.main(parameters, messages)
            