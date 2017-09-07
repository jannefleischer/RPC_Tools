# -*- coding: utf-8 -*-
import arcpy
from rpctools.utils.params import Tbx, Tool

class TbxFieldSelection(Tbx):

    @property
    def label(self):
        return encode(u'Gemeinden auswählen')

    @property
    def Tool(self):
        return FieldSelectionTool

    def _getParameterInfo(self):

        params = self.par
        projekte = self.folders.get_projects()

        # Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = u'Projekt_auswählen'.encode('cp1252')
        p.displayName = u'Projekt'.encode('cp1252')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.value = self.config.active_project

        return params


class FieldSelectionTool(Tool):
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
    _table = "Zentren"
    def add_outputs(self):
        mxd = arcpy.mapping.MapDocument("Current")
        lyrname_selected = 'Ausgewählte Gemeinden im Betrachtungsraum'
        lyrname_not_selected = 'Nicht ausgewählte Gemeinden'
        lyr_selected = arcpy.mapping.ListLayers(mxd, lyrname_selected)
        lyr_not_selected = arcpy.mapping.ListLayers(mxd, lyrname_not_selected)
        if not lyr_selected:
            self.output.add_layer('standortkonkurrenz', 'Zentren_selected',
                                 template_folder='Standortkonkurrenz',
                                 featureclass=self._table,
                                 workspace=self._workspace,
                                 name='Ausgewählte Gemeinden im '+\
                                 'Betrachtungsraum')
        if not lyr_not_selected:
            self.output.add_layer('standortkonkurrenz', 'Zentren_background',
                                 template_folder='Standortkonkurrenz',
                                 featureclass=self._table,
                                 workspace=self._workspace,
                                 name='Nicht ausgewählte Gemeinden',
                                 zoom=True)

    def run(self):
        pass
