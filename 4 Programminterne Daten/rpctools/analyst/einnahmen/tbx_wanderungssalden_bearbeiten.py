# -*- coding: utf-8 -*-

import arcpy
import os
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.utils.constants import Nutzungsart
from rpctools.analyst.einnahmen.script_Wanderungssalden_bearbeiten_Einwohner import Salden_bearbeiten
from rpctools.analyst.einnahmen.script_Wanderungssalden_bearbeiten_Arbeit import Salden_bearbeiten2


class TbxSaldenbearbeiten(Tbx):
    """ superclass for wanderungssalden einwohner/gewerbe"""
    _nutzungsart = None
    _saldo_field = None

    def _getParameterInfo(self):

        par = self.par

        # Projektname
        par.name = arcpy.Parameter()
        par.name.name = u'Projektname'
        par.name.displayName = u'Projektname'
        par.name.parameterType = 'Required'
        par.name.direction = 'Input'
        par.name.datatype = u'GPString'
        par.name.filter.list = []

        par.gemeinde = arcpy.Parameter()
        par.gemeinde.name = u'Gemeinde'
        par.gemeinde.displayName = u'Gemeinden'
        par.gemeinde.parameterType = 'Required'
        par.gemeinde.direction = 'Input'
        par.gemeinde.datatype = u'GPString'
        par.gemeinde.filter.list = []

        par.saldo = arcpy.Parameter()
        par.saldo.name = u'Saldo'
        par.saldo.displayName = u'Saldo'
        par.saldo.parameterType = 'Required'
        par.saldo.direction = 'Input'
        par.saldo.datatype = u'GPLong'

        par.summe = arcpy.Parameter()
        par.summe.name = u'Summe'
        par.summe.displayName = u' Gesamtsumme der Wanderungssalden'
        par.summe.parameterType = 'Required'
        par.summe.datatype = u'GPLong'
        par.summe.enabled = False

        par.kontrolle = arcpy.Parameter()
        par.kontrolle.name = u'kontrolle'
        par.kontrolle.displayName = u'Wanderungssalden so aktualisieren, dass die Gesamtsumme 0 beträgt'
        par.kontrolle.parameterType = 'Optional'
        par.kontrolle.datatype = u'GPBoolean'



        return par

    def _updateParameters(self, params):
        par = self.par
        path_gemeindebilanzen = self.folders.get_table("Gemeindebilanzen", 'FGDB_Einnahmen.gdb')

        if par.changed('name'):
            where = 'Nutzungsart = {}'.format(self._nutzungsart)
            rows = self.query_table('Teilflaechen_Plangebiet',
                                    ['Nutzungsart'],
                                    workspace='FGDB_Definition_Projekt.gdb',
                                    where=where)
            if not rows:
                par.gemeinde.enabled = False
                par.gemeinde.filter.list = []
                par.gemeinde.value = (u'Projekt enthält keine Flächen mit der '
                                      u'benötigten Nutzungsart')
            else:
                par.gemeinde.enabled = True
                gemeinden = []
                fields = ["GEN", self._saldo_field]
                if arcpy.Exists(path_gemeindebilanzen):
                    rows = self.query_table('Gemeindebilanzen', fields,
                                            workspace='FGDB_Einnahmen.gdb')
                    for gem_name, saldo in rows:
                        gemeinden.append(u"{} || Saldo: {}".format(gem_name, saldo))
                    par.gemeinde.filter.list = sorted(gemeinden)
                    par.gemeinde.value = sorted(gemeinden)[0]

        if par.changed('saldo') or par.changed('name') or par.changed('gemeinde'):
            target_gemeinde = par.gemeinde.value
            target_gemeinde_kurz = target_gemeinde.split(" ||")[0]
            summe = 0
            fields = [self._saldo_field, "GEN"]

            if arcpy.Exists(path_gemeindebilanzen):
                rows = self.query_table('Gemeindebilanzen', fields,
                                        workspace='FGDB_Einnahmen.gdb')
                for saldo in rows:
                    if saldo[1] == target_gemeinde_kurz and par.saldo.value != None:
                        summe += par.saldo.value
                    else:
                        summe += saldo[0]
                par.summe.value = summe

    def _updateMessages(self, params):

        par = self.par
        gemeinde_saldo = par.gemeinde.value
        gemeinde_saldo = gemeinde_saldo.split(" ||")[0]

        pfad_rahmendaten = self.folders.get_table(
            tablename='Projektrahmendaten',
            workspace="FGDB_Definition_Projekt.gdb",
            project=par.name.value)
        cursor = arcpy.da.SearchCursor(pfad_rahmendaten, ["Gemeindename"])
        for projekt in cursor:
            gemeinde_projekt = projekt[0]

        path_gemeindebilanzen = os.path.join(self.folders.get_db('FGDB_Einnahmen.gdb'), "Gemeindebilanzen")
        if not arcpy.Exists(path_gemeindebilanzen):
            par.name.setErrorMessage(u'Es müssen zuerst Wanderungssalden geschätzt werden, ehe diese bearbeitet werden können.')

        where = 'Nutzungsart = {}'.format(self._nutzungsart)
        rows = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb',
                                where=where)
        if not rows:
            par.gemeinde.setErrorMessage(u'Projekt enthält keine Flächen mit der benötigten Nutzungsart.')

        if par.saldo.value > 0 and gemeinde_saldo != gemeinde_projekt:
            par.saldo.setErrorMessage('Das Wanderungssaldo dieser Gemeinde darf nicht positiv sein.')


class TbxEWSaldenbearbeiten(TbxSaldenbearbeiten):
    """Toolbox Wanderungssalden für Einnahmen Wohnen"""
    _nutzungsart = Nutzungsart.WOHNEN
    _saldo_field = "Einw_Saldo"

    @property
    def label(self):
        return u'Schritt 1a: Einwohner-Salden bearbeiten'

    @property
    def Tool(self):
        return Salden_bearbeiten


class TbxGewSaldenbearbeiten(TbxSaldenbearbeiten):
    """Toolbox Wanderungssalden für Einnahmen Gewerbe"""
    _nutzungsart = Nutzungsart.GEWERBE
    _saldo_field = "SvB_Saldo"

    @property
    def label(self):
        return u'Schritt 2a: Erwerbstätige-Salden bearbeiten'

    @property
    def Tool(self):
        return Salden_bearbeiten2
