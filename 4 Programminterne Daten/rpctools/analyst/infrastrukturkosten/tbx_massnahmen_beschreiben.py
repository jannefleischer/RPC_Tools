# -*- coding: utf-8 -*-

import arcpy

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from collections import OrderedDict


class MassnahmenBeschreiben(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Kosten.gdb'
    
    def add_outputs(self):
        pass
    
    def run(self):
        """"""


class TbxMassnahmenBeschreiben(Tbx):
    table = 'Erschliessungsnetze_Punktelemente'
    missing_msg = u'keine Maßnahmen vorhanden'

    @property
    def label(self):
        return encode(u'Schritt ?: Maßnahmen beschreiben')

    @property
    def Tool(self):
        return MassnahmenBeschreiben

    def _getParameterInfo(self):        
        params = self.par
        self.current_massnahme_id = None
        
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
        p.displayName = encode(u'Bezeichnung der Maßnahme ändern')
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

        self.add_temporary_management(self.folders.workspace)
        
        return params
        
    def _open(self, params):
        id_netzelement = self.config.active_measure_id
        if id_netzelement is not None:
            element_name = self.elements.keys()[
                self.elements.values().index(id_netzelement)]
            self.par.netzelement.value = element_name
        self.update_netzelement()
        self._recently_opened = True
        
    def execute(self, parameters, messages):
        self.commit_massnahme_changes()
        super(TbxMassnahmenBeschreiben, self).execute(parameters, messages)
        
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
        idx = self.par.selected_index('massnahmen')
        netzelement = self.par.netzelement.value
        id_netzelement = self.elements[netzelement]
        names, self.massnahmen_ids = self.get_massnahmen(id_netzelement)
        self.par.massnahmen.filter.list = names
        if not names:
            massnahme = self.missing_msg
        else:
            idx = max([0, idx])
            massnahme = names[idx]
        self.par.massnahmen.value = massnahme
        self.current_massnahme_id = self.get_selected_massnahme_id()
        self.update_massnahme()
        
    def get_massnahmen(self, id_netzelement):
        rows = self.query_table(
            self.table, columns=['Bezeichnung', 'OBJECTID'],
            where='IDNetzelement = {}'.format(id_netzelement))
        if not rows:
            return [], []
        names, ids = zip(*rows)
        return list(names), list(ids)
    
    def get_selected_massnahme_id(self): 
        idx = self.par.selected_index('massnahmen')
        id = self.massnahmen_ids[idx] if idx >= 0 else None
        return id
        
    def update_massnahme(self):
        massnahme = self.par.massnahmen.value
        enabled = True
        if massnahme == self.missing_msg:
            enabled = False
            self.par.desc.value = ''
        else: 
            self.par.desc.value = massnahme
            id = self.get_selected_massnahme_id()
            values = self.query_table(
                self.table, columns=['Kosten_EH_EUR', 'Kosten_BU_EUR',
                                     'Kosten_EN_EUR', 'Lebensdauer'],
                where="OBJECTID = {}".format(id))[0]
            self.par.kosten_eh.value = values[0]
            self.par.kosten_bu.value = values[1]
            self.par.kosten_en.value = values[2]
            self.par.lebensdauer.values = values[3]
        self.par.massnahmen.enabled = enabled
        self.par.desc.enabled = enabled
        self.par.kosten_eh.enabled = enabled
        self.par.kosten_bu.enabled = enabled
        self.par.kosten_en.enabled = enabled
        self.par.lebensdauer.enabled = enabled

    def _updateParameters(self, params):
        if params.changed('projectname'):
            self._open(params)
            
        if params.changed('netzelement', 'massnahmen', 'desc'):
            if not self._recently_opened:
                self.commit_massnahme_changes()

        if params.changed('netzelement') and self.par.netzelement.filter.list:
            self.update_netzelement()

        elif params.changed('massnahmen') and self.par.massnahmen.filter.list:
            self.current_massnahme_id = self.get_selected_massnahme_id()
            self.update_massnahme()

        elif params.changed('desc'):
            self.update_netzelement()
            
        
        self._recently_opened = False
        return params
    
    def commit_massnahme_changes(self):
        id = self.current_massnahme_id
        if id is None:
            return
        self.update_table(
            self.table,
            {'Bezeichnung': self.par.desc.value,
             'Kosten_EH_EUR': self.par.kosten_eh.value,
             'Kosten_BU_EUR': self.par.kosten_bu.value,
             'Kosten_EN_EUR': self.par.kosten_en.value,
             'Lebensdauer': self.par.lebensdauer.value
             },
            where="OBJECTID = {}".format(id)
        )
    
if __name__ == '__main__':
    t = TbxMassnahmenBeschreiben()
    params = t.getParameterInfo()
    t.execute()
    t.get_massnahmen(13)