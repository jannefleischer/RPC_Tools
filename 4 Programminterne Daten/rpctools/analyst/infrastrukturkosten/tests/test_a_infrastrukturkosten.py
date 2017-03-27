# -*- coding: utf-8 -*-

import unittest
import T5_Kostenmodell
import kosten_lib
import arcpy, csv, shutil, os


PROJECT_FOLDER = join(os.getcwd().split("2 Planungsprojekte analysieren")[0], "3 Benutzerdefinierte Projekte")
TEST_TEMPLATE = 'Test_Template'
PROJECT_TMP = '__unittest__'

params_kosten = [PROJECT_TMP]
params_kosten_csv = 'test_params_kostenmodell.csv'
params_aufteilung = ['testregel', 10, 20, 70]

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


class TestAKosten(unittest.TestCase):

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

    def test1_kostenaufteilung(self):
        params = params_aufteilung
        kosten_lib.kostenregel_anlegen(
            params_aufteilung[0],
            params_aufteilung[1],
            params_aufteilung[2],
            params_aufteilung[3]
        )
        kosten_lib.kostenregel_bearbeiten(
            params_aufteilung[0], 36, 33, 31
        )
        kosten_lib.kostenregel_loeschen(params_aufteilung[0])

    def test2_infrastrukturkosten(self):
        params = load_csv_params(params_kosten_csv, params_kosten)
        T5_Kostenmodell.main(to_arcpy_params(params), arcpy)

    @classmethod
    def tearDownClass(cls):
        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        try:
            shutil.rmtree(tmp_project_folder)
        except WindowsError:
            print u'Fehler beim Löschen des temporären Unittest-Verzeichnisses'

if __name__ == '__main__':
    unittest.main()


