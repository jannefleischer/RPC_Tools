# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_closest_point
import numpy as np
import pandas as pd


class EditMarkets(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def run(self):
        markets_df = self.parent_tbx.markets_df
        delete_df = markets_df.loc[markets_df['do_delete'] == True]
        update_df = markets_df.loc[markets_df['do_delete'] == False]
        if len(delete_df) > 0:
            arcpy.AddMessage(u'Lösche Märkte')
        for idx, market in delete_df.iterrows():
            arcpy.AddMessage(u' - {}'.format(market['pretty']))
            self.parent_tbx.delete_rows_in_table(
                'Maerkte', where='id={}'.format(market['id']))
        arcpy.AddMessage(u'Schreibe Änderungen in Datenbank...')
        self.parent_tbx.dataframe_to_table('Maerkte', update_df,
                                           ['id'], upsert=False)
        arcpy.RefreshActiveView()


class TbxEditMarkets(Tbx):
    
    @property
    def label(self):
        return encode(u'Märkte bearbeiten')

    @property
    def Tool(self):
        return EditMarkets

    def _getParameterInfo(self):
        
        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
    
        param = self.add_parameter('markets')
        param.name = encode(u'Märkte')
        param.displayName = encode(u'Markt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
        
        param = self.add_parameter('name')
        param.name = encode(u'Name')
        param.displayName = encode(u'Name des Marktes')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        
        # Handelsketten
        
        self.chains_df = self.table_to_dataframe(
            'Ketten',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True
        )        
    
        param = self.add_parameter('chain')
        param.name = encode(u'Kette')
        param.displayName = encode(u'Handelskette')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = sorted(self.chains_df['name'].values.tolist())
        
        # Betriebstypen

        self.types_df = self.table_to_dataframe(
            'Betriebstypen',
            workspace='FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb',
            is_base_table=True
        )
        
        pretty_names = []
        for idx, typ in self.types_df.iterrows():
            details = ''
            lower = typ['von_m2']
            upper = typ['bis_m2']
            if not np.isnan(lower):
                details = u'(ab {} m²'.format(lower)
                if not np.isnan(upper):
                    details += u' bis {} m²'.format(upper)
                details += u' Verkaufsfläche)'
                details.replace('.', ',')
            pretty = u'{name} {details}'.format(name=typ['name'],
                                                details=details)
            pretty_names.append(pretty)
        self.types_df['pretty'] = pretty_names
    
        param = self.add_parameter('type_name')
        param.name = encode(u'Betriebstyp')
        param.displayName = encode(u'Betriebstyp')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = pretty_names
    
        param = self.add_parameter('do_delete')
        param.name = encode(u'Löschen')
        param.displayName = encode(u'Markt entfernen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'
        
        self.markets_df = []
        return self.par
    
    def add_market_to_db(self, name, coords): 
        df_markets = self.table_to_dataframe('Maerkte')
        if len(df_markets) == 0:
            new_id = 1
        else: 
            new_id = df_markets['id'].max() + 1
        columns = df_markets.columns
        new_market = pd.DataFrame(np.zeros((1, len(columns))), columns=columns)
        new_market['id'] = new_id
        new_market['name'] = name
        new_market['SHAPE'] = [coords]
        new_market['id_betriebstyp_nullfall'] = 1
        new_market['id_betriebstyp_planfall'] = 1
        self.insert_dataframe_in_table('Maerkte', new_market)
    
    def _open(self, params):
        self.markets_df = self.table_to_dataframe('Maerkte')
        self.markets_df['do_delete'] = False
        self.markets_df.sort(columns='id', inplace=True)
        if len(self.markets_df) == 0:
            return

        x, y = self.config.active_coord
        closest_idx = None
        if x and y:
            closest_idx, c = get_closest_point((x, y), self.markets_df['SHAPE'])
        
        pretty_names = []
        for idx, market in self.markets_df.iterrows():
            pretty = self.get_pretty_market_name(market)
            pretty_names.append(pretty)
        self.markets_df['pretty'] = pretty_names
        self.update_market_list(closest_idx)
        self.set_selected_market_inputs()
        
    def get_pretty_market_name(self, market):
        chain_name = self.chains_df['name'][
            self.chains_df['id_kette'] == market['id_kette']].values[0]
        typ_name = self.types_df['name'][
            self.types_df['id_betriebstyp'] == \
            market['id_betriebstyp_nullfall']].values[0]
        pretty = u'"{name}" ({id}) - {typ} ({chain})'.format(
            id=market['id'], name=market['name'], typ=typ_name, 
            chain=chain_name)
        if market['do_delete']:
            pretty += u' - WIRD ENTFERNT'
        return pretty
    
    def set_selected_market_inputs(self):
        market_idx = self.markets_df['pretty'] == self.par.markets.value
        market = self.markets_df.loc[market_idx]
        self.par.name.value = market['name'].values[0]
        chain_name = self.chains_df['name'][
            self.chains_df['id_kette'] == market['id_kette'].values[0]]
        self.par.chain.value = chain_name.values[0]        
        typ_pretty = self.types_df['pretty'][
            self.types_df['id_betriebstyp'] ==
            market['id_betriebstyp_nullfall'].values[0]]
        self.par.type_name.value = typ_pretty.values[0]
        do_delete = market['do_delete'].values[0]
        # strange: can't assign the bool of do_delete directly, arcpy is
        # ignoring it
        self.par.do_delete.value = True if do_delete else False
    
    def validate_inputs(self):
        if len(self.table_to_dataframe('Maerkte', columns=['id'])) == 0:
            msg = (u'Es sind keine Märkte vorhanden. '
                   u'Bitte lesen Sie zunächst Märkte ein oder fügen Sie '
                   u'sie manuell hinzu.')
            return False, msg
        return True, ''
        
    def update_market_list(self, idx=None):
        if idx is None:
            idx = self.par.markets.filter.list.index(
                self.par.markets.value) if self.par.markets.value else 0
        pretty = self.markets_df['pretty'].values.tolist()
        self.par.markets.filter.list = pretty
        self.par.markets.value = pretty[idx] if idx >= 0 else pretty[0]
        
    def _updateParameters(self, params):
        if len(self.markets_df) == 0:
            return
        market_idx = self.markets_df['pretty'] == self.par.markets.value

        if self.par.changed('name'):
            self.markets_df.loc[market_idx, 'name'] = self.par.name.value
            
        elif self.par.changed('chain'):
            id_chain = self.chains_df['id_kette'][
                self.chains_df['name'] == self.par.chain.value].values[0]
            self.markets_df.loc[market_idx, 'id_kette'] = id_chain
            
        elif self.par.changed('type_name'):
            id_typ = self.types_df['id_betriebstyp'][
                self.types_df['pretty'] == self.par.type_name.value].values[0]
            self.markets_df.loc[market_idx, 'id_betriebstyp_nullfall'] = id_typ
            self.markets_df.loc[market_idx, 'id_betriebstyp_planfall'] = id_typ
            
        elif self.par.changed('do_delete'):
            do_delete = self.par.do_delete.value
            self.markets_df.loc[market_idx, 'do_delete'] = do_delete
        
        # update the pretty names of the markets
            
        if (self.par.changed('name') or 
            self.par.changed('chain') or
            self.par.changed('type_name') or
            self.par.changed('do_delete')):
            i = np.where(market_idx == True)[0][0]
            pretty = self.get_pretty_market_name(
                self.markets_df.iloc[i])
            self.markets_df.loc[market_idx, 'pretty'] = pretty
            self.update_market_list()
            
        if self.par.changed('markets'):
            self.set_selected_market_inputs()
        return params

    def _updateMessages(self, params):
        valid, msg = self.validate_inputs()
        if not valid:
            self.par.projectname.setErrorMessage(msg)

if __name__ == '__main__':
    t = TbxEditMarkets()
    t._getParameterInfo()
    t.set_active_project()
    t._open(None)
    t._updateParameters(None)
    t.execute()
