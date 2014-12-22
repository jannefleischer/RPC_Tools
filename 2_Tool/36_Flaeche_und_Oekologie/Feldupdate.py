#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AchimTack
#
# Created:     15.10.2014
# Copyright:   (c) AchimTack 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


import arcpy, sys, os

subdirectories = os.listdir(r"C:\Achim\Dropbox\02_Geschaeftliches\02 GGR\RPC-Entwicklungsumgebung\00_Entwicklungsumgebung\3_Projekte")

for dir in subdirectories:

    mainPath = str(sys.path[0]).split("2_Tool")[0]

    projectName = dir

    gdbPfad = os.path.join(mainPath,'3_Projekte',projectName,'FGDB_11_Definition_Projekt_'+projectName+'.gdb')

    teilfaechen_plangebiet = os.path.join(gdbPfad,"Teilflaechen_Plangebiet")

    try:
        arcpy.AddField_management(teilfaechen_plangebiet,"umfang_meter","FLOAT")
        arcpy.CalculateField_management(teilfaechen_plangebiet,"umfang_meter","!shape.length@METER!","PYTHON_9.3")

    except Exception as e:
        print e