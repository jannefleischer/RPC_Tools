# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.standortkonkurrenz.T1_Lebensmittelmaerkte_einlesen import MarktEinlesen

class TbxMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 1: Märkte einlesen')

    @property
    def Tool(self):
        return MarktEinlesen

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

        # Bestandsliste_Superm�rkte
        param_2 = arcpy.Parameter()
        param_2.name = u'Bestandsliste_Superm\xe4rkte'
        param_2.displayName = u'Bestandsliste Superm\xe4rkte'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPDataFile'


        # Punktfeature_f�r_Bev�lkerungsmodellierung
        param_3 = arcpy.Parameter()
        param_3.name = u'Punktfeature_f\xfcr_Bev\xf6lkerungsmodellierung'
        param_3.displayName = u'Punktfeature f\xfcr Bev\xf6lkerungsmodellierung'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = language('feature class')


        return params

    def _updateParameters(self, params):

		i=-1
		i+=1
		if self.params[i].altered and not self.params[i].hasBeenValidated:
			projectname=self.params[0].value

			if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Bestandsliste_Supermaerkte.xls"))==False:
					shutil.copyfile(join(BASE_PATH,'2_Tool','Standortkonkurrenz_Supermaerkte','Template_Maerkte_Standorte.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Bestandsliste_Supermaerkte.xls"))


			##tablepath_siedlungszellen = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Siedlungszahlendaten')
			tablepath_template_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Bestandsliste_Supermaerkte.xls')
			self.params[1].value=tablepath_template_maerkte
			##self.params[2].value=tablepath_siedlungszellen

		return


