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
from rpctools.definitions.nutzungsart.buildingtypes import (
    Gebaeudetyp, Gebaeudetypen, Sortiment, Sortimente)
from collections import OrderedDict


class TbxNutzungen(TbxFlaechendefinition):
    _label = u'Schritt 3{sub}: Nutzungen - {name} definieren'
    _nutzungsart = Nutzungsart.UNDEFINIERT

    @property
    def label(self):
        return self._label

    def init_aufsiedlung(self, params, heading='', beginn_name='',
                         default_zeitraum=5):
        """WORKAROUND: add the aufsiedlungs parameters outside of
        _getParameterInfo, strangely the subclasses of TbxNutzungen are
        not recognized as subclasses (so you can't call _getParameterInfo
        of TbxFlaechendefinition here"""


        # Beginn der Aufsiedlung (Jahreszahl)
        param = self.add_parameter('bezugsbeginn')
        param.name = u'Beginn_der_Aufsiedlung__Jahreszahl_'
        param.displayName = beginn_name or encode(u'Beginn der Aufsiedlung '
                                                  u'(Jahreszahl)')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.filter.type = 'Range'
        # ToDo: Jahre an die Jahre der Projektdefinition anpassen
        param.filter.list = [2010, 2050]
        param.value = 2018
        param.category = heading

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
        param.value = default_zeitraum
        param.filter.type = 'Range'
        param.filter.list = [1, 20]
        param.category = heading

        return params

    def _updateParameters(self, params):
        params = super(TbxNutzungen, self)._updateParameters(params)

        flaeche = params.teilflaeche.value
        if flaeche:
            tfl = self.get_teilflaeche(params.teilflaeche.value)

            if params.changed('bezugsbeginn', 'dauer_aufsiedlung'):
                table = 'Teilflaechen_Plangebiet'
                column_values = dict(
                    Beginn_Nutzung=params.bezugsbeginn.value,
                    Aufsiedlungsdauer=params.dauer_aufsiedlung.value)
                self.update_table(table, column_values, tfl.where_clause)

        return params

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""
        columns = ['Beginn_Nutzung', 'Aufsiedlungsdauer']
        pkey = dict(id_teilflaeche=flaechen_id)
        rows = self.query_table('Teilflaechen_Plangebiet',
                                columns,
                                pkey=pkey)
        for row in rows:
            self.par.bezugsbeginn.value = row[0]
            self.par.dauer_aufsiedlung.value = row[1]


class TbxNutzungenWohnen(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='a', name='Wohnen')
    _nutzungsart = Nutzungsart.WOHNEN

    ew_je_we_range = [r / 10.0 for r in range(10, 50)]

    def __init__(self):
        super(TbxNutzungenWohnen, self).__init__()
        self.gebaeudetypen = Gebaeudetypen(self.folders)

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

    def _updateParameters(self, params):
        params = super(TbxNutzungenWohnen, self)._updateParameters(params)

        flaeche = params.teilflaeche.value
        if flaeche:
            tfl = self.get_teilflaeche(params.teilflaeche.value)

            for gt in self.gebaeudetypen.itervalues():
                assert isinstance(gt, Gebaeudetyp)
                if params.changed(gt.param_we, gt.param_ew_je_we):
                    table = 'Wohnen_WE_in_Gebaeudetypen'
                    pkey = dict(IDTeilflaeche=tfl.flaechen_id,
                                IDGebaeudetyp=gt.typ_id)
                    column_values = dict(
                        Gebaeudetyp=gt.name,
                        WE=params[gt.param_we].value,
                        EW_je_WE=params[gt.param_ew_je_we].value,
                    )
                    r = self.upsert_row_in_table(table, column_values, pkey)

        return params

    def update_teilflaechen_inputs(self, flaechen_id, flaechenname):
        """update all inputs based on currently selected teilflaeche"""
        super(TbxNutzungenWohnen, self).update_teilflaechen_inputs(
            flaechen_id,flaechenname)
        columns = ['IDGebaeudetyp', 'WE', 'EW_je_WE']
        pkey = dict(IDTeilflaeche=flaechen_id)
        rows = self.query_table('Wohnen_WE_in_Gebaeudetypen',
                                columns,
                                pkey=pkey)

        # if there are no values defined yet, set to default values
        if not rows:
            for gt in self.gebaeudetypen.itervalues():
                self.par[gt.param_we].value = 0
                self.par[gt.param_ew_je_we].value = gt.default_ew_je_we

        # otherwise, update parameters from query
        for row in rows:
            gt = self.gebaeudetypen[row[0]]
            self.par[gt.param_we].value = row[1]
            self.par[gt.param_ew_je_we].value = row[2]

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
        param = self.add_parameter('gebietstyp')
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
        param = self.add_parameter(name)
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
        param = self.add_parameter(name)
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
        param = self.add_parameter(name)
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
        param = self.add_parameter(name)
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
        param = self.add_parameter(name)
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
        param = self.add_parameter(name)
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

        tfl = self.teilflaechen[flaeche]
        gemeindetyp = get_gemeindetyp(tfl.ags)
        kennwerte = self.dichtekennwerte[gemeindetyp]
        for name in self.branche_params:
            param = self.par[name]
            jobs_per_ha = kennwerte[param.id_branche]
            n_jobs += tfl.ha * (param.value / 100.) * jobs_per_ha

        self.par.arbeitsplaetze_insgesamt.value = n_jobs

    def _updateMessages(self, params):
        pass


class TbxNutzungenEinzelhandel(TbxNutzungen):
    _label = TbxNutzungen._label.format(sub='c', name='Einzelhandel')
    _nutzungsart = Nutzungsart.EINZELHANDEL
    tablename = 'Einzelhandel_Verkaufsflaechen'

    @property
    def Tool(self):
        return Nutzungen

    def __init__(self):
        super(TbxNutzungenEinzelhandel, self).__init__()
        self.sortimente = Sortimente(self.folders)

    def _getParameterInfo(self):
        params = super(TbxNutzungenEinzelhandel, self)._getParameterInfo()
        # workaround
        heading = '1) Voraussichtliche Eröffnung '
        beginn_name = 'Baubeginn'
        params = self.init_aufsiedlung(params, heading=heading,
                                       beginn_name=beginn_name,
                                       default_zeitraum=1)

        heading = u'2) Verkaufsflächen'

        for srt in self.sortimente.itervalues():
            assert isinstance(srt, Sortiment)
            # Verkaufsfläche nach Sortiment
            param = self.add_parameter(srt.param_vfl)
            param.name = encode(srt.kurzname)
            param.displayName = encode(u'{}  (Verkaufsfläche in qm)'.format(srt.name))
            param.parameterType = 'Required'
            param.direction = 'Input'
            param.datatype = u'Long'
            param.value = u'0'
            param.filter.type = 'Range'
            param.filter.list = [0, 20000]
            param.category = heading

        return params

    def _updateParameters(self, params):
        params = super(TbxNutzungenEinzelhandel, self)._updateParameters(params)
        flaeche = params.teilflaeche.value
        if flaeche:
            tfl = self.get_teilflaeche(params.teilflaeche.value)

            for srt in self.sortimente.itervalues():
                assert isinstance(srt, Sortiment)
                if params.changed(srt.param_vfl):
                    pkey = dict(IDTeilflaeche=tfl.flaechen_id,
                                IDSortiment=srt.typ_id)
                    column_values = dict(
                        NameSortiment=srt.kurzname,
                        Verkaufsflaeche_qm=params[srt.param_vfl].value,
                    )
                    r = self.upsert_row_in_table(
                        self.tablename, column_values, pkey)
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