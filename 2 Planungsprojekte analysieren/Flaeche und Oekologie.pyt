# -*- coding: utf-8 -*-
# reload

from rpctools.analyst.flaeche_oekologie import tbx_Bodenbedeckung_bewerten
reload(tbx_Bodenbedeckung_bewerten)
from rpctools.analyst.flaeche_oekologie import tbx_Bodenbedeckung_kontrollieren
reload(tbx_Bodenbedeckung_kontrollieren)

from rpctools.analyst.flaeche_oekologie import tbx_Integrationsgrad
reload(tbx_Integrationsgrad)

from rpctools.analyst.flaeche_oekologie import tbx_Ueberschneidungen
reload(tbx_Ueberschneidungen)
from rpctools.analyst.flaeche_oekologie import tbx_Schutzgebiete
reload(tbx_Schutzgebiete)

from rpctools.analyst.flaeche_oekologie import tbx_wohnflaechendichte
reload(tbx_wohnflaechendichte)
from rpctools.analyst.flaeche_oekologie import tbx_wohndichte
reload(tbx_wohndichte)

from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_bewerten import TbxBodenBewertung
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenKontrolle
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenEntfernen_Nullfall
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenEntfernen_Planfall
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenAnzeigen_Nullfall
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenAnzeigen_Planfall
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxZeichnung_Nullfall
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxZeichnung_Planfall

from rpctools.analyst.flaeche_oekologie.tbx_Integrationsgrad import TbxIntegrationsgrad
from rpctools.analyst.flaeche_oekologie.tbx_Integrationsgrad import TbxIntegrationsgrad_loeschen

from rpctools.analyst.flaeche_oekologie.tbx_wohnflaechendichte import TbxWohnflaechendichte
from rpctools.analyst.flaeche_oekologie.tbx_wohndichte import TbxWohndichte

from rpctools.analyst.flaeche_oekologie.tbx_Schutzgebiete import TbxSchutzgebiete
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerWald
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerNatur
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerLandschaft
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerFreiraum_100
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerFreiraum_50
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerFreiraum
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerWald_50
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerHochspannung


class Toolbox(object):
    def __init__(self):
        self.label = u'flaeche_oekologie'
        self.alias = ''
        self.tools = [TbxBodenKontrolle,
                      TbxBodenBewertung,
                      TbxBodenEntfernen_Nullfall,
                      TbxBodenEntfernen_Planfall,
                      TbxBodenAnzeigen_Nullfall,
                      TbxBodenAnzeigen_Planfall,
                      TbxZeichnung_Nullfall,
                      TbxZeichnung_Planfall,

					  TbxIntegrationsgrad,
                      TbxIntegrationsgrad_loeschen,

					  TbxWohnflaechendichte,
                      TbxWohndichte,

                      TbxLayerWald,
                      TbxLayerNatur,
                      TbxLayerLandschaft,
                      TbxSchutzgebiete,
                      TbxLayerFreiraum_100,
                      TbxLayerFreiraum_50,
                      TbxLayerFreiraum,
                      TbxLayerWald_50,
                      TbxLayerHochspannung
                      ]




