from fgdb_reader import Read_FGDB
import numpy as np


def calc_weighted_mean(Data, Nutzungsart=None):
    """
    Calculates the weighted mean coordinates for areas with the same
    'Nutzungsart'
    
    Parameters
    ----------
    Data : np.array of str
        Input data. Columns: Nutzungsart, Flaeche_ha, INSIDE_X, INSIDE_Y
    Nutzungsart : int, optional
        Only areas of the given 'Nutzungsart' will be considered
    """
    Data = Data.astype(np.float)
    if Nutzungsart is not None:
        Data = Data[Data[:, 0] == Nutzungsart]
    # multiply X- and Y-column with the relative area sizes
    weighted_XY = np.einsum('ij,i->ij', Data[:, 2:4], Data[:, 1] / 
                                 np.sum(Data[:, 1]))
    
    XY = np.array([np.sum(weighted_XY[:, 0]), np.sum(weighted_XY[:, 1])])
    
    return XY
    




database = r'c:\projektcheck\3 Benutzerdefinierte Projekte\test_mean2' + \
    '\FGDB_Definition_Projekt.gdb'
table = 'Teilflaechen_Plangebiet'
columns = np.array(['Nutzungsart', 'Flaeche_ha', 'INSIDE_X', 'INSIDE_Y'])
Results = Read_FGDB(database, table, columns)
Results.get_result_block()
print(calc_weighted_mean(Results.result_block, Nutzungsart=0))