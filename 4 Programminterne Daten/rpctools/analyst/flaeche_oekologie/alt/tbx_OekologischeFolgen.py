# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.flaeche_oekologie.oekologische_folgen import OekologischeFolgen

class TbxOekologischeFolgen(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 5: Ökologische Folgen berechnen')

    @property
    def Tool(self):
        return OekologischeFolgen

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

        # Region_ausw�hlen
        param_2 = params.projectname = arcpy.Parameter()
        param_2.name = u'Region_ausw\xe4hlen'
        param_2.displayName = u'Region ausw\xe4hlen'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'

        param_2.filter.list = [u'Braunschweig-Salzgitter-Wolfenbuettel', u'In und um Duesseldorf', u'Kreis Euskirchen', u'Kreis Unna', u'Landkreis Harburg', u'Landkreis Wolfenbuettel', u'Rheinisch-Bergischer Kreis']

        # L�nge_der_gemeinsamen_Grenze_Planfl�che_Gemeinde__m_
        param_3 = params.gemeinsameGrenze = arcpy.Parameter()
        param_3.name = u'L\xe4nge_der_gemeinsamen_Grenze_Planfl\xe4che_Gemeinde__m_'
        param_3.displayName = u'L\xe4nge der gemeinsamen Grenze Planfl\xe4che|Gemeinde (m)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Double'

        # L�nge_der_gesamten_Grenze_der_Planfl�che__m_
        param_4 = params.gesamteGrenze = arcpy.Parameter()
        param_4.name = u'L\xe4nge_der_gesamten_Grenze_der_Planfl\xe4che__m_'
        param_4.displayName = u'L\xe4nge der gesamten Grenze der Planfl\xe4che (m)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Double'

        # Was_wird_haupts�chlich_auf_der_Projektfl�che_errichtet_
        param_5 = params.Bauart = arcpy.Parameter()
        param_5.name = u'Was_wird_haupts\xe4chlich_auf_der_Projektfl\xe4che_errichtet_'
        param_5.displayName = u'Was wird haupts\xe4chlich auf der Projektfl\xe4che errichtet?'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPString'

        param_5.filter.list = [u'Wohnen', u'Gewerbe', u'Einzelhandel']

        # Sind_schutzw�rdige_B�den_betroffen_
        param_6 = params.Schutzwuerdig = arcpy.Parameter()
        param_6.name = u'Sind_schutzw\xfcrdige_B\xf6den_betroffen_'
        param_6.displayName = u'Sind schutzw\xfcrdige B\xf6den betroffen?'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPString'

        param_6.filter.list = [u'Ja', u'Nein']

        return params



    def _updateParameters(self, params):

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
    #            pfad_flaeche = join(base_path,'3 Benutzerdefinierte Projekte',projekt,gdb,"Teilflaechen_Plangebiet")

    #            arcpy.AddField_management(pfad_flaeche,"area_hektares","FLOAT")
    #            arcpy.CalculateField_management(pfad_flaeche,"area_hektares","!shape.area@HECTARES!","PYTHON_9.3")

    #            flaechengroesse = 0
    #            cursor = arcpy.SearchCursor(pfad_flaeche)
    #            for flaeche in cursor:
    #                flaechengroesse = flaechengroesse + flaeche.area_hektares
    #            flaechengroesse = str(flaechengroesse).replace(",",".")
    #            self.params[4].value = flaechengroesse

            if self.params[i].altered and not self.params[i].hasBeenValidated:
                #Projektname
                projekt = self.params[i].value
                gdb = "FGDB_Definition_Projekt_" + projekt + ".gdb"
                pfad_umfang = join(BASE_PATH,'3 Benutzerdefinierte Projekte',projekt,gdb,"Teilflaechen_Plangebiet")


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

		return


