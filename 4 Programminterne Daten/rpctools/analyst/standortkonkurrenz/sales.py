from rpctools.utils.config import Folders, Config
from rpctools.utils.spatial_lib import clip_raster
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point

import arcpy
import os

class Sales(object):
    def __init__(self, df_distances, df_markets, df_communities):

        self.distances = df_distances
        self.communities = df_communities
        self.markets = df_markets






