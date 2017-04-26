# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.standortkonkurrenz.T1_Lebensmittelmaerkte_einlesen \
     import MarktEinlesen

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
        param = params.projectname = arcpy.Parameter()
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = projekte
        if projekte:
            param.value = projekte[0]

        # Bestandsliste_Supermärkte
        param = params.bestand = arcpy.Parameter()
        param.name = encode(u'Bestandsliste_Supermärkte')
        param.displayName = encode(u'Bestandsliste Supermärkte')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPDataFile'

        # Punktfeature_für_Bevölkerungsmodellierung
        param = params.feature = arcpy.Parameter()
        param.name = encode(u'Punktfeature_für_Bevölkerungsmodellierung')
        param.displayName = encode(u'Punktfeature für '
                                   u'Bevölkerungsmodellierung')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = 'GPFeatureLayer'

        return params

    def _updateParameters(self, params):   
        #if self.par.changed('projectname'):
            #projectname = params.projectname.value
            #target = os.path.join(self.folders.get_projectpath(),
                                  #"Bestandsliste_Supermaerkte.xls")

            #if not os.path.exists(target):
                #source = 
                #shutil.copyfile(join(BASE_PATH,'2_Tool','Standortkonkurrenz_Supermaerkte','Template_Maerkte_Standorte.xls'),
                                #target)


            ###tablepath_siedlungszellen = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Siedlungszahlendaten')
            #tablepath_template_maerkte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Bestandsliste_Supermaerkte.xls')
            #self.params[1].value=tablepath_template_maerkte
            ##self.params[2].value=tablepath_siedlungszellen

        return params


