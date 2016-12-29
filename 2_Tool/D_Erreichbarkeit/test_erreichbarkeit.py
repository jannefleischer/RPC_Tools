# -*- coding: utf-8 -*-

import unittest
import T3_Erreichbarkeit_OEPNV, T4_Erreichbarkeit_Einrichtungen
import arcpy, csv, shutil, os

project_folder = os.path.join(os.getcwd().split("2_Tool")[0], "3_Projekte")
test_template = 'test'
test_folder = os.path.join(project_folder, test_template)
path_Halte = os.path.join(test_folder,'FGDB_Erreichbarkeit_Projekt_'+test_template+'.gdb','OEPNV_Haltestellen')
#tmp_project = 'unittest'
#tmp_project_folder = os.path.join(project_folder, tmp_project)
#test_template = 'test_template'
template_kitas =  os.path.join(test_folder, 'Einrichtungen_Kindertagesstaetten.xls')
template_grundschulen = os.path.join(test_folder, 'Einrichtungen_Grundschulen.xls')
template_einzelhandel = os.path.join(test_folder, 'Einrichtungen_Einzelhandel.xls')
template_apotheken = os.path.join(test_folder, 'Einrichtungen_Apotheken.xls')
template_aerzte = os.path.join(test_folder, 'Einrichtungen_Aerzte.xls')
template_kh = os.path.join(test_folder, 'Einrichtungen_Krankenhaeuser.xls')
template_sons = os.path.join(test_folder, 'Einrichtungen_Sonstige.xls')

params = ['test']

def to_arcpy_params(lst):
    arcpy_params = []
    for p in lst:
        ap = arcpy.Parameter()
        if isinstance(p, bool):
            ap.datatype = 'GPBoolean'
        ap.value = p
        arcpy_params.append(ap)
    return arcpy_params

class Test3_Nutzung(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        arcpy.AddErrorMessage = arcpy.AddError

    #def test3_erreichbarkeit(self):
        #params = [test_template, '', '', '']
        #rows = arcpy.SearchCursor(path_Halte)
        #for i, row in enumerate(rows):
            #if i > 1:
                #break
            #params[i+1] = row.Name
        #T3_Erreichbarkeit_OEPNV.main(to_arcpy_params(params), arcpy)

    def test4_einrichtungen(self):
        params = [test_template, False, template_kitas, template_grundschulen, 
                  template_aerzte, template_apotheken, 
                  template_kh, template_sons, False, template_einzelhandel, '']
        T4_Erreichbarkeit_Einrichtungen.main(to_arcpy_params(params), arcpy)

    #@classmethod
    #def tearDownClass(cls):
        #shutil.rmtree(tmp_project_folder)

if __name__ == '__main__':
    unittest.main()


