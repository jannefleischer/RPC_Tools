import openpyxl
import os
import sys
import time
import win32com.client
from openpyxl.utils import get_column_letter
import numpy as np

# file-names
filename = 'demo.xlsx'
filename2 = r'C:\ProjektCheck\test_excel\demo.xlsx'
input_block = np.diag(np.arange(6))
input_block[0,:] = np.ones(6)


def insert_cell_block(filename, sh_name, upper_left, cell_block):
    """
    Overwrite a cell-block in an Excel-file.
    
    Parameters
    ----------
    filename : str
        Path to the Excel-file
    sh_name : str
        Name of the worksheet where the cells will 
    upper_left : list of int
        Indices of the upper-left cell that will be overwritten.
        Cell A1 equals upper_left = [1, 1].
    cell_block : Matix of str or float or int
        Cell-block that will be copied to the Excel-file.
    
    """
    wb = openpyxl.load_workbook(filename)
    ws1 = wb.active
    ws1.title = "sheet1"
    block_cols, block_rows = np.shape(cell_block)
    start_row = upper_left[0]
    start_col = upper_left[1]
    for row in range(block_rows):
        for col in range(block_cols):
            cell_id = get_column_letter(start_col+col) + str(start_row+row)
            ws1[cell_id] = input_block[row, col]
    wb.save(filename)
    wb.close()

insert_cell_block(filename, [4, 8], input_block)

def append_rows(filename, rows):
    """
    Write and save new lines in .xlsx file.
    
    Parameters
    ----------
    filename : str
        Path to the Excel file
    
    """
    wb = openpyxl.load_workbook(filename)
    ws1 = wb.active
    ws1.title = "range names"
    ws1.append((rows, rows))
    wb.save(filename)
    wb.close()
    
  
def clear_cellblock(filename, upper_left, lower_right):
    """
    clear the all cells between upper_left and lower_right
    """
    wb = openpyxl.load_workbook(filename)
    sh = wb.get_sheet_by_name("range names")
    for row in sh[upper_left+':'+lower_right]:
        for cell in row:
            cell.value = None
    wb.save(filename)
    wb.close()    
    
    
def clear_cellblock_2(filename, upper_left, lower_right):
    """
    delete all rows between first an last
    """
    excel = win32com.client.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = 0
    wb = excel.Workbooks.Open(filename)
    excel.Range(upper_left+':'+lower_right).Select()
    excel.Selection.ClearContents()
    wb.Save()
    wb.Close()
    
    
def delete_rows(filename, first, last):
    """
    All rows from first to last are removed completely
    """
    excel = win32com.client.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = 0
    wb = excel.Workbooks.Open(filename)
    sh = wb.ActiveSheet
    rangeObj = sh.Range('A'+str(first)+':A'+str(last))
    rangeObj.EntireRow.Delete()    
    wb.Save()
    wb.Close() 
    
    
def delete_columns(filename, first, last):
    """
    All columns from first to last are removed completely
    """
    excel = win32com.client.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = 1
    wb = excel.Workbooks.Open(filename)
    sh = wb.ActiveSheet
    rangeObj = sh.Range(first+'1:'+last+'1')
    rangeObj.EntireColumn.Delete()    
    wb.Save()
    wb.Close() 
    
    
def open_file_in_excel(path):
    """
    Open .xlsx file in Excel and wait for 5 seconds to check if saving works
    """
    # open demo.xlsx file in Excel
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = True
    xl.Workbooks.Open(path)

    time.sleep(5)


def check_if_file_is_open(path):
    """
    Check if a file is opened in Excel.
    If file is open: Save and close
    """
    excel = win32com.client.Dispatch("Excel.Application")
    if excel.Workbooks.Count > 0:
        for i in range(1, excel.Workbooks.Count+1):
            #print(excel.Workbooks.Item(i).Name, filename)
            if excel.Workbooks.Item(i).Name == filename:
                wb = excel.Workbooks.Item(i)
                wb.Save()
                wb.Close()
                break    

        
        
        
        

#delete_rows(filename2, 1, 4)




#start = time.time()
#clear_cellblock_2(filename2, 'A1', 'N2000')
#print(time.time() - start)
#time.sleep(3)
#start = time.time()
#clear_cellblock(filename, 'A1', 'N2000')
#print(time.time() - start)
#write_some_lines(filename, "before opening Excel")
#open_file_in_excel(filename2)
#check_if_file_is_open(filename2)
#time.sleep(5)
#write_some_lines(filename, "after opening Excel")

print('done')





"""
MAY BE USEFUL LATER:

try:
    ws1.append(("after opening excel", "after opening excel"))
    wb.save(filename)
except:
    print('file is already opened')
# not used: opens demo.xlsx file
#os.system('start excel.exe "%s\\demo.xlsx"' % (sys.path[0], ))
"""










