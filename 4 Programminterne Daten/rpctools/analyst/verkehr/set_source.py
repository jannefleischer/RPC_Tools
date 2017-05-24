# -*- coding: utf-8 -*-
#

import arcpy

from rpctools.utils.params import Tool

class SetSource(Tool):
    _workspace = 'FGDB_Verkehr.gdb'

    def run(self):
        toolbox = self.parent_tbx
        source_x = toolbox.par.x_source.value
        source_y = toolbox.par.y_source.value
        source_id = toolbox.par.teilflaeche.value.split('|')[0][-2]
        toolbox.update_table('Teilflaechen_Plangebiet',
                             {'SOURCE_X': source_x, 'SOURCE_Y': source_y},
                             where='id_teilflaeche={}'.format(source_id),
                             workspace='FGDB_Definition_Projekt.gdb')
