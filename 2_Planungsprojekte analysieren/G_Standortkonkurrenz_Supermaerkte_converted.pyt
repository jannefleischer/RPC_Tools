# -*- coding: utf-8 -*-

import contextlib
import os
import sys
import arcpy
import imp
import T1_Lebensmittelmaerkte_einlesen
import T2_Hinzufuegen_neuen_Marktes
import T3_Definition_Zentren
import T4_Zentren_bearbeiten
import T5_StandortkonkurrenzSupermaerkteTool
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', '..'))
LIB_PATH = os.path.join(BASE_PATH, '2_Tool', '2_Projektverwaltung')
project_lib = imp.load_source('project_lib', 
                              os.path.join(LIB_PATH, 'project_lib.py'))
# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx

class Toolbox(object):
    def __init__(self):
        self.label = u'G Standortkonkurrenz'
        self.alias = ''
        self.tools = [Hinzufuegen, MaerkteLaden, Standortkonkurrenz, DefinitionZentren, ZentrenBearbeiten]

# Tool implementation code

class Hinzufuegen(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx\02HinzufuegenNeuenMarkt"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
            self.initializeParameters() # ruft InitializeParameters auf
      
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
        
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)      
        
            i = 0
            self.params[i].filter.list = list_projects
            self.Projekt= i
            i+=1
            self.neueHaltestellen = i # Neue Haltestellen
            i+=1
            self.abfrage = i #
            i+=1
            self.discounter = i #
            i+=1
        
            return
  
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parmater
            has been changed."""
        #    self.params[13].value="Zum Abspeichern eines zweiten Marktes Checkbox anklicken oder mit Ok einen Markt abspeichern und beenden"
            self.params[11].enabled=0
            self.params[self.abfrage ].enabled=0
            self.params[self.discounter ].enabled=0
            NeueHaltestellen = self.params[self.neueHaltestellen].value
            if NeueHaltestellen=="Sonstige":
                self.params[self.abfrage ].enabled=1
                self.params[self.abfrage ].parameterType="Required"
                self.params[self.discounter].enabled=1
            else:
                self.params[self.abfrage ].enabled=0
                self.params[self.discounter].enabled=0
                self.params[self.abfrage ].parameterType="Optional"
        
            if self.params[10].value == "Erweiterung":
        
                projectname = self.params[0].value
        
                tablepath_maerkte = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Standortdaten')
        
                rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
                list_uebergabepunkte=[]
                for row in rows_uebergabepunkte :
                ##               list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
                    list_uebergabepunkte.append( row.Betriebstyp+ " | "+row.Strasse +" | "+row.HNR + " | "+ row.Ort + " | "+str(row.VKFL_gesamt)+" qm")
                # repr(row.Betriebstyp).replace('u','',1).replace("'",'')
        
                del tablepath_maerkte,rows_uebergabepunkte,row
                list_uebergabepunkte=list(set(list_uebergabepunkte))
                list_uebergabepunkte=sorted(list_uebergabepunkte)
                self.params[11].filter.list = list_uebergabepunkte
                self.params[11].parameterType="Required"
        
            if self.params[12].value == True and not self.params[12].hasBeenValidated:
        
                self.params[12].enabled=0
                self.params[13].value="Bitte warten..... Abspeichern"
                tbx_path, tool_method = __file__.split('#')
                toolname = tool_method.split('.')[0]
        
                projectname = self.params[0].value
                tabelle_zentren =os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Neuer_Markt_temp')
                try:
                    arcpy.DeleteRows_management(tabelle_zentren)
                except:
                    pass
                #alle alten weg nun wieder fuellen
        
                cur_Insert= arcpy.InsertCursor(tabelle_zentren)
        
                zeile=cur_Insert.newRow()
                pnt = arcpy.CreateObject("Point")
        
                TypdesMarktes = self.params[self.neueHaltestellen].value
                if TypdesMarktes=="Sonstige":
        
                    TypdesMarktes=str(self.params[2].value)
                    self.params[13].value=str(self.params[2].value)+" "+str(len(self.params[2].value))
        
                if self.params[3].value==False:
                    discounter=0
                else:
                    discounter=1
        
                Name_desMarktes="Unbenannt"
        
                if self.params[4].value==None:
                    self.params[13].value="Fehler keine Verkaufsfläche eingegeben!"
                    return
                else:
                    VKFL=self.params[4].value
        
                if self.params[5].value==None:
                    self.params[13].value="Fehler keine Strasse eingegeben!"
                    return
                else:
                    Strasse=self.params[5].value
        
                if self.params[6].value==None:
                    self.params[13].value="Fehler keine Hausnummer eingegeben!"
                    return
                else:
                    Hausnummer=self.params[6].value
        
                if self.params[7].value==None:
                    self.params[13].value="Fehler keine Postleitzahl eingegeben!"
                    return
                else:
                    PLZ=self.params[7].value
        
                if self.params[8].value==None:
                    self.params[13].value="Fehler kein Ort eingegeben!"
                    return
                else:
                    Ort=self.params[8].value
        
        
                if self.params[9].value==None:
        ##            self.params[13].value="Fehler keine Postleitzahl eingegeben!"
        ##            return
                    Ortsteil=" "
                else:
                    Ortsteil=self.params[9].value
        
                if self.params[10].value==None:
                #neuer markt?!
                    self.params[13].value="Fehler bitte angeben ob es sich um eine Erweiterung oder einen neuen Markt handelt!"
                else:
                    if self.params[10].value=="Erweiterung":
                        tablepath_maerkte = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Standortdaten')
        
                        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
                        list_uebergabepunkte=[]
                        Typpus = self.params[11].value.split(' | ')[0]
                        strasse = self.params[11].value.split(' | ')[1]
                        hnr = self.params[11].value.split(' | ')[2]
                        ort = self.params[11].value.split(' | ')[3]
                        qm = int(self.params[11].value.split(' | ')[4].replace(' qm',''))
        
                        qm_alt=0
                        fund =0
                        for row in rows_uebergabepunkte :
                            if row.Betriebstyp==Typpus and unicode(strasse)==unicode(row.Strasse) and hnr == row.HNR and unicode(ort) ==unicode( row.Ort) and qm == row.VKFL_Gesamt:
                                fund=1
                                qm_alt=row.VKFL_Gesamt
                                erweiterungsmarktid=row.Id
                                ##rows_uebergabepunkte.deleteRow(row)
                                break
        
        ##                    messages.AddMessage(row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt)
        ##                    print row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt
                        del rows_uebergabepunkte,tablepath_maerkte,row
                        if fund==0:
                            self.params[13].value="Fehler! - Der zu erweiterde Markt wurde nicht in der Bestandsliste gefunden. Nicht gespeichert."
                            return
                        else:
                            #wurde gefunden
                            Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']
                            TypdesMarktes=str(self.params[2].value)
                            found=0
                            for g in Discounter:
                                if TypdesMarktes == g:
                                    found=1
        
                            if found==1 or self.params[3].value==true:
                                boni =1.47
                            else:
                                boni=1
        
        
        
        
                    elif self.params[10].value=="Neuen Markt":
        
                            boni=1
        
                            self.params[3].value = false
                            self.params[10].value=""
                            self.params[11].value=""
                            self.params[11].enabled=0    
        
        
                pnt.X=0
                pnt.Y=0
                lat=0
                longi=0
                a=0
        
        
                zeile.setValue("Id",600)
                zeile.setValue("Betriebstyp",str(TypdesMarktes))
                zeile.setValue("Name_postalisch",str(Name_desMarktes))
                zeile.setValue("PLZ",int(PLZ))
                zeile.setValue("Ortsteil",str(Ortsteil))
                zeile.setValue("Ort",str(Ort))
                zeile.setValue("Strasse",str(Strasse))
                zeile.setValue("HNR",str(Hausnummer))
                zeile.setValue("VKFL_Gesamt",int(VKFL))
                zeile.setValue("Lat",float(lat))
                zeile.setValue("Lon",float(longi))
                zeile.setValue("Qualitaet",int(a))
                zeile.setValue("Bonifaktor",float(boni))
                zeile.setValue("EntfallenderMarktID",int(erweiterungsmarktid))
                zeile.shape = pnt
                cur_Insert.insertRow(zeile)
        
                del cur_Insert
            
                self.params[2].value=""
                self.params[3].value=False
                self.params[4].value=""
                self.params[5].value=""
                self.params[6].value=""
                self.params[7].value=""
                self.params[8].value=""
                self.params[9].value=""
                self.params[10].value=""
                self.params[13].value="Letzten Markt eingeben und mit Ok die Toolboxeingabe beenden."  
      
                return
        
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            if self.params[10].value == "Erweiterung":
                self.params[11].parameterType="Required"
        
            else:
                self.params[11].parameterType="Optional"
            return
    
    def __init__(self):
        self.label = u'2 Hinzuf\xfcgen eines neuen Marktes'
        self.canRunInBackground = False
        reload(T2_Hinzufuegen_neuen_Marktes)
    def getParameterInfo(self):
        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Anbieter_des_Marktes
        param_2 = arcpy.Parameter()
        param_2.name = u'Anbieter_des_Marktes'
        param_2.displayName = u'Anbieter des Marktes'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.filter.list = [u'Aktiv-Discount', u'Aldi', u'Alnatura', u'basic', u'biocompany', u'Biomarkt', u'Coma', u'Combi', u'denns', u'diska', u'Edeka', u'famila', u'globus', u'HIT', u'Jibi', u'K + K (Klaas & Kock)', u'Kaufland', u'Konsum-Leipzig', u'Lidl', u'Markant', u'Marktkauf', u'Migros', u'Mix-Markt', u'nahkauf', u'Netto', u'Netto(Edeka)', u'Norma', u'NP', u'Penny', u'Perfetto (Karstadt)', u'Plaza', u'Real', u'Rewe', u'Sky', u'Sonstige', u'Tegut', u'Toom', u'treff 3000', u'vitalia', u'viv', u'V-Markt', u'Wasgau', u'WEZ']

        # Neuer_Anbieter__bei_Auswahl_von_Sonstige_
        param_3 = arcpy.Parameter()
        param_3.name = u'Neuer_Anbieter__bei_Auswahl_von_Sonstige_'
        param_3.displayName = u'Neuer Anbieter (bei Auswahl von Sonstige)'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'

        # Ja__es_handelt_sich_um_einen_Discounter
        param_4 = arcpy.Parameter()
        param_4.name = u'Ja__es_handelt_sich_um_einen_Discounter'
        param_4.displayName = u'Ja, es handelt sich um einen Discounter'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Boolesch'

        # Verkaufsfläche_gesamt__m2_
        param_5 = arcpy.Parameter()
        param_5.name = u'Verkaufsfl\xe4che_gesamt__m2_'
        param_5.displayName = u'Verkaufsfl\xe4che gesamt (m2)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Zeichenfolge'

        # Straße
        param_6 = arcpy.Parameter()
        param_6.name = u'Stra\xdfe'
        param_6.displayName = u'Stra\xdfe'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'

        # Hausnummer
        param_7 = arcpy.Parameter()
        param_7.name = u'Hausnummer'
        param_7.displayName = u'Hausnummer'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Zeichenfolge'

        # Postleitzahl
        param_8 = arcpy.Parameter()
        param_8.name = u'Postleitzahl'
        param_8.displayName = u'Postleitzahl'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Zeichenfolge'

        # Ort
        param_9 = arcpy.Parameter()
        param_9.name = u'Ort'
        param_9.displayName = u'Ort'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Zeichenfolge'

        # Ortsteil
        param_10 = arcpy.Parameter()
        param_10.name = u'Ortsteil'
        param_10.displayName = u'Ortsteil'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'Zeichenfolge'

        # Handelt_es_sich_bei_dem_neuen_Markt_um_eine_Erweiterung_oder_einen_neuen_Markt_
        param_11 = arcpy.Parameter()
        param_11.name = u'Handelt_es_sich_bei_dem_neuen_Markt_um_eine_Erweiterung_oder_einen_neuen_Markt_'
        param_11.displayName = u'Handelt es sich bei dem neuen Markt um eine Erweiterung oder einen neuen Markt?'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Zeichenfolge'
        param_11.filter.list = [u'Erweiterung', u'Neuen Markt']

        # Markterweiterung_wurde_ausgewählt__Welcher_Markt_soll_erweitert_werden_
        param_12 = arcpy.Parameter()
        param_12.name = u'Markterweiterung_wurde_ausgew\xe4hlt__Welcher_Markt_soll_erweitert_werden_'
        param_12.displayName = u'Markterweiterung wurde ausgew\xe4hlt. Welcher Markt soll erweitert werden?'
        param_12.parameterType = 'Optional'
        param_12.direction = 'Input'
        param_12.datatype = u'Zeichenfolge'

        # Einen_zusätzlichen_Markt_definieren
        param_13 = arcpy.Parameter()
        param_13.name = u'Einen_zus\xe4tzlichen_Markt_definieren'
        param_13.displayName = u'Einen zus\xe4tzlichen Markt definieren'
        param_13.parameterType = 'Optional'
        param_13.direction = 'Input'
        param_13.datatype = u'Boolesch'

        # Status
        param_14 = arcpy.Parameter()
        param_14.name = u'Status'
        param_14.displayName = u'Status'
        param_14.parameterType = 'Optional'
        param_14.direction = 'Input'
        param_14.datatype = u'Zeichenfolge'
        param_14.value = u'Zum Abspeichern eines zweiten Marktes Checkbox anklicken oder mit Ok einen Markt abspeichern und beenden'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6, 
                      param_7, param_8, param_9, param_10, param_11, param_12, 
                      param_13, param_14]

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
        T2_Hinzufuegen_neuen_Marktes.main(parameters, messages)      
        

class MaerkteLaden(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx\01Lebensmittelmaerkteeinladen"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)        
        
            i = 0
            self.params[i].filter.list = list_projects
            self.Projekt= i
            i+=1
            self.Pfad = i # für template
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parmater
            has been changed."""
            i=-1
            i+=1 
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname=self.params[0].value
        
                if os.path.isfile(os.path.join(BASE_PATH,'3_Projekte',projectname,"Bestandsliste_Supermaerkte.xls"))==False:
                        shutil.copyfile(os.path.join(BASE_PATH,'2_Tool','G_Standortkonkurrenz_Supermaerkte','Template_Maerkte_Standorte.xls'),os.path.join(BASE_PATH,'3_Projekte',projectname,"Bestandsliste_Supermaerkte.xls"))
        
                
                ##tablepath_siedlungszellen = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Siedlungszahlendaten')
                tablepath_template_maerkte = os.path.join(BASE_PATH,'3_Projekte',projectname,'Bestandsliste_Supermaerkte.xls')
                self.params[1].value=tablepath_template_maerkte
                ##self.params[2].value=tablepath_siedlungszellen
        
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    
    def __init__(self):
        self.label = u'1 Lebensmittelm\xe4rkte und Punktlayer einladen'
        self.canRunInBackground = False
        reload(T1_Lebensmittelmaerkte_einlesen)
    def getParameterInfo(self):
        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Bestandsliste_Supermärkte
        param_2 = arcpy.Parameter()
        param_2.name = u'Bestandsliste_Superm\xe4rkte'
        param_2.displayName = u'Bestandsliste Superm\xe4rkte'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Datei'

        # Punktfeature_für_Bevölkerungsmodellierung
        param_3 = arcpy.Parameter()
        param_3.name = u'Punktfeature_f\xfcr_Bev\xf6lkerungsmodellierung'
        param_3.displayName = u'Punktfeature f\xfcr Bev\xf6lkerungsmodellierung'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Feature-Class'

        parameters = [param_1, param_2, param_3]

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
        T1_Lebensmittelmaerkte_einlesen.main(parameters, messages)      
            

class Standortkonkurrenz(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx\05StartendesStandortkonkurrenzSupermaerktetools"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
        
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)
        
            i = 0
            self.params[i].filter.list = list_projects
            self.Projekt= i
            i+=1
            self.Maerkteshp = i
            i+=1
            self.Siedlungsshp = i
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parmater
            has been changed."""
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    
    def __init__(self):
        self.label = u'5 Starten_des_Standortkonkurrenz_Supermaerktetools'
        self.canRunInBackground = False
        reload(T5_StandortkonkurrenzSupermaerkteTool)
    def getParameterInfo(self):
        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        parameters = [param_1]

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
        T5_StandortkonkurrenzSupermaerkteTool.main(parameters, messages)            
            

class DefinitionZentren(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx\03DefinitionZentren"""
    # -*- coding: utf-8 -*-
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
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)
        
            i=-1
            i+=1 ;
            #set project
            self.params[i].filter.list = list_projects
        
            i+=1 ;
            #zentren
            i+=1 ;
            self.params[i].filter.list = []
                
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            i=-1
            i+=1
        
            list_uebergabepunkte =[]
        
            self.params[4].value = "Zum Speichern bitte das Kästchen anklicken"
        
            if (self.params[i].altered and not self.params[i].hasBeenValidated or self.params[1].altered and not self.params[1].hasBeenValidated ):
        
                projectname = self.params[0].value
        
                tablepath_maerkte = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Standortdaten')
        
                rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
                list_uebergabepunkte=[]
                for row in rows_uebergabepunkte :
                ##               list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
                    list_uebergabepunkte.append( str(row.Id) +" | "+ repr(row.Betriebstyp).replace('u','',1).replace("'",'')+ " | "+row.Strasse +" "+row.HNR + " "+ row.Ort + " | " + row.Ortsteil + " | "+ str(row.VKFL_gesamt) +" qm")
        
                del tablepath_maerkte,rows_uebergabepunkte
        
                tablepath_c_zentrenheck = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')
        
                cur_loescher= arcpy.SearchCursor(tablepath_c_zentrenheck)
        
                for row_zent in cur_loescher:
                    for stelle,liste in enumerate( list_uebergabepunkte):
        
                        if row_zent.Markt_1 == int( liste.split(' | ')[0]):
                            list_uebergabepunkte.pop(stelle)
        
                try:
                    del row_zent
                except:
                    pass
                del cur_loescher,tablepath_c_zentrenheck       
        
                self.params[2].filter.list = list_uebergabepunkte
                
            if self.params[3].value == True and not self.params[3].hasBeenValidated:
                if (self.params[2].value!=""):
        ##                try:
                    projectname = self.params[0].value
                    tabelle_zentren =os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')

                    Zentrum = str(self.params[1].value)
                    Markt_1 = int(repr(self.params[2].value).split(' | ')[0].replace("u",'').replace("'",''))

                    #Step 3: Insert new row with given values
                    Insert = arcpy.InsertCursor(tabelle_zentren)
                    row = Insert.newRow()
                    row.Zentren = Zentrum
                    row.Markt_1 = Markt_1

                    Insert.insertRow(row)


                    del tabelle_zentren, Insert


                    self.params[4].value ="Die Eingaben für das Zentrum " + str(self.params[1].value) + " wurden gespeichert. Geben Sie weitere Märkte zu diesem Zentrum an oder beenden Sie die Eingabe mit 'OK'"
                    self.params[3].value = False
                    self.params[2].value = ""
##                    self.params[1].value = ""

                    tablepath_maerkte = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Standortdaten')

                    rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
                    list_uebergabepunkte=[]
                    for row in rows_uebergabepunkte :
                    ##               list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
                        list_uebergabepunkte.append( str(row.Id) +" | "+ repr(row.Betriebstyp).replace('u','').replace("'",'')+ " | "+row.Strasse +" "+row.HNR + " "+ row.Ort + " | " + row.Ortsteil + " | "+str(row.VKFL_gesamt)+" qm")

                    del tablepath_maerkte,rows_uebergabepunkte



                    tablepath_c_zentrenheck = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')

                    cur_loescher= arcpy.SearchCursor(tablepath_c_zentrenheck)

                    for row_zent in cur_loescher:
                        for stelle,liste in enumerate( list_uebergabepunkte):

                            if row_zent.Markt_1 == int( liste.split(' | ')[0]):
                                list_uebergabepunkte.pop(stelle)


                    del row_zent,cur_loescher,tablepath_c_zentrenheck


                    self.params[2].filter.list = list_uebergabepunkte
                    self.params[2].value = list_uebergabepunkte[0]
        
        ##                except:
        ##                    self.params[2].value = ""
        ##                    self.params[3].value = False
        ##                    self.params[4].value ="ERROR - Fehler in der Eingabe "
        ##                    return
        
                else:
        
                    self.params[2].value = ""
                    self.params[1].value = ""
                    self.params[3].value = False
                    self.params[4].value ="ERROR - Nichts eingegeben! "
                    return
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    def __init__(self):
        self.label = u'3 Definition von Zentren'
        self.canRunInBackground = False
        reload(T3_Definition_Zentren)
    def getParameterInfo(self):
        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Zentrenbezeichnung
        param_2 = arcpy.Parameter()
        param_2.name = u'Zentrenbezeichnung'
        param_2.displayName = u'Zentrenbezeichnung'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Auswahl_der_Märkte
        param_3 = arcpy.Parameter()
        param_3.name = u'Auswahl_der_M\xe4rkte'
        param_3.displayName = u'Auswahl der M\xe4rkte'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'

        # Speichern
        param_4 = arcpy.Parameter()
        param_4.name = u'Speichern'
        param_4.displayName = u'Speichern'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Boolesch'

        # Status
        param_5 = arcpy.Parameter()
        param_5.name = u'Status'
        param_5.displayName = u'Status'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Zeichenfolge'

        parameters = [param_1, param_2, param_3, param_4, param_5]

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
        T3_Definition_Zentren.main(parameters, messages)
            

class ZentrenBearbeiten(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\G_Standortkonkurrenz_Supermaerkte\G_Standortkonkurrenz_Supermaerkte.tbx\04Zentrenbearbeiten"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
      
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)
        
            i=-1
        
            #set project
            i+=1 
            self.params[i].filter.list = list_projects
            self.params[3].enabled = 0
            self.params[3].value = "Bitte wählen Sie das Projekt aus"
            return
      
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            i=-1
            i+=1
        
            #nach Projektauswahl die Dropdownliste für die Flächennutzungen füllen
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value
        
                tabelle_gebaeude = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')
                rows_gebaeude = arcpy.SearchCursor(tabelle_gebaeude)
                list_gebaeude = []
                for row in rows_gebaeude :
                    gefunden=0
                    for zen in list_gebaeude:
                ##        print str(zen).split(' | ')[0].replace ("[u'",'')
                        if row.Zentren == str(zen).split(' | ')[0].replace ("[u'",''):
                            zen.append(" | " + str( row.Markt_1 ))
                ##            print list_gebaeude
                            gefunden=1
                            break
                    try:
                        del zen
                    except:
                        pass
        
                    if gefunden==0:
                        list_gebaeude.append([(row.Zentren) + " | " + str( row.Markt_1 )] )
                list_neu=[]
                for a in list_gebaeude:
        
                    print str(a).replace("[u'",'').replace(',','').replace("' '",'').replace("']",'')
                    list_neu.append(str(a).replace("[u'",'').replace(',','').replace("' '",'').replace("']",''))
        
                list_gebaeude= list_neu
                list_gebaeude  = list(set(list_gebaeude))
        
        
                del tabelle_gebaeude,rows_gebaeude
        
        
                i+=1 ; self.params[i].filter.list = list_gebaeude
                self.params[3].value = "Bitte wählen Sie das zu bearbeitende Zentrum aus"
            if self.params[1].altered and not self.params[1].hasBeenValidated:
                self.params[3].value = "Um den ausgewählten Eintrag zu löschen, klicken Sie bitte auf Löschen"
        
        #ausgewählte Vornutzung löschen
            if self.params[2].altered and not self.params[2].hasBeenValidated:
                parameterString = self.params[1].value
                zentrum = parameterString.split(" | ")[0]
                markt1 = parameterString.split(" | ")[1]
        
        
                self.params[3].value = zentrum + " "+markt1
        
                projectname = self.params[0].value
                tabelle_gebaeude = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')
                Update = arcpy.UpdateCursor(tabelle_gebaeude)
                for row in Update:
                    if(str(row.Zentren) == str(zentrum)):
                        Update.deleteRow(row)
                        self.params[3].value = parameterString + " geloescht"
                        self.params[2].value = False
                #Den Filter für die vorhandenen Vornutzungen neu erstellen und den angezeigten Wert auf den ersten Listenwert setzen
                tabelle_gebaeude = os.path.join(BASE_PATH,'3_Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projectname+'.gdb','Zentren')
                rows_gebaeude = arcpy.SearchCursor(tabelle_gebaeude)
                list_gebaeude = []
                for row in rows_gebaeude :
                    gefunden=0
                    for zen in list_gebaeude:
                ##        print str(zen).split(' | ')[0].replace ("[u'",'')
                        if row.Zentren == str(zen).split(' | ')[0].replace ("[u'",''):
                            zen.append(" | " + str( row.Markt_1 ))
                ##            print list_gebaeude
                            gefunden=1
                            break
                    try:
                        del zen
                    except:
                        pass
        
                    if gefunden==0:
                        list_gebaeude.append([(row.Zentren) + " | " + str( row.Markt_1 )] )
                list_neu=[]
                for a in list_gebaeude:
        
                    print str(a).replace("[u'",'').replace(',','').replace("' '",'').replace("']",'')
                    list_neu.append(str(a).replace("[u'",'').replace(',','').replace("' '",'').replace("']",''))
        
                list_gebaeude= list_neu
                self.params[1].filter.list= list_gebaeude
        #        i+=1 ; self.params[1].filter.list = list_gebaeude
        
                #Liste nur füllen wenn noch Einträge vorhanden sind. Except leert die Liste
                try:
                    self.params[1].value = list_gebaeude[0]
                except:
                    self.params[1].value = ""
                   #pass
                self.params[3].value = "Bitte wählen Sie das zu bearbeitende Zentrum aus"
        
            return
      
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return
    
    def __init__(self):
        self.label = u'4 Zentren bearbeiten'
        self.canRunInBackground = False
        reload(T4_Zentren_bearbeiten)
    def getParameterInfo(self):
        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Eingegebene_Zentren
        param_2 = arcpy.Parameter()
        param_2.name = u'Eingegebene_Zentren'
        param_2.displayName = u'Eingegebene Zentren'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Löschen
        param_3 = arcpy.Parameter()
        param_3.name = u'L\xf6schen'
        param_3.displayName = u'L\xf6schen'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Boolesch'

        # Status
        param_4 = arcpy.Parameter()
        param_4.name = u'Status'
        param_4.displayName = u'Status'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Zeichenfolge'
        param_4.value = u'Bitte w\xe4hlen Sie das Projekt aus'

        parameters = [param_1, param_2, param_3, param_4]

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
        T4_Zentren_bearbeiten.main(parameters, messages)
            
            