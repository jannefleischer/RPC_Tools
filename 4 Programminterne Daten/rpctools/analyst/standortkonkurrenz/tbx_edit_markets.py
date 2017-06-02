# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
import numpy as np


class EditMarkets(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def run(self):
        # ToDo: remove marked markets
        pass


class TbxEditMarkets(Tbx):
    _deletion_flag = u' - WIRD GELÖSCHT'

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
    
        param = self.add_parameter('market_name')
        param.name = encode(u'Markt')
        param.displayName = encode(u'Markt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
        
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
    
        param = self.add_parameter('marked_for_deletion')
        param.name = encode(u'Löschen')
        param.displayName = encode(u'Markt löschen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'
        
        self.add_temporary_management(
            'FGDB_Standortkonkurrenz_Supermaerkte.gdb')

        return self.par
    
    def _open(self, params):
        self.markets_df = self.table_to_dataframe('Maerkte')        
        self.markets_df['marked_for_deletion'] = False
        
        pretty_names = []
        for idx, market in self.markets_df.iterrows():
            pretty = self.get_pretty_market_name(market)
            pretty_names.append(pretty)
        self.markets_df['pretty'] = pretty_names
        self.update_market_names()
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
        return pretty
    
    def set_selected_market_inputs(self):
        market_idx = self.markets_df['pretty'] == self.par.market_name.value
        market = self.markets_df.loc[market_idx]
        chain_name = self.chains_df['name'][
            self.chains_df['id_kette'] == market['id_kette'].values[0]]
        self.par.chain.value = chain_name.values[0]
        typ_pretty = self.types_df['pretty'][
            self.types_df['id_betriebstyp'] ==
            market['id_betriebstyp_nullfall'].values[0]]
        self.par.type_name.value = typ_pretty.values[0]
        do_delete = self._deletion_flag in market['pretty']
        self.par.marked_for_deletion.value = True if do_delete else False
    
    def update_market_db(self):
        pass
    
    def update_market_names(self):
        idx = self.par.market_name.filter.list.index(
            self.par.market_name.value) if self.par.market_name.value else 0
        pretty = self.markets_df['pretty'].values
        self.par.market_name.filter.list = sorted(pretty)
        self.par.market_name.value = pretty[idx] if idx >= 0 else pretty[0]
        
    def _updateParameters(self, params):
        market_idx = self.markets_df['pretty'] == self.par.market_name.value
        
        if self.par.changed('chain'):
            id_chain = self.chains_df['id_kette'][
                self.chains_df['name'] == self.par.chain.value].values[0]
            self.markets_df.loc[market_idx, 'id_kette'] = id_chain
            
        elif self.par.changed('type_name'):
            id_typ = self.types_df['id_betriebstyp'][
                self.types_df['pretty'] == self.par.type_name.value].values[0]
            self.markets_df.loc[market_idx, 'id_betriebstyp_nullfall'] = id_typ
            
        elif self.par.changed('marked_for_deletion'):            
            if self.par.marked_for_deletion.value:
                self.markets_df.loc[market_idx, 'pretty'] += self._deletion_flag
            else:
                self.markets_df.loc[market_idx, 'pretty'] = self.markets_df.loc[
                    market_idx, 'pretty'].values[0].replace(self._deletion_flag, '')
        
        # update the pretty names of the markets
        
        if (self.par.changed('chain') or
            self.par.changed('type_name')):
            i = np.where(market_idx == True)[0][0]
            pretty = self.get_pretty_market_name(
                self.markets_df.iloc[i])
            self.markets_df.loc[market_idx, 'pretty'] = pretty
            
        if (self.par.changed('chain') or
            self.par.changed('type_name') or
            self.par.changed('marked_for_deletion')):
            self.update_market_names()
            
        if self.par.changed('market_name'):
            pass
        return params


if __name__ == '__main__':
    t = TbxEditMarkets()
    t._getParameterInfo()
    t.set_active_project()
    t._open(None)
    t._updateParameters(None)
    t.execute()
