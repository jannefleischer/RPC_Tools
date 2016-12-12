# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Verkehrsmengen_ermitteln.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules

import unittest
import csv

import T1_Basisdaten_bearbeiten as t1
import T2_Routings_durchfuehren as t2
import T3_Verkehrsmengen_ermitteln as t3


class Test03_Verkehrsmenge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        values = []
        with open('test_params.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                values.append(row[1])

        def parameter_mocked(i):
            return values[i]

        for mod in [t1, t2, t3]:
            mod.arcpy.GetParameterAsText = parameter_mocked


    def test01(self):
        t1.main()

    def test02(self):
        t2.main()

    def test03(self):
        t3.main()


if __name__ == '__main__':
    unittest.main()
