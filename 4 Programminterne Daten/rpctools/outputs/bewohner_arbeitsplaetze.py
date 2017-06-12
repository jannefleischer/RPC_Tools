# -*- coding: utf-8 -*-

from rpctools.utils.output import Output
from rpctools.diagrams.bewohner_arbeitsplaetze import (ArbeitsplatzEntwicklung,
                                                       BewohnerEntwicklung,
                                                       BranchenAnteile)


class BewohnerOutput(Output):

    def define_outputs(self):
        self.add_diagram(BewohnerEntwicklung)


class ArbeitsplaetzeOutput(Output):

    def define_outputs(self):
        self.add_diagram(ArbeitsplatzEntwicklung, BranchenAnteile)
