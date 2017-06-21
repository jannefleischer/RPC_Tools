from rpctools.addins.common import ToolboxButton, folders

__all__ = [
    "NutzungenDefinieren", "Wohnen", "Gewerbe", "Einzelhandel"
]


class NutzungenDefinieren(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxTeilflaecheVerwalten'


class Wohnen(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenWohnen'


class Gewerbe(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenGewerbe'


class Einzelhandel(ToolboxButton):
    _path = folders.DEFINITION_PYT_PATH
    _pyt_file = 'Projektdefinition.pyt'
    _toolbox_name = 'TbxNutzungenEinzelhandel'