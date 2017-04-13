from fgdb_reader import Read_FGDB
import numpy as np

database = r'c:\projektcheck\3 Benutzerdefinierte Projekte\test_mean2' + \
    '\FGDB_Definition_Projekt.gdb'
table = 'Teilflaechen_Plangebiet'
columns = np.array(['Nutzungsart', 'Flaeche_ha', 'Shape_Length', 'Shape_Area'])
Results = Read_FGDB(database, table, columns)
Results.get_result_block()

def calc_weighted_mean(Data, Nutzungsart=None):
    """
    """
    Data = Data.astype(np.float)
    if Nutzungsart is not None:
        Data = Data[Data[:, 0] == Nutzungsart]
    return Data

print(calc_weighted_mean(Results.result_block, Nutzungsart=0))