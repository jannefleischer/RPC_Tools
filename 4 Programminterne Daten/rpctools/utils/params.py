# -*- coding: utf-8 -*-

import gc
import sys
import os
from abc import ABCMeta, abstractmethod, abstractproperty
from rpctools.utils.config import Folders
from rpctools.utils.config import Config
from rpctools.utils.output import Output, ArcpyEnv
from rpctools.utils.message import Message
from rpctools.utils.singleton import Singleton
from rpctools.utils.param_module import Params
from rpctools.utils.arcpy_parameter import Parameter
import arcpy


class ToolFolders(Folders):
    def join_and_check(self, *args, **kwargs):
        """
        Joins paths and checks if joined path points to existing resource
        (directory, database or table) if requested

        overrides check function to show path errors while running and exit
        when first error occurs

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
        path = os.path.join(*args)
        check = kwargs.get('check', True)
        if check and not arcpy.Exists(path):
            arcpy.AddError(
                'Pfad oder Tabelle existiert nicht: "{}"'.format(path))
            sys.exit()
        return path


class Tool(object):
    """
    Base Class for a ArcGIS Tool

    Attributes
    ----------
    folders : Folders object
        gives access to relative paths

    mes : Message object
        for sending messages to ArcGIS
    """
    __metaclass__ = ABCMeta

    _param_projectname = 'projectname'
    """The parameter that holds the projectname"""
    _dbname = None
    """the name of the default database of the tool"""

    def __init__(self, params, parent_tbx):
        """
        Parameters
        ----------
        params : Params object
        parent_tbx: Tbx object, the toolbox the Tool belongs to
                    (=the calling toolbox)
        """
        self.par = params
        self.mes = Message()
        self.parent_tbx = parent_tbx
        self.folders = ToolFolders(params=self.par)
        self.output = Output(folders=self.folders, params=params,
                             parent_tbx=parent_tbx)

    def main(self, par, parameters=None, messages=None):
        """
        The main method

        Parameters
        ----------
        par : the Params-object

        parameters : the list of parameters sent by ArcGIS

        messages : the messages-object sent by ArcGIS
        """
        self.par = par
        if parameters:
            self.par._update_parameters(parameters)
        if messages:
            self.mes = messages
        gc.collect()
        # Set the progressor
        arcpy.SetProgressor("step",
                            "Executing Tool {}...".format(self.__class__),
                            0, 100, 1)
        self.run()
        arcpy.ResetProgressor()

    @property
    def db(self):
        """ The full path to the default Database of the tool"""
        return self.folders.get_db()

    @property
    def projectname(self):
        """Return the current projectname"""
        return self.par._get_projectname()

    @abstractmethod
    def run(self):
        """The run method - has to be implemented in the subclass"""


class Dependency(object):
    """Class for defining dependencies between multiple paramaters and updating
    their values according to the defined target"""
    def __init__(self, param_names, target_value, type='sum'):
        """
        Parameters
        ----------
        param_names : list of str
                names of the parameters depending on each other
        target_value : the targeted value
        type : str, optional
                the type of the dependency (atm only sum, may be extended to
                other cases in the future)
        """

        self.param_names = param_names
        self.target_value = target_value
        self.type = type

    def update(self, params):
        """
        check if dependent params were altered and set them to target value

        Parameters
        ----------
        params : Param object
        """
        if self.type == 'sum':
            self._set_sum(params)

    def _set_sum(self, params):
        """set values of dependent parameters to sum up to target value"""
        actual_sum = 0
        altered = False
        for name in self.param_names:
            param = params[name]
            altered = altered or param.altered
            actual_sum += param.value

        if not altered:
            return

        if actual_sum != self.target_value:
            difference = self.target_value - actual_sum
            for name in reversed(self.param_names):
                param = params[name]
                old_val = param.value
                new_val = param.value + difference
                if new_val < 0:
                    new_val = 0
                elif new_val > self.target_value:
                    new_val = self.target_value
                difference = difference + old_val - new_val
                param.value = new_val


class Tbx(object):
    """Base Class for a ArcGIS Toolbox"""
    __metaclass__ = ABCMeta
    __metaclass__ = Singleton

    _temp_table_prefix = 'RPC_Tools'
    # name of temp. tables, project needs to be appended
    _temp_table_name = (
        _temp_table_prefix +
        '_{class_name}_{source_db}_{source_table}_'
    )

    config = Config()

    @abstractproperty
    def Tool(self):
        """
        Returns the Toolclass

        To be defined in the subclass
        """

    @abstractproperty
    def label(self):
        """
        Returns the label as string

        To be defined in the subclass
        """

    @property
    def projects_changed(self):
        """projects that were changed (only works if toolbox works with
        temporary databases)"""
        return self.folders.get_temporary_projects()

    def __init__(self):

        # ggf. später reload entfernen???
        Tool = self.reload_tool()

        # the parameters
        self.par = Params(param_projectname=Tool._param_projectname,
                          dbname=Tool._dbname)
        # define the folders
        self.folders = Folders(params=self.par)
        self.projects = []
        # an instance of the tool
        self.tool = Tool(self.par, self)
        self.canRunInBackground = False
        # update projects on call of updateParameters
        self.update_projects = True
        self._dependencies = []
        # updates to these tables are written to temp. tables and written to
        # project db only on execution of tool
        self._temporary_gdbs = []

        self.recently_opened = False

    def reload_tool(self):
        """reload the tool's module"""
        tool_module_name = self.Tool.__module__
        reload(sys.modules[tool_module_name])
        tool_name = self.Tool.__name__
        tool_module = __import__(tool_module_name,
                                 globals(),
                                 locals(),
                                 [tool_name],
                                 -1)
        Tool = getattr(tool_module, tool_name)
        return Tool

    @abstractmethod
    def _getParameterInfo(self):
        """
        Define the Parameters and return a list or Params()-instance with the
        parameter
        """

    def add_parameter(self, param_name):
        """
        Add a (patched) arcpy-parameter and return this parameter

        Parameters
        ----------
        param_name : str

        Returns
        -------
        parameter : arcpy.Parameter-instance
        """
        parameter = self.par[param_name] = Parameter()
        return parameter

    def getParameterInfo(self):
        """
        Define the Parameters and return a list or Params()-instance with the
        parameter
        """
        self.folders._invalid_paths = []
        params = self._getParameterInfo()._od.values()
        return params

    def isLicensed(self):
        """If toolbox is licenced"""
        return True

    def updateParameters(self, parameters):
        """
        The updateParameters-method called by ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters
        """

        self.par._update_parameters(parameters)
        # if a toolbox is opened, remove ALL temporary databases
        if self.par.toolbox_opened():
            self.clear_temporary_dbs()
            self.recently_opened = True
            # updating projects messes up the initial project management
            if self.update_projects:
                self._set_active_project()
        else:
            self.recently_opened = False
        # updating projects messes up the initial project management
        if self.update_projects:
            self._update_project_list()
        self._update_dependencies(self.par)
            #self._create_temporary_copies()
        self._updateParameters(self.par)

    def _set_active_project(self):
        active_project = self.config.active_project
        project_param = self.par[self.par._param_projectname]
        project_param.filter.list = []
        project_param.value = active_project
        project_param.enabled = False

    def _validate_active_project(self):
        active_project = self.config.active_project
        projects = self.folders.get_projects()
        if not active_project:
            return False, (u'Kein aktives Projekt ausgewählt!')
        elif active_project not in projects:
            return False, (u'Aktives Projekt kann nicht gefunden werden!')
        return True, ''

    def _update_project_list(self):
        """
        Update the parameter list of existing projects
        """
        if self.par._param_projectname not in self.par:
            return
        projects = self.folders.get_projects()
        project_param = self.par[self.par._param_projectname]
        if projects == project_param.filter.list:
            return
        project_param.filter.list = projects
        if len(projects) == 0:
            project_param.value = ''
        # if previously selected project was deleted in the meantime
        elif project_param.value not in projects:
            project_param.value = projects[0]

    def _check_project(self):
        pass

    def add_dependency(self, param_names, target_value, type='sum'):
        """
        define a dependency between different parameters, they have to sum up
        to a target value.
        if one of them is changed, the others will be auto set while updating
        the parameters

        Parameters
        ----------
        param_names : list,
               qualified names of the parameters

        target_sum : int
               the target value the parameters sum up to

        type : str, optional
               only 'sum' supported atm
        """
        dependency = Dependency(param_names, target_value, type=type)
        self._dependencies.append(dependency)

    def _update_dependencies(self, params):
        """check if dependent params were altered and set them to target sum"""
        for dependency in self._dependencies:
            dependency.update(params)

    def _updateParameters(self, params):
        """
        Update the Parameters if something changed

        To define in the subclass
        """

    def updateMessages(self, parameters):
        """
        The updateMessages-method called by ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters
        """
        self.par._update_parameters(parameters)
        params = self.par._od.values()
        if self.update_projects:
            valid, message = self._validate_active_project()
            if not valid:
                params[0].setErrorMessage(message)
                return
        # check if toolbox contains invalid paths, add errors to first param.
        if params and self.folders._invalid_paths:
            invalid = ', '.join(self.folders._invalid_paths)
            params[0].setErrorMessage(
                'Pfade oder Tabellen existieren nicht: {}'.format(invalid))
        self._updateMessages(self.par)

    def _updateMessages(self, parameters):
        """ to define in the subclass """

    def update_table(self,
                     table,
                     column_values,
                     where=None,
                     pkey=None,
                     fgdb=''):
        """
        Update rows in a FileGeodatabase with given values

        Parameters
        ----------
        table : str
            table name
        column_values: dict,
            the columns and the values to update them with as key/value-pairs
        where: str, optional
            a where clause to pick single rows
        pkey: dict, optional
            the columns and the values of the primary key as key/value-pairs
        fgdb : str, optional
            the database name

        Returns
        -------
        r : int
            the number of updated rows
        """
        where = where or self.get_where_clause(pkey)
        table_path = self._get_table_path(fgdb, table)
        columns = column_values.keys()
        cursor = arcpy.da.UpdateCursor(table_path, columns, where_clause=where)
        r = 0
        for row in cursor:
            for i, column in enumerate(columns):
                row[i] = column_values[column]
            cursor.updateRow(row)
            r += 1
        del cursor
        return r

    def delete_rows_in_table(self,
                             table,
                             pkey,
                             fgdb='',
                             ):
        """
        Delete rows in a FileGeodatabase which match the where-clause

        Parameters
        ----------
        table : str
            full path to the table
        pkey: dict
            the columns and the values of the primary key as key/value-pairs
        fgdb : str, optional
            the database name

        Returns
        -------
        r : int
            the number of deleted rows
        """
        where = self.get_where_clause(pkey)
        table_path = self._get_table_path(fgdb, table)
        columns = pkey.keys()
        cursor = arcpy.da.UpdateCursor(table_path, columns, where_clause=where)
        r = 0
        for row in cursor:
            cursor.deleteRow()
            r += 1
        del cursor
        return r

    def _get_table_path(self, fgdb, table):
        """
        return the full table path,
        return the temporary fgdb, if db is handled temporarly (creates the
        temporary table if it does not exist yet)
        """
        dbname = os.path.basename(fgdb) or self.tool._dbname
        table = os.path.basename(table)
        # if table is in temp. management -> write to temporary table instead
        if dbname in self._temporary_gdbs:
            temp_db = self.folders.get_temporary_db(fgdb=fgdb, check=False)
            # create on demand
            if not arcpy.Exists(temp_db):
                self._create_temporary_copy(fgdb)
            table_path = self.folders.get_temporary_table(table, fgdb=fgdb)
        else:
            table_path = self.folders.get_table(table, workspace=fgdb)
        return table_path

    def insert_row_in_table(self, table, column_values, fgdb=''):
        """
        insert new row
        in a FileGeodatabase with given values

        Parameters
        ----------
        table : str
            full path to the table
        column_values: dict,
            the columns and the values to insert as key/value-pairs
        fgdb : str, optional
            the database name
        """
        table_path = self._get_table_path(fgdb, table)
        columns = column_values.keys()
        values = column_values.values()
        cursor = arcpy.da.InsertCursor(table_path, columns)
        cursor.insertRow(values)
        del cursor

    def upsert_row_in_table(self, table, column_values, pkey, fgdb=''):
        """
        update a row, or - if it does not exist yet - insert the row
        in a FileGeodatabase with given values

        Parameters
        ----------
        table : str
            full path to the table
        column_values: dict,
            the columns and the values to insert as key/value-pairs
        pkey: dict,
            the columns and the values of the primary key as key/value-pairs
        fgdb : str, optional
            the database name
        """
        where_clause = self.get_where_clause(pkey)
        # try to update the row
        r = self.update_table(table, column_values, where=where_clause,
                              fgdb=fgdb)
        # if there are no rows matching the primary key
        if not r:
            # insert new row
            column_values.update(pkey)
            self.insert_row_in_table(table, column_values, fgdb)

    def get_where_clause(self, pkey):
        """
        convert a primary key dict to a where_clause

        Parameters
        ----------
        pkey : dict
            key-value-Pairs of columns and values

        Returns
        -------
        where_clause : str
        """
        if pkey is None:
            return None
        where_clause = ' AND '.join(["{} = {}".format(k, v)
                                     if not isinstance(v, (str, unicode))
                                     else "{} = '{}'".format(k, v)
                                     for (k, v) in pkey.iteritems()
                                     ])
        return where_clause

    def query_table(self, table, columns, fgdb='', where=None, pkey=None):
        """
        get rows from a FileGeodatabase with given values

        Parameters
        ----------
        table : str
            full path to the table
        columns: list,
            the requested columns
        where: str, optional
            a where clause to pick single rows
        pkey: dict, optional

        Returns
        -------
        rows : list of lists
            the queried rows with values of requested columns in same order as
            in columns argument
        """
        where = where or self.get_where_clause(pkey)
        table = os.path.basename(table)
        dbname = os.path.basename(fgdb) or self.tool._dbname
        table_path = self.folders.get_table(table, workspace=fgdb)
        if dbname in self._temporary_gdbs:
            temp_db = self.folders.get_temporary_db(fgdb=fgdb, check=False)
            # only query temp. db if it exists (created on demand in update)
            if arcpy.Exists(temp_db):
                table_path = self.folders.get_temporary_table(table, fgdb=fgdb)
        cursor = arcpy.da.SearchCursor(table_path, columns, where_clause=where)
        rows = [row for row in cursor]
        del cursor
        return rows

    def clear_temporary_dbs(self):
        """remove all temporary gdbs"""
        for project in self.folders.get_temporary_projects():
            path = self.folders.get_temporary_projectpath(project=project)
            #for fgdb in self._temporary_gdbs:
                #path = self.folders.get_temporary_db(fgdb=fgdb, project=project,
                                                     #check=False)
            if arcpy.Exists(path):
                arcpy.Delete_management(path)

    def add_temporary_management(self, fgdb=''):
        """
        add a FileGeoDatabase to be managed temporarly,
        all updates on their tables happen inside the temporary database,
        the changes made are only transferred into the project database after
        pressing OK in the UI

        Parameters
        ----------
        fgdb : str
            name of the FileGeoDatabase
        """
        if fgdb not in self._temporary_gdbs:
            self._temporary_gdbs.append(fgdb)

    def _create_temporary_copy(self, fgdb=''):
        """
        make a copy of a project fgdbs in the given temporary table
        """
        project_db = self.folders.get_db(workspace=fgdb)
        temp_db = self.folders.get_temporary_db(fgdb=fgdb, check=False)
        if arcpy.Exists(temp_db):
            arcpy.Delete_management(temp_db)
        # deactivate adding of temp. gdbs to table of contents
        with ArcpyEnv(addOutputsToMap=False):
            arcpy.Copy_management(project_db, temp_db)

    def _commit_temporaries(self):
        """transfer all changes made in temporary tables into project tables"""
        gc.collect()

        arcpy.AddMessage(
            u'Getätigte Änderungen werden in das Projekt übernommen...'.encode('latin1'))

        with ArcpyEnv(overwriteOutput=True):
            changes = 0
            for project in self.folders.get_temporary_projects():
                for fgdb in self._temporary_gdbs:
                    project_db = self.folders.get_db(workspace=fgdb,
                                                     project=project)
                    temp_db = self.folders.get_temporary_db(fgdb=fgdb,
                                                            project=project,
                                                            check=False)
                    # temporary dbs only exist,
                    # if changes were made (else nothing to do here)
                    if arcpy.Exists(temp_db):
                        changes += self._replace_with_tempdb(temp_db,
                                                             project_db)
                arcpy.AddMessage(
                    '{} Datenbank(en) wurden erfolgreich geändert'.format(changes))

    def _replace_with_tempdb(self, temp_db, project_db):
        """
        replace project_db with temp_db

        Parameters
        ----------
        temp_db : str
        project_db : str
        """
        self.tool.output.change_layers_workspace(project_db, temp_db)
        res = arcpy.Compact_management(project_db)
        del res
        arcpy.Delete_management(project_db)
        arcpy.Copy_management(temp_db, project_db)
        # repair datasource of layers that reference the project_db
        # which was temporarily deleted
        self.tool.output.change_layers_workspace(temp_db, project_db)
        return 1

    def execute(self, parameters=None, messages=None):
        """
        Run the tool with the parameters and messages from ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters

        messages : the message-object of ArcGIS

        """
        self._commit_temporaries()
        self.tool.main(self.par, parameters, messages)
        self.clear_temporary_dbs()

    def print_test_parameters(self):
        """
        Print the parameters to use in tests

        Examples
        --------
        >> tbx.print_test_parameters()
        ### Category 1 ###
        params.param_1.value = 123
        params.param_2.value = 456
        ### Category 2 ###
        params.param_3.value = 'DefaultString'
        """
        params = self._getParameterInfo()
        self._updateParameters(params)
        category = None
        for k, v in self.par._od.iteritems():
            if v.category and v.category != category:
                category = v.category
                print(u'### {} ###'.format(v.category))
            value = v.value
            if isinstance(value, (str, unicode)):
                value = u"'{}'".format(value)
            print (u'params.{k}.value = {v}'.format(v=value, k=k))

    def print_tool_parameters(self):
        """
        Print the parameters to use in a Tool

        Examples
        --------
        >> tbx.print_tool_parameters()
        ### Category 1 ###
        param_1 = params.param_1.value
        param_2 = params.param_2.value
        ### Category 2 ###
        param_3 = params.param_3.value
        """
        self._getParameterInfo()
        category = None
        for k, v in self.par._od.iteritems():
            if v.category and v.category != category:
                category = v.category
                print(u'### {} ###'.format(v.category))
            print (u'{k} = self.par.{k}.value'.format(k=k))


    def rename_params_in_tool(self):
        """
        rename parameters[n] into params.param_xyz in the Tools's module
        and save under new name tool_OLDNAME.py
        """
        module = sys.modules[self.Tool.__module__]
        path = module.__file__.rstrip('co')
        with open(path, 'r') as original_file:
            src = original_file.read()

        stub = 'parameters[{}].value'
        self._getParameterInfo()
        for i, key in enumerate(self.par._od):
            src = src.replace(stub.format(i), key)

        new_basename = 'tool_{}'.format(os.path.basename(path))
        new_fn = os.path.join(os.path.dirname(path), new_basename)

        with open(new_fn, 'w') as new_file:
            new_file.write(src)



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
