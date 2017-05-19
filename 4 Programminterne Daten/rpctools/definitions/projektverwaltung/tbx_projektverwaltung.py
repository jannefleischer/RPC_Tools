# -*- coding: utf-8 -*-

import datetime
import arcpy
from rpctools.utils.params import Tbx
from rpctools.utils.encoding import encode
from rpctools.definitions.projektverwaltung.projektverwaltung \
     import ProjektLoeschen, ProjektAnlegen, ProjektKopieren


class TbxProjektVerwaltung(Tbx):
    """Toolbox Projektverwaltung"""

    def __init__(self):
        super(TbxProjektVerwaltung, self).__init__()
        self.update_projects = False


class TbxProjektAnlegen(TbxProjektVerwaltung):
    """Toolbox Projekt anlegen"""

    @property
    def label(self):
        return u'Projekt neu anlegen'

    @property
    def category(self):
        return u'Erstellen'

    @property
    def Tool(self):
        return ProjektAnlegen

    def _getParameterInfo(self):
        params = self.par

        # Name_des_neuen_Projektes
        p = self.add_parameter('name')
        p.name = u'Name_des_neuen_Projektes'
        p.displayName = u'Name des neuen Projektes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.value = u''

        # Shapefile_des_Plangebiets____shp_
        p = self.add_parameter('shapefile')
        p.name = u'Flaechen_des_Plangebiets'
        p.displayName = u'(Teil-)Flächen des Plangebiets'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPFeatureLayer'
        p.value = self.folders.TEMPLATE_FLAECHEN

        # Beginn_des_Betrachtungszeitraumes
        p = self.add_parameter('begin')
        p.name = u'Beginn_des_Betrachtungszeitraumes'
        p.displayName = u'Beginn des Betrachtungszeitraumes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [2010, 2050]
        p.value = datetime.datetime.now().year

        # Ende_des_Betrachtungszeitraumes
        p = self.add_parameter('end')
        p.name = u'Ende_des_Betrachtungszeitraumes'
        p.displayName = u'Ende des Betrachtungszeitraumes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'

        #Eingaben zu Beginn deaktiviere/füllen
        params.end.filter.list = [2010, 2050]
        params.end.value = 2050

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if self.par.changed('begin', 'end'):
            # Ende des Betrachtungszeitraumes prüfen
            # und ggf. auf ein Jahr nach Beginn setzen
            if params.end.value <= params.begin.value:
                params.end.value = params.begin.value + 1


class TbxProjektKopieren(TbxProjektVerwaltung):
    """Toolbox Projekt anlegen"""

    @property
    def label(self):
        return u'Projekt kopieren'

    @property
    def category(self):
        return u'Erstellen'

    @property
    def Tool(self):
        return ProjektKopieren

    def _getParameterInfo(self):
        params = self.par

        projects = self.folders.get_projects()

        # Name_des_neuen_Projektes
        p = self.add_parameter('name')
        p.name = u'Name_des_neuen_Projektes'
        p.displayName = u'Name des neuen Projektes'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.value = u''

        # Bestehendes_Projekt_auswählen
        p = self.add_parameter('existing_project')
        p.name = encode('Bestehendes_Projekt_auswählen')
        p.displayName = encode('Bestehendes Projekt auswählen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.filter.list = projects

        return params

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        projects = self.folders.get_projects()
        params.existing_project.filter.list = projects


class TbxProjekteLoeschen(TbxProjektVerwaltung):
    """Toolbox Projekt loeschen"""
    @property
    def label(self):
        return u'Projekte löschen'

    @property
    def Tool(self):
        return ProjektLoeschen

    def _getParameterInfo(self):
        projects = self.folders.get_projects()

        # Bestehendes_Projekt_auswählen
        p = self.add_parameter('projekte')
        p.name = encode('1-Projekt_auswählen')
        p.displayName = encode('Zu löschende Projekt auswählen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.multiValue = True
        p.filter.list = projects

        return self.par

    def _updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        projects = self.folders.get_projects()
        params.projekte.enabled = True
        params.projekte.filter.list = projects


if __name__ == '__main__':
    t = TbxProjektAnlegen()
    params = t.getParameterInfo()
    t.par.name.value = 'Test918'
    t.execute()
    t.print_tool_parameters()

    #t = TbxProjektKopieren()
    #params = t.getParameterInfo()
    #t.print_tool_parameters()

    #t = TbxProjekteLoeschen()
    #params = t.getParameterInfo()
    #t.print_tool_parameters()
