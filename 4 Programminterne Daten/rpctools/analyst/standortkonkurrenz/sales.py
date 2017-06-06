from rpctools.utils.config import Folders, Config
from rpctools.utils.spatial_lib import clip_raster
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point
from rpctools.utils.params import DummyTbx

import arcpy
import os
import numpy as np
import pandas as pd

class Sales(object):
    NULLFALL = 0
    PLANFALL = 1

    def __init__(self, df_distances, df_markets, df_zensus):

        self.distances = df_distances
        self.markets = df_markets
        self.zensus = df_zensus
        self.tbx = DummyTbx()
        
    def calculate_nullfall(self):
        return self._calculate_sales(self.NULLFALL)

    def calculate_planfall(self):
        return self._calculate_sales(self.PLANFALL)
        
    def _calculate_sales(self, setting):
        df_markets = self._prepare_markets(self.markets, setting)
        df_markets.set_index('id', inplace=True) 
        #df_markets.sort(columns='id', inplace=True)
        #dist_matrix = self.get_dist_matrix().sort()
        ## dist_matrix and df_markets should have same market-ids
        #assert (df_markets['id'] != dist_matrix.index).sum() == 0
        
        ## Hochzahl * Reisezeit
        #attraction_matrix = dist_matrix.mul(df_markets['exponent'].values[0],
                                            #axis=0)
                                            
        # no exp. over whole matrix -> row-wise instead
        
        df_kk = pd.DataFrame()
        df_kk['id_siedlungszelle'] = self.zensus['id']
        df_kk['kk'] = self.zensus['kk']
        kk_merged = self.distances.merge(df_kk, on='id_siedlungszelle')
        
        kk_matrix = kk_merged.pivot(index='id_markt',
                                    columns='id_siedlungszelle',
                                    values='kk')
        
        dist_matrix = kk_merged.pivot(index='id_markt',
                                      columns='id_siedlungszelle',
                                      values='distanz')
        
        n_cells = len(np.unique(self.distances['id_siedlungszelle']))
        
        attraction_matrix = pd.DataFrame(data=np.zeros(dist_matrix.shape),
                                         index=dist_matrix.index, 
                                         columns=dist_matrix.columns)
        
        for index, market in df_markets.iterrows():
            distances = dist_matrix.loc[index]
            factor = market['exp_faktor']
            exponent = market['exponent']
            attraction_matrix.loc[index] = factor * np.exp(distances * exponent)
        
        probabilities = attraction_matrix / attraction_matrix.sum(axis=0)
        kk_flow = probabilities * kk_matrix
        
        return kk_flow
        
    def get_dist_matrix(self):
        # Dataframe for distances
        dist_matrix = self.distances.pivot(index='id_markt',
                                           columns='id_siedlungszelle',
                                           values='distanz')
        return dist_matrix    

    def _prepare_markets(self, df_markets, setting):
        """
        setting - nullfall or planfall
        """
        base_ws = 'FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb'
        betriebstyp_col = 'id_betriebstyp_nullfall' \
            if setting == self.NULLFALL else 'id_betriebstyp_planfall'
        
        # ignore markets that don't exist yet resp. are closed
        df_markets = df_markets[df_markets[betriebstyp_col] != 0]
    
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






