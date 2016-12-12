# -*- coding: utf-8 -*-

import unittest
import T5_Kostenmodell
import arcpy, csv, shutil, os

project_folder = os.path.join(os.getcwd().split("2_Tool")[0], "3_Projekte")
tmp_project = 'unittest'
tmp_project_folder = os.path.join(project_folder, tmp_project)
test_template = 'test_template'

params_kosten = [tmp_project]

class TestA_Kosten(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        cls.params = []
        def mock_params(i):
            return cls.params[i]

        with open('test_params_infrastrukturkosten.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                params_kosten.append(row[1])

        arcpy.GetParameterAsText = mock_params

    def test_infrastrukturkosten(self):
        self.__class__.params = params_kosten
        T5_Kostenmodell.main()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp_project_folder)

if __name__ == '__main__':
    unittest.main()


