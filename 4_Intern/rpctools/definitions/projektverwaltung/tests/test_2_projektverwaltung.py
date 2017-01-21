# -*- coding: utf-8 -*-

import unittest
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung import Projektverwaltung
from rpctools.definitions.projektverwaltung.teilflaeche_benennen import TeilflaechenBenennen

import arcpy
import os, shutil, gc
from os.path import join
from time import gmtime, strftime

PROJECT_FOLDER = join(os.getcwd().split("2_Tool")[0], "3_Projekte")
PROJECT_TMP = '__unittest__'

shp_template = join(PROJECT_FOLDER, "projektflaechen_template.shp")
params_verwaltung = ['', PROJECT_TMP, PROJECT_TMP, shp_template, 2010, 2050]
flaechenname = 'Nr. 1 | 50.77 ha | Flaeche_1'

def to_arcpy_params(lst):
    arcpy_params = []
    for p in lst:
        ap = arcpy.Parameter()
        ap.value = p
        arcpy_params.append(ap)
    return arcpy_params

class Test2Projektverwaltung(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)

        test_mxd = arcpy.mapping.MapDocument("test.mxd")
        def mocked_doc(path):
            return test_mxd
        arcpy.mapping.MapDocument = mocked_doc

    def test1_anlegen(self):
        params = params_verwaltung
        params[0] = "Neues Projekt anlegen"
        Projektverwaltung(to_arcpy_params(params), arcpy).main()

    def test2_teilflaeche_benennen(self):
        params = [PROJECT_TMP, flaechenname + 'dfas', flaechenname + 'neu']
        TeilflaechenBenennen(to_arcpy_params(params), arcpy).main()
        gc.collect()

    def test3_loeschen(self):
        params = params_verwaltung
        params[0] = "Bestehendes Projekt löschen"
        Projektverwaltung(to_arcpy_params(params), arcpy).main()

if __name__ == '__main__':
    unittest.main()

