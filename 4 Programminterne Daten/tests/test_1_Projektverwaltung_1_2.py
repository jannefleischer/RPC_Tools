# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung import (
     TbxProjekteLoeschen, TbxProjektAnlegen, TbxProjektKopieren)
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_verwalten import \
     TbxTeilflaecheVerwalten
from rpctools.definitions.projektverwaltung.projektverwaltung import (
     ProjektAnlegen, ProjektKopieren, ProjektLoeschen)
from rpctools.definitions.projektverwaltung.teilflaeche_verwalten import \
     TeilflaechenVerwalten

from test_lib import mocked_map_document, test_name, remove_project_dir
import gc
import pytest

### get the toolboxes with their parameters ###

@pytest.fixture(scope='module')
def tbx_anlegen():
    tbx = TbxProjektAnlegen()
    tbx.getParameterInfo()
    return tbx

@pytest.fixture(scope='module')
def tbx_kopieren():
    tbx = TbxProjektKopieren()
    tbx.getParameterInfo()
    return tbx

@pytest.fixture(scope='module')
def tbx_loeschen():
    tbx = TbxProjekteLoeschen()
    tbx.getParameterInfo()
    return tbx

@pytest.fixture(scope='module')
def tbx_flaeche():
    tbx = TbxTeilflaecheVerwalten()
    tbx.getParameterInfo()
    return tbx

@pytest.fixture(scope='module')
def params_anlegen(tbx_anlegen, test_name):
    params = tbx_anlegen.par
    params.begin.value = 2010
    params.end.value = 2050
    params.name.value = test_name
    params.shapefile.value = tbx_anlegen.folders.TEMPLATE_FLAECHEN
    return params

@pytest.fixture(scope='module')
def params_loeschen(tbx_loeschen, test_name):
    params = tbx_loeschen.par
    params.name.value = test_name
    return params

@pytest.fixture
def params_flaeche(tbx_flaeche, test_name):
    params = tbx_flaeche.par
    params.projectname.value = test_name
    #params.teilflaeche.value = flaechenname
    params.name.value = 'flaeche test neu'
    return params

### ordered Tests (with the above defined parameter-functions as arguments) ###

@pytest.mark.order1
def test1_anlegen(tbx_anlegen, params_anlegen, mocked_map_document):
    remove_project_dir(tbx_anlegen)
    ProjektAnlegen(params_anlegen, tbx_anlegen).run()

@pytest.mark.order2
def test2_teilflaeche_benennen(tbx_flaeche, params_flaeche, mocked_map_document):
    TeilflaechenVerwalten(params_flaeche, tbx_flaeche).run()
    gc.collect()

@pytest.mark.order3
def test3_loeschen(tbx_loeschen, params_loeschen, mocked_map_document):
    ProjektLoeschen(params_anlegen, tbx_loeschen).run()


def test_try():
    assert False

if __name__ == '__main__':
    pytest.main([__file__])
