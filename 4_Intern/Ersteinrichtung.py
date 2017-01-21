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
import _rpcpath

def install_packages(python_path):

    print("\n"+ "Verwendeter Python-Pfad: " + python_path + "\n")

    #Creating list with missing packages
    used_packages = ['pip', 'setuptools', 'matplotlib', 'numpy',
                     'pyodbc', 'six', 'xlrd', 'xlsxwriter', 'pytest']
    missing = []

    for package in used_packages:
        try:
            used_package = __import__(package)
        except:
            missing.append(package)

    if len(missing) == 0:
        print("Es wurden bereits alle erforderlichen Pakete installiert." + "\n")
        raw_input()
        sys.exit()
    else:
        print("Folgende Pakete werden in den angegebenen Python-Pfad installiert: " + str(missing) + "\n")

    #Installing pip
    try:
        import pip
    except ImportError, e:
        try:
            os.system("get-pip.py")
            print("Paket 'pip' wurde installiert.")
        except:
            print("Paket 'pip' konnte nicht installiert werden. Eine Installation weiterer Pakete ist damit nicht möglich. ")
            raw_input()
            sys.exit()

    #Installing missing packages
    import pip
    install_path = join(python_path, 'Lib', 'site-packages')
    print('Installationspad: ' + install_path + "\n")

    for package in missing:
        pip.main(['install', '--target', install_path, package])
        try:
            new_package = __import__(package)
            print("Paket " + package + " wurde installiert." + "\n")
        except:
            print("Paket " + package + " konnte nicht installiert werden." + "\n")

    # install rpcpackage from local directory
    pip.main(['install', '--target', install_path, '--editable', '.',
              '--upgrade'])

    print('Installation abgeschlossen.')
    raw_input()
    sys.exit()

install_packages(sys.exec_prefix)
