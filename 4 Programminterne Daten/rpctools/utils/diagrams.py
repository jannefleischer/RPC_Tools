import subprocess
import os
from argparse import ArgumentParser
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from rpctools.utils.params import Tbx, Tool
import sys

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
        
    def show(self):
        plt.show()
        
    def create(self, projectname=''):
        self._getParameterInfo()
        self.set_active_project(projectname=projectname)
        self._create()
        
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
    
    def run(self, projectname=''):
        clsname = type(self).__name__
        module = self.__module__
        subprocess.Popen(
            [os.path.join(sys.exec_prefix, 'python.exe'),
            '-m' , module, '-p', projectname, '-c', clsname], shell=True)

def show_diagram(my_globals):
    """
    Show diagram in a subprocess
    
    Parameters
    ----------
    my_globals: dict
        a dict with the globals of the calling module
        
    """
    parser = ArgumentParser()
    parser.add_argument('-p', '--projektname', dest='projektname',
                        help='Projektname')
    parser.add_argument('-c', '--clsname', dest='clsname',
                        help='Klassenname')
    options = parser.parse_args()
    diagram = my_globals[options.clsname]()
    diagram.create(options.projektname)
    diagram.show()    