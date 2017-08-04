# -*- coding: utf-8 -*-
from rpctools.addins.common import FileButton

__all__ = ['HilfeGesamt', 'HilfeVerwaltung', 'HilfeNutzungen',
           'HilfeBewohnerArbeitsplaetze', 'HilfeInfrastruktur',
           'HilfeEinnahmen', 'HilfeVerkehr', 'HilfeStandortkonkurrenz',
           'HilfeFlaeche', 'HilfeOekologie', 'HilfeErreichbarkeit',
           'HinweiseBilanzen']


class HilfeGesamt(FileButton):
    _file = 'ProjektCheck_Anleitung_Gesamtueberblick.pdf'


class HilfeVerwaltung(FileButton):
    _file = 'ProjektCheck_Anleitung_Projekte_verwalten.pdf'


class HilfeNutzungen(FileButton):
    _file = 'ProjektCheck_Anleitung_Projekt_definieren.pdf'


class HilfeBewohnerArbeitsplaetze(FileButton):
    _file = u'ProjektCheck_Anleitung_Bewohner_und_Arbeitsplätze.pdf'


class HilfeInfrastruktur(FileButton):
    _file = 'ProjektCheck_Anleitung_Infrastrukturfolgekosten.pdf'


class HilfeEinnahmen(FileButton):
    _file = 'ProjektCheck_Anleitung_Kommunale_Steuereinnahmen.pdf'


class HilfeVerkehr(FileButton):
    _file = 'ProjektCheck_Anleitung_Verkehr_im_Umfeld.pdf'


class HilfeStandortkonkurrenz(FileButton):
    _file = 'ProjektCheck_Anleitung_Standortkonkurrenz_Supermaerkte.pdf'    


class HilfeFlaeche(FileButton):
    _file = 'ProjektCheck_Anleitung_Flaecheninanspruchnahme.pdf'


class HilfeOekologie(FileButton):
    _file = 'ProjektCheck_Anleitung_Oekologie.pdf'


class HilfeErreichbarkeit(FileButton):
    _file = 'ProjektCheck_Anleitung_Erreichbarkeit.pdf'


class HinweiseBilanzen(FileButton):
    _file = 'ProjektCheck_Hinweise_zur_Ergebnisinterpretation_Kommunale_Einnahmen.pdf'

