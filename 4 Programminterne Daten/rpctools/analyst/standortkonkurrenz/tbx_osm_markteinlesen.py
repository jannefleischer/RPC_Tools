# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil
import re
import pandas as pd
import numpy as np

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_ags, minimal_bounding_poly, remove_duplicates
from rpctools.analyst.standortkonkurrenz.osm_einlesen import (OSMShopsReader,
                                                              Point)


class MarktEinlesen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
    
    def __init__(self, *args):
        super(MarktEinlesen, self).__init__(*args)

        self.df_chains = self.parent_tbx.table_to_dataframe(
            'Ketten',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        self.df_bt = self.parent_tbx.table_to_dataframe(
            'Betriebstypen',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        self.df_bt.fillna(sys.maxint, inplace=True)

        self.df_chains_alloc = self.parent_tbx.table_to_dataframe(
            'Ketten_Zuordnung',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        self.df_chains_alloc.sort(columns='prioritaet', ascending=False)

    def run(self):
        """"""

    def add_outputs(self):
        group_layer = ("standortkonkurrenz")
        fc = 'Maerkte'
        folder = 'Standortkonkurrenz'
        layer_nullfall = 'Märkte im Bestand'
        layer_changed = 'veränderte Märkte im Bestand'
        layer_planfall = 'geplante Märkte'

        self.output.add_layer(group_layer, layer_nullfall, fc,
                              template_folder=folder, zoom=False)
        self.output.add_layer(group_layer, layer_changed, fc,
                              template_folder=folder, zoom=False)
        self.output.add_layer(group_layer, layer_planfall, fc,
                              template_folder=folder, zoom=False)

        self.output.hide_layer('projektdefinition')

    def markets_to_db(self, supermarkets, tablename='Maerkte', truncate=False,
                      planfall=False, is_buffer=False, start_id=None,
                      is_osm=False):
        """Create the point-features for supermarkets"""
        sr = arcpy.SpatialReference(self.parent_tbx.config.epsg)

        columns = [
            'name',
            'id_betriebstyp_nullfall',
            'id_betriebstyp_planfall',
            'id_kette',
            'SHAPE@',
            'id_teilflaeche',
            'id',
            'adresse',
            'is_buffer',
            'is_osm',
            'vkfl',
            'adresse'
        ]
        table = self.folders.get_table(tablename)
        # remove results as well (distances etc.)
        res_table = self.folders.get_table('Beziehungen_Maerkte_Zellen')

        # delete markets of nullfall and ALL results (easiest way)
        if truncate:
            self.parent_tbx.delete_rows_in_table(
                tablename, where='id_betriebstyp_nullfall > 0')
            arcpy.TruncateTable_management(self.folders.get_table(res_table))

        if start_id is None:
            ids = [id for id, in self.parent_tbx.query_table('Maerkte', ['id'])]
            start_id = max(ids) + 1 if ids else 0

        with arcpy.da.InsertCursor(table, columns) as rows:
            for i, market in enumerate(supermarkets):
                id_nullfall = 0 if planfall else market.id_betriebstyp
                if market.name is None:
                    continue
                market.create_geom()
                # set sales area, if not set yet (esp. osm markets)
                vkfl = market.vkfl or self.betriebstyp_to_vkfl(market)
                if market.geom:
                    rows.insertRow((
                        market.name,
                        id_nullfall,
                        market.id_betriebstyp,
                        market.id_kette,
                        market.geom,
                        market.id_teilflaeche,
                        start_id + i,
                        market.adresse,
                        int(is_buffer),
                        int(is_osm),
                        vkfl, 
                        market.adresse
                    ))

    def set_ags(self):
        """
        Assign community size to supermarkets
        """
        markets = self.folders.get_table('Maerkte')
        ags = get_ags(markets, 'id')
        cursor = arcpy.da.UpdateCursor(markets, ['id', 'AGS'])
        for row in cursor:
            try:
                a = ags[row[0]]
            except:
                continue
            row[1] = a[0]
            cursor.updateRow(row)
        del cursor

    def vkfl_to_betriebstyp(self, markets):
        """
        set types of use (betriebstyp) matching the sales area (vkfl)
        of all given markets
        returns the markets with set types of use
        """
        for market in markets:
            if market.id_kette > 0:
                idx = self.df_chains['id_kette'] == market.id_kette
                is_discounter = self.df_chains[idx]['discounter'].values[0]
            else:
                market.id_kette = 0
                is_discounter = 0
            if is_discounter:
                market.id_betriebstyp = 7
            elif market.vkfl is not None:
                fit_idx = ((self.df_bt['von_m2'] <= market.vkfl) &
                           (self.df_bt['bis_m2'] > market.vkfl))
                if fit_idx.sum() > 0:
                    market.id_betriebstyp = self.df_bt[fit_idx]['id_betriebstyp'].values[0]
        return markets
    
    def betriebstyp_to_vkfl(self, market):
        """
        return the sales area (vkfl) matching the type of use (betriebstyp)
        of a single market
        """
        # some discounters have (since there is no specific betriebstyp and 
        # therefore no hint on possible vkfl for them)
        if market.id_betriebstyp == 7:
            default_vkfl = self.df_chains[
                self.df_chains['id_kette']==market.id_kette]
            if len(default_vkfl) != 0:
                vkfl = default_vkfl['default_vkfl'].values[0]
                return vkfl
        # all other vkfl are assigned via betriebstyp (+ unmatched discounters)
        idx = self.df_bt['id_betriebstyp'] == market.id_betriebstyp
        vkfl = self.df_bt[idx]['default_vkfl'].values[0]
        return vkfl

    def parse_meta(self, markets, field='name', known_only=False):
        """
        use the name of the markets to parse and assign chain-ids and
        betriebstyps
        
        known_only: str, optional
            only return markets that belong to known chains if True
        """

        ret_markets = []

        for market in markets:
            # no name -> nothing to parse
            name = getattr(market, field)
            try:
                name = str(name)
            except:
                pass
            if not name:
                arcpy.AddMessage(u'  - Markt mit fehlendem Attribut "{}" wird '
                                 u'übersprungen'.format(field))
                continue
            match_found = False
            for idx, chain_alloc in self.df_chains_alloc.iterrows():
                match_result = re.match(chain_alloc['regex'],
                                        name)
                if not match_result:
                    continue
                match_found = True
                id_kette = chain_alloc['id_kette']
                # don't add markets with id -1 (indicates markets that
                # don't qualify as supermarkets or discounters)
                if id_kette >= 0:
                    market.id_betriebstyp = chain_alloc['id_betriebstyp']
                    market.id_kette = id_kette
                    ret_markets.append(market)
                else:
                    arcpy.AddMessage(
                        u'  - Markt "{}" ist kein Lebensmitteleinzelhandel, '
                        u'wird übersprungen'.format(market.name))
                break
            # markets that didn't match (keep defaults)
            if not match_found:
                if known_only:
                    arcpy.AddMessage(
                        u'  - Markt "{}" gehört zu keiner bekannten Kette. '
                        u'wird übersprungen'.format(market.name))
                else:
                    ret_markets.append(market)
        return ret_markets

    def delete_area_market(self, id_area):
        '''delete the market corresponding to a planned area and the already
        calculated results for this market'''
        markets = self.folders.get_table('Maerkte')
        where = 'id_teilflaeche={}'.format(id_area)
        rows = self.parent_tbx.query_table(
            'Maerkte', columns=['id'], where=where)
        if not rows:
            return
        # delete all results (there should be only one market per area,
        # but iterate anyway if sth went wrong before)
        for row in rows:
            market_id = row[0]
            self.parent_tbx.delete_rows_in_table(
                'Beziehungen_Maerkte_Zellen',
                where='id_markt = {}'.format(market_id))
        # delete the market
        self.parent_tbx.delete_rows_in_table(
            'Maerkte', where=where)


class OSMMarktEinlesen(MarktEinlesen):
    _markets_table = 'Maerkte'

    def run(self):

        tbx = self.parent_tbx
        
        communities = self.folders.get_table('Zentren')
        multi_poly = minimal_bounding_poly(communities, where='"Auswahl"<>0')
        
        epsg = self.parent_tbx.config.epsg
        multi_poly = [[Point(p.X, p.Y, epsg=epsg) for p in poly if p]
                      for poly in multi_poly]
        
        epsg = tbx.config.epsg
        arcpy.AddMessage('Sende Standortanfrage an Geoserver...')
        reader = OSMShopsReader(epsg=epsg)
        truncate = self.par.truncate.value
        if truncate:
            n = tbx.delete_rows_in_table(self._markets_table, where='is_osm=1')
            arcpy.AddMessage(u'{} vorhandene OSM-Märkte gelöscht'.format(n))
        if self.par.count.value == 0:
            return
        
        markets = []
        for poly in multi_poly:
            m = reader.get_shops(poly, count=self.par.count.value-len(markets))
            markets += m
        arcpy.AddMessage(u'{} Märkte gefunden'.format(len(markets)))
        arcpy.AddMessage(u'Analysiere gefundene Märkte...'
                         .format(len(markets)))
        
        markets = self.parse_meta(markets, known_only=self.par.known_only.value)
        arcpy.AddMessage(u'Schreibe {} Märkte in die Datenbank...'
                         .format(len(markets)))
        self.markets_to_db(markets,
                           tablename=self._markets_table,
                           truncate=False,  # already truncated osm markets
                           is_buffer=False,
                           is_osm=True)

        arcpy.AddMessage('Entferne Duplikate...')
        n = remove_duplicates(self.folders.get_table(self._markets_table),
                              'id', match_field='id_kette', 
                              where='is_osm=1', distance=50)
        arcpy.AddMessage('{} Duplikate entfernt...'.format(n))
        arcpy.AddMessage(u'Aktualisiere die AGS der Märkte...')
        self.set_ags()


class TbxOSMMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'Märkte aus OpenStreetMap im Betrachtungsraum einlesen')

    @property
    def Tool(self):
        return OSMMarktEinlesen

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []

        param = self.add_parameter('count')
        param.name = encode(u'Anzahl')
        param.displayName = encode(u'Maximale Anzahl an '
                                   u'hinzuzufügenden Märkten')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [0, 5000]
        param.value = 1000

        param = self.add_parameter('truncate')
        param.name = encode(u'truncate')
        param.displayName = encode(u'Vorhandene OSM-Märkte entfernen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'
    
        param = self.add_parameter('known_only')
        param.name = encode(u'known_only')
        param.displayName = encode(u'Nur Märkte großer Ketten hinzufügen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'
        param.value = True

        return params

    def _updateParameters(self, params):

        return params


if __name__ == '__main__':
    t = TbxOSMMarktEinlesen()
    t._getParameterInfo()
    t.par.truncate.value = True
    t.set_active_project()
    t.execute()
