# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# project_lib.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH / HCU Hamburg / GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', '..'))
PROJECT_FOLDER = os.path.join(BASE_PATH, '3_Projekte')
PROJECT_TEMPLATE = 'Template'
TEST_TEMPLATE = 'Test_Template'
TEST_TMP_PROJECT = '__unittest__'

def get_projects():
    '''
    returns all available projects inside the project folder
    (except the template and temp. projects which are not meant to be edited)
    '''
    subfolders = [s for s in os.listdir(PROJECT_FOLDER)
                  if os.path.isdir(os.path.join(PROJECT_FOLDER, s))   
                  and s not in [PROJECT_TEMPLATE, 
                                TEST_TEMPLATE, 
                                TEST_TMP_PROJECT
                                ]
                  ]    
    return subfolders

if __name__ == "__main__":
    get_projects()