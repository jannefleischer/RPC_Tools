from rpctools.utils.params import Tool
from rpctools.definitions.projektverwaltung.projektverwaltung \
     import Projektverwaltung


class Projektauswahl(Projektverwaltung):
    _param_projectname = 'active_project'
    _workspace = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        self.parent_tbx.config.active_project = self.par.active_project.value
        self.output.define_projection()
        self.add_output_new_project()
        self.add_diagramm()
