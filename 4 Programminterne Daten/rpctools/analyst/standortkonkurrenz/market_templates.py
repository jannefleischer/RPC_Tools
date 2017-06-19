# -*- coding: utf-8 -*-
from csv import DictWriter
import subprocess
import os
import sys
import xlwt

class MarketTemplate(object):
    
    template_types = ['CSV-Datei', 'Exceldatei', 'Shapefile']
    required_fields = [u'Name',
                       u'Kette',
                       u'Ort',
                       u'Postleitzahl',
                       u'Straße',
                       u'Hausnummer']
    option_1 = [u'Verkaufsfläche']
    option_2 = [u'Betriebstyp']

    template_name = 'maerkte'
    subfolder = 'input_templates'
    
    def __init__(self, template_type, base_path):
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
        
        else:
            raise Exception('unknown type of template')
            
        self.fields = self.required_fields + self.option_1
    
    def create(self): 

        if self.template_type == 'CSV-Datei':
            self._create_csv_template(self.file_path, self.fields)
        
        elif self.template_type == 'Exceldatei':
            self._create_excel_template(self.file_path, self.fields)
            
    def open(self):
        if self.template_type in ['CSV-Datei', 'Exceldatei']:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', self.file_path))
            elif os.name == 'nt':
                os.startfile(self.file_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', self.file_path))

    @staticmethod
    def _create_csv_template(file_path, fields):
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, mode='w+') as csv_file:
            csv_file.write(u'\ufeff'.encode('utf8'))
            writer = DictWriter(csv_file, [f.encode('utf8') for f in fields],
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