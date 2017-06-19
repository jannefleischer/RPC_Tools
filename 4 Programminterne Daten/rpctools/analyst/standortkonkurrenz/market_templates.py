# -*- coding: utf-8 -*-
from csv import DictWriter, DictReader
import subprocess
import os
import sys
import xlwt
import arcpy
from collections import OrderedDict
import pandas as pd
import numpy as np

from rpctools.utils.spatial_lib import google_geocode
from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point, Supermarket


class MarketTemplate(object):
    '''
    class for managing templates holding markets as inputs for the Tool
    'Standortkonkurrenz'    
    
    Parameters
    ----------
        template_type : str,
            type of file to use as template
            (for options see keys of class variable 'template_types')
        path : str,
            the path to write to and read the templates from
        filename : str, optional (defaults to 'maerkte_template.<extension>')
            name of the file
        epsg : int, optional (defaults to 4326)
            the projection (required to write shapefiles)
    '''
    
    template_types = {
        'CSV-Datei': '.csv',
        'Exceldatei': '.xls',
        'Shapefile': '.shp'
     }
    
    _required_fields = OrderedDict({
        u'Name' : str,
        u'Kette': str,
        u'Ort': str,
        u'PLZ': int,
        u'Straße': int,
        u'Hausnummer': int
    })
    _option_1 = {u'Vkfl_m²': int}
    _option_2 = {u'BTyp': int}

    _default_name = 'maerkte_template'
    
    _delimiter = ';'
    
    def __init__(self, template_type, path, filename=None, epsg=4326):
        self.path = path
        self.template_type = template_type
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        if template_type not in self.template_types.keys():
            raise Exception('unknown type of template')
        
        if not filename:
            filename = '{name}{ext}'.format(
                name=self._default_name,
                ext=self.template_types[template_type]
            )
        self.file_path = os.path.join(self.path, filename)
        
        self.epsg = epsg
        self.sr = arcpy.SpatialReference(epsg)
            
        self.fields = self._required_fields.copy()
        self.fields.update(self._option_1)
    
    def create(self):
        '''create the template file, overwrites if already exists'''

        if self.template_type == 'CSV-Datei':
            self._create_csv_template(self.file_path, self.fields.keys(),
                                      self._delimiter)
        
        elif self.template_type == 'Exceldatei':
            self._create_excel_template(self.file_path, self.fields.keys())

        elif self.template_type == 'Shapefile':
            self._create_shape_template(self.file_path, self.fields,
                                        spatial_reference=self.sr)
            
    def open(self):
        '''open the file (externally with default app if not a shape file)'''
        if self.template_type in ['CSV-Datei', 'Exceldatei']:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', self.file_path))
            elif os.name == 'nt':
                os.startfile(self.file_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', self.file_path))
        elif self.template_type == 'Shapefile':
            layer = arcpy.mapping.Layer(self.file_path)
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
            arcpy.mapping.AddLayer(df, layer, "TOP")

    @staticmethod
    def _create_csv_template(file_path, fields, delimiter=';'):
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, mode='w+') as csv_file:
            csv_file.write(u'\ufeff'.encode('utf8'))
            writer = DictWriter(csv_file,
                                [f.encode('utf8') for f in fields],
                                delimiter=delimiter)
            writer.writeheader()
            
    @staticmethod
    def _create_excel_template(file_path, fields):
        if os.path.exists(file_path):
            os.remove(file_path)
        book = xlwt.Workbook()
        sheet = book.add_sheet(u'Bestandsmärkte')
        for i, field in enumerate(fields):
            sheet.write(0, i, field)
        book.save(file_path)
    
    @staticmethod
    def _create_shape_template(file_path, fields, spatial_reference):
        if arcpy.Exists(file_path):
            arcpy.Delete_management(file_path)
        out_path, out_name = os.path.split(os.path.splitext(file_path)[0])
        arcpy.CreateFeatureclass_management(out_path, out_name,
                                            geometry_type='POINT',
                                            spatial_reference=spatial_reference)
        for field, dtype in fields.iteritems():
            field_type = 'LONG' if dtype == int else 'TEXT'
            arcpy.AddField_management(file_path, field, field_type)
            
    def get_markets(self):
        if self.template_type == 'CSV-Datei':
            df = pd.DataFrame.from_csv(self.file_path, sep=self._delimiter,
                                       encoding='latin1')
            df[df.index.name] = df.index
        required = self._required_fields.keys()
        if np.in1d(required, df.columns).sum() < len(required):
            raise LookupError('missing fields in given file')
        markets = self._df_to_markets(df)
        return markets
    
    def _df_to_markets(self, df):
        markets = []
        for i, (idx, row) in enumerate(df.iterrows()):
            address = '{postcode} {city} {street} {number}'.format(
                postcode=row['PLZ'],
                city=row['Ort'], 
                street=row[u'Straße'], 
                number=row['Hausnummer']
            )
            lat, lon = google_geocode(address)
            market = Supermarket(i, lon, lat,
                                 row['Name'], row['Kette'],
                                 epsg=4326)
            market = market.transform(self.epsg)
            markets.append(market)
        return markets
        