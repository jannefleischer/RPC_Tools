# -*- coding: utf-8 -*-
import os
import pythonaddins
from imp import load_source
import functools
import threading

from rpctools.utils.singleton import Singleton
from rpctools.utils.config import Folders, Config

__all__ = ['ToolboxWrapper', 'ToolboxButton', 'Output', 'FileButton']

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
                                     self.path.encode('utf-8'))  # probieren: self.path.encode(sys.getfilesystemencoding())
            self._tbx = getattr(tbx_module, self._toolbox_name)()
            self._tbx.getParameterInfo()
        return self._tbx


class ToolboxButton(ToolboxWrapper):
    """super class for buttons calling toolboxes on click"""
    # show the toolbox on click (if False, just execute the Tool)
    _do_show = True
    _message = None

    def __init__(self):
        super(ToolboxButton, self).__init__()
        self.enabled = True
        self.checked = False
    
    def show_message(self): 
        if self._message:
            pythonaddins.MessageBox(self._message, 'Hinweis', 0)

    def onClick(self):
        """call toolbox on click"""
        self.show_message()
        self.open()
        
    def open(self): 
        # validate active project
        self.tbx.set_active_project()
        valid, msg = self.tbx.validate_active_project()
        # call toolbox
        if valid:
            valid, msg = self.tbx.validate_inputs()
            if valid:
                # let the GUI build an instance of the toolbox to show it
                # (regular call of updateParameters etc. included)
                if self._do_show:
                    pythonaddins.GPToolDialog(self.path, self._toolbox_name)
                # execute main function of Tool only (no updates etc. possible)
                else:
                    self.tbx.execute()
                return
        pythonaddins.MessageBox(msg, 'Fehler', 0)


class Output(ToolboxWrapper):
    '''wrapper to show outputs of specific tool'''
    __metaclass__ = Singleton
    _show_layers = True
    _show_diagrams = True
    _redraw = False
    def show(self):
        self.tbx.set_active_project()
        valid, msg = self.tbx.validate_active_project()
        if not valid:
            pythonaddins.MessageBox(msg, 'Fehler', 0)
            return
        self.tbx.show_outputs(show_layers=self._show_layers, 
                              show_diagrams=self._show_diagrams,
                              redraw=self._redraw)
        
    def onClick(self):
        self.show()
        
def threaded(function):
    @functools.wraps(function)
    def _threaded(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
    return _threaded


class FileButton(object):
    '''class showing pdf-files'''
    _path = folders.MANUALS_PATH
    _file = None
    
    def __init__(self):
        self.open = threaded(os.startfile)
        
    def onClick(self):
        #subprocess.Popen(["start", "/WAIT", "{}".format(os.path.join(self._path, self._file))], shell=True)
        #os.system('start "{}"'.format(os.path.join(self._path, self._file)))
        self.open(os.path.join(self._path, self._file))

