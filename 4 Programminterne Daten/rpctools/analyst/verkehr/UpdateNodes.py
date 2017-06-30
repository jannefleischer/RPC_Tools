# -*- coding: utf-8 -*-
#

import arcpy
import numpy as np
from rpctools.utils.config import Folders
from rpctools.utils.params import Tool
from rpctools.analyst.verkehr.otp_router import OTPRouter
from rpctools.analyst.verkehr.routing import Routing


class UpdateNodes(Routing):

    def add_outputs(self):
        self.output.add_layer('verkehr', 'Zielpunkte_gewichtet',
                              featureclass='Zielpunkte',
                              template_folder='Verkehr',
                              name='Zielpunkte gewichtet')
        self.output.add_layer('verkehr', 'links',
                              featureclass='links',
                              template_folder='Verkehr',
                              name='Zusätzliche PKW-Fahrten gewichtet')
        return

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
        # split id
        node_id_set = [node_id[i] for i, weight in enumerate(man_weights) \
                       if weight != None]
        node_id_not_set = [i for i in node_id if i not in node_id_set]
        #split weight
        man_weights_set = [weight / 100 for weight in man_weights \
                           if weight != None]
        man_weights_not_set = [old_weight for i, old_weight in \
                               enumerate(old_weights) \
                               if man_weights[i] == None]
        total_man_weight = sum(man_weights_set)
        total_old_weight_not_set = sum(man_weights_not_set)
        if total_man_weight <= 1:
            remaining_weight = 1 - total_man_weight
            man_weights_not_set = np.array(man_weights_not_set) * \
                remaining_weight / total_old_weight_not_set
            man_weights_set = np.array(man_weights_set)
        else:
            total_weight = total_man_weight + total_old_weight_not_set
            man_weights_not_set = np.array(man_weights_not_set) / total_weight
            man_weights_set = np.array(man_weights_set) / total_weight

        transfer_nodes = otp_router.transfer_nodes
        self.remove_output()

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

        set_new_weights(man_weights_not_set, node_id_not_set)
        set_new_weights(man_weights_set, node_id_set)

        transfer_nodes.assign_weights_to_routes()
        otp_router.calc_vertex_weights()
        otp_router.create_polyline_features()

    def remove_output(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        layers1 = arcpy.mapping.ListLayers(mxd, "Zielpunkte*", df)
        layers2 = arcpy.mapping.ListLayers(mxd, "*Fahrten*", df)
        layers = sum([layers1, layers2], [])
        for layer in layers:
            arcpy.mapping.RemoveLayer(df, layer)
