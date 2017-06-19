# -*- coding: utf-8 -*-
from csv import DictWriter
import subprocess
import os
import sys
import xlwt
import arcpy
from collections import OrderedDict

class MarketTemplate(object):
    
    template_types = ['CSV-Datei', 'Exceldatei', 'Shapefile']
    required_fields = OrderedDict({
        u'Name' : str,
        u'Kette': str,
        u'Ort': str,
        u'PLZ': int,
        u'Straße': int,
        u'Hausnummer': int
    })
    option_1 = {u'Vkfl': int}
    option_2 = {u'BTyp': int}

    template_name = 'maerkte_template'
    subfolder = 'input_templates'
    
    def __init__(self, template_type, base_path, epsg=None):
        self.template_folder = os.path.join(base_path, self.subfolder)
        self.template_type = template_type
        
        if not os.path.exists(self.template_folder):
            os.mkdir(self.template_folder)
        
        if self.template_type == 'CSV-Datei':
            fn = self.template_name + '.csv'
            self.file_path = os.path.join(self.template_folder, fn)
        
        elif self.template_type == 'Exceldatei':
            fn = self.template_name + '.xls'
            self.file_path = os.path.join(self.template_folder, fn)
            
        elif self.template_type == 'Shapefile':
            fn = self.template_name + '.shp'
            self.file_path = os.path.join(self.template_folder, fn)
        
        else:
            raise Exception('unknown type of template')
        
        if epsg:
            self.sr = arcpy.SpatialReference(epsg)
            
        self.fields = self.required_fields.copy()
        self.fields.update(self.option_1)
    
    def create(self): 

        if self.template_type == 'CSV-Datei':
            self._create_csv_template(self.file_path, self.fields.keys())
        
        elif self.template_type == 'Exceldatei':
            self._create_excel_template(self.file_path, self.fields.keys())

        elif self.template_type == 'Shapefile':
            self._create_shape_template(self.file_path, self.fields,
                                        spatial_reference=self.sr)
            
    def open(self):
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
    def _create_csv_template(file_path, fields):
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, mode='w+') as csv_file:
            csv_file.write(u'\ufeff'.encode('utf8'))
            writer = DictWriter(csv_file,
                                [f.encode('utf8') for f in fields],
                                delimiter=';')
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
         