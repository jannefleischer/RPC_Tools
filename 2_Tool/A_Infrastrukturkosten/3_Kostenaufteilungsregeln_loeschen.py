# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Kostenaufteilungsregeln_loeschen.py
# 
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import arcpy

import kosten_lib as k

arcpy.env.overwriteOutput = True

#Pfade einrichten
name = arcpy.GetParameterAsText(0)

k.kostenregel_loeschen(name)

# Endmeldung
message = 'Regel geloescht'
print message
arcpy.AddMessage(message)