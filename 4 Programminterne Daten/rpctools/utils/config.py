# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# project_lib.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH / HCU Hamburg / GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
from os import listdir
import sys
from os.path import join, isdir, abspath, dirname, basename, exists
from os import mkdir
import arcpy
import json

from rpctools.utils.singleton import Singleton
from rpctools.utils.encoding import encode


class Config(object):
    __metaclass__ = Singleton

    _default = {
        'active_project': '',
        'epsg': 31467,
        'transformation': "DHDN_To_WGS_1984_5x",
        'max_area_distance': 1000,
    }

    _config = {}

    def __init__(self):

        self.config_file = Folders().CONFIG_FILE
        self._callbacks = {}

        if exists(self.config_file):
            self.read()
            # add missing Parameters
            changed = False
            for k, v in self._default.iteritems():
                if k not in self._config:
                    self._config[k] = v
                    changed = True
            if changed:
                self.write()

        # write default config, if file doesn't exist yet
        else:
            self._config = self._default.copy()
            self.write()

    def read(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        try:
            with open(config_file, 'r') as f:
                self._config = json.load(f)
        except:
            self._config = self._default.copy()
            print('Error while loading config. Using default values.')

    def write(self, config_file=None):
        if config_file is None:
            config_file = self.config_file

        with open(config_file, 'w') as f:
            config_copy = self._config.copy()
            # pretty print to file
            json.dump(config_copy, f, indent=4, separators=(',', ': '))

    # access stored config entries like fields
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self._config:
            return self._config[name]
        raise AttributeError

    def __setattr__(self, name, value):
        if name in self._config:
            self._config[name] = value
            if name in self._callbacks:
                for callback in self._callbacks[name]:
                    callback(value)
        else:
            self.__dict__[name] = value
        #if name in self._callbacks:
            #for callback in self._callbacks[name]:
                #callback(value)

    def __repr__(self):
        return repr(self._config)
    
    def on_change(self, attribute, callback):
        if attribute not in self._callbacks:
            self._callbacks[attribute] = []
        self._callbacks[attribute].append(callback)
        
    def remove_listeners(attribute):
        if attribute in self._callbacks:
            self._callbacks.pop(attribute)

########################################################################
class Folders(object):
    """"""
    def __init__(self, params=None):
        """class that returns path"""
        self.BASE_PATH = abspath(join(dirname(__file__), '..', '..', '..'))
        self._PROJECT_BASE_PATH = '3 Benutzerdefinierte Projekte'
        self._INTERN = '4 Programminterne Daten'
        self._BASE_DBS = 'workspaces'
        self._TEMPORARY_GDB_PATH = 'temp_gdb'
        self._TEMPLATE_BASE_PATH = 'templates'
        self._TEMPLATE_FLAECHEN = 'projektflaechen_template.shp'
        self._PROJECT_TEMPLATE = 'Template'
        self._TEST_TEMPLATE = 'Test_Template'
        self._TEMPLATE_LAYERFOLDER = 'layers'
        self._TEMPLATE_DIAGRAMFOLDER = 'diagrams'
        self._TOCFOLDER = 'toc'
        self._TEST_TMP_PROJECT = '__unittest__'
        self._AUSGABE_PATH = 'Ergebnisausgabe'
        self._TEXTE = 'texte'
        self._MXDS = 'mxds'
        self._DEFINITION_PYT_PATH = '1 Planungsprojekte definieren'
        self._ANALYST_PYT_PATH = '1 Planungsprojekte definieren'
        # the params
        self._params = params
        self._invalid_paths = []
        self._config_file = 'config.txt'

    def join_and_check(self, *args, **kwargs):
        """
        Joins paths and checks if joined path points to existing resource
        (directory, database or table) if requested and stores the invalid
        paths

        Parameters
        ----------
        args: paths to join
        check : str, optional
            if True, checks if joined path points to existing resource
        Returns
        -------
        path : str
            the joined path
        """
        path = join(*args)
        check = kwargs.get('check', True)
        if check and not arcpy.Exists(path):
            self._invalid_paths.append(path)
        return path

    @property
    def project(self):
        """The project name"""
        projectname = self._params._get_projectname()
        return projectname

    @property
    def dbname(self):
        """The default database name"""
        dbname = self._params._dbname
        return dbname

    @property
    def INTERN(self):
        return self.join_and_check(self.BASE_PATH, self._INTERN)

    @property
    def BASE_DBS(self):
        return self.join_and_check(self.INTERN, self._BASE_DBS)

    @property
    def MXDS(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH, self._MXDS)

    @property
    def TEXTE(self):
        return self.join_and_check(self.INTERN, self._TEXTE)

    @property
    def PROJECT_BASE_PATH(self):
        return self.join_and_check(self.BASE_PATH, self._PROJECT_BASE_PATH)

    @property
    def TEMPLATE_BASE_PATH(self):
        return self.join_and_check(self.BASE_PATH, self._INTERN,
                                   self._TEMPLATE_BASE_PATH)

    @property
    def TEMPORARY_GDB_PATH(self):
        path = join(self.INTERN, self._TEMPORARY_GDB_PATH)
        if not exists(path):
            mkdir(path)
        return path    

    @property
    def TEMPLATE_FLAECHEN(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH,
                                   self._TEMPLATE_FLAECHEN)

    @property
    def TEMPLATE_LAYERFOLDER(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH,
                                   self._TEMPLATE_LAYERFOLDER)

    @property
    def TEMPLATE_DIAGRAMFOLDER(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH,
                                   self._TEMPLATE_DIAGRAMFOLDER)

    @property
    def TOCFOLDER(self):
        return self.join_and_check(self.TEMPLATE_LAYERFOLDER, self._TOCFOLDER)

    @property
    def PROJECT_TEMPLATE(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH,
                                   self._PROJECT_TEMPLATE)

    @property
    def TEST_TEMPLATE(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH,
                                   self._TEST_TEMPLATE)

    @property
    def TEST_TMP_PROJECT(self):
        return self.join_and_check(self.PROJECT_BASE_PATH,
                                   self._TEST_TMP_PROJECT)

    @property
    def CONFIG_FILE(self):
        return join(self.INTERN, self._config_file)
    
    @property
    def ANALYST_PYT_PATH(self):
        return self.join_and_check(self.BASE_PATH, self._ANALYST_PYT_PATH)

    @property
    def DEFINITION_PYT_PATH(self):
        return self.join_and_check(self.BASE_PATH, self._DEFINITION_PYT_PATH)

    def get_projects(self):
        '''
        returns all available projects inside the project folder
        (except the temp. projects which are not meant to be edited)
        '''
        subfolders = [f for f in listdir(self.PROJECT_BASE_PATH)
                      if isdir(self.get_projectpath(f))
                      and f != self._TEST_TMP_PROJECT]
        return sorted(subfolders)

    def get_temporary_projects(self):
        '''
        returns all projects for which temporary databases exist
        '''
        subfolders = [f for f in listdir(self.TEMPORARY_GDB_PATH)
                      if isdir(self.get_temporary_projectpath(f))]
        return sorted(subfolders)

    def get_projectpath(self, project=None, check=True):
        """
        The Path to the Project Folder

        Parameters
        ----------
        project : str
            the project name
        Returns
        -------
        projectpath : str
            the full path of the Project folder
        """
        projectname = project or self.project
        return self.join_and_check(self.PROJECT_BASE_PATH,
                                   projectname,
                                   check=check)

    def get_temporary_projectpath(self, project=None):
        projectname = project or self.project
        path = join(self.TEMPORARY_GDB_PATH, projectname)
        if not exists(path):
            mkdir(path)
        return path

    def get_temporary_db(self, project=None, fgdb='', check=True):
        dbname = basename(fgdb) or self.dbname
        return self.join_and_check(
            self.get_temporary_projectpath(project=project),
            dbname, check=check)

    def get_temporary_table(self, table_name, fgdb='',
                            project=None, check=True):
        return self.join_and_check(
            self.get_temporary_db(fgdb=fgdb, project=project, check=True),
            table_name, check=check)

    @property
    def PROJECT_PATH(self):
        """The Projectpath"""
        return self.get_projectpath()

    @property
    def AUSGABE_PATH(self):
        """The Projectpath"""
        return self.join_and_check(self.PROJECT_PATH, self._AUSGABE_PATH)

    def get_db(self, workspace='', project=None, check=True):
        """
        A Workspace in the Project Folder

        Parameters
        ----------
        workspace : str, optional
            the name of the Workspace
        project : str, optional
            the project name

        Returns
        -------
        projectdb : str
            the full path of the Workspace
        """
        dbname = basename(workspace) or self.dbname
        projectname = project or self.project
        return self.join_and_check(self.get_projectpath(projectname), dbname,
                                   check=check)

    def get_table(self, tablename, workspace='', project='', check=True):
        """
        A Table in a Workspace in the Project Folder

        Parameters
        ----------
        tablename : str
        workspace : str, optional
            the name of the Workspace
        project : str, optional
            the project name

        Returns
        -------
        table : str
            the full path to a table in the Workspace
        """
        dbname = basename(workspace) or self.dbname
        projectname = project or self.project
        table = self.join_and_check(self.get_db(dbname, projectname),
                                    tablename,
                                    check=check)
        return table

    def get_basedb(self, workspace, check=True):
        """
        A Base Workspace

        Parameters
        ----------
        workspace : str
            the name of the Workspace

        Returns
        -------
        basedb : str
            the full path of the Workspace
        """
        return self.join_and_check(self.BASE_DBS, workspace, check=check)

    def get_base_table(self, workspace, table, check=True):
        """
        A Table in a Base Workspace

        Parameters
        ----------
        workspace : str
            the name of the Workspace
        tablename : str
            the name of the table
        check : bool
            if false, don't check if table exists

        Returns
        -------
        base_table : str
            the full path to the table in the Base Workspace
        """
        dbname = basename(workspace)
        table = self.join_and_check(self.get_basedb(dbname), table,
                                    check=check)
        return table

    def update_table(self, table, column_values, where=None, workspace='',
                     project='', check=True):
        """
        Update rows in a Workspace in the Project Folder

        Parameters
        ----------
        table : str
            the name of the table
        column_values: dict,
            the columns and the values to update them with as key/value-pairs
        where: str, optional
            a where clause to pick single rows
        workspace : str, optional
            the name of the Workspace
        project : str, optional
            the project name
        check : bool, optional
            if false, don't check if table exists
        """
        table = self.get_table(table, workspace=workspace, project=project, check=True)
        columns = column_values.keys()
        cursor = arcpy.da.UpdateCursor(table, columns, where_clause=where)
        for row in cursor:
            for i, column in enumerate(columns):
                row[i] = column_values[column]
            cursor.updateRow(row)
        del cursor

    def get_layer(self, layername, folder='', enhance = True):
        """
        A lyr-file

        Parameters
        ----------
        layername : str
            the name of the lyr-file

        folder : str, optional
            a subfolder

        enhance = boolean, optional
            True -> ".lyr" will be added to layername

        Returns
        -------
        layer : str
            the full path to the lyr-file
        """
        layername = encode(layername)
        if (enhance == True):
            layerfile = '{}.lyr'.format(layername)
        else:
            layerfile = layername

        layer = self.join_and_check(self.TEMPLATE_LAYERFOLDER, folder, layerfile)
        return layer

    def get_diagram_template(self, name, subfolder='', enhance=True):
        """
        Return a diagram from the templates

        Parameters
        ----------
        name : str
            the name of the diagram
        subfolder : str, optional
            a subfolder for a specific diagram
        enhance : bool, optional (Default=True)
            if true, add .grf as extension to the diagram name

        Returns
        -------
        path : str
            the full path to the diagram
        """
        filename = encode(name)
        if enhance:
            filename = '{}.grf'.format(filename)
        diagram_path = self.join_and_check(self.TEMPLATE_DIAGRAMFOLDER,
                                           subfolder,
                                           filename)
        return diagram_path

if __name__ == '__main__':
    c = Config()
    print(c)