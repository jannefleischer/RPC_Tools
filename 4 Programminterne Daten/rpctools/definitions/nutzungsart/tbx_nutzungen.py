# -*- coding: utf-8 -*-

import sys

from os.path import abspath, dirname, join
import numpy as np
import arcpy
import datetime
import pandas as pd

from rpctools.utils.params import Tbx
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.definitions.nutzungsart.nutzungen import (
    NutzungenGewerbe, NutzungenWohnen, NutzungenEinzelhandel)
from rpctools.utils.encoding import encode
from rpctools.utils.constants import Branche, Gewerbegebietstyp
from rpctools.utils.spatial_lib import get_gemeindetyp
from rpctools.utils.basetable_definitions import (
    Gebaeudetyp, Gebaeudetypen, Sortiment, Sortimente, Branche, Branchen)
from collections import OrderedDict


class TbxNutzungen(TbxFlaechendefinition):
    _label = u'Schritt 3{sub}: Nutzungen - {name} definieren'
    _nutzungsart = Nutzungsart.UNDEFINIERT
    _duration_heading = None
    _displayname_begin = u'Beginn der Aufsiedlung (Jahreszahl)'

    @property
    def label(self):
        return self._label

    def _getParameterInfo(self):
        super(TbxNutzungen, self)._getParameterInfo()

        # Beginn der Aufsiedlung (Jahreszahl)
        param = self.add_parameter('bezugsbeginn')
        param.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param.displayName = self._displayname_begin
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.filter.type = 'Range'
        # ToDo: Jahre an die Jahre der Projektdefinition anpassen
        param.filter.list = [2010, 2050]
        param.category = self._duration_heading

        param.value = datetime.datetime.now().year + 1
    
        # Dauer des Bezugs (Jahre, 1 = Bezug wird noch im Jahr des
        # Bezugsbeginns abgeschlossen)
        param = self.add_parameter('dauer_aufsiedlung')
        param.name = u'dauer_aufsiedlung'
        param.displayName = (u'Dauer des Bezugs (Jahre, 1 = Bezug wird noch '
                             u'im Jahr des Bezugsbeginns abgeschlossen)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 1
        param.filter.type = 'Range'
        param.filter.list = [1, 20]
        param.category = self._duration_heading

        return self.par

    def set_selected_area(self):
        area, i = self.get_selected_area()
        self.par.bezugsbeginn.value = int(area['Beginn_Nutzung'])
        if 'dauer_aufsiedlung' in self.par:
            self.par.dauer_aufsiedlung.value = int(area['Aufsiedlungsdauer'])

    def _updateParameters(self, params):
        area, idx = self.get_selected_area()
        
        if self.par.changed('area'):
            self.set_selected_area()
        
        elif self.par.changed('bezugsbeginn'):
            self.df_areas.loc[idx, 'Beginn_Nutzung'] = self.par.bezugsbeginn.value
        elif ('dauer_aufsiedlung' in self.par and
            self.par.changed('dauer_aufsiedlung')):
            self.df_areas.loc[idx, 'Aufsiedlungsdauer'] = \
                self.par.dauer_aufsiedlung.value
        return params


class TbxNutzungenWohnen(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='a', name='Wohnen')
    _nutzungsart = Nutzungsart.WOHNEN
    _duration_heading = "1) Bezugszeitraum"
    _displayname_begin = u'Beginn des Bezugs (Jahreszahl)'

    ew_je_we_range = [r / 10.0 for r in range(10, 50)]

    def __init__(self):
        super(TbxNutzungenWohnen, self).__init__()
        self.gebaeudetypen = Gebaeudetypen(self.folders)

    @property
    def Tool(self):
        return NutzungenWohnen

    def _getParameterInfo(self):
        params = super(TbxNutzungenWohnen, self)._getParameterInfo()

        # specific parameters for "Wohnen"

        heading = encode(u"2) Anzahl Wohneinheiten nach Gebäudetypen")

        for gt in self.gebaeudetypen.itervalues():
            assert isinstance(gt, Gebaeudetyp)
            # Anzahl WE in Gebäudetypen
            param = self.add_parameter(gt.param_we)
            param.name = encode(u'Bewohner {}'.format(gt.display_name))
            param.displayName = encode(u'Anzahl WE in {}'.format(gt.display_name))
            param.parameterType = 'Required'
            param.direction = 'Input'
            param.datatype = u'Long'
            param.value = u'0'
            param.filter.type = 'Range'
            param.filter.list = [0, 500]
            param.category = heading

        heading = ("3) Mittlere Anzahl Einwohner pro Wohneinheit " +
                   "(3 Jahre nach Bezug)")

        for gt in self.gebaeudetypen.itervalues():
            assert isinstance(gt, Gebaeudetyp)
            # Mittlere Anzahl Einwohner pro WE in Einfamilienhäusern
            # (kurz nach dem Bezug)
            param = self.add_parameter(gt.param_ew_je_we)
            param.name = encode(u'EW_JE_WE {}'.format(gt.display_name))
            param.displayName = encode(u'in {}'.format(gt.display_name))
            param.parameterType = 'Required'
            param.direction = 'Input'
            param.datatype = u'GPDouble'
            param.value = gt.default_ew_je_we
            param.filter.list = self.ew_je_we_range
            param.category = heading

        return params
    
    def _open(self, params):
        self.df_acc_units = self.get_accommodation_units()
        super(TbxNutzungenWohnen, self)._open(params)        
        
    def get_accommodation_units(self):
        df_acc_units = self.table_to_dataframe(
            'Wohnen_WE_in_Gebaeudetypen')
        return df_acc_units

    def set_selected_area(self):
        """update all inputs based on currently selected teilflaeche"""
        super(TbxNutzungenWohnen, self).set_selected_area()
        area, idx = self.get_selected_area()

        acc_idx = self.df_acc_units['IDTeilflaeche'] == area['id_teilflaeche']
        rows = self.df_acc_units[acc_idx]
        # if there are no values defined yet, set to default values
        if len(rows) == 0:
            columns=['IDTeilflaeche', 'IDGebaeudetyp',
                     'WE', 'EW_je_WE']
            for gt in self.gebaeudetypen.itervalues():
                we = 0
                ew_je_we = gt.default_ew_je_we
                self.par[gt.param_we].value = we
                self.par[gt.param_ew_je_we].value = ew_je_we
                row = pd.DataFrame([[area['id_teilflaeche'], gt.typ_id,
                                     we, ew_je_we]],
                                   columns=columns)
                self.df_acc_units = self.df_acc_units.append(
                    row, ignore_index=True)
        
        else:
            # otherwise: update values
            for index, row in rows.iterrows():
                gt = self.gebaeudetypen[row['IDGebaeudetyp']]
                self.par[gt.param_we].value = row['WE']
                self.par[gt.param_ew_je_we].value = row['EW_je_WE']

    #def update_dataframes(self):
        #""""""
        #area, area_idx = self.get_selected_area()
        #area_id = area['id_teilflaeche']
        #we_sum = 0
        #for gt in self.gebaeudetypen.itervalues():
            #row_idx = ((self.df_acc_units['IDTeilflaeche'] == area['id_teilflaeche']).values &
                       #(self.df_acc_units['IDGebaeudetyp'] == gt.typ_id).values)
            #we = self.par[gt.param_we].value
            #ew_je_we = self.par[gt.param_ew_je_we].value
            #self.df_acc_units.loc[row_idx, 'WE'] = we
            #self.df_acc_units.loc[row_idx, 'EW_je_WE'] = ew_je_we
            #we_sum += we
        #self.df_areas.loc[area_idx, 'WE_gesamt'] = we_sum
        
    def _update_row(self, area, geb_typ, key, value):
        area_id = area['id_teilflaeche']
        row_idx = ((self.df_acc_units['IDTeilflaeche'] == area['id_teilflaeche']).values &
                   (self.df_acc_units['IDGebaeudetyp'] == geb_typ).values)
        self.df_acc_units.loc[row_idx, key] = value
        
    def _updateParameters(self, params):
        params = super(TbxNutzungenWohnen, self)._updateParameters(params)
        area, area_idx = self.get_selected_area()
        
        for gt in self.gebaeudetypen.itervalues():
            if params.changed(gt.param_we):
                self._update_row(area, gt.typ_id, 'WE',
                                 self.par[gt.param_we].value)
            elif params.changed(gt.param_ew_je_we):
                self._update_row(area, gt.typ_id, 'EW_je_WE',
                                 self.par[gt.param_ew_je_we].value)

        return params    


class TbxNutzungenGewerbe(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='b', name='Gewerbe')
    _nutzungsart = Nutzungsart.GEWERBE
    _duration_heading = "1) Bezugszeitraum"
    _displayname_begin = u'Beginn des Bezugs (Jahreszahl)'

    # properties derived from base tables
    _gewerbegebietstypen = None
    _presets = None
    _dichtekennwerte = None
    tablename = 'Gewerbe_Anteile'

    def __init__(self):
        super(TbxNutzungenGewerbe, self).__init__()
        self.branchen = Branchen(self.folders)

    @property
    def Tool(self):
        return NutzungenGewerbe

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

        heading = u"2) Voraussichtlicher Anteil der Branchen an der Nettofläche"

        # Gebietstyp auswählen
        param = self.add_parameter('gebietstyp')
        param.name = u'Gebietstyp'
        param.displayName = encode(u'Gebietstyp auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param.filter.list = self.gewerbegebietstypen.keys()
        param.value = param.filter.list[0]
        param.category = heading

        # remember params
        sum_params = []
        
        for branche in self.branchen.itervalues():
            assert isinstance(branche, Branche)
            param = self.add_parameter(branche.param_gewerbenutzung)
            param.name = encode(encode(branche.name))
            param.displayName = encode(
                u'{} (in % der Nettofläche)'.format(branche.name))
            param.parameterType = 'Required'
            param.direction = 'Input'
            param.datatype = u'Long'
            param.value = branche.default_gewerbenutzung
            param.filter.type = 'Range'
            param.filter.list = [0, 100]
            param.category = heading
            sum_params.append(branche.param_gewerbenutzung)
        
        self.add_dependency(sum_params, 100)

        heading = u'3) Voraussichtliche Anzahl an Arbeitsplätzen'

        # Arbeitsplatzzahl schätzen
        param = self.add_parameter('auto_select')
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
        param = self.add_parameter('arbeitsplaetze_insgesamt')
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
        param.filter.list = [0, 10000]

        return params

    def set_gewerbe_presets(self, id_gewerbe):
        """set all branche values to db-presets of given gewerbe-id"""
        presets = self.presets[id_gewerbe]
        for branche in self.branchen.itervalues():
            param = self.par[branche.param_gewerbenutzung]
            preset = presets[branche.id]
            param.value = preset

    def _updateParameters(self, params):
        params = super(TbxNutzungenGewerbe, self)._updateParameters(params)

        altered = False

        flaeche = params.teilflaeche.value
        tfl = self.get_teilflaeche(flaeche)
        if not tfl:
            return params

        # set presets
        if self.par.changed('gebietstyp'):
            id_gewerbe = self.gewerbegebietstypen[params.gebietstyp.value]
            if id_gewerbe != Gewerbegebietstyp.BENUTZERDEFINIERT:
                self.set_gewerbe_presets(id_gewerbe)
                altered = True
        else:
            # check if one of the branchenanteile changed
            if any(map(self.par.changed,
                       [branche.param_gewerbenutzung
                        for branche in self.branchen.values()])):
                # set selection to "benutzerdefiniert" and recalc. jobs
                self.par.gebietstyp.value = self.par.gebietstyp.filter.list[0]
                altered = True

        auto_idx = self.par.auto_select.filter.list.index(
            self.par.auto_select.value)

        if self.par.changed('auto_select'):
            # auto calc. entry
            if auto_idx == 0:
                altered = True
                params.arbeitsplaetze_insgesamt.enabled = False
            # manual entry
            else:
                params.arbeitsplaetze_insgesamt.enabled = True
            
        if altered:  #and auto_idx == 0:
            n_jobs = self.estimate_jobs()
            if auto_idx == 0:
                params.arbeitsplaetze_insgesamt.value = n_jobs
                
        return params

    def commit_tfl_changes(self):
        """"""
        super(TbxNutzungenGewerbe, self).commit_tfl_changes()
        tfl = self.par._current_tfl
        for branche in self.branchen.itervalues():
            job_param = self.par[branche.param_gewerbenutzung]
            table = self.tablename
            pkey = {'IDTeilflaeche': tfl.flaechen_id,
                    'IDBranche': branche.id}
            column_values = {
                'anteil': job_param.value,
                'anzahl_jobs_schaetzung': branche.estimated_jobs,
                'dichtekennwert_ap_pro_ha_brutto': branche.jobs_per_ha
            }
            r = self.upsert_row_in_table(table, column_values, pkey)
            
        table_jobs = 'Gewerbe_Arbeitsplaetze'
        pkey = {'IDTeilflaeche': tfl.flaechen_id}
        job_param = self.par.arbeitsplaetze_insgesamt
        column_values = {'Arbeitsplaetze': job_param.value}
        r = self.upsert_row_in_table(table_jobs, column_values, pkey)
        # write number of jobs into flaechen table as well 
        self.update_table('Teilflaechen_Plangebiet',
                          column_values={'AP_gesamt': job_param.value}, 
                          where='id_teilflaeche={}'.format(tfl.flaechen_id))

    def estimate_jobs(self):
        """calculate estimation of number of jobs
        sets estimated jobs to branchen"""
        flaeche = self.par.teilflaeche.value
        if not flaeche:
            return
        jobs_sum = 0

        tfl = self.teilflaechen[flaeche]
        gemeindetyp = get_gemeindetyp(tfl.ags)
        kennwerte = self.dichtekennwerte[gemeindetyp]
        for branche in self.branchen.itervalues():
            param = self.par[branche.param_gewerbenutzung]
            branche.jobs_per_ha = kennwerte[branche.id]
            jobs_branche = tfl.ha * (param.value / 100.) * branche.jobs_per_ha
            branche.estimated_jobs = jobs_branche
            jobs_sum += jobs_branche
        
        return jobs_sum
        
    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""
        super(TbxNutzungenGewerbe, self).update_teilflaechen_inputs(
            flaechen_id, flaechenname) 
        columns = ['IDBranche', 'anteil']
        
        pkey = {'IDTeilflaeche': flaechen_id}
        rows = self.query_table(self.tablename,
                                columns,
                                pkey=pkey)
        # if there are no values defined yet, set to default values
        if not rows:
            for branche in self.branchen.itervalues():
                self.par[branche.param_gewerbenutzung].value = \
                    branche.default_gewerbenutzung
        # update parameters from query else
        else: 
            for row in rows:
                branche = self.branchen[row[0]]
                self.par[branche.param_gewerbenutzung].value = row[1]
            table_jobs = 'Gewerbe_Arbeitsplaetze'
            auto_idx = self.par.auto_select.filter.list.index(
                self.par.auto_select.value)
            # custom settings -> load from db
            if auto_idx == 1:                
                n_jobs = self.query_table(
                    table_jobs, columns=['Arbeitsplaetze'], pkey=pkey)[0][0]
            # auto calc. -> estimate jobs
            else:
                n_jobs = self.estimate_jobs()
            self.par.arbeitsplaetze_insgesamt.value = n_jobs

        self.par.gebietstyp.value = self.par.gebietstyp.filter.list[0]


class TbxNutzungenEinzelhandel(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='c', name='Einzelhandel')
    _nutzungsart = Nutzungsart.EINZELHANDEL
    _duration_heading = '1) Voraussichtliche Eröffnung'
    _displayname_begin = u'Eröffnung'
    tablename = 'Einzelhandel_Verkaufsflaechen'
    _default_duration = 1

    @property
    def Tool(self):
        return NutzungenEinzelhandel

    def __init__(self):
        super(TbxNutzungenEinzelhandel, self).__init__()
        self.sortimente = Sortimente(self.folders)

    def _getParameterInfo(self):
        params = super(TbxNutzungenEinzelhandel, self)._getParameterInfo()

        heading = u'2) Verkaufsflächen'

        for srt in self.sortimente.itervalues():
            assert isinstance(srt, Sortiment)
            # Verkaufsfläche nach Sortiment
            param = self.add_parameter(srt.param_vfl)
            param.name = encode(srt.kurzname)
            param.displayName = encode(u'{} (Verkaufsfläche in qm)'.format(srt.name))
            param.parameterType = 'Required'
            param.direction = 'Input'
            param.datatype = u'Long'
            param.value = u'0'
            param.filter.type = 'Range'
            param.filter.list = [0, 20000]
            param.category = heading

        return params

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""
        super(TbxNutzungenEinzelhandel, self).update_teilflaechen_inputs(
            flaechen_id,flaechenname)
        columns = ['IDSortiment', 'Verkaufsflaeche_qm']
        pkey = dict(IDTeilflaeche=flaechen_id)
        rows = self.query_table(self.tablename,
                                columns,
                                pkey=pkey)

        # if there are no values defined yet, set to default values
        if not rows:
            for srt in self.sortimente.itervalues():
                self.par[srt.param_vfl].value = 0

        # otherwise, update parameters from query
        for row in rows:
            srt = self.sortimente[row[0]]
            self.par[srt.param_vfl].value = row[1]
            
    def commit_tfl_changes(self):
        """"""
        super(TbxNutzungenEinzelhandel, self).commit_tfl_changes()
        tfl = self.par._current_tfl
        sqm_sum = 0
        for srt in self.sortimente.itervalues():
            assert isinstance(srt, Sortiment)
            pkey = dict(IDTeilflaeche=tfl.flaechen_id,
                        IDSortiment=srt.typ_id)
            sqm = self.par[srt.param_vfl].value
            column_values = dict(
                NameSortiment=srt.kurzname,
                Verkaufsflaeche_qm=sqm,
            )
            r = self.upsert_row_in_table(
                self.tablename, column_values, pkey)
            sqm_sum += sqm
        
        self.update_table('Teilflaechen_Plangebiet',
                          column_values={'VF_gesamt': sqm_sum}, 
                          where='id_teilflaeche={}'.format(tfl.flaechen_id))
        

if __name__ == '__main__':
    t = TbxNutzungenWohnen()
    t.getParameterInfo()
    t.set_active_project()
    t.open()
    t._updateParameters(t.par)
    t.execute()
    #t.commit_tfl_changes()
    #t.tool.calculate_ways()
    #t.tool.update_wege_projekt()
    #t.tool.main(t.par, None)
    #df = t.table_to_dataframe('Teilflaechen_Plangebiet',
                              #workspace='FGDB_Definition_Projekt.gdb')
    #t.table_to_dataframe('Wohnen_WE_in_Gebaeudetypen', columns=None)
    #t.print_test_parameters()
    #t.print_tool_parameters()
    #t.updateParameters(params)
    #t.updateMessages(params)
    #t.print_test_parameters()