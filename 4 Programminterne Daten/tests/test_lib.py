# -*- coding: utf-8 -*-

import arcpy
import pytest
import os
import shutil

from rpctools.utils.config import TEST_TMP_PROJECT

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
    
@pytest.fixture(scope='module')
def test_name():
    # common test-name (not shown in toolbox)
    return TEST_TMP_PROJECT

def remove_project_dir(toolbox):
    project_dir = toolbox.folders.PROJECT_PATH
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)

def setup_template_dir(toolbox):
    print('setup')
    remove_project_dir(toolbox)
    shutil.copytree(
        os.path.join(toolbox.folders.TEST_TEMPLATE),
        os.path.join(toolbox.folders.PROJECT_PATH)
    )
