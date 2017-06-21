from rpctools.addins.common import ToolboxButton, folders
from rpctools.addins.outputs import MaerkteAnzeigen, ZentrenAnzeigen

__all__ = [
    "BestandOSMEinlesen", "TemplateErzeugen",
    "TemplateEinlesenDatei", "TemplateEinlesenFeatureClass", 
    "MarktBearbeiten", "MarktHinzu", "BestandMarktBearbeiten",
    "PlanfallMarktBearbeiten", "BestandMarktHinzu",
    "PlanfallMarktHinzu", "PlanfallMarktErweitern",
    "ZentrumBearbeiten", "ZentrumHinzu", "StandortkonkurrenzProjektwirkung"
]


class BestandOSMEinlesen(ToolboxButton):
    """Implementation for rpc_tools.bestand_osm (Button)"""
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxOSMMarktEinlesen'
    _do_show = True


class TemplateErzeugen(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxCreateTemplate'


class TemplateEinlesenDatei(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxMaerkteImportierenDatei'


class TemplateEinlesenFeatureClass(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxMaerkteImportierenFeatureClass'


class MarktBearbeiten(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = None

    def __init__(self):
        super(MarktBearbeiten, self).__init__()
        self.enabled = True
        self.shape = 'NONE'
        self.cursor = 3
        
    def onClick(self, coord=None):
        maerkte_anzeigen.onClick()

    def onMouseDownMap(self, x, y, button, shift):
        config.active_coord = (x, y)
        super(MarktBearbeiten, self).onClick()


class MarktHinzu(MarktBearbeiten):
    '''does the same thing as MarktBearbeiten except adding a market at
    click position before opening toolbox'''
    _new_market_name = ''
    
    def onMouseDownMap(self, x, y, button, shift):
        tbx = self.tbx
        tbx.set_active_project()
        tbx.add_market_to_db(self._new_market_name, (x, y))
        arcpy.RefreshActiveView()
        super(MarktHinzu, self).onMouseDownMap(x, y, button, shift)


class BestandMarktBearbeiten(MarktBearbeiten):
    _toolbox_name = 'TbxEditMarketsNullfall'


class PlanfallMarktBearbeiten(MarktBearbeiten):
    _toolbox_name = 'TbxEditMarketsPlanfall'


class BestandMarktHinzu(MarktHinzu):
    _toolbox_name = 'TbxEditMarketsNullfall'
    _new_market_name = 'unbenannter Markt im Bestand'


class PlanfallMarktHinzu(MarktHinzu):
    _toolbox_name = 'TbxEditMarketsPlanfall'
    _new_market_name = 'unbenannter geplanter Markt'


class PlanfallMarktErweitern(object):
    pass


class ZentrumBearbeiten(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxEditCenters'

    def __init__(self):
        super(ZentrumBearbeiten, self).__init__()
        self.enabled = True
        self.shape = 'NONE'
        self.cursor = 3
        self.output = ZentrenAnzeigen()
        
    def onClick(self, coord=None):
        self.output.show()

    def onMouseDownMap(self, x, y, button, shift):
        config.active_coord = (x, y)
        super(ZentrumBearbeiten, self).onClick()


class ZentrumHinzu(ZentrumBearbeiten):
    _new_center_name = 'unbenannter Versorgungsbereich'
    def __init__(self):
        super(ZentrumHinzu, self).__init__()
        self.shape = 'Line'
        
    def onLine(self, line_geometry):
        tbx = self.tbx
        tbx.set_active_project()
        array = arcpy.Array()
        points = line_geometry.getPart(0)  
        for point in points:  
            array.add(point)
        first = line_geometry.firstPoint
        array.add(first)
        polygon = arcpy.Polygon(array)
        tbx.add_center_to_db(self._new_center_name, polygon)
        arcpy.RefreshActiveView()
        config.active_coord = (first.X, first.Y)
        super(ZentrumBearbeiten, self).onClick()

    def onMouseDownMap(self, x, y, button, shift): 
        pass


class StandortkonkurrenzProjektwirkung(ToolboxButton):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxProjektwirkungMarkets'
