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
from rpctools.analyst.flaeche_oekologie import tbx_UZVR
reload(tbx_UZVR)
from rpctools.analyst.flaeche_oekologie import tbx_wohnflaechendichte
reload(tbx_wohnflaechendichte)


from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_bewerten import TbxBodenBewertung
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenKontrolle
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenEntfernen
from rpctools.analyst.flaeche_oekologie.tbx_Bodenbedeckung_kontrollieren import TbxBodenAnzeigen
from rpctools.analyst.flaeche_oekologie.tbx_Integrationsgrad import TbxIntegrationsgrad
from rpctools.analyst.flaeche_oekologie.tbx_Integrationsgrad import TbxIntegrationsgrad_loeschen
from rpctools.analyst.flaeche_oekologie.tbx_UZVR import TbxUZVR
from rpctools.analyst.flaeche_oekologie.tbx_wohnflaechendichte import TbxWohnflaeche

from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerWald
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerNatur
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerLandschaft
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerWasser
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerFreiraum
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerBodenversiegelung
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidungen import TbxLayerHochspannung

class Toolbox(object):
    def __init__(self):
        self.label = u'flaeche_oekologie'
        self.alias = ''
        self.tools = [TbxBodenKontrolle ,
                      TbxBodenBewertung,
					  TbxIntegrationsgrad,
					  TbxUZVR,
					  TbxWohnflaeche,
                      TbxLayerWald,
                      TbxLayerNatur,
                      TbxLayerLandschaft,
                      TbxLayerWasser,
                      TbxLayerFreiraum,
                      TbxLayerBodenversiegelung,
                      TbxLayerHochspannung,
                      TbxBodenAnzeigen,
                      TbxBodenEntfernen,
                      TbxIntegrationsgrad_loeschen
                      ]




