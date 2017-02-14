# -*- coding: utf-8 -*-

import unittest
import arcpy, csv, shutil, os

import T1_Vorberechnungen
import T2_Zentrale_Orte_OEPNV_Abfrage
import T3_Erreichbarkeit_OEPNV
import T4_Erreichbarkeit_Einrichtungen
import T5_Ergebnissammler

PROJECT_FOLDER = join(os.getcwd().split("2_Tool")[0], "3 Benutzerdefinierte Projekte")
TEST_TEMPLATE = 'Test_Template'
PROJECT_TMP = '__unittest__'

tmp_project_folder = join(PROJECT_FOLDER, PROJECT_TMP)
PATH_HALTE = join(tmp_project_folder,
                          'FGDB_Erreichbarkeit_{}.gdb'.format(TEST_TEMPLATE),
                          'OEPNV_Haltestellen')
PATH_ORTE = join(tmp_project_folder,
                         'FGDB_Erreichbarkeit_{}.gdb'.format(TEST_TEMPLATE),
                         'Zentrale_Orte_75km')

params_common = [PROJECT_TMP]
template_kitas = join(tmp_project_folder, 'Einrichtungen_Kindertagesstaetten.xls')
template_grundschulen = join(tmp_project_folder, 'Einrichtungen_Grundschulen.xls')
template_einzelhandel = join(tmp_project_folder, 'Einrichtungen_Einzelhandel.xls')
template_apotheken = join(tmp_project_folder, 'Einrichtungen_Apotheken.xls')
template_aerzte = join(tmp_project_folder, 'Einrichtungen_Aerzte.xls')
template_kh = join(tmp_project_folder, 'Einrichtungen_Krankenhaeuser.xls')
template_sons = join(tmp_project_folder, 'Einrichtungen_Sonstige.xls')

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

class TestDErreichbarkeit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        arcpy.AddErrorMessage = arcpy.AddError

        if os.path.exists(tmp_project_folder):
            shutil.rmtree(tmp_project_folder)
        shutil.copytree(
            join(PROJECT_FOLDER, TEST_TEMPLATE),
            join(tmp_project_folder)
        )

    def test1_vorberechnungen(self):
        T1_Vorberechnungen.main(to_arcpy_params(params_common), arcpy)

    def test2_zentrale_orte(self):
        params = params_common[:]
        params.extend(['', '', ''])
        rows = arcpy.SearchCursor(PATH_ORTE)
        for i, row in enumerate(rows):
            if i > 1:
                break
            params[i+1] = row.Name
        T2_Zentrale_Orte_OEPNV_Abfrage.main(to_arcpy_params(params), arcpy)

    def test3_erreichbarkeit_oepnv(self):
        params = params_common[:]
        params.extend(['', '', ''])
        rows = arcpy.SearchCursor(PATH_HALTE)
        for i, row in enumerate(rows):
            if i > 1:
                break
            params[i+1] = row.Name
        T3_Erreichbarkeit_OEPNV.main(to_arcpy_params(params), arcpy)

    def test4_einrichtungen(self):
        params = params_common[:]
        params.extend([False, template_kitas, template_grundschulen,
                       template_aerzte, template_apotheken,
                       template_kh, template_sons, False,
                       template_einzelhandel, ''])
        T4_Erreichbarkeit_Einrichtungen.main(to_arcpy_params(params), arcpy)

    def test5_ergebnisse(self):
        T5_Ergebnissammler.main(to_arcpy_params(params_common), arcpy)

    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree(tmp_project_folder)
        except WindowsError:
            print u'Fehler beim Löschen des temporären Unittest-Verzeichnisses'

if __name__ == '__main__':
    unittest.main()



