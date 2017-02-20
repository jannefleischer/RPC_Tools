# -*- coding: utf-8 -*-

import unittest
import arcpy, csv, shutil, os

import T1_Basisdaten_bearbeiten
import T2_Routings_durchfuehren
import T3_Verkehrsmengen_ermitteln

PROJECT_FOLDER = join(os.getcwd().split("2 Planungsprojekte analysieren")[0], "3 Benutzerdefinierte Projekte")
TEST_TEMPLATE = 'Test_Template'
PROJECT_TMP = '__unittest__'
MAPQUEST_KEY = 'D0CXAXhgKGKmuAxA3x7HZq10MvbqhPiF'

params_common = [PROJECT_TMP]
params_verkehrsmengen_csv = 'test_params_verkehrsmengen.csv'

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
        try:
            p = float(p)
            ap.datatype = 'GPDouble'
        except:
            pass
        ap.value = p
        arcpy_params.append(ap)
    return arcpy_params

class TestCVerkehr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_mxd = arcpy.mapping.MapDocument("test.mxd")

        # mock the function to get the currently opened mxd
        document = arcpy.mapping.MapDocument
        def current_mocked(path):
            if path == 'CURRENT':
                return test_mxd
            else:
                return document(path)
        arcpy.mapping.MapDocument = current_mocked
        arcpy.AddErrorMessage = arcpy.AddError

        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        shutil.copytree(
            join(PROJECT_FOLDER, TEST_TEMPLATE),
            join(tmp_project_folder)
        )

    def test1_basisdaten(self):
        T1_Basisdaten_bearbeiten.main(to_arcpy_params(params_common), arcpy)

    def test2_routing(self):
        params = params_common[:]
        params.append(MAPQUEST_KEY)
        T2_Routings_durchfuehren.main(to_arcpy_params(params), arcpy)

    def test3_verkehrsmengen(self):
        params = load_csv_params(params_verkehrsmengen_csv, params_common)
        T3_Verkehrsmengen_ermitteln.main(to_arcpy_params(params), arcpy)

    @classmethod
    def tearDownClass(cls):
        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        try:
            shutil.rmtree(tmp_project_folder)
        except WindowsError:
            print u'Fehler beim Löschen des temporären Unittest-Verzeichnisses'

if __name__ == '__main__':
    unittest.main()
    # -*- coding: utf-8 -*-



