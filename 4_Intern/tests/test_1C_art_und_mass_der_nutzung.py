# -*- coding: utf-8 -*-

from rpctools.definitions.nutzungsart.tbx_flaechenbilanz import TbxFlaechenbilanz
from rpctools.definitions.nutzungsart.tbx_nutzungen import TbxNutzungen
from rpctools.definitions.nutzungsart.flaechenbilanz import Flaechenbilanz
from rpctools.definitions.nutzungsart.nutzungen import Nutzungen

from test_lib import (test_name, remove_project_dir, test_name,
                      setup_template_dir)
import os, shutil, gc
from os.path import join
from time import gmtime, strftime
import pytest

### get the toolboxes with their parameters ###

@pytest.fixture(scope='module')
def tbx_bilanz(test_name):
    tbx = TbxFlaechenbilanz()
    tbx._getParameterInfo()
    tbx.par.projectname.value = test_name
    return tbx

@pytest.fixture(scope='module')
def tbx_nutzungen(test_name):
    tbx = TbxNutzungen()
    params = tbx._getParameterInfo()
    tbx._updateParameters(params)
    tbx.par.projectname.value = test_name
    return tbx

@pytest.fixture(scope='module')
def setup_template(tbx_bilanz):
    setup_template_dir(tbx_bilanz)

### setup the parameters used in the tests ###

@pytest.fixture(scope='module')
def flaechenname():
    return 'Flaeche_1'

@pytest.fixture
def params_bilanz(tbx_bilanz, flaechenname, test_name):
    params = tbx_bilanz.par
    params.teilflaeche.value = flaechenname    
    params.projectname.value = test_name
    params.startjahr.value = 2017
    
    ### 01_Generelle Flächenaufteilung ###
    params.ant_verkehrsfl.value = 10
    params.ant_gruenfl.value = 10
    params.ant_sonstige_fl.value = 10
    params.ant_nettobauland.value = 70
    ### 02_Aufteilung Nettobauland ###
    params.ant_gewerbefl.value = 10
    params.ant_nettowohnbauland.value = 90
    ### 03_Aufteilung Verkehrsfläche ###
    params.laermschutz.value = 10
    params.privatwege.value = 10
    params.auessere_erschl.value = 10
    params.innere_erschl.value = 70
    ### 04_Aufteilung Grünfläche ###
    params.spielplatz.value = 10
    params.strassenbegleitgruen.value = 10
    params.ausgleich_ersatz.value = 10
    params.allg_gruen.value = 70
    
    return params

@pytest.fixture
def params_nutzungen(tbx_nutzungen, flaechenname, test_name):
    params = tbx_nutzungen.par
    params.teilflaeche.value = flaechenname   
    params.projectname.value = test_name
    params.beginn_aufsiedlung.value = 2017
    
    ### 1) Aufsiedlungszeitraum ###
    params.dauer_aufsiedlung.value = 5
    ### 2) Wohnen - Anzahl Wohneinheiten nach Gebäudetypen ###
    params.we_efh.value = 100
    params.we_zfh.value = 100
    params.we_rh.value = 100
    params.we_mfh.value = 100
    ### 3) Wohnen - Anteile Eigentum und Miete ###
    params.ant_eigentum_efh.value = 90
    params.ant_eigentum_zfh.value = 80
    params.ant_eigentum_rh.value = 70
    params.ant_eigentum_mfh.value = 20
    ### 4) Wohnen - Einwohner pro Wohneinheit ###
    params.ew_je_we_efh.value = '3,2 Bewohner pro Wohneinheit'
    params.ew_je_we_zfh.value = '3,0 Bewohner pro Wohneinheit'
    params.ew_je_we_rh.value = '3,0 Bewohner pro Wohneinheit'
    params.ew_je_we_mfh.value = '2,1 Bewohner pro Wohneinheit'
    ### 5) Wohnen - Zuzugsquote ###
    params.zuzugsquote_ew.value = 80
    ### 6) Gewerbe - Gebietstyp und Brachenstruktur ###
    params.gebietstyp.value = '<kein Gewerbegebiet vorhanden>'
    params.ant_jobs_verarb_gewerbe.value = 40
    params.ant_jobs_baugewerbe.value = 6
    params.ant_jobs_handel.value = 17
    params.ant_jobs_logistik.value = 10
    params.ant_jobs_freiwisstech.value = 14
    params.ant_jobs_sonst_dl.value = 13
    ### 7) Gewerbe - Zuzugs- und Eigentumsquote ###
    params.zuzugsquote_gewerbe.value = 80
    params.ant_eigentum_gewerbe.value = 100
    ### 8) Einzelhandel (nur Lebensmitteleinzelhandel) ###
    params.verkaufsflaeche.value = 2000    
    
    return params
    
### Tests (with the above defined parameter-functions as arguments) ### 
    
def test_bilanz(tbx_bilanz, params_bilanz, setup_template):
    Flaechenbilanz(params_bilanz).run()
    
def test_nutzung(tbx_nutzungen, params_nutzungen, setup_template):
    Nutzungen(params_nutzungen).run()

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--setup-show'])

