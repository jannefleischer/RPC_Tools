# -*- coding: utf-8 -*-
#

import arcpy
import numpy as np
from rpctools.utils.config import Folders
from rpctools.utils.params import Tool
from rpctools.analyst.verkehr.otp_router import OTPRouter
from rpctools.outputs.verkehr import VerkehrOutput


class UpdateNodes(Tool):
    _workspace = 'FGDB_Verkehr.gdb'
    _param_projectname = 'project'
    
    @property
    def Output(self):
        return VerkehrOutput

    def run(self):

        otp_router = OTPRouter.from_dump(self.folders.get_otp_pickle_filename())
            
        toolbox = self.parent_tbx
        # get input data
        input_data = toolbox.query_table('Zielpunkte',
                                          ['node_id', 'Manuelle_Gewichtung',
                                           'Gewicht'])
        node_id = [tup[0] for tup in input_data]
        man_weights = [tup[1] for tup in input_data]
        old_weights = [tup[2] for tup in input_data]

        # divide in lists with/without manual weight
        idx_correct = 0
        node_id_not_set = []
        man_weights_not_set = []
        old_weights_not_set = []
        for i in range(len(man_weights)):
            man_weight=man_weights[i-idx_correct]
            if man_weight == None:
                node_id_not_set.append(node_id.pop(i-idx_correct))
                man_weights_not_set.append(man_weights.pop(i-idx_correct))
                old_weights_not_set.append(old_weights.pop(i-idx_correct))
                idx_correct += 1

        # calculate new weights
        total_man_weight = sum(man_weights)
        total_old_weight_not_set = sum(old_weights_not_set)
        if total_man_weight <= 100:
            remaining_weight = 100 - total_man_weight
            old_weights_not_set = np.array(old_weights_not_set) * \
                remaining_weight / total_old_weight_not_set
            man_weights = np.array(man_weights)
        else:
            total_weight = total_man_weight + total_old_weight_not_set
            old_weights_not_set = np.array(old_weights_not_set) / total_weight
            man_weights = np.array(man_weights) / total_weight
            
        transfer_nodes = otp_router.transfer_nodes
        
        def set_new_weights(weights, node_ids):
            """"""
            # write data to the new table
            for i, weight in enumerate(weights):
                id_node = node_ids[i]
                print id_node, weight
                transfer_nodes[id_node].weight = weight
                where = 'node_id = {}'.format(id_node)
                toolbox.update_table('Zielpunkte',
                                  {'Neue_Gewichte': weight}, where=where)

        set_new_weights(old_weights_not_set, node_id_not_set)
        set_new_weights(man_weights, node_id)
        
        transfer_nodes.assign_weights_to_routes()
        otp_router.calc_vertex_weights()
        otp_router.create_polyline_features()        

        # update the layers
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        layers = arcpy.mapping.ListLayers(mxd, "Zielpunkte*", df)
        for layer in layers:
            arcpy.mapping.RemoveLayer(df, layer)

        