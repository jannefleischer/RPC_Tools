# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from collections import OrderedDict

class MassnahmeBeschreiben(Tool):
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Kosten.gdb'
    
    def run(self):
        """"""


class TbxMassnahmeBeschreiben(Tbx):

    @property
    def label(self):
        return encode(u'Schritt ?: Maßnahme beschreiben')

    @property
    def Tool(self):
        return MassnahmeBeschreiben

    def _getParameterInfo(self):
        # Projekt
        params = self.par
        p = self.add_parameter('projectname')
        p.name = u'Projekt'
        p.displayName = u'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        projects = self.folders.get_projects()
        p.filter.list = projects
        p.value = '' if len(projects) == 0 else p.filter.list[0]
    
        self.elements = self.get_punctual_elements()
        
        p = self.add_parameter('netzelement')
        p.name = encode(u'Netzelement')
        p.displayName = encode(u'Netzelement')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        values = self.elements.keys()
        p.filter.list = values
        if values:
            p.value = values[0]
    
        p = self.add_parameter('massnahmen')
        p.name = encode(u'Maßnahmen')
        p.displayName = encode(u'Maßnahmen')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
        p.filter.list = []
    
        p = self.add_parameter('desc')
        p.name = encode(u'Bezeichnung der Maßnahme')
        p.displayName = encode(u'Bezeichnung der Maßnahme')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPString'
    
        p = self.add_parameter('kosten_eh')
        p.name = u'Kosten der erstmaligen Herstellung (Euro)'
        p.displayName = u'Kosten der erstmaligen Herstellung (Euro)'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPDouble'
    
        p = self.add_parameter('kosten_bu')
        p.name = encode(u'Jährliche Kosten für Betrieb und Unterhaltung (Euro)')
        p.displayName = encode(u'Jährliche Kosten für '
                               u'Betrieb und Unterhaltung (Euro)')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPDouble'        
    
        p = self.add_parameter('kosten_en')
        p.name = encode(u'Erneuerungskosten nach Ablauf der Lebensdauer (Euro)')
        p.displayName = encode(u'Erneuerungskosten nach Ablauf der '
                               u'Lebensdauer (Euro)')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPDouble'
        
        p = self.add_parameter('lebensdauer')
        p.name = encode(u'Technische oder wirtschaftliche Lebensdauer bis '
                        u'zur Erneuerung (Jahre)')
        p.displayName = encode(u'Technische oder wirtschaftliche Lebensdauer '
                               u'bis zur Erneuerung (Jahre)')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = u'GPLong'
        p.filter.type = 'Range'
        p.filter.list = [0, 100]

        self.add_temporary_management(self.folders.dbname)
        
        return params
        
    def _open(self, params):
        self.update_netzelement()
        self._recently_opened = True
        
    def get_punctual_elements(self):
        table = 'Netze_und_Netzelemente'
        columns = ('Netzelement', 'IDNetzelement')
        elements = OrderedDict(self.query_table(
            table, workspace='FGDB_Kosten_Tool.gdb', 
            columns=columns, is_base_table=True,
            where="Typ = 'Punkt'"
        ))
        return elements
        
    def update_netzelement(self):
        netzelement = self.par.netzelement.value
        id_netzelement = self.elements[netzelement]
        massnahmen = self.get_massnahmen(id_netzelement)
        self.par.massnahmen.filter.list = massnahmen
        
    def get_massnahmen(self, id_netzelement):
        table = 'Erschliessungsnetze_Punktelemente'
        massnahmen = self.query_table(
            table, columns=['Bezeichnung'],
            where='IDNetzelement = {}'.format(id_netzelement))
        return [m[0] for m in massnahmen]
        
    def update_massnahme(self):
        massnahme = self.par.massnahmen.value
        self.par.desc.value = massnahme
        table = 'Erschliessungsnetze_Punktelemente'
        values = self.query_table(
            table, columns=['Kosten_EH_EUR', 'Kosten_BU_EUR',
                            'Kosten_EN_EUR', 'Lebensdauer'],
            where="Bezeichnung = '{}'".format(massnahme))[0]
        self.par.kosten_eh.value = values[0]
        self.par.kosten_bu.value = values[1]
        self.par.kosten_en.value = values[2]
        self.par.lebensdauer.values = values[3]

    def _updateParameters(self, params):
        if params.changed('projectname'):
            self._open(params)

        if params.changed('netzelement') and self.par.netzelement.filter.list:
            self.update_netzelement()
            
        if params.changed('massnahmen') and self.par.massnahmen.filter.list:
            # don't commit after toolbox just opened (else the defaults overwrite
            # the actual settings)
            if not self._recently_opened:
                self.commit_changes()
            self.update_massnahme() 
            
        self._recently_opened = False
        return params    

    def commit_changes(self):
        pass
    
if __name__ == '__main__':
    t = TbxMassnahmeBeschreiben()
    params = t.getParameterInfo()