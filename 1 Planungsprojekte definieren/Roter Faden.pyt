# -*- coding: utf-8 -*-

import _rpcpath

from rpctools.utils.params import Tbx
from rpctools.definitions.roter_faden.installation_pruefen import InstallationPruefen

import arcpy


class Toolbox(object):
    def __init__(self):
        self.label = u'A Roter Faden'
        self.alias = ''
        self.tools = [Ersteinrichtung]


class Ersteinrichtung(Tbx):
    """Tool checks if python modules are installed"""

    @property
    def label(self):
        return u'Ersteinrichtung'

    @property
    def Tool(self):
        return InstallationPruefen

    def getParameterInfo(self):
        params = self.par

        # Pfad_zur_Python_Installation_
        params.path = arcpy.Parameter()
        params.path.name = u'Pfad_zur_Python_Installation_'
        params.path.displayName = u'Pfad zur Python-Installation:'
        params.path.parameterType = 'Required'
        params.path.direction = 'Input'
        params.path.datatype = language('string')
        params.path.value = folders.PYTHON_EXECUTABLE
        params.path.enabled = False
        params.path.value = sys.exec_prefix

        # Paket__matplotlib__vorhanden
        params.matplotlib = arcpy.Parameter()
        params.matplotlib.name = u'Paket__matplotlib__vorhanden'
        params.matplotlib.displayName = u"Paket 'matplotlib' vorhanden"
        params.matplotlib.parameterType = 'Required'
        params.matplotlib.direction = 'Input'
        params.matplotlib.datatype = language('boolean')
        params.matplotlib.value = u'false'
        params.matplotlib.enabled = True
        params.matplotlib.value = False

        # Paket__numpy__vorhanden
        params.numpy = arcpy.Parameter()
        params.numpy.name = u'Paket__numpy__vorhanden'
        params.numpy.displayName = u"Paket 'numpy' vorhanden"
        params.numpy.parameterType = 'Required'
        params.numpy.direction = 'Input'
        params.numpy.datatype = language('boolean')
        params.numpy.value = u'false'
        params.numpy.enabled = True
        params.numpy.value = False

        # Paket__pyodbc__vorhanden
        params.pyodbc = arcpy.Parameter()
        params.pyodbc.name = u'Paket__pyodbc__vorhanden'
        params.pyodbc.displayName = u"Paket 'pyodbc' vorhanden"
        params.pyodbc.parameterType = 'Required'
        params.pyodbc.direction = 'Input'
        params.pyodbc.datatype = language('boolean')
        params.pyodbc.value = u'false'
        params.pyodbc.enabled = True
        params.pyodbc.value = False

        # Paket__setuptools__vorhanden
        params.setuptools = arcpy.Parameter()
        params.setuptools.name = u'Paket__setuptools__vorhanden'
        params.setuptools.displayName = u"Paket 'setuptools' vorhanden"
        params.setuptools.parameterType = 'Required'
        params.setuptools.direction = 'Input'
        params.setuptools.datatype = language('boolean')
        params.setuptools.value = u'false'
        params.setuptools.enabled = True
        params.setuptools.value = False

        # Paket__six__vorhanden
        params.six = arcpy.Parameter()
        params.six.name = u'Paket__six__vorhanden'
        params.six.displayName = u"Paket 'six' vorhanden"
        params.six.parameterType = 'Required'
        params.six.direction = 'Input'
        params.six.datatype = language('boolean')
        params.six.value = u'false'
        params.six.enabled = True
        params.six.value = False

        # Paket__xlrd__vorhanden
        params.xlrd = arcpy.Parameter()
        params.xlrd.name = u'Paket__xlrd__vorhanden'
        params.xlrd.displayName = u"Paket 'xlrd' vorhanden"
        params.xlrd.parameterType = 'Required'
        params.xlrd.direction = 'Input'
        params.xlrd.datatype = language('boolean')
        params.xlrd.value = u'false'
        params.xlrd.enabled = True
        params.xlrd.value = False

        # Paket__xlsxwriter__vorhanden
        params.xlsxwriter = arcpy.Parameter()
        params.xlsxwriter.name = u'Paket__xlsxwriter__vorhanden'
        params.xlsxwriter.displayName = u"Paket 'xlsxwriter' vorhanden"
        params.xlsxwriter.parameterType = 'Required'
        params.xlsxwriter.direction = 'Input'
        params.xlsxwriter.datatype = language('boolean')
        params.xlsxwriter.value = u'false'
        params.xlsxwriter.enabled = True
        params.xlsxwriter.value = False

        return params

    def updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""


        try:
            import matplotlib
            params.matplotlib.value = True
        except ImportError, e:
            params.matplotlib.value = False
            pass

        try:
            import numpy
            params.numpy.value = True
        except ImportError, e:
            params.numpy.value = False
            pass

        try:
            import pyodbc
            params.pyodbc.value = True
        except ImportError, e:
            params.pyodbc.value = False
            pass

        try:
            import setuptools
            params.setuptools.value = True
        except ImportError, e:
            params.setuptools.value = False
            pass

        try:
            import six
            params.six.value = True
        except ImportError, e:
            params.six.value = False
            pass

        try:
            import xlrd
            params.xlrd.value = True
        except ImportError, e:
            params.xlrd.value = False
            pass

        try:
            import xlsxwriter
            params.xlsxwriter.value = True
        except ImportError, e:
            params.xlsxwriter.value = False
            pass
