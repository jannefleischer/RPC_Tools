# -*- coding: utf-8 -*-

from collections import OrderedDict
import gc
import sys
import os
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

    def param_altered(self):
        return [p for p in self.values() if p.altered]


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


class Tbx(object):
    """Base Class for a ArcGIS Toolbox"""
    __metaclass__ = ABCMeta
    __metaclass__ = Singleton

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
        self.update_projects = True

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
        # updating projects messes up the initial project management
        if self.update_projects:
            self._update_project_list()
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

    def execute(self, parameters=None, messages=None):
        """
        Run the tool with the parameters and messages from ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters

        messages : the message-object of ArcGIS

        """
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


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
