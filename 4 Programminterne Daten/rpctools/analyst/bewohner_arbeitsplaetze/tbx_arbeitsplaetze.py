# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxFlaechendefinition
from rpctools.utils.params import Tool
from rpctools.utils.constants import Nutzungsart
from rpctools.utils.spatial_lib import get_gemeindetyp
from rpctools.diagrams.bewohner_arbeitsplaetze import (ArbeitsplatzEntwicklung,
                                                       BranchenAnteile)
import pandas as pd
import arcpy


class Arbeitsplaetze(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Bewohner_Arbeitsplaetze.gdb'

    def run(self):
        """"""
        tfl = self.parent_tbx.get_teilflaeche(self.par.teilflaeche.value)
        arcpy.AddMessage(u'Berechne Arbeitsplätze für die Teilfläche "{}"'
                         .format(tfl.name))
        self.calculate_growth(tfl)
        self.calculate_percentages(tfl)
        self.diagram(tfl)
        
    def calculate_growth(self, tfl): ### Structure and age ###
        flaechen_table = 'Teilflaechen_Plangebiet'
        project_table = 'Projektrahmendaten'
        jobs_year_table = 'AP_nach_Jahr'
        definition_workspace = 'FGDB_Definition_Projekt.gdb'
        
        arcpy.AddMessage('Berechne Wachstum...')
        
        tbx = self.parent_tbx
        flaechen_id = tfl.flaechen_id
    
        n_jobs = self.parent_tbx.query_table(
                'Gewerbe_Arbeitsplaetze', columns=['Arbeitsplaetze'], 
                workspace=definition_workspace)[0][0]
        
        begin, duration = tbx.query_table(
                flaechen_table,
                workspace=definition_workspace, 
                columns=['Beginn_Nutzung', 'Aufsiedlungsdauer'],
                where='id_teilflaeche={}'.format(flaechen_id))[0]
        
        end = tbx.query_table(project_table,
                              workspace=definition_workspace,
                              columns=['Ende_Betrachtungszeitraum'])[0][0]
    
        # empty the bewohner table (results will be stored there)
        tbx.delete_rows_in_table(jobs_year_table,
                                 where='IDTeilflaeche={}'.format(flaechen_id))
    
        for progress in range(0, end - begin + 1):
            proc_factor = (float(progress + 1) / duration
                           if progress + 1 <= duration
                           else 1)
            year = begin + progress
            
            tbx.insert_row_in_table(
                jobs_year_table,
                column_values={
                    'Jahr': year,
                    'AP': n_jobs * proc_factor, 
                    'IDTeilflaeche': flaechen_id
                }
            )
            
    def calculate_percentages(self, tfl):
        perc_table = 'Gewerbe_Anteile'
        perc_res_table = 'Branchenanteile'
        definition_workspace = 'FGDB_Definition_Projekt.gdb'
        
        tbx = self.parent_tbx
        flaechen_id = tfl.flaechen_id
    
        arcpy.AddMessage('Berechne Branchenanteile...')
        
        tbx.delete_rows_in_table(perc_res_table,
                                 where='IDTeilflaeche={}'.format(flaechen_id))
        
        perc_table_df = tbx.table_to_dataframe(
            perc_table, where='IDTeilflaeche={}'.format(flaechen_id),
            workspace=definition_workspace)
        
        perc_res_df = pd.DataFrame()
        perc_res_df['IDBranche'] = perc_table_df['IDBranche']
        perc_res_df['Anteil'] = (
            perc_table_df['dichtekennwert_ap_pro_ha_brutto'] *
            perc_table_df['anteil'])
        
        perc_res_df['Anteil'] /= perc_res_df['Anteil'].sum()
        perc_res_df['IDTeilflaeche'] = flaechen_id
        
        tbx.insert_dataframe_in_table(perc_res_table, perc_res_df)
        
    def diagram(self, tfl):
        diagram = ArbeitsplatzEntwicklung()
        diagram.create(flaechen_id=tfl.flaechen_id, flaechen_name=tfl.name)
        diagram.show()
        diagram = BranchenAnteile()
        diagram.create(flaechen_id=tfl.flaechen_id, flaechen_name=tfl.name)
        diagram.show()
        

class TbxArbeitsplaetze(TbxFlaechendefinition):
    _nutzungsart = Nutzungsart.GEWERBE

    @property
    def Tool(self):
        return Arbeitsplaetze

    @property
    def label(self):
        return u'Arbeitsplätze schätzen'

if __name__ == '__main__':
    t = TbxArbeitsplaetze()
    params = t.getParameterInfo()
    t.par.projectname.value = t.config.active_project
    t.tool.main(t.par, None)