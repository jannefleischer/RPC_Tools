# -*- coding: utf-8 -*-

import unittest
import flaechenbilanz, nutzungen
import arcpy, csv, shutil, os

project_folder = os.path.join(os.getcwd().split("2_Tool")[0], "3_Projekte")
tmp_project = 'unittest'
tmp_project_folder = os.path.join(project_folder, tmp_project)
test_template = 'test_template'

teilflaeche = 'Flaeche_1'
params_flaechenbilanz = [tmp_project, teilflaeche, '2015']
params_nutzungen = [tmp_project, teilflaeche, '2015']

class Test3_Nutzung(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        shutil.copytree(
            os.path.join(project_folder, test_template),
            os.path.join(tmp_project_folder)
        )
        cls.params = []
        def mock_params(i):
            return cls.params[i]

        with open('test_params_flaechenbilanz.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                params_flaechenbilanz.append(row[1])

        with open('test_params_nutzungen.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                params_nutzungen.append(row[1])

        arcpy.GetParameterAsText = mock_params

    def test_flaechenbilanz(self):
        self.__class__.params = params_flaechenbilanz
        flaechenbilanz.main()

    def test_nutzungen(self):
        self.__class__.params = params_nutzungen
        nutzungen.main()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp_project_folder)

if __name__ == '__main__':
    unittest.main()


