# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.standortkonkurrenz.T3_Definition_Zentren import DefinitionZentren

class TbxDefinitionZentren(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 3: Zentren definieren')

    @property
    def Tool(self):
        return DefinitionZentren

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()




        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        # Zentrenbezeichnung
        param_2 = arcpy.Parameter()
        param_2.name = u'Zentrenbezeichnung'
        param_2.displayName = u'Zentrenbezeichnung'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'


        # Auswahl_der_M�rkte
        param_3 = arcpy.Parameter()
        param_3.name = u'Auswahl_der_M\xe4rkte'
        param_3.displayName = u'Auswahl der M\xe4rkte'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPString'
        param_3.filter.list = []

        # Speichern
        param_4 = arcpy.Parameter()
        param_4.name = u'Speichern'
        param_4.displayName = u'Speichern'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPBoolean'


        # Status
        param_5 = arcpy.Parameter()
        param_5.name = u'Status'
        param_5.displayName = u'Status'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPString'


        return params


    def _updateParameters(self, params):

		i=-1
		i+=1

		list_uebergabepunkte =[]

		self.params[4].value = "Zum Speichern bitte das Kästchen anklicken"

		if (self.params[i].altered and not self.params[i].hasBeenValidated or self.params[1].altered and not self.params[1].hasBeenValidated ):

			projectname = self.params[0].value

			tablepath_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')

			rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
			list_uebergabepunkte=[]
			for row in rows_uebergabepunkte :
			##               list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
				list_uebergabepunkte.append( str(row.Id) +" | "+ repr(row.Betriebstyp).replace('u','',1).replace("'",'')+ " | "+row.Strasse +" "+row.HNR + " "+ row.Ort + " | " + row.Ortsteil + " | "+ str(row.VKFL_gesamt) +" qm")

			del tablepath_maerkte,rows_uebergabepunkte

			tablepath_c_zentrenheck = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')

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
				tabelle_zentren =join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')

				Zentrum = str(self.params[1].value)
				Markt_1 = int(repr(self.params[2].value).split(' | ')[0].replace("u",'').replace("'",''))

				#Step 3: Insert new row with given values
				Insert = arcpy.InsertCursor(tabelle_zentren)
				row = Insert.newRow()
				row.Zentren = Zentrum
				row.Markt_1 = Markt_1

				Insert.insertRow(row)


				del tabelle_zentren, Insert


				self.params[4].value ="Die Eingaben f�r das Zentrum " + str(self.params[1].value) + " wurden gespeichert. Geben Sie weitere M�rkte zu diesem Zentrum an oder beenden Sie die Eingabe mit 'OK'"
				self.params[3].value = False
				self.params[2].value = ""
##                    self.params[1].value = ""

				tablepath_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')

				rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
				list_uebergabepunkte=[]
				for row in rows_uebergabepunkte :
				##               list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
					list_uebergabepunkte.append( str(row.Id) +" | "+ repr(row.Betriebstyp).replace('u','').replace("'",'')+ " | "+row.Strasse +" "+row.HNR + " "+ row.Ort + " | " + row.Ortsteil + " | "+str(row.VKFL_gesamt)+" qm")

				del tablepath_maerkte,rows_uebergabepunkte



				tablepath_c_zentrenheck = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')

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


