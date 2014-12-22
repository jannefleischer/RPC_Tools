__author__ = 'rieffel'
import arcpy

table = r'C:\Users\rieffel\Dropbox\RPC\00_Entwicklungsumgebung\2_Tool\22_Bevoelkerungsmodellierung\FGDB_22_Bevoelkerungsmodellierung_Tool.gdb\template'

x = 0
while x <= 74:
    if x < 10:
        feldname = "alt00"+str(x)
    else:
        feldname = "alt0" + str(x)
    arcpy.AddField_management(table,feldname,"DOUBLE")
    print feldname
    x += 1