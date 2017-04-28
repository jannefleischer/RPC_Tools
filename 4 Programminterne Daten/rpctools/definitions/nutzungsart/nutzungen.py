# -*- coding: utf-8 -*-

from rpctools.utils.params import Tool
import arcpy
import pandas as pd

class Nutzungen(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        """"""

class NutzungenWohnen(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        """"""
        
        self.commit_correction_factors()
        
    def commit_correction_factors(self):
        tbx = self.parent_tbx
        geb_typ_col = 'IDGebaeudetyp'
        ew_col = 'EW_je_WE'
        reference_col = 'Ew_pro_WE_Referenz'
        cor_factor_col = 'Korrekturfaktor_EW'
        pkey =  'OBJECTID'
        project_table = 'Wohnen_WE_in_Gebaeudetypen'
        base_table = 'Wohnen_Gebaeudetypen'
        
        dataframe = tbx.table_to_dataframe(project_table,
                                           columns=[pkey, ew_col, geb_typ_col,
                                                    cor_factor_col])
        
        reference = tbx.table_to_dataframe(
            base_table, workspace='FGDB_Definition_Projekt_Tool.gdb',
            columns=[geb_typ_col, reference_col], is_base_table=True)
        
        join = pd.merge(dataframe, reference, on=geb_typ_col)
        join[cor_factor_col] = (join[ew_col] /
                                join[reference_col])
        
        tbx.dataframe_to_table(project_table,
                               join[[pkey, cor_factor_col]],
                               [pkey])
        
        print
        #self.parent_tbx.query_table('Wohnen_Gebaeudetypen', )
        
class Calculations():
    @staticmethod
    def calc_correction_factors(dataframe, reference):
        pass