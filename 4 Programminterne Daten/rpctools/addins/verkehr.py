from rpctools.addins.common import ToolboxButton, folders, config

__all__ = ['InitialRouting', 'RoutingSettings',
           'WeightedRouting', 'Anbindungspunkt']


class InitialRouting(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxRouting'


class RoutingSettings(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxSettings'


class WeightedRouting(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxUpdateNodes'


class Anbindungspunkt(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxSetSource'

    def __init__(self):
        super(Anbindungspunkt, self).__init__()
        self.enabled = True
        self.shape = 'NONE'
        self.cursor = 3
        
    def onClick(self, coord=None):
        if coord is None:
            return
        config.active_coord = coord
        super(Anbindungspunkt, self).onClick()

    def onMouseDownMap(self, x, y, button, shift):
        self.onClick((x, y))