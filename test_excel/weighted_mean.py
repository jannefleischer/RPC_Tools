from fgdb_reader import Read_FGDB
import numpy as np

database = 'C:\Arbeit\RPC\Github\3 Benutzerdefinierte Projekte\Test\FGDB_Definition_Projekt.gdb'
table = 'Teilflaechen_Plangebiet'
columns = np.array(['Flaeche_ha', 'Shape_Length', 'Shape_Area'])
Results = Read_FGDB(database, table, columns)
Results.get_result_block()

def calc_weighted_mean(Data, Nutzungsart=None):
    """
    """
    if Nutzungsart is not None:
        Data = Data[Data[:, 0] == Nutzungsart]
    return Data

print(calc_weighted_mean(Results.result_block, Nutzungsart=None))