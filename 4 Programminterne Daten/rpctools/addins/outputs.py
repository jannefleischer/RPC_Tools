from rpctools.addins.common import Output, folders


class ProjektAnzeigen(Output):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektverwaltung.pyt'
    _toolbox_name = 'TbxProjektauswahl'


class ErschliessungsnetzeAnzeigen(Output):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Infrastrukturkosten.pyt'
    _toolbox_name = 'TbxInfrastrukturmengenBilanz'
    _show_diagrams = False


class ZentrenAnzeigen(Output):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxEditCenters'


class MaerkteAnzeigen(Output):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Standortkonkurrenz_Supermaerkte.pyt'
    _toolbox_name = 'TbxOSMMarktEinlesen'
    

class HaltestellenAnzeigen(Output):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Erreichbarkeit.pyt'
    _toolbox_name = 'TbxHaltestellenZentraleOrte'
    

class AnbindungspunkteAnzeigen(Output):
    _path = folders.ANALYST_PYT_PATH
    _pyt_file = 'Verkehrserzeugung.pyt'
    _toolbox_name = 'TbxSetSource'

