# -*- coding: utf-8 -*-
import arcpy
#Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
#damit die vorhandenen Projekte in der DropdownListe angezeigt werden
blabla=[]
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""

    self.params = arcpy.GetParameterInfo()




  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    import os, arcpy

    tbx_path, tool_method = __file__.split('#')
    toolname = tool_method.split('.')[0]

    base_path = os.path.dirname(tbx_path)
    base_path = os.path.dirname(base_path)
    base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

    tablepath_projects = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb','angelegteProjekte')

    try:
        rows_projects = arcpy.SearchCursor(tablepath_projects)
        message = "jep"
    except:
        rows_projects  = []
        message = "nope"

    list_projects =[]

    for row in rows_projects:
    	list_projects.append(row.Name)
    list_projects = list(set(list_projects))
    list_projects = sorted(list_projects)


    list_uebergabepunkte = []
    list_parameter_zent=[]

    i=-1
    i+=1 ;
    #set project
    self.params[i].filter.list = list_projects

    i+=1 ;
    self.params[i].filter.list = list_parameter_zent
    i+=1 ;
    self.params[i].filter.list = list_uebergabepunkte
    i+=1 ;
    self.params[i].filter.list = list_uebergabepunkte
    i+=1 ;
    self.params[i].filter.list = list_uebergabepunkte


    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    import os, arcpy

    tbx_path, tool_method = __file__.split('#')
    toolname = tool_method.split('.')[0]

    base_path = os.path.dirname(tbx_path)
    base_path = os.path.dirname(base_path)
    base_path = os.path.dirname(base_path) # erzeugt Pfad zum Ordner, in dem Script liegt

    i=-1
    i+=1

    list_uebergabepunkte =[]
    list_parameter_zent=[1,2,3,4,5,6,7,8,9,10]
    self.params[6].value = "Zum Speichern bitte das Kästchen anklicken"

    if (self.params[i].altered and not self.params[i].hasBeenValidated or self.params[1].altered and not self.params[1].hasBeenValidated ):

        list_uebergabepunkte=[]
        projectname = self.params[i].value


        tablepath_maerkte = os.path.join(base_path,'3_Projekte',projectname,'FGDB_34_Wertveraenderungen_'+projectname+'.gdb','Standorte')

        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)

    	for row in rows_uebergabepunkte :
##       		list_uebergabepunkte.append("ID: "+str( row.Id) + " | Name: " + repr(row.Name_postalisch))
            list_uebergabepunkte.append( row.Id)
       	try:
            del tablepath_maerkte,rows_uebergabepunkte,row
        except:
            pass

        try:
            tablepath_c_zentrenheck = os.path.join(base_path,'3_Projekte',projectname,'FGDB_34_Wertveraenderungen_'+projectname+'.gdb','Zentren')

            cur_loescher= arcpy.SearchCursor(tablepath_c_zentrenheck)

            for row_zent in cur_loescher:
                if row_zent.Zentren !="":
                    list_parameter_zent.remove(row_zent.Zentren)
                if row_zent.Markt_1 !="":
                    list_uebergabepunkte.remove(row_zent.Markt_1)
                if row_zent.Markt_2 !="":
                    list_uebergabepunkte.remove(row_zent.Markt_2)
                if row_zent.Markt_3 !="":
                    list_uebergabepunkte.remove(row_zent.Markt_3)

            del row_zent,cur_loescher,tablepath_c_zentrenheck
        except:
            pass

        self.params[1].filter.list=list(set(list_parameter_zent ))
        list_uebergabepunkte = sorted(list(set(list_uebergabepunkte )))
        i=2;
        self.params[i].filter.list = list_uebergabepunkte

        i+=1;
        self.params[i].filter.list = list_uebergabepunkte

        i+=1;
        self.params[i].filter.list = list_uebergabepunkte


    if self.params[5].value == True and not self.params[5].hasBeenValidated:
        if (self.params[2].value!="" and self.params[3].value!="" and self.params[4].value!=""):

            if (self.params[2].value==self.params[3].value) or (self.params[2].value==self.params[4].value) or (self.params[3].value==self.params[4].value):


                self.params[4].value = ""
                self.params[3].value = ""
                self.params[2].value = ""
                self.params[1].value = ""
                self.params[5].value = False
                self.params[6].value ="ERROR - Die Eingaben sind nicht möglich - Bitte Überprüfen Sie ihre Eingaben "
                return
            else:

                projectname = self.params[0].value
                tabelle_zentren = os.path.join(base_path,'3_Projekte',projectname,'FGDB_34_Wertveraenderungen_'+projectname+'.gdb','Zentren')

                try:
                    Zentrum = self.params[1].value
                    Markt_1 = self.params[2].value
                    Markt_2 = self.params[3].value
                    Markt_3 = self.params[4].value


                    #Step 3: Insert new row with given values
                    Insert = arcpy.InsertCursor(tabelle_zentren)
                    row = Insert.newRow()
                    row.Zentren = Zentrum
                    row.Markt_1 = Markt_1
                    row.Markt_2 = Markt_2
                    row.Markt_3 = Markt_3
                    Insert.insertRow(row)


                    del tabelle_zentren, Insert,row


                    self.params[6].value ="Die Eingaben für die Zentrennummer " + str(self.params[1].value) + " wurden gespeichert. Wählen Sie die nächste Zentrennummer aus oder beenden Sie die Eingabe mit 'OK'"
                    self.params[5].value = False
                    self.params[4].value = ""
                    self.params[3].value = ""
                    self.params[2].value = ""
                    self.params[1].value = ""
                except:
                    self.params[4].value = ""
                    self.params[3].value = ""
                    self.params[2].value = ""
                    self.params[5].value = False
                    self.params[6].value ="ERROR - Fehler in der Eingabe "
                    return

        else:

                    self.params[4].value = ""
                    self.params[3].value = ""
                    self.params[2].value = ""
                    self.params[1].value = ""
                    self.params[5].value = False
                    self.params[6].value ="ERROR - Drei Märkte müssen mindestens zu einem Zentrum verbunden werden! "
                    return

    try:
        tablepath_c_zentrenheck = os.path.join(base_path,'3_Projekte',projectname,'FGDB_34_Wertveraenderungen_'+projectname+'.gdb','Zentren')

        cur_loescher= arcpy.SearchCursor(tablepath_c_zentrenheck)

        for row_zent in cur_loescher:
            if row_zent.Zentren !="":
                try:
                    list_parameter_zent.remove(row_zent.Zentren)
                except:
                    pass
            if row_zent.Markt_1 !="":
                try:
                    list_uebergabepunkte.remove(row_zent.Markt_1)
                except:
                    pass
            if row_zent.Markt_2 !="":
                try:
                    list_uebergabepunkte.remove(row_zent.Markt_2)
                except:
                    pass
            if row_zent.Markt_3 !="":
                try:
                    list_uebergabepunkte.remove(row_zent.Markt_3)
                except:
                    pass

        self.params[1].filter.list = list_parameter_zent
        self.params[2].filter.list = list_uebergabepunkte
        self.params[3].filter.list = list_uebergabepunkte
        self.params[4].filter.list = list_uebergabepunkte
        del row_zent,cur_loescher
    except:
        pass




    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return