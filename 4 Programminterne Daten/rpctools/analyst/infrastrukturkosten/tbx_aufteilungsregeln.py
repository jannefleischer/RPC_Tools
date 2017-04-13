# -*- coding: utf-8 -*-
import arcpy
from rpctools.utils.params import Tbx
from rpctools.utils.params import Tool
from rpctools.utils.encoding import encode


from rpctools.utils import kosten_lib as kosten
reload(kosten)

ACTIONS = [u'Kostenaufteilungsregel anlegen',
           u'Kostenaufteilungsregel bearbeiten',
           u'Kostenaufteilungsregel entfernen']

class Kostenregeln(Tool):

    def run(self):

        kostenaufteilungsregel_tabelle = self.folders.get_base_table(
            'FGDB_Kosten_Tool.gdb', 'T01DEF_Kostenaufteilungsregeln')
        parameters = self.par
        action = parameters.action.value
        name = parameters.name.value
        gemeinden = parameters.gemeinden.value / 100.
        kreis = parameters.kreis.value / 100.
        private = parameters.private.value / 100.

        if action == ACTIONS[0]:
            kosten.kostenregel_anlegen(name, gemeinden, kreis, private,
                                       kostenaufteilungsregel_tabelle)

        elif action == ACTIONS[1]:
            kosten.kostenregel_bearbeiten(name, gemeinden, kreis, private,
                                          kostenaufteilungsregel_tabelle)

        elif action == ACTIONS[2]:
            kosten.kostenregel_loeschen(name, kostenaufteilungsregel_tabelle)

class TbxKostenaufteilungsregeln(Tbx):
    @property
    def label(self):
        return encode(u'Schritt 2: Kostenaufteilungsregeln verwalten')

    @property
    def Tool(self):
        return Kostenregeln

    def _getParameterInfo(self):

        params = self.par

        # Was_wollen_Sie_tun_
        param_1 = params.action = arcpy.Parameter()
        param_1.name = u'Was_wollen_Sie_tun_'
        param_1.displayName = u'Was wollen Sie tun?'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'GPString'

        param_1.filter.list = ACTIONS
        param_1.value = ACTIONS[0]

        # Regelnahme
        param_2 = params.name = arcpy.Parameter()
        param_2.name = u'Regelnahme'
        param_2.displayName = u'Regelnahme'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'GPString'


        # Kostenübernahme_Gemeinde_____
        param_3 = params.gemeinden = arcpy.Parameter()
        param_3.name = u'Kosten\xfcbernahme_Gemeinde_____'
        param_3.displayName = u'Kosten\xfcbernahme Gemeinde (%):'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPLong'
        param_3.value = u'30'
        param_3.filter.type = 'Range'
        param_3.filter.list = [0, 100]
        param_3.enabled = 0

        # Kostenübernahme_Kreis_____
        param_4 = params.kreis = arcpy.Parameter()
        param_4.name = u'Kosten\xfcbernahme_Kreis_____'
        param_4.displayName = u'Kosten\xfcbernahme Kreis (%):'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPLong'
        param_4.value = u'30'
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]
        param_4.enabled = 0

        # Kostenübernahme_Private_____
        param_5 = params.private = arcpy.Parameter()
        param_5.name = u'Kosten\xfcbernahme_Private_____'
        param_5.displayName = u'Kosten\xfcbernahme Private (%):'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPLong'
        param_5.value = u'40'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 100]
        param_5.enabled = 0

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def sliderSummenKontrolle(listeSliderID, zielwertSlidersumme):
            istsumme = 0
            for s in listeSliderID:
                istsumme+=params[s].value

            if istsumme <> zielwertSlidersumme:
                abweichung = zielwertSlidersumme - istsumme
                for s in reversed(listeSliderID):
                    alterWert = params[s].value
                    neuerWert = params[s].value + abweichung
                    if neuerWert < 0:
                        neuerWert = 0
                    elif neuerWert > zielwertSlidersumme:
                        neuerWert = zielwertSlidersumme
                    abweichung = abweichung + alterWert - neuerWert
                    params[s].value = neuerWert
            return

        tablepath_rules = self.folders.get_base_table(
            'FGDB_Kosten_Tool.gdb', 'T01DEF_Kostenaufteilungsregeln')

        i = 0

        rows_rules = arcpy.SearchCursor(tablepath_rules, 'Vorgabewert = 0')
        list_rules = []
        for row in rows_rules:
            list_rules.append(row.Kostenregelname)
        list_rules = sorted(set(list_rules))
        params.name.filter.list = list_rules

        if params.action.value == ACTIONS[0]:
            params.name.enabled = 1
            params.name.filter.list = []
            for p in params[2:]:
                p.enabled = 1

        elif params.action.value == ACTIONS[1]:
            params.name.enabled = 1
            params.name.filter.list = list_rules
            for p in params[2:]:
                p.enabled = 1

        elif params.action.value == ACTIONS[2]:
            params.name.enabled = 1
            params.name.filter.list = list_rules
            for p in params[2:]:
                p.enabled = 0

        if params.name.altered and not params.name.hasBeenValidated:
            params.name.filter.list = list_rules

            fields = ['Anteil']

            where_clause = '"Kostenregelname" = ' + "'" + params.name.value + "'" + ' AND Kostentraeger = 1'
            rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
            for row in rows:
                params.gemeinden.value = row[0]*100

            where_clause = '"Kostenregelname" = ' + "'" + params.name.value + "'" + ' AND Kostentraeger = 2'
            rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
            for row in rows:
                params.kreis.value = row[0]*100

            where_clause = '"Kostenregelname" = ' + "'" + params.name.value + "'" + ' AND Kostentraeger = 3'
            rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
            for row in rows:
                params.private.value = row[0]*100

        # Anteile verteilen
        i = 1
        listeSliderID = [i+1,i+2,i+3]
        zielwertSlidersumme = 100
        for r in listeSliderID:
            if params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        return

