# -*- coding: utf-8 -*-

from rpctools.analyst.bewohner_arbeitsplaetze import tbx_bewohner
reload(tbx_bewohner)

from rpctools.analyst.bewohner_arbeitsplaetze.tbx_bewohner import TbxBewohner


class Toolbox(object):
    def __init__(self):
        self.label = u'Bewohner und Arbeitsplätze'
        self.alias = ''
        self.tools = [TbxBewohner]
