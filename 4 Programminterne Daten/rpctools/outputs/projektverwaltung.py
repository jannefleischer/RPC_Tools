# -*- coding: utf-8 -*-

from rpctools.utils.output import Output


class ProjektverwaltungOutput(Output):
    _workspace = 'FGDB_Definition_Projekt.gdb'

    def define_outputs(self):
        # add Teilflächen
        fc = "Teilflaechen_Plangebiet"
        layer = "Teilflächen des Plangebiets"
        self.add_layer("projektdefinition", layer, fc)

        # add OpenStreetmap
        layer = "OpenStreetMap"
        self.add_layer("hintergrundkarten", layer,
                        zoom=False, in_project=False)