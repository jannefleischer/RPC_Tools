# -*- coding: utf-8 -*-

import os
import sys

import arcpy

from rpctools.utils.params import Tool
import rpctools.utils.chronik as c
from rpctools.utils.encoding import encode
import rpctools.utils.layer_einnahmen as lib_einnahmen

class Gewerbesteuer(Tool):
    """Steuersalden-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        pass

    def run(self):
        """run Steuersalden Tool"""

        params = self.par
        projektname = self.projectname

        Gewerbesteuermessbetrag_Projekt = 0
        
        gewerbe_vorhanden = False
        gewerbe_messbetrag = 0
        einzelhandel_vorhanden = False
        einzelhandel_messbetrag = 0
        
        fields1 = ['Nutzungsart', 'id_teilflaeche', 'ags_bkg']
        table_teilflaechen = self.folders.get_table('Teilflaechen_Plangebiet', "FGDB_Definition_Projekt.gdb")
        cursor1 = arcpy.da.SearchCursor(table_teilflaechen, fields1)
        for row1 in cursor1:
            ags = row1[2]
            ags2 = ags[0:2]
            if teilflaeche[0] == Nutzungsart.GEWERBE:
                gewerbe_vorhanden = True
                Summe_Arbeitsplatzschaetzungen = 0
                fields2 = ['anzahl_jobs_schaetzung']
                table_gewerbeanteile = self.folders.get_table('Gewerbe_Anteile', "FGDB_Definition_Projekt.gdb")
                cursor2 = arcpy.da.SearchCursor(table_gewerbeanteile, fields2)
                for row2 in cursor2:
                    Summe_Arbeitsplatzschaetzungen += row2[0]
                    
                Reale_Summe_AP = 0
                fields3 = ['Arbeitsplaetze']
                table_arbeitsplaetze = self.folders.get_table('Gewerbe_Arbeitsplaetze', "FGDB_Definition_Projekt.gdb")
                cursor3 = arcpy.da.SearchCursor(table_arbeitsplaetze, fields3)
                for row3 in cursor3:
                    Summe_Arbeitsplatzschaetzungen += row3[0]
                    
                Korrekturfaktor_AP = Reale_Summe_AP / Summe_Arbeitsplatzschaetzungen
                
                fields4 = ['anzahl_jobs_schaetzung', 'branche']
                cursor4 = arcpy.da.SearchCursor(table_gewerbeanteile, fields4)
                for row4 in cursor4:
                    Messbetrag = 0
                    fields5 = ['AGS2', 'IDBranche', 'GewStMessbetrag_pro_Arbeitsplatz']
                    where1 = '"AGS2"' + "='" + ags2 + "'" + " AND " + '"IDBranche"' + "='" + row4[1] + "'"  
                    table_messbetrag_pro_ap = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "GewSt_Messbetrag_pro_Arbeitsplatz")
                    cursor5 = arcpy.da.SearchCursor(table_messbetrag_pro_ap, fields5, where1)
                    for branche in cursor5:
                        Messbetrag_pro_Arbeitsplatz = branche[2] 
                    
                    Messbetrag = cursor4[0] * Korrekturfaktor_AP * Messbetrag_pro_Arbeitsplatz
                    gewerbe_messbetrag += Messbetrag
                                
            if teilflaeche[0] == Nutzungsart.EINZELHANDEL:
                einzelhandel_vorhanden = True
                fields6 = ['Verkaufsflaeche_qm', 'ID_Teilflaeche', 'IDSortiment']
                where2 = '"ID_Teilflaeche"' + "='" + row1[1] + "'"
                table_verkaufsflaechen = self.folders.get_table('Einzelhandel_Verkaufsflaechen', "FGDB_Definition_Projekt.gdb")
                cursor6 = arcpy.da.SearchCursor(table_verkaufsflaechen, fields6, where2)
                for row6 in cursor6:
                    Messbetrag = 0
                    verkaufsflaeche = row6[0]

                    fields7 = ['GewStMessbetrag_pro_qm_Verkaufsflaeche', 'ID_Sortiment']
                    where3 = '"ID_Sortiment"' + "='" + row6[2] + "'"
                    table_messbetrag_pro_qm = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "GewSt_Messbetrag_und_SvB_pro_qm_Verkaufsflaeche")
                    cursor7 = arcpy.da.SearchCursor(table_messbetrag_pro_qm, fields7, where3)
                    for row7 in cursor7:
                        messbetrag_pro_qm =row7[0]
                    
                    Messbetrag = verkaufsflaeche * messbetrag_pro_qm
                    einzelhandel_messbetrag += Messbetrag
        
        Gewerbesteuermessbetrag_Projekt = gewerbe_messbetrag + einzelhandel_messbetrag
        
        SvB_Branchen = 0
        if gewerbe_vorhanden:
            fields = ['Arbeitsplaetze']
            table_arbeitsplaetze = self.folders.get_table('Gewerbe_Arbeitsplaetze', "FGDB_Definition_Projekt.gdb")
            cursor = arcpy.da.SearchCursor(table_arbeitsplaetze, fields)
            for gewerbe in cursor:
                SvB_Branchen += gewerbe[0]
            
        SvB_Verkaufsflaechen = 0
        if einzelhandel_vorhanden:
            fields = ['Verkaufsflaeche_qm', 'IDSortiment']
            cursor = arcpy.da.SearchCursor(table_verkaufsflaechen, fields)
            for verkaufsflaeche in cursor:
                fields2 = ['SvB_pro_qm_Verkaufsflaeche', 'ID_Sortiment']
                where2 = '"ID_Sortiment"' + "='" + verkaufsflaeche[1] + "'"
                cursor2 = arcpy.da.SearchCursor(table_messbetrag_pro_qm, fields2, where2)
                for row in cursor2:
                    SvB_Verkaufsflaechen += verkaufsflaeche[0] * row[0]
                
        Bewerbesteuermessbetrag_pro_SvB_Projekt = Gewerbesteuermessbetrag_Projekt / (SvB_Branchen + SvB_Verkaufsflaechen)
        
        table_bilanzen = self.folders.get_table("Gemeindebilanzen", "FGDB_Einnahmen.gdb")
        fields = ["AGS", "GewSt", "Hebesatz_GewSt", "SvB_Saldo"]        
        cursor = arcpy.da.UpdateCursor(table_bilanzen, fields)
        for row in cursor:
            if row[0] == ags:
                row[1] = Bewerbesteuermessbetrag_pro_SvB_Projekt * (row[2] / 100) * (row[3] + SvB_Verkaufsflaechen) / (SvB_Branchen + SvB_Verkaufsflaechen)
            else:
                row[1] = Bewerbesteuermessbetrag_pro_SvB_Projekt * (row[2] / 100) * row[3] / (SvB_Branchen + SvB_Verkaufsflaechen)
            cursor.updateRow(row)

        c.set_chronicle("Gewerbesteuer", self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=projektname))

