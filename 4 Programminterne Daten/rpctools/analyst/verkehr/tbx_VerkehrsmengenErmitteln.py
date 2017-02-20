# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.verkehr.T3_Verkehrsmengen_ermitteln import VerkehrsmengenErmitteln

class TbxVerkehrsmengenErmitteln(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 3: Verkehrsmengen ermitteln')

    @property
    def Tool(self):
        return VerkehrsmengenErmitteln

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

        heading = encode(u"01 - Parameter für Wohnnutzungen")

        # Wohnen_Wege_EW
        param_2 = params.wohnen_wege_ev = arcpy.Parameter()
        param_2.name = u'Wohnen_Wege_EW'
        param_2.displayName = u'Wege je Einwohner und Werktag'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPDouble'
        param_2.value = 3.3

        # Wohnen_MIV_Anteil
        param_3 = params.wohnen_MIV = arcpy.Parameter()
        param_3.name = u'Wohnen_MIV_Anteil'
        param_3.displayName = u'MIV-Anteil'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = 65
        param_3.filter.type = 'Range'
        param_3.filter.list = [0, 100]

        # Wohnen_Pers_KFZ
        param_4 = params.wohnen_pers_kfz = arcpy.Parameter()
        param_4.name = u'Wohnen_Pers_KFZ'
        param_4.displayName = u'Personen je KFZ'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPDouble'
        param_4.value = 1.1

        # Wohnen_Anteil_Besucherfahrten
        param_5 = params.wohnen_besucherfahrten = arcpy.Parameter()
        param_5.name = u'Wohnen_Anteil_Besucherfahrten'
        param_5.displayName = u'Anteil der Besucherfahrten am Verkehrsaufkommen'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = 15
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 100]

        # Wohnen_WF_Fahrten_je_EW
        param_6 = params.wohnen_fahrten_je_EW = arcpy.Parameter()
        param_6.name = u'Wohnen_WF_Fahrten_je_EW'
        param_6.displayName = u'Wirtschaftsverkehrsfahrten je Einwohner und Werktag'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPDouble'
        param_6.value = 0.05

        heading = encode(u"02 - Parameter für Einzelhandel")

        # Versorgung_BGF_Beschaeftigter
        param_7 = params.Versorgung_BGF_Beschaeftigter = arcpy.Parameter()
        param_7.name = u'Versorgung_BGF_Beschaeftigter'
        param_7.displayName = u'Bruttogeschossfläche je beschäftigter Person (m²)'.encode('CP1252')
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'GPDouble'
        param_7.value = 55

        # Versorgung_Anwesenheit
        param_8 = params.Versorgung_Anwesenheit = arcpy.Parameter()
        param_8.name = u'Versorgung_Anwesenheit'
        param_8.displayName = u'Anwesenheit beschäftigter Personen'.encode('CP1252')
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'GPDouble'
        param_8.value = 90
        param_8.filter.type = 'Range'
        param_8.filter.list = [0, 100]

        # Versorgung_Wege_Beschaeftigter
        param_9 = params.Versorgung_Wege_Beschaeftigter = arcpy.Parameter()
        param_9.name = u'Versorgung_Wege_Beschaeftigter'
        param_9.displayName = u'Wege je beschäftigter Person und Werktag'.encode('CP1252')
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'GPDouble'
        param_9.value = 2.5

        # Versorgung_MIV_Anteil
        param_10 = params.Versorgung_MIV = arcpy.Parameter()
        param_10.name = u'Versorgung_MIV_Anteil'
        param_10.displayName = u'MIV-Anteil'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = 65
        param_10.filter.type = 'Range'
        param_10.filter.list = [0, 100]

        # Versorgung_Pers_KFZ
        param_11 = params.Versorgung_Pers_KFZ = arcpy.Parameter()
        param_11.name = u'Versorgung_Pers_KFZ'
        param_11.displayName = u'Personen je KFZ'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'GPDouble'
        param_11.value = 1.1

        # Versorgung_Besucher_Tag
        param_12 = params.Versorgung_Besucher_Tag = arcpy.Parameter()
        param_12.name = u'Versorgung_Besucher_Tag'
        param_12.displayName = u'Kunden je Bruttogeschossfläche und Werktag'.encode('CP1252')
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'GPDouble'
        param_12.value = 2.25

        # Versorgung_Lieferwege_100m2
        param_13 = params.Versorgung_Lieferwege_100m2 = arcpy.Parameter()
        param_13.name = u'Versorgung_Lieferwege_100m2'
        param_13.displayName = u'Lieferwege je 100m² Bruttogeschossfläche'.encode('CP1252')
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'GPDouble'
        param_13.value = 0.3

        heading = encode(u"03 - Parameter für Gewerbebetriebe")

        # Gewerbe_Anwesenheit
        param_14 = params.Gewerbe_Anwesenheit = arcpy.Parameter()
        param_14.name = u'Gewerbe_Anwesenheit'
        param_14.displayName = u'Anwesenheit beschäftigter Personen'.encode('CP1252')
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'GPDouble'
        param_14.value = 90
        param_14.filter.type = 'Range'
        param_14.filter.list = [0, 100]


        # Gewerbe_Wege_Beschaeftigter
        param_15 = params.Gewerbe_Wege_Beschaeftigter = arcpy.Parameter()
        param_15.name = u'Gewerbe_Wege_Beschaeftigter'
        param_15.displayName = u'Wege je beschäftigter Person und Werkag'.encode('CP1252')
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'GPDouble'
        param_15.value = 2.0

        # Gewerbe_MIV_Anteil
        param_16 = params.Gewerbe_MIV_Anteil = arcpy.Parameter()
        param_16.name = u'Gewerbe_MIV_Anteil'
        param_16.displayName = u'MIV-Anteil'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'Long'
        param_16.value = 65
        param_16.filter.type = 'Range'
        param_16.filter.list = [0, 100]

        # Gewerbe_Pers_KFZ
        param_17 = params.Gewerbe_Pers_KFZ = arcpy.Parameter()
        param_17.name = u'Gewerbe_Pers_KFZ'
        param_17.displayName = u'Personen je KFZ '
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'GPDouble'
        param_17.value = 1.1

        # Gewerbe_Anteil_Besucherfahrten
        param_18 = params.Gewerbe_Besucherfahrten = arcpy.Parameter()
        param_18.name = u'Gewerbe_Kundenwege_Beschaeftigte'
        param_18.displayName = u'Wege der Kunden je Beschäftigtem'.encode('CP1252')
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'GPDouble'
        param_18.value = 1

        # Gewerbe_Lieferwege_Beschaeftigte
        param_19 = params.Gewerbe_Lieferwege_Beschaeftigte = arcpy.Parameter()
        param_19.name = u'Gewerbe_Lieferwege_Beschaeftigte'
        param_19.displayName = u'Lieferwege je Beschäftigtem'.encode('CP1252')
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'GPDouble'
        param_19.value = 0.05

        heading = encode(u"04 - Parameter für Schulen")

        # Schulen_Wege_Schueler
        param_20 = params.Schulen_Wege_Schueler = arcpy.Parameter()
        param_20.name = u'Schulen_Wege_Schueler'
        param_20.displayName = u'Wege je Schüler'.encode('CP1252')
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'GPDouble'
        param_20.value = 2

        # Schulen_MIV_Anteil
        param_21 = params.Schulen_MIV = arcpy.Parameter()
        param_21.name = u'Schulen_MIV_Anteil'
        param_21.displayName = u'MIV-Anteil'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'Long'
        param_21.value = 65
        param_21.filter.type = 'Range'
        param_21.filter.list = [0, 100]

        # Schulen_Schueler_KFZ
        param_22 = params.Schulen_Schueler_KFZ = arcpy.Parameter()
        param_22.name = u'Schulen_Schueler_KFZ'
        param_22.displayName = u'Schüler je KFZ'.encode('CP1252')
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'GPDouble'
        param_22.value = 1.5

        # Schulen_Schueler_je_Lehrer
        param_23 = Schulen_Schueler_je_Lehrer = arcpy.Parameter()
        param_23.name = u'Schulen_Schueler_je_Lehrer'
        param_23.displayName = u'Schüler je Lehrkraft'.encode('CP1252')
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'GPDouble'
        param_23.value = 10

        # Schulen_Wege_Lehrer
        param_24 = params.Schulen_Wege_Lehrer = arcpy.Parameter()
        param_24.name = u'Schulen_Wege_Lehrer'
        param_24.displayName = u'Wege je Lehrkraft'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'GPDouble'
        param_24.value = 2

        # Schulen_Pers_KFZ
        param_25 = paramsSchulen_Pers_KFZ = arcpy.Parameter()
        param_25.name = u'Schulen_Pers_KFZ'
        param_25.displayName = u'Lehrkraft je KFZ'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'GPDouble'
        param_25.value = 1.1

        # Schulen_Lieferwege_Schueler
        param_26 = params.Schulen_Lieferwege_Schueler = arcpy.Parameter()
        param_26.name = u'Schulen_Lieferwege_Schueler'
        param_26.displayName = u'Lieferwege je Schüler'.encode('CP1252')
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'GPDouble'
        param_26.value = 0.01

        return params

    def _updateParameters(self, params):
		return

