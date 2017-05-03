# -*- coding: utf-8 -*-
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
import arcpy

class Settings(Tool):
    _dbname = 'FGDB_Verkehr.gdb'
    _param_projectname = 'project'
    
    def run(self):
        pass

class TbxSettings(Tbx):

    @property
    def label(self):
        return encode(u'Schritt 1: Einstellungen des Verkehrsaufkommens')

    @property
    def Tool(self):
        return Settings
    
    def _getParameterInfo(self):
        params = self.par
        
        # Projekt
        param = params.project = arcpy.Parameter()
        param.name = u'Projekt'
        param.displayName = u'Projekt'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        
        category = 'Verkehrsaufkommen Wohnen'
        
        # Wohnen
        param = params.wohnen_wege_ev = arcpy.Parameter()
        param.name = u'Wohnen_Wege_EW'
        param.displayName = u'Wege je Einwohner und Werktag'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPDouble'
        param.value = 3.3
        param.category = category
    
        param = params.wohnen_miv = arcpy.Parameter()
        param.name = u'Wohnen_MIV_Anteil'
        param.displayName = u'Anteil PKW-Fahrten'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 65
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = category
    
        category = 'Verkehrsaufkommen Gewerbe'
        
        # Gewerbe
        param = params.gewerbe_wege_ev = arcpy.Parameter()
        param.name = u'Gewerbe_Wege_EW'
        param.displayName = encode(u'Wege je Beschäftigtem und Werktag')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPDouble'
        param.value = 3.3
        param.category = category
    
        param = params.gewerbe_miv = arcpy.Parameter()
        param.name = u'Gewerbe Anteil PKW-Fahrten'
        param.displayName = u'Anteil PKW-Fahrten'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 65
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = category
    
        category = 'Verkehrsaufkommen Einzelhandel'
        
        # Einzelhandel
        param = params.einzelhandel_wege_ev = arcpy.Parameter()
        param.name = u'EH_Wege_EW'
        param.displayName = u'Wege je Kunden und Werktag'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPDouble'
        param.value = 3.3
        param.category = category    
        
        param = params.einzelhandel_miv = arcpy.Parameter()
        param.name = u'EH_MIV_Anteil'
        param.displayName = u'Anteil PKW-Fahrten'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Long'
        param.value = 65
        param.filter.type = 'Range'
        param.filter.list = [0, 100]
        param.category = category
        
        return params
    

    