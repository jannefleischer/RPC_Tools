from fgdb_reader import Read_FGDB

database = 'C:\ProjektCheck\3 Benutzerdefinierte Projekte\test123' + \
'\FGDB_Definition_Projekt.gdb'
table = '\Teilflaechen_Plangebiet'
columns = np.array(['Flaeche_ha', 'INSIDE_X', 'INSIDE_Y'])
Results = Read_FGDB(gdb_path, test_data, columns, 'WE>0 and WE<20')