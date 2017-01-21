# -*- coding: utf-8 -*-

import unittest
import T1_Vorberechnungen
import T2_Einkommensteuer
import T3_Familienleistungsausgleich
import T4_Grundsteuer
import T5_Gewerbesteuer
import T6_KFA
import T7_KRU
import arcpy, csv, shutil, os

PROJECT_FOLDER = join(os.getcwd().split("2_Tool")[0], "3_Projekte")
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
            join(tmp_project_folder)
        )

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


