# -*- coding: utf-8 -*-

import unittest
import pytest
import arcpy, csv, shutil, os
from os.path import join

from rpctools.analyst.einnahmen.T1_Vorberechnungen import Vorberechnungen
from rpctools.analyst.einnahmen.tbx_einnahmen import TbxVorberechnungen

from rpctools.analyst.einnahmen.T2_Einkommensteuer import Einkommenssteuer
from rpctools.analyst.einnahmen.T3_Familienleistungsausgleich \
     import  Familienleistungsausgleich
from rpctools.analyst.einnahmen.T4_Grundsteuer import Grundsteuer
from rpctools.analyst.einnahmen.T5_Gewerbesteuer import Gewerbesteuer
from rpctools.analyst.einnahmen.T6_KFA import KFA
from rpctools.analyst.einnahmen.T7_KRU import KRU
from rpctools.utils.config import Folders
from test_lib import (test_name, test_name, setup_template_dir)


"""
TODO
"""

@pytest.fixture(scope='module')
def tbx_vorberechnungen():
    tbx = TbxVorberechnungen()
    params = tbx.getParameterInfo()
    tbx.updateParameterInfo(params)
    return tbx

@pytest.fixture(scope='module')
def params_vorbetrachtungen(tbx_vorberechnungen):
    params = tbx_vorberechnungen.par
    params.name.value =

"""
TODO
"""
folders = Folders()
PROJECT_FOLDER = folders.PROJECT_BASE_PATH
TEST_TEMPLATE = 'Test_Template'
PROJECT_TMP = '__unittest__'

params_common = [PROJECT_TMP]
params_vorberechnungen_csv = 'test_params_vorberechnungen.csv'
params_grundsteuer_csv = 'test_params_grundsteuer.csv'
params_gewerbesteuer_csv = 'test_params_gewerbesteuer.csv'

def load_csv_params(csv_file, prepend=[]):
    params = prepend[:]
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            params.append(row[1])
    return params

def to_arcpy_params(lst):
    arcpy_params = []
    for p in lst:
        ap = arcpy.Parameter()
        if isinstance(p, bool):
            ap.datatype = 'GPBoolean'
        ap.value = p
        arcpy_params.append(ap)
    return arcpy_params





class TestBEinnahmen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        arcpy.AddErrorMessage = arcpy.AddError

        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        shutil.copytree(
            join(PROJECT_FOLDER, TEST_TEMPLATE),
            tmp_project_folder)


    def test1_vorberechnungen(self):
        params = load_csv_params(params_vorberechnungen_csv, params_common)
        T1_Vorberechnungen.main(to_arcpy_params(params), arcpy)

    def test2_einkommensteuer(self):
        T2_Einkommensteuer.main(to_arcpy_params(params_common), arcpy)

    def test3_familienausgleich(self):
        T3_Familienleistungsausgleich.main(to_arcpy_params(params_common), arcpy)

    def test4_grundsteuer(self):
        params = load_csv_params(params_grundsteuer_csv, params_common)
        T4_Grundsteuer.main(to_arcpy_params(params), arcpy)

    def test5_gewerbesteuer(self):
        params = load_csv_params(params_gewerbesteuer_csv, params_common)
        T5_Gewerbesteuer.main(to_arcpy_params(params), arcpy)

    def test6_KFA(self):
        T6_KFA.main(to_arcpy_params(params_common), arcpy)

    def test7_KRU(self):
        T7_KRU.main(to_arcpy_params(params_common), arcpy)

    @classmethod
    def tearDownClass(cls):
        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        try:
            shutil.rmtree(tmp_project_folder)
        except WindowsError:
            print u'Fehler beim Löschen des temporären Unittest-Verzeichnisses'

if __name__ == '__main__':
    unittest.main()


