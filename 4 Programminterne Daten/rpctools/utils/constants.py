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

from enum import Enum

class Nutzungsart(Enum):
    UNDEFINIERT = 0
    WOHNEN = 1
    GEWERBE = 2
    EINZELHANDEL = 3
    
class Branche(Enum):
    VERARBEITEND = 1
    BAUGEWERBE = 2
    GROSSHANDEL = 3
    FINANZEN = 4
    DIENSTLEISTUNGEN = 5
    OEFFENTLICH = 6
    
class Gewerbegebietstyp(Enum):
    BENUTZERDEFINIERT = 0
    GEWERBE_GROSS = 1
    GEWERBE_KLEIN = 2
    TECHNOLOGIE = 3
    LOGISTIK = 4
    BUERO = 5
    