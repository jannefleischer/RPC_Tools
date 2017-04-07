# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# install_packages.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------

import os, sys
from os.path import join
import subprocess
from collections import OrderedDict
import arcpy


def install_packages(python_path):

    arcpy.AddMessage("\n"+ "Verwendeter Python-Pfad: " + python_path + "\n")

    #Creating list with missing packages
    used_packages = OrderedDict()
    used_packages['appdirs']='appdirs-1.4.3-py2.py3-none-any.whl'
    used_packages['six']='six-1.10.0-py2.py3-none-any.whl'
    used_packages['pyparsing']='pyparsing-2.2.0-py2.py3-none-any.whl'
    used_packages['packaging']='packaging-16.8-py2.py3-none-any.whl'
    used_packages['setuptools']='setuptools-34.3.3-py2.py3-none-any.whl'

    used_packages['functools32']='functools32-3.2.3.post2-py27-none-any.whl'

    used_packages['numpy'] = 'numpy-1.12.1+mkl-cp27-cp27m-win32.whl'
    used_packages['cycler'] = 'cycler-0.10.0-py2.py3-none-any.whl'
    used_packages['dateutil']='python_dateutil-2.6.0-py2.py3-none-any.whl'
    used_packages['pytz']='pytz-2017.2-py2.py3-none-any.whl'

    used_packages['matplotlib']='matplotlib-2.0.0-cp27-cp27m-win32.whl'

    used_packages['pyodbc']='pyodbc-4.0.16-cp27-cp27m-win32.whl'

    used_packages['xlrd']='xlrd-1.0.0-py2-none-any.whl'
    used_packages['xlsxwriter']='XlsxWriter-0.9.6-py2.py3-none-any.whl'

    used_packages['py']='py-1.4.33-py2.py3-none-any.whl'
    used_packages['colorama']='colorama-0.3.7-py2.py3-none-any.whl'

    used_packages['pytest']='pytest-3.0.7-py2.py3-none-any.whl'

    used_packages['imagesize']='imagesize-0.7.1-py2.py3-none-any.whl'
    used_packages['pygments']='Pygments-2.2.0-py2.py3-none-any.whl'
    used_packages['snowballstemmer']='snowballstemmer-1.2.1-py2.py3-none-any.whl'
    used_packages['alabaster']='alabaster-0.7.10-py2.py3-none-any.whl'
    used_packages['docutils']='docutils-0.13.1-py2-none-any.whl'
    used_packages['requests']='requests-2.13.0-py2.py3-none-any.whl'

    used_packages['babel']='Babel-2.4.0-py2-none-any.whl'
    used_packages['markupsafe']='MarkupSafe-1.0-cp27-cp27m-win32.whl'
    used_packages['jinja2']='Jinja2-2.9.6-py2.py3-none-any.whl'

    used_packages['sphinx']='Sphinx-1.5.5-py2.py3-none-any.whl'
    used_packages['numpydoc']='numpydoc-0.6.0-py2-none-any.whl'
    used_packages['enum']='enum-0.4.6-py2-none-any.whl'
    missing = OrderedDict()

    #Installing pip
    base_path = os.path.dirname(__file__)
    wheel_path = os.path.join(base_path, 'wheels')
    arcpy.AddMessage('Install or upgrade pip')
    process = subprocess.Popen([os.path.join(python_path, 'python'),
                     os.path.join(wheel_path, "pip-9.0.1-py2.py3-none-any.whl", "pip"),
                     'install',
                     '--upgrade',
                     os.path.join(wheel_path, "pip-9.0.1-py2.py3-none-any.whl")],
                           shell=True)
    ret = process.wait()
    if ret:
        arcpy.AddWarning('pip nicht richtig installiert')
    else:
        arcpy.AddMessage('pip installiert')

    ##Installing packages
    import pip
    arcpy.AddMessage('wheel_path; {}'.format(wheel_path))

    for package, filename in used_packages.iteritems():
        arcpy.AddMessage('{p}: {f}'.format(p=package, f=filename))
        pip.main(['install', '-f', wheel_path, os.path.join(wheel_path, filename)])

        try:
            new_package = __import__(package)
            arcpy.AddMessage("Paket " + package + " wurde installiert." + "\n")
        except:
            arcpy.AddWarning("Paket " + package + " konnte nicht installiert werden." + "\n")

    # install rpctools package
    # ToDo: Finally change from --editable to wheel
    arcpy.AddMessage("installiere RPCTools")

    process = subprocess.Popen([os.path.join(python_path, 'python.exe'),
                                "-m", "pip",
                                'install',
                                '--editable',
                                base_path],
                               shell=True)

    ret = process.wait()

    if ret:
        arcpy.AddWarning('rpctools konnte nicht installiert werden')
    else:
        arcpy.AddMessage("RPCTools installiert")

    arcpy.AddMessage('Installation abgeschlossen.')


if __name__ == '__main__':
    install_packages('C:\\Python27\\ArcGIS10.4')
