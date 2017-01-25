# -*- coding: utf-8 -*-

import arcpy
import pytest
import os
import shutil

from rpctools.utils.config import _TEST_TMP_PROJECT, TEST_TEMPLATE

@pytest.fixture(scope='session')
def mocked_map_document():
    # mocks the access to a currently opened mxd in arcgis
    MapDocument = arcpy.mapping.MapDocument
    def mocked_doc(path):
        if path == 'CURRENT':
            return MapDocument(os.path.join(os.path.dirname(__file__),
                                            "test.mxd"))
        return MapDocument(path)
    arcpy.mapping.MapDocument = mocked_doc
    return arcpy
    
@pytest.fixture
def test_name():
    # common test-name (not shown in toolbox)
    return TEST_TMP_PROJECT

@pytest.fixture
def test_template_name():
    # name of test-template (not shown in toolbox)
    return TEST_TEMPLATE

def remove_project_dir(toolbox):
    project_dir = toolbox.folders.PROJECT_PATH
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)