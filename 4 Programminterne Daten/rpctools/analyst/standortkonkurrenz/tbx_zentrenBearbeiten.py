# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.standortkonkurrenz.T4_Zentren_bearbeiten import ZentrenBearbeiten

class TbxZentrenBearbeitenn(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 4: Zentren bearbeiten')

    @property
    def Tool(self):
        return ZentrenBearbeiten

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

        # Eingegebene_Zentren
        param_2 = arcpy.Parameter()
        param_2.name = u'Eingegebene_Zentren'
        param_2.displayName = u'Eingegebene Zentren'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'


        # L�schen
        param_3 = arcpy.Parameter()
        param_3.name = u'L\xf6schen'
        param_3.displayName = u'L\xf6schen'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPBoolean'


        # Status
        param_4 = arcpy.Parameter()
        param_4.name = u'Status'
        param_4.displayName = u'Status'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPString'

        param_4.value = u'Bitte w\xe4hlen Sie das Projekt aus'

        return params


    def _updateParameters(self, params):

		i=-1
		i+=1

		#nach Projektauswahl die Dropdownliste f�r die Fl�chennutzungen f�llen
		if self.params[i].altered and not self.params[i].hasBeenValidated:
			projectname = self.params[i].value

			tabelle_gebaeude = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')
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
			self.params[3].value = "Bitte w�hlen Sie das zu bearbeitende Zentrum aus"
		if self.params[1].altered and not self.params[1].hasBeenValidated:
			self.params[3].value = "Um den ausgew�hlten Eintrag zu l�schen, klicken Sie bitte auf L�schen"

	#ausgew�hlte Vornutzung l�schen
		if self.params[2].altered and not self.params[2].hasBeenValidated:
			parameterString = self.params[1].value
			zentrum = parameterString.split(" | ")[0]
			markt1 = parameterString.split(" | ")[1]


			self.params[3].value = zentrum + " "+markt1

			projectname = self.params[0].value
			tabelle_gebaeude = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')
			Update = arcpy.UpdateCursor(tabelle_gebaeude)
			for row in Update:
				if(str(row.Zentren) == str(zentrum)):
					Update.deleteRow(row)
					self.params[3].value = parameterString + " geloescht"
					self.params[2].value = False
			#Den Filter f�r die vorhandenen Vornutzungen neu erstellen und den angezeigten Wert auf den ersten Listenwert setzen
			tabelle_gebaeude = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Zentren')
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

			#Liste nur f�llen wenn noch Eintr�ge vorhanden sind. Except leert die Liste
			try:
				self.params[1].value = list_gebaeude[0]
			except:
				self.params[1].value = ""
			   #pass
			self.params[3].value = "Bitte w�hlen Sie das zu bearbeitende Zentrum aus"

		return

