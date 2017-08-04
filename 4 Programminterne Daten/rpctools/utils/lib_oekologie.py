import arcpy
import math
import rpctools.utils.config as config
import os

def create_bodenbedeckung(projekt):

    folders = config.Folders()
    workspace_projekt_oekologie = folders.get_db('FGDB_Flaeche_und_Oekologie.gdb', projekt)
    path_bodenbedeckung = folders.get_table('Bodenbedeckung_Anteile', "FGDB_Flaeche_und_Oekologie.gdb", projekt)
    path_bodenbedeckung_tool = folders.get_base_table("FGDB_Flaeche_und_Oekologie_Tool.gdb", 'Bodenbedeckung_Anteile',  projekt)

    anteile_alt = create_bodenanteile(0, projekt)
    anteile_neu = create_bodenanteile(1, projekt)


    fields = ["IDBodenbedeckung", "Planfall", "Bodenbedeckung_Anteil"]
    cursor = arcpy.da.UpdateCursor(path_bodenbedeckung, fields)
    for row in cursor:
        if row[1] == 0 and row[0] == 1:
             row[2] = anteile_alt[0]
        elif row[1] == 0 and row[0] == 2:
             row[2] = anteile_alt[1]
        elif row[1] == 0 and row[0] == 3:
             row[2] = anteile_alt[2]
        elif row[1] == 0 and row[0] == 4:
             row[2] = anteile_alt[3]
        elif row[1] == 0 and row[0] == 5:
             row[2] = anteile_alt[4]
        elif row[1] == 0 and row[0] == 6:
             row[2] = anteile_alt[5]
        elif row[1] == 0 and row[0] == 7:
             row[2] = anteile_alt[6]
        elif row[1] == 0 and row[0] == 8:
             row[2] = anteile_alt[7]
        elif row[1] == 0 and row[0] == 9:
             row[2] = anteile_alt[8]
        elif row[1] == 0 and row[0] == 10:
             row[2] = anteile_alt[9]
        elif row[1] == 0 and row[0] == 11:
             row[2] = anteile_alt[10]
        elif row[1] == 1 and row[0] == 1:
             row[2] = anteile_neu[0]
        elif row[1] == 1 and row[0] == 2:
             row[2] = anteile_neu[1]
        elif row[1] == 1 and row[0] == 3:
             row[2] = anteile_neu[2]
        elif row[1] == 1 and row[0] == 4:
             row[2] = anteile_neu[3]
        elif row[1] == 1 and row[0] == 5:
             row[2] = anteile_neu[4]
        elif row[1] == 1 and row[0] == 6:
             row[2] = anteile_neu[5]
        elif row[1] == 1 and row[0] == 7:
             row[2] = anteile_neu[6]
        elif row[1] == 1 and row[0] == 8:
             row[2] = anteile_neu[7]
        elif row[1] == 1 and row[0] == 9:
             row[2] = anteile_neu[8]
        elif row[1] == 1 and row[0] == 10:
             row[2] = anteile_neu[9]
        elif row[1] == 1 and row[0] == 11:
             row[2] = anteile_neu[10]
        cursor.updateRow(row)

def import_zeichenanteile(projekt):

    folders = config.Folders()
    workspace_projekt_definition = folders.get_db('FGDB_Definition_Projekt.gdb', projekt)
    path_teilflaechen = folders.get_table('Teilflaechen_Plangebiet', "FGDB_Definition_Projekt.gdb", projekt)
    workspace_projekt_oekologie = folders.get_db('FGDB_Flaeche_und_Oekologie.gdb', projekt)
    path_nullfall = folders.get_table('Bodenbedeckung_Nullfall', "FGDB_Flaeche_und_Oekologie.gdb", projekt)
    path_planfall = folders.get_table('Bodenbedeckung_Planfall', "FGDB_Flaeche_und_Oekologie.gdb", projekt)



    boden_absolut = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    boden_anteil = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    gesamtflaeche = 0
    pointer = 0

    fields = ["SHAPE_Area", "IDBodenbedeckung"]
    cursor = arcpy.da.SearchCursor(path_nullfall, fields)
    for row in cursor:
        gesamtflaeche += row[0]
        pointer = row[1] - 1
        boden_absolut[pointer] += row[0]
    else:
        boden_anteil[0] = 100
        return boden_anteil

    for x in xrange(11):
        boden_anteil[x] = boden_absolut[x] / gesamtflaeche
        boden_anteil[x] = math.floor(boden_anteil[x])

    summe = sum(boden_anteil)
    differenz = 100 - summe
    if differenz > 0:
        boden_anteil[0] += differenz

    return boden_anteil