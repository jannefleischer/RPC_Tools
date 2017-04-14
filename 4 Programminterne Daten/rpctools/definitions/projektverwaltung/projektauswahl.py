from rpctools.utils.params import Tool
from rpctools.definitions.projektverwaltung.T1_Projektverwaltung \
     import Projektverwaltung


class Projektauswahl(Projektverwaltung):
    _param_projectname = 'active_project'
    _dbname = 'FGDB_Definition_Projekt.gdb'

    def run(self):
        self.parent_tbx.config.active_project = self.par.active_project.value
        self.parent_tbx.config.write()
        self.add_output_new_project()