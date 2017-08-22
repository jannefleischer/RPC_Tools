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
from rpctools.utils.spatial_lib import get_ags, extent_to_bbox
from rpctools.analyst.standortkonkurrenz.osm_einlesen import (OSMShopsReader,
                                                              Point)


class MarktEinlesen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
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

    def markets_to_db(self, supermarkets, tablename='Maerkte', truncate=False, planfall=False, is_buffer=False):
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
            'is_buffer'
        ]
        table = self.folders.get_table(tablename)
        # remove results as well (distances etc.)
        res_table = self.folders.get_table('Beziehungen_Maerkte_Zellen')

        # delete markets of nullfall and ALL results (easiest way)
        if truncate:
            self.parent_tbx.delete_rows_in_table(
                tablename, where='id_betriebstyp_nullfall > 0')
            arcpy.TruncateTable_management(self.folders.get_table(res_table))

        df = self.parent_tbx.table_to_dataframe('Maerkte')
        max_id = df['id'].max() if len(df) > 0 else 0

        with arcpy.da.InsertCursor(table, columns) as rows:
            for i, markt in enumerate(supermarkets):
                id_nullfall = 0 if planfall else markt.id_betriebstyp
                if markt.name is None:
                    continue
                markt.create_geom()
                if markt.geom:
                    rows.insertRow((
                        markt.name,
                        id_nullfall,
                        markt.id_betriebstyp,
                        markt.id_kette,
                        markt.geom,
                        markt.id_teilflaeche,
                        max_id + i + 1,
                        markt.adresse,
                        int(is_buffer)
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

    def set_betriebstyp_vkfl(self, markets):
        """
        use the name of the chain of the markets to parse and assign
        chain-ids and betriebstyps
        """
        df_chains = self.parent_tbx.table_to_dataframe(
            'Ketten',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        df_bt = self.parent_tbx.table_to_dataframe(
            'Betriebstypen',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        df_bt.fillna(sys.maxint, inplace=True)
        for market in markets:
            if market.id_kette > 0:
                idx = df_chains['id_kette'] == market.id_kette
                is_discounter = df_chains[idx]['discounter'].values[0]
            else:
                market.id_kette = 0
                is_discounter = 0
            if is_discounter:
                market.id_betriebstyp = 7
            elif market.vkfl is not None:
                fit_idx = ((df_bt['von_m2'] <= market.vkfl) &
                           (df_bt['bis_m2'] > market.vkfl))
                if fit_idx.sum() > 0:
                    market.id_betriebstyp = df_bt[fit_idx]['id_betriebstyp'].values[0]
        return markets

    def parse_meta(self, markets, field='name'):
        """
        use the name of the markets to parse and assign chain-ids and
        betriebstyps
        """

        df_chains_alloc = self.parent_tbx.table_to_dataframe(
            'Ketten_Zuordnung',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True)
        df_chains_alloc.sort(columns='prioritaet', ascending=False)

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
            for idx, chain_alloc in df_chains_alloc.iterrows():
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
            # add markets that didn't match (keep defaults)
            if not match_found:
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
    _markets_table_tmp = 'Maerkte_tmp'
    _markets_in_communities = 'Maerkte_in_Gemeinden'
    _markets_buffer = 'Maerkte_Puffer'
    _markets_boundary = 'Maerkte_Randbedingung'
    _selected_communities = "Ausgewaehlte_Gemeinden"
    def run(self):

        tbx = self.parent_tbx
        # paths
        markets_path = tbx.folders.get_table(self._markets_table,
                                             workspace=self._workspace)
        markets_boundary_path = tbx.folders.get_table(self._markets_boundary,
                                             workspace=self._workspace)
        tmp_markets_path = tbx.folders.get_table(self._markets_table_tmp,
                                             workspace=self._workspace)
        buffer_path = tbx.folders.get_table(self._markets_buffer,
                                             workspace=self._workspace)
        markets_in_communities_path = tbx.folders.get_table(self._markets_in_communities,
                                             workspace=self._workspace)
        selected_communities_path = tbx.folders.get_table(
            self._selected_communities, workspace=self._workspace)
        # calc. center of areas
        flaechen_df = tbx.table_to_dataframe(
            'Teilflaechen_Plangebiet',
            columns=['INSIDE_X', 'INSIDE_Y'],
            workspace='FGDB_Definition_Projekt.gdb')
        x = flaechen_df['INSIDE_X'].mean()
        y = flaechen_df['INSIDE_Y'].mean()

        epsg = tbx.config.epsg
        centroid = Point(x, y, epsg=epsg)
        arcpy.AddMessage('Sende Standortanfrage an Geoserver...')
        reader = OSMShopsReader(epsg=epsg)
        markets = reader.get_shops(count=self.par.count.value)
        arcpy.AddMessage(u'{} Märkte gefunden'.format(len(markets)))
        arcpy.AddMessage(u'Analysiere gefundene Märkte...'
                         .format(len(markets)))
        truncate = self.par.truncate.value
        markets = self.parse_meta(markets)
        arcpy.AddMessage(u'Schreibe {} Märkte in die Datenbank...'
                         .format(len(markets)))
        tbx.delete_rows_in_table(self._markets_table, where='is_buffer=1')
        arcpy.Copy_management(markets_path, markets_boundary_path)
        tbx.delete_rows_in_table(markets_boundary_path)
        self.markets_to_db(markets,
                           tablename=self._markets_boundary,
                           truncate=truncate,
                           is_buffer=True)

        arcpy.AddMessage(u'Aktualisiere die AGS der Märkte...')
        self.set_ags()
        # only markets in buffer zone


        arcpy.Clip_analysis(markets_boundary_path, buffer_path,
                            tmp_markets_path)
        #arcpy.Delete_management(markets_path)
        arcpy.Clip_analysis(tmp_markets_path, selected_communities_path, markets_in_communities_path)
        cursor = arcpy.da.SearchCursor(markets_in_communities_path, ['id'],
                                       where_clause='is_buffer=1')
        in_com_ids = [str(id) for id, in cursor]
        del(cursor)
        where = 'id IN ({})'.format(','.join(in_com_ids))
        tbx.delete_rows_in_table(tmp_markets_path, where)
        tbx.delete_rows_in_table(self._markets_table, where='is_buffer=1')
        arcpy.Delete_management(markets_path)
        arcpy.Rename_management(in_data=tmp_markets_path,
                                out_data=markets_path)
        arcpy.Delete_management(markets_boundary_path)
        arcpy.Delete_management(markets_in_communities_path)



class TbxOSMMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'OpenStreetMap anfragen')

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

        #param = self.add_parameter('radius')
        #param.name = encode(u'Radius')
        #param.displayName = encode(u'Maximale Entfernung der '
                                   #u'Märkte vom Plangebiet in Kilometern')
        #param.parameterType = 'Required'
        #param.direction = 'Input'
        #param.datatype = u'GPLong'
        #param.filter.type = 'Range'
        #param.filter.list = [1, 100]
        #param.value = 5

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
        param.displayName = encode(u'Vorhandene Märkte entfernen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'

        return params

    def _updateParameters(self, params):

        return params


if __name__ == '__main__':
    t = TbxOSMMarktEinlesen()
    t._getParameterInfo()
    t.par.truncate.value = True
    t.set_active_project()
    t.execute()
