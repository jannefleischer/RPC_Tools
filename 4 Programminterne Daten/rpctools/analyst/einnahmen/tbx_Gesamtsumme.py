# -*- coding: utf-8 -*-

import arcpy
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.analyst.einnahmen.script_Gesamtsumme import Gesamtsumme
import rpctools.utils.chronik as c

class TbxGesamtsumme(Tbx):
    """Toolbox TbxGesamtsumme für Einnahmen"""

    @property
    def label(self):
        return u'Gesamtsumme'

    @property
    def Tool(self):
        return Gesamtsumme

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

        return par

    def _updateMessages(self, params):

        par = self.par


        wohnen_vorhanden = False
        gewerbe_oder_einzelhandel_vorhanden = False

        cursor = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb',
                                where=where)

        for row in cursor:
            if row[0] == Nutzungsart.GEWERBE:
                gewerbe_oder_einzelhandel_vorhanden = True
            if row[0] == Nutzungsart.EINZELHANDEL:
                gewerbe_oder_einzelhandel_vorhanden = True
            if row[0] == Nutzungsart.WOHNEN:
                wohnen_vorhanden = True

        table = self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=par.name.value)
        cursor = self.query_table(table_name = 'Chronik_Nutzung',
                                columns = ['Arbeitsschritt', 'Letzte_Nutzung'],
                                workspace='FGDB_Einnahmen.gdb')

        for row in cursor:
            if row[0] == "Grundsteuer" and row[1] is None:
                par.name.setErrorMessage(u'Es wurde noch keine Grundsteuer berechnet!')

            if wohnen_vorhanden and row[0] == "Wanderung Einwohner" and row[1] is None:
                par.name.setErrorMessage(u'Es wurden noch keine Wanderungssalden für Einwohner berechnet!')
            if wohnen_vorhanden and row[0] == "Einkommensteuer" and not c.compare_chronicle("Einkommensteuer", "Wanderung Einwohner", table):
                par.name.setErrorMessage(u'Es wurden noch keine Einkommensteuer berechnet!')
            if wohnen_vorhanden and row[0] == "Familienleistungsausgleich"  and not c.compare_chronicle("Familienleistungsausgleich", "Einkommensteuer", table):
                par.name.setErrorMessage(u'Es wurde noch kein Familienleistungsausgleich berechnet!')

            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Wanderung Beschaeftigte" and row[1] is None:
                par.name.setErrorMessage(u'Es wurden noch keine Wanderungssalden für Beschäftigte berechnet!')
            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Gewerbesteuer" and not c.compare_chronicle("Gewerbesteuer", "Wanderung Beschaeftigte", table):
                par.name.setErrorMessage(u'Es wurde noch keine Gewerbesteuer berechnet!')
            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Umsatzsteuer" and not c.compare_chronicle("Umsatzsteuer", "Gewerbesteuer", table):
                par.name.setErrorMessage(u'Es wurden noch keine Umsatzsteuer berechnet!')