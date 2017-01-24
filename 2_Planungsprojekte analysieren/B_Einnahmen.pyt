# -*- coding: utf-8 -*-

import _rpcpath
import contextlib
import os
import sys
import argparse

from rpctools.analyst.einnahmen import (tbx_vorberechnungen, tbx_einnahmen,
                                        tbx_grundsteuer, tbx_gewerbesteuer)  
reload(tbx_vorberechnungen)
reload(tbx_einnahmen)
reload(tbx_grundsteuer)
reload(tbx_gewerbesteuer)
from rpctools.analyst.einnahmen.tbx_vorberechnungen import TbxVorberechnungen
from rpctools.analyst.einnahmen.tbx_einnahmen import (
    TbxEinkommenssteuer,
    TbxFamilienleistungsausgleich,
    TbxKFA,
    TbxKRU)
from rpctools.analyst.einnahmen.tbx_grundsteuer import TbxGrundsteuer
from rpctools.analyst.einnahmen.tbx_gewerbesteuer import TbxGewerbesteuer
tools = [TbxVorberechnungen,
         TbxEinkommenssteuer,
         TbxFamilienleistungsausgleich,
         TbxGrundsteuer,
         TbxGewerbesteuer,
         TbxKFA,
         TbxKRU]


class Toolbox(object):
    def __init__(self):
        self.label = u'32_Einnahmen'
        self.alias = ''
        self.tools = tools


def main():
    tbx = Toolbox()
    for Tool in tbx.tools:
        tool = Tool()
        print tool.label
        print(tool.getParameterInfo())
        tool.execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()