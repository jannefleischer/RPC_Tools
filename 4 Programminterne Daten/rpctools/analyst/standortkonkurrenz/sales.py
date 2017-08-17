# -*- coding: utf-8 -*-
from rpctools.utils.config import Folders, Config
from rpctools.utils.spatial_lib import clip_raster
from rpctools.utils.spatial_lib import Point
from rpctools.utils.params import DummyTbx

import arcpy
import os
import numpy as np
import pandas as pd


class Sales(object):
    NULLFALL = 0
    PLANFALL = 1
    # time to separate same markets into 'Umfeld' and 'Abstand'
    # example: cut_off_time = 5 min
    #          nearest market = 4 min drive -> 'Umfeld'
    #          second market = 7 min drive -> 'Umfeld'
    #          third market = 12 min drive -> 'Abstand'
    # Note: switched from times to km -> cutoff is > 1 km
    relation_dist = 1  # km

    def __init__(self, df_distances, df_markets, df_zensus, debug=False):

        self.distances = df_distances
        self.markets = df_markets
        self.zensus = df_zensus
        self.tbx = DummyTbx()
        self.debug = debug

    def calculate_nullfall(self):
        return self._calculate_sales(self.NULLFALL)

    def calculate_planfall(self):
        return self._calculate_sales(self.PLANFALL)

    def _calculate_sales(self, setting):
        df_markets = self._prepare_markets(self.markets, setting)
        df_markets.set_index('id', inplace=True)

        # drop rows with markets, that are not in the dataframe of markets
        # used for current settings
        # (e.g. planfall markets when current setting is nullfall)
        ids_not_in_df = np.setdiff1d(
            np.unique(self.distances['id_markt']), df_markets.index)
        distances = self.distances.drop(
            self.distances.index[np.in1d(self.distances['id_markt'],
                                         ids_not_in_df)])
        # calc with distances in kilometers
        distances['distanz'] /= 1000
        distances[distances < 0] = -1

        # in case of Nullfall take zensus points without planned areas
        if setting == self.NULLFALL:
            zensus = self.zensus[self.zensus['id_teilflaeche'] < 0]
        else:
            zensus = self.zensus

        df_kk = pd.DataFrame()
        df_kk['id_siedlungszelle'] = zensus['id']
        df_kk['kk'] = zensus['kk']
        kk_merged = distances.merge(df_kk, on='id_siedlungszelle')

        kk_matrix = kk_merged.pivot(index='id_markt',
                                    columns='id_siedlungszelle',
                                    values='kk')

        dist_matrix = kk_merged.pivot(index='id_markt',
                                      columns='id_siedlungszelle',
                                      values='distanz')
        dist_matrix = dist_matrix.fillna(0)

        n_cells = len(np.unique(distances['id_siedlungszelle']))
        attraction_matrix = pd.DataFrame(data=np.zeros(dist_matrix.shape),
                                         index=dist_matrix.index,
                                         columns=dist_matrix.columns)

        for index, market in df_markets.iterrows():
            dist = dist_matrix.loc[index]
            factor = market['exp_faktor']
            exponent = market['exponent']
            attraction_matrix.loc[index] = factor * np.exp(dist * exponent)

        unreachable = dist_matrix < 0
        attraction_matrix[unreachable] = 0
        competitor_matrix = self.calc_competitors(dist_matrix, df_markets)

        if self.debug:
            setting_str = 'Nullfall' if setting == self.NULLFALL else 'Planfall'
            arcpy.AddMessage('DEBUG: Schreibe Zwischenergebnisse')
            if setting == self.NULLFALL:
                self.write_intermediate_results(dist_matrix.transpose(),
                                                'debug_Distanzmatrix')
            self.write_intermediate_results(
                attraction_matrix.transpose(),
                u'debug_Attraktivität_{}'.format(setting_str))
            self.write_intermediate_results(
                competitor_matrix.transpose(),
                u'debug_KK_Anteile_{}'.format(setting_str))
            arcpy.AddMessage('DEBUG: Berechnung')

        # include competition between same market types in attraction_matrix
        attraction_matrix *= competitor_matrix.values

        probabilities = attraction_matrix / attraction_matrix.sum(axis=0)
        kk_flow = probabilities * kk_matrix
        kk_flow = kk_flow.fillna(0)

        if self.debug:
            arcpy.AddMessage('DEBUG: Schreibe weitere Zwischenergebnisse')
            self.write_intermediate_results(
                attraction_matrix.transpose(),
                u'debug_Verteilungsmassstab_erster_Schritt_{}'.format(setting_str))
            self.write_intermediate_results(
                probabilities.transpose(),
                u'debug_Verteilungsmassstab_zweiter_Schritt_{}'.format(setting_str))
            self.write_intermediate_results(
                kk_flow.transpose(),
                u'debug_Kaufkraftstroeme_{}'.format(setting_str))

        return kk_flow

    def write_intermediate_results(self, dataframe, table):
        self.tbx.insert_dataframe_in_table(
            table, dataframe.reset_index(),
            workspace='FGDB_Standortkonkurrenz_Supermaerkte.gdb',
            create=True)

    def calc_competitors(self, dist_matrix, df_markets):
        """
        account competition through other markets of the same brand
        """
        cut_off_time = self.relation_dist
        dist_matrix = dist_matrix.T
        dist_matrix = dist_matrix.mask(dist_matrix < 0)
        # TODO check here
        results = pd.DataFrame(data=1., index=dist_matrix.index,
                               columns=dist_matrix.columns)
        competing_markets = df_markets[['id_kette']]
        for id_kette in np.unique(competing_markets['id_kette']):
            markets_of_same_type = \
                competing_markets[competing_markets['id_kette'] == id_kette]
            if len(markets_of_same_type['id_kette']) == 1 or id_kette == 0:
                continue
            indices = list(markets_of_same_type.index)
            number_of_competing_markets = len(indices)
            same_type_dist_matrix = dist_matrix[indices]
            same_type_dist_ranking = same_type_dist_matrix.rank(axis=1)
            same_type_dist_matrix['Minimum'] = \
                same_type_dist_matrix.loc[:, indices].min(axis=1)
            # time differences between way to nearest market and other markets
            same_type_dist_matrix = same_type_dist_matrix.sub(
                same_type_dist_matrix['Minimum'], axis=0)
            del same_type_dist_matrix['Minimum']
            competition_factors = same_type_dist_matrix < cut_off_time
            competition_factors['Umkreis'] = competition_factors.sum(axis=1)
            competition_factors['Abstand'] = \
                number_of_competing_markets - competition_factors['Umkreis']
            for market_id in indices:
                # write data for near markets with:
                # -> 1 near market
                factor = df_markets.loc[market_id]['ein_Markt_in_Naehe']
                results.loc[(competition_factors[market_id]==True) & \
                            (competition_factors['Umkreis']==1), \
                            market_id] = factor
                # -> 2 near markets
                factor = df_markets.loc[market_id]['zwei_Maerkte_in_Naehe']
                results.loc[(competition_factors[market_id]==True) & \
                            (competition_factors['Umkreis']==2), \
                            market_id] = factor
                # -> more than 2 near markets
                factor = df_markets.loc[market_id]['drei_Maerkte_in_Naehe']
                results.loc[(competition_factors[market_id]==True) & \
                            (competition_factors['Umkreis']>2), \
                            market_id] = factor
                # write data for far markets with:
                # -> market is far; 1 near market exsists; no other far market
                factor = df_markets.loc[market_id]\
                    ['zweiter_Markt_mit_Abstand_zum_ersten']
                results.loc[(competition_factors[market_id]==False) & \
                            (competition_factors['Umkreis']==1) & \
                            (competition_factors['Abstand']==1), \
                            market_id] = factor
                # -> market is far; 1 near market exsists;
                # >1 far market exsists
                factor = df_markets.loc[market_id]\
                    ['dritter_Markt_mit_Abstand_zum_ersten']
                results.loc[(competition_factors[market_id]==False) & \
                            (competition_factors['Umkreis']==1) & \
                            (competition_factors['Abstand']>1), \
                            market_id] = factor
                # -> market is far; >1 near market exsists
                factor = df_markets.loc[market_id]\
                    ['dritter_Markt_mit_Abstand_zum_ersten_und_zweiten']
                results.loc[(competition_factors[market_id]==False) & \
                            (competition_factors['Umkreis']>1), \
                            market_id] = factor
            # if more than 3 markets: markets 4 to end set to 0
            # if market 3 and 4 have same distance: keep both
            results.loc[:, indices] = results.loc[:, indices].mask((same_type_dist_ranking > 3) | (same_type_dist_ranking.isnull()), 0.)
        # Return results in shape of dist_matrix
        return results.T

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

        attractivity_cols = ['ein_Markt_in_Naehe', 'zwei_Maerkte_in_Naehe',
                             'drei_Maerkte_in_Naehe',
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






