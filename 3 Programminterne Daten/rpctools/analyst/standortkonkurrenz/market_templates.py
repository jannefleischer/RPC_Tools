# -*- coding: utf-8 -*-
from csv import DictWriter, DictReader
import subprocess
import os
import sys
import xlsxwriter
import xlrd
import arcpy
from collections import OrderedDict
import pandas as pd
import numpy as np
import string

from rpctools.utils.spatial_lib import google_geocode
from rpctools.utils.config import Config

from rpctools.analyst.standortkonkurrenz.osm_einlesen import Point, Supermarket

config = Config()

DEFAULT_NAME = 'maerkte_vorlage'

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
        filename : str, optional (defaults to 'maerkte_vorlage.<extension>')
            name of the file
        epsg : int, optional (defaults to 4326)
            the projection (required to write shapefiles)
    '''

    template_types = {
        'CSV-Datei': ('.csv', 'ProjektCheck_Anleitung_WB7_Erfassungsvorlage_Maerkte_CSVDatei_befuellen.pdf'),
        'Exceldatei': ('.xlsx', 'ProjektCheck_Anleitung_WB7_Erfassungsvorlage_Maerkte_Exceldatei_befuellen.pdf'),
        'Shapefile': ('.shp', 'ProjektCheck_Anleitung_WB7_Erfassungsvorlage_Maerkte_ShapeFile_befuellen.pdf')
     }

    _required_fields = OrderedDict([
        (u'Name', str),
        (u'Kette', str)
    ])

    _address_fields = OrderedDict([
        (u'Ort', str),
        (u'PLZ', str),
        (u'Straße', str),
        (u'Hausnummer', int)
    ])

    _option_1 = {u'Vkfl_m²': int}
    _option_2 = {u'BTyp': int}

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
                name=DEFAULT_NAME,
                ext=self.template_types[template_type][0]
            )
        self.file_path = os.path.join(self.path, filename)

        self.epsg = epsg
        self.sr = arcpy.SpatialReference(epsg)

        self.fields = self._required_fields.copy()
        if self.template_type in ['CSV-Datei', 'Exceldatei']:
            self.fields.update(self._address_fields)
        self.fields.update(self._option_1)

    def create(self):
        '''create the template file, overwrites if already exists'''

        if self.template_type == 'CSV-Datei':
            self._create_csv_template(self.file_path, self.fields.keys(),
                                      self._delimiter)

        elif self.template_type == 'Exceldatei':
            self._create_excel_template(self.file_path, self.fields)

        elif self.template_type == 'Shapefile':
            self._create_shape_template(self.file_path, self.fields,
                                        spatial_reference=self.sr)

    def open(self):
        '''open the file (externally with default app if not a shape file)'''
        if self.template_type == 'Exceldatei':
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', self.file_path))
            elif os.name == 'nt':
                os.startfile(self.file_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', self.file_path))
        elif self.template_type == 'CSV-Datei':
            subprocess.Popen(r'explorer /select,"{}"'
                             .format(self.file_path))
        elif self.template_type == 'Shapefile':
            layer = arcpy.mapping.Layer(self.file_path)
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
            arcpy.mapping.AddLayer(df, layer, "TOP")
            del(mxd)
            del(df)

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
        book = xlsxwriter.Workbook(file_path)
        sheet = book.add_worksheet()
        alphabet = string.ascii_uppercase
        for i, (field, dtype) in enumerate(fields.iteritems()):
            form = book.add_format()
            if dtype == str:
                form.set_num_format('@')
            sheet.set_column('{l}:{l}'.format(l=alphabet[i]), 50, form)
            sheet.write(0, i, field)
        book.close()

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
        arcpy.DeleteField_management(file_path, 'Id')

    def get_markets(self):
        '''read and return the markets from file'''
        if self.template_type == 'CSV-Datei':
            df = None
            for encoding in ['utf-8-sig', 'ISO-8859-1']:
                try:
                    df = pd.DataFrame.from_csv(self.file_path, sep=self._delimiter,
                                               encoding=encoding)
                    break
                except:
                    continue
            if df is None:
                raise Exception(u'Es gibt ein Problem mit der '
                                u'Zeichenkodierung der CSV-Datei!')
            df = df.reset_index()
        elif self.template_type == 'Exceldatei':
            df = pd.read_excel(self.file_path)
        elif self.template_type == 'Shapefile':
            columns = [f.name for f in arcpy.ListFields(self.file_path)]
            cursor = arcpy.da.SearchCursor(self.file_path, columns)
            rows = [row for row in cursor]
            del cursor
            df = pd.DataFrame.from_records(rows, columns=columns)
        else:
            raise Exception('unknown type of template')
        required = self._required_fields.keys()
        if self.template_type in ['CSV-Datei', 'Exceldatei']:
            required += self._address_fields.keys()
        if np.in1d(required, df.columns).sum() < len(required):
            raise LookupError('missing fields in given file')
        markets = self._df_to_markets(df)
        return markets

    def _df_to_markets(self, df):
        markets = []
        api_key = config.google_api_key
        for i, (idx, row) in enumerate(df.iterrows()):
            address = ''
            name, kette, vkfl = row['Name'], row['Kette'], row[u'Vkfl_m²']
            if self.template_type in ['CSV-Datei', 'Exceldatei']:
                for field in self._address_fields.keys():
                    address += u' {}'.format(row[field])
                arcpy.AddMessage(u'Geocoding {name} {address}...'.format(
                    name=name, address=address))
                location, msg = google_geocode(address, api_key=api_key)
                if location is None:
                    arcpy.AddMessage(u'Fehler: {msg}'.format(msg=msg))
                    continue
                lat, lon = location
                market = Supermarket(i, lon, lat, name, kette, vkfl=vkfl,
                                     adresse=address, epsg=4326)
                market.transform(self.epsg)
            else:
                x, y = row['Shape']
                market = Supermarket(i, x, y, name, kette, vkfl=vkfl,
                                     epsg=self.epsg)
            markets.append(market)
        return markets
