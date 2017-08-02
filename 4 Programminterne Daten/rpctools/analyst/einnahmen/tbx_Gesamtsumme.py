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

        par.summe = arcpy.Parameter()
        par.summe.name = u'Bestandteile'
        par.summe.displayName = u'Bestandteile der Gesamtsumme'
        par.summe.parameterType = 'Required'
        par.summe.direction = 'Input'
        par.summe.datatype = u'GPString'
        par.summe.value = "Alles"
        par.summe.enabled = False

        return par

    def _updateParameters(self, params):
        par = self.par
        anzahl_bestandteile = 0
        self.spalten = ["Summe_Einnahmenbilanz"]
        grundsteuer = ""
        einkommensteuer = ""
        fla = ""
        gewerbesteuer = ""
        umsatzsteuer = ""

        wohnen_vorhanden = False
        gewerbe_oder_einzelhandel_vorhanden = False

        cursor = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb')

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
            if row[0] == "Grundsteuer" and row[1] is not None:
                self.spalten.append("GrSt")
                if anzahl_bestandteile == 0:
                    grundsteuer = "Grundsteuer"
                else:
                    grundsteuer = " + Grundsteuer"
                anzahl_bestandteile += 1

            if wohnen_vorhanden and row[0] == "Einkommensteuer" and not c.compare_chronicle("Wanderung Einwohner", "Einkommensteuer", table):
                self.spalten.append("ESt")
                if anzahl_bestandteile == 0:
                    einkommensteuer = "Einkommensteuer"
                else:
                    einkommensteuer = " + Einkommensteuer"
                anzahl_bestandteile += 1

            if wohnen_vorhanden and row[0] == "Familienleistungsausgleich"  and not c.compare_chronicle("Familienleistungsausgleich", "Einkommensteuer", table):
                self.spalten.append("FamLeistAusgl")
                if anzahl_bestandteile == 0:
                    fla = "Familienleistungsausgleich"
                else:
                    fla = " + Familienleistungsausgleich"
                anzahl_bestandteile += 1

            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Gewerbesteuer" and not c.compare_chronicle("Wanderung Beschaeftigte", "Gewerbesteuer", table):
                self.spalten.append("GewSt")
                if anzahl_bestandteile == 0:
                    gewerbesteuer = "Gewerbesteuer"
                else:
                    gewerbesteuer = " + Gewerbesteuer"
                anzahl_bestandteile += 1

            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Umsatzsteuer" and not c.compare_chronicle("Gewerbesteuer", "Umsatzsteuer", table):
                self.spalten.append("USt")
                if anzahl_bestandteile == 0:
                    umsatzsteuer = "Umsatzsteuer"
                else:
                    umsatzsteuer = " + Umsatzsteuer"
                anzahl_bestandteile += 1

        bestandteile = grundsteuer + einkommensteuer + fla + gewerbesteuer + umsatzsteuer
        par.summe.value = bestandteile


    def _updateMessages(self, params):

        par = self.par

        wohnen_vorhanden = False
        gewerbe_oder_einzelhandel_vorhanden = False

        cursor = self.query_table('Teilflaechen_Plangebiet',
                                ['Nutzungsart'],
                                workspace='FGDB_Definition_Projekt.gdb')

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

            if wohnen_vorhanden and row[0] == "Wanderung Einwohner" and row[1] is None:
                par.name.setErrorMessage(u'Es wurden noch keine Wanderungssalden für Einwohner berechnet!')

            if gewerbe_oder_einzelhandel_vorhanden and row[0] == "Wanderung Beschaeftigte" and row[1] is None:
                par.name.setErrorMessage(u'Es wurden noch keine Wanderungssalden für Beschäftigte berechnet!')
