from rpctools.addins.common import ToolboxButton, folders

__all__ = [
    'EinwohnersaldenSchaetzen', 'BeschaeftigtensaldenSchaetzen',
    'EinwohnersaldenBearbeiten', 'BeschaeftigtensaldenBearbeiten',
    'EinnahmeverschiebungenSchaetzen',
    'Einkommensteuer', 'Grundsteuer',
    'Hebesaetze', 'Gemeindebilanzen',
    'BilanzenGesamtsumme', 'Umsatzsteuer',
    'BilanzenHinweise', 'Familienleistungsausgleich'
]


# ToDo: which toolbox for einwohner/beschaeftigte schaetzen?
class EinwohnersaldenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxWanderungssalden'


class BeschaeftigtensaldenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxWanderungssalden'


class EinwohnersaldenBearbeiten(ToolboxButton):
    """Implementation for rpc_tools.einwohnersalden (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxEWSaldenbearbeiten'


class BeschaeftigtensaldenBearbeiten(ToolboxButton):
    """Implementation for rpc_tools.beschaeftigtensalden (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxGewSaldenbearbeiten'


class EinnahmeverschiebungenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.einnahmeverschiebungen_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxSteuersalden'


class Einkommensteuer(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class Grundsteuer(object):
    """Implementation for rpc_tools.hebesaetze_grundsteuer_b (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class Hebesaetze(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
    
class Gemeindebilanzen(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
    
class BilanzenGesamtsumme(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
    
class Umsatzsteuer(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
    
class BilanzenHinweise(object):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class Familienleistungsausgleich(object):
    """Implementation for rpc_tools.hebesaetze_grundsteuer_b (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
