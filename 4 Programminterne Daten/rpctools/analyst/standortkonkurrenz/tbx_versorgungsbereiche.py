# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.utils.spatial_lib import get_closest_point, get_ags
import numpy as np
import pandas as pd

NULLFALL = 0
PLANFALL = 1


class EditCenters(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'

    def add_outputs(self):         
        group_layer = ("standortkonkurrenz")
        fc = 'Zentren'
        layer = 'Zentren'
    
        self.output.add_layer(group_layer, layer, fc, zoom=False)

    def run(self):
        #markets_df = self.parent_tbx.markets_df
        #delete_df = markets_df.loc[markets_df['do_delete'] == True]
        #update_df = markets_df.loc[markets_df['do_delete'] == False]
        #if len(delete_df) > 0:
            #arcpy.AddMessage(u'Lösche Märkte')
        #for idx, market in delete_df.iterrows():
            #arcpy.AddMessage(u' - {}'.format(market['pretty']))
            #self.parent_tbx.delete_rows_in_table(
                #'Maerkte',
                #where='id={}'.format(market['id']))
            #self.parent_tbx.delete_rows_in_table(
                #'Beziehungen_Maerkte_Zellen',
                #where='id_markt={}'.format(market['id']))
        #arcpy.AddMessage(u'Schreibe Änderungen in Datenbank...')
        #self.parent_tbx.dataframe_to_table('Maerkte', update_df,
                                           #['id'], upsert=False)
        #arcpy.RefreshActiveView()
        pass
    

class TbxEditCenters(Tbx):
    
    @property
    def label(self):
        return 'Zentren bearbeiten'

    @property
    def Tool(self):
        return EditCenters

    def _getParameterInfo(self):
        
        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
    
        param = self.add_parameter('centres')
        param.name = encode(u'Versorgungsbereiche')
        param.displayName = encode(u'Versorgungsbereich auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
        
        param = self.add_parameter('name')
        param.name = encode(u'Name')
        param.displayName = encode(u'Name des Versorgungsbereichs')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'

        param = self.add_parameter('do_delete')
        param.name = encode(u'Löschen')
        param.displayName = encode(u'Versorgungsbereich entfernen')
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = u'GPBoolean'
        
        self.centers_df = []
        return self.par
    
    def get_centers(self):
        '''return the markets in db as a dataframe, filtered by existance
        in nullfall and planfall (dependent on setting of this toolbox)'''
        df_centers = self.table_to_dataframe('Zentren')
        return df_centers
    
    def add_center_to_db(self, name, polygon):
        '''add a market to the database located in given coordinates
        (if market becomes planfall or nullfall depends on setting of toolbox)
        '''
        # take ALL markets (planfall and nullfall) to get correct max id
        df_centers = self.get_centers()
        if len(df_centers) == 0:
            new_id = 1
        else: 
            new_id = df_centers['id'].max() + 1
        column_values = {
            'id': new_id,
            'name': name,
            'SHAPE@': polygon
        }
        self.insert_rows_in_table('Zentren', column_values)
    
    def _open(self, params):
        #self.markets_df = self.get_markets()
        #self.markets_df['do_delete'] = False
        #self.markets_df.sort(columns='id', inplace=True)
        #if len(self.markets_df) == 0:
            #return

        #x, y = self.config.active_coord
        #closest_idx = None
        #if x and y:
            #closest_idx, c = get_closest_point((x, y), self.markets_df['SHAPE'])
        
        #pretty_names = []
        #for idx, market in self.markets_df.iterrows():
            #pretty = self.get_pretty_market_name(market)
            #pretty_names.append(pretty)
        #self.markets_df['pretty'] = pretty_names
        #self.update_market_list(closest_idx)
        #self.set_selected_market_inputs()
        pass
    
    def set_selected_center_inputs(self):
        #betriebstyp_col = 'id_betriebstyp_nullfall' \
            #if self.setting == NULLFALL else 'id_betriebstyp_planfall'
        #market_idx = self.markets_df['pretty'] == self.par.markets.value
        #market = self.markets_df.loc[market_idx]
        #self.par.name.value = market['name'].values[0]
        #chain_name = self.chains_df['name'][
            #self.chains_df['id_kette'] == market['id_kette'].values[0]]
        #self.par.chain.value = chain_name.values[0]        
        #typ_pretty = self.types_df['pretty'][
            #self.types_df['id_betriebstyp'] ==
            #market[betriebstyp_col].values[0]]
        #self.par.type_name.value = typ_pretty.values[0]
        #do_delete = market['do_delete'].values[0]
        ## strange: can't assign the bool of do_delete directly, arcpy is
        ## ignoring it
        #self.par.do_delete.value = True if do_delete else False
        pass
    
    def validate_inputs(self):
        if len(self.table_to_dataframe('Zentren', columns=['id'])) == 0:
            msg = (u'Es sind keine Zentren definiert. '
                   u'Bitte fügen Sie sie manuell hinzu.')
            return False, msg
        return True, ''
        
    def update_center_list(self, idx=None):
        if idx is None:
            idx = self.par.centers.filter.list.index(
                self.par.centers.value) if self.par.centers.value else 0
        names = self.centers_df['name'].values
        self.par.centers.filter.list = names
        self.par.centers.value = names[idx] if idx >= 0 else names[0]
        
    def _updateParameters(self, params):
        #if len(self.markets_df) == 0:
            #return
        #market_idx = self.markets_df['pretty'] == self.par.markets.value

        #if self.par.changed('name'):
            #self.markets_df.loc[market_idx, 'name'] = self.par.name.value
            
        #elif self.par.changed('chain'):
            #id_chain = self.chains_df['id_kette'][
                #self.chains_df['name'] == self.par.chain.value].values[0]
            #self.markets_df.loc[market_idx, 'id_kette'] = id_chain
            
        #elif self.par.changed('type_name'):
            #id_typ = self.types_df['id_betriebstyp'][
                #self.types_df['pretty'] == self.par.type_name.value].values[0]
            ## only change nullfall type when toolbox is set to nullfall
            ## in case of planfall it stays 0
            #if self.setting == NULLFALL:
                #self.markets_df.loc[market_idx, 'id_betriebstyp_nullfall'] = id_typ
            ## ToDo: set different type for planfall if nullfall is edited?
            #self.markets_df.loc[market_idx, 'id_betriebstyp_planfall'] = id_typ
            
        #elif self.par.changed('do_delete'):
            #do_delete = self.par.do_delete.value
            #self.markets_df.loc[market_idx, 'do_delete'] = do_delete
        
        ## update the pretty names of the markets
            
        #if (self.par.changed('name') or 
            #self.par.changed('chain') or
            #self.par.changed('type_name') or
            #self.par.changed('do_delete')):
            #i = np.where(market_idx == True)[0][0]
            #pretty = self.get_pretty_market_name(
                #self.markets_df.iloc[i])
            #self.markets_df.loc[market_idx, 'pretty'] = pretty
            #self.update_market_list()
            
        #if self.par.changed('markets'):
            #self.set_selected_market_inputs()
        return params

    def _updateMessages(self, params):
        valid, msg = self.validate_inputs()
        if not valid:
            self.par.projectname.setErrorMessage(msg)

if __name__ == '__main__':
    t = TbxEditCenters()
    t._getParameterInfo()
    t.set_active_project()
    t.add_center_to_db('Test add', (3544252, 5925427))
    t._open(None)
    t._updateParameters(None)
    t.execute()
