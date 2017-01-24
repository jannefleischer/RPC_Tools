# -*- coding: utf-8 -*-

import unittest
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung import Projektverwaltung
from rpctools.definitions.projektverwaltung.tbx_projektverwaltung import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_bennenen import TbxTeilflaecheBenennen
from rpctools.definitions.projektverwaltung.teilflaeche_benennen import TeilflaechenBenennen

import arcpy
import os, shutil, gc
from os.path import join
from time import gmtime, strftime

class Test2Projektverwaltung(unittest.TestCase):
    
    tbx_proj = TbxProjektVerwaltung()
    tbx_flaeche = TbxTeilflaecheBenennen()
    
    flaechenname = 'Nr. 1 | 50.77 ha | Flaeche_1'
    test_name = '__unittest__'

    @classmethod
    def setUpClass(cls):
        params_proj = cls.tbx_proj.par
        params_proj.begin.value = 2010
        params_proj.end.value = 2050
        params_proj.name.value = cls.test_name
        params_proj.existing_project.value = cls.test_name
        shape = arcpy.Parameter()
        shape.value = cls.tbx_proj.folders.TEMPLATE_FLAECHEN
        params_proj.shapefile = shape
        
        params_flaeche = cls.tbx_flaeche.par     
        params_flaeche.project.value = cls.test_name       
        params_flaeche.teilflaeche.value = cls.flaechenname
        params_flaeche.name.value = cls.flaechenname + ' neu'
        
        tmp_project_folder = cls.tbx_proj.folders.PROJECT_PATH
        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)     
                    
        MapDocument = arcpy.mapping.MapDocument
        def mocked_doc(path):
            print(path)
            if path == 'CURRENT':
                return MapDocument(os.path.join(os.path.dirname(__file__),
                                                "test.mxd"))
            return MapDocument(path)
        arcpy.mapping.MapDocument = mocked_doc

    def test1_anlegen(self):
        params = self.tbx_proj.par
        params.action.value = "Neues Projekt anlegen"
        Projektverwaltung(params).run()
 
    def test2_teilflaeche_benennen(self):   
        params = self.tbx_flaeche.par
        TeilflaechenBenennen(params).run()
        gc.collect()

    def test3_loeschen(self):        
        params = self.tbx_proj.par
        params.action.value = "Bestehendes Projekt löschen"
        Projektverwaltung(params).run()

if __name__ == '__main__':
    unittest.main()

