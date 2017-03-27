# -*- coding: utf-8 -*-

import pytest
import gc

from rpctools.analyst.infrastrukturkosten.tbx_kostenermittlung \
     import TbxInfrastrukturkostenermittlung
from rpctools.analyst.infrastrukturkosten.tbx_aufteilungsregeln \
     import TbxKostenaufteilungsregeln, Kostenregeln, ACTIONS
from rpctools.analyst.infrastrukturkosten.kostenmodell import Kostenmodell
from test_lib import test_name, test_name, setup_template_dir


### get the toolboxes with their parameters ###

@pytest.fixture(scope='module')
def tbx_regeln():
    tbx = TbxKostenaufteilungsregeln()
    params = tbx._getParameterInfo()
    tbx._updateParameters(params)
    return tbx

@pytest.fixture(scope='module')
def tbx_ermittlung(test_name):
    tbx = TbxInfrastrukturkostenermittlung()
    params = tbx._getParameterInfo()
    tbx._updateParameters(params)
    tbx.par.projectname.value = test_name
    return tbx

### copy the test template to the test project (if passed as test argument) ###

@pytest.fixture(scope='module')
def setup_template(tbx_ermittlung):
    setup_template_dir(tbx_ermittlung)

### setup the parameters used in the tests ###

@pytest.fixture
def params_regeln(tbx_regeln):
    params = tbx_regeln.par
    params.name.value = 'Testregel'
    params.gemeinden.value = 30
    params.kreis.value = 30
    params.private.value = 40
    return params

@pytest.fixture
def params_ermittlung(tbx_ermittlung):
    params = tbx_ermittlung.par
    params.sonderkostenfaktor.value = 0
    params.entwaesserungssystem.value = 'Mischwassersystem'
    ### 01 - Zusatzangaben Entwässerung ###
    params.rueckhaltebecken_typ.value = None
    params.rueckhaltebecken_m3.value = None
    params.zus_kanalmeter.value = None
    ### 02 - Zusätzliche Kostenfaktoren ###
    params.zus_herstellungskosten.value = None
    params.zus_betriebskosten.value = None
    ### 03 - Aufteilung der Kosten auf Kostenträger ###
    params.KB1_KP1.value = 'Kommune zahlt alles'
    params.KB2_KP1.value = '§127 BauGB'
    params.KB2_KP2.value = 'Kommune zahlt alles'
    params.KB2_KP3.value = 'Kommune zahlt alles'
    params.KB3_KP1.value = '§127 BauGB'
    params.KB3_KP2.value = 'Kommune zahlt alles'
    params.KB3_KP3.value = 'Kommune zahlt alles'
    params.KB4_KP1.value = '§127 BauGB'
    params.KB4_KP2.value = 'Kommune zahlt alles'
    params.KB4_KP3.value = 'Kommune zahlt alles'
    params.KB5_KP1.value = '§127 BauGB'
    params.KB5_KP2.value = 'Kommune zahlt alles'
    params.KB5_KP3.value = 'Kommune zahlt alles'
    params.KB6_KP1.value = '§127 BauGB'
    params.KB6_KP2.value = 'Kommune zahlt alles'
    params.KB6_KP3.value = 'Kommune zahlt alles'
    params.KB7_KP1.value = '§127 BauGB'
    params.KB7_KP2.value = 'Kommune zahlt alles'

    return params

### Tests (with the above defined parameter-functions as arguments) ###

def test_regeln(params_regeln):
    for action in ACTIONS:
        params_regeln.action.value = action
        Kostenregeln(params_regeln).run()

def test_kosten(params_ermittlung, setup_template):
    gc.collect()
    Kostenmodell(params_ermittlung).run()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

