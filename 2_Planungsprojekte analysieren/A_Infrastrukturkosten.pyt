# -*- coding: utf-8 -*-

import _rpcpath
import contextlib
import os
import sys
import arcpy
import argparse
import kosten_lib as kosten
import T5_Kostenmodell
import imp
BASE_PATH = os.path.abspath(join(os.path.dirname(__file__),
                                         '..', '..'))
LIB_PATH = join(BASE_PATH, '2_Tool', '2_Projektverwaltung')
project_lib = imp.load_source('project_lib',
                              join(LIB_PATH, 'project_lib.py'))

# Export of toolbox F:\ggr Projekte\RPC_Tools\2_Tool\A_Infrastrukturkosten\A_Infrastrukturkosten.tbx

class Toolbox(object):
    def __init__(self):
        self.label = u'11_Definition_Projekt_Tool'
        self.alias = ''
        self.tools = [Infrastrukturkostenermittlung, KostenaufteilungsregelnVerwalten]

# Tool implementation code

class Infrastrukturkostenermittlung(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\A_Infrastrukturkosten\A_Infrastrukturkosten.tbx\Infrastrukturkostenermittlung22222"""
    #Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
    #damit die vorhandenen Projekte in der DropdownListe angezeigt werden
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""

        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters

        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""

            list_projects = project_lib.get_projects()
            list_projects = sorted(list_projects)
            tablepath_costrules = join(BASE_PATH,'2_Tool','A_Infrastrukturkosten','FGDB_Kosten_Tool.gdb','T01DEF_Kostenaufteilungsregeln')

            try:
                rows_costrules = arcpy.SearchCursor(tablepath_costrules)
                message = "jep"
            except:
                rows_costrules = []
                message = "nope"

            list_costrules = []
            for row in rows_costrules:
                list_costrules.append(row.Kostenregelname)
            list_costrules = list(set(list_costrules))
            list_costrules = sorted(list_costrules)

            list_teilflaechen = []

            #set parameters
            self.params[0].filter.list = list_projects
            self.params[2].filter.list = ["Mischwassersystem","Trennwassersystem","Oberflaechenentwaesserung"]
            self.params[3].filter.list = ["Rueckhaltebecken - offen","Rueckhaltebecken - geschlossen","Rueckhaltebecken - Stauraumkanal","Rueckhaltebecken - Retentionsbodenfilter"]

            #self.params[2].category = "01 - Zusatzangaben Entwässerung"
            self.params[3].category = u"01 - Zusatzangaben Entw\xe4sserung"
            self.params[4].category = u"01 - Zusatzangaben Entw\xe4sserung"
            self.params[5].category = u"01 - Zusatzangaben Entw\xe4sserung"

            self.params[6].category = u"02 - Zus\xe4tzliche Kostenfaktoren"
            self.params[7].category = u"02 - Zus\xe4tzliche Kostenfaktoren"

            i=7
            heading = u'03 - Aufteilung der Kosten auf Kostentr\xe4ger'
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules
            i+=1; self.params[i].category = heading; self.params[i].filter.list = list_costrules


            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""

            tbx_path = __file__

            base_path = os.path.dirname(tbx_path)
            base_path = os.path.dirname(base_path)
            base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

            if self.params[0].altered and not self.params[0].hasBeenValidated:

                projektname = self.params[0].value
                projekt_fgdb = "FGDB_Definition_Projekt_"+self.params[0].value+".gdb"

                tablepath_teilflaechen = join(base_path,'3_Projekte',projektname,projekt_fgdb,"Teilflaechen_Plangebiet")

                rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)

                list_teilflaechen =[]

                for row in rows_teilflaechen:
                    list_teilflaechen.append(row.Name)
                list_teilflaechen = list(set(list_teilflaechen))
                list_teilflaechen = sorted(list_teilflaechen)

                #self.params[5].filter.list = list_teilflaechen


            #Alte Kostenaufteilung einlesen

            if self.params[0].altered and not self.params[0].hasBeenValidated:

                projectname = self.params[0].value

                tablepath_costrules_project = join(base_path,'3_Projekte',projectname,'FGDB_Kosten.gdb','Projektspez_Kostenauft')

                where_clause = """"Kostenbereich" = '01 - Planungsaufwand' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB1_KP1 = row[0]

                where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB2_KP1 = row[0]

                where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB2_KP2 = row[0]

                where_clause = """"Kostenbereich" = '02 - Gruen-, Ausgleichs- und Ersatzflaechen' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB2_KP3 = row[0]

                where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB3_KP1 = row[0]

                where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB3_KP2 = row[0]

                where_clause = """"Kostenbereich" = '03 - Innere Verkehrserschliessung' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB3_KP3 = row[0]

                where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB4_KP1 = row[0]

                where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB4_KP2 = row[0]

                where_clause = """"Kostenbereich" = '04 - Aeussere Verkehrserschliessung' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB4_KP3 = row[0]

                where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB5_KP1 = row[0]

                where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB5_KP2 = row[0]

                where_clause = """"Kostenbereich" = '05 - Wasserversorgung' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB5_KP3 = row[0]

                where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB6_KP1 = row[0]

                where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB6_KP2 = row[0]

                where_clause = """"Kostenbereich" = '06 - Abwasserentsorgung' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB6_KP3 = row[0]

                where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB7_KP1 = row[0]

                where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB7_KP2 = row[0]

                where_clause = """"Kostenbereich" = '07 - Laermschutz' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB7_KP3 = row[0]

                where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '1 - Erstmalige Herstellung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB8_KP1 = row[0]

                where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '2 - Betrieb und Unterhaltung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB8_KP2 = row[0]

                where_clause = """"Kostenbereich" = '08 - Zusatzkosten' and "Kostenphase" = '3 - Erneuerung' """
                rows = arcpy.da.SearchCursor(tablepath_costrules_project,'Kostenaufteilungsregel',where_clause)
                for row in rows:
                    KB8_KP3 = row[0]


                i = 7
                #"01 Planungskosten"
                i+=1 ; self.params[i].value = KB1_KP1

                #"02 Grün-, Ausgleichs- und Ersatzflächen"
                i+=1 ; self.params[i].value = KB2_KP1
                i+=1 ; self.params[i].value = KB2_KP2
                i+=1 ; self.params[i].value = KB2_KP3

                #"03 Innere Verkehrserschließung"
                i+=1 ; self.params[i].value = KB3_KP1
                i+=1 ; self.params[i].value = KB3_KP2
                i+=1 ; self.params[i].value = KB3_KP3

                #"04 Äußere Verkehrserschließung"
                i+=1 ; self.params[i].value = KB4_KP1
                i+=1 ; self.params[i].value = KB4_KP2
                i+=1 ; self.params[i].value = KB4_KP3

                #"05 Wasserversorgung"
                i+=1 ; self.params[i].value = KB5_KP1
                i+=1 ; self.params[i].value = KB5_KP2
                i+=1 ; self.params[i].value = KB5_KP3

                #"06 Abwasserentsorgung"
                i+=1 ; self.params[i].value = KB6_KP1
                i+=1 ; self.params[i].value = KB6_KP2
                i+=1 ; self.params[i].value = KB6_KP3

                #"07 Lärmschutz"
                i+=1 ; self.params[i].value = KB7_KP1
                i+=1 ; self.params[i].value = KB7_KP2

            return


        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return

    def __init__(self):
        self.label = u'1 Infrastrukturkosten ermitteln'
        self.canRunInBackground = False
        reload(T5_Kostenmodell)

    def getParameterInfo(self):
        # Projekt_auswählen
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt_ausw\xe4hlen'
        param_1.displayName = u'Projekt ausw\xe4hlen'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = []

        # Kostenauf-___abschlag____
        param_2 = arcpy.Parameter()
        param_2.name = u'Kostenauf-___abschlag____'
        param_2.displayName = u'Kostenauf- / abschlag (%)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'0'

        # Entwaesserungstyp
        param_3 = arcpy.Parameter()
        param_3.name = u'Entwaesserungstyp'
        param_3.displayName = u'Entwaesserungstyp'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Zeichenfolge'
        param_3.filter.list = [u'Mischwassersystem', u'Trennwassersystem', u'Oberflaechenentwaesserung']

        # Rückhaltebauwerke__Typenauswahl_
        param_4 = arcpy.Parameter()
        param_4.name = u'R\xfcckhaltebauwerke__Typenauswahl_'
        param_4.displayName = u'R\xfcckhaltebauwerke (Typenauswahl)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Zeichenfolge'
        param_4.filter.list = [u'Rueckhaltebecken - offen', u'Rueckhaltebecken - geschlossen', u'Rueckhaltebecken - Stauraumkanal', u'Rueckhaltebecken - Retentionsbodenfilter']

        # Rückhaltebauwerke__m³_Fassungsvermögen_
        param_5 = arcpy.Parameter()
        param_5.name = u'R\xfcckhaltebauwerke__m\xb3_Fassungsverm\xf6gen_'
        param_5.displayName = u'R\xfcckhaltebauwerke (m\xb3 Fassungsverm\xf6gen)'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'Zeichenfolge'

        # Zusätzliche_Kanalmeter
        param_6 = arcpy.Parameter()
        param_6.name = u'Zus\xe4tzliche_Kanalmeter'
        param_6.displayName = u'Zus\xe4tzliche Kanalmeter'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'Zeichenfolge'

        # Zusätzliche_Herstellungskosten
        param_7 = arcpy.Parameter()
        param_7.name = u'Zus\xe4tzliche_Herstellungskosten'
        param_7.displayName = u'Zus\xe4tzliche Herstellungskosten'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Zeichenfolge'

        # Zusätzliche_Betriebskosten__jährlich_
        param_8 = arcpy.Parameter()
        param_8.name = u'Zus\xe4tzliche_Betriebskosten__j\xe4hrlich_'
        param_8.displayName = u'Zus\xe4tzliche Betriebskosten (j\xe4hrlich)'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'Zeichenfolge'

        # Kostenübernahme_der_Projektplanung
        param_9 = arcpy.Parameter()
        param_9.name = u'Kosten\xfcbernahme_der_Projektplanung'
        param_9.displayName = u'Kosten\xfcbernahme der Projektplanung'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Zeichenfolge'
        param_9.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Grün-__Ausgleichs-_und_Ersatzflächen__Erstmalige_Herstellung
        param_10 = arcpy.Parameter()
        param_10.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Erstmalige_Herstellung'
        param_10.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Erstmalige Herstellung'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Zeichenfolge'
        param_10.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Grün-__Ausgleichs-_und_Ersatzflächen__Betrieb_und_Unterhaltung
        param_11 = arcpy.Parameter()
        param_11.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Betrieb_und_Unterhaltung'
        param_11.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Betrieb und Unterhaltung'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Zeichenfolge'
        param_11.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Grün-__Ausgleichs-_und_Ersatzflächen__Erneuerung
        param_12 = arcpy.Parameter()
        param_12.name = u'Gr\xfcn-__Ausgleichs-_und_Ersatzfl\xe4chen__Erneuerung'
        param_12.displayName = u'Gr\xfcn-, Ausgleichs- und Ersatzfl\xe4chen: Erneuerung'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Zeichenfolge'
        param_12.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Innere_Verkehrserschließung__Erstmalige_Herstellung
        param_13 = arcpy.Parameter()
        param_13.name = u'Innere_Verkehrserschlie\xdfung__Erstmalige_Herstellung'
        param_13.displayName = u'Innere Verkehrserschlie\xdfung: Erstmalige Herstellung'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'Zeichenfolge'
        param_13.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Innere_Verkehrserschließung__Betrieb_und_Unterhaltung
        param_14 = arcpy.Parameter()
        param_14.name = u'Innere_Verkehrserschlie\xdfung__Betrieb_und_Unterhaltung'
        param_14.displayName = u'Innere Verkehrserschlie\xdfung: Betrieb und Unterhaltung'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'Zeichenfolge'
        param_14.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Innere_Verkehrserschließung__Erneuerung
        param_15 = arcpy.Parameter()
        param_15.name = u'Innere_Verkehrserschlie\xdfung__Erneuerung'
        param_15.displayName = u'Innere Verkehrserschlie\xdfung: Erneuerung'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'Zeichenfolge'
        param_15.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Äußere_Verkehrserschließung__Erstmalige_Herstellung
        param_16 = arcpy.Parameter()
        param_16.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Erstmalige_Herstellung'
        param_16.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Erstmalige Herstellung'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'Zeichenfolge'
        param_16.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Äußere_Verkehrserschließung__Betrieb_und_Unterhaltung
        param_17 = arcpy.Parameter()
        param_17.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Betrieb_und_Unterhaltung'
        param_17.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Betrieb und Unterhaltung'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Zeichenfolge'
        param_17.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Äußere_Verkehrserschließung__Erneuerung
        param_18 = arcpy.Parameter()
        param_18.name = u'\xc4u\xdfere_Verkehrserschlie\xdfung__Erneuerung'
        param_18.displayName = u'\xc4u\xdfere Verkehrserschlie\xdfung: Erneuerung'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'Zeichenfolge'
        param_18.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Wasserversorgung__Erstmalige_Herstellung
        param_19 = arcpy.Parameter()
        param_19.name = u'Wasserversorgung__Erstmalige_Herstellung'
        param_19.displayName = u'Wasserversorgung: Erstmalige Herstellung'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'Zeichenfolge'
        param_19.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Wasserversorgung__Betrieb_und_Unterhaltung
        param_20 = arcpy.Parameter()
        param_20.name = u'Wasserversorgung__Betrieb_und_Unterhaltung'
        param_20.displayName = u'Wasserversorgung: Betrieb und Unterhaltung'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'Zeichenfolge'
        param_20.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Wasserversorgung__Erneuerung
        param_21 = arcpy.Parameter()
        param_21.name = u'Wasserversorgung__Erneuerung'
        param_21.displayName = u'Wasserversorgung: Erneuerung'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'Zeichenfolge'
        param_21.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Abwasserentsorgung__Erstmalige_Herstellung
        param_22 = arcpy.Parameter()
        param_22.name = u'Abwasserentsorgung__Erstmalige_Herstellung'
        param_22.displayName = u'Abwasserentsorgung: Erstmalige Herstellung'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'Zeichenfolge'
        param_22.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Abwasserentsorgung__Betrieb_und_Unterhaltung
        param_23 = arcpy.Parameter()
        param_23.name = u'Abwasserentsorgung__Betrieb_und_Unterhaltung'
        param_23.displayName = u'Abwasserentsorgung: Betrieb und Unterhaltung'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'Zeichenfolge'
        param_23.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Abwasserentsorgung__Erneuerung
        param_24 = arcpy.Parameter()
        param_24.name = u'Abwasserentsorgung__Erneuerung'
        param_24.displayName = u'Abwasserentsorgung: Erneuerung'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'Zeichenfolge'
        param_24.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Lärmschutz__Erstmalige_Herstellung
        param_25 = arcpy.Parameter()
        param_25.name = u'L\xe4rmschutz__Erstmalige_Herstellung'
        param_25.displayName = u'L\xe4rmschutz: Erstmalige Herstellung'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'Zeichenfolge'
        param_25.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        # Lärmschutz__Betrieb_und_Unterhaltung
        param_26 = arcpy.Parameter()
        param_26.name = u'L\xe4rmschutz__Betrieb_und_Unterhaltung'
        param_26.displayName = u'L\xe4rmschutz: Betrieb und Unterhaltung'
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'Zeichenfolge'
        param_26.filter.list = [u'Investor zahlt alles', u'Kommune zahlt alles', u'TestName', u'\xa7127 BauGB']

        parameters = [param_1, param_2, param_3, param_4, param_5, param_6,
                      param_7, param_8, param_9, param_10, param_11, param_12,
                      param_13, param_14, param_15, param_16, param_17,
                      param_18, param_19, param_20, param_21, param_22,
                      param_23, param_24, param_25, param_26]

        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()

        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateParameters()

    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateMessages()

    def execute(self, parameters, messages):
        T5_Kostenmodell.main(parameters, messages)

class KostenaufteilungsregelnVerwalten(object):
    """F:\ggr Projekte\RPC_Tools\2_Tool\A_Infrastrukturkosten\A_Infrastrukturkosten.tbx\KostenaufteilungsregelnVerwalten2"""
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""

        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters

        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""

            i = 0
            self.params[i+2].enabled = 0; self.params[i+3].enabled = 0; self.params[i+4].enabled = 0

            self.params[i+1].filter.list = []

            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""

            def sliderSummenKontrolle(listeSliderID, zielwertSlidersumme):
                istsumme = 0
                for s in listeSliderID:
                    istsumme+=self.params[s].value

                if istsumme <> zielwertSlidersumme:
                    abweichung = zielwertSlidersumme - istsumme
                    for s in reversed(listeSliderID):
                        alterWert = self.params[s].value
                        neuerWert = self.params[s].value + abweichung
                        if neuerWert < 0:
                            neuerWert = 0
                        elif neuerWert > zielwertSlidersumme:
                            neuerWert = zielwertSlidersumme
                        abweichung = abweichung + alterWert - neuerWert
                        self.params[s].value = neuerWert
                return

            tablepath_rules = join(BASE_PATH,'2_Tool','A_Infrastrukturkosten','FGDB_Kosten_Tool.gdb','T01DEF_Kostenaufteilungsregeln')

            i = 0

            rows_rules = arcpy.SearchCursor(tablepath_rules, 'Vorgabewert = 0')
            list_rules = []
            for row in rows_rules:
                list_rules.append(row.Kostenregelname)
            list_rules = sorted(set(list_rules))
            self.params[i+1].filter.list = list_rules


            if self.params[i].value == 'Kostenaufteilungsregel anlegen':
                self.params[i+1].enabled = 1
                self.params[i+1].filter.list = []
                self.params[i+2].enabled = 1
                self.params[i+2].enabled = 1; self.params[i+3].enabled = 1; self.params[i+4].enabled = 1

            elif self.params[i].value == 'Kostenaufteilungsregel bearbeiten':
                self.params[i+1].enabled = 1
                self.params[i+1].filter.list = list_rules
                self.params[i+2].enabled = 1; self.params[i+3].enabled = 1; self.params[i+4].enabled = 1

            elif self.params[i].value == 'Kostenaufteilungsregel entfernen':
                self.params[i+1].enabled = 1
                self.params[i+1].filter.list = list_rules
                self.params[i+2].enabled = 0
                self.params[i+2].enabled = 0; self.params[i+3].enabled = 0; self.params[i+4].enabled = 0

            if self.params[i+1].altered and not self.params[i+1].hasBeenValidated:
                self.params[i+1].filter.list = list_rules

                tablepath_rules = join(base_path,'2_Tool','A_Infrastrukturkosten','FGDB_Kosten_Tool.gdb','T01DEF_Kostenaufteilungsregeln')
                fields = ['Anteil']

                where_clause = '"Kostenregelname" = ' + "'" + self.params[i+1].value + "'" + ' AND Kostentraeger = 1'
                rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
                for row in rows:
                    self.params[2].value = row[0]*100

                where_clause = '"Kostenregelname" = ' + "'" + self.params[i+1].value + "'" + ' AND Kostentraeger = 2'
                rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
                for row in rows:
                    self.params[3].value = row[0]*100

                where_clause = '"Kostenregelname" = ' + "'" + self.params[i+1].value + "'" + ' AND Kostentraeger = 3'
                rows = arcpy.da.SearchCursor(tablepath_rules,fields,where_clause)
                for row in rows:
                    self.params[4].value = row[0]*100

            # Anteile verteilen
            i = 1
            listeSliderID = [i+1,i+2,i+3]
            zielwertSlidersumme = 100
            for r in listeSliderID:
                if self.params[r].altered:
                    sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            return

    def __init__(self):
        self.label = u'2 Kostenaufteilungsregeln verwalten'
        self.canRunInBackground = False
        reload(kosten)

    def getParameterInfo(self):
        # Was_wollen_Sie_tun_
        param_1 = arcpy.Parameter()
        param_1.name = u'Was_wollen_Sie_tun_'
        param_1.displayName = u'Was wollen Sie tun?'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Zeichenfolge'
        param_1.filter.list = [u'Kostenaufteilungsregel anlegen', u'Kostenaufteilungsregel bearbeiten', u'Kostenaufteilungsregel entfernen']

        # Regelnahme
        param_2 = arcpy.Parameter()
        param_2.name = u'Regelnahme'
        param_2.displayName = u'Regelnahme'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Zeichenfolge'

        # Kostenübernahme_Gemeinde_____
        param_3 = arcpy.Parameter()
        param_3.name = u'Kosten\xfcbernahme_Gemeinde_____'
        param_3.displayName = u'Kosten\xfcbernahme Gemeinde (%):'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'GPLong'
        param_3.value = u'30'
        param_3.filter.type = 'Range'
        param_3.filter.list = [0, 100]

        # Kostenübernahme_Kreis_____
        param_4 = arcpy.Parameter()
        param_4.name = u'Kosten\xfcbernahme_Kreis_____'
        param_4.displayName = u'Kosten\xfcbernahme Kreis (%):'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'GPLong'
        param_4.value = u'30'
        param_4.filter.type = 'Range'
        param_4.filter.list = [0, 100]

        # Kostenübernahme_Private_____
        param_5 = arcpy.Parameter()
        param_5.name = u'Kosten\xfcbernahme_Private_____'
        param_5.displayName = u'Kosten\xfcbernahme Private (%):'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'GPLong'
        param_5.value = u'40'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 100]

        parameters = [param_1, param_2, param_3, param_4, param_5]
        validator = getattr(self, 'ToolValidator', None)
        validator(parameters).initializeParameters()

        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateParameters()

    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateMessages()

    def execute(self, parameters, messages):
        action = parameters[0].valueAsText
        name = parameters[1].valueAsText

        gemeinden = parameters[2].value/100.
        kreis = parameters[3].value/100.
        private = parameters[4].value/100.
        if action == 'Kostenaufteilungsregel anlegen':
            kosten.kostenregel_anlegen(name,gemeinden,kreis,private)

        elif action == 'Kostenaufteilungsregel bearbeiten':
            kosten.kostenregel_bearbeiten(name,gemeinden,kreis,private)

        elif action == 'Kostenaufteilungsregel entfernen':
            kosten.kostenregel_loeschen(name)