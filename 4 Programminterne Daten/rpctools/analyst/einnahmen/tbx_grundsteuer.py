# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.config import Folders as folders
from rpctools.analyst.einnahmen.script_Grundsteuer import Grundsteuer


class TbxGrundsteuer(Tbx):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'Schritt 4: Grundsteuer'

    @property
    def Tool(self):
        return Grundsteuer

    def _getParameterInfo(self):

        params = self.par

        # Projektname
        param = params.name = arcpy.Parameter()
        param.name = u'Projektname'
        param.displayName = u'Projektname'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        heading = "1 Hebesatz Grundsteuer B in der Projektgemeinde"

        param = params.slider1 = arcpy.Parameter()
        param.name = u'HebesatzB'
        param.displayName = u'als von-Hundert-Satz'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [50, 500]
        param.category = heading

        heading = u"2 Wohnen: Jahresrohmieten nach Ertragswertverfahren (alte Bundesländer)"

        param = params.slider2 = arcpy.Parameter()
        param.name = u'efh'
        param.displayName = u'Einfamilienhaus (Jahresrohmiete 1964 pro qm Wohnfläche) in Euro-Cent pro Monat'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [30, 500]
        param.category = heading

        param = params.slider3 = arcpy.Parameter()
        param.name = u'dh'
        param.displayName = u'Doppelhaus (Jahresrohmiete 1964 pro qm Wohnfläche) in Euro-Cent pro Monat'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [30, 500]
        param.category = heading

        param = params.slider4 = arcpy.Parameter()
        param.name = u'rh'
        param.displayName = u'Reihenhaus (Jahresrohmiete 1964 pro qm Wohnfläche) in Euro-Cent pro Monat'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [30, 500]
        param.category = heading

        param = params.slider5 = arcpy.Parameter()
        param.name = u'mfh'
        param.displayName = u'Mehrfamilienhaus (Jahresrohmiete 1964 pro qm Wohnfläche) in Euro-Cent pro Monat'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [30, 500]
        param.category = heading


        heading = u"3 Wohnen: Bodenwert nach Sachwertverfahren (Einfamilienhäuser in den neuen Bundesländern)"

        param = params.slider6 = arcpy.Parameter()
        param.name = u'bodenwert'
        param.displayName = u'Bodenwert 1935 in Euro-Cent pro Quadratmeter (im Sinne des Sachwertverfahrens)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [30, 800]
        param.category = heading

        param = params.slider7 = arcpy.Parameter()
        param.name = u'groesse_efh'
        param.displayName = u'Mittlere Größe der Einfamilienhausgrundstücke'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [300, 2000]
        param.category = heading


        heading = u"4 Gewerbe/Einzelhandel: Voraussichtliches Bauvolumen"

        param = params.slider8 = arcpy.Parameter()
        param.name = u'bueroflaeche'
        param.displayName = u'Bürofläche: qm Brutto-Grundfläche (BGF)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Double'
        param.value = 0
        param.category = heading

        param = params.slider9 = arcpy.Parameter()
        param.name = u'lagerflaeche'
        param.displayName = u'Hallen und Lagerfläche: qm Brutto-Grundfläche (BGF)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Double'
        param.value = 0
        param.category = heading

        return params


    def eingaben_auslesen(self, params):

        fields = ['AGS', 'Gemeindetyp']
        folder = folders()
        tablepath_rahmendaten = folder.get_table('Projektrahmendaten', "FGDB_Definition_Projekt.gdb", params.name.value)
        cursor = arcpy.da.SearchCursor(tablepath_rahmendaten, fields)
        for row in cursor:
            ags = row[0]
            gemeindetyp = row[1]

        fields = ['AGS', 'Hebesatz_GrStB']
        where_clause = '"AGS"' + "= '" + ags + "'"
        cursor = self.query_table('bkg_gemeinden', fields, "FGDB_Basisdaten_deutschland.gdb", where_clause, is_base_table = True)
        for row in cursor:
            params.slider1.value = row[1]

        fields = ["EFH_Rohmiete", 'DHH_Rohmiete', 'RHW_Rohmiete', 'MFH_Rohmiete', 'Bodenwert_Sachwertverfahren', 'qm_Grundstueck_pro_WE_EFH', 'BGF_Buero', 'BGF_Halle']
        cursor = self.query_table('GrSt_Basisdaten', fields)
        if cursor:
            for row in cursor:
                params.slider2.value = row[0]
                params.slider3.value = row[1]
                params.slider4.value = row[2]
                params.slider5.value = row[3]
                params.slider6.value = row[4]
                params.slider7.value = row[5]
                params.slider8.value = row[6]
                params.slider9.value = row[7]
        else:
            fields = ['Gemeindetyp', "EFH_Rohmiete", 'DHH_Rohmiete', 'RHW_Rohmiete', 'MFH_Rohmiete', 'Bodenwert_SWV', 'qm_Grundstueck_pro_WE_EFH']
            where_clause = '"Gemeindetyp"' + " = " + str(gemeindetyp)
            cursor = self.query_table('GrSt_Startwerte_Rohmieten_Bodenwert', fields, "FGDB_Einnahmen_Tool.gdb", where_clause, is_base_table = True)
            for row in cursor:
                params.slider2.value = row[1]
                params.slider3.value = row[2]
                params.slider4.value = row[3]
                params.slider5.value = row[4]
                params.slider6.value = row[5]
                params.slider7.value = row[6]
                params.slider8.value = 0
                params.slider9.value = 0



    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if params.name.altered and not params.name.hasBeenValidated:
            self.eingaben_auslesen(params)

        ags = ""
        fields = ['AGS']
        cursor = self.query_table('Projektrahmendaten', fields, "FGDB_Definition_Projekt.gdb")
        for row in cursor:
            ags = row[0]

        efh = 0
        fields = ["Gebaeudetyp", 'WE']
        cursor = self.query_table('Wohnen_WE_in_Gebaeudetypen', fields, "FGDB_Definition_Projekt.gdb")
        for row in cursor:
            if row[0] == "Einfamilienhaus":
                efh += row[1]

        if int(ags) <= 10999999:
            self.par.slider2.enabled  = True
            self.par.slider3.enabled  = True
            self.par.slider4.enabled  = True
            self.par.slider5.enabled  = True
            self.par.slider6.enabled  = False
            self.par.slider7.enabled  = False
        else:
            self.par.slider2.enabled  = False
            self.par.slider3.enabled  = False
            self.par.slider4.enabled  = False
            self.par.slider5.enabled  = False
            if efh > 0:
                self.par.slider6.enabled  = True
                self.par.slider7.enabled  = True
            else:
                self.par.slider6.enabled  = False
                self.par.slider7.enabled  = False



        rows = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb')
        wohnen_exists = False
        gewerbe_exists = False
        einzelhandel_exists = False
        for row in rows:
            if row[0] == Nutzungsart.WOHNEN:
                wohnen_exists = True
            if row[0] == Nutzungsart.GEWERBE:
                gewerbe_exists = True
            if row[0] == Nutzungsart.EINZELHANDEL:
                einzelhandel_exists = True

        if einzelhandel_exists or gewerbe_exists:
            self.par.slider8.enabled = True
            self.par.slider9.enabled = True
        else:
            self.par.slider8.enabled = False
            self.par.slider9.enabled = False

        if not wohnen_exists:
            self.par.slider2.enabled  = False
            self.par.slider3.enabled  = False
            self.par.slider4.enabled  = False
            self.par.slider5.enabled  = False
            self.par.slider6.enabled  = False
            self.par.slider7.enabled  = False