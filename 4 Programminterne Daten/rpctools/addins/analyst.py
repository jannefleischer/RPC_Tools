from rpctools.utils.config import Folders
import os

folders = Folders()

__all__ = ["BewohnerSchaetzen", "WanderungssaldenSchaetzen",
           "Einwohnersalden", "Beschaeftigtensalden",
           "EinnahmeverschiebungenSchaetzen"]


### BEWOHNER ARBEISTPLAETZE ###


class BewohnerSchaetzen(object):
    """Implementation for rpc_tools.bewohner_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Bewohner_Arbeitsplaetze.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxBewohner')


### EINNAHMEN ###


class WanderungssaldenSchaetzen(object):
    """Implementation for rpc_tools.wanderungssalden_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxWanderungssalden')


class Einwohnersalden(object):
    """Implementation for rpc_tools.einwohnersalden (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxEWSaldenbearbeiten')


class Beschaeftigtensalden(object):
    """Implementation for rpc_tools.beschaeftigtensalden (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxGewSaldenbearbeiten')


class EinnahmeverschiebungenSchaetzen(object):
    """Implementation for rpc_tools.einnahmeverschiebungen_schaetzen (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = os.path.join(folders.ANALYST_PYT_PATH,
                                 'Einnahmen.pyt')
    def onClick(self):
        pythonaddins.GPToolDialog(self.path, 'TbxSteuersalden')
