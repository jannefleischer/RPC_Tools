import matplotlib
matplotlib.use('ps')
import matplotlib.pyplot as plt
import subprocess
import os
from argparse import ArgumentParser
from abc import abstractmethod
import sys
import pickle
import arcpy

from rpctools.utils.params import DummyTbx
from rpctools.utils import diagram_exec
from rpctools.utils.encoding import encode


class Diagram(DummyTbx):
    _workspace = None
    
    def __init__(self, projectname=None, title='Diagramm'):
        """
        title : str
        """
        super(Diagram, self).__init__()    
        self.projectname = projectname
        self.title = title
        if self._workspace:
            self.folders._workspace = self._workspace
        
    @abstractmethod
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

    def show(self):
        pass    


class ArcpyDiagram(Diagram):
    
    def __init__(self, projectname=None, title='Diagramm'):
        """
        title : str
        """
        super(ArcpyDiagram, self).__init__(projectname=projectname, title=title)
        self.graph = None
        self.template = None
        
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
        self._getParameterInfo()
        self.set_active_project(projectname=self.projectname)
        self.graph, self.template = self._create(**kwargs)
        self.created = True

    def _create(self, **kwargs):
        """to be implemented by subclasses,
        has to return the graph-object and the path to the template"""
        
    def show(self):
        #if not self.graph:
        self.create()
        title = self.graph.graphPropsGeneral.title or self.title
        self.output.add_graph(self.template, self.graph, title)



class MatplotDiagram(Diagram):
    '''
    superclass to plot diagrams with matplotlib
    '''
    # USE THIS PLT, NEVER IMPORT MATPLOTLIB SOMEWHERE ELSE!!!!
    # (matplotlib needs to be set to PS, as tkinter causes errors and
    # crashes within arcmap)
    plt = plt
    def __init__(self, projectname=None, title='Diagramm'):
        """
        title : str
        """
        super(MatplotDiagram, self).__init__(projectname=projectname, title=title)
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
        #if not self.figure:
        self.create()
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

    def show_external(self, plot, filename):
        if plot is None:
            return
        with open(filename,'wb') as f:
            pickle.dump(plot, f)
        subprocess.Popen(
            [os.path.join(sys.exec_prefix, 'python.exe'),
             '-m' , diagram_exec.__name__, '-f', filename,
             '-t', encode(self.title)], shell=True)
        
    def _create(self, **kwargs):
        """to be implemented by subclasses,
        has to return the axes-object of the plot"""
