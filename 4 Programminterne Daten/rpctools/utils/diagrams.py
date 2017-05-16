import matplotlib
#matplotlib.use('ps')
import matplotlib.pyplot as plt
import subprocess
import os
from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod
from rpctools.utils.params import Tbx, Tool
from rpctools.utils import diagram_exec
from rpctools.utils.encoding import encode
import sys
import pickle


class Dummy(Tool):
    
    def run(self):
        pass


class Diagram(Tbx):
    '''
    superclass to plot diagrams with matplotlib
    '''
    # USE THIS PLT, NEVER IMPORT MATPLOTLIB SOMEWHERE ELSE!!!!
    # (matplotlib needs to be set to PS, as tkinter causes errors and
    # crashes within arcmap)
    plt = plt
    def __init__(self, title='Diagramm'):
        """
        title : str
        """
        super(Diagram, self).__init__()
        self.title = title
        self.figure = None
        
    def show(self, external=True):
        '''
        show the created plot in current process or externally in own process
        
        if not shown in external process, ArcMap will crash
        
        Parameters
        ----------
        external: bool, optional
            show the plot in an external process
            defaults to True
        '''
        filename = os.path.join(self.folders.TEMPORARY_GDB_PATH, 
                                '{}diagram.pickle'.format(
                                    self.__class__.__name__))
        if external:
            self.show_external(self.figure, filename)
        else: 
            self.plt.show()
        
    def create(self, **kwargs):
        '''
        create a plot
        
        Parameters
        ----------
        projectname: str, optional
            the name of the project the data the plot is based on belongs to
            defaults to the active project
            
        kwargs: other optional parameters the subclassing diagram needs
        '''
        projectname = kwargs['projectname'] if 'projectname' in kwargs else None
        self._getParameterInfo()
        self.set_active_project(projectname=projectname)
        self.figure = self._create(**kwargs)
        
    def _create(self):
        """to be implemented by subclasses,
        has to return the axes-object of the plot"""
        
    @property
    def label(self):
        return ''
    
    def _getParameterInfo(self):
        p = self.add_parameter('projectname')
        p.name = 'Projekt'
        p.displayName = 'Projekt'
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.filter.list = []
        return self.par
    
    @property
    def Tool(self):
        return Dummy
    
    def show_external(self, plot, filename):
        if plot is None:
            return
        with open(filename,'wb') as f:
            pickle.dump(plot, f)
        subprocess.Popen(
            [os.path.join(sys.exec_prefix, 'python.exe'),
             '-m' , diagram_exec.__name__, '-f', filename,
             '-t', encode(self.title)], shell=True)
