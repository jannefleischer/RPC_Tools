# -*- coding: utf-8 -*-

from rpctools.definitions.projektverwaltung.tbx_projektverwaltung import TbxProjektVerwaltung
from rpctools.definitions.projektverwaltung.tbx_teilflaechen_bennenen import TbxTeilflaecheBenennen
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung import Projektverwaltung
from rpctools.definitions.projektverwaltung.teilflaeche_benennen import TeilflaechenBenennen

from test_lib import mocked_map_document, test_name, remove_project_dir
import gc
import pytest

### get the toolboxes with their parameters ###

@pytest.fixture(scope='module')
def tbx_verwaltung():
    tbx = TbxProjektVerwaltung()
    tbx._getParameterInfo()
    return tbx

@pytest.fixture(scope='module')
def tbx_flaeche():
    tbx = TbxTeilflaecheBenennen()
    tbx._getParameterInfo()    
    return tbx

### setup the parameters used in the tests ###

@pytest.fixture
def flaechenname():
    return 'Nr. 1 | 50.77 ha | Flaeche_1'

@pytest.fixture
def params_verwaltung(tbx_verwaltung, test_name):
    params = tbx_verwaltung.par
    params.begin.value = 2010
    params.end.value = 2050
    params.name.value = test_name
    params.existing_project.value = test_name
    params.shapefile.value = tbx_verwaltung.folders.TEMPLATE_FLAECHEN
    return params
    
@pytest.fixture
def params_flaeche(tbx_flaeche, test_name, flaechenname):
    params = tbx_flaeche.par
    params.project.value = test_name
    params.teilflaeche.value = flaechenname
    params.name.value = 'flaeche test neu'
    return params

### ordered Tests (with the above defined parameter-functions as arguments) ### 
    
@pytest.mark.order1
def test1_anlegen(tbx_verwaltung, params_verwaltung):
    remove_project_dir(tbx_verwaltung)
    params_verwaltung.action.value = "Neues Projekt anlegen"
    Projektverwaltung(params_verwaltung).run()

@pytest.mark.order2
def test2_teilflaeche_benennen(params_flaeche):   
    TeilflaechenBenennen(params_flaeche).run()
    gc.collect()

@pytest.mark.order3
def test3_loeschen(params_verwaltung, mocked_map_document):        
    params_verwaltung.action.value = "Bestehendes Projekt löschen"
    Projektverwaltung(params_verwaltung).run()

if __name__ == '__main__':
    pytest.main([__file__])

