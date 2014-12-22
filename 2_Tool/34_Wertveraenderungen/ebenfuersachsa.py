

import arcpy, os,sys

projektname="HCU_ZGB_OTLindenEZH"
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_Basis_Daten = os.path.join(base_path, '2_Tool', '34_Wertveraenderungen','FGDB_34_Wertveraenderungen_Tool.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Wertveraenderungen_' + projektname + '.gdb')

cur_sacha = arcpy.SearchCursor (os.path.join(workspace_projekt,"Siedlungszellen_Linden_Sascha"))
cur_siedlungszellen= arcpy.UpdateCursor(os.path.join(workspace_projekt,"Siedlungszahlendaten"))

array_sacha=[]
for a in cur_sacha:
    array_sacha.append(int(a.Id_1))

for meins in cur_siedlungszellen:
    gefunden=0
    for sascha in array_sacha:
        if (sascha == int( meins.SZ_ID)):
            gefunden=1
            break
    if gefunden==0:
        cur_siedlungszellen.deleteRow(meins)

del cur_sacha,cur_siedlungszellen