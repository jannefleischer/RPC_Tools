# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import TeilflaechenVerwalten


class TbxTeilflaecheVerwalten(Tbx):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'Schritt 2: Teilflaechen verwalten'

    @property
    def Tool(self):
        return TeilflaechenVerwalten

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        p = params.project = arcpy.Parameter()
        p.name = u'Projekt'
        p.displayName = u'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        projects = self.folders.get_projects()
        p.filter.list = projects
        p.value = '' if len(projects) == 0 else p.filter.list[0]

        # Teilfläche
        p = params.teilflaeche = arcpy.Parameter()
        p.name = encode(u'Teilfläche')
        p.displayName = encode(u'Teilfläche')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []

        # Name
        p = params.name = arcpy.Parameter()
        p.name = u'Name'
        p.displayName = u'Name'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'

        # Nutzungsart
        p = params.nutzungsart = arcpy.Parameter()
        p.name = encode(u'Nutzungsart')
        p.displayName = encode(u'Nutzungsart')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = self.tool.nutzungsarten.keys()

        return params

    def get_row(self):
        flaechen_id = self.teilflaechen[flaechenname]
        where = '"OBJECTID" = {}'.format(flaechen_id)
        nutzungsart_id = self.nutzungsarten[self.par.nutzungsart.value]
        rows = arcpy.UpdateCursor(self.teilflaechen_table, where)
        row = row.next()
        for row in rows:
            row.NAME = neuer_name  #self.par.name.valueAsText
            row.Nutzungsart = nutzungsart_id
            rows.updateRow(row)


    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if params.project.altered and not params.project.hasBeenValidated:
            params.teilflaeche.value = ''

            list_teilflaechen = self.tool.teilflaechen.keys()
            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaechen:
                flaeche = list_teilflaechen[0]
                params.teilflaeche.value = list_teilflaechen[0]

        if ((params.project.altered and not params.project.hasBeenValidated) or
            (params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated)):

            flaeche = params.teilflaeche.value
            # ToDo: get the currently selected name without splitting string
            flaechenname = self.tool.get_flaechenname(flaeche)
            params.name.value = flaechenname
            flaechen_id = self.tool.teilflaechen[flaeche]
            nutzungsart_id = self.tool.get_nutzungsart_id(flaechen_id)
            nutzungsarten = self.tool.nutzungsarten
            nutzungsart = nutzungsarten.keys()[
                nutzungsarten.values().index(nutzungsart_id)]
            params.nutzungsart.value = nutzungsart

    def _updateMessages(self, params):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        if params.project.value != None and params.name.value != None:
            projectname = params.project.value
            tablepath_teilflaechen = self.tool.teilflaechen_table
            namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

            params.name.clearMessage()

            for row in namen_cursor:
                if params.name.value == row[0]:
                    params.name.setErrorMessage("Name wurde bereits vergeben.")


if __name__ == '__main__':

    t = TbxTeilflaecheVerwalten()
    params = t.getParameterInfo()
    t.print_test_parameters()
    t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()