# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import arcpy
from rpctools.utils.params import Tool

class Ergebnisinterpretation(Tool):
    """Ergebnisinterpretation-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        pass

    def run(self):
        """run Ergebnisinterpretation Tool"""
        text =  "Alle Werte der fiskalischen Bilanz verstehen sich als 'pro Jahr'-Angaben. " + "Diese beziehen sich auf einen Zeitpunkt deutlich nach dem Bezugsbeginn des Planungsprojekts. Zu diesem Zeitpunkt ist der Bezug vollständig abgeschlossen. Zudem sind für Wohngebietsflächen mindestens sieben Jahre vergangen, denn in den ersten sieben Jahren hat die Zuweisung der Einkommensteuer i.d.R. noch nicht auf die Neubau-bedingten Einwohnerwanderungen reagiert."
        title = "Hinweise zur Ergebnisinterpretation"
        return ctypes.windll.user32.MessageBoxW(0, text, title, 0)

