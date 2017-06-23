# -*- coding: utf-8 -*-
import arcpy

from rpctools.utils.params import Tbx, Tool, Folders
from rpctools.utils.encoding import encode
import numpy as np
import pandas as pd
import time


class KostenkennwerteKontrollieren(Tool):

    def add_outputs(self):
        pass

    def run(self):
        self.kostenkennwerte()
        pass

    def kostenkennwerte(self):
        tbx = self.parent_tbx
        current_year = int(time.strftime("%Y"))
        frame_data = tbx.table_to_dataframe('Rahmendaten',
                                            workspace='FGDB_Kosten_Tool',
                                            is_base_table=True)
        time_factor = (1 + interest) * np.exp(current_year - reference_year)

        return time_factor


class TbxKostenkennwerteKontrollieren(Tbx):

    @property
    def label(self):
        return encode(u'Kostenkennwerte kontrollieren')

    @property
    def Tool(self):
        return KostenkennwerteKontrollieren

    def _open(self, params):
        pass

    def _updateParameters(self, params):
        pass

    def _getParameterInfo(self):
        pass


if __name__ == '__main__':
    t = TbxKostenkennwerteKontrollieren()
    t._getParameterInfo()
    t.set_active_project()
    t._updateParameters(None)
    t.execute()
