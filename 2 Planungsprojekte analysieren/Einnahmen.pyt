# -*- coding: utf-8 -*-

from rpctools.analyst.einnahmen import (tbx_wanderungssalden_schaetzen_Einwohner,
                                        tbx_wanderungssalden_bearbeiten,
                                       tbx_wanderungssalden_schaetzen_Arbeit,
                                        tbx_Einkommensteuer,
##                                        tbx_Ergebnisinterpretation,
                                        tbx_Familienleistungsausgleich,
##                                        tbx_Gesamtsumme,
                                       tbx_Gewerbesteuer_kontrollieren,
##                                        tbx_Gewerbesteuer_schaetzen,
                                          tbx_grundsteuer
##                                        tbx_Umsatzsteuer
)



reload(tbx_wanderungssalden_schaetzen_Einwohner)
reload(tbx_wanderungssalden_bearbeiten)
reload(tbx_wanderungssalden_schaetzen_Arbeit)
reload(tbx_Einkommensteuer)
##reload(tbx_Ergebnisinterpretation)
reload(tbx_Familienleistungsausgleich)
##reload(tbx_Gesamtsumme)
reload(tbx_Gewerbesteuer_kontrollieren)
##reload(tbx_Gewerbesteuer_schaetzen)
reload(tbx_grundsteuer)
##reload(tbx_Umsatzsteuer)

from rpctools.analyst.einnahmen.tbx_wanderungssalden_schaetzen_Einwohner import TbxWanderungssalden1
from rpctools.analyst.einnahmen.tbx_wanderungssalden_schaetzen_Arbeit import TbxWanderungssalden2
from rpctools.analyst.einnahmen.tbx_wanderungssalden_bearbeiten import TbxEWSaldenbearbeiten
from rpctools.analyst.einnahmen.tbx_wanderungssalden_bearbeiten import TbxGewSaldenbearbeiten
from rpctools.analyst.einnahmen.tbx_grundsteuer import TbxGrundsteuer
from rpctools.analyst.einnahmen.tbx_Einkommensteuer import TbxEinkommensteuer
from rpctools.analyst.einnahmen.tbx_Familienleistungsausgleich import TbxFLA
from rpctools.analyst.einnahmen.tbx_Gewerbesteuer_kontrollieren import TbxKontrolleGewerbesteuer
class Toolbox(object):
    def __init__(self):
        self.label = u'Einnahmen'
        self.alias = ''
        self.tools = [
                    TbxWanderungssalden1,
                    TbxWanderungssalden2,
                    TbxEWSaldenbearbeiten,
                    TbxGewSaldenbearbeiten,
                    TbxGrundsteuer,
                    TbxEinkommensteuer,
                    TbxFLA,
                    TbxKontrolleGewerbesteuer
        ]
