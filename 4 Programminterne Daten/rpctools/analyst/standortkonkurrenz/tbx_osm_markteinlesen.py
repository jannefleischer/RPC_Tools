# -*- coding: utf-8 -*-
import os
import sys
import arcpy
import shutil

from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
from rpctools.analyst.standortkonkurrenz.osm_einlesen import (OSMShopsReader,
                                                              Point)


class OSMMarktEinlesen(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'


    def add_output(self):
        group_layer = ("standortkonkurrenz")
        fc = self.folders.get_table('Maerkte')
        layer = self.folders.get_layer('Märkte Nullfall')
        self.output.add_output(group_layer, layer, fc, zoom=False)
        
        fc = self.folders.get_table('Maerkte')
        layer = self.folders.get_layer('Märkte Planfall')
        self.output.add_output(group_layer, layer, fc, zoom=False)    


    def add_markets(self, supermarkets):
        """Create the point-features for supermarkets"""
        tablename = 'Maerkte'
        sr = arcpy.SpatialReference(self.parent_tbx.config.epsg)
        columns = ['name', 'id_betriebstyp_nullfall', 'id_betriebstyp_planfall',
                   'SHAPE@']
        table = self.folders.get_table(tablename)
        arcpy.TruncateTable_management(table)
        with arcpy.da.InsertCursor(table, columns) as rows:
            for markt in supermarkets:
                markt.create_geom()
                if markt.geom:
                    rows.insertRow((markt.name, 1, 1, markt.geom))
    
    def run(self):
        tbx = self.parent_tbx
        flaechen_df = tbx.table_to_dataframe(
            'Teilflaechen_Plangebiet',
            columns=['INSIDE_X', 'INSIDE_Y'], 
            workspace='FGDB_Definition_Projekt.gdb')
        x = flaechen_df['INSIDE_X'].mean()
        y = flaechen_df['INSIDE_Y'].mean()
        epsg = tbx.config.epsg
        centroid = Point(x, y, epsg=epsg)
        arcpy.AddMessage('Sende Standortanfrage an Geoserver...')
        reader = OSMShopsReader(epsg=epsg)
        markets = reader.get_shops(centroid, distance=self.par.radius.value,
                                   count=self.par.count.value)
        arcpy.AddMessage(u'{} Märkte gefunden'.format(len(markets)))
        arcpy.AddMessage(u'Supermärkte werden in die Datenbank übertragen...'
                         .format(len(markets)))
        self.add_markets(markets)
        self.add_output()


class TbxOSMMarktEinlesen(Tbx):

    @property
    def label(self):
        return encode(u'Marktstandorte online aus OpenStreetMap abfragen')

    @property
    def Tool(self):
        return OSMMarktEinlesen

    def _getParameterInfo(self):

        params = self.par

        # Projekt_auswählen
        param = self.add_parameter('projectname')
        param.name = encode(u'Projekt_auswählen')
        param.displayName = encode(u'Projekt auswählen')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPString'
        param.filter.list = []
    
        param = self.add_parameter('radius')
        param.name = encode(u'Radius')
        param.displayName = encode(u'maximale Entfernung der '
                                   u'Märkte vom Plangebiet in Metern')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [0, 20000]
        param.value = 5000
        
        param = self.add_parameter('count')
        param.name = encode(u'Anzahl')
        param.displayName = encode(u'maximale Anzahl an '
                                   u'hinzuzufügenden Märkten')
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'GPLong'
        param.filter.type = 'Range'
        param.filter.list = [0, 5000]
        param.value = 1000
        
        return params

    def _updateParameters(self, params):   

        return params


if __name__ == '__main__':
    t = TbxOSMMarktEinlesen()
    t._getParameterInfo()
    t.set_active_project()
    t.execute()
