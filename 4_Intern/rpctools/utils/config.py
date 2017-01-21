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
from os.path import join, isdir, abspath, dirname, basename


########################################################################
class Folders(object):
    """"""
    def __init__(self, params=None):
        """class that returns path"""
        self.BASE_PATH = abspath(join(dirname(__file__),'..', '..', '..'))
        self._PROJECT_FOLDER = '3_Projekte'
        self._INTERN = '4_Intern'
        self._BASE_DBS = 'fgdbs'
        self._TEMPLATE_FOLDER = 'templates'
        self._TEMPLATE_FLAECHEN = 'projektflaechen_template.shp'
        self._PROJECT_TEMPLATE = 'Template'
        self._TEST_TEMPLATE = 'Test_Template'
        self._TEST_TMP_PROJECT = '__unittest__'
        self._AUSGABE_PATH = 'Ergebnisausgabe'
        self._TEXTE = 'texte'
        self._MXDS = 'mxds'
        self.PYTHON_EXECUTABLE = u'C:\\Python27-ArcGIS\\ArcGIS10.4'
        # the params
        self._params = params

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
        return join(self.BASE_PATH, self._INTERN)

    @property
    def BASE_DBS(self):
        return join(self.INTERN, self._BASE_DBS)

    @property
    def MXDS(self):
        return join(self.INTERN, self._MXDS)

    @property
    def TEXTE(self):
        return join(self.INTERN, self._TEXTE)

    @property
    def PROJECT_FOLDER(self):
        return join(self.BASE_PATH, self._PROJECT_FOLDER)

    @property
    def TEMPLATE_FOLDER(self):
        return join(self.BASE_PATH, self._INTERN, self._TEMPLATE_FOLDER)

    @property
    def TEMPLATE_FLAECHEN(self):
        return join(self.TEMPLATE_FOLDER, self._TEMPLATE_FLAECHEN)

    @property
    def PROJECT_TEMPLATE(self):
        return join(self.TEMPLATE_FOLDER, self._PROJECT_TEMPLATE)

    @property
    def TEST_TEMPLATE(self):
        return join(self.TEMPLATE_FOLDER, self._TEST_TEMPLATE)

    @property
    def TEST_TMP_PROJECT(self):
        return join(self.PROJECT_FOLDER, self._TEST_TMP_PROJECT)

    def get_projects(self):
        '''
        returns all available projects inside the project folder
        (except the template and temp. projects which are not meant to be edited)
        '''
        subfolders = [f for f in listdir(self.PROJECT_FOLDER)
                      if isdir(self.get_projectpath(f))
                      and f not in [self._PROJECT_TEMPLATE,
                                    self._TEST_TEMPLATE,
                                    self._TEST_TMP_PROJECT
                                    ]
                      ]
        return sorted(subfolders)

    def get_projectpath(self, project=None):
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
        return join(self.PROJECT_FOLDER, projectname)

    @property
    def PROJECT_PATH(self):
        """The Projectpath"""
        return self.get_projectpath()

    @property
    def AUSGABE_PATH(self):
        """The Projectpath"""
        return join(self.PROJECT_PATH, self._AUSGABE_PATH)

    def get_db(self, fgdb='', project=''):
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
        return join(self.get_projectpath(projectname), dbname)

    def get_table(self, tablename, fgdb='', project=''):
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
        table = join(self.get_db(dbname, projectname), tablename)
        return table

    def get_basedb(self, fgdb):
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
        return join(self.BASE_DBS, fgdb)

    def get_base_table(self, fgdb, table):
        """
        A Table in a Base FileGeodatabase

        Parameters
        ----------
        fgdb : str
            the name of the FileGeodatabase
        tablename : str
            the name of the table

        Returns
        -------
        base_table : str
            the full path to the table in the Base FileGeodatabase
        """
        dbname = basename(fgdb)
        table = join(self.get_basedb(dbname), table)
