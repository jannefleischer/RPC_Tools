# -*- coding: utf-8 -*-
from rpctools.addins.common import ToolboxButton, folders

__all__ = [
    "HaltestellenEinlesen", "Haltestellenplan",
    "FahrtzeitZentraleOrte", "Isochrone", 
    "EinrichtungenEinlesen"
]


class HaltestellenEinlesen(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = u'Erreichbarkeit.pyt'
    _toolbox_name = '?'


class Haltestellenplan(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = u'Erreichbarkeit.pyt'
    _toolbox_name = '?'


class FahrtzeitZentraleOrte(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = u'Erreichbarkeit.pyt'
    _toolbox_name = '?'


class Isochrone(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = u'Erreichbarkeit.pyt'
    _toolbox_name = 'TbxIsochrone'


class EinrichtungenEinlesen(ToolboxButton):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = u'Erreichbarkeit.pyt'
    _toolbox_name = 'TbxEinrichtungen'
