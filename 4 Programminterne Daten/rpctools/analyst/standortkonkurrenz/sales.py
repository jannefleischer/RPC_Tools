from rpctools.utils.config import Folders, Config
from rpctools.utils.spatial_lib import clip_raster
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point
from rpctools.utils.params import DummyTbx

import arcpy
import os
import numpy as np

class Sales(object):
    NULLFALL = 0
    PLANFALL = 1

    def __init__(self, df_distances, df_markets):

        self.distances = df_distances
        self.markets = df_markets
        self.tbx = DummyTbx()        
        
    def calculate_attractivity(self):
        df_markets = self.prepare_markets(self.markets, self.NULLFALL)
        print()

    def prepare_markets(self, df_markets, setting):
        """
        setting - nullfall or planfall
        """
        base_ws = 'FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb'
        betriebstyp_col = 'id_betriebstyp_nullfall' \
            if setting == self.NULLFALL else 'id_betriebstyp_planfall'
    
        df_communities = self.tbx.table_to_dataframe(
            table_name='bkg_gemeinden',
            columns=['AGS', 'groessenklasse'],
            workspace='FGDB_Basisdaten_deutschland.gdb',
            is_base_table=True)
        
        # add groessenklassen to markets
        df_markets = df_markets.merge(df_communities, on='AGS')
        
        # dataframe for exponential parameters
        df_exponential_parameters = self.tbx.table_to_dataframe(
            table_name='Exponentialfaktoren',
            columns=['gem_groessenklasse', 'id_kette', 'id_betriebstyp',
                     'exponent', 'exp_faktor'],
            workspace=base_ws, is_base_table=True)
        
        df_attractivity_factors = self.tbx.table_to_dataframe(
            table_name='Attraktivitaetsfaktoren',
            workspace=base_ws, is_base_table=True)
        
        attractivity_cols = ['ein_Markt_in_Umkreis', 'zwei_Maerkte_in_Umkreis',
                             'drei_Maerkte_in_Umkreis',
                             'zweiter_Markt_mit_Abstand_zum_ersten',
                             'dritter_Markt_mit_Abstand_zum_ersten',
                             'dritter_Markt_mit_Abstand_zum_ersten_und_zweiten']
        
        # add columns to markets
        df_markets['exponent'] = 0
        df_markets['exp_faktor'] = 0
        for col in attractivity_cols:
            df_markets[col] = 0
        
        # add the parameters to markets
        for index, market in df_markets.iterrows():
            gr_klasse = market['groessenklasse']
            id_kette = market['id_kette']
            id_betriebstyp = market[betriebstyp_col]
            
            def get_entry_idx(df, id_kette, id_betriebstyp):
                '''look up for an entry in given df and return index
                (default if special one not found),
                scheme is the same for tables attractivity and exp. factors'''
                # look for entry of combination kette/betriebstyp
                idx = np.logical_and(
                    df['id_kette'] == id_kette,
                    df['id_betriebstyp'] == id_betriebstyp)
                # take the default entry for kette if combination is not found
                if idx.sum() == 0:
                    idx = np.logical_and(
                        df['id_kette'] == 0,
                        df['id_betriebstyp'] == id_betriebstyp)
                return idx
            
            # exp. factors            
            df_exp_gr_klasse = df_exponential_parameters[
                df_exponential_parameters['gem_groessenklasse'] == gr_klasse]            
            idx = get_entry_idx(df_exp_gr_klasse, id_kette, id_betriebstyp)
            entry = df_exp_gr_klasse[idx]
            df_markets.loc[index, 'exponent'] = entry['exponent'].values[0]
            df_markets.loc[index, 'exp_faktor'] = entry['exp_faktor'].values[0]
            
            # attractivity
            idx = get_entry_idx(df_attractivity_factors,
                                id_kette, id_betriebstyp)
            entry = df_attractivity_factors[idx]
            for col in attractivity_cols:
                df_markets.loc[index, col] = entry[col].values[0]
            
        
        # adapt column names of df_exponential_parameters to df_markets
        # for merge
        df_exponential_parameters.columns = ['groessenklasse', 'id_kette',
                                             'id_betriebstyp_nullfall',
                                             'exponent', 'exp_faktor']

        return df_markets    






