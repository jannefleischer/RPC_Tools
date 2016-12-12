# -*- coding: utf-8 -*-

import unittest
import csv
import arcpy

import T1_Basisdaten_bearbeiten as t1
import T2_Routings_durchfuehren as t2
import T3_Verkehrsmengen_ermitteln as t3

test_project = 'test'
MAPQUEST_KEY = 'D0CXAXhgKGKmuAxA3x7HZq10MvbqhPiF'
values = [test_project]

class TestC_Verkehr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # first param is always the project name
        with open('test_params.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                values.append(row[1])

        def parameter_mocked(i):
            if i == 1:
                return MAPQUEST_KEY
            return values[i]

        test_mxd = arcpy.mapping.MapDocument("test.mxd")

        def document_mocked(path):
            return test_mxd

        arcpy.mapping.MapDocument = document_mocked
        arcpy.GetParameterAsText = parameter_mocked


    def test01(self):
        t1.main()

    def test02(self):
        t2.main()

    def test03(self):
        t3.main()


if __name__ == '__main__':
    unittest.main()
