# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.standortkonkurrenz.T2_Hinzufuegen_neuen_Marktes import MarktHinzufuegen

class TbxMarktHinzufuegen(Tbx):

    @property
    def label(self):
        return encode(u'Neuen Markt hinzufügen')

    @property
    def Tool(self):
        return MarktHinzufuegen

    def _getParameterInfo(self):

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

        # Projektauswahl
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektauswahl'
        param_1.displayName = u'Projektauswahl'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = []

        # Anbieter_des_Marktes
        param_2 = arcpy.Parameter()
        param_2.name = u'Anbieter_des_Marktes'
        param_2.displayName = u'Anbieter des Marktes'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = language('string')
        param_2.filter.list = [u'Aktiv-Discount', u'Aldi', u'Alnatura', u'basic', u'biocompany', u'Biomarkt', u'Coma', u'Combi', u'denns', u'diska', u'Edeka', u'famila', u'globus', u'HIT', u'Jibi', u'K + K (Klaas & Kock)', u'Kaufland', u'Konsum-Leipzig', u'Lidl', u'Markant', u'Marktkauf', u'Migros', u'Mix-Markt', u'nahkauf', u'Netto', u'Netto(Edeka)', u'Norma', u'NP', u'Penny', u'Perfetto (Karstadt)', u'Plaza', u'Real', u'Rewe', u'Sky', u'Sonstige', u'Tegut', u'Toom', u'treff 3000', u'vitalia', u'viv', u'V-Markt', u'Wasgau', u'WEZ']

        # Neuer_Anbieter__bei_Auswahl_von_Sonstige_
        param_3 = arcpy.Parameter()
        param_3.name = u'Neuer_Anbieter__bei_Auswahl_von_Sonstige_'
        param_3.displayName = u'Neuer Anbieter (bei Auswahl von Sonstige)'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = language('string')

        # Ja__es_handelt_sich_um_einen_Discounter
        param_4 = arcpy.Parameter()
        param_4.name = u'Ja__es_handelt_sich_um_einen_Discounter'
        param_4.displayName = u'Ja, es handelt sich um einen Discounter'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = language('boolean')

        # Verkaufsfl�che_gesamt__m2_
        param_5 = arcpy.Parameter()
        param_5.name = u'Verkaufsfl\xe4che_gesamt__m2_'
        param_5.displayName = u'Verkaufsfl\xe4che gesamt (m2)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = language('string')

        # Stra�e
        param_6 = arcpy.Parameter()
        param_6.name = u'Stra\xdfe'
        param_6.displayName = u'Stra\xdfe'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = language('string')

        # Hausnummer
        param_7 = arcpy.Parameter()
        param_7.name = u'Hausnummer'
        param_7.displayName = u'Hausnummer'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = language('string')

        # Postleitzahl
        param_8 = arcpy.Parameter()
        param_8.name = u'Postleitzahl'
        param_8.displayName = u'Postleitzahl'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = language('string')

        # Ort
        param_9 = arcpy.Parameter()
        param_9.name = u'Ort'
        param_9.displayName = u'Ort'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = language('string')

        # Ortsteil
        param_10 = arcpy.Parameter()
        param_10.name = u'Ortsteil'
        param_10.displayName = u'Ortsteil'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = language('string')

        # Handelt_es_sich_bei_dem_neuen_Markt_um_eine_Erweiterung_oder_einen_neuen_Markt_
        param_11 = arcpy.Parameter()
        param_11.name = u'Handelt_es_sich_bei_dem_neuen_Markt_um_eine_Erweiterung_oder_einen_neuen_Markt_'
        param_11.displayName = u'Handelt es sich bei dem neuen Markt um eine Erweiterung oder einen neuen Markt?'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = language('string')
        param_11.filter.list = [u'Erweiterung', u'Neuen Markt']

        # Markterweiterung_wurde_ausgew�hlt__Welcher_Markt_soll_erweitert_werden_
        param_12 = arcpy.Parameter()
        param_12.name = u'Markterweiterung_wurde_ausgew\xe4hlt__Welcher_Markt_soll_erweitert_werden_'
        param_12.displayName = u'Markterweiterung wurde ausgew\xe4hlt. Welcher Markt soll erweitert werden?'
        param_12.parameterType = 'Optional'
        param_12.direction = 'Input'
        param_12.datatype = language('string')

        # Einen_zus�tzlichen_Markt_definieren
        param_13 = arcpy.Parameter()
        param_13.name = u'Einen_zus\xe4tzlichen_Markt_definieren'
        param_13.displayName = u'Einen zus\xe4tzlichen Markt definieren'
        param_13.parameterType = 'Optional'
        param_13.direction = 'Input'
        param_13.datatype = language('boolean')

        # Status
        param_14 = arcpy.Parameter()
        param_14.name = u'Status'
        param_14.displayName = u'Status'
        param_14.parameterType = 'Optional'
        param_14.direction = 'Input'
        param_14.datatype = language('string')
        param_14.value = u'Zum Abspeichern eines zweiten Marktes Checkbox anklicken oder mit Ok einen Markt abspeichern und beenden'

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6,
                      param_7, param_8, param_9, param_10, param_11, param_12,
                      param_13, param_14]

        validator = getattr(self, 'ToolValidator', None)
        if validator:
            validator(parameters).initializeParameters()

        self.updateParameters(parameters)

        return parameters



    def _updateParameters(self, params):


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

			tablepath_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')

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
			tabelle_zentren =join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Neuer_Markt_temp')
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
				self.params[13].value="Fehler keine Verkaufsfl�che eingegeben!"
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
					tablepath_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')

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






