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
TEMPLATE_FOLDER = os.path.join(BASE_PATH, '4_Intern', 'templates')
TEMPLATE_FLAECHEN = 'projektflaechen_template.shp'
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
    return sorted(subfolders)

def get_gdb(project, fgdb):
    gdb = os.path.join(BASE_PATH,
                         '3_Projekte',
                         project,
                         fgdb)
    return gdb

def get_table(project, fgdb, tablename):
    table = os.path.join(get_gdb(project, fgdb), tablename)
    return table

def get_template_flaechen():
    flaechen = os.path.join(TEMPLATE_FOLDER, TEMPLATE_FLAECHEN)
    return flaechen


def encode(text):
    """encode text to CP1252"""
    if not isinstance(text, unicode):
        try:
            u = text.decode('utf8')
        except UnicodeDecodeError:
            u = text.decode('latin1')
        except UnicodeDecodeError:
            u = text.decode('CP1252')
    else:
        u = text
    text_cp1252 = u.encode('CP1252')
    return text_cp1252


if __name__ == "__main__":
    get_projects()