# -*- coding: utf-8 -*-
import arcpy

# import the buttons and tools (class names as in config.xml)
from rpctools.addins.infrastruktur import *
from rpctools.addins.nutzungen import *
from rpctools.addins.outputs import *
from rpctools.addins.standortkonkurrenz import *
from rpctools.addins.verkehr import *
from rpctools.addins.bewohner_arbeitsplaetze import *
from rpctools.addins.einnahmen import *
from rpctools.addins.projektverwaltung import *
from rpctools.addins.flaeche_oekologie import *


class SkizzeBeenden(object):
    """Implementation for rpc_tools.skizze_beenden (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.

