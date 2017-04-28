# -*- coding: utf-8 -*-
#

import arcpy
import numpy as np
from rpctools.utils.config import Folders
from rpctools.utils.params import Tool


class UpdateNodes(Tool):
    _dbname = 'FGDB_Verkehr.gdb'
    _param_projectname = 'project'

    def run(self):
        toolbox = self.parent_tbx
        # add new column
        nodes_path = self.folders.get_table('Zielpunkte', workspace='',
                                            project='', check=True)
        arcpy.AddField_management(nodes_path, 'Neue_Gewichte',
                                  field_type='DOUBLE')
        # get input data
        input_data = toolbox.query_table('Zielpunkte',
                                          ['node_id', 'Manuelle_Gewichtung',
                                           'Gewicht_Bewohnerverkehr'])
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

        # write data to the new table
        if old_weights_not_set.tolist() != None:
            for i in range(len(old_weights_not_set)):
                weight = old_weights_not_set[i]
                id_node = node_id_not_set[i]
                print id_node, weight
                where = 'node_id = {}'.format(id_node)
                toolbox.update_table('Zielpunkte',
                                  {'Neue_Gewichte': weight}, where=where)

        if man_weights.tolist() != None:
            for i in range(len(man_weights)):
                weight = man_weights[i]
                id_node = node_id[i]
                print id_node, weight
                where = 'node_id = {}'.format(id_node)
                toolbox.update_table('Zielpunkte',
                                  {'Neue_Gewichte': weight}, where=where)
        pass