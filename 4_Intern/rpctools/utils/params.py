# -*- coding: utf-8 -*-

from collections import OrderedDict
import gc
import sys
from pprint import pformat
from abc import ABCMeta, abstractmethod, abstractproperty
from config import Folders
#reload(sys.modules[Folders.__module__])
import arcpy


class Message(object):

    def addMessage(self, message):
        arcpy.AddMessage(message)
        print(message)
        
    def addErrorMessage(self, message):
        arcpy.AddError(message)
        print(message)
        
    def addWarningMessage(self, message):
        arcpy.AddWarning(message)
        print(message)

    def addIDMessage(self, message, message_ID, add_argument1=None, add_argument2=None):
        arcpy.AddIDMessage(message, message_ID, add_argument1=add_argument1, add_argument2=add_argument2)
        print(message)

    def addGPMessages(self):
        arcpy.AddMessage()

    def AddMessage(self, message):
        arcpy.AddMessage(message)
        print(message)
        
    def AddErrorMessage(self, message):
        arcpy.AddError(message)
        print(message)
        
    def AddWarningMessage(self, message):
        arcpy.AddWarning(message)
        print(message)

    def AddIDMessage(self, message, message_ID, add_argument1=None, add_argument2=None):
        arcpy.AddIDMessage(message, message_ID, add_argument1=add_argument1, add_argument2=add_argument2)
        print(message)

    def AddGPMessages(self):
        arcpy.AddMessage()


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
                 dbname=None,
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
        """
        self._od = OrderedDict(*args, **kwargs)
        self._param_projectname = param_projectname
        self._dbname = dbname

    def __getattr__(self, name):
        try:
            return self._od[name]
        except KeyError:
            raise AttributeError('Attribute {} not found in Params-instance. Available attributes are {}'.format(name, self._od.keys()))

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

    def __len__(self):
        return len(self._od)

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
            self[key] = parameters[i]

    def _get_projectname(self):
        """
        return the value for project name parameter if exists, else None

        Returns
        -------
        projectname : str
        """
        param_projectname = getattr(self, self._param_projectname, None)
        if param_projectname:
            return param_projectname.value
        return None


class Tool(object):
    __metaclass__ = ABCMeta

    _param_projectname = 'projectname'
    _dbname = None

    """Base Class for a ArcGIS Tool"""
    def __init__(self, params):
        self.par = params
        self.mes = Message()
        self.folders = Folders(params=self.par)

    def main(self, par, parameters=None, messages=None):
        self.par = par
        if parameters:
            self.par._update_parameters(parameters)
        if messages:
            self.mes = messages
        gc.collect()
        self.run()

    @property
    def db(self):
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
        # reload the tool's module
        #reload(sys.modules[self.Tool.__module__])
        
        # the parameters
        self.par = Params(param_projectname=self.Tool._param_projectname,
                          dbname=self.Tool._dbname)
        # define the folders
        self.folders = Folders(params=self.par)
        # an instance of the tool
        self.tool = self.Tool(self.par)
        self.canRunInBackground = False

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
        return self._getParameterInfo()._od.values()

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Update the Parameters if something changed"""
        self.par._update_parameters(parameters)
        self._updateParameters(self.par)

    def _updateParameters(self, params):
        """Update the Parameters if something changed"""

    def updateMessages(self, parameters):
        """"""
        self.par._update_parameters(parameters)
        self._updateMessages(parameters)

    def _updateMessages(self, parameters):
        """"""

    def execute(self, parameters=None, messages=None):
        """Run the tool with the parameters and messages from ArcGIS"""
        self.tool.main(self.par, parameters, messages)      
        
    def print_test_parameters(self):
        self._getParameterInfo()
        category = None
        for k, v in self.par._od.iteritems():            
            if v.category and v.category != category:
                category = v.category
                print(u'### {} ###'.format(v.category))
            value = v.value
            if isinstance(value, (str, unicode)):
                value = u"'{}'".format(value)
            print (u'params.{k}.value = {v}'.format(v=value, k=k))
            
    def print_default_parameters(self):
        self._getParameterInfo()
        category = None
        for k, v in self.par._od.iteritems():            
            if v.category and v.category != category:
                category = v.category
                print(u'### {} ###'.format(v.category))
            print (u'{k} = self.par.{k}.value'.format(k=k)) 

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
