# -*- coding: utf-8 -*-
import os
import sys
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.analyst.infrastrukturkosten.kostenmodell import Kostenmodell

class TbxInfrastrukturkostenermittlung(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 3: Infrastrukturkosten ermitteln')

    @property
    def Tool(self):
        return Kostenmodell

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

        # Kostenauf-___abschlag____
        param_2 = params.sonderkostenfaktor = arcpy.Parameter()
        param_2.name = u'Kostenauf-___abschlag____'
        param_2.displayName = u'Kostenauf- / abschlag (%)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'0'

        # Entwaesserungstyp
        types = [u'Mischwassersystem', u'Trennwassersystem', u'Oberflaechenentwaesserung']
        param_3 = params.entwaesserungssystem = arcpy.Parameter()
        param_3.name = u'Entwaesserungstyp'
        param_3.displayName = u'Entwaesserungstyp'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPString'

        param_3.filter.list = types
        param_3.value = types[0]

        heading = encode(u"01 - Zusatzangaben Entwässerung")

        # Rückhaltebauwerke__Typenauswahl_
        param_4 = params.rueckhaltebecken_typ = arcpy.Parameter()
        param_4.name = u'R\xfcckhaltebauwerke__Typenauswahl_'
        param_4.displayName = u'R\xfcckhaltebauwerke (Typenauswahl)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'GPString'

        param_4.filter.list = [u'Rueckhaltebecken - offen', u'Rueckhaltebecken - geschlossen', u'Rueckhaltebecken - Stauraumkanal', u'Rueckhaltebecken - Retentionsbodenfilter']

        # Rückhaltebauwerke__m³_Fassungsvermögen_
        param_5 = params.rueckhaltebecken_m3 = arcpy.Parameter()
        param_5.name = u'R\xfcckhaltebauwerke__m\xb3_Fassungsverm\xf6gen_'
        param_5.displayName = u'R\xfcckhaltebauwerke (m\xb3 Fassungsverm\xf6gen)'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'GPString'


        # Zusätzliche_Kanalmeter
        param_6 = params.zus_kanalmeter = arcpy.Parameter()
        param_6.name = u'Zus\xe4tzliche_Kanalmeter'
        param_6.displayName = u'Zus\xe4tzliche Kanalmeter'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'GPString'


        for p in params[3:6]:
            p.category = heading

        heading = encode(u"02 - Zusätzliche Kostenfaktoren")

        # Zusätzliche_Herstellungskosten
        param_7 = params.zus_herstellungskosten = arcpy.Parameter()
        param_7.name = u'Zus\xe4tzliche_Herstellungskosten'
        param_7.displayName = u'Zus\xe4tzliche Herstellungskosten'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'GPString'


        # Zusätzliche_Betriebskosten__jährlich_
        param_8 = params.zus_betriebskosten = arcpy.Parameter()
        param_8.name = u'Zus\xe4tzliche_Betriebskosten__j\xe4hrlich_'
        param_8.displayName = u'Zus\xe4tzliche Betriebskosten (j\xe4hrlich)'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'GPString'


        for p in params[6:8]:
            p.category = heading

        heading = encode(u'03 - Aufteilung der Kosten auf Kostenträger')

        # Kostenübernahme_der_Projektplanung
        param_9 = params.KB1_KP1 = arcpy.Parameter()
        param_9.name = u'Kosten\xfcbernahme_der_Projektplanung'
        param_9.displayName = u'Kosten\xfcbernahme der Projektplanung'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'GPString'


        # Grün-__Ausgleichs-_und_Ersatzflächen__Erstmalige_Herstellung
        param_10 = params.KB2_KP1 = arcpy.Parameter()
        param_10.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Erstmalige_Herstellung'
        param_10.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Erstmalige Herstellung'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'GPString'


        # Grün-__Ausgleichs-_und_Ersatzflächen__Betrieb_und_Unterhaltung
        param_11 = params.KB2_KP2 = arcpy.Parameter()
        param_11.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Betrieb_und_Unterhaltung'
        param_11.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Betrieb und Unterhaltung'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'GPString'


        # Grün-__Ausgleichs-_und_Ersatzflächen__Erneuerung
        param_12 = params.KB2_KP3 = arcpy.Parameter()
        param_12.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Erneuerung'
        param_12.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Erneuerung'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'GPString'


        # Innere_Verkehrserschließung__Erstmalige_Herstellung
        param_13 = params.KB3_KP1 = arcpy.Parameter()
        param_13.name = u'Innere_Verkehrserschlie\xdfung__Erstmalige_Herstellung'
        param_13.displayName = u'Innere Verkehrserschlie\xdfung: Erstmalige Herstellung'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'GPString'


        # Innere_Verkehrserschließung__Betrieb_und_Unterhaltung
        param_14 = params.KB3_KP2 = arcpy.Parameter()
        param_14.name = u'Innere_Verkehrserschlie\xdfung__Betrieb_und_Unterhaltung'
        param_14.displayName = u'Innere Verkehrserschlie\xdfung: Betrieb und Unterhaltung'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'GPString'


        # Innere_Verkehrserschließung__Erneuerung
        param_15 = params.KB3_KP3 = arcpy.Parameter()
        param_15.name = u'Innere_Verkehrserschlie\xdfung__Erneuerung'
        param_15.displayName = u'Innere Verkehrserschlie\xdfung: Erneuerung'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'GPString'


        # Äußere_Verkehrserschließung__Erstmalige_Herstellung
        param_16 = params.KB4_KP1 = arcpy.Parameter()
        param_16.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Erstmalige_Herstellung'
        param_16.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Erstmalige Herstellung'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'GPString'


        # Äußere_Verkehrserschließung__Betrieb_und_Unterhaltung
        param_17 = params.KB4_KP2 = arcpy.Parameter()
        param_17.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Betrieb_und_Unterhaltung'
        param_17.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Betrieb und Unterhaltung'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'GPString'


        # Äußere_Verkehrserschließung__Erneuerung
        param_18 = params.KB4_KP3 = arcpy.Parameter()
        param_18.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Erneuerung'
        param_18.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Erneuerung'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'GPString'


        # Wasserversorgung__Erstmalige_Herstellung
        param_19 = params.KB5_KP1 = arcpy.Parameter()
        param_19.name = u'Wasserversorgung__Erstmalige_Herstellung'
        param_19.displayName = u'Wasserversorgung: Erstmalige Herstellung'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'GPString'


        # Wasserversorgung__Betrieb_und_Unterhaltung
        param_20 = params.KB5_KP2 = arcpy.Parameter()
        param_20.name = u'Wasserversorgung__Betrieb_und_Unterhaltung'
        param_20.displayName = u'Wasserversorgung: Betrieb und Unterhaltung'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'GPString'


        # Wasserversorgung__Erneuerung
        param_21 = params.KB5_KP3 = arcpy.Parameter()
        param_21.name = u'Wasserversorgung__Erneuerung'
        param_21.displayName = u'Wasserversorgung: Erneuerung'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'GPString'


        # Abwasserentsorgung__Erstmalige_Herstellung
        param_22 = params.KB6_KP1 = arcpy.Parameter()
        param_22.name = u'Abwasserentsorgung__Erstmalige_Herstellung'
        param_22.displayName = u'Abwasserentsorgung: Erstmalige Herstellung'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'GPString'


        # Abwasserentsorgung__Betrieb_und_Unterhaltung
        param_23 = params.KB6_KP2 = arcpy.Parameter()
        param_23.name = u'Abwasserentsorgung__Betrieb_und_Unterhaltung'
        param_23.displayName = u'Abwasserentsorgung: Betrieb und Unterhaltung'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'GPString'


        # Abwasserentsorgung__Erneuerung
        param_24 = params.KB6_KP3 = arcpy.Parameter()
        param_24.name = u'Abwasserentsorgung__Erneuerung'
        param_24.displayName = u'Abwasserentsorgung: Erneuerung'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'GPString'


        # Lärmschutz__Erstmalige_Herstellung
        param_25 = params.KB7_KP1 = arcpy.Parameter()
        param_25.name = u'L\xe4rmschutz__Erstmalige_Herstellung'
        param_25.displayName = u'L\xe4rmschutz: Erstmalige Herstellung'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'GPString'


        # Lärmschutz__Betrieb_und_Unterhaltung
        param_26 = params.KB7_KP2 = arcpy.Parameter()
        param_26.name = u'L\xe4rmschutz__Betrieb_und_Unterhaltung'
        param_26.displayName = u'L\xe4rmschutz: Betrieb und Unterhaltung'
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'GPString'


        for p in params[8:]:
            p.category = heading

        return params

    def _updateParameters(self, params):

        # Alte Kostenaufteilung einlesen

        if self.par.projectname and not self.par.projectname.hasBeenValidated:
            tablepath_costrules = self.folders.get_base_table(
                'FGDB_Kosten_Tool.gdb', 'T01DEF_Kostenaufteilungsregeln')

            default_costrules = [u'Investor zahlt alles', u'Kommune zahlt alles',
                                 u'TestName', encode(u'§127 BauGB')]

            rows_costrules = arcpy.SearchCursor(tablepath_costrules)
            list_costrules = sorted([row.Kostenregelname for row in rows_costrules])
            list_costrules = default_costrules

            for p in self.par[8:]:
                p.filter.list = list_costrules

            projectname = self.par.projectname.value

            tablepath_costrules_project = self.folders.get_table(
                'Projektspez_Kostenauft',
                workspace='FGDB_Kosten.gdb')

            #params = self.par

            where_clause = """"Kostenbereich" = '01 - Planungsaufwand' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB1_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB2_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB2_KP2.value = row[0]

            where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '3 - Erneuerung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB2_KP3.value = row[0]

            where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB3_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB3_KP2.value = row[0]

            where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '3 - Erneuerung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB3_KP3.value = row[0]

            where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB4_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB4_KP2.value = row[0]

            where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '3 - Erneuerung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB4_KP3.value = row[0]

            where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB5_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB5_KP2.value = row[0]

            where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '3 - Erneuerung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB5_KP3.value = row[0]

            where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB6_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB6_KP2.value = row[0]

            where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '3 - Erneuerung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB6_KP3.value = row[0]

            where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB7_KP1.value = row[0]

            where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            for row in rows:
                params.KB7_KP2.value = row[0]

            #where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '3 - Erneuerung' """
            #rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            #for row in rows:
                #params.KB7_KP3.value = row[0]

            #where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '1 - Erstmalige Herstellung' """
            #rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            #for row in rows:
                #params.KB8_KP1.value = row[0]

            #where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
            #rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            #for row in rows:
                #params.KB8_KP2.value = row[0]

            #where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '3 - Erneuerung' """
            #rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
            #for row in rows:
                #params.KB8_KP3.value = row[0]






