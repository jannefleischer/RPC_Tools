# -*- coding: utf-8 -*-

from rpctools.analyst.bewohner_arbeitsplaetze.tbx_bewohner import TbxBewohner
from rpctools.analyst.bewohner_arbeitsplaetze.tbx_arbeitsplaetze import \
     TbxArbeitsplaetze


class Toolbox(object):
    def __init__(self):
        self.label = u'Bewohner und Arbeitsplätze'
        self.alias = ''
        self.tools = [TbxBewohner, TbxArbeitsplaetze]
