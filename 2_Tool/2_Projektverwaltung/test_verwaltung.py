# -*- coding: utf-8 -*-

import unittest
import _projektVerwaltung, teilflaecheBenennen
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

def to_arcpy_params(lst):
    arcpy_params = []
    for p in lst:
        ap = arcpy.Parameter()
        ap.value = p
        arcpy_params.append(ap)
    return arcpy_params

class Test2_Projektverwaltung(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
      
        test_mxd = arcpy.mapping.MapDocument("test.mxd")
        def mocked_doc(path):
            return test_mxd
        arcpy.mapping.MapDocument = mocked_doc

    def test1_anlegen(self):
        params = params_verwaltung
        params[0] = "Neues Projekt anlegen"
        _projektVerwaltung.main(to_arcpy_params(params), arcpy)

    def test2_teilflaeche_benennen(self):        
        params = [tmp_project, flaechenname, flaechenname]        
        teilflaecheBenennen.main(to_arcpy_params(params), arcpy)
        gc.collect()

    def test3_loeschen(self):
        params = params_verwaltung
        params[0] = "Bestehendes Projekt löschen"
        _projektVerwaltung.main(to_arcpy_params(params), arcpy)

if __name__ == '__main__':
    unittest.main()

