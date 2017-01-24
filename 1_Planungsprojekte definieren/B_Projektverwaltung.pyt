# -*- coding: utf-8 -*-

import _rpcpath
import argparse

# reload
from rpctools.definitions.projektverwaltung import tbx_projektverwaltung
reload(tbx_projektverwaltung)
from rpctools.definitions.projektverwaltung import tbx_teilflaechen_bennenen
reload(tbx_teilflaechen_bennenen)

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung \
     import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_bennenen \
     import TbxTeilflaecheBenennen


class Toolbox(object):
    def __init__(self):
        self.label = u'Projektverwaltung'
        self.alias = ''
        self.tools = [TbxTeilflaecheBenennen, 
                      TbxProjektVerwaltung]

def main():
    tbx = Toolbox()
    tool = ProjektVerwaltung()
    tool.execute(tool.getParameterInfo(), None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    options = parser.parse_args()
    if options.debug:
        main()
        # -*- coding: utf-8 -*-
        