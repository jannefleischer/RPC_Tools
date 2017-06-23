# -*- coding: utf-8 -*-
import os
import pythonaddins
from imp import load_source

from rpctools.utils.singleton import Singleton
from rpctools.utils.config import Folders, Config

__all__ = ['ToolboxWrapper', 'ToolboxButton', 'Output']

folders = Folders()
config = Config()


class ToolboxWrapper(object):
    # path to pyt file
    _path = None
    # the pyt importing the required toolbox
    _pyt_file = None
    # the class name of the toolbox (as imported in the pyt file)
    _toolbox_name = None

    def __init__(self):
        self.path = os.path.join(self._path, self._pyt_file)
        self._tbx = None

    @property
    def tbx(self):
        """the instanciated toolbox (load on demand only)"""
        if not self._tbx:
            tbx_module = load_source(self._toolbox_name,
                                     self.path.encode('utf-8'))
            self._tbx = getattr(tbx_module, self._toolbox_name)()
            self._tbx.getParameterInfo()
        return self._tbx


class ToolboxButton(ToolboxWrapper):
    """super class for buttons calling toolboxes on click"""
    # show the toolbox on click (if False, just execute the Tool)
    _do_show = True

    def __init__(self):
        super(ToolboxButton, self).__init__()
        self.enabled = True
        self.checked = False

    def onClick(self):
        """call toolbox on click"""
        # validate active project
        self.tbx.set_active_project()
        valid, msg = self.tbx.validate_inputs()
        # call toolbox
        if valid:
            # let the GUI build an instance of the toolbox to show it
            # (regular call of updateParameters etc. included)
            if self._do_show:
                pythonaddins.GPToolDialog(self.path, self._toolbox_name)
            # execute main function of Tool only (no updates etc. possible)
            else:
                self.tbx.execute()
        else:
            pythonaddins.MessageBox(msg, 'Fehler', 0)


class Output(ToolboxWrapper):
    '''wrapper to show outputs of specific tool'''
    __metaclass__ = Singleton
    _show_layers = True
    _show_diagrams = True
    def show(self):
        self.tbx.set_active_project()
        self.tbx.show_outputs(show_layers=self._show_layers, 
                              show_diagrams=self._show_diagrams)
        
    def onClick(self):
        self.show()
