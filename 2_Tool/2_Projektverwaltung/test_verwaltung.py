# -*- coding: utf-8 -*-

import unittest
import projektVerwaltung, teilflaecheBenennen
import arcpy
import os, shutil, gc
from time import gmtime, strftime

#tmp_project = 'test_tmp_' + strftime("%H-%M-%S_%d-%m-%Y", gmtime())
project_folder = os.path.join(os.getcwd().split("2_Tool")[0], "3_Projekte")
tmp_project = 'unittest'
tmp_project_folder = os.path.join(project_folder, tmp_project)

shp_template = os.path.join(project_folder, "projektflaechen_template.shp")
params_verwaltung = ['', tmp_project, tmp_project, shp_template, 2010, 2050]
flaechenname = 'Nr. 1 | 50.77 ha | Flaeche_1'
params_teilflaeche = [tmp_project, flaechenname, flaechenname]

class Test2_Projektverwaltung(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        cls.params = []
        def mock_params(i):
            return cls.params[i]

        arcpy.GetParameterAsText = mock_params

        test_mxd = arcpy.mapping.MapDocument("test.mxd")

        def mocked_doc(path):
            return test_mxd

        arcpy.mapping.MapDocument = mocked_doc

    def test1_anlegen(self):
        self.__class__.params = params_verwaltung
        Test2_Projektverwaltung.params[0] = "Neues Projekt anlegen"
        projektVerwaltung.main()

    def test2_teilflaeche_benennen(self):
        self.__class__.params = params_teilflaeche
        teilflaecheBenennen.main()
        gc.collect()

    def test3_loeschen(self):
        self.__class__.params = params_verwaltung
        self.__class__.params[0] = "Bestehendes Projekt löschen"
        projektVerwaltung.main()

if __name__ == '__main__':
    unittest.main()

