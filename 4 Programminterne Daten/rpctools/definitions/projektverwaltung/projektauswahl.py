from rpctools.utils.params import Tool


class Projektauswahl(Tool):

    def run(self):
        self.parent_tbx.config.active_project = self.par.active_project.value
        self.parent_tbx.config.write()