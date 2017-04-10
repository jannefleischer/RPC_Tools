# -*- coding: utf-8 -*-

import sys

from os.path import abspath, dirname, join
import numpy as np
import arcpy
import datetime

from rpctools.utils.params import Tbx
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.definitions.nutzungsart.nutzungen import Nutzungen
from rpctools.utils.encoding import encode


class TbxNutzungen(TbxFlaechendefinition):
    _label = u'Schritt 3{sub}: Nutzungen - {name} definieren'
    _nutzungsart = Nutzungsart.UNDEFINIERT

    @property
    def label(self):
        return self._label

    def init_aufsiedlung(self, params, heading='', beginn_name=''):
        """WORKAROUND: add the aufsiedlungs parameters outside of
        _getParameterInfo, strangely the subclasses of TbxNutzungen are
        not recognized as subclasses (so you can't call _getParameterInfo
        of TbxFlaechendefinition here"""


        # Beginn der Aufsiedlung (Jahreszahl)
        param = params.bezugsbeginn = arcpy.Parameter()
        param.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param.displayName = beginn_name or encode(u'Beginn der Aufsiedlung '
                                                  u'(Jahreszahl)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.filter.type = 'Range'
        param.filter.list = [2010, 2050]
        param.value = 2018
        param.category = heading

        param.value = datetime.datetime.now().year + 1

        # Dauer des Bezugs (Jahre, 1 = Bezug wird noch im Jahr des
        # Bezugsbeginns abgeschlossen)
        param = params.dauer_aufsiedlung = arcpy.Parameter()
        param.name = u'dauer_aufsiedlung'
        param.displayName = (u'Dauer des Bezugs (Jahre, 1 = Bezug wird noch '
                             u'im Jahr des Bezugsbeginns abgeschlossen)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 5
        param.filter.type = 'Range'
        param.filter.list = [1, 20]
        param.category = heading

        return params

    def _updateParameters(self, params):
        if params.changed('projectname'):
            params.teilflaeche.value = ''
            self.update_teilflaechen_list(self._nutzungsart)
        return params


class TbxNutzungenWohnen(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='a', name='Wohnen')
    _nutzungsart = Nutzungsart.WOHNEN

    @property
    def Tool(self):
        return Nutzungen

    def _getParameterInfo(self):
        params = super(TbxNutzungenWohnen, self)._getParameterInfo()
        # workaround
        heading = "1) Bezugszeitraum"
        beginn_name="Beginn des Bezugs (Jahreszahl)"
        params = self.init_aufsiedlung(params, heading=heading,
                                       beginn_name=beginn_name)

        # specific parameters for "Wohnen"

        heading = encode(u"2) Anzahl Wohneinheiten nach Gebäudetypen")

        # Anzahl WE in Einfamilienhäusern
        param = params.we_efh = arcpy.Parameter()
        param.name = encode(u'Bewohner Einfamilienhaus')
        param.displayName = encode(u'Anzahl WE in Einfamilienhäusern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]
        param.category = heading

        # Anzahl WE in Doppelhäusern
        param = params.we_zfh = arcpy.Parameter()
        param.name = encode(u'Bewohner Doppelhaus')
        param.displayName = encode(u'Anzahl WE in Doppelhäusern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]

        param.category = heading

        # Anzahl WE in Reihenhäusern
        param = params.we_rh = arcpy.Parameter()
        param.name = encode(u'Bewohner Reihenhaus')
        param.displayName = encode(u'Anzahl WE in Reihenhäusern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]

        param.category = heading

        # Anzahl WE in Mehrfamilienhäusern
        param = params.we_mfh = arcpy.Parameter()
        param.name = encode(u'Bewohner Mehrfamilienhaus')
        param.displayName = encode(u'Anzahl WE in Mehrfamilienhäusern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]
        param.category = heading

        heading = "3) Einwohner pro Wohneinheit"

        list_EwProWE = []
        for i in range(1,5):
            for j in range(0,10):
                list_EwProWE.append(str(i)+","+str(j)+
                                    " Bewohner pro Wohneinheit")

        # Mittlere Anzahl Einwohner pro WE in Einfamilienhäusern
        # (kurz nach dem Bezug)
        param = params.ew_je_we_efh = arcpy.Parameter()
        param.name = u'Bewohner Einfamilienhaus kndB'
        param.displayName = encode(u'Mittlere Anzahl Einwohner pro WE in '
                                   u'Einfamilienhäusern (kurz nach dem Bezug)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,2 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading

        # Mittlere Anzahl Einwohner pro WE in Doppelhäusern
        # (kurz nach dem Bezug)
        param = params.ew_je_we_zfh = arcpy.Parameter()
        param.name = u'Bewohner Doppelhäuser kndB'
        param.displayName = encode(u'Mittlere Anzahl Einwohner pro WE in '
                                   u'Doppelhäusern (kurz nach dem Bezug)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,0 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading

        # Mittlere Anzahl Einwohner pro WE in Reihenhäusern
        # (kurz nach dem Bezug)
        param = params.ew_je_we_rh = arcpy.Parameter()
        param.name = u'Bewohner Reihenhaus kndB'
        param.displayName = encode(u'Mittlere Anzahl Einwohner pro WE in '
                                   u'Reihenhäusern (kurz nach dem Bezug)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,0 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading

        # Mittlere Anzahl Einwohner pro WE in Mehrfamilienhäusern kurz nach
        # dem Bezug
        param = params.ew_je_we_mfh = arcpy.Parameter()
        param.name = u'Bewohner Mehrfamilienhaus kndB'
        param.displayName = encode(u'Mittlere Anzahl Einwohner pro WE in '
                                   u'Mehrfamilienhäusern '
                                   u'(kurz nach dem Bezug)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'2,1 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading

        return params

    def _updateParameters(self, params):
        params = super(TbxNutzungenWohnen, self)._updateParameters(params)
        return params

    def _updateMessages(self, params):
        pass


class TbxNutzungenGewerbe(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='b', name='Gewerbe')
    _nutzungsart = Nutzungsart.GEWERBE

    @property
    def Tool(self):
        return Nutzungen

    def _getParameterInfo(self):
        params = super(TbxNutzungenGewerbe, self)._getParameterInfo()

        # workaround
        heading = "1) Bezugszeitraum"
        params = self.init_aufsiedlung(params, heading=heading)

        heading = u"2) Voraussichtlicher Anteil der Branchen an der Nettofläche"

        # Gebietstyp auswählen
        param = params.gebietstyp = arcpy.Parameter()
        param.name = u'Gebietstyp'
        param.displayName = encode(u'Gebietstyp auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
          
        table = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb', 
                                            'Gewerbegebietstypen')
        types = [u'<benutzerdefiniert>']
        #try:
        columns = ['Name_Gewerbegebietstyp']
        cursor = arcpy.da.SearchCursor(table, columns)
        for r in cursor: 
            types.append(r[0])
        #except:
            ## warning handled in toolbox class
            #pass
        param.filter.list = types
        param.value = types[0]
        param.category = heading
    
        dependent_params = []

        # Anteil der Arbeitsplätze im verarbeitenden Gewerbe in Prozent
        name = 'ant_jobs_verarb_gewerbe'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'verarbeitendes Gewerbe'
        param.displayName = encode(u'Verarbeitendes Gewerbe (in % der '
                                   u'Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 40
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading        

        # Anteil der Arbeitsplätze im Baugewerbe in Prozent
        name = 'ant_jobs_baugewerbe'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'Baugewerbe'
        param.displayName = encode(u'Baugewerbe (in % der Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 10
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        # Anteil der Arbeitsplätze im Handel inkl. Kfz in Prozent
        name = 'ant_jobs_handel'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'Handel'
        param.displayName = encode(u'Großhandel, Logistik, Kfz-Handel '
                                   u'(in % der Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 5
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        # Anteil der Arbeitsplätze im Bereich der freiberuflichen wissenschaftl
        # bzw. techn. Dienstleistungen in Prozent
        name = 'ant_jobs_freiwisstech'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'Finanzen'
        param.displayName = encode(u'Finanzen, Versicherungen, IuK, '
                                   u'wissensorientierte Dienstleistungen '
                                   u'(in % der Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 25
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        # Anteil der Arbeitsplätze im Bereich sonstiger Diensteistungen
        name = 'ant_jobs_sonst_dl'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'Sonstige'
        param.displayName = encode(u'Sonstige unternehmensorientierte '
                                   u'Dienstleistungen (in % der Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 10
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading

        # Öffentliche Verwaltung
        name = 'ant_oev'
        dependent_params.append(name)
        param = params[name] = arcpy.Parameter()
        param.name = u'Öffentliche Verwaltung'
        param.displayName = encode(u'Öffentliche Verwaltung '
                                   u'(in % der Nettofläche)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 10
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        
        dependent_params = ['ant_jobs_verarb_gewerbe', 
                            'ant_jobs_baugewerbe', 
                            'ant_jobs_handel', 
                            'ant_jobs_freiwisstech', 
                            'ant_jobs_sonst_dl', 
                            'ant_oev']
        
        self.add_sum_dependency(dependent_params, 100)

        heading = u'3) Voraussichtliche Anzahl an Arbeitsplätzen'

        # Arbeitsplatzzahl schätzen
        param = params.auto_select = arcpy.Parameter()
        param.name = u'Arbeitsplatzzahl schätzen'
        param.displayName = encode(u'Vorgehen zur Schätzung der Zahl der '
                                   u'Arbeitsplätze nach Vollbezug')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = [u'Arbeitsplatzzahl automatisch schätzen',
                             u'Eigenen Wert eingeben']
        param.value = param.filter.list[0]
        param.category = heading

        # Arbeitsplätze insgesamt
        param = params.arbeitsplaetze_insgesamt = arcpy.Parameter()
        param.name = u'Arbeitsplätze insgesamt'
        param.displayName = encode(u'Schätzung der Zahl der Arbeitsplätze '
                                   u'nach Vollbezug (Summe über alle '
                                   u'Branchen)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.category = heading

        return params

    def _updateParameters(self, params):
        params = super(TbxNutzungenGewerbe, self)._updateParameters(params)

        #idx = auto_select.filter.list.index(auto_select.value)
        #if idx == 0:
        return params

    def _updateMessages(self, params):
        pass


class TbxNutzungenEinzelhandel(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='c', name='Einzelhandel')
    _nutzungsart = Nutzungsart.EINZELHANDEL

    @property
    def Tool(self):
        return Nutzungen

    def _getParameterInfo(self):
        params = super(TbxNutzungenEinzelhandel, self)._getParameterInfo()
        # workaround
        heading = '1) Voraussichtliche Eröffnung '
        params = self.init_aufsiedlung(params, heading=heading)

        heading = u'2) Verkaufsflächen'

        # Lebensmittel (Verkaufsfläche in qm)
        param = params.lebensmittel = arcpy.Parameter()
        param.name = u'Lebensmittel'
        param.displayName = encode(u'Lebensmittel (Verkaufsfläche in qm)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 1200
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.category = heading

        # Sonstiger periodischer Bedarf (Verkaufsfläche in qm)
        param = params.periodischer_bedarf = arcpy.Parameter()
        param.name = u'periodische Bedarf'
        param.displayName = encode(u'Sonstiger periodischer Bedarf '
                                   u'(Verkaufsfläche in qm)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 1200
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.category = heading

        # Aperiodischer Bedarf ohne Baumarkt und Möbel (Verkaufsfläche in qm)
        param = params.aperiodischer_bedarf = arcpy.Parameter()
        param.name = u'aperiodische Bedarf'
        param.displayName = encode(u'Aperiodischer Bedarf ohne Baumarkt und '
                                   u'Möbel (Verkaufsfläche in qm)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 1200
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.category = heading

        # Baumarkt (Verkaufsfläche in qm)
        param = params.baumarkt = arcpy.Parameter()
        param.name = u'Baumarkt'
        param.displayName = encode(u'Baumarkt (Verkaufsfläche in qm)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 1200
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.category = heading

        # Möbel (Verkaufsfläche in qm)
        param = params.moebel = arcpy.Parameter()
        param.name = u'Möbel'
        param.displayName = encode(u'Möbel (Verkaufsfläche in qm)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.value = 1200
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.category = heading


        return params

    def _updateParameters(self, params):
        params = super(TbxNutzungenEinzelhandel, self)._updateParameters(params)
        return params

    def _updateMessages(self, params):
        pass

class TbxNutzungenAlt(Tbx):

    @property
    def label(self):
        return 'Schritt 4 (alt): Nutzungen eingeben'

    @property
    def Tool(self):
        return Nutzungen

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        projects = self.folders.get_projects()

        param = params.projectname = arcpy.Parameter()
        param.name = u'Projekt'
        param.displayName = u'Projekt'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = projects
        param.value = '' if len(projects) == 0 else param.filter.list[0]

        # Teilfläche
        param = params.teilflaeche = arcpy.Parameter()
        param.name = u'Teilfl\xe4che'
        param.displayName = u'Teilfl\xe4che'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []

        # Nutzungsart
        param = params.nutzungsart = arcpy.Parameter()
        param.name = u'Nutzungsart'
        param.displayName = u'Nutzungsart'
        param.datatype = u'GPString'
        param.enabled = False


        # Beginn_der_Aufsiedlung__Jahreszahl_
        param = params.beginn_aufsiedlung = arcpy.Parameter()
        param.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param.displayName = u'Beginn der Aufsiedlung (Jahreszahl)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.filter.type = 'Range'
        param.filter.list = [2010, 2050]

        param.value = datetime.datetime.now().year + 1

        # Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_
        heading = "1) Aufsiedlungszeitraum"
        param = params.dauer_aufsiedlung = arcpy.Parameter()
        param.name = u'Dauer_der_Aufsiedlung__Jahre__1___Aufsiedlung_wird_noch_im_Jahr_des_Aufsiedlungsbeginns_abgeschlossen_'
        param.displayName = u'Dauer der Aufsiedlung (Jahre, 1 = Aufsiedlung wird noch im Jahr des Aufsiedlungsbeginns abgeschlossen)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 5
        param.filter.type = 'Range'
        param.filter.list = [1, 20]
        param.category = heading


        heading = encode(u"2) Wohnen - Anzahl Wohneinheiten nach Gebäudetypen")
        nutzungsart = Nutzungsart.WOHNEN

        # Anzahl_WE_in_Ein-_und_Zweifamilienhäusern
        param = params.we_efh = arcpy.Parameter()
        param.name = u'Anzahl_WE_in_Einfamilienh\xe4usern'
        param.displayName = u'Anzahl WE in Einfamilienh\xe4usern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anzahl_WE_in_Doppelhäusern
        param = params.we_zfh = arcpy.Parameter()
        param.name = u'Anzahl_WE_in_Doppelh\xe4usern'
        param.displayName = u'Anzahl WE in Doppelh\xe4usern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]

        param.category = heading
        param.nutzungsart = nutzungsart

        # Anzahl_WE_in_Reihenhäusern
        param = params.we_rh = arcpy.Parameter()
        param.name = u'Anzahl_WE_in_Reihenh\xe4usern'
        param.displayName = u'Anzahl WE in Reihenh\xe4usern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]

        param.category = heading
        param.nutzungsart = nutzungsart

        # Anzahl_WE_in_Mehrfamilienhäusern
        param = params.we_mfh = arcpy.Parameter()
        param.name = u'Anzahl_WE_in_Mehrfamilienh\xe4usern'
        param.displayName = u'Anzahl WE in Mehrfamilienh\xe4usern'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 500]
        param.category = heading
        param.nutzungsart = nutzungsart


        heading = "3) Wohnen - Anteile Eigentum und Miete"

        # Anteil_Eigentümernutzung_in_Ein-_und_Zweifamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param = params.ant_eigentum_efh = arcpy.Parameter()
        param.name = u'Anteil_Eigent\xfcmernutzung_in_Einfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param.displayName = u'Anteil Eigent\xfcmernutzung in Einfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'90'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_Eigentümernutzung_in_Doppelhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param = params.ant_eigentum_zfh = arcpy.Parameter()
        param.name = u'Anteil_Eigent\xfcmernutzung_in_Doppelh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param.displayName = u'Anteil Eigent\xfcmernutzung in Doppelh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'80'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_Eigentümernutzung_in_Reihenhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param = params.ant_eigentum_rh = arcpy.Parameter()
        param.name = u'Anteil_Eigent\xfcmernutzung_in_Reihenh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param.displayName = u'Anteil Eigent\xfcmernutzung in Reihenh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'70'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_Eigentümernutzung_in_Mehrfamilienhäusern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_
        param = params.ant_eigentum_mfh = arcpy.Parameter()
        param.name = u'Anteil_Eigent\xfcmernutzung_in_Mehrfamilienh\xe4usern__in____Rest_der_Wohnungen_werden_durch_Mieter_genutzt_'
        param.displayName = u'Anteil Eigent\xfcmernutzung in Mehrfamilienh\xe4usern (in %, Rest der Wohnungen werden durch Mieter genutzt)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'20'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart


        heading = "4) Wohnen - Einwohner pro Wohneinheit"

        list_EwProWE = []
        for i in range(1,5):
            for j in range(0,10):
                list_EwProWE.append(str(i)+","+str(j)+" Bewohner pro Wohneinheit")

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienhäusern__kurz_nach_dem_Bezug_
        param = params.ew_je_we_efh = arcpy.Parameter()
        param.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Einfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param.displayName = u'Mittlere Anzahl Einwohner pro WE in Einfamilienh\xe4usern (kurz nach dem Bezug)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,2 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading
        param.nutzungsart = nutzungsart

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelhäusern__kurz_nach_dem_Bezug_
        param = params.ew_je_we_zfh = arcpy.Parameter()
        param.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Doppelh\xe4usern__kurz_nach_dem_Bezug_'
        param.displayName = u'Mittlere Anzahl Einwohner pro WE in Doppelh\xe4usern (kurz nach dem Bezug)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,0 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading
        param.nutzungsart = nutzungsart

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenhäusern__kurz_nach_dem_Bezug_
        param = params.ew_je_we_rh = arcpy.Parameter()
        param.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Reihenh\xe4usern__kurz_nach_dem_Bezug_'
        param.displayName = u'Mittlere Anzahl Einwohner pro WE in Reihenh\xe4usern (kurz nach dem Bezug)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'3,0 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading
        param.nutzungsart = nutzungsart

        # Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienhäusern__kurz_nach_dem_Bezug_
        param = params.ew_je_we_mfh = arcpy.Parameter()
        param.name = u'Mittlere_Anzahl_Einwohner_pro_WE_in_Mehrfamilienh\xe4usern__kurz_nach_dem_Bezug_'
        param.displayName = u'Mittlere Anzahl Einwohner pro WE in Mehrfamilienh\xe4usern (kurz nach dem Bezug)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'2,1 Bewohner pro Wohneinheit'
        param.filter.list = list_EwProWE
        param.category = heading
        param.nutzungsart = nutzungsart


        heading = "5) Wohnen - Zuzugsquote"

        # Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_
        param = params.zuzugsquote_ew = arcpy.Parameter()
        param.name = u'Wie_viel_Prozent_der_Bewohner_der_neuen_Wohnungen_werden_neu_in_die_Gemeinde_ziehen_'
        param.displayName = u'Wie viel Prozent der Bewohner der neuen Wohnungen werden neu in die Gemeinde ziehen?'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'80'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart


        heading = "6) Gewerbe - Gebietstyp und Brachenstruktur"
        nutzungsart = Nutzungsart.GEWERBE

        # Gebietstyp_auswählen
        param = params.gebietstyp = arcpy.Parameter()
        param.name = u'Gebietstyp_ausw\xe4hlen'
        param.displayName = u'Gebietstyp ausw\xe4hlen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.value = u'<kein Gewerbegebiet vorhanden>'
        param.filter.list = [u'Industriegebiet', u'Logistikgebiet', u'Klassisches Gewerbegebiet', u'Kleinteiliges Gewerbegebiet', u'Hoeherwertiges Gewerbegebiet', u'Technologiepark, Wissenschaftspark', u'<kein Gewerbegebiet vorhanden>']
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_verarbeitenden_Gewerbe__in_Prozent_
        param = params.ant_jobs_verarb_gewerbe = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_verarbeitenden_Gewerbe__in_Prozent_'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im verarbeitenden Gewerbe (in Prozent)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'40'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_Baugewerbe__in_Prozent_
        param = params.ant_jobs_baugewerbe = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_Baugewerbe__in_Prozent_'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im Baugewerbe (in Prozent)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'6'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_Handel__inkl__Kfz___in_Prozent_
        param = params.ant_jobs_handel = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_Handel__inkl__Kfz___in_Prozent_'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im Handel (inkl. Kfz) (in Prozent)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'17'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_Verkehrs-_und_Lagereibereich___in_Prozent_
        param = params.ant_jobs_logistik = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_Verkehrs-_und_Lagereibereich___in_Prozent_'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im Verkehrs- und Lagereibereich  (in Prozent)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'10'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_
        param = params.ant_jobs_freiwisstech = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_der_freiberuflichen__wissenschaftl__bzw__techn__Dienstleistungen__in_Prozent_'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich der freiberuflichen, wissenschaftl. bzw. techn. Dienstleistungen (in Prozent)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'14'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Anteil_der_Arbeitsplätze_im_Bereich_sonstiger_Diensteistungen
        param = params.ant_jobs_sonst_dl = arcpy.Parameter()
        param.name = u'Anteil_der_Arbeitspl\xe4tze_im_Bereich_sonstiger_Diensteistungen'
        param.displayName = u'Anteil der Arbeitspl\xe4tze im Bereich sonstiger Diensteistungen'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'13'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart


        heading = "7) Gewerbe - Zuzugs- und Eigentumsquote"

        # Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_
        param = params.zuzugsquote_gewerbe = arcpy.Parameter()
        param.name = u'Wie_viel_Prozent_der_Unternehmen_werden_neu_in_die_Gemeinde_ziehen_'
        param.displayName = u'Wie viel Prozent der Unternehmen werden neu in die Gemeinde ziehen?'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'80'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        # Welcher_Anteil_der_Gebäude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_
        param = params.ant_eigentum_gewerbe = arcpy.Parameter()
        param.name = encode(u'Welcher_Anteil_der_Geb\xe4ude_ist_voraussichtlich_im_Eigentum_der_Unternehmen_')
        param.displayName = encode(u'Welcher Anteil der Geb\xe4ude ist voraussichtlich im Eigentum der Unternehmen?')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'100'
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = heading
        param.nutzungsart = nutzungsart

        heading = "8) Einzelhandel (nur Lebensmitteleinzelhandel)"
        nutzungsart = Nutzungsart.EINZELHANDEL

        # Verkaufsfläche__in_Quadratmetern_
        param = params.verkaufsflaeche = arcpy.Parameter()
        param.name = nutzungsart
        param.displayName = encode(u'Verkaufsfl\xe4che (in Quadratmetern)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = u'0'
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]

        param.category = heading
        param.nutzungsart = nutzungsart

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def update_categories(nutzungsart_id):
            for param in params:
                if hasattr(param, 'nutzungsart'):
                    if param.nutzungsart != nutzungsart_id:
                        #param.category = u'nicht benötigt'
                        param.enabled = False
                    else:
                        param.enabled = True

        if params.projectname.altered and not params.projectname.hasBeenValidated:
            params.teilflaeche.value = ''

            list_teilflaechen = self.tool.teilflaechen.keys()
            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaechen:
                flaeche = list_teilflaechen[0]
                params.teilflaeche.value = list_teilflaechen[0]

        if ((params.projectname.altered and not params.projectname.hasBeenValidated) or
            (params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated)):
            flaeche = params.teilflaeche.value
            flaechen_id = self.tool.teilflaechen[flaeche]
            nutzungsart_id = self.tool.get_nutzungsart_id(flaechen_id)
            nutzungsarten = self.tool.nutzungsarten
            nutzungsart = nutzungsarten.keys()[
                nutzungsarten.values().index(nutzungsart_id)]
            params.nutzungsart.value = nutzungsart
            update_categories(nutzungsart_id)

        def eingaben_auslesen():

            projectname = params.projectname.value
            teilflaeche = params.teilflaeche.value

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
                    params.dauer_aufsiedlung.value = row[1]
                    if row[0] != None:
                        params.beginn_aufsiedlung.value = row[0]
                    else:
                        params.beginn_aufsiedlung.value = row[3]

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

            params.we_efh.value = efh
            params.we_zfh.value = zfh
            params.we_rh.value = rh
            params.we_mfh.value = mfh

            #Wohnen - Anteile Eigentum und Miete
            fields = ['Gebaeudetyp', 'Ant_Eigentuemer', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    params.ant_eigentum_efh.value = row[1]
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    params.ant_eigentum_zfh.value = row[1]
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    params.ant_eigentum_rh.value = row[1]
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    params.ant_eigentum_mfh.value = row[1]

            #Wohnen - Einwohner pro Wohneinheit
            fields = ['Gebaeudetyp', 'EW_je_WE', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tablepath_flaechenbilanz,fields)
            for row in rows:
                if row[2] == teilflaeche and row[0] == "Einfamilienhaus":
                    params.ew_je_we_efh.value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Zweifamilien- oder Doppelhaus":
                    params.ew_je_we_zfh.value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Reihenhaus":
                    params.ew_je_we_rh.value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"
                if row[2] == teilflaeche and row[0] == "Mehrfamilienhaus":
                    params.ew_je_we_mfh.value = str(row[1]).replace(".", ",") + " Bewohner pro Wohneinheit"

            #Gewerbe
            rows = arcpy.da.SearchCursor(tabelle_gewerbeanteile, ["teilflaeche", "branche", "Anteil_A", "Anteil_B" , "Anteil_C" , "Anteil_D" , "Anteil_E", "Anteil_F", "Anteil_Zuzug", "Anteil_Eigentum"])
            for row in rows:
                if row[0] == teilflaeche:
                    params.gebietstyp.value = row[1]
                    params.ant_jobs_verarb_gewerbe.value = row[2]
                    params.ant_jobs_baugewerbe.value = row[3]
                    params.ant_jobs_handel.value = row[4]
                    params.ant_jobs_logistik.value = row[5]
                    params.ant_jobs_freiwisstech.value = row[6]
                    params.ant_jobs_sonst_dl.value = row[7]
                    params.zuzugsquote_gewerbe.value = row[8]
                    params.ant_eigentum_gewerbe.value = row[9]


            #Einzelhandel (nur Lebensmitteleinzelhandel)
            fields = ['Verkaufsflaeche', 'Teilflaeche_Plangebiet']
            rows = arcpy.da.SearchCursor(tabelle_Versorgung_Verkaufsflaechen,fields)
            for row in rows:
                if row[1] == teilflaeche:
                    params.verkaufsflaeche.value = row[0]


        # Gebietstyp auswählen
        if params.gebietstyp.altered and not params.gebietstyp.hasBeenValidated:
            gebtyp = params.gebietstyp.value
            tablepath_gebietstyp = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebietstypen')
            self.folders.get_base_table
            rows = arcpy.SearchCursor(tablepath_gebietstyp)

            for row in rows:
                if gebtyp == row.Gebietstyp:
                    params.ant_jobs_verarb_gewerbe.value = row.Ant_VerarbGew
                    params.ant_jobs_baugewerbe.value = row.Ant_BauGew
                    params.ant_jobs_handel.value = row.Ant_HanKfZ
                    params.ant_jobs_logistik.value = row.Ant_VerLag
                    params.ant_jobs_freiwisstech.value = row.Ant_FrWiTeDi
                    params.ant_jobs_sonst_dl.value = row.Ant_SoDi

        # Automatische Anpassung der Slider
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


        # bestehende Eingaben (falls vorhanden) übernehmen
        i = 1
        if params[i].altered and not params[i].hasBeenValidated:
            eingaben_auslesen()


        # Slider für Anteile an Arbeitsplätzen nach Gewerbetyp generieren
        listeSliderID = [19, 20, 21,22, 23, 24]
        zielwertSlidersumme = 100

        for r in listeSliderID:
            if params[r].altered:
                sliderSummenKontrolle(listeSliderID, zielwertSlidersumme)

        return params

if __name__ == '__main__':
    t = TbxNutzungenGewerbe()
    params = t.getParameterInfo()
    #t.print_test_parameters()
    #t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()