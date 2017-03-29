# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import arcpy

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import TeilflaechenVerwalten


class TbxTeilflaecheBenennen(Tbx):
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
        p = params.teilflaeche = arcpy.Parameter()
        p.name = encode(u'Nutzungsart')
        p.displayName = encode(u'Nutzungsart')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        table = self.folders.get_table('Nutzungsart')
        table = self.folders.get_table('asdfgf')
        #fields = ['id', '']
        #rows = arcpy.da.SearchCursor(table, fields)
        p.filter.list = []

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if params.project.altered and not params.project.hasBeenValidated:
            projectname = params.project.value
            params.teilflaeche.value = ''

            tablepath_teilflaechen = self.tool.teilflaechen

            rows_teilflaechen = arcpy.SearchCursor(tablepath_teilflaechen)
            list_teilflaechen = []
            for row in rows_teilflaechen:
                list_teilflaechen.append('Nr. ' + str(row.OBJECTID) + " | "
                                         + str(round(row.Flaeche_ha, 2))
                                         + " ha" + " | " + row.NAME)

            list_teilflaechen = list(set(list_teilflaechen))
            list_teilflaechen = sorted(list_teilflaechen)

            params.teilflaeche.filter.list = list_teilflaechen

            if list_teilflaechen:
                flaeche = list_teilflaechen[0]
                params.teilflaeche.value = list_teilflaechen[0]

        if params.teilflaeche.altered:
            flaeche = params.teilflaeche.value
            flaechenname = flaeche.split('|')[2]
            params.name.value = flaechenname

        #Teilfläche auswählen
        #if params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated:
            #projectname = params.project.value
            #flaechenname_id = flaechenname.split('|')[0].replace('Nr.', '').strip()

    def _updateMessages(self, params):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""


        if params.project.value != None and params.name.value != None:
            projectname = params[0].value
            tablepath_teilflaechen = self.tool.teilflaechen
            namen_cursor = arcpy.da.SearchCursor(tablepath_teilflaechen, "Name")

            params.name.clearMessage()

            for row in namen_cursor:
                if params.name.value == row[0]:
                    params.name.setErrorMessage("Name wurde bereits vergeben.")


if __name__ == '__main__':

    t = TbxTeilflaecheBenennen()
    params = t.getParameterInfo()
    t.print_test_parameters()
    t.print_tool_parameters()
    t.updateParameters(params)
    t.updateMessages(params)
    t.print_test_parameters()