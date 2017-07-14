from rpctools.addins.common import ToolboxButton, folders, config
from rpctools.addins.outputs import AnbindungspunkteAnzeigen

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
        self.output = AnbindungspunkteAnzeigen()
        
    def onClick(self, coord=None):
        self.output.show()

    def onMouseDownMap(self, x, y, button, shift):
        config.active_coord = (x, y)
        super(Anbindungspunkt, self).onClick()