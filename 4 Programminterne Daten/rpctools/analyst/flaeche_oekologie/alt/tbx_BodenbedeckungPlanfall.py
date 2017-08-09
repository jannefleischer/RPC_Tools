# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.flaeche_oekologie.Bodenbedeckungbeschreiben import BodenbedeckungPlanfall

class TbxBodenbedeckungPlanfall(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 2: Planfall beschreiben')

    @property
    def Tool(self):
        return BodenbedeckungPlanfall

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        # Teilfl�che
        param_2 = params.teilflaeche = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'
        list_teilflaechen = []
        param_2.filter.list = list_teilflaechen

        heading = encode("01_Bodenbedeckung")

        # Bodenbedeckung_auf_der_Teilfl�che
        param_3 = params.bodenflaeche = arcpy.Parameter()
        param_3.name = u'Bodenbedeckung_auf_der_Teilfl\xe4che'
        param_3.displayName = u'Bodenbedeckung auf der Teilfl\xe4che'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPString'
        param_3.filter.list = [u'Ueberbaute Flaechen', u'Natuerliche Wasserflaeche', u'Platten', u'Baeume, Straeucher', u'Wassergebundene Decke, Rasengittersteine', u'Stauden', u'Wiese', u'Asphalt, Beton', u'Offener Boden, Acker', u'Kleinpflaster', u'Rasen']

        # Anteil_an_der_Teilfl�che____
        param_4 = params.flaechenanteil = arcpy.Parameter()
        param_4.name = u'Anteil_an_der_Teilfl\xe4che____'
        param_4.displayName = u'Anteil an der Teilfl\xe4che (%)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = 0
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        heading = encode("02_Speichern")

        # Speichern
        param_5 = params.speichern = arcpy.Parameter()
        param_5.name = u'Speichern'
        param_5.displayName = u'Speichern'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'GPBoolean'
        param_5.enabled = False

        param_5.filter.list = [u'true', u'false']

        # Status
        param_6 = params.status = arcpy.Parameter()
        param_6.name = u'Status'
        param_6.displayName = u'Status'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPString'


        return params

    def _updateParameters(self, params):

        #Projekt auswaehlen
            i=-1
            i+=1

            self.params[5].value = "Bitte waehlen Sie das Projekt aus"

        #Wert i==0
            if self.params[i].altered and not self.params[i].hasBeenValidated:
                projectname = self.params[i].value

                tablepath_teilflaechen = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Definition_Projekt.gdb','Teilflaechen_Plangebiet')

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

                tablepath_teilflaechen = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Definition_Projekt.gdb','Teilflaechen_Plangebiet')
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
        #Fl�chengr��e der Teilfl�chen ermitteln um aus den Anteilen absolute Werte zu machen
                #Projektname
                projekt = self.params[0].value
                gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
                pfad_flaeche = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projekt,gdb,"Teilflaechen_Plangebiet")
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
                tabelle_bodenbedeckung = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Flaeche_und_Oekologie.gdb','Bodenbedeckung')
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

