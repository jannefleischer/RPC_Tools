# -*- coding: utf-8 -*-

from rpctools.utils.params import Tool
import arcpy
import pandas as pd

class Bewohner(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Bewohner_Arbeitsplaetze.gdb'

    def run(self):
        """"""
        tbx = self.parent_tbx
        
        # table and column names
        tfl = tbx.get_teilflaeche(self.par.teilflaeche.value)
        flaechen_id = tfl.flaechen_id
        bewohner_table = 'Bewohner_nach_Altersgruppe_und_Jahr'    
        wohnen_struct_table = 'Wohnen_Struktur_und_Alterung_WE'
        ew_base_table = 'Einwohner_pro_WE'
        flaechen_col = 'IDTeilflaeche'
        alter_we_col = 'AlterWE'
        geb_typ_col = 'IDGebaeudetyp'
        id_aclass_col = 'IDAltersklasse'
        aclass_col = 'Altersklasse'
        year_col = 'Jahr'
        ew_col = 'Einwohner'
        wohnungen_col = 'Wohnungen'
        n_bewohner_col = 'Bewohner'
        
        arcpy.AddMessage('Berechne Bewohnerzahl...')
        # empty the bewohner table (results will be stored there)
        tbx.delete_rows_in_table(bewohner_table)
    
        # get all required tables as dataframes        
        bewohner_df = tbx.table_to_dataframe(bewohner_table)
        
        ew_base_df = tbx.table_to_dataframe(
            ew_base_table, workspace='FGDB_Bewohner_Arbeitsplaetze_Tool.gdb',
            is_base_table=True)
        
        wohnen_struct_df = tbx.table_to_dataframe(
            wohnen_struct_table, pkey={flaechen_col: flaechen_id}, 
            workspace='FGDB_Definition_Projekt.gdb')
        
        if len(wohnen_struct_df) == 0:
            arcpy.AddError('Keine Definitionen gefunden.')
            return
        
        # corresponding SQL: Einwohner_pro_WE INNER JOIN 
        # Wohnen_Struktur_und_Alterung_WE ON 
        # (Einwohner_pro_WE.AlterWE = Wohnen_Struktur_und_Alterung_WE.AlterWE) 
        # AND (Einwohner_pro_WE.IDGebaeudetyp = 
        # Wohnen_Struktur_und_Alterung_WE.IDGebaeudetyp)
        joined = wohnen_struct_df.merge(ew_base_df, how='inner',
                                        on=[alter_we_col, geb_typ_col])
        
        # GROUP BY Wohnen_Struktur_und_Alterung_WE.IDTeilflaeche, 
        # Wohnen_Struktur_und_Alterung_WE.Jahr, Einwohner_pro_WE.IDAltersklasse, 
        # Einwohner_pro_WE.Altersklasse
        grouped = joined.groupby([year_col, id_aclass_col, aclass_col])
        
        # make an appendable copy of the (empty) bewohner dataframe
        group_template = bewohner_df.copy()
        # flaechen_id will be the same for all group entries
        group_template[flaechen_col] = [flaechen_id]
        
        # iterate the groups and set their number of inhabitants etc.
        for g in grouped:
            group = g[1]
            entry = group_template.copy()
            # corr. SQL:  Sum([Einwohner]*[Wohnungen])
            n_bewohner = (group[ew_col] * group[wohnungen_col]).sum()
            entry[n_bewohner_col] = [n_bewohner]
            entry[id_aclass_col] = group[id_aclass_col].unique()
            entry[aclass_col] = group[aclass_col].unique()
            entry[year_col] = group[year_col].unique()
            bewohner_df = bewohner_df.append(entry)            
        
        arcpy.AddMessage('Schreibe Bewohnerzahl...')        
        tbx.insert_dataframe_in_table(bewohner_table, bewohner_df)