# -*- coding: utf-8 -*-

import unittest
import flaechen_bilanz, nutzungen
import arcpy, csv, shutil, os

PROJECT_FOLDER = join(os.getcwd().split("2_Tool")[0], "3_Projekte")
TEST_TEMPLATE = 'Test_Template'
PROJECT_TMP = '__unittest__'

teilflaeche = 'Flaeche_1'
params_flaechenbilanz = [PROJECT_TMP, teilflaeche, '2015']
params_nutzungen = [PROJECT_TMP, teilflaeche, '2015']
params_nutzungen_csv = 'test_params_nutzungen.csv'
params_flaechenbilanz_csv = 'test_params_flaechenbilanz.csv'

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

class Test3Nutzung(unittest.TestCase):

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

    def test_flaechenbilanz(self):
        params = load_csv_params(params_flaechenbilanz_csv, params_flaechenbilanz)
        flaechen_bilanz.main(to_arcpy_params(params), arcpy)

    def test_nutzungen(self):
        params = load_csv_params(params_nutzungen_csv, params_nutzungen)
        nutzungen.main(to_arcpy_params(params), arcpy)

    @classmethod
    def tearDownClass(cls):
        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        shutil.rmtree(tmp_project_folder)

if __name__ == '__main__':
    unittest.main()


