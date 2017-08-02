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
    _toolbox_name = 'TbxWanderungssalden1'


class EinwohnersaldenBearbeiten(ToolboxButton):
    """Implementation for rpc_tools.einwohnersalden (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxEWSaldenbearbeiten'


class BeschaeftigtensaldenSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxWanderungssalden2'


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


class Einkommensteuer(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxEinkommensteuer'


class Grundsteuer(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_grundsteuer_b (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxGrundsteuer'


class Hebesaetze(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxKontrolleGewerbesteuer'


class Gemeindebilanzen(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxGewerbesteuer'


class BilanzenGesamtsumme(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxGesamtsumme'


class Umsatzsteuer(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxUmsatzsteuer'


class BilanzenHinweise(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_gewerbesteuer (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    #_do_show = False
    _toolbox_name = 'TbxErgebnisinterpretation'


class Familienleistungsausgleich(ToolboxButton):
    """Implementation for rpc_tools.hebesaetze_grundsteuer_b (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Einnahmen.pyt'
    _toolbox_name = 'TbxFLA'

