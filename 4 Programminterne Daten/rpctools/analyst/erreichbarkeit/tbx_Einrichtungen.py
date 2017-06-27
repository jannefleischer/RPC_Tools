# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.erreichbarkeit.T4_Erreichbarkeit_Einrichtungen import Einrichtungen

class TbxEinrichtungen(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 2: Einrichtungen einlesen')

    @property
    def Tool(self):
        return Einrichtungen

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        i=-1
        i+=1 ;
        self.Projekt= i
        i+=1
        self.Bereitsvorhandene=i
        i+=1
        self.Kita=i
        i+=1
        self.Grundschulen=i
        i+=1
        self.Arzt=i
        i+=1
        self.Apotheken=i
        i+=1
        self.Krankenhaeuser=i
        i+=1
        self.Sonstige=i
        i+=1
        self.BooleanEinzel=i
        i+=1
        self.Einzelhandel=i
        i+=1
        self.Einzelhandel_feature=i

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

        # Bereits_eingeladene_Einrichtung_f�r_das_Projekt_verwenden
        param_2 = params.projectname = arcpy.Parameter()
        param_2.name = u'Bereits_eingeladene_Einrichtung_f\xfcr_das_Projekt_verwenden'
        param_2.displayName = u'Bereits geladene Einrichtung f\xfcr das Projekt verwenden'
        param_2.parameterType = 'Optional'
        param_2.direction = 'Input'
        param_2.datatype = u'GPBoolean'


        # Kita
        param_3 = params.kita = arcpy.Parameter()
        param_3.name = u'Kita'
        param_3.displayName = u'Kita'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPDataFile'


        # Grundschulen
        param_4 = params.grundschule = arcpy.Parameter()
        param_4.name = u'Grundschulen'
        param_4.displayName = u'Grundschulen'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPDataFile'


        # Allgemein_Mediziner
        param_5 = params.arzt = arcpy.Parameter()
        param_5.name = u'Allgemein_Mediziner'
        param_5.displayName = u'Allgemein Mediziner'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPDataFile'


        # Apotheken
        param_6 = params.apotheke = arcpy.Parameter()
        param_6.name = u'Apotheken'
        param_6.displayName = u'Apotheken'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPDataFile'


        # Krankenh�user
        param_7 = params.krankenhaus = arcpy.Parameter()
        param_7.name = u'Krankenh\xe4user'
        param_7.displayName = u'Krankenh\xe4user'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'GPDataFile'


        # Sonstige
        param_8 = params.sonstige = arcpy.Parameter()
        param_8.name = u'Sonstige'
        param_8.displayName = u'Sonstige'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'GPDataFile'


        # Einzelhandelstandorte_aus_34_Versorgung_�bernehmen
        param_9 = params.ehs1 = arcpy.Parameter()
        param_9.name = u'Einzelhandelstandorte_aus_34_Versorgung_\xfcbernehmen'
        param_9.displayName = u'Einzelhandelstandorte aus Toolbox "Standardversorgung" \xfcbernehmen'.encode('CP1252')
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = u'GPBoolean'


        # Einzelhandelstandorte
        param_10 = params.ehs2 = arcpy.Parameter()
        param_10.name = u'Einzelhandelstandorte'
        param_10.displayName = u'Einzelhandelstandorte'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'GPDataFile'


        # Einzelhandelstandorte_aus_Toolbox_34_Versorgung
        param_11 = params.ehs3 = arcpy.Parameter()
        param_11.name = u'Einzelhandelstandorte_aus_Toolbox_34_Versorgung'
        param_11.displayName = u'Einzelhandelstandorte aus Toolbox "Standardversorgung"'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = language('feature class')


        return params


    def _updateParameters(self, params):

        i=-1
        i+=1 ;
        #Immer aus
        self.params[self.Einzelhandel_feature].enabled=0
        #Projekt
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            projectname=self.params[0].value

            #check ob alle 5 template excel datein vorhanden
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Kindertagesstaetten.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Kitas_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Kindertagesstaetten.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Grundschulen.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Grundschulen_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Grundschulen.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Einzelhandel.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Einzelhandel_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Einzelhandel.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Apotheken.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Apotheken_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Apotheken.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Aerzte.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Aerzte_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Aerzte.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Krankenhaeuser.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Krankenhaeuser_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Krankenhaeuser.xls"))
            if os.path.isfile(join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Sonstige.xls"))==False:
                shutil.copyfile(join(BASE_PATH,'2_Tool','Erreichbarkeit','Einrichtungen_Sonstige_template.xls'),join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,"Einrichtungen_Sonstige.xls"))


            tablepath_template_kitas =  join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Kindertagesstaetten.xls')
            tablepath_template_grundschulen = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Grundschulen.xls')
            tablepath_template_einzelhandel = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Einzelhandel.xls')
            tablepath_template_apotheken = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Apotheken.xls')
            tablepath_template_aerzte = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Aerzte.xls')
            tablepath_template_kh = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Krankenhaeuser.xls')
            tablepath_template_sons = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Sonstige.xls')

            self.params[self.Kita].value=tablepath_template_kitas
            self.params[self.Grundschulen].value=tablepath_template_grundschulen
            self.params[self.Einzelhandel].value=tablepath_template_einzelhandel
            self.params[self.Apotheken].value=tablepath_template_apotheken
            self.params[self.Arzt].value=tablepath_template_aerzte
            self.params[self.Krankenhaeuser].value=tablepath_template_kh
            self.params[self.Sonstige].value=tablepath_template_sons

        i+=1
        #Booleanabfrage
        if self.params[i].value==True:
            #Alle Eingaben sperren da schon Datenvorhanden die genutzt werden sollen
            self.params[self.Kita].enabled=0
            self.params[self.Grundschulen].enabled=0
            self.params[self.Arzt].enabled=0
            self.params[self.Einzelhandel].enabled=0
            self.params[self.Apotheken].enabled=0
            self.params[self.Krankenhaeuser].enabled=0
            self.params[self.Sonstige].enabled=0

            self.params[self.BooleanEinzel].enabled=0
            self.params[self.Einzelhandel].enabled=0
            self.params[self.Einzelhandel_feature].enabled=0

        else:
            self.params[self.Kita].enabled=1
            self.params[self.Grundschulen].enabled=1
            self.params[self.Arzt].enabled=1
            self.params[self.Einzelhandel].enabled=1
            self.params[self.Apotheken].enabled=1
            self.params[self.Krankenhaeuser].enabled=1
            self.params[self.Sonstige].enabled=1


            self.params[self.BooleanEinzel].enabled=1

        if self.params[self.BooleanEinzel].value==True:
            projectname=self.params[0].value
            tablepath_einzelhandel = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')
            self.params[self.Einzelhandel_feature].value=tablepath_einzelhandel
            self.params[self.Einzelhandel].enabled=0
            self.params[self.Einzelhandel_feature].enabled=1
        elif self.params[self.Projekt].value!=None and self.params[self.Kita].enabled!=0:
            projectname=self.params[0].value
            tablepath_template_einzelhandel = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projectname,'Einrichtungen_Einzelhandel.xls')
            self.params[self.Einzelhandel].value=tablepath_template_einzelhandel
            self.params[self.Einzelhandel].enabled=1
            self.params[self.Einzelhandel_feature].enabled=0

        return



