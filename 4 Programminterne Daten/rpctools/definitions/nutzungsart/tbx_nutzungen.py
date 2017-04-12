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
from rpctools.utils.constants import Branche, Gewerbegebietstyp
from rpctools.utils.spatial_lib import get_gemeindetyp
from collections import OrderedDict


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
        param.datatype = u'GPDouble'
        param.value = 3.2
        param.filter.type = 'Range'
        param.filter.list = [0., 4.]
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
    
    # properties derived from base tables
    _gewerbegebietstypen = None
    _presets = None
    _dichtekennwerte = None

    @property
    def Tool(self):
        return Nutzungen
    
    @property
    def gewerbegebietstypen(self):
        """dictionary with names of gewerbegebiete as keys and ids as values"""
        if self._gewerbegebietstypen is None:            
            table = self.folders.get_base_table(
                'FGDB_Definition_Projekt_Tool.gdb',
                'Gewerbegebietstypen')
            self._gewerbegebietstypen = OrderedDict({u'<benutzerdefiniert>': 0})
            columns = ['Name_Gewerbegebietstyp', 'IDGewerbegebietstyp']
            cursor = arcpy.da.SearchCursor(table, columns)
            for name, id_gewerbe in cursor: 
                self._gewerbegebietstypen[name] = id_gewerbe
        return self._gewerbegebietstypen

    @property
    def presets(self):    
        """dictionary with gewerbetyp as keys and dictionaries 
        (key / value-pairs: id branche / recommended value) as values"""        
        if self._presets is None:            
            table = self.folders.get_base_table(
                'FGDB_Definition_Projekt_Tool.gdb',
                'Vorschlagswerte_Branchenstruktur')
            self._presets = {}
            columns = ['IDGewerbegebietstyp', 
                       'ID_Branche_ProjektCheck', 
                       'Vorschlagswert_in_Prozent']
            cursor = arcpy.da.SearchCursor(table, columns)
            for id_gewerbe, id_branche, value in cursor: 
                if id_gewerbe not in self._presets:
                    self._presets[id_gewerbe] = {}
                self._presets[id_gewerbe][id_branche] = value
        return self._presets
    
    @property
    def dichtekennwerte(self):    
        """dictionary with gewerbetyp as keys and dictionaries 
        (key / value-pairs: id branche / jobs per ha) as values"""        
        if self._dichtekennwerte is None:            
            table = self.folders.get_base_table(
                'FGDB_Definition_Projekt_Tool.gdb',
                'Dichtekennwerte_Gewerbe')
            self._dichtekennwerte = {}
            columns = ['Gemeindetyp_ProjektCheck', 
                       'ID_Branche_ProjektCheck', 
                       'AP_pro_ha_brutto']
            cursor = arcpy.da.SearchCursor(table, columns)
            for gemeindetyp, id_branche, jobs_per_ha in cursor: 
                if gemeindetyp not in self._dichtekennwerte:
                    self._dichtekennwerte[gemeindetyp] = {}
                self._dichtekennwerte[gemeindetyp][id_branche] = jobs_per_ha
        return self._dichtekennwerte    

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
          
        param.filter.list = self.gewerbegebietstypen.keys()
        param.value = param.filter.list[0]
        param.category = heading
    
        # remember params of 
        self.branche_params = []

        # Anteil der Arbeitsplätze im verarbeitenden Gewerbe in Prozent
        name = 'ant_jobs_verarb_gewerbe'
        self.branche_params.append(name)
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
        param.id_branche = Branche.VERARBEITEND

        # Anteil der Arbeitsplätze im Baugewerbe in Prozent
        name = 'ant_jobs_baugewerbe'
        self.branche_params.append(name)
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
        param.id_branche = Branche.BAUGEWERBE

        # Anteil der Arbeitsplätze im Handel inkl. Kfz in Prozent
        name = 'ant_jobs_grosshandel'
        self.branche_params.append(name)
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
        param.id_branche = Branche.GROSSHANDEL

        # Anteil der Arbeitsplätze im Bereich der freiberuflichen wissenschaftl
        # bzw. techn. Dienstleistungen in Prozent
        name = 'ant_jobs_freiwisstech'
        self.branche_params.append(name)
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
        param.id_branche = Branche.FINANZEN

        # Anteil der Arbeitsplätze im Bereich sonstiger Diensteistungen
        name = 'ant_jobs_sonst_dl'
        self.branche_params.append(name)
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
        param.id_branche = Branche.DIENSTLEISTUNGEN

        # Öffentliche Verwaltung
        name = 'ant_oev'
        self.branche_params.append(name)
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
        param.id_branche = Branche.OEFFENTLICH
        
        self.add_dependency(self.branche_params, 100)

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
        param.enabled = False
        param.filter.type = 'Range'
        param.filter.list = [0, 2000]

        return params
    
    def set_gewerbe_presets(self, id_gewerbe):
        """set all branche values to db-presets of given gewerbe-id"""
        presets = self.presets[id_gewerbe]
        for param_name in self.branche_params:
            param = self.par[param_name]
            preset = presets[param.id_branche]
            param.value = preset

    def _updateParameters(self, params):
        params = super(TbxNutzungenGewerbe, self)._updateParameters(params)

        reestimate_jobs = False
        
        # set presets
        if self.par.changed('gebietstyp'):
            id_gewerbe = self.gewerbegebietstypen[params.gebietstyp.value]
            if id_gewerbe != Gewerbegebietstyp.BENUTZERDEFINIERT:
                self.set_gewerbe_presets(id_gewerbe)
                reestimate_jobs = True
                # ToDo: write to db
        else:
            altered = False
            # check if one of the branchenanteile changed
            if any(map(self.par.changed, self.branche_params)):
                # set selection to "benutzerdefiniert" and recalc. jobs
                self.par.gebietstyp.value = self.par.gebietstyp.filter.list[0]
                reestimate_jobs = True
         
        auto_idx = self.par.auto_select.filter.list.index(
            self.par.auto_select.value)
        
        if self.par.changed('auto_select'):
            # auto calc. entry
            if auto_idx == 0:
                reestimate_jobs = True
                params.arbeitsplaetze_insgesamt.enabled = False
            # manual entry
            else:                
                params.arbeitsplaetze_insgesamt.enabled = True
        
        if reestimate_jobs and auto_idx == 0:
            self.set_estimate_jobs()
            # ToDo write to gdb
            
        return params
    
    def set_estimate_jobs(self):
        """calculate estimation of number of jobs and set value of corresponding 
        param 'arbeitsplaetze_insgesamt'"""
        flaeche = self.par.teilflaeche.value
        if not flaeche:
            return
        n_jobs = 0
        
        flaechen_id, flaechenname, ha, ags = \
            self.teilflaechen[flaeche]
        gemeindetyp = get_gemeindetyp(ags)
        kennwerte = self.dichtekennwerte[gemeindetyp]
        for name in self.branche_params:
            param = self.par[name]
            jobs_per_ha = kennwerte[param.id_branche]
            n_jobs += ha * (param.value / 100.) * jobs_per_ha
        
        self.par.arbeitsplaetze_insgesamt.value = n_jobs

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

if __name__ == '__main__':
    t = TbxNutzungenGewerbe()
    params = t.getParameterInfo()
    #t.print_test_parameters()
    #t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()