# -*- coding: utf-8 -*-

import contextlib
import os
import sys

import arcpy

# You can ignore/delete this code; these are basic utility functions to
# streamline porting

@contextlib.contextmanager
def script_run_as(filename, args=None):
    oldpath = sys.path[:]
    oldargv = sys.argv[:]
    newdir = os.path.dirname(filename)
    sys.path = oldpath + [newdir]
    sys.argv = [filename] + [arg.valueAsText for arg in (args or [])]
    oldcwd = os.getcwdu()
    os.chdir(newdir)

    try:
        # Actually run
        yield filename
    finally:
        # Restore old settings
        sys.path = oldpath
        sys.argv = oldargv
        os.chdir(oldcwd)

def set_parameter_as_text(params, index, val):
    if (hasattr(params[index].value, 'value')):
        params[index].value.value = val
    else:
        params[index].value = val

# Export of toolbox C:\Users\handke\Dropbox\Regioprojectcheck\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung.tbx

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = u'3_Art und Mass der Nutzung'
        self.alias = ''
        self.tools = [Flaechenbilanz, Nutzungen]

# Tool implementation code

class Flaechenbilanz(object):
    """C:\Users\handke\Dropbox\Regioprojectcheck\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung.tbx\Flaechenbilanz"""
    # -*- coding: utf-8 -*-

    import arcpy, os
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
        import datetime

        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]

        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')

        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []

        list_projects =[]

        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)

        list_teilflaechen = []

        i=-1

        #set project
        i+=1 ; self.params[i].filter.list = list_projects

        #set point
        i+=1 ; self.params[i].filter.list = list_teilflaechen

        #Startjahr auf aktuelles Jahr setzen
        i+=1 ; self.params[i].value = datetime.datetime.now().year

        i = 2
        heading = "01_Generelle Flächenaufteilung"
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading

        heading = "02_Aufteilung Nettobauland"
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading

        heading = "03_Aufteilung Verkehrsfläche"
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading

        heading = "04_Aufteilung Grünfläche"
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading
        i+=1 ; self.params[i].category = heading

        return

      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def eingaben_auslesen():
            projectname = self.params[0].value
            teilflaeche = self.params[1].value
            tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
            tablepath_flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Flaechenbilanz')

            # Oberkategorien
            queries_S1 = ((1,'Erschliessungsflaeche'),(2,'Gruenflaeche'),(3,'Sonstige Flaechen'),(4,'Nettobauland'))
            fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S1','Anteil_S1']

            for query in queries_S1:
                where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S1" = ' + "'" + query[1] + "'"
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                value = 0
                for row in rows:
                    value = row[2]
                self.params[query[0]+2].value = value


            # Nettobauland
            queries_S2 = ((1,'Gewerbeflaeche'),(2,'Nettowohnbauland'))
            fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

            for query in queries_S2:
                where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                value = 0
                for row in rows:
                    value = row[2]
                self.params[query[0]+6].value = value


            # Verkehr
            queries_S2 = ((1,'Laermschutzanlagen'),(2,'Privat - Innere Erschliessung'),(3,'Oeffentlich - Aeussere Erschliessung'),(4,'Oeffentlich - Innere Erschliessung'))
            fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

            for query in queries_S2:
                where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                value = 0
                for row in rows:
                    value = row[2]
                self.params[query[0]+8].value = value

            # Gruenflaechen
            queries_S2 = ((1,'Spielplaetze'),(2,'Strassenbegleitgruen'),(3,'Ausgleichs- und Ersatzflaechen'),(4,'Allgemeine Gruenflaechen'))
            fields = ['Teilflaeche_Plangebiet','Flaechennutzung_S2','Anteil_S2']

            for query in queries_S2:
                where_clause = """"Teilflaeche_Plangebiet" ='"""+teilflaeche+"'" + ' AND "Flaechennutzung_S2" = ' + "'" + query[1] + "'"
                rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields,where_clause)
                value = 0
                for row in rows:
                    value = row[2]
                self.params[query[0]+10].value = value

            return

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

        # Pfad zum Ordner, in dem Script liegt, erzeugen
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path)

        # Auswahl Teilfläche
        i = 0
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            projectname = self.params[i].value

            tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append(row.Name)
            list_teilflaechen = sorted(set(list_teilflaechen))
            i+=1 ; self.params[i].filter.list = list_teilflaechen

            if len(list_teilflaechen) == 1:
                self.params[i].value = list_teilflaechen[0]
                eingaben_auslesen()

        # bestehende Eingaben (falls vorhanden) übernehmen
        i = 1
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            eingaben_auslesen()

        # Slider generieren
        i = 2
        # Oberkategorien
        listeSliderID = [i+1,i+2,i+3,i+4]
        zielwertSlidersumme = 100

        for r in listeSliderID:
            if self.params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        # Nettobauland
        listeSliderID = [i+5,i+6]

        for r in listeSliderID:
            if self.params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)


        # Verkehr
        listeSliderID = [i+7,i+8,i+9,i+10]

        for r in listeSliderID:
            if self.params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        # Grünfläche
        listeSliderID = [i+11,i+12,i+13,i+14]

        for r in listeSliderID:
            if self.params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)


        return

      def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def __init__(self):
        self.label = u'1 Fl\xe4chenbilanz eingeben'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projektname
        param_1 = arcpy.Parameter()
        param_1.name = u'Projektname'
        param_1.displayName = u'Projektname'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'String'
        param_1.filter.list = [u'Test_Achim_2', u'thomas_test_neu']

        # Teilfläche
        param_2 = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'

        # Startjahr
        param_3 = arcpy.Parameter()
        param_3.name = u'Startjahr'
        param_3.displayName = u'Startjahr'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'2016'

        # Verkehrsfläche____
        param_4 = arcpy.Parameter()
        param_4.name = u'Verkehrsfl\xe4che____'
        param_4.displayName = u'Verkehrsfl\xe4che (%)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'0'

        # Grünfläche____
        param_5 = arcpy.Parameter()
        param_5.name = u'Gr\xfcnfl\xe4che____'
        param_5.displayName = u'Gr\xfcnfl\xe4che (%)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'0'

        # Sonstige_Flächen____
        param_6 = arcpy.Parameter()
        param_6.name = u'Sonstige_Fl\xe4chen____'
        param_6.displayName = u'Sonstige Fl\xe4chen (%)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'0'

        # Nettobauland____
        param_7 = arcpy.Parameter()
        param_7.name = u'Nettobauland____'
        param_7.displayName = u'Nettobauland (%)'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Long'
        param_7.value = u'100'

        # Gewerbeflaeche____
        param_8 = arcpy.Parameter()
        param_8.name = u'Gewerbeflaeche____'
        param_8.displayName = u'Gewerbeflaeche (%)'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Long'
        param_8.value = u'0'

        # Nettowohnbauland____
        param_9 = arcpy.Parameter()
        param_9.name = u'Nettowohnbauland____'
        param_9.displayName = u'Nettowohnbauland (%)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Long'
        param_9.value = u'100'

        # Flächen_für_Lärmschutz____
        param_10 = arcpy.Parameter()
        param_10.name = u'Fl\xe4chen_f\xfcr_L\xe4rmschutz____'
        param_10.displayName = u'Fl\xe4chen f\xfcr L\xe4rmschutz (%)'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = u'0'

        # Privatwege____
        param_11 = arcpy.Parameter()
        param_11.name = u'Privatwege____'
        param_11.displayName = u'Privatwege (%)'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Long'
        param_11.value = u'0'

        # Äußere_Erschließung____
        param_12 = arcpy.Parameter()
        param_12.name = u'\xc4u\xdfere_Erschlie\xdfung____'
        param_12.displayName = u'\xc4u\xdfere Erschlie\xdfung (%)'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Long'
        param_12.value = u'0'

        # Innere_Erschließung____
        param_13 = arcpy.Parameter()
        param_13.name = u'Innere_Erschlie\xdfung____'
        param_13.displayName = u'Innere Erschlie\xdfung (%)'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'Long'
        param_13.value = u'100'

        # Spielplatzfläche____
        param_14 = arcpy.Parameter()
        param_14.name = u'Spielplatzfl\xe4che____'
        param_14.displayName = u'Spielplatzfl\xe4che (%)'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'Long'
        param_14.value = u'0'

        # Straßenbegleitgrün____
        param_15 = arcpy.Parameter()
        param_15.name = u'Stra\xdfenbegleitgr\xfcn____'
        param_15.displayName = u'Stra\xdfenbegleitgr\xfcn (%)'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'Long'
        param_15.value = u'0'

        # Ausgleichs-_und_Ersatzflächen
        param_16 = arcpy.Parameter()
        param_16.name = u'Ausgleichs-_und_Ersatzfl\xe4chen'
        param_16.displayName = u'Ausgleichs- und Ersatzfl\xe4chen'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'Long'
        param_16.value = u'0'

        # Allgemeine_Grünflächen
        param_17 = arcpy.Parameter()
        param_17.name = u'Allgemeine_Gr\xfcnfl\xe4chen'
        param_17.displayName = u'Allgemeine Gr\xfcnfl\xe4chen'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Long'
        param_17.value = u'100'

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11, param_12, param_13, param_14, param_15, param_16, param_17]
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
        with script_run_as(u'C:\\Users\\handke\\Dropbox\\Regioprojectcheck\\2_Tool\\3_Art und Mass der Nutzung\\flaechenbilanz.py'):
            # ---------------------------------------------------------------------------
            # REGIOPROJEKTCHECK
            # 10_Kostenmodell.py
            #
            # Description:
            # PROJECT URL: http://www.regioprojektcheck.de
            #
            # Author:
            # GGR Planung
            #
            # LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
            # ---------------------------------------------------------------------------


            # Import arcpy modules
            import arcpy, os
            arcpy.env.overwriteOutput = True


            # Variablen definieren
            i=-1
            i+=1;projektname = parameters[i].valueAsText
            i+=1;teilflaeche = parameters[i].valueAsText
            i+=1;startjahr = parameters[i].valueAsText

            i+=1;verkehrsflaeche = int(parameters[i].valueAsText)
            i+=1;gruenflaeche = int(parameters[i].valueAsText)
            i+=1;sonst_flaechen = int(parameters[i].valueAsText)
            i+=1;nettobauland = int(parameters[i].valueAsText)

            i+=1;gewerbeflaeche = int(parameters[i].valueAsText)
            i+=1;nettowohnbauland = int(parameters[i].valueAsText)

            i+=1;laermschutz = int(parameters[i].valueAsText)
            i+=1;privatwege = int(parameters[i].valueAsText)
            i+=1;aeussere_erschliessung = int(parameters[i].valueAsText)
            i+=1;innere_erschliessung = int(parameters[i].valueAsText)

            i+=1;spielplatz = int(parameters[i].valueAsText)
            i+=1;strassenbegleitgruen = int(parameters[i].valueAsText)
            i+=1;ausgleich = int(parameters[i].valueAsText)
            i+=1;allg_gruenflaeche = int(parameters[i].valueAsText)

            #Pfade einrichten
            base_path = str(sys.path[0]).split("2_Tool")[0]
            workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
            teilflaechen = os.path.join(workspace_projekt_definition,'Teilflaechen_Plangebiet')
            flaechenbilanz = os.path.join(workspace_projekt_definition,'Flaechenbilanz')

            # Suche Größe der aktuellen Teilfläche heraus
            with arcpy.da.SearchCursor(teilflaechen, ['Name', 'Flaeche_ha']) as cursor:
                for row in cursor:
                    if row[0] == teilflaeche:
                        flaeche = float(row[1])

            # Lösche bisherige Eingaben für gewählte Teilfläche
            with arcpy.da.UpdateCursor(flaechenbilanz, "Teilflaeche_Plangebiet") as cursor:
                for row in cursor:
                    if row[0] == teilflaeche:
                        cursor.deleteRow()

            # Füge neue Eingaben für gewählte Teilfläche ein
            fields = ['Teilflaeche_Plangebiet', 'Startjahr', 'Flaechennutzung_S1', 'Flaechennutzung_S2', 'Anteil_S1', 'Anteil_S2', 'Flaeche_ha']
            cursor = arcpy.da.InsertCursor(flaechenbilanz, fields)

            cursor.insertRow((teilflaeche,startjahr,'Nettobauland','Nettowohnbauland',nettobauland,nettowohnbauland, flaeche * nettobauland / 100 * nettowohnbauland / 100))
            cursor.insertRow((teilflaeche,startjahr,'Nettobauland','Gewerbeflaeche',nettobauland,gewerbeflaeche, flaeche * nettobauland / 100 * gewerbeflaeche / 100))

            cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Laermschutzanlagen',verkehrsflaeche,laermschutz,flaeche * verkehrsflaeche / 100 * laermschutz / 100))
            cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Privat - Innere Erschliessung',verkehrsflaeche,privatwege,flaeche * verkehrsflaeche / 100 * privatwege / 100))
            cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Oeffentlich - Aeussere Erschliessung',verkehrsflaeche,aeussere_erschliessung,flaeche * verkehrsflaeche / 100 * aeussere_erschliessung / 100))
            cursor.insertRow((teilflaeche,startjahr,'Erschliessungsflaeche','Oeffentlich - Innere Erschliessung',verkehrsflaeche,innere_erschliessung,flaeche * verkehrsflaeche / 100 * innere_erschliessung / 100))

            cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Spielplaetze',gruenflaeche,spielplatz,flaeche * gruenflaeche / 100 * spielplatz / 100))
            cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Strassenbegleitgruen',gruenflaeche,strassenbegleitgruen,flaeche * gruenflaeche / 100 * strassenbegleitgruen / 100))
            cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Ausgleichs- und Ersatzflaechen',gruenflaeche,ausgleich,flaeche * gruenflaeche / 100 * ausgleich / 100))
            cursor.insertRow((teilflaeche,startjahr,'Gruenflaeche','Allgemeine Gruenflaechen',gruenflaeche,allg_gruenflaeche,flaeche * gruenflaeche / 100 * allg_gruenflaeche / 100))

            cursor.insertRow((teilflaeche,startjahr,'Sonstige Flaechen','Sonstige Flaechen',sonst_flaechen,sonst_flaechen,flaeche* sonst_flaechen / 100))

class Nutzungen(object):
    """C:\Users\handke\Dropbox\Regioprojectcheck\2_Tool\3_Art und Mass der Nutzung\3_Art und Mass der Nutzung.tbx\Nutzungen"""
    # -*- coding: utf-8 -*-
    import arcpy
    import os
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
        import os, arcpy, datetime

        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]

        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

        tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')

        try:
            rows_projects = arcpy.SearchCursor(tablepath_projects)
        except:
            rows_projects  = []

        list_projects =[]

        for row in rows_projects:
            list_projects.append(row.Name)
        list_projects = list(set(list_projects))
        list_projects = sorted(list_projects)


        list_teilflaechen = []

        list_EwProWE = []
        for i in range(1,5):
            for j in range(0,10):
                list_EwProWE.append(str(i)+","+str(j)+" Bewohner pro Wohneinheit")

        i=-1

        #set project
        i+=1 ; self.params[i].filter.list = list_projects

        #set point
        i+=1 ; self.params[i].filter.list = list_teilflaechen

        heading = "1) Aufsiedlungszeitraum"
        i+=1 ; self.params[i].category = heading # Startjahr
        i+=1 ; self.params[i].category = heading # Aufsiedlungsdauer

        heading = "2) Wohnen - Anzahl Wohneinheiten nach Gebäudetypen"
        i+=1 ; self.params[i].category = heading # Anzahl WE in Einfamilienhäusern
        i+=1 ; self.params[i].category = heading # Anzahl WE in Doppelhäusern
        i+=1 ; self.params[i].category = heading # Anzahl WE in Reihenhäusern
        i+=1 ; self.params[i].category = heading # Anzahl WE in Mehrfamilienhäusern

        heading = "3) Wohnen - Anteile Eigentum und Miete"
        i+=1 ; self.params[i].category = heading # Anteil Eigentum in Einfamilienhäusern
        i+=1 ; self.params[i].category = heading # Anteil Eigentum in Doppelhäusern
        i+=1 ; self.params[i].category = heading # Anteil Eigentum in Reihenhäusern
        i+=1 ; self.params[i].category = heading # Anteil Eigentum in Mehrfamilienhäusern

        heading = "4) Wohnen - Einwohner pro Wohneinheit"
        i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Einfamilienhäusern
        i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Doppelhäusern
        i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Reihenhäusern
        i+=1 ; self.params[i].filter.list = list_EwProWE ; self.params[i].category = heading # Ew pro WE in Mehrfamilienhäusern

        heading = "5) Wohnen - Zuzugsquote"
        i+=1 ; self.params[i].category = heading # Zuzugsquote Wohnen

        heading = "6) Gewerbe - Gebietstyp und Brachenstruktur"
        i+=1 ; self.params[i].category = heading # Gebietstyp Gewerbe
        i+=1 ; self.params[i].category = heading # Anteil Verarbeitendes Gewerbe
        i+=1 ; self.params[i].category = heading # Anteil Baugewerbe
        i+=1 ; self.params[i].category = heading # Anteil Handel und Kfz
        i+=1 ; self.params[i].category = heading # Anteil Verkehr und Lagerei
        i+=1 ; self.params[i].category = heading # Anteil Freiberufl. ... Dienstleistungen
        i+=1 ; self.params[i].category = heading # Anteil Sonstige Dienstleistungen

        heading = "7) Gewerbe - Zuzugs- und Eigentumsquote"
        i+=1 ; self.params[i].category = heading # Zuzugsquote Gewerbe
        i+=1 ; self.params[i].category = heading # Anteil Eigentum Gewerbe

        heading = "8) Einzelhandel (nur Lebensmitteleinzelhandel)"
        i+=1 ; self.params[i].category = heading # Verkaufsfläche

        # Vorgabewerte für Aufsiedelung setzen
        self.params[2].value = datetime.datetime.now().year + 1
        self.params[3].value = 5

        return


      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def eingaben_auslesen():

            projectname = self.params[0].value
            teilflaeche = self.params[1].value

            tablepath_flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Wohneinheiten_Details')
            tabelle_gebaude = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gebaeude_Details')
            tabelle_Versorgung_Verkaufsflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Versorgung_Verkaufsflaechen')
            flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Flaechenbilanz')
            plangebiet = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
            tabelle_gewerbeanteile = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Anteile')

            #Startjahr und Aufsiedlungsdauer
            fields = ['Beginn_Nutzung', 'Aufsiedlungsdauer', 'Name', 'Startjahr']
            rows = arcpy.da.SearchCursor(plangebiet,fields)
            for row in rows:
                if row[2] == teilflaeche:
                    self.params[3].value = row[1]
                    if row[0] != None:
                        self.params[2].value = row[0]
                    else:
                        self.params[2].value = row[3]

            # Wohnen - Anzahl Wohneinheiten nach Gebäudetypen
            fields = ['Gebaeudetyp', 'Anzahl_Gebaeude', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tabelle_gebaude,fields)

            efh = 0
            zfh = 0
            rh = 0
            mfh = 0

            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    efh += row[1]
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                       zfh += row[1]
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    rh += row[1]
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    mfh += row[1]

            self.params[4].value = efh
            self.params[5].value = zfh
            self.params[6].value = rh
            self.params[7].value = mfh

            #Wohnen - Anteile Eigentum und Miete
            fields = ['Gebaeudetyp', 'Ant_Eigentuemer', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    self.params[8].value = row[1]
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    self.params[9].value = row[1]
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    self.params[10].value = row[1]
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    self.params[11].value = row[1]

            #Wohnen - Einwohner pro Wohneinheit
            fields = ['Gebaeudetyp', 'EW_je_WE', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    self.params[12].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    self.params[13].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    self.params[14].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    self.params[15].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"

            #Gewerbe
            rows = arcpy.da.SearchCursor(tabelle_gewerbeanteile, ["teilflaeche", "branche", "Anteil_A", "Anteil_B" , "Anteil_C" , "Anteil_D" , "Anteil_E", "Anteil_F", "Anteil_Zuzug", "Anteil_Eigentum"])
            for row in rows:
                if row[0] == teilflaeche:
                    self.params[17].value = row[1]
                    self.params[18].value = row[2]
                    self.params[19].value = row[3]
                    self.params[20].value = row[4]
                    self.params[21].value = row[5]
                    self.params[22].value = row[6]
                    self.params[23].value = row[7]
                    self.params[24].value = row[8]
                    self.params[25].value = row[9]


            #Einzelhandel (nur Lebensmitteleinzelhandel)
            fields = ['Verkaufsflaeche', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tabelle_Versorgung_Verkaufsflaechen,fields)
            for row in rows:
                if row[1] == teilflaeche:
                    self.params[26].value = row[0]

            return


        #import os, arcpy, win32ui, win32con
        import os, arcpy

        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]

        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

    # Gebietstyp auswählen
        i=17
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            gebtyp = self.params[i].value
            tablepath_gebietstyp = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebietstypen')

            rows = arcpy.SearchCursor(tablepath_gebietstyp)

            for row in rows:
                if gebtyp == row.Gebietstyp:
                    self.params[i+1].value = row.Ant_VerarbGew
                    self.params[i+2].value = row.Ant_BauGew
                    self.params[i+3].value = row.Ant_HanKfZ
                    self.params[i+4].value = row.Ant_VerLag
                    self.params[i+5].value = row.Ant_FrWiTeDi
                    self.params[i+6].value = row.Ant_SoDi

    # Automatische Anpassung der Slider
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

        # Pfad zum Ordner, in dem Script liegt, erzeugen
        tbx_path, tool_method = __file__.split('#')
        toolname = tool_method.split('.')[0]
        base_path = os.path.dirname(tbx_path)
        base_path = os.path.dirname(base_path)
        base_path = os.path.dirname(base_path)

        # Auswahl Teilfläche
        i = 0
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            projectname = self.params[i].value

            tablepath_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')
            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append(row.Name)
            list_teilflaechen = sorted(set(list_teilflaechen))
            i+=1 ; self.params[i].filter.list = list_teilflaechen

            if len(list_teilflaechen) == 1:
                self.params[i].value = list_teilflaechen[0]
                eingaben_auslesen()


        # bestehende Eingaben (falls vorhanden) übernehmen
        i = 1
        if self.params[i].altered and not self.params[i].hasBeenValidated:
            eingaben_auslesen()


        # Slider für Anteile an Arbeitsplätzen nach Gewerbetyp generieren
        listeSliderID = [18, 19, 20, 21,22, 23]
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
        self.label = u'2 Nutzungen eingeben'
        self.canRunInBackground = False
    def getParameterInfo(self):
        # Projekt
        param_1 = arcpy.Parameter()
        param_1.name = u'Projekt'
        param_1.displayName = u'Projekt'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'String'
        param_1.filter.list = [u'Test_Achim_2', u'thomas_test_neu']

        # Teilfläche
        param_2 = arcpy.Parameter()
        param_2.name = u'Teilfl\xe4che'
        param_2.displayName = u'Teilfl\xe4che'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'

        # Beginn_der_Aufsiedlung__Jahreszahl_
        param_3 = arcpy.Parameter()
        param_3.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param_3.displayName = u'Beginn der Aufsiedlung (Jahreszahl)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.value = u'2017'

        # Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_
        param_4 = arcpy.Parameter()
        param_4.name = u'Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_'
        param_4.displayName = u'Dauer der Aufsiedlung (Jahre, 1 = Aufsiedlung wird noch im Jahr des Aufsiedlungsbeginns abgeschlossen)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'5'

        # Anzahl_WE_in_Ein-_und_Zweifamilienhäusern
        param_5 = arcpy.Parameter()
        param_5.name = u'Anzahl_WE_in_Ein-_und_Zweifamilienh\xe4usern'
        param_5.displayName = u'Anzahl WE in Ein- und Zweifamilienh\xe4usern'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'0'

        # Anzahl_WE_in_Doppelhäusern
        param_6 = arcpy.Parameter()
        param_6.name = u'Anzahl_WE_in_Doppelh\xe4usern'
        param_6.displayName = u'Anzahl WE in Doppelh\xe4usern'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'0'

        # Anzahl_WE_in_Reihenhäusern
        param_7 = arcpy.Parameter()
        param_7.name = u'Anzahl_WE_in_Reihenh\xe4usern'
        param_7.displayName = u'Anzahl WE in Reihenh\xe4usern'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Long'
        param_7.value = u'0'

        # Anzahl_WE_in_Mehrfamilienhäusern
        param_8 = arcpy.Parameter()
        param_8.name = u'Anzahl_WE_in_Mehrfamilienh\xe4usern'
        param_8.displayName = u'Anzahl WE in Mehrfamilienh\xe4usern'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Long'
        param_8.value = u'0'

        # Anteil_Eigentümernutzung_in_Ein-_und_Zweifamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_9 = arcpy.Parameter()
        param_9.name = u'Anteil_Eigent\xfcmernutzung_in_Ein-_und_Zweifamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_9.displayName = u'Anteil Eigent\xfcmernutzung in Ein- und Zweifamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Long'
        param_9.value = u'90'

        # Anteil_Eigentümernutzung_in_Doppelhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_10 = arcpy.Parameter()
        param_10.name = u'Anteil_Eigent\xfcmernutzung_in_Doppelh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_10.displayName = u'Anteil Eigent\xfcmernutzung in Doppelh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = u'80'

        # Anteil_Eigentümernutzung_in_Reihenhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_11 = arcpy.Parameter()
        param_11.name = u'Anteil_Eigent\xfcmernutzung_in_Reihenh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_11.displayName = u'Anteil Eigent\xfcmernutzung in Reihenh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Long'
        param_11.value = u'70'

        # Anteil_Eigentümernutzung_in_Mehrfamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_12 = arcpy.Parameter()
        param_12.name = u'Anteil_Eigent\xfcmernutzung_in_Mehrfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_12.displayName = u'Anteil Eigent\xfcmernutzung in Mehrfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Long'
        param_12.value = u'20'

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienhäusern__kurz_nach_dem_Bezug_
        param_13 = arcpy.Parameter()
        param_13.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_13.displayName = u'Mittlere Anzahl Einwohner pro WE in Einfamilienh\xe4usern (kurz nach dem Bezug)'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'String'
        param_13.value = u'3,2 Bewohner pro Wohneinheit'
        param_13.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelhäusern__kurz_nach_dem_Bezug_
        param_14 = arcpy.Parameter()
        param_14.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelh\xe4usern__kurz_nach_dem_Bezug_'
        param_14.displayName = u'Mittlere Anzahl Einwohner pro WE in Doppelh\xe4usern (kurz nach dem Bezug)'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'String'
        param_14.value = u'3,0 Bewohner pro Wohneinheit'
        param_14.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenhäusern__kurz_nach_dem_Bezug_
        param_15 = arcpy.Parameter()
        param_15.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenh\xe4usern__kurz_nach_dem_Bezug_'
        param_15.displayName = u'Mittlere Anzahl Einwohner pro WE in Reihenh\xe4usern (kurz nach dem Bezug)'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'String'
        param_15.value = u'3,0 Bewohner pro Wohneinheit'
        param_15.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienhäusern__kurz_nach_dem_Bezug_
        param_16 = arcpy.Parameter()
        param_16.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_16.displayName = u'Mittlere Anzahl Einwohner pro WE in Mehrfamilienh\xe4usern (kurz nach dem Bezug)'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'String'
        param_16.value = u'2,1 Bewohner pro Wohneinheit'
        param_16.filter.list = [u'1,0 Bewohner pro Wohneinheit', u'1,1 Bewohner pro Wohneinheit', u'1,2 Bewohner pro Wohneinheit', u'1,3 Bewohner pro Wohneinheit', u'1,4 Bewohner pro Wohneinheit', u'1,5 Bewohner pro Wohneinheit', u'1,6 Bewohner pro Wohneinheit', u'1,7 Bewohner pro Wohneinheit', u'1,8 Bewohner pro Wohneinheit', u'1,9 Bewohner pro Wohneinheit', u'2,0 Bewohner pro Wohneinheit', u'2,1 Bewohner pro Wohneinheit', u'2,2 Bewohner pro Wohneinheit', u'2,3 Bewohner pro Wohneinheit', u'2,4 Bewohner pro Wohneinheit', u'2,5 Bewohner pro Wohneinheit', u'2,6 Bewohner pro Wohneinheit', u'2,7 Bewohner pro Wohneinheit', u'2,8 Bewohner pro Wohneinheit', u'2,9 Bewohner pro Wohneinheit', u'3,0 Bewohner pro Wohneinheit', u'3,1 Bewohner pro Wohneinheit', u'3,2 Bewohner pro Wohneinheit', u'3,3 Bewohner pro Wohneinheit', u'3,4 Bewohner pro Wohneinheit', u'3,5 Bewohner pro Wohneinheit', u'3,6 Bewohner pro Wohneinheit', u'3,7 Bewohner pro Wohneinheit', u'3,8 Bewohner pro Wohneinheit', u'3,9 Bewohner pro Wohneinheit', u'4,0 Bewohner pro Wohneinheit', u'4,1 Bewohner pro Wohneinheit', u'4,2 Bewohner pro Wohneinheit', u'4,3 Bewohner pro Wohneinheit', u'4,4 Bewohner pro Wohneinheit', u'4,5 Bewohner pro Wohneinheit', u'4,6 Bewohner pro Wohneinheit', u'4,7 Bewohner pro Wohneinheit', u'4,8 Bewohner pro Wohneinheit', u'4,9 Bewohner pro Wohneinheit']

        # Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_
        param_17 = arcpy.Parameter()
        param_17.name = u'Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_'
        param_17.displayName = u'Wie viel Prozent der Bewohner der neuen Wohnungen werden neu in die Gemeinde ziehen?'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Long'
        param_17.value = u'80'

        # Gebietstyp_auswählen
        param_18 = arcpy.Parameter()
        param_18.name = u'Gebietstyp_ausw\xe4hlen'
        param_18.displayName = u'Gebietstyp ausw\xe4hlen'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'String'
        param_18.value = u'<kein Gewerbegebiet vorhanden>'
        param_18.filter.list = [u'Industriegebiet', u'Logistikgebiet', u'Klassisches Gewerbegebiet', u'Kleinteiliges Gewerbegebiet', u'Hoeherwertiges Gewerbegebiet', u'Technologiepark, Wissenschaftspark', u'<kein Gewerbegebiet vorhanden>']

        # Anteil_der_Arbeitsplätze_im_verarbeitenden_Gewerbe__in_Prozent_
        param_19 = arcpy.Parameter()
        param_19.name = u'Anteil_der_Arbeitspl\xe4tze_im_verarbeitenden_Gewerbe__in_Prozent_'
        param_19.displayName = u'Anteil der Arbeitspl\xe4tze im verarbeitenden Gewerbe (in Prozent)'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'Long'
        param_19.value = u'40'

        # Anteil_der_Arbeitsplätze_im_Baugewerbe__in_Prozent_
        param_20 = arcpy.Parameter()
        param_20.name = u'Anteil_der_Arbeitspl\xe4tze_im_Baugewerbe__in_Prozent_'
        param_20.displayName = u'Anteil der Arbeitspl\xe4tze im Baugewerbe (in Prozent)'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'Long'
        param_20.value = u'6'

        # Anteil_der_Arbeitsplätze_im_Handel__inkl__Kfz___in_Prozent_
        param_21 = arcpy.Parameter()
        param_21.name = u'Anteil_der_Arbeitspl\xe4tze_im_Handel__inkl__Kfz___in_Prozent_'
        param_21.displayName = u'Anteil der Arbeitspl\xe4tze im Handel (inkl. Kfz) (in Prozent)'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'Long'
        param_21.value = u'17'

        # Anteil_der_Arbeitsplätze_im_Verkehrs-_und_Lagereibereich___in_Prozent_
        param_22 = arcpy.Parameter()
        param_22.name = u'Anteil_der_Arbeitspl\xe4tze_im_Verkehrs-_und_Lagereibereich___in_Prozent_'
        param_22.displayName = u'Anteil der Arbeitspl\xe4tze im Verkehrs- und Lagereibereich  (in Prozent)'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'Long'
        param_22.value = u'10'

        # Anteil_der_Arbeitsplätze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_
        param_23 = arcpy.Parameter()
        param_23.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_'
        param_23.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich der freiberuflichen, wissenschaftl. bzw. techn. Dienstleistungen (in Prozent)'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'Long'
        param_23.value = u'14'

        # Anteil_der_Arbeitsplätze_im_Bereich_sonstiger_Diensteistungen
        param_24 = arcpy.Parameter()
        param_24.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_sonstiger_Diensteistungen'
        param_24.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich sonstiger Diensteistungen'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'Long'
        param_24.value = u'13'

        # Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_
        param_25 = arcpy.Parameter()
        param_25.name = u'Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_'
        param_25.displayName = u'Wie viel Prozent der Unternehmen werden neu in die Gemeinde ziehen?'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'Long'
        param_25.value = u'80'

        # Welcher_Anteil_der_Gebäude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_
        param_26 = arcpy.Parameter()
        param_26.name = u'Welcher_Anteil_der_Geb\xe4ude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_'
        param_26.displayName = u'Welcher Anteil der Geb\xe4ude ist voraussichtlich im Eigentum der Unternehmen?'
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'Long'
        param_26.value = u'100'

        # Verkaufsfläche__in_Quadratmetern_
        param_27 = arcpy.Parameter()
        param_27.name = u'Verkaufsfl\xe4che__in_Quadratmetern_'
        param_27.displayName = u'Verkaufsfl\xe4che (in Quadratmetern)'
        param_27.parameterType = 'Required'
        param_27.direction = 'Input'
        param_27.datatype = u'Long'
        param_27.value = u'0'

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11, param_12, param_13, param_14, param_15, param_16, param_17, param_18, param_19, param_20, param_21, param_22, param_23, param_24, param_25, param_26, param_27]
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
        with script_run_as(u'C:\\Users\\handke\\Dropbox\\Regioprojectcheck\\2_Tool\\3_Art und Mass der Nutzung\\nutzungen.py'):

            import time
            import datetime
            import sys
            import imp
            import xlsxwriter
            from xlsxwriter.utility import xl_rowcol_to_cell, xl_col_to_name
            import arcpy, os

            projectname = parameters[0].valueAsText
            parameterString = parameters[1].valueAsText

            base_path = str(sys.path[0]).split("2_Tool")[0]
            Teilflaeche_Plangebiet = parameterString.split(" | ")[0]
            tabelle_gebaude = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gebaeude_Details')
            tabelle_wohneinheiten_details = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Wohneinheiten_Details')
            tabelle_verkaufsflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Versorgung_Verkaufsflaechen')
            tabelle_gewerbe = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Teilflaechen')
            tabelle_betriebsflaeche = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Betriebsflaechen')
            tabelle_betriebsstruktur = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Betriebsstruktur')
            tabelle_gewerbeanteile = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gewerbe_Anteile')

            #Alte Eingaben löschen

            with arcpy.da.UpdateCursor(tabelle_gebaude, 'Teilflaeche_Plangebiet') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(tabelle_wohneinheiten_details, 'Teilflaeche_Plangebiet') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(tabelle_verkaufsflaechen, 'Teilflaeche_Plangebiet') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(tabelle_gewerbe, 'teilflaeche') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()


            with arcpy.da.UpdateCursor(tabelle_betriebsflaeche, 'teilflaeche') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(tabelle_betriebsstruktur, 'teilflaeche') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(tabelle_gewerbeanteile, 'teilflaeche') as cursor:
                for row in cursor:
                    if row[0] == Teilflaeche_Plangebiet:
                        cursor.deleteRow()

            # WOHNGEBÄUDE

            flaechenbilanz = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Flaechenbilanz')
            plangebiet = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')

            cursor = arcpy.da.UpdateCursor(plangebiet, ['Name','Beginn_Nutzung','Aufsiedlungsdauer'])
            for row in cursor:
                if row[0] == parameters[1].valueAsText:
                    row[1] = parameters[2].valueAsText
                    row[2] = parameters[3].valueAsText
                    cursor.updateRow(row)

            for i in range(0,int(parameters[3].valueAsText)):

                jahr = int(parameters[2].valueAsText) + i

                messages.AddMessage(jahr)
                Insert = arcpy.da.InsertCursor(tabelle_gebaude, ['Teilflaeche_Plangebiet','Gebaeudetyp','Anzahl_Gebaeude','Jahr'])
                row = ["","","",""]

                #Ein- und Zweifamilienhäuser
                if int(parameters[4].valueAsText) >0:
                    row[0] = parameters[1].valueAsText
                    row[1] = "Einfamilienhaus"
                    row[2] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText)
                    row[3] = jahr
                    Insert.insertRow(row)

                #Doppelhäuser
                if int(parameters[5].valueAsText) >0:
                    row[0] = parameters[1].valueAsText
                    row[1] = "Zweifamilien- oder Doppelhaus"
                    row[2] =  int(parameters[5].valueAsText) / int(parameters[3].valueAsText)
                    row[3] = jahr
                    Insert.insertRow(row)

                #Reihenhäuser
                if int(parameters[6].valueAsText) >0:
                    row[0] = parameters[1].valueAsText
                    row[1] = "Reihenhaus"
                    row[2] =  int(parameters[6].valueAsText) / int(parameters[3].valueAsText)
                    row[3] = jahr
                    Insert.insertRow(row)

                #Mehrfamilienhäuser
                if int(parameters[7].valueAsText) >0:
                    row[0] = parameters[1].valueAsText
                    row[1] = "Mehrfamilienhaus"
                    row[2] =  int(parameters[7].valueAsText) / int(parameters[3].valueAsText)
                    row[3] = jahr
                    Insert.insertRow(row)

                del row, Insert

                #tabelle "Wohneinheiten_Details" oeffnen und Werte fuer Miete_Eigentum. und Anzahl Wohneinheiten speichern
                tabelle_wohneinheiten_details = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Wohneinheiten_Details')

                Insert = arcpy.da.InsertCursor(tabelle_wohneinheiten_details, ['Gebaeudetyp','Teilflaeche_Plangebiet','Miete_Eigentum','EW_je_WE','Jahr','Anzahl_WE', 'Ant_Eigentuemer'])
                row = ["","","","","","",""]

                #Ein- und Zweifamilienhäuser
                eigentum = int(parameters[8].valueAsText)
                miete = 100 - int(parameters[8].valueAsText)
                nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

                for nutzungstyp in nutzungstypen:
                    row[0] = "Einfamilienhaus"
                    row[1] = parameters[1].valueAsText
                    row[2] = nutzungstyp[1]
                    row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                    row[4] = jahr
                    row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                    row[6] = parameters[8].valueAsText
                    Insert.insertRow(row)

                #Doppelhäuser
                eigentum = int(parameters[9].valueAsText)
                miete = 100 - int(parameters[9].valueAsText)
                nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

                for nutzungstyp in nutzungstypen:
                    row[0] = "Zweifamilien- oder Doppelhaus"
                    row[1] = parameters[1].valueAsText
                    row[2] = nutzungstyp[1]
                    row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                    row[4] = jahr
                    row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                    row[6] = parameters[9].valueAsText
                    Insert.insertRow(row)

                #Reihenhäuser
                eigentum = int(parameters[10].valueAsText)
                miete = 100 - int(parameters[10].valueAsText)
                nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

                for nutzungstyp in nutzungstypen:
                    row[0] = "Reihenhaus"
                    row[1] = parameters[1].valueAsText
                    row[2] = nutzungstyp[1]
                    row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                    row[4] = jahr
                    row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                    row[6] = parameters[10].valueAsText
                    Insert.insertRow(row)

                #RMehrfamilienhäuser
                eigentum = int(parameters[11].valueAsText)
                miete = 100 - int(parameters[11].valueAsText)
                nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

                for nutzungstyp in nutzungstypen:
                    row[0] = "Mehrfamilienhaus"
                    row[1] = parameters[1].valueAsText
                    row[2] = nutzungstyp[1]
                    row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                    row[4] = jahr
                    row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                    row[6] = parameters[11].valueAsText
                    Insert.insertRow(row)

            del row, Insert


            # GEWERBE

            Insert = arcpy.InsertCursor(tabelle_gewerbeanteile)
            row = Insert.newRow()
            row.setValue("teilflaeche", parameters[1].valueAsText)
            row.setValue("branche", parameters[17].valueAsText)
            row.setValue("Anteil_A", parameters[18].valueAsText)
            row.setValue("Anteil_B", parameters[19].valueAsText)
            row.setValue("Anteil_C", parameters[20].valueAsText)
            row.setValue("Anteil_D", parameters[21].valueAsText)
            row.setValue("Anteil_E", parameters[22].valueAsText)
            row.setValue("Anteil_F", parameters[23].valueAsText)
            row.setValue("Anteil_Zuzug", parameters[24].valueAsText)
            row.setValue("Anteil_Eigentum", parameters[25].valueAsText)
            Insert.insertRow(row)
            del row, Insert


            base_path = str(sys.path[0]).split("2_Tool")[0]
            sheetlibpath = os.path.join(base_path,'2_Tool',"2_Projektverwaltung",'sheet_lib.py')
            sl = imp.load_source('sheet_lib', sheetlibpath)

            def beschaeftigte_gewerbe(projektname):

                #Pfade anlegen
                base_path = str(sys.path[0]).split("2_Tool")[0]
                shape_bkggemeiden=os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','bkg_gemeinden')
                workspace_Basis_Daten_Versor=os.path.join(base_path,'2_Tool',"G_Standortkonkurrenz_Supermaerkte",'FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb')
                workspace_Basis_Daten=os.path.join(base_path,'2_Tool',"3_Art und Mass der Nutzung",'FGDB_Definition_Projekt_Tool.gdb')
                shape_teilflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Teilflaechen_Plangebiet')
                workspace_definition= os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')


                # Process: Layer lagebezogen auswählen
                arcpy.MakeFeatureLayer_management(shape_bkggemeiden, 'bkg_gemeinden_lyr')
                arcpy.SelectLayerByLocation_management('bkg_gemeinden_lyr', "CONTAINS",shape_teilflaeche , "", "NEW_SELECTION")


                # If features matched criterias write them to a new feature class
                matchcount = int(arcpy.GetCount_management('bkg_gemeinden_lyr').getOutput(0))
                if matchcount == 0:
                    b='Zuordnung zu einer Gemeinde unmoeglich - Kontaktieren Sie den Programmierer.'
                    print b
                    messages.AddMessage(b)
                    exit(1)
                else:
                    AGS=0
                    GAGS=0
                    cur_Search_Lry=arcpy.SearchCursor('bkg_gemeinden_lyr')
                    for a in cur_Search_Lry:
                        AGS=int(a.AGS)
                        print "AGS ",AGS
                        break
                    del cur_Search_Lry

                    cur_Sear_GGEN= arcpy.SearchCursor(os.path.join(workspace_Basis_Daten_Versor,"Gesamtgemeinden"))

                    array_ags_gags=[]
                    for speicher in cur_Sear_GGEN:
                        array_ags_gags.append([int(speicher.AGS),int(speicher.VAGS)])

                    del speicher,cur_Sear_GGEN

                    for b in array_ags_gags:
                        if AGS==b[0]:
                            GAGS=b[1]
                            print "GAGS ",GAGS
                            break

                    del array_ags_gags

                    array_branche_anzahl=[]
                    cur_Search_beschaeftigte= arcpy.SearchCursor(os.path.join(workspace_definition,"Gewerbe_Teilflaechen"))

                    for c in cur_Search_beschaeftigte:
                        if len(array_branche_anzahl)==0:
                            array_branche_anzahl.append([str(c.branche),(c.beschaeftigte)])
                        else:
                            if len([t for t in array_branche_anzahl if t[0]==c.Branche])>0:
                                #bereits vorhanden
                                for z in array_branche_anzahl:
                                    if z[0]==c.branche:
                                        z[1]+=(c.beschaeftigte)


                            else:
                                array_branche_anzahl.append([str(c.branche),(c.beschaeftigte)])

                    print array_branche_anzahl
                    del cur_Search_beschaeftigte



                    #gesamtgemeinde + anzahl beschaeftigte pro branche -> multiplikation -> fertig
                    gesamt_anzahl=0
                    for hh in array_branche_anzahl:
                        gesamt_anzahl+=hh[1]

                    print gesamt_anzahl
                    gesamt_anzahl=round(gesamt_anzahl)
                    print "Gesamt anzahl ",gesamt_anzahl
                    array_ergebnis=[]

                    print "Teilzeit"
                    cur_Search_teilzeit = arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"gewerbe_teilzeit"))
                    for p in cur_Search_teilzeit:
                        laenge= len(str(p.NR))
                        if (p.Nr == int(str(GAGS)[:laenge])):
            ##                print p.Nr
                            b1=0
                            faktor=0
                            for branchen in array_branche_anzahl:
                                faktor=p.getValue(branchen[0])
                                b1 += (faktor*branchen[1])/100.
            ##                    print "Faktor ",faktor,"Branche",branchen[0],"Anzahl Besch",branchen[1] ,"Ergebnis",faktor*branchen[1]
                            b1=int(b1)
                            array_ergebnis.append(["Teilzeit",b1])
                            break
            ##        print "Summe der einzelnen Ergebnisse ",b1
            ##        print array_ergebnis
                    del cur_Search_teilzeit
            ##        print "Geringfuegig"
                    cur_Search_gering = arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"gewerbe_geringfuegig"))
                    for p in cur_Search_gering:
                        laenge= len(str(p.NR))
                        if (p.Nr == int(str(GAGS)[:laenge])):
                            b1=0
                            faktor=0
                            for branchen in array_branche_anzahl:
                                faktor=p.getValue(branchen[0])
                                b1 += (faktor*branchen[1])/100.
                                print "Faktor ",faktor ,"Ergebnis",b1
                            b1=int(b1)
                            array_ergebnis.append(["Geringfuegig",b1])
                            break

            ##        print array_ergebnis
                    del cur_Search_gering
                    print "Akademisch"
                    cur_Search_akademisch = arcpy.SearchCursor(os.path.join(workspace_Basis_Daten,"gewerbe_akademisch"))
                    for p in cur_Search_akademisch:
                        laenge= len(str(p.NR))
                        if (p.Nr == int(str(GAGS)[:laenge])):
                            b1=0
                            faktor=0
                            for branchen in array_branche_anzahl:
                                faktor=p.getValue(branchen[0])
                                b1 += (faktor*branchen[1])/100.
                                print "Faktor ",faktor ,"Ergebnis",b1
                            b1=int(b1)
                            array_ergebnis.append(["Hochschulausbildung",b1])
                            array_ergebnis.append(["Gesamt",int(gesamt_anzahl)])
                            break

                    print array_ergebnis
                    del cur_Search_akademisch,array_branche_anzahl,gesamt_anzahl


                    try:
                        arcpy.Delete_management(os.path.join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
            ##            arcpy.Delete_management(os.path.join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
            ##            arcpy.DeleteFeatures_management("Gewerbe_Beschaeftigte_Zahlen")
                    except:
                        pass

                    try:
                        arcpy.CreateTable_management(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen")

                    except:
                        a="Fehler Gewerbe_Beschaeftigte_Zahlen konnte nicht erstellt werden. Bitte ArcGis neustarten oder alle Files schliessen."
                        print a
                        messages.AddErrorMessage(a)
                        exit(1)

                    try:
                        arcpy.AddField_management(os.path.join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"), "Info", "TEXT",250)
                        arcpy.AddField_management(os.path.join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"), "Anzahl", "LONG")

                    except:
                        a="Fehler Gewerbe_Beschaeftigte_Zahlen konnte nicht erstellt werden. Bitte ArcGis neustarten oder alle Files schliessen."
                        print a
                        messages.AddErrorMessage(a)
                        exit(1)

                    cur_Ins_beschaef= arcpy.InsertCursor(os.path.join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
                    for a in array_ergebnis:
                        row = cur_Ins_beschaef.newRow()
                        row.setValue("Info",a[0])
                        row.setValue("Anzahl",a[1])
                        cur_Ins_beschaef.insertRow(row)

                    del cur_Ins_beschaef



            schrittmeldung = 'Eingaben werden gelesen \n'
            messages.AddMessage(schrittmeldung)
            print schrittmeldung

            #Parameter aus Tool auslesen

            projektname = parameters[0].valueAsText
            teilflaeche = parameters[1].valueAsText
            startjahr = parameters[2].valueAsText
            aufsiedlungsdauer = parameters[3].valueAsText
            gebtyp = parameters[17].valueAsText
            zuzugsquote = parameters[24].valueAsText
            eigentumsquote = parameters[25].valueAsText
            Ant_Betr_VerarbGew = parameters[18].valueAsText
            Ant_Betr_BauGew = parameters[19].valueAsText
            Ant_Betr_HanKfZ = parameters[20].valueAsText
            Ant_Betr_VerLag = parameters[21].valueAsText
            Ant_Betr_FrWiTeDi = parameters[22].valueAsText
            Ant_Betr_SoDi = parameters[23].valueAsText

            if gebtyp != "<kein Gewerbegebiet vorhanden>":

                ######################################################
                #Prüfung der Branchenstruktur auf 100%
                SummeBranchen = int(Ant_Betr_VerarbGew) + int(Ant_Betr_BauGew) + int(Ant_Betr_HanKfZ) + int(Ant_Betr_VerLag) + int(Ant_Betr_FrWiTeDi) + int(Ant_Betr_SoDi)

                if SummeBranchen < 100:
                    schrittmeldung = 'Die Summe der Branchenanteile liegt unter 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
                elif SummeBranchen > 100:
                    schrittmeldung = 'Die Summe der Branchenanteile liegt ueber 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
                else:
                    ######################################################
                    #Zeitstempel definieren
                    import time
                    import datetime
                    ts = time.time()
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                    ######################################################
                    #Flaechenbilanz berechnen

                    #Pfade anlegen
                    base_path = str(sys.path[0]).split("2_Tool")[0]
                    tabelle_flaechenbilanzgrundlage = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_flaechenutzungsbilanz')
                    tabelle_flaechennutzung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Flaechenbilanz_Planung_Prozent')
                    shape_teilflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Teilflaechen_Plangebiet')
                    flaechenbilanz = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Flaechenbilanz')

                    #Größe der Gewerbefläche auslesen
                    flaechenbilanz_cursor = arcpy.SearchCursor(flaechenbilanz)

                    for row in flaechenbilanz_cursor:
                        if row.Teilflaeche_Plangebiet == teilflaeche and row.Flaechennutzung_S2 == "Gewerbeflaeche":
                            flaechengroesse = row.Flaeche_ha


                    #In Abhaengigkeit vom Gebietstyp die Flaechenbilanz definieren
                    # Dazu zunächst die Anteilswerte aus Grundlagentabelle auslesen
                    rows_flaechenbilanzgrundlage = arcpy.SearchCursor(tabelle_flaechenbilanzgrundlage)
                    ant_s2_allgGruen = 0
                    ant_s2_strBeglGruen = 0
                    ant_s2_InErsch = 0
                    ant_s2_GewBauland = 0

                    for row in rows_flaechenbilanzgrundlage:
                        if row.Flaechennutzung_S1 == "Gruenflaeche":
                            if row.Flaechennutzung_S2 == "Allgemeine Gruenflaechen":
                                if gebtyp == "Industriegebiet":
                                    ant_s2_allgGruen = row.Industriegebiet
                                elif gebtyp == "Logistikgebiet":
                                    ant_s2_allgGruen = row.Logistikgebiet
                                elif gebtyp == "Klassisches Gewerbegebiet":
                                    ant_s2_allgGruen = row.Klass_Gewerbe
                                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                    ant_s2_allgGruen = row.Klein_Gewerbe
                                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                    ant_s2_allgGruen = row.Hoeher_Gewerbe
                                elif gebtyp == "Technologiepark, Wissenschaftspark":
                                    ant_s2_allgGruen = row.TechWissPark
                            if row.Flaechennutzung_S2 == "Strassenbegleitgruen":
                                if gebtyp == "Industriegebiet":
                                    ant_s2_strBeglGruen = row.Industriegebiet
                                elif gebtyp == "Logistikgebiet":
                                    ant_s2_strBeglGruen = row.Logistikgebiet
                                elif gebtyp == "Klassisches Gewerbegebiet":
                                    ant_s2_strBeglGruen = row.Klass_Gewerbe
                                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                    ant_s2_strBeglGruen = row.Klein_Gewerbe
                                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                    ant_s2_strBeglGruen = row.Hoeher_Gewerbe
                                elif gebtyp == "Technologiepark, Wissenschaftspark":
                                    ant_s2_strBeglGruen = row.TechWissPark
                        if row.Flaechennutzung_S1 == "Erschliessungsflaeche":
                            if row.Flaechennutzung_S2 == "Oeffentlich - Innere Erschliessung":
                                if gebtyp == "Industriegebiet":
                                    ant_s2_InErsch = row.Industriegebiet
                                elif gebtyp == "Logistikgebiet":
                                    ant_s2_InErsch = row.Logistikgebiet
                                elif gebtyp == "Klassisches Gewerbegebiet":
                                    ant_s2_InErsch = row.Klass_Gewerbe
                                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                    ant_s2_InErsch = row.Klein_Gewerbe
                                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                    ant_s2_InErsch = row.Hoeher_Gewerbe
                                elif gebtyp == "Technologiepark, Wissenschaftspark":
                                    ant_s2_InErsch = row.TechWissPark
                        if row.Flaechennutzung_S1 == "Nettobauland":
                            if row.Flaechennutzung_S2 == "Gewerbeflaeche":
                                if gebtyp == "Industriegebiet":
                                    ant_s2_GewBauland = row.Industriegebiet
                                elif gebtyp == "Logistikgebiet":
                                    ant_s2_GewBauland = row.Logistikgebiet
                                elif gebtyp == "Klassisches Gewerbegebiet":
                                    ant_s2_GewBauland = row.Klass_Gewerbe
                                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                    ant_s2_GewBauland = row.Klein_Gewerbe
                                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                    ant_s2_GewBauland = row.Hoeher_Gewerbe
                                elif gebtyp == "Technologiepark, Wissenschaftspark":
                                    ant_s2_GewBauland = row.TechWissPark


                    # und dann die definierten Anteile mit der Projektflaeche multiplizieren
                    s2_allgGrue = flaechengroesse * ant_s2_allgGruen / 100
                    s2_strBeglGrue = flaechengroesse * ant_s2_strBeglGruen / 100
                    s2_InErsch = flaechengroesse * ant_s2_InErsch / 100
                    s2_GewBauland = flaechengroesse * ant_s2_GewBauland / 100


                    ######################################################
                    # Anzahl der Betriebe nach Branchen bestimmen
                    schrittmeldung = 'Branchenstrukturberechnung wird vorbereitet \n'
                    messages.AddMessage(schrittmeldung)
                    print schrittmeldung

                    # erstmal Pfade definieren
                    tabelle_BFG = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_betriebsflaechengroesse')
                    tabelle_betriebsstruktur = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Betriebsstruktur')

                    # dann zunächst die Betriebsanteile mit den definierten Parzellengrößen gewichten
                    rows_BFG = arcpy.SearchCursor(tabelle_BFG)

                    for row in rows_BFG:
                        if row.Branche == "C":
                            BFG_Betr_VerarbGew = float(row.Betriebsflaechengroesse_ha)
                        if row.Branche == "F":
                            BFG_Betr_BauGew = float(row.Betriebsflaechengroesse_ha)
                        if row.Branche == "G":
                            BFG_Betr_HanKfZ = float(row.Betriebsflaechengroesse_ha)
                        if row.Branche == "H":
                            BFG_Betr_VerLag = float(row.Betriebsflaechengroesse_ha)
                        if row.Branche == "M":
                            BFG_Betr_FrWiTeDi = float(row.Betriebsflaechengroesse_ha)
                        if row.Branche == "N":
                            BFG_Betr_SoDi = float(row.Betriebsflaechengroesse_ha)

                    Flaeche_Betr_VerarbGew_temp = float(Ant_Betr_VerarbGew) * BFG_Betr_VerarbGew
                    Flaeche_Betr_BauGew_temp = float(Ant_Betr_BauGew) * BFG_Betr_BauGew
                    Flaeche_Betr_HanKfZ_temp = float(Ant_Betr_HanKfZ) * BFG_Betr_HanKfZ
                    Flaeche_Betr_VerLag_temp = float(Ant_Betr_VerLag) * BFG_Betr_VerLag
                    Flaeche_Betr_FrWiTeDi_temp = float(Ant_Betr_FrWiTeDi) * BFG_Betr_FrWiTeDi
                    Flaeche_Betr_SoDi_temp = float(Ant_Betr_SoDi) * BFG_Betr_SoDi

                    Flaeche_Gesamt_Temp = Flaeche_Betr_VerarbGew_temp + Flaeche_Betr_BauGew_temp + Flaeche_Betr_HanKfZ_temp + Flaeche_Betr_VerLag_temp + Flaeche_Betr_FrWiTeDi_temp + Flaeche_Betr_SoDi_temp

                    #daraus die Flächenanteile ermitteln
                    schrittmeldung = 'Gewerbeflaeche nach Branchen wird berechnet \n'
                    messages.AddMessage(schrittmeldung)
                    print schrittmeldung

                    gewerbebauland = float(s2_GewBauland)
                    Flaeche_Betr_VerarbGew = float(Flaeche_Betr_VerarbGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                    Flaeche_Betr_BauGew = float(Flaeche_Betr_BauGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                    Flaeche_Betr_HanKfZ = float(Flaeche_Betr_HanKfZ_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                    Flaeche_Betr_VerLag = float(Flaeche_Betr_VerLag_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                    Flaeche_Betr_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                    Flaeche_Betr_SoDi = float(Flaeche_Betr_SoDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)

                    #und über die BFG wieder zur Anzahl der Betriebe
                    schrittmeldung = 'Betriebszahl nach Branchen wird berechnet \n'
                    messages.AddMessage(schrittmeldung)
                    print schrittmeldung
                    BFGfaktor = 1.00
                    if gebtyp == "Industriegebiet":
                        BFGfaktor = 1.50
                    elif gebtyp == "Logistikgebiet":
                        BFGfaktor = 1.50
                    elif gebtyp == "Klassisches Gewerbegebiet":
                        BFGfaktor = 1.00
                    elif gebtyp == "Kleinteiliges Gewerbegebiet":
                        BFGfaktor = 0.70
                    elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                        BFGfaktor = 0.90
                    elif gebtyp == "Technologiepark, Wissenschaftspark":
                        BFGfaktor = 0.85
                    Anz_Betr_VerarbGew = Flaeche_Betr_VerarbGew / (BFG_Betr_VerarbGew * BFGfaktor)
                    Anz_Betr_BauGew = Flaeche_Betr_BauGew / (BFG_Betr_BauGew * BFGfaktor)
                    Anz_Betr_HanKfZ = Flaeche_Betr_HanKfZ / (BFG_Betr_HanKfZ * BFGfaktor)
                    Anz_Betr_VerLag = Flaeche_Betr_VerLag / (BFG_Betr_VerLag * BFGfaktor)
                    Anz_Betr_FrWiTeDi = Flaeche_Betr_FrWiTeDi / (BFG_Betr_FrWiTeDi * BFGfaktor)
                    Anz_Betr_SoDi = Flaeche_Betr_SoDi / (BFG_Betr_SoDi * BFGfaktor)

                    #Betriebsflaechen nach Branchen in Tabelle schreiben
                    tabelle_betriebsflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Betriebsflaechen')
                    tabelle_betriebsflaeche_Insert = arcpy.InsertCursor(tabelle_betriebsflaeche)

                    rowBFins = tabelle_betriebsflaeche_Insert.newRow()

                    rowBFins.teilflaeche = teilflaeche
                    rowBFins.gebietstyp = str(gebtyp)
                    rowBFins.Betriebsflaeche_C = float(Flaeche_Betr_VerarbGew)
                    rowBFins.Betriebsflaeche_F = float(Flaeche_Betr_BauGew)
                    rowBFins.Betriebsflaeche_G = float(Flaeche_Betr_HanKfZ)
                    rowBFins.Betriebsflaeche_H = float(Flaeche_Betr_VerLag)
                    rowBFins.Betriebsflaeche_M = float(Flaeche_Betr_FrWiTeDi)
                    rowBFins.Betriebsflaeche_N = float(Flaeche_Betr_SoDi)
                    rowBFins.timestamp = str(timestamp)

                    tabelle_betriebsflaeche_Insert.insertRow(rowBFins)


                    #und nun noch die Beschäftigten berechnen
                    schrittmeldung = 'Beschaeftigtenzahl nach Branchen wird berechnet \n'
                    messages.AddMessage(schrittmeldung)
                    print schrittmeldung

                    tabelle_FKZ = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_flaechenkennziffern')
                    rows_FKZ = arcpy.SearchCursor(tabelle_FKZ)

                    for row in rows_FKZ:
                        if row.Branche == "C":
                            FKZ_VerarbGew = float(row.Beschaeftigte_je_Hektar)
                        if row.Branche == "F":
                            FKZ_BauGew = float(row.Beschaeftigte_je_Hektar)
                        if row.Branche == "G":
                            FKZ_HanKfZ = float(row.Beschaeftigte_je_Hektar)
                        if row.Branche == "H":
                            FKZ_VerLag = float(row.Beschaeftigte_je_Hektar)
                        if row.Branche == "M":
                            FKZ_FrWiTeDi = float(row.Beschaeftigte_je_Hektar)
                        if row.Branche == "N":
                            FKZ_SoDi = float(row.Beschaeftigte_je_Hektar)

                    Besch_VerarbGew = float(Flaeche_Betr_VerarbGew) * float(FKZ_VerarbGew)
                    Besch_BauGew = float(Flaeche_Betr_BauGew) * float(FKZ_BauGew)
                    Besch_HanKfZ = float(Flaeche_Betr_HanKfZ) * float(FKZ_HanKfZ)
                    Besch_VerLag = float(Flaeche_Betr_VerLag) * float(FKZ_VerLag)
                    Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
                    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)

                    ################################################
                    ### Aufsiedlugnsdauer einrechnen
                    schrittmeldung = 'Aufsiedlungsdauer wird auf Flaechen-, Betriebs- Beschaeftigtenstruktur umgelegt \n'
                    messages.AddMessage(schrittmeldung)
                    print schrittmeldung

                    #### Aufsiedlugnsdauer Betriebe
                    # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
                    tabelle_parameter_aufsiedlungsdauer = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
                    tabelle_gewerbe_betriebsstruktur_Insert = arcpy.InsertCursor(tabelle_betriebsstruktur)

                    #für Branche C
                    anzahl_betriebe_start = Anz_Betr_VerarbGew
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)

                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer, sql)
                    for row2 in tabelle_parameter_aufsiedlungsdauer_Search:
                        parameter_jahr1 = row2.Jahr1
                        parameter_jahr2 = row2.Jahr2
                        parameter_jahr3 = row2.Jahr3
                        parameter_jahr4 = row2.Jahr4
                        parameter_jahr5 = row2.Jahr5
                        parameter_jahr6 = row2.Jahr6
                        parameter_jahr7 = row2.Jahr7
                        parameter_jahr8 = row2.Jahr8
                        parameter_jahr9 = row2.Jahr9
                        parameter_jahr10 = row2.Jahr10
                        parameter_jahr11 = row2.Jahr11
                        parameter_jahr12 = row2.Jahr12
                        parameter_jahr13 = row2.Jahr13
                        parameter_jahr14 = row2.Jahr14
                        parameter_jahr15 = row2.Jahr15
                        parameter_jahr16 = row2.Jahr16
                        parameter_jahr17 = row2.Jahr17
                        parameter_jahr18 = row2.Jahr18
                        parameter_jahr19 = row2.Jahr19
                        parameter_jahr20 = row2.Jahr20
                        parameter_jahr21 = row2.Jahr21
                        parameter_jahr22 = row2.Jahr22
                        parameter_jahr23 = row2.Jahr23
                        parameter_jahr24 = row2.Jahr24
                        parameter_jahr25 = row2.Jahr25
                        parameter_jahr26 = row2.Jahr26
                        parameter_jahr27 = row2.Jahr27
                        parameter_jahr28 = row2.Jahr28
                        parameter_jahr29 = row2.Jahr29
                        parameter_jahr30 = row2.Jahr30
                    del tabelle_parameter_aufsiedlungsdauer_Search

                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "C"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                    #für Branche F
                    anzahl_betriebe_start = Anz_Betr_BauGew
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "F"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


                    #für Branche G
                    anzahl_betriebe_start = Anz_Betr_HanKfZ
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "G"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


                    #für Branche H
                    anzahl_betriebe_start = Anz_Betr_VerLag
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "H"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                    #für Branche M
                    anzahl_betriebe_start = Anz_Betr_FrWiTeDi
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "M"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                    #für Branche N
                    anzahl_betriebe_start = Anz_Betr_SoDi
                    aufsiedlungsdauer = str(aufsiedlungsdauer)

                    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                    row3.projekt = projektname
                    row3.teilflaeche = teilflaeche
                    row3.branche = "N"
                    row3.ID_ts = timestamp

                    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)



                    #### Aufsiedlugnsdauer Beschäftigte
                    # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
                    tabelle_parameter_aufsiedlungsdauer = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
                    tabelle_beschaeftigte = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Beschaeftigte')
                    tabelle_beschaeftigte_insert = arcpy.InsertCursor(tabelle_beschaeftigte)
                    tabelle_projektrahmendaten = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Projektrahmendaten')

                    #Beschaeftigte Branche C / Besch_VerarbGew
                    anzahl_Besch_max = float(Besch_VerarbGew)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "C"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)


                    #Beschaeftigte Branche F / Besch_BauGew
                    anzahl_Besch_max = float(Besch_BauGew)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "F"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)


                    #Beschaeftigte Branche G / Besch_HanKfZ
                    anzahl_Besch_max = float(Besch_HanKfZ)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "G"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)

                    Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
                    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
                    #Beschaeftigte Branche H / Besch_VerLag
                    anzahl_Besch_max = float(Besch_VerLag)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "H"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)


                    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
                    #Beschaeftigte Branche M / Besch_FrWiTeDi
                    anzahl_Besch_max = float(Besch_FrWiTeDi)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "M"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)


                    #Beschaeftigte Branche N / Besch_SoDi
                    anzahl_Besch_max = float(Besch_SoDi)
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    Besch_Jahr = 0
                    Besch_Jahr_neu = 0
                    row3 = tabelle_beschaeftigte_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                            Besch_Jahr = float(Besch_Jahr)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)
                            jahraufsiedlung = jahraufsiedlung + 1

                        else:
                            Besch_Jahr = float(anzahl_Besch_max)
                            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                            Besch_Jahr_neu = float(Besch_Jahr_neu)

                        row3.jahr = long(jahrcount) + long(startjahr)
                        row3.Teilflaeche_Plangebiet = teilflaeche
                        row3.Branche = "N"
                        row3.Anzahl = float(Besch_Jahr)
                        row3.Anzahl_neu = float(Besch_Jahr_neu)
                        row3.ID_ts = timestamp
                        tabelle_beschaeftigte_insert.insertRow(row3)

                    ##############################
                    ## Gebaeude berechnen

                    schrittmeldung = 'Gebaeudedaten werden berechnet \n'
                    messages.AddMessage(schrittmeldung)
                    print str(schrittmeldung)

                    tabelle_gebaeudegrundlagen = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebaeude')
                    tabelle_gebaeudedetails = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Gebaeude_Details')
                    tabelle_gebaeudedetails_insert = arcpy.InsertCursor(tabelle_gebaeudedetails)

                    rows_GGF = arcpy.SearchCursor(tabelle_gebaeudegrundlagen)
                    GGF_halle = 0
                    GGF_verwaltung = 0
                    GeVo_halle = 0
                    GeVo_verwlatung = 0

                    for row in rows_GGF:
                        if row.Branche == "C":
                            GGF_halle_VerarbGew = float(row.anteil_halle) * float(Flaeche_Betr_VerarbGew)
                            GGF_verwaltung_VerarbGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerarbGew)
                            GeVo_halle_VerarbGew = float(GGF_halle_VerarbGew) * float(row.hoehe_halle)
                            GeVo_verwaltung_VerarbGew = float(GGF_verwaltung_VerarbGew) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_VerarbGew)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerarbGew)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerarbGew)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerarbGew)
                        if row.Branche == "F":
                            GGF_halle_BauGew = float(row.anteil_halle) * float(Flaeche_Betr_BauGew)
                            GGF_verwaltung_BauGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_BauGew)
                            GeVo_halle_BauGew = float(GGF_halle_BauGew) * float(row.hoehe_halle)
                            GeVo_verwaltung_BauGew = float(GGF_verwaltung_BauGew) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_BauGew)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_BauGew)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_BauGew)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_BauGew)
                        if row.Branche == "G":
                            GGF_halle_HanKfZ = float(row.anteil_halle) * float(Flaeche_Betr_HanKfZ)
                            GGF_verwaltung_HanKfZ = float(row.anteil_verwaltung) * float(Flaeche_Betr_HanKfZ)
                            GeVo_halle_HanKfZ = float(GGF_halle_HanKfZ) * float(row.hoehe_halle)
                            GeVo_verwaltung_HanKfZ = float(GGF_verwaltung_HanKfZ) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_HanKfZ)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_HanKfZ)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_HanKfZ)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_HanKfZ)
                        if row.Branche == "H":
                            GGF_halle_VerLag = float(row.anteil_halle) * float(Flaeche_Betr_VerLag)
                            GGF_verwaltung_VerLag = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerLag)
                            GeVo_halle_VerLag = float(GGF_halle_VerLag) * float(row.hoehe_halle)
                            GeVo_verwaltung_VerLag = float(GGF_verwaltung_VerLag) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_VerLag)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerLag)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerLag)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerLag)
                        if row.Branche == "M":
                            GGF_halle_FrWiTeDi = float(row.anteil_halle) * float(Flaeche_Betr_FrWiTeDi)
                            GGF_verwaltung_FrWiTeDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_FrWiTeDi)
                            GeVo_halle_FrWiTeDi = float(GGF_halle_FrWiTeDi) * float(row.hoehe_halle)
                            GeVo_verwaltung_FrWiTeDi = float(GGF_verwaltung_FrWiTeDi) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_FrWiTeDi)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_FrWiTeDi)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_FrWiTeDi)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_FrWiTeDi)
                        if row.Branche == "N":
                            GGF_halle_SoDi = float(row.anteil_halle) * float(Flaeche_Betr_SoDi)
                            GGF_verwaltung_SoDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_SoDi)
                            GeVo_halle_SoDi = float(GGF_halle_SoDi) * float(row.hoehe_halle)
                            GeVo_verwaltung_SoDi = float(GGF_verwaltung_SoDi) * float(row.hoehe_verwaltung)
                            GGF_halle = float(GGF_halle) + float(GGF_halle_SoDi)
                            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_SoDi)
                            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_SoDi)
                            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_SoDi)


                    ## Gebaeude für Hallen nach Aufsiedlugnszeit berechnen
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    GGF_jahr = 0
                    GeVo_jahr = 0
                    grundstuecksflaeche_jahr = 0

                    rowGeb = tabelle_gebaeudedetails_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            GGF_jahr = float(GGF_halle) * float(parameter_jahr) * 10000
                            GeVo_jahr = float(GeVo_halle) * float(parameter_jahr) * 10000
                            grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
                            jahraufsiedlung = jahraufsiedlung + 1
                        else:
                            GGF_jahr = float(GGF_halle) * 10000
                            GeVo_jahr = float(GeVo_halle) * 10000
                            grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

                        rowGeb.jahr = long(jahrcount) + long(startjahr)
                        rowGeb.Teilflaeche_Plangebiet = teilflaeche
                        rowGeb.Gebaeudetyp = "Hallen"
                        rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
                        rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
                        rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
                        rowGeb.Geb_ID = timestamp

                        tabelle_gebaeudedetails_insert.insertRow(rowGeb)

                    ## Gebaeude für Bürogebaude nach Aufsiedlugnszeit berechnen
                    aufsiedlungsdauer = str(aufsiedlungsdauer)
                    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                    for row in rows_projektrahmen:
                        ende = row.Ende_Betrachtungszeitraum
                        ende = long(ende) + 1

                    anfang = long(startjahr)
                    dauer = long(aufsiedlungsdauer)
                    jahr = long(startjahr) - 1
                    GGF_jahr = 0
                    GeVo_jahr = 0
                    grundstuecksflaeche_jahr = 0


                    rowGeb = tabelle_gebaeudedetails_insert.newRow()
                    jahrcount = -1
                    jahraufsiedlung = 1
                    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                    for jahr in range(anfang, ende):
                        jahrcount = jahrcount + 1
                        jahr = jahr + 1
                        if jahr < vollaufsiedlung:
                            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                            GGF_jahr = float(GGF_verwaltung) * float(parameter_jahr) * 10000
                            GeVo_jahr = float(GeVo_verwlatung) * float(parameter_jahr) * 10000
                            grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
                            jahraufsiedlung = jahraufsiedlung + 1
                        else:
                            GGF_jahr = float(GGF_verwaltung) * 10000
                            GeVo_jahr = float(GeVo_verwlatung) * 10000
                            grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

                        rowGeb.jahr = long(jahrcount) + long(startjahr)
                        rowGeb.Teilflaeche_Plangebiet = teilflaeche
                        rowGeb.Gebaeudetyp = "Buerogebaeude"
                        rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
                        rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
                        rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
                        rowGeb.Geb_ID = timestamp

                        tabelle_gebaeudedetails_insert.insertRow(rowGeb)

                    ###############################
                    ## Tabelle Gewerbe_teilflaechen fuellen

                    schrittmeldung = 'Projektinformationen werden zusammengefasst und in Datenbank geschrieben \n'
                    messages.AddMessage(schrittmeldung)
                    print str(schrittmeldung)

                    tabelle_teilflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Teilflaechen')
                    tabelle_teilflaeche_insert = arcpy.InsertCursor(tabelle_teilflaeche)
                    rowTF = tabelle_teilflaeche_insert.newRow()

                    # Zeile für Branche C / VerarbGew
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "C"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_VerarbGew)
                    rowTF.anzahlBetriebe = int(Anz_Betr_VerarbGew)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)

                    # Zeile für Branche F / BauGew
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "F"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_BauGew)
                    rowTF.anzahlBetriebe = int(Anz_Betr_BauGew)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)

                    # Zeile für Branche G / HanKfZ
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "G"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_HanKfZ)
                    rowTF.anzahlBetriebe = int(Anz_Betr_HanKfZ)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)

                    # Zeile für Branche H / VerLag
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "H"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_VerLag)
                    rowTF.anzahlBetriebe = int(Anz_Betr_VerLag)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)

                    # Zeile für Branche M / FrWiTeDi
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "M"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_FrWiTeDi)
                    rowTF.anzahlBetriebe = int(Anz_Betr_FrWiTeDi)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)

                    # Zeile für Branche N / SoDi
                    rowTF.teilflaeche = teilflaeche
                    rowTF.gebietstyp = str(gebtyp)
                    rowTF.branche = "N"
                    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                    rowTF.zuzugsquote = long(zuzugsquote)
                    rowTF.nettobauland = float(gewerbebauland)
                    rowTF.bruttoflaeche = float(flaechengroesse)
                    rowTF.beschaeftigte = float(Besch_SoDi)
                    rowTF.anzahlBetriebe = int(Anz_Betr_SoDi)
                    rowTF.timestamp = timestamp

                    tabelle_teilflaeche_insert.insertRow(rowTF)


                    beschaeftigte_gewerbe(projektname)
                    schrittmeldung = 'Die Berechnungen sind abgeschlossen  \n'
                    messages.AddMessage(schrittmeldung)
                    print str(schrittmeldung)










                ##########################################################################
                ##########################################################################
                ##########################################################################
                ##########################################################################
                ##########################################################################
                ## Ergebnisausgabe
                    schrittmeldung = 'Die Ergebnisausgabe wird erzeugt. Dies kann wenige Minuten in Anspruch nehmen. \n'
                    messages.AddMessage(schrittmeldung)
                    print str(schrittmeldung)

                    # Pfade setzen
                    base_path = str(sys.path[0]).split("2_Tool")[0]
                    workspace_projekt_gewerbe = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
                    tablepath_gewerbe = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Teilflaechen')
                    tablepath_Beschaeftigte = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Beschaeftigte')
                    tablepath_Flaechenbilanz = os.path.join(workspace_projekt_gewerbe,'Flaechenbilanz')
                    tablepath_Gebaeude = os.path.join(workspace_projekt_gewerbe,'Gebaeude_Details')
                    tablepath_Betriebe = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Betriebsstruktur')
                    grafikpath_erlauterungstext = os.path.join(base_path,'2_Tool','3_Art und Mass der Nutzung','Erlauterungstexte')

                    logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
                    ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
                    excelpfad = os.path.join(ausgabeordner,'11_Projektdefinition_Gewerbe.xlsx')

                    try:
                        os.remove(excelpfad)
                    except:
                        pass

                    # Workbook und Tabellenblätter anlegen
                    wb = xlsxwriter.Workbook(excelpfad)
                    sl.infosheet(projektname, str("Projektinformation").decode('utf-8'), wb)
                    ws2 = wb.add_worksheet('Erlaeuterungen')
                    ws3 = wb.add_worksheet('Tabellen')
                    ws4 = wb.add_worksheet('Grafiken')
                    ws4_1 = wb.add_worksheet('Art der Arbeitsplaetze')
                    ws5 = wb.add_worksheet('Rohdaten')

                    ##Styles anlegen
                    bold = wb.add_format({'bold': True})
                    bold.set_align('vtop')
                    bold.set_bg_color('white')
                    bold.set_border(0)

                    wrap = wb.add_format()
                    wrap.set_text_wrap()
                    wrap.set_align('vtop')
                    wrap.set_bg_color('white')
                    wrap.set_border(0)

                    normal = wb.add_format()
                    normal.set_bg_color('white')
                    normal.set_border(0)

                    formatDez = wb.add_format()
                    formatDez.set_num_format(0x02)
                    formatDez.set_bg_color('white')
                    formatDez.set_border(0)

                    formatDez1 = wb.add_format()
                    formatDez1.set_num_format(0x01)
                    formatDez1.set_bg_color('white')
                    formatDez1.set_border(0)

                    ###Hintergrund weiss faerben
                    format = wb.add_format()
                    format.set_bg_color('white')
                    format.set_border(0)


                    for x in range(0,200):
                        for y in range(0,200):
                            ws2.write(x,y,"", format)
                            ws3.write(x,y,"", format)
                            ws4.write(x,y,"", format)

                            ws4_1.write(x,y,"", format)

                            ws5.write(x,y,"", format)

                    ###Spaltenbreiten definieren
                    ws2.set_column(0, 0, 86)
                    for x in range(0,200):
                        ws3.set_column(x, 0, 10)
                    ws4.set_column(0, 0, 75)

                    ### ToDo: Für Überschriften im Tabellenblatt noch Zellen zusammenfügen und grau einfärben

                    ########
                    ## Erläuterungstexte einfügen
                    # Pfade zu Grafiken herstellen und einfügen
                    Erlaeuterung = os.path.join(grafikpath_erlauterungstext, 'Gewerbe.png')
                    # ws2.insert_image(0, 0, Erlaeuterung, {'x_scale': 0.32, 'y_scale': 0.32})

                    ###### Tabellenblatt 5: Rohdaten einladen
                    ## Rohdaten tablepath_gewerbe
                    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                    rows = arcpy.SearchCursor(tablepath_gewerbe)
                    #Feldnamen auslesen
                    fieldnames = [f.name for f in arcpy.ListFields(tablepath_gewerbe)]

                    j = 1
                    for row in rows:
                        i = 0
                        for fieldname in fieldnames:
                            try:
                                wert = string(row.getValue(fieldname))
                            except:
                                wert = row.getValue(fieldname)
                            ws5.write(j, i, wert,formatDez)
                            i = i+1

                        j = j+1


                    #Felder als Header in Worksheet einfuegen
                    i = 0
                    for fieldname in fieldnames:
                        column_with = len(fieldname)+2
                        ws5.set_column(i, i, column_with)
                        ws5.write(0, i, fieldname, bold)
                        i = i+1


                    ## Rohdaten tablepath_Beschaeftigte
                    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                    rows = arcpy.SearchCursor(tablepath_Beschaeftigte)
                    #Feldnamen auslesen
                    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Beschaeftigte)]

                    irestart = i + 2

                    j = 1
                    for row in rows:
                        i = irestart
                        for fieldname in fieldnames:
                            try:
                                wert = string(row.getValue(fieldname))
                            except:
                                wert = row.getValue(fieldname)
                            ws5.write(j, i, wert,formatDez)
                            i = i+1

                        j = j+1

                    #Felder als Header in Worksheet einfuegen
                    i = irestart
                    for fieldname in fieldnames:
                        column_with = len(fieldname)+2
                        ws5.set_column(i, i, column_with)
                        ws5.write(0, i, fieldname, bold)
                        i = i+1


                    ## Rohdaten tablepath_Flaechenbilanz
                    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                    rows = arcpy.SearchCursor(tablepath_Flaechenbilanz)
                    #Feldnamen auslesen
                    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Flaechenbilanz)]

                    irestart = i + 2

                    j = 1
                    for row in rows:
                        i = irestart
                        for fieldname in fieldnames:
                            try:
                                wert = string(row.getValue(fieldname))
                            except:
                                wert = row.getValue(fieldname)
                            ws5.write(j, i, wert,formatDez)
                            i = i+1

                        j = j+1

                    #Felder als Header in Worksheet einfuegen
                    i = irestart
                    for fieldname in fieldnames:
                        column_with = len(fieldname)+2
                        ws5.set_column(i, i, column_with)
                        ws5.write(0, i, fieldname, bold)
                        i = i+1


                    ## Rohdaten tablepath_Gebaeude
                    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                    rows = arcpy.SearchCursor(tablepath_Gebaeude)
                    #Feldnamen auslesen
                    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Gebaeude)]

                    irestart = i + 2

                    j = 1
                    for row in rows:
                        i = irestart
                        for fieldname in fieldnames:
                            try:
                                wert = string(row.getValue(fieldname))
                            except:
                                wert = row.getValue(fieldname)
                            ws5.write(j, i, wert,formatDez)
                            i = i+1

                        j = j+1

                    #Felder als Header in Worksheet einfuegen
                    i = irestart
                    for fieldname in fieldnames:
                        column_with = len(fieldname)+2
                        ws5.set_column(i, i, column_with)
                        ws5.write(0, i, fieldname, bold)
                        i = i+1



                    ## Rohdaten tablepath_Betriebe
                    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                    rows = arcpy.SearchCursor(tablepath_Betriebe)
                    #Feldnamen auslesen
                    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Betriebe)]

                    irestart = i + 2

                    j = 1
                    for row in rows:
                        i = irestart
                        for fieldname in fieldnames:
                            try:
                                wert = string(row.getValue(fieldname))
                            except:
                                wert = row.getValue(fieldname)
                            ws5.write(j, i, wert,formatDez)
                            i = i+1

                        j = j+1

                    #Felder als Header in Worksheet einfuegen
                    i = irestart
                    for fieldname in fieldnames:
                        column_with = len(fieldname)+2
                        ws5.set_column(i, i, column_with)
                        ws5.write(0, i, fieldname, bold)
                        i = i+1


                    ###### Tabellenblatt 3: Tabellen erstellen
                    ## Tabelle Projektuebersicht
                    j = 0
                    i = 0
                    ws3.write(j, i, 'Projektuebersicht', bold)
                    j = j + 1
                    ws3.write(j, i, 'Teilflaeche', bold)
                    i = i + 1
                    ws3.write(j, i, 'Gebietstyp', bold)
                    i = i + 1
                    ws3.write(j, i, 'Aufsiedlungsdauer [Jahre]', bold)
                    i = i + 1
                    ws3.write(j, i, 'Zuzugsquote [%]', bold)
                    i = i + 1
                    ws3.write(j, i, 'Nettobauland [Hektar]', bold)
                    i = i + 1
                    ws3.write(j, i, 'Bruttobauland [Hektar]', bold)
                    i = i + 1
                    ws3.write(j, i, 'Beschaeftigte', bold)
                    i = i + 1
                    ws3.write(j, i, 'Betriebe', bold)
                    i = i + 1
                    ws3.write(j, i, 'Branche', bold)
                    j = j + 1
                    i = 0
                    for x in range(2,8):
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                        i = i + 1
                        cell = xl_rowcol_to_cell(j-1,i+1)
                        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                        i = 0
                        j = j + 1

                    ## Tabelle Beschäftigte
                    j = j + 2
                    i = 0
                    ws3.write(j, i, 'Beschaeftigte', bold)
                    j = j + 1
                    ws3.write(j, i, 'Branche', bold)
                    i = i + 1
                    ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
                    for x in range(2, 32):
                        i = i + 1
                        jahrcell = xl_rowcol_to_cell(j,i-1)
                        ws3.write(j, i, '='+jahrcell+'+1', bold)
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'C', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    zeilejahr = j - 1
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'F', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'G', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'H', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'M', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'N', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1


                    ## Tabelle Neue Beschaeftigte
                    j = j + 2
                    i = 0
                    ws3.write(j, i, 'Neue Beschaeftigte', bold)
                    j = j + 1
                    ws3.write(j, i, 'Branche', bold)
                    i = i + 1
                    jahrcellbetrieb = xl_rowcol_to_cell(j,i)
                    ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
                    i = 1
                    for x in range(2, 32):
                        i = i + 1
                        jahrcell = xl_rowcol_to_cell(j,i-1)
                        ws3.write(j, i, '='+jahrcell+'+1', bold)
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'C', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    zeilejahr = j - 1
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'F', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 32):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'G', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'H', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'M', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1
                    i = 1
                    ws3.write(j, 0, 'N', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        spaltejahr = x - 1
                        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                        i = i + 1
                    j = j + 1


                    ## Tabelle Betriebe
                    j = j + 2
                    i = 0
                    ws3.write(j, i, 'Betriebe', bold)
                    j = j + 1
                    ws3.write(j, i, 'Branche', bold)
                    i = i + 1
                    ws3.write(j, i, '='+jahrcellbetrieb+'', bold)
                    i = 1
                    for x in range(2, 32):
                        i = i + 1
                        jahrcell = xl_rowcol_to_cell(j,i-1)
                        ws3.write(j, i, '='+jahrcell+'+1', bold)
                    bracol = xl_col_to_name(46)
                    colcount = 46
                    jahrcol = xl_col_to_name(colcount)
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'C', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'F', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    colcount = 46
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'G', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    colcount = 46
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'H', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    colcount = 46
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'M', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    colcount = 46
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                    ws3.write(j, 0, 'N', normal)
                    zellebranche = xl_rowcol_to_cell(j,0)
                    colcount = 46
                    for x in range(2, 33):
                        colcount = colcount + 1
                        jahrcol = xl_col_to_name(colcount)
                        spaltejahr = x - 1
                        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                        i = i + 1
                    j = j + 1
                    i = 1

                ###### Charts anlegen
                    # Chart Branchenstruktur anlegen
                    chart_Branchenstruktur = wb.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
                    chart_Branchenstruktur.set_style(40)
                    chart_Branchenstruktur.set_size({'width': 529, 'height': 226})
                    chart_Branchenstruktur.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                    chart_Branchenstruktur.set_legend({'position': 'right'})
                    chart_Branchenstruktur.set_title({'name': 'Branchenstruktur','name_font':  {'name': 'Calibri', 'size': 12}})

                    # Werte in Chartobjekte schreiben
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$3:$H$3",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$3",
                    })
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$4:$H$4",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$4",
                    })
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$5:$H$5",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$5",
                    })
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$6:$H$6",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$6",
                    })
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$7:$H$7",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$7",
                    })
                    chart_Branchenstruktur.add_series({
                        'values': "=Tabellen!$G$8:$H$8",
                        'categories': "=Tabellen!$G$2:$H$2",
                        'name': "=Tabellen!$I$8",
                    })

                    # Chart Beschaeftigte anlegen
                    chart_Beschaeftigte = wb.add_chart({'type': 'bar'})
                    chart_Beschaeftigte.set_style(40)
                    chart_Beschaeftigte.set_size({'width': 529, 'height': 283})
                    chart_Beschaeftigte.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                    chart_Beschaeftigte.set_title({'name': 'Beschaeftigte nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
                    chart_Beschaeftigte.set_legend({'none': True})

                    # Werte in Chartobjekte schreiben
                    chart_Beschaeftigte.add_series({
                        'values': "=Tabellen!$G$3:$G$8",
                        'categories': "=Tabellen!$I$3:$I$8",
                    })

                    # Chart Betriebe anlegen
                    chart_Betriebe = wb.add_chart({'type': 'bar'})
                    chart_Betriebe.set_style(40)
                    chart_Betriebe.set_size({'width': 529, 'height': 283})
                    chart_Betriebe.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                    chart_Betriebe.set_title({'name': 'Betriebe nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
                    chart_Betriebe.set_legend({'none': True})

                    # Werte in Chartobjekte schreiben
                    chart_Betriebe.add_series({
                        'values': "=Tabellen!$H$3:$H$8",
                        'categories': "=Tabellen!$I$3:$I$8",
                        'name': "=Tabellen!$I$8",
                    })


                    # Chart Beschaeftigte kum anlegen
                    chart_Besch_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
                    chart_Besch_kum.set_style(40)
                    chart_Besch_kum.set_size({'width': 529, 'height': 283})
                    chart_Besch_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                    chart_Besch_kum.set_legend({'position': 'bottom'})
                    chart_Besch_kum.set_title({'name': 'Beschaeftigte im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

                    # Werte in Chartobjekte schreiben
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$13:$AF$13",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$13",
                    })
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$14:$AF$14",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$14",
                    })
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$15:$AF$15",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$15",
                    })
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$16:$AF$16",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$16",
                    })
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$17:$AF$17",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$17",
                    })
                    chart_Besch_kum.add_series({
                        'values': "=Tabellen!$B$18:$AF$18",
                        'categories': "=Tabellen!$B$12:$AF$12",
                        'name': "=Tabellen!$A$18",
                    })




                    # Chart Betriebe kum anlegen
                    chart_Betriebe_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
                    chart_Betriebe_kum.set_style(40)
                    chart_Betriebe_kum.set_size({'width': 529, 'height': 283})
                    chart_Betriebe_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                    chart_Betriebe_kum.set_legend({'position': 'bottom'})
                    chart_Betriebe_kum.set_title({'name': 'Betriebe im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

                    # Werte in Chartobjekte schreiben
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$33:$AF$33",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$33",
                    })
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$34:$AF$34",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$34",
                    })
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$35:$AF$35",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$35",
                    })
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$36:$AF$36",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$36",
                    })
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$37:$AF$37",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$37",
                    })
                    chart_Betriebe_kum.add_series({
                        'values': "=Tabellen!$B$38:$AF$38",
                        'categories': "=Tabellen!$B$32:$AF$32",
                        'name': "=Tabellen!$A$38",
                    })



                    # Charts in Tabelle schreiben
                    ws4.insert_chart('A2', chart_Branchenstruktur)
                    ws4.insert_chart('A14', chart_Beschaeftigte)
                    ws4.insert_chart('A29', chart_Betriebe)
                    ws4.insert_chart('A44', chart_Besch_kum)
                    ws4.insert_chart('A59', chart_Betriebe_kum)

                    ######
                    #Gewerbe Beschaeftigte Art der beschaeftigung
                    if arcpy.Exists(os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb',"Gewerbe_Beschaeftigte_Zahlen")):
                        path_beschaeftigte_Zahlen= os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb',"Gewerbe_Beschaeftigte_Zahlen")
                        datenauslesen=[]
                        for uu in arcpy.SearchCursor(path_beschaeftigte_Zahlen):
                            datenauslesen.append(uu.Anzahl)

                        if len(datenauslesen)==4:
                            #Alles okay mit den Daten - eigentlich quatsch aber absicherung

                            ws4_1.write(2, 1, "Art der Arbeitsplaetze".decode('utf-8'), bold)
                            ws4_1.write(4, 1, "Von den   "+str(datenauslesen[3])+"   Arbeitsplaetzen, die durch die Gewerbeansiedlung entstehen werden, sind vermutlich".decode('utf-8'))
                            ws4_1.write(5, 1, str(datenauslesen[0])+"   Arbeitsplaetze fuer Teilzeitbeschaeftigte,")
                            ws4_1.write(6, 1, str(datenauslesen[1])+"   Arbeitsplaetze fuer geringfuegig entlohnte Beschaeftigte (Minijobber) und")
                            ws4_1.write(7, 1, str(datenauslesen[2])+"   Arbeitsplaetze fuer Beschaeftigte mit einer akademischen Ausbildung (d.h. mit Fach- oder Hochschulabschluss).")

                            del path_beschaeftigte_Zahlen, datenauslesen


                    #Workbook speichern
                    try:
                        wb.close()
                    except:
                        messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

                    schrittmeldung = 'Die Ergebnisausgabe wurde erzeugt. Das Tool wurde erfolgreich angewendet.  \n'
                    messages.AddMessage(schrittmeldung)



            #EINZELHANDEL
            projectname = parameters[0].valueAsText
            tabelle_gebaude = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Gebaeude_Details')
            Insert = arcpy.InsertCursor(tabelle_gebaude)
            row = Insert.newRow()
            row.Teilflaeche_Plangebiet = parameters[1].valueAsText
            row.Gebaeudetyp = "Einzelhandel"
            Insert.insertRow(row)
            del row, Insert

            #tabelle "Wohneinheiten_Details" oeffnen und Werte fuer Miete_Eigentum, Qualitastsstufe und Anzahl Wohneinheiten speichern
            tabelle_wohneineheiten_details = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Wohneinheiten_Details')
            Insert = arcpy.InsertCursor(tabelle_wohneineheiten_details)
            row = Insert.newRow()
            row.Gebaeudetyp = "Einzelhandel"
            row.Wohnflaeche_qm = 0
            row.Teilflaeche_Plangebiet = parameters[1].valueAsText
            row.Miete_Eigentum = 100
            row.Anzahl_WE = 0
            row.Jahr = jahr
            row.EW_je_WE = 0
            Insert.insertRow(row)
            del row, Insert

            #tabelle "Versorgung_Verkaufsflaechen" oeffnen und Werte  speichern
            tabelle_Versorgung_Verkaufsflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Versorgung_Verkaufsflaechen')
            Insert = arcpy.InsertCursor(tabelle_Versorgung_Verkaufsflaechen)
            row = Insert.newRow()
            row.Teilflaeche_Plangebiet = parameters[1].valueAsText
            row.Verkaufsflaeche = parameters[26].valueAsText
            Insert.insertRow(row)
            del row, Insert
