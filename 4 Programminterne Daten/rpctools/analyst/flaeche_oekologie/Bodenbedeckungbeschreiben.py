# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# Bodenbedeckungbeschreiben.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
import os
import arcpy
import sys
from os.path import join
from rpctools.utils.params import Tool

class BodenbedeckungVornutzung(Tool):

    def run(self):
        messages = self.mes
        parameters = self.par

    	wcd = os.getcwd()
    	rootPfad = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]

    	#Projektname
    	projekt = parameters[0].valueAsText
    	gdb = "FGDB_Flaeche_und_Oekologie_" + projekt + ".gdb"
    	pfad_flaeche = join(rootPfad,'3 Benutzerdefinierte Projekte',projekt,gdb,"Bodenbedeckung")
    	#Feldliste erstellen
    	try:
    		fields = arcpy.ListFields(pfad_flaeche)
    		#messages.AddMessage(fields)
    		update = arcpy.UpdateCursor(pfad_flaeche)
    		for row in update:
    			#messages.AddMessage(row.Teilflaeche)
    			for field in fields:
    				#messages.AddMessage(field.name)
    				if row.getValue(field.name) == None:
    					#messages.AddMessage(field.name)
    					row.setValue(field.name,0)
    			update.updateRow(row)
    		del update
    	except Exception as e:
    		messages.AddMessage(e)
    		del update


class BodenbedeckungPlanfall(Tool):

    def run(self):
        messages = self.mes
        parameters = self.par

    	wcd = os.getcwd()
    	rootPfad = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]

    	#Projektname
    	projekt = parameters[0].valueAsText
    	gdb = "FGDB_Flaeche_und_Oekologie_" + projekt + ".gdb"
    	pfad_flaeche = join(rootPfad,'3 Benutzerdefinierte Projekte',projekt,gdb,"Bodenbedeckung")
    	#Feldliste erstellen
    	try:
    		fields = arcpy.ListFields(pfad_flaeche)
    		#messages.AddMessage(fields)
    		update = arcpy.UpdateCursor(pfad_flaeche)
    		for row in update:
    			#messages.AddMessage(row.Teilflaeche)
    			for field in fields:
    				#messages.AddMessage(field.name)
    				if row.getValue(field.name) == None:
    					#messages.AddMessage(field.name)
    					row.setValue(field.name,0)
    			update.updateRow(row)
    		del update
    	except Exception as e:
    		messages.AddMessage(e)
    		del update