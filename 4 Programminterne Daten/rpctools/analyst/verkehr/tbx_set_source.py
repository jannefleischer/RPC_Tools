# -*- coding: utf-8 -*-
#
import arcpy
import os

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten \
     import TbxFlaechendefinition
from rpctools.utils.constants import Nutzungsart


class SetSource(Tool):
    _workspace = 'FGDB_Verkehr.gdb'

    def add_outputs(self):
        # update the names of the areas the points belong to
        df_areas = self.parent_tbx.table_to_dataframe(
            'Teilflaechen_Plangebiet', 
            workspace='FGDB_Definition_Projekt.gdb',
            columns=['id_teilflaeche', 'Name']
        )
        df_points = self.parent_tbx.table_to_dataframe(
            'Anbindungspunkte', columns=['id_teilflaeche'])
        df_points = df_points.merge(df_areas, on='id_teilflaeche')
        df_points.rename(columns={'Name': 'name_teilflaeche'}, inplace=True)
        self.parent_tbx.dataframe_to_table('Anbindungspunkte', df_points,
                                           ['id_teilflaeche'])
        
        self.output.add_layer('verkehr', 'Anbindungspunkte',
                              featureclass='Anbindungspunkte',
                              template_folder='Verkehr')

    def run(self):
        area, i = self.parent_tbx.get_selected_area()
        toolbox = self.parent_tbx
        source_x = toolbox.par.x_source.value
        source_y = toolbox.par.y_source.value
        shape = arcpy.Point(source_x, source_y)
        id = area['id_teilflaeche']
        toolbox.update_table('Anbindungspunkte',
                             {'Shape': shape},
                             where='id_teilflaeche={}'.format(id),
                             workspace='FGDB_Verkehr.gdb')
        arcpy.AddMessage(u"initialisiertes Verkehrsaufkommen wird gelöscht")
        self.remove_output()
        # delete pickle file
        pickle_path = self.folders.get_otp_pickle_filename(check=False)
        if os.path.exists(pickle_path):
            os.remove(pickle_path)

    def remove_output(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        layers1 = arcpy.mapping.ListLayers(mxd, "Zielpunkte*", df)
        layers2 = arcpy.mapping.ListLayers(mxd, "*Fahrten*", df)
        layers = sum([layers1, layers2], [])
        for layer in layers:
            arcpy.mapping.RemoveLayer(df, layer)
        del mxd


class TbxSetSource(TbxFlaechendefinition):

    @property
    def label(self):
        return encode(u'Anbindungspunkte setzen')

    @property
    def Tool(self):
        return SetSource

    def _open(self, params):
        super(TbxSetSource, self)._open(params)
        x, y = self.config.active_coord
        params.x_source.value = x
        params.y_source.value = y
        params.x_source.enabled = False
        params.y_source.enabled = False

    def _getParameterInfo(self):
        params = super(TbxSetSource, self)._getParameterInfo()

        # x coord
        p = self.add_parameter('x_source')
        p.name = u'x'
        p.displayName = u'X-Koordinate des Anbindungspunktes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPDouble'
        p.value = 0

        # y coord
        p = self.add_parameter('y_source')
        p.name = u'y'
        p.displayName = u'Y-Koordinate des Anbindungspunktes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPDouble'
        p.value = 0

        return self.par
    
    def set_selected_area(self):
        pass

if __name__ == '__main__':
    tbx = TbxSetSource()
    tbx._getParameterInfo()
    tbx.set_active_project()
    tbx.open()
    tbx.show_outputs()
    tbx.execute()
    print