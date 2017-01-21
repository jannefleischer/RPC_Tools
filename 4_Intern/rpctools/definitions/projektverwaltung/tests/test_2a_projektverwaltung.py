# -*- coding: utf-8 -*-

import pytest

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung import TbxProjektVerwaltung
from rpctools.utils.encoding import encode


def test_tbx_projektverwaltung():
    tb = TbxProjektVerwaltung()
    params = tb.getParameterInfo()
    print(params)
    print(tb.tool.db)
    params.name.value = 'Wedel0'
    print(tb.tool.db)
    print(tb.folders.get_table('aaa'))
    print(tb.folders.get_table('aaa', 'Andere.gdb'))
    print(tb.folders.get_table('aaa', 'Andere.gdb', 'AnderesProjekt'))

    params.action.value = "Bestehendes Projekt kopieren"
    tb.updateParameters(params)
    params.name.value = 'Wedel2'
    tb.updateParameters(params)
    params.existing_project.value = 'Wedel0'
    tb.updateParameters(params)
    print(params)
    try:
        tb.execute(params, '')
    except SystemExit as e:
        print(e)


    params.action.value = encode("Bestehendes Projekt löschen")
    tb.updateParameters(params)
    params.name.value = 'Wedel2'
    tb.updateParameters(params)
    print(params)
    tb.execute(params, '')


if __name__ == '__main__':
    test_tbx_projektverwaltung()