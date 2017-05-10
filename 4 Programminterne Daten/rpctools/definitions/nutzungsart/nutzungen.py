# -*- coding: utf-8 -*-

from rpctools.utils.params import Tool
import arcpy
import pandas as pd

class Nutzungen(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):        
        """"""
        
    def update_wege_flaeche(self, flaechen_id, ways, ways_miv): 
        wege_col = 'Wege_gesamt'
        wege_miv_col = 'Wege_MIV'
        flaechen_table = 'Teilflaechen_Plangebiet'
        flaechen_id_col = 'id_teilflaeche'
        self.parent_tbx.update_table(
            flaechen_table,
            column_values={wege_miv_col: ways_miv.sum(),
                           wege_col: ways.sum()}, 
            where='{} = {}'.format(flaechen_id_col, flaechen_id)
        )
        
    def update_wege_projekt(self):
        '''updates the table "Wege_je_Nutzung" by summing up the calculated
        ways for all areas with Nutzungsart defined for toolbox'''
        flaechen_table = 'Teilflaechen_Plangebiet'
        flaechen_id_col = 'id_teilflaeche'
        wege_table = 'Wege_je_Nutzung'
        
        nutzungsart = self.parent_tbx._nutzungsart
        flaechen_df = self.parent_tbx.table_to_dataframe(
            flaechen_table, columns=['Wege_gesamt', 'Wege_MIV'],
            where='Nutzungsart={}'.format(nutzungsart))
        ways_sum = flaechen_df['Wege_gesamt'].sum()
        ways_miv_sum = flaechen_df['Wege_MIV'].sum()
        pkw_anteil = (float(ways_miv_sum) / ways_sum) * 100 if ways_sum > 0 else 0
        self.parent_tbx.upsert_row_in_table(
            wege_table, 
            {'Wege_gesamt': ways_sum,
             'PKW_Anteil': pkw_anteil},
            {'Nutzungsart': nutzungsart}, 
            workspace='FGDB_Verkehr.gdb')
        
        
class NutzungenWohnen(Nutzungen):

    def run(self):
        """"""
        self.calculate_we_ways()
        self.update_wege_projekt()
        
    def calculate_we_ways(self):        
        tbx = self.parent_tbx
    
        # table and column names        
        wohnen_we_table = 'Wohnen_WE_in_Gebaeudetypen'
        geb_typ_table = 'Wohnen_Gebaeudetypen'
        flaechen_table = 'Teilflaechen_Plangebiet'
        wohnen_struct_table = 'Wohnen_Struktur_und_Alterung_WE'
        project_table = 'Projektrahmendaten'        
        geb_typ_col = 'IDGebaeudetyp'
        ew_col = 'EW_je_WE'
        reference_col = 'Ew_pro_WE_Referenz'
        cor_factor_col = 'Korrekturfaktor_EW'
        we_col = 'WE'
        wege_je_ew_col = 'Wege_je_Einwohner'
        pkw_perc_col = 'Anteil_Pkw_Fahrer'
        pkey =  'OBJECTID'
        id_flaeche_col = 'IDTeilflaeche'
    
        # get all required tables as dataframes
        wohnen_we_df = tbx.table_to_dataframe(
            wohnen_we_table, columns=[pkey, ew_col, geb_typ_col,
                                      cor_factor_col, we_col,
                                      id_flaeche_col])
        
        geb_typ_df = tbx.table_to_dataframe(
            geb_typ_table, workspace='FGDB_Definition_Projekt_Tool.gdb',
                    columns=[geb_typ_col, reference_col, wege_je_ew_col,
                             pkw_perc_col],
                    is_base_table=True)
        
        ### Korrekturfaktoren ###
        
        arcpy.AddMessage('Berechne Korrekturfaktoren...')
        
        
        joined = pd.merge(wohnen_we_df, geb_typ_df, on=geb_typ_col)
        joined[cor_factor_col] = (joined[ew_col] /
                                  joined[reference_col])
        
        tbx.dataframe_to_table(wohnen_we_table,
                               joined[[pkey, cor_factor_col]],
                               [pkey])
        
        ### Calculate ways ###
        
        arcpy.AddMessage('Berechne Anzahl der Wege...')
        
        grouped = joined.groupby(id_flaeche_col)
        for g in grouped:
            group = g[1]
            flaechen_id = group[id_flaeche_col].unique()[0]
            n_ew = group[ew_col] * group[we_col]
            n_ways = n_ew * group[wege_je_ew_col]
            n_ways_miv = n_ways * group[pkw_perc_col] / 100
            self.update_wege_flaeche(flaechen_id, n_ways.sum(), n_ways_miv.sum())
        
        ### Structure and age ###
        
        arcpy.AddMessage('Berechne Wohneinheiten...')
        # empty the table
        tbx.delete_rows_in_table(wohnen_struct_table)
        # empty now, but easier to allocate all fields this way
        wohnen_struct_df = tbx.table_to_dataframe(wohnen_struct_table)
        # calc. structure grouped by flaechen id
        grouped_we = wohnen_we_df.groupby(id_flaeche_col)
        end = tbx.query_table(project_table,
                              columns=['Ende_Betrachtungszeitraum'])[0][0]
        for g in grouped_we:
            wohnen_ew_group = g[1]
            flaechen_id = wohnen_ew_group[id_flaeche_col].unique()[0]
            begin, duration = tbx.query_table(
                flaechen_table,
                columns=['Beginn_Nutzung', 'Aufsiedlungsdauer'],
                where='id_teilflaeche={}'.format(flaechen_id))[0]
            flaechen_template = pd.DataFrame()
            geb_types = wohnen_ew_group[geb_typ_col].values
            flaechen_template[geb_typ_col] = geb_types            
            flaechen_template[id_flaeche_col] = flaechen_id
            flaechen_template['Wohnungen'] = (
                wohnen_ew_group[we_col].values.astype(float) / duration)
            for j in range(begin, end + 1):
                for i in range(1, duration + 1):
                    if j - begin + i - duration + 1 > 0:
                        df = flaechen_template.copy()
                        df['Jahr'] = j
                        df['AlterWE'] = j - begin + i - duration + 1
                        wohnen_struct_df = wohnen_struct_df.append(df)
        # is ignored anyway
        #wohnen_struct_df[pkey] = range(1, len(wohnen_struct_df) + 1)
        tbx.insert_dataframe_in_table(wohnen_struct_table, wohnen_struct_df)
        

class NutzungenGewerbe(Nutzungen):
    
    def run(self):
        self.calculate_ways()
        self.update_wege_projekt()
        
    def calculate_ways(self):
        pkw_perc_col = 'Anteil_Pkw_Fahrer'
        id_branche_col = 'ID_Branche_ProjektCheck'
        wege_je_besch_col = u'Wege_je_Beschäftigten'
        flaechen_table = 'Teilflaechen_Plangebiet'
        branchen_table = 'Gewerbe_Branchen'
        id_flaeche_col = 'IDTeilflaeche'
        n_jobs_col = 'anzahl_jobs_schaetzung'
        
        arcpy.AddMessage('Berechne Anzahl der Wege...')
        
        gew_tablename = self.parent_tbx.tablename
        
        gew_table_df = self.parent_tbx.table_to_dataframe(gew_tablename)
        gew_table_df.rename(columns={'IDBranche': id_branche_col}, inplace=True)
        branchen_table_df = self.parent_tbx.table_to_dataframe(
            branchen_table, workspace='FGDB_Definition_Projekt_Tool.gdb',
            is_base_table=True)
        
        joined = gew_table_df.merge(branchen_table_df, on=id_branche_col,
                                    how='inner')
        
        grouped = joined.groupby(by=id_flaeche_col)
        for g in grouped:
            group = g[1]
            flaechen_id = group[id_flaeche_col].unique()[0]
            n_ways = group[n_jobs_col] * group[wege_je_besch_col]
            n_ways_miv = n_ways * group[pkw_perc_col] / 100
            self.update_wege_flaeche(flaechen_id, n_ways.sum(), n_ways_miv.sum())

        
class NutzungenEinzelhandel(Nutzungen):
    
    def run(self):
        self.calculate_ways()
        self.update_wege_projekt()
        
    def calculate_ways(self): 
        besucher_sqm_col = 'Besucher_je_qm_Vfl'
        pkw_perc_col = 'Anteil_Pkw_Fahrer'
        id_sort_col = 'IDSortiment'
        vfl_col = 'Verkaufsflaeche_qm'
        wege_je_besucher_col = 'Wege_je_Besucher'
        id_flaeche_col = 'IDTeilflaeche'
        
        arcpy.AddMessage('Berechne Anzahl der Wege...')
        
        vfl_tablename = self.parent_tbx.tablename
        sortimente_tablename = 'Einzelhandel_Sortimente'
        
        vfl_table_df = self.parent_tbx.table_to_dataframe(vfl_tablename)
        sortimente_df = self.parent_tbx.table_to_dataframe(
            sortimente_tablename, workspace='FGDB_Definition_Projekt_Tool.gdb',
            is_base_table=True)
        # column names of the ids differ -> rename one of them
        sortimente_df.rename(
            columns={'ID_Sortiment_ProjektCheck': id_sort_col}, inplace=True)        
        joined = vfl_table_df.merge(sortimente_df, on=id_sort_col,
                                    how='inner')
        
        grouped = joined.groupby(by=id_flaeche_col)
        for g in grouped:
            group = g[1]
            flaechen_id = group[id_flaeche_col].unique()[0]
            n_ways = (group[vfl_col] *
                      group[besucher_sqm_col] *
                      group[wege_je_besucher_col])
            n_ways_miv = n_ways * group[pkw_perc_col] / 100
            self.update_wege_flaeche(flaechen_id, n_ways.sum(), n_ways_miv.sum())
