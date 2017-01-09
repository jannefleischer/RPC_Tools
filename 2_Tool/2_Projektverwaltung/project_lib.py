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
TEMPLATE_PROJECT = 'Template'

def get_projects():
    subfolders = [s for s in os.listdir(PROJECT_FOLDER)
                  if s != TEMPLATE_PROJECT 
                  and os.path.isdir(os.path.join(PROJECT_FOLDER, s))]
    return subfolders

if __name__ == "__main__":
    get_projects()