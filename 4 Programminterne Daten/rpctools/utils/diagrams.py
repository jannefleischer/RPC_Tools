import subprocess
import os
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from rpctools.utils.params import Tbx, Tool
from rpctools.utils import diagram_exec
import sys
import pickle

class Dummy(Tool):
    
    def run(self):
        pass


class Diagram(Tbx):
    
    def __init__(self, title='Titel'):
        """
        title : str
        """
        super(Diagram, self).__init__()
        self.title = title
        
    def show(self, external=True):
        filename = os.path.join(self.folders.TEMPORARY_GDB_PATH, 
                                'diagram.pickle')
        if external:
            self.show_external(self.figure, filename)
        else: 
            plt.show()
        
    def create(self, projectname=''):
        self._getParameterInfo()
        self.set_active_project(projectname=projectname)
        self.figure = self._create()
        
    def _create(self):
        """"""
        
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
        with open(filename,'wb') as f:
            pickle.dump(plot, f)
        subprocess.Popen(
            [os.path.join(sys.exec_prefix, 'python.exe'),
             '-m' , diagram_exec.__name__, '-f', filename], shell=True)
