# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.T4_Grundsteuer import Grundsteuer


class TbxGrundsteuer(Tbx):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'4 Grundsteuer'

    @property
    def Tool(self):
        return Grundsteuer

    def _getParameterInfo(self):

        params = self.par
        # Projektname
        param_1 = params.name = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Gemeindegrössenklasse_1964
        param_2 = params.ggk_1964 = arcpy.Parameter()
        param_2.name = encode(u'Gemeindegrößenklasse_1964')
        param_2.displayName = encode(u'Gemeindegrößenklasse 1964')
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'
        param_2.filter.list = [u'unter 2000 EW',
                               u'2000 bis 5000 EW',
                               u'5000 bis 10000 EW',
                               u'10000 bis 50000 EW',
                               u'50000 bis 500000 EW',
                               encode(u'über 500000 EW')]

        # Grundsteuerhebesatz_als_vH_Satz
        param_3 = params.hebesatz = arcpy.Parameter()
        param_3.name = u'Grundsteuerhebesatz_als_vH_Satz'
        param_3.displayName = u'Grundsteuerhebesatz als vH Satz'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPDouble'

        heading = "01 Mieten"

        # Einfamilienhaus__Monatsrohmiete__in_€_m²_
        param_4 = params.efh_rohmiete = arcpy.Parameter()
        param_4.name = encode(u'Einfamilienhaus__Monatsrohmiete__in_€')
        param_4.displayName = encode(u'Einfamilienhaus: Monatsrohmiete (in €)')
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPDouble'
        param_4.category = heading

        # Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_€_m²_
        param_5 = params.zfh_rohmiete = arcpy.Parameter()
        param_5.name = encode(u'Zweifamilien-_oder_Doppelhaus__Monatsrohmiete__in_€')
        param_5.displayName = encode(u'Zweifamilien- oder Doppelhaus: Monatsrohmiete (in €)')
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPDouble'
        param_5.category = heading

        # Reihenhaus__Monatsrohmiete__in_€_m²_
        param_6 = params.rh_rohmiete = arcpy.Parameter()
        param_6.name = encode(u'Reihenhaus__Monatsrohmiete__in_€')
        param_6.displayName = encode(u'Reihenhaus: Monatsrohmiete (in €)')
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'GPDouble'
        param_6.category = heading

        # Mehrfamilienhaus__Monatsrohmiete__in_€_m²_
        param_7 = params.mfh_rohmiete = arcpy.Parameter()
        param_7.name = encode(u'Mehrfamilienhaus__Monatsrohmiete__in_€')
        param_7.displayName = encode(u'Mehrfamilienhaus: Monatsrohmiete (in €)')
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'GPDouble'
        param_7.category = heading

        heading = "02 Garagen"

        # Jahresrohmiete_Garagen___pro_Garage_
        param_8 = params.garagen_jahresrohmiete = arcpy.Parameter()
        param_8.name = u'Jahresrohmiete_Garagen___pro_Garage_'
        param_8.displayName = u'Jahresrohmiete Garagen (pro Garage)'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'GPDouble'
        param_8.category = heading

        # Jahresrohmiete_Carports___pro_Garage_
        param_9 = params.carports_jahresrohmiete = arcpy.Parameter()
        param_9.name = u'Jahresrohmiete_Carports___pro_Garage_'
        param_9.displayName = u'Jahresrohmiete Carports (pro Garage)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'GPDouble'
        param_9.category = heading

        return params
