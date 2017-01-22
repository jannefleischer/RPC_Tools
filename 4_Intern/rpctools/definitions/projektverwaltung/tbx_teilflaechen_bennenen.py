# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.teilflaeche_benennen import TeilflaechenBenennen


class TbxTeilflaecheBenennen(Tbx):
    """Toolbox to name Teilflächen"""

    @property
    def label(self):
        return u'2 Teilflaechen verwalten'

    @property
    def Tool(self):
        return TeilflaechenBenennen

    def getParameterInfo(self):
        # Projekt
        params = self.par

        projects = get_projects()
        params.project = arcpy.Parameter()
        params.project.name = u'Projekt'
        params.project.displayName = u'Projekt'
        params.project.parameterType = 'Required'
        params.project.direction = 'Input'
        params.project.datatype = u'Zeichenfolge'
        params.project.value = u' '
        params.project.filter.list = projects

        # Teilfläche
        params.teilflaeche = arcpy.Parameter()
        params.teilflaeche.name = encode(u'Teilfläche')
        params.teilflaeche.displayName = encode(u'Teilfläche')
        params.teilflaeche.parameterType = 'Required'
        params.teilflaeche.direction = 'Input'
        params.teilflaeche.datatype = u'GPString'
        params.teilflaeche.filter.list = []

        # Name
        params.name = arcpy.Parameter()
        params.name.name = u'Name'
        params.name.displayName = u'Name'
        params.name.parameterType = 'Required'
        params.name.direction = 'Input'
        params.name.datatype = u'GPString'

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        #Projekt auswählen

        if params.project.altered and not params.project.hasBeenValidated:
            projects = self.folders.get_projects()
            params.project.filter.list = projects

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

            if list_teilflaeche:
                params.teilflaeche.value = list_teilflaechen[0]


        #Teilfläche auswählen
        if params.teilflaeche.altered and not params.teilflaeche.hasBeenValidated:

            projectname = params.project.value
            flaechenname = params.teilflaeche.value
            flaechenname_id = flaechenname.split('|')[0].replace('Nr.', '').strip()

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
