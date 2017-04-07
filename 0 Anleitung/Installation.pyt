# -*- coding: utf-8 -*-
# reload
import sys
import os
import imp


class Toolbox(object):
    def __init__(self):
        self.label = u'ProjektCheck Tools installieren'
        self.alias = ''
        self.tools = [TbxInstallation]


class TbxInstallation(object):
    def __init__(self):
        self.name = 'Installation'
        self.label = 'ProjektCheck Tools installieren'
        self.alias = 'ProjektCheck Tools installieren'
        self.tools = [TbxInstallation]

    def __init__(self):
        """"""
        self.pythonpath = sys.exec_prefix
        base = os.path.dirname(os.path.dirname(__file__))
        install_module_path = os.path.join(base, '4 Programminterne Daten',
                                      'Ersteinrichtung.py')
        self.install_module = imp.load_source('Ersteinrichtung',
                                              install_module_path)


    def getParameterInfo(self):
        """
        Define the Parameters and return a list or Params()-instance with the
        parameter
        """
        p = arcpy.Parameter()
        p.name = 'pythonpath'
        p.displayName = 'pythonpath'
        p.datatype = u'GPString'
        p.enabled = False
        p.value = self.pythonpath
        return [p]

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

    def updateMessages(self, parameters):
        """
        The updateMessages-method called by ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters
        """

    def execute(self, parameters=None, messages=None):
        """
        Run the tool with the parameters and messages from ArcGIS

        Parameters
        ----------
        parameters : list of ArcGIS-Parameters

        messages : the message-object of ArcGIS

        """
        self.install_module.install_packages(self.pythonpath)

