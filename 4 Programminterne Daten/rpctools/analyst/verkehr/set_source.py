# -*- coding: utf-8 -*-
#

import arcpy

from rpctools.utils.params import Tool

class SetSource(Tool):
    _workspace = 'FGDB_Verkehr.gdb'

    def add_outputs(self):
        self.output.add_layer('verkehr', 'Anbindungspunkte',
                              featureclass='Anbindungspunkte',
                              template_folder='Verkehr')

    def run(self):
        toolbox = self.parent_tbx
        source_x = toolbox.par.x_source.value
        source_y = toolbox.par.y_source.value
        shape = arcpy.Point(source_x, source_y)
        source_id = toolbox.par.teilflaeche.value.split('|')[0][-2]
        toolbox.update_table('Anbindungspunkte',
                             {'Shape': shape},
                             where='id_teilflaeche={}'.format(source_id),
                             workspace='FGDB_Verkehr.gdb')
        arcpy.AddMessage("initialisiertes Verkehrsaufkommen wir gelöscht")
        self.remove_output()
        # delete pickle file
        pickle_path = self.folders.get_otp_pickle_filename()
        if arcpy.Exists(pickle_path):
            arcpy.Delete_management(pickle_path)

    def remove_output(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        layers1 = arcpy.mapping.ListLayers(mxd, "Zielpunkte*", df)
        layers2 = arcpy.mapping.ListLayers(mxd, "*Fahrten*", df)
        layers = sum([layers1, layers2], [])
        for layer in layers:
            arcpy.mapping.RemoveLayer(df, layer)
