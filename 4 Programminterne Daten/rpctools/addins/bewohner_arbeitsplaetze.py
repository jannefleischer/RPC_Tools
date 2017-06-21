from rpctools.addins.common import ToolboxButton, folders

__all__ = ['BewohnerSchaetzen', 'ArbeitsplaetzeSchaetzen']

class BewohnerSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Bewohner_Arbeitsplaetze.pyt'
    _toolbox_name = 'TbxBewohner'


class ArbeitsplaetzeSchaetzen(ToolboxButton):
    """Implementation for rpc_tools.arbeitsplaetze_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Bewohner_Arbeitsplaetze.pyt'
    _toolbox_name = 'TbxArbeitsplaetze'
