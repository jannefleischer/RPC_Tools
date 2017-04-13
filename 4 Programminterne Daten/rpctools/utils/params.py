# -*- coding: utf-8 -*-

from collections import OrderedDict
import gc
import sys
import os
import numpy as np
from pprint import pformat
from abc import ABCMeta, abstractmethod, abstractproperty
from rpctools.utils.config import Folders
#reload(sys.modules[Folders.__module__])
import arcpy


class Message(object):

    @staticmethod
    def addMessage(message):
        arcpy.AddMessage(message)
        print(message)

    @staticmethod
    def addErrorMessage(message):
        arcpy.AddError(message)
        print(message)

    @staticmethod
    def addWarningMessage(message):
        arcpy.AddWarning(message)
        print(message)

    @staticmethod
    def addIDMessage(message, message_ID,
                     add_argument1=None, add_argument2=None):
        arcpy.AddIDMessage(message, message_ID,
                           add_argument1=add_argument1, add_argument2=add_argument2)
        print(message)

    @staticmethod
    def addGPMessages():
        arcpy.AddMessage('')

    @staticmethod
    def AddMessage(message):
        arcpy.AddMessage(message)
        print(message)

    @staticmethod
    def AddErrorMessage(message):
        arcpy.AddError(message)
        print(message)

    @staticmethod
    def AddWarningMessage(message):
        arcpy.AddWarning(message)
        print(message)

    @staticmethod
    def AddIDMessage(message, message_ID,
                     add_argument1=None, add_argument2=None):
        arcpy.AddIDMessage(message, message_ID,
                           add_argument1=add_argument1,
                           add_argument2=add_argument2)
        print(message)

    @staticmethod
    def AddGPMessages():
        arcpy.AddMessage('')


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Params(object):
    """Parameter class like an ordered dict"""

    def __init__(self,
                 param_projectname='name',
                 dbname='',
                 *args, **kwargs):
        """
        Parameters
        ----------
        param_projectname : str (optional, default='name')
            the name of the project_name-Parameter
        param_dbname : str (optional)
            the name of the Default Database for the Tool

        Examples
        --------
        >>> params = Params()
        >>> params.param1 = 99
        >>> params.param2 = 42
        >>> params.param3 = 123

        >>> len(params)
        3
        >>> params[0]
        99
        >>> params[1]
        42
        >>> params.param2
        42
        >>> params.param1
        99
        >>> params['param2']
        42
        >>> for param in params:
        ...     print(param)
        99
        42
        123
        >>> del params.param1
        >>> params.param1
        Traceback (most recent call last):
            ...
        AttributeError: Attribute param1 not found in Params-instance. Available attributes are ['param2', 'param3']
        >>> params[0]
        42
        >>> params[1]
        123
        >>> params[2]
        Traceback (most recent call last):
            ...
        IndexError: list index out of range
        >>> del params[0]
        >>> params[0]
        123
        >>> params.param3
        123
        >>> params.param4 = 444
        >>> params.param5 = 555
        >>> params[:2]
        [123, 444]
        >>> params[1:3]
        [444, 555]
        >>> 'param5' in params
        True
        >>> 'param6' in params
        False
        """
        self._od = OrderedDict(*args, **kwargs)
        self._param_projectname = param_projectname
        self._dbname = dbname

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        try:
            return self._od[name]
        except KeyError:
            msg = 'Attribute {} not found in Params-instance. Available attributes are {}'.format(name, self._od.keys())
            raise AttributeError(msg)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._od[name] = value

    def __delattr__(self, name):
        del self._od[name]

    def __getitem__(self, i):
        try:
            return self._od.values()[i]
        except TypeError:
            return self._od[i]

    def __setitem__(self, i, value):
        try:
            self._od.items()[i] = value
        except TypeError:
            self._od[i] = value

    def __delitem__(self, i):
        try:
            del self._od[i]
        except KeyError:
            del self._od[self._od.keys()[i]]

    def __iter__(self):
        return self._od.itervalues()

    def __contains__(self, value):
        return value in self._od

    def __len__(self):
        return len(self._od)

    def __getslice__(self, start, stop):
        return self._od.values().__getslice__(start, stop)

    def __repr__(self):
        ret = self._od.items()
        return pformat(ret)

    def _update_parameters(self, parameters):
        """update the parameter values with a list of parameters"""
        n_params_tbx = len(self)
        n_params_tool = len(parameters)
        msg = '{} Parameter der Toolbox passen nicht zu den {} Parametern des Tools'
        assert n_params_tbx == n_params_tool, msg.format(n_params_tbx,
                                                         n_params_tool)
        # setze die Werte
        for i, key in enumerate(self._od):
            self[key]._arc_object = parameters[i]

    def _get_projectname(self):
        """
        return the value for project name parameter if exists, else empty string

        Returns
        -------
        projectname : str
        """
        param_projectname = getattr(self, self._param_projectname, None)
        if param_projectname:
            return param_projectname.value
        return ''

    def changed(self, *names):
        """check parameter with names if thy are altered and not validated"""
        change = False
        for name in names:
            param = self._od[name]
            if param.altered and not param.hasBeenValidated:
                change = True
        return change

    def toolbox_opened(self):
        """return True if toolbox was opened just before last update"""
        opened = not any([p.hasBeenValidated for p in self])
        return opened

    def selected_index(self, name):
        """get the index of the current selection of given list-parameter"""
        param = self._od[name]
        index = param.filter.list.index(param.value)
        return index

    def get_multivalues(self, name):
        """
        return a numpy recarray with the values of a value table

        Parameters
        ----------
        name : str
            the name of the value-table parameter

        Returns
        -------
        ra : np.recarray
            the values as np.recarray. The column names are defined
            by the param.columns
        """
        param = getattr(self, name)
        if not param.datatype == 'GPValueTable':
            raise ValueError('{} is no ValueTable'.format(name))
        column_names = [p[1] for p in param.columns]
        ra = np.rec.fromrecords(param.values, names=column_names)
        return ra

    def set_multivalues(self, name, values):
        """
        set the values of a value table with the values
        given as a recarray

        Parameters
        ----------
        name : str
            the name of the value-table parameter
        values : np.recarray
            the values to assign to the parameter
        """
        msg = 'values must be a recarray and not {}'.format(type(ra).__name__)
        assert isinstance(values, np.rec.recarray), msg
        param = getattr(self, name)
        if not param.datatype == 'GPValueTable':
            raise ValueError('{} is no ValueTable'.format(name))
        param.values = ra.tolist()


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

    def __init__(self, params):
        """
        Parameters
        ----------
        params : Params object
        """
        self.par = params
        self.mes = Message()
        self.folders = ToolFolders(params=self.par)
        self.output = Output(folders=self.folders, params=params)

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
        self.run()

    @property
    def db(self):
        """ The full path to the default Database of the tool"""
        return self.folders.get_db()

    @abstractmethod
    def run(self):
        """The run method - has to be implemented in the subclass"""


class Dependency():
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

    def __init__(self):
        # todo: replace later with Tool=self.Tool
        Tool = self.reload_tool()

        # the parameters
        self.par = Params(param_projectname=Tool._param_projectname,
                          dbname=Tool._dbname)
        # define the folders
        self.folders = Folders(params=self.par)
        self.projects = []
        # an instance of the tool
        self.tool = Tool(self.par)
        self.canRunInBackground = False
        # update projects on call of updateParameters
        self.update_projects = True
        self._dependencies = []
        # updates to these tables are written to temp. tables and written to
        # project db only on execution of tool
        self._temporary_gdbs = []

        self.recently_opened = False

    def reload_tool(self):
        # reload the tool's module
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
        #with open(r'C:\Users\JMG.GGRS\Desktop\test.txt', 'a') as f:
            #f.write('just opened: {}\n'.format(self.par.toolbox_opened()))
        if self.par.toolbox_opened():
            self.clear_temporary_dbs()
            self.recently_opened = True
        else:
            self.recently_opened = False
        # updating projects messes up the initial project management
        if self.update_projects:
            self._update_project_list()
        self._update_dependencies(self.par)
            #self._create_temporary_copies()
        self._updateParameters(self.par)

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
        # check if toolbox contains invalid paths, add errors to first param.
        if params and self.folders._invalid_paths:
            invalid = ', '.join(self.folders._invalid_paths)
            params[0].setErrorMessage(
                'Pfade oder Tabellen existieren nicht: {}'.format(invalid))
        self._updateMessages(self.par)

    def _updateMessages(self, parameters):
        """ to define in the subclass """

    def update_table(self, table, column_values, fgdb='', where=None):
        """
        Update rows in a FileGeodatabase with given values

        Parameters
        ----------
        table : str
            full path to the table
        column_values: dict,
            the columns and the values to update them with as key/value-pairs
        where: str, optional
            a where clause to pick single rows
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
            table_path = self.folders.get_table(table, fgdb=fgdb)
        columns = column_values.keys()
        cursor = arcpy.da.UpdateCursor(table_path, columns, where_clause=where)
        for row in cursor:
            for i, column in enumerate(columns):
                row[i] = column_values[column]
            cursor.updateRow(row)
        del cursor

    def query_table(self, table, columns, fgdb='', where=None):
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

        Returns
        -------
        rows : list of lists
            the queried rows with values of requested columns in same order as
            in columns argument
        """
        table = os.path.basename(table)
        dbname = os.path.basename(fgdb) or self.tool._dbname
        table_path = self.folders.get_table(table, fgdb=fgdb)
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
        dbname = os.path.basename(fgdb) or self.dbname
        self._temporary_gdbs.append(fgdb)

    def _create_temporary_copy(self, fgdb=''):
        """make a copy of a project fgdbs in the given temporary table"""
        project_db = self.folders.get_db(fgdb=fgdb)
        temp_db = self.folders.get_temporary_db(fgdb=fgdb, check=False)
        if arcpy.Exists(temp_db):
            arcpy.Delete_management(temp_db)
        # deactivate adding of temp. gdbs to table of contents
        old_state = arcpy.env.addOutputsToMap
        arcpy.env.addOutputsToMap = False
        arcpy.Copy_management(project_db, temp_db)
        arcpy.env.addOutputsToMap = old_state

    def _commit_temporaries(self):
        """transfer all changes made in temporary tables into project tables"""
        gc.collect()
        old_state = arcpy.env.overwriteOutput
        arcpy.env.overwriteOutput = True
        for project in self.folders.get_temporary_projects():
            for fgdb in self._temporary_gdbs:
                project_db = self.folders.get_db(fgdb=fgdb, project=project)
                temp_db = self.folders.get_temporary_db(fgdb=fgdb,
                                                        project=project,
                                                        check=False)      
                if arcpy.Exists(temp_db):                    
                    #arcpy.Delete_management(project_db)
                    #arcpy.Copy_management(temp_db, project_db)                
                    dirpath, dirname, tables = arcpy.da.Walk(temp_db).next()   
                    for table in tables:
                        temp_table = os.path.join(temp_db, table)
                        project_table = os.path.join(project_db, table)
                        arcpy.Copy_management(temp_table, project_table)
        arcpy.env.overwriteOutput = old_state

    def execute(self, parameters=None, messages=None):
        """
        Run the tool with the parameters and messages from ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters

        messages : the message-object of ArcGIS

        """
        self._commit_temporaries()
        self.clear_temporary_dbs()
        self.tool.main(self.par, parameters, messages)

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
        params = self._getParameterInfo()
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


class Output():
    """
    Add and update layers to the current ArcMap file.
    """

    module = {
                "analysen" : "Analysen",
                "bevoelkerung": "Wirkungsbereich 1 - Bewohner und Arbeitsplaetze",
                "erreichbarkeit": "Wirkungsbereich 2 - Erreichbarkeit",
                "verkehr": "Wirkungsbereich 3 - Verkehr im Umfeld",
                "oekologie": "Wirkungsbereich 4 - Fläche und Ökologie",
                "infrastruktur": "Wirkungsbereich 5 - Infrastrukturfolgekosten",
                "einnahmen": "Wirkungsbereich 6 - Kommunale Steuereinnahmen",
                "standortkonkurrenz": "Wirkungsbereich 7 - Standortkonkurrenz Lebensmitteleinzelhandel",
                "projektdefinition": "Projektdefinition",
                "hintergrundkarten": "Hintergrundkarten Projekt-Check"}



    def __init__(self, folders, params):
        self.folders = folders
        self.params = params


    def set_projectlayer(self, projektname):
        """
        Check and add project layer
        """

        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame

        layer_exists = arcpy.mapping.ListLayers(
                                                    current_mxd,
                                                    projektname,
                                                    current_dataframe)
        if layer_exists:
            is_grouplayer = layer_exists[0].isGroupLayer
        else:
            is_grouplayer = False

        if not layer_exists or not is_grouplayer:
            group_layer_template = self.folders.get_layer(layername = "__Projektname__", folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            addLayer.name = projektname
            arcpy.mapping.AddLayer(current_dataframe, addLayer, "TOP")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()


    def get_projectlayer(self, projectname):
        """
        Returns project layer in table of contents
        """
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        layers = arcpy.mapping.ListLayers(current_mxd, projectname, current_dataframe)
        projectlayer = []
        for layer in layers:
            if layer.isGroupLayer:
                projectlayer = layer

        return projectlayer

    def set_headgrouplayer(self, project_layer, dataframe):
        """
        Check and add headgroup layer
        """
        if not arcpy.mapping.ListLayers(project_layer, self.module["projektdefinition"], dataframe):
            group_layer_template = self.folders.get_layer(layername = self.module["projektdefinition"], folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayerToGroup(dataframe, project_layer, addLayer, "BOTTOM")

        if not arcpy.mapping.ListLayers(project_layer, self.module["analysen"], dataframe):
            group_layer_template = self.folders.get_layer(layername = self.module["analysen"], folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayerToGroup(dataframe, project_layer, addLayer, "BOTTOM")

        if not arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"), self.module["hintergrundkarten"], dataframe):
            group_layer_template = self.folders.get_layer(layername = self.module["hintergrundkarten"], folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayer(dataframe, addLayer, "BOTTOM")


    def set_grouplayer(self, project_layer, group, dataframe, headgroup = ""):
        """
        Check and add subgroup layer
        """
        if not arcpy.mapping.ListLayers(project_layer, group, dataframe):
            group_layer_template = self.folders.get_layer(layername = group,
                folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            if headgroup == "":
                target_headgroup = self.module["analysen"]
            target_headgrouplayer = arcpy.mapping.ListLayers(project_layer, target_headgroup, dataframe)[0]
            arcpy.mapping.AddLayerToGroup(dataframe, target_headgrouplayer, addLayer, "BOTTOM")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

    def set_subgrouplayer(self, project_layer, group, subgroup, dataframe):
        """
        Check and add subgroup layer
        """
        group_layer = arcpy.mapping.ListLayers(project_layer, group, dataframe)[0]
        if not arcpy.mapping.ListLayers(group_layer, subgroup, dataframe):
            subgroup_layer_template = self.folders.get_layer(layername = subgroup,
                folder='toc', enhance = True)
            addLayer = arcpy.mapping.Layer(subgroup_layer_template)
            target_grouplayer = arcpy.mapping.ListLayers(project_layer, group, dataframe)[0]
            arcpy.mapping.AddLayerToGroup(dataframe, target_grouplayer, addLayer, "BOTTOM")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

    def add_output(self, group, featureclass, template_layer, disable_other = True, subgroup=""):
        """
        Add output layer to group

        Parameters
        ----------
        group : str
            the layer group

        featureclass : str
            the full path of the feature class, which should be converted into a layer

        template_layer : str
            full path of the template layer

        disable_other = boolean
            if true, then all other layers will be turned off

        subgroup = str
            the subgroup of the layergroup
        """

        projektname = self.params._get_projectname()
        arcpy.AddMessage(template_layer)

        # Layer-Gruppen hinuzfuegen, falls nicht vorhanden
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame

        self.set_projectlayer(projektname)
        project_layer = self.get_projectlayer(projektname)
        self.set_headgrouplayer(project_layer, current_dataframe)
        self.set_grouplayer(project_layer, group, current_dataframe)
        if subgroup != "":
            self.set_subgrouplayer(project_layer, group, subgroup, current_dataframe)

        # Neuen Layer hinzufuegen
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        target_grouplayer = arcpy.mapping.ListLayers(project_layer, group, current_dataframe)[0]
        if subgroup != "":
            target_subgrouplayer = arcpy.mapping.ListLayers(target_grouplayer, subgroup, current_dataframe)[0]
        source_layer = arcpy.mapping.Layer(template_layer)
        arcpy.AddMessage(source_layer)
        arcpy.AddMessage(featureclass)
        source_ws = arcpy.Describe(source_layer).path
        target_ws = arcpy.Describe(featureclass).path
        source_layer.findAndReplaceWorkspacePath(source_ws, target_ws)
        if subgroup == "":
            arcpy.mapping.AddLayerToGroup(current_dataframe, target_grouplayer, source_layer, "BOTTOM")
        else:
            arcpy.mapping.AddLayerToGroup(current_dataframe, target_subgrouplayer, source_layer, "BOTTOM")

        # Auf Layer zentrieren
        new_layer = arcpy.mapping.ListLayers(project_layer, source_layer.name, current_dataframe)[0]
        ext = new_layer.getExtent()
        current_dataframe.extent = ext
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

        if disable_other == True:
            for lyr in arcpy.mapping.ListLayers(project_layer):
                lyr.visible = False
        new_layer.visible = True
        if subgroup != "":
            target_subgrouplayer.visible = True
        target_grouplayer.visible = True
        project_layer.visible = True
        if group in [self.module["verkehr"], self.module["einnahmen"], self.module["erreichbarkeit"],
                        self.module["infrastruktur"], self.module["oekologie"], self.module["standortkonkurrenz"],
                        self.module["bevoelkerung"]]:
            arcpy.mapping.ListLayers(project_layer, self.module["analysen"], current_dataframe)[0].visible = True
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

    def delete_output(self, layer):

        projektname = self.params._get_projectname()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        project_layer = self.get_projectlayer(projektname)

        if project_layer:
            layer_exists = arcpy.mapping.ListLayers(project_layer, layer, current_dataframe)
            if layer_exists:
                arcpy.mapping.RemoveLayer(current_dataframe, layer_exists[0])

        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

    def update_output(self, group, layername ):
        """"""
        projektname = self.params._get_projectname()

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
