# -*- coding: utf-8 -*-

from collections import OrderedDict
import gc
import sys
from pprint import pformat
from abc import ABCMeta, abstractmethod, abstractproperty
from config import Folders
from arcpy import Messages, Parameter


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
        """
        self._od = OrderedDict(*args, **kwargs)
        self._param_projectname = param_projectname
        self._dbname = dbname

    def __getattr__(self, name):
        return self._od[name]

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
        msg = '{} Parameter der Toolbox passen nicht zu den {} Parameters des Tools'
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

    def _set_validated(self):
        for param in self:
            if isinstance(param, Parameter):
                param._altered = False
                param._validated = True


class Tool(object):
    __metaclass__ = ABCMeta

    _param_projectname = 'name'
    _dbname = None

    """Base Class for a ArcGIS Tool"""
    def __init__(self, params):
        self.par = params
        self.mes = Messages()
        self.folders = Folders(params=self.par)

    def main(self, parameters, messages):
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
    __metaclass__ = ABCMeta

    @abstractproperty
    def Tool(self):
        """"""

    @abstractproperty
    def label(self):
        """"""

    """Base Class for a ArcGIS Toolbox"""
    def __init__(self):
        # reload the tool's module
        reload(sys.modules[self.Tool.__module__])
        # the parameters
        self.par = Params(param_projectname=self.Tool._param_projectname,
                          dbname=self.Tool._dbname)
        # define the folders
        self.folders = Folders(params=self.par)
        # an instance of the tool
        self.tool = self.Tool(self.par)

    @abstractmethod
    def getParameterInfo(self):
        """
        Define the Parameters and return a list or Params()-instance with the
        parameter
        """

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Update the Parameters if something changed"""
        self.par._update_parameters(parameters)
        self._updateParameters(self.par)
        self.par._set_validated()

    def _updateParameters(self, params):
        """Update the Parameters if something changed"""

    def updateMessages(self, parameters):
        """"""
        self.par._update_parameters(parameters)
        self._updateMessages(parameters)

    def _updateMessages(self, parameters):
        """"""

    def execute(self, parameters, messages):
        """Run the tool with the parameters and messages from ArcGIS"""
        self.tool.main(parameters, messages)

