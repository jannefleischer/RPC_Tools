import arcpy
from arcpy import env
import numpy as np


#gdb_path = r"C:\ProjektCheck\3 Benutzerdefinierte Projekte" + \
#"\Wir_wollen_Diagramme\FGDB_Definition_Projekt.gdb"
#test_data = 'Wohnen_WE_in_Gebaeudetypen'
#columns = np.array(["WE", "EW_je_WE"])

class Read_FGDB(object):
    
    
    def __init__(self, gdb_path, table, columns, clause=None):
        self.gdb_path = gdb_path
        self.table = table
        self.columns = columns
        self.clause = clause
        self.result_block = []
        
        
    def get_result_block(self):
        """
        Extract data from gdb.
        
        Parameters
        ----------
        gdb_path : str
            Path to GDB
        table : str
            Table inside the GDB
        columns : np.array of str
            Columns inside the table
        
        Returns
        -------
        result_block : np.array of str
            Extracted data from GDB
        """
        env.workspace = self.gdb_path
        result_block = self.columns
        with arcpy.da.SearchCursor(self.table, self.columns, 
                                   where_clause=self.clause) as cur:
            for cols in cur:
                new_row = np.array(cols)
                result_block = np.vstack((result_block, new_row))
        
        self.result_block = result_block


    def sort_results_by_col(self, col, header=1):
        """
        """
        self.result_block[header:, :] = self.result_block[header:, :]\
            [self.result_block[header:, col].argsort()]



if __name__ == '__main__':
    filename = 'demo.xlsx'
    filename2 = r'C:\ProjektCheck\test_excel\demo.xlsx'
    gdb_path = r"C:\ProjektCheck\3 Benutzerdefinierte Projekte" + \
    "\Wir_wollen_Diagramme\FGDB_Definition_Projekt.gdb"
    test_data = 'Wohnen_WE_in_Gebaeudetypen'
    columns = np.array(["WE", "EW_je_WE"])
    
    Results = Read_FGDB(gdb_path, test_data, columns, 'WE>0 and WE<20')
    Results.get_result_block()
    Results.sort_results_by_col(1)
    cell_block = Results.result_block    