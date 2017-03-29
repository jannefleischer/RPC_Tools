# -*- coding: utf-8 -*-

import sys

from os.path import abspath, dirname, join
import numpy as np
import arcpy
import datetime

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode


from rpctools.definitions.nutzungsart.nutzungen import Nutzungen

class TbxNutzungen(Tbx):

    @property
    def label(self):
        return 'Schritt 4: Nutzungen eingeben'

    @property
    def Tool(self):
        return Nutzungen

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        projekte = self.folders.get_projects()

        param = params.projectname = arcpy.Parameter()
        param.name = u'Projekt'
        param.displayName = u'Projekt'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = projekte
        if projekte:
            param.value = projekte[0]

        # Teilfläche
        param = params.teilflaeche = arcpy.Parameter()
        param.name = u'Teilfl\xe4che'
        param.displayName = u'Teilfl\xe4che'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = []

        heading = "1) Aufsiedlungszeitraum"
        # Beginn_der_Aufsiedlung__Jahreszahl_
        param_3 = params.beginn_aufsiedlung = arcpy.Parameter()
        param_3.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param_3.displayName = u'Beginn der Aufsiedlung (Jahreszahl)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Long'
        param_3.filter.type = 'Range'
        param_3.filter.list = [2010, 2050]
        param_3.category = heading
        param_3.value = datetime.datetime.now().year + 1

        # Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_
        param_4 = params.dauer_aufsiedlung = arcpy.Parameter()
        param_4.name = u'Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_'
        param_4.displayName = u'Dauer der Aufsiedlung (Jahre, 1 = Aufsiedlung wird noch im Jahr des Aufsiedlungsbeginns abgeschlossen)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = 5
        param_4.filter.type = 'Range'
        param_4.filter.list = [1, 20]
        param_4.category = heading


        heading = encode(u"2) Wohnen - Anzahl Wohneinheiten nach Gebäudetypen")

        # Anzahl_WE_in_Ein-_und_Zweifamilienhäusern
        param_5 = params.we_efh = arcpy.Parameter()
        param_5.name = u'Anzahl_WE_in_Einfamilienh\xe4usern'
        param_5.displayName = u'Anzahl WE in Einfamilienh\xe4usern'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'0'
        param_5.filter.type = 'Range'
        param_5.filter.list = [0, 500]
        param_5.category = heading

        # Anzahl_WE_in_Doppelhäusern
        param_6 = params.we_zfh = arcpy.Parameter()
        param_6.name = u'Anzahl_WE_in_Doppelh\xe4usern'
        param_6.displayName = u'Anzahl WE in Doppelh\xe4usern'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Long'
        param_6.value = u'0'
        param_6.filter.type = 'Range'
        param_6.filter.list = [0, 500]
        param_6.category = heading

        # Anzahl_WE_in_Reihenhäusern
        param_7 = params.we_rh = arcpy.Parameter()
        param_7.name = u'Anzahl_WE_in_Reihenh\xe4usern'
        param_7.displayName = u'Anzahl WE in Reihenh\xe4usern'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'Long'
        param_7.value = u'0'
        param_7.filter.type = 'Range'
        param_7.filter.list = [0, 500]
        param_7.category = heading

        # Anzahl_WE_in_Mehrfamilienhäusern
        param_8 = params.we_mfh = arcpy.Parameter()
        param_8.name = u'Anzahl_WE_in_Mehrfamilienh\xe4usern'
        param_8.displayName = u'Anzahl WE in Mehrfamilienh\xe4usern'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Long'
        param_8.value = u'0'
        param_8.filter.type = 'Range'
        param_8.filter.list = [0, 500]
        param_8.category = heading


        heading = "3) Wohnen - Anteile Eigentum und Miete"

        # Anteil_Eigentümernutzung_in_Ein-_und_Zweifamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_9 = params.ant_eigentum_efh = arcpy.Parameter()
        param_9.name = u'Anteil_Eigent\xfcmernutzung_in_Einfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_9.displayName = u'Anteil Eigent\xfcmernutzung in Einfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_9.parameterType = 'Required'
        param_9.direction = 'Input'
        param_9.datatype = u'Long'
        param_9.value = u'90'
        param_9.filter.type = 'Range'
        param_9.filter.list = [0, 100]
        param_9.category = heading

        # Anteil_Eigentümernutzung_in_Doppelhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_10 = params.ant_eigentum_zfh = arcpy.Parameter()
        param_10.name = u'Anteil_Eigent\xfcmernutzung_in_Doppelh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_10.displayName = u'Anteil Eigent\xfcmernutzung in Doppelh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_10.parameterType = 'Required'
        param_10.direction = 'Input'
        param_10.datatype = u'Long'
        param_10.value = u'80'
        param_10.filter.type = 'Range'
        param_10.filter.list = [0, 100]
        param_10.category = heading

        # Anteil_Eigentümernutzung_in_Reihenhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_11 = params.ant_eigentum_rh = arcpy.Parameter()
        param_11.name = u'Anteil_Eigent\xfcmernutzung_in_Reihenh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_11.displayName = u'Anteil Eigent\xfcmernutzung in Reihenh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_11.parameterType = 'Required'
        param_11.direction = 'Input'
        param_11.datatype = u'Long'
        param_11.value = u'70'
        param_11.filter.type = 'Range'
        param_11.filter.list = [0, 100]
        param_11.category = heading

        # Anteil_Eigentümernutzung_in_Mehrfamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param_12 = params.ant_eigentum_mfh = arcpy.Parameter()
        param_12.name = u'Anteil_Eigent\xfcmernutzung_in_Mehrfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param_12.displayName = u'Anteil Eigent\xfcmernutzung in Mehrfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param_12.parameterType = 'Required'
        param_12.direction = 'Input'
        param_12.datatype = u'Long'
        param_12.value = u'20'
        param_12.filter.type = 'Range'
        param_12.filter.list = [0, 100]
        param_12.category = heading


        heading = "4) Wohnen - Einwohner pro Wohneinheit"

        list_EwProWE = []
        for i in range(1,5):
            for j in range(0,10):
                list_EwProWE.append(str(i)+","+str(j)+" Bewohner pro Wohneinheit")

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienhäusern__kurz_nach_dem_Bezug_
        param_13 = params.ew_je_we_efh = arcpy.Parameter()
        param_13.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_13.displayName = u'Mittlere Anzahl Einwohner pro WE in Einfamilienh\xe4usern (kurz nach dem Bezug)'
        param_13.parameterType = 'Required'
        param_13.direction = 'Input'
        param_13.datatype = u'GPString'

        param_13.value = u'3,2 Bewohner pro Wohneinheit'
        param_13.filter.list = list_EwProWE
        param_13.category = heading

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelhäusern__kurz_nach_dem_Bezug_
        param_14 = params.ew_je_we_zfh = arcpy.Parameter()
        param_14.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelh\xe4usern__kurz_nach_dem_Bezug_'
        param_14.displayName = u'Mittlere Anzahl Einwohner pro WE in Doppelh\xe4usern (kurz nach dem Bezug)'
        param_14.parameterType = 'Required'
        param_14.direction = 'Input'
        param_14.datatype = u'GPString'

        param_14.value = u'3,0 Bewohner pro Wohneinheit'
        param_14.filter.list = list_EwProWE
        param_14.category = heading

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenhäusern__kurz_nach_dem_Bezug_
        param_15 = params.ew_je_we_rh = arcpy.Parameter()
        param_15.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenh\xe4usern__kurz_nach_dem_Bezug_'
        param_15.displayName = u'Mittlere Anzahl Einwohner pro WE in Reihenh\xe4usern (kurz nach dem Bezug)'
        param_15.parameterType = 'Required'
        param_15.direction = 'Input'
        param_15.datatype = u'GPString'

        param_15.value = u'3,0 Bewohner pro Wohneinheit'
        param_15.filter.list = list_EwProWE
        param_15.category = heading

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienhäusern__kurz_nach_dem_Bezug_
        param_16 = params.ew_je_we_mfh = arcpy.Parameter()
        param_16.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param_16.displayName = u'Mittlere Anzahl Einwohner pro WE in Mehrfamilienh\xe4usern (kurz nach dem Bezug)'
        param_16.parameterType = 'Required'
        param_16.direction = 'Input'
        param_16.datatype = u'GPString'

        param_16.value = u'2,1 Bewohner pro Wohneinheit'
        param_16.filter.list = list_EwProWE
        param_16.category = heading


        heading = "5) Wohnen - Zuzugsquote"

        # Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_
        param_17 = params.zuzugsquote_ew = arcpy.Parameter()
        param_17.name = u'Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_'
        param_17.displayName = u'Wie viel Prozent der Bewohner der neuen Wohnungen werden neu in die Gemeinde ziehen?'
        param_17.parameterType = 'Required'
        param_17.direction = 'Input'
        param_17.datatype = u'Long'
        param_17.value = u'80'
        param_17.filter.type = 'Range'
        param_17.filter.list = [0, 100]
        param_17.category = heading


        heading = "6) Gewerbe - Gebietstyp und Brachenstruktur"

        # Gebietstyp_auswählen
        param_18 = params.gebietstyp = arcpy.Parameter()
        param_18.name = u'Gebietstyp_ausw\xe4hlen'
        param_18.displayName = u'Gebietstyp ausw\xe4hlen'
        param_18.parameterType = 'Required'
        param_18.direction = 'Input'
        param_18.datatype = u'GPString'

        param_18.value = u'<kein Gewerbegebiet vorhanden>'
        param_18.filter.list = [u'Industriegebiet', u'Logistikgebiet', u'Klassisches Gewerbegebiet', u'Kleinteiliges Gewerbegebiet', u'Hoeherwertiges Gewerbegebiet', u'Technologiepark, Wissenschaftspark', u'<kein Gewerbegebiet vorhanden>']
        param_18.category = heading

        # Anteil_der_Arbeitsplätze_im_verarbeitenden_Gewerbe__in_Prozent_
        param_19 = params.ant_jobs_verarb_gewerbe = arcpy.Parameter()
        param_19.name = u'Anteil_der_Arbeitspl\xe4tze_im_verarbeitenden_Gewerbe__in_Prozent_'
        param_19.displayName = u'Anteil der Arbeitspl\xe4tze im verarbeitenden Gewerbe (in Prozent)'
        param_19.parameterType = 'Required'
        param_19.direction = 'Input'
        param_19.datatype = u'Long'
        param_19.value = u'40'
        param_19.filter.type = 'Range'
        param_19.filter.list = [0, 100]
        param_19.category = heading

        # Anteil_der_Arbeitsplätze_im_Baugewerbe__in_Prozent_
        param_20 = params.ant_jobs_baugewerbe = arcpy.Parameter()
        param_20.name = u'Anteil_der_Arbeitspl\xe4tze_im_Baugewerbe__in_Prozent_'
        param_20.displayName = u'Anteil der Arbeitspl\xe4tze im Baugewerbe (in Prozent)'
        param_20.parameterType = 'Required'
        param_20.direction = 'Input'
        param_20.datatype = u'Long'
        param_20.value = u'6'
        param_20.filter.type = 'Range'
        param_20.filter.list = [0, 100]
        param_20.category = heading

        # Anteil_der_Arbeitsplätze_im_Handel__inkl__Kfz___in_Prozent_
        param_21 = params.ant_jobs_handel = arcpy.Parameter()
        param_21.name = u'Anteil_der_Arbeitspl\xe4tze_im_Handel__inkl__Kfz___in_Prozent_'
        param_21.displayName = u'Anteil der Arbeitspl\xe4tze im Handel (inkl. Kfz) (in Prozent)'
        param_21.parameterType = 'Required'
        param_21.direction = 'Input'
        param_21.datatype = u'Long'
        param_21.value = u'17'
        param_21.filter.type = 'Range'
        param_21.filter.list = [0, 100]
        param_21.category = heading

        # Anteil_der_Arbeitsplätze_im_Verkehrs-_und_Lagereibereich___in_Prozent_
        param_22 = params.ant_jobs_logistik = arcpy.Parameter()
        param_22.name = u'Anteil_der_Arbeitspl\xe4tze_im_Verkehrs-_und_Lagereibereich___in_Prozent_'
        param_22.displayName = u'Anteil der Arbeitspl\xe4tze im Verkehrs- und Lagereibereich  (in Prozent)'
        param_22.parameterType = 'Required'
        param_22.direction = 'Input'
        param_22.datatype = u'Long'
        param_22.value = u'10'
        param_22.filter.type = 'Range'
        param_22.filter.list = [0, 100]
        param_22.category = heading

        # Anteil_der_Arbeitsplätze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_
        param_23 = params.ant_jobs_freiwisstech = arcpy.Parameter()
        param_23.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_'
        param_23.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich der freiberuflichen, wissenschaftl. bzw. techn. Dienstleistungen (in Prozent)'
        param_23.parameterType = 'Required'
        param_23.direction = 'Input'
        param_23.datatype = u'Long'
        param_23.value = u'14'
        param_23.filter.type = 'Range'
        param_23.filter.list = [0, 100]
        param_23.category = heading

        # Anteil_der_Arbeitsplätze_im_Bereich_sonstiger_Diensteistungen
        param_24 = params.ant_jobs_sonst_dl = arcpy.Parameter()
        param_24.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_sonstiger_Diensteistungen'
        param_24.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich sonstiger Diensteistungen'
        param_24.parameterType = 'Required'
        param_24.direction = 'Input'
        param_24.datatype = u'Long'
        param_24.value = u'13'
        param_24.filter.type = 'Range'
        param_24.filter.list = [0, 100]
        param_24.category = heading


        heading = "7) Gewerbe - Zuzugs- und Eigentumsquote"

        # Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_
        param_25 = params.zuzugsquote_gewerbe = arcpy.Parameter()
        param_25.name = u'Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_'
        param_25.displayName = u'Wie viel Prozent der Unternehmen werden neu in die Gemeinde ziehen?'
        param_25.parameterType = 'Required'
        param_25.direction = 'Input'
        param_25.datatype = u'Long'
        param_25.value = u'80'
        param_25.filter.type = 'Range'
        param_25.filter.list = [0, 100]
        param_25.category = heading

        # Welcher_Anteil_der_Gebäude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_
        param_26 = params.ant_eigentum_gewerbe = arcpy.Parameter()
        param_26.name = encode(u'Welcher_Anteil_der_Geb\xe4ude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_')
        param_26.displayName = encode(u'Welcher Anteil der Geb\xe4ude ist voraussichtlich im Eigentum der Unternehmen?')
        param_26.parameterType = 'Required'
        param_26.direction = 'Input'
        param_26.datatype = u'Long'
        param_26.value = u'100'
        param_26.filter.type = 'Range'
        param_26.filter.list = [0, 100]
        param_26.category = heading

        heading = "8) Einzelhandel (nur Lebensmitteleinzelhandel)"

        # Verkaufsfläche__in_Quadratmetern_
        param_27 = params.verkaufsflaeche = arcpy.Parameter()
        param_27.name = encode(u'Verkaufsfl\xe4che__in_Quadratmetern_')
        param_27.displayName = encode(u'Verkaufsfl\xe4che (in Quadratmetern)')
        param_27.parameterType = 'Required'
        param_27.direction = 'Input'
        param_27.datatype = u'Long'
        param_27.value = u'0'
        param_27.filter.type = 'Range'
        param_27.filter.list = [0, 20000]
        param_27.category = heading

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        projects = self.folders.get_projects()
        params.project.filter.list = projects
        if len(projects) == 0:
            params.project.value = ''
        # if previously selected project was deleted in the meantime
        elif params.project.value not in projects:
            params.project.value = projects[0]

        def eingaben_auslesen():

            projectname = self.par.projectname.value
            teilflaeche = self.par.teilflaeche.value

            tablepath_flaechenbilanz = self.folders.get_table('Wohneinheiten_Details')
            tabelle_gebaude = self.folders.get_table('Gebaeude_Details')
            tabelle_Versorgung_Verkaufsflaechen = self.folders.get_table('Versorgung_Verkaufsflaechen')
            flaechenbilanz = self.folders.get_table('Flaechenbilanz')
            plangebiet = self.folders.get_table('Teilflaechen_Plangebiet')
            tabelle_gewerbeanteile = self.folders.get_table('Gewerbe_Anteile')

            #Startjahr und Aufsiedlungsdauer
            fields = ['Beginn_Nutzung', 'Aufsiedlungsdauer', 'Name', 'Startjahr']
            rows = arcpy.da.SearchCursor(plangebiet,fields)
            for row in rows:
                if row[2] == teilflaeche:
                    self.par[3].value = row[1]
                    if row[0] != None:
                        self.par[2].value = row[0]
                    else:
                        self.par[2].value = row[3]

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

            self.par[4].value = efh
            self.par[5].value = zfh
            self.par[6].value = rh
            self.par[7].value = mfh

            #Wohnen - Anteile Eigentum und Miete
            fields = ['Gebaeudetyp', 'Ant_Eigentuemer', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    self.par[8].value = row[1]
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    self.par[9].value = row[1]
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    self.par[10].value = row[1]
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    self.par[11].value = row[1]

            #Wohnen - Einwohner pro Wohneinheit
            fields = ['Gebaeudetyp', 'EW_je_WE', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    self.par[12].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    self.par[13].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    self.par[14].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    self.par[15].value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"

            #Gewerbe
            rows = arcpy.da.SearchCursor(tabelle_gewerbeanteile, ["teilflaeche", "branche", "Anteil_A", "Anteil_B" , "Anteil_C" , "Anteil_D" , "Anteil_E", "Anteil_F", "Anteil_Zuzug", "Anteil_Eigentum"])
            for row in rows:
                if row[0] == teilflaeche:
                    self.par[17].value = row[1]
                    self.par[18].value = row[2]
                    self.par[19].value = row[3]
                    self.par[20].value = row[4]
                    self.par[21].value = row[5]
                    self.par[22].value = row[6]
                    self.par[23].value = row[7]
                    self.par[24].value = row[8]
                    self.par[25].value = row[9]


            #Einzelhandel (nur Lebensmitteleinzelhandel)
            fields = ['Verkaufsflaeche', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tabelle_Versorgung_Verkaufsflaechen,fields)
            for row in rows:
                if row[1] == teilflaeche:
                    self.par[26].value = row[0]

            return


    # Gebietstyp auswählen
        i=17
        if self.par[i].altered and not self.par[i].hasBeenValidated:
            gebtyp = self.par[i].value
            tablepath_gebietstyp = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebietstypen')
            self.folders.get_base_table
            rows = arcpy.SearchCursor(tablepath_gebietstyp)

            for row in rows:
                if gebtyp == row.Gebietstyp:
                    self.par[i+1].value = row.Ant_VerarbGew
                    self.par[i+2].value = row.Ant_BauGew
                    self.par[i+3].value = row.Ant_HanKfZ
                    self.par[i+4].value = row.Ant_VerLag
                    self.par[i+5].value = row.Ant_FrWiTeDi
                    self.par[i+6].value = row.Ant_SoDi

    # Automatische Anpassung der Slider
        def sliderSummenKontrolle(listeSliderID, zielwertSlidersumme):
            istsumme = 0
            for s in listeSliderID:
                istsumme+=self.par[s].value

            if istsumme <> zielwertSlidersumme:
                abweichung = zielwertSlidersumme - istsumme
                for s in reversed(listeSliderID):
                    alterWert = self.par[s].value
                    neuerWert = self.par[s].value + abweichung
                    if neuerWert < 0:
                        neuerWert = 0
                    elif neuerWert > zielwertSlidersumme:
                        neuerWert = zielwertSlidersumme
                    abweichung = abweichung + alterWert - neuerWert
                    self.par[s].value = neuerWert
            return

        # Auswahl Teilfläche
        i = 0
        if self.par[i].altered and not self.par[i].hasBeenValidated:
            projectname = self.par[i].value

            tablepath_teilflaechen = self.folders.get_table('Teilflaechen_Plangebiet')
            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen :
                list_teilflaechen.append(row.Name)
            list_teilflaechen = sorted(set(list_teilflaechen))
            i+=1 ; self.par[i].filter.list = list_teilflaechen

            if len(list_teilflaechen) == 1:
                self.par[i].value = list_teilflaechen[0]
                eingaben_auslesen()


        # bestehende Eingaben (falls vorhanden) übernehmen
        i = 1
        if self.par[i].altered and not self.par[i].hasBeenValidated:
            eingaben_auslesen()


        # Slider für Anteile an Arbeitsplätzen nach Gewerbetyp generieren
        listeSliderID = [18, 19, 20, 21,22, 23]
        zielwertSlidersumme = 100

        for r in listeSliderID:
            if self.par[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        return
