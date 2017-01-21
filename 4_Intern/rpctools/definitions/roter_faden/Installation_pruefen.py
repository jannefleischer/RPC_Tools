# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# install_packages.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------

from os.path import abspath, dirname, join
BASE_PATH = dirname(dirname(abspath(__file__)))
sys.path.append(join(BASE_PATH, '4_Intern'))

from rpctools.utils.params import Tool


class InstallationPruefen(Tool):
    """"""
    def main(self):
        """"""


