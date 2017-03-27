# -*- coding: utf-8 -*-
# reload
from rpctools.analyst.flaeche_oekologie import tbx_Vornutzungbeschreiben
reload(tbx_Vornutzungbeschreiben)
from rpctools.analyst.flaeche_oekologie import tbx_BodenbedeckungPlanfall
reload(tbx_BodenbedeckungPlanfall)
from rpctools.analyst.flaeche_oekologie import tbx_wohnflaechendichte
reload(tbx_wohnflaechendichte)
from rpctools.analyst.flaeche_oekologie import tbx_Ueberschneidung
reload(tbx_Ueberschneidung)
from rpctools.analyst.flaeche_oekologie import tbx_OekologischeFolgen
reload(tbx_OekologischeFolgen)


from rpctools.analyst.flaeche_oekologie.tbx_Vornutzungbeschreiben import TbxVornutzungbeschreiben
from rpctools.analyst.flaeche_oekologie.tbx_BodenbedeckungPlanfall import TbxBodenbedeckungPlanfall
from rpctools.analyst.flaeche_oekologie.tbx_wohnflaechendichte import Tbxwohnflaechendichte
from rpctools.analyst.flaeche_oekologie.tbx_Ueberschneidung import TbxUeberschneidung
from rpctools.analyst.flaeche_oekologie.tbx_OekologischeFolgen import TbxOekologischeFolgen

class Toolbox(object):
    def __init__(self):
        self.label = u'flaeche_oekologie'
        self.alias = ''
        self.tools = [TbxVornutzungbeschreiben,
                      TbxBodenbedeckungPlanfall,
					  Tbxwohnflaechendichte,
					  TbxUeberschneidung,
					  TbxOekologischeFolgen]




