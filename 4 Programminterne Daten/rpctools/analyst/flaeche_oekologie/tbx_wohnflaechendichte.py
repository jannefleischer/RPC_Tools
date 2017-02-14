# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.encoding import language
from rpctools.analyst.flaeche_oekologie.bewertung_wohnflaechendichte import BewertungWohnflaechendichte

class Tbxwohnflaechendichte(Tbx):

    @property
    def label(self):
        return encode(u'Wohnflächendichte ermitteln')

    @property
    def Tool(self):
        return BewertungWohnflaechendichte

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        i=0

        heading = u"Durchschnittliche �berbaute Fl�che nach Geb�udetyp".encode('CP1252')
        self.params[1].category = heading
        self.params[2].category = heading
        self.params[3].category = heading
        self.params[4].category = heading

        # Projekt_auswählen
        param_1 = params.projectname = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = language('string')
        param_1.filter.list = projekte
        if projekte:
            param_1.value = projekte[0]

        # Durchschnittliche_�berbaute_Fl�che_je_Wohneinheit_in_Ein-_und_Zweifamilienh�usern__qm_
        param_2 = arcpy.Parameter()
        param_2.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Ein-_und_Zweifamilienh\xe4usern__qm_'
        param_2.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Ein- und Zweifamilienh\xe4usern (qm)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'100'
        param_2.filter.type = 'Range'
        param_2.filter.list = [0, 100]

        # Durchschnittliche_�berbaute_Fl�che_je_Wohneinheit_in_Doppelh�usern__qm_
        param_3 = arcpy.Parameter()
        param_3.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Doppelh\xe4usern__qm_'
        param_3.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Doppelh\xe4usern (qm)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'100'
        param_3.filter.type = 'Range'
        param_3.filter.list = [0, 100]

        # Durchschnittliche_�berbaute_Fl�che_je_Wohneinheit_in_Reihenh�usern__qm_
        param_4 = arcpy.Parameter()
        param_4.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Reihenh\xe4usern__qm_'
        param_4.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Reihenh\xe4usern (qm)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'100'
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        # Durchschnittliche_�berbaute_Fl�che_je_Wohneinheit_in_Mehrfamilienh�usern__qm_
        param_5 = arcpy.Parameter()
        param_5.name = u'Durchschnittliche_\xfcberbaute_Fl\xe4che_je_Wohneinheit_in_Mehrfamilienh\xe4usern__qm_'
        param_5.displayName = u'Durchschnittliche \xfcberbaute Fl\xe4che je Wohneinheit in Mehrfamilienh\xe4usern (qm)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'100'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 100]

        return params

    def _updateParameters(self, params):
		return



