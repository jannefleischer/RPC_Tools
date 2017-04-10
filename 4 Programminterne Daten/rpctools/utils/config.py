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
from os.path import join, isdir, abspath, dirname, basename
import arcpy

TEST_TMP_PROJECT = '__unittest__'

########################################################################
class Folders(object):
    """"""
    def __init__(self, params=None):
        """class that returns path"""
        self.BASE_PATH = abspath(join(dirname(__file__), '..', '..', '..'))
        self._PROJECT_BASE_PATH = '3 Benutzerdefinierte Projekte'
        self._INTERN = '4 Programminterne Daten'
        self._BASE_DBS = 'fgdbs'
        self._TEMPLATE_BASE_PATH = 'templates'
        self._TEMPLATE_FLAECHEN = 'projektflaechen_template.shp'
        self._PROJECT_TEMPLATE = 'Template'
        self._TEST_TEMPLATE = 'Test_Template'
        self._TEMPLATE_LAYERFOLDER = 'layers'
        self._TOCFOLDER = 'toc'
        self._TEST_TMP_PROJECT = TEST_TMP_PROJECT
        self._AUSGABE_PATH = 'Ergebnisausgabe'
        self._TEXTE = 'texte'
        self._MXDS = 'mxds'
        # the params
        self._params = params
        self._invalid_paths = []


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
        arcpy.AddError
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
        return self.join_and_check(self.BASE_PATH, self._INTERN, self._TEMPLATE_BASE_PATH)

    @property
    def TEMPLATE_FLAECHEN(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH, self._TEMPLATE_FLAECHEN)

    @property
    def TEMPLATE_LAYERFOLDER(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH, self._TEMPLATE_LAYERFOLDER)

    @property
    def TOCFOLDER(self):
        return self.join_and_check(self.TEMPLATE_LAYERFOLDER, self._TOCFOLDER)

    @property
    def PROJECT_TEMPLATE(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH, self._PROJECT_TEMPLATE)

    @property
    def TEST_TEMPLATE(self):
        return self.join_and_check(self.TEMPLATE_BASE_PATH, self._TEST_TEMPLATE)

    @property
    def TEST_TMP_PROJECT(self):
        return self.join_and_check(self.PROJECT_BASE_PATH, self._TEST_TMP_PROJECT)

    def get_projects(self):
        '''
        returns all available projects inside the project folder
        (except the temp. projects which are not meant to be edited)
        '''
        subfolders = [f for f in listdir(self.PROJECT_BASE_PATH)
                      if isdir(self.get_projectpath(f))
                      and f != self._TEST_TMP_PROJECT]
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

    @property
    def PROJECT_PATH(self):
        """The Projectpath"""
        return self.get_projectpath()

    @property
    def AUSGABE_PATH(self):
        """The Projectpath"""
        return self.join_and_check(self.PROJECT_PATH, self._AUSGABE_PATH)

    def get_db(self, fgdb='', project=None, check=True):
        """
        A FileGeodatabase in the Project Folder

        Parameters
        ----------
        fgdb : str, optional
            the name of the FileGeodatabase
        project : str, optional
            the project name

        Returns
        -------
        projectdb : str
            the full path of the FileGeodatabase
        """
        dbname = basename(fgdb) or self.dbname
        projectname = project or self.project
        return self.join_and_check(self.get_projectpath(projectname), dbname,
                                   check=check)

    def get_table(self, tablename, fgdb='', project='', check=True):
        """
        A Table in a FileGeodatabase in the Project Folder

        Parameters
        ----------
        tablename : str
        fgdb : str, optional
            the name of the FileGeodatabase
        project : str, optional
            the project name

        Returns
        -------
        table : str
            the full path to a table in the FileGeodatabase
        """
        dbname = basename(fgdb) or self.dbname
        projectname = project or self.project
        table = self.join_and_check(self.get_db(dbname, projectname),
                                    tablename,
                                    check=check)
        return table

    def get_basedb(self, fgdb, check=True):
        """
        A Base FileGeodatabase

        Parameters
        ----------
        fgdb : str
            the name of the FileGeodatabase

        Returns
        -------
        basedb : str
            the full path of the FileGeodatabase
        """
        return self.join_and_check(self.BASE_DBS, fgdb, check=check)

    def get_base_table(self, fgdb, table, check=True):
        """
        A Table in a Base FileGeodatabase

        Parameters
        ----------
        fgdb : str
            the name of the FileGeodatabase
        tablename : str
            the name of the table
        check : bool
            if false, don't check if table exists

        Returns
        -------
        base_table : str
            the full path to the table in the Base FileGeodatabase
        """
        dbname = basename(fgdb)
        table = self.join_and_check(self.get_basedb(dbname), table,
                                    check=check)
        return table

    def update_table(self, table, column_values, where=None, fgdb='',
                     project='', check=True):
        """
        Update rows in a FileGeodatabase in the Project Folder

        Parameters
        ----------
        table : str
            the name of the table
        column_values: dict,
            the columns and the values to update them with as key/value-pairs
        where: str, optional
            a where clause to pick single rows
        fgdb : str, optional
            the name of the FileGeodatabase
        project : str, optional
            the project name
        check : bool, optional
            if false, don't check if table exists
        """
        table = self.get_table(table, fgdb=fgdb, project=project, check=True)
        columns = column_values.keys()
        cursor = arcpy.da.UpdateCursor(table, columns, where_clause=where)
        for row in cursor:
            for i, column in enumerate(columns):
                row[i] = column_values[column]
            cursor.updateRow(row)
        del cursor

    def get_layer(self, layername, folder=''):
        """
        A lyr-file

        Parameters
        ----------
        layername : str
            the name of the lyr-file

        folder : str, optional
            a subfolder

        Returns
        -------
        layer : str
            the full path to the lyr-file
        """
        layerfile = '{}.lyr'.format(layername)
        layer = self.join_and_check(self.TEMPLATE_LAYERFOLDER, folder, layerfile)
        return layer
