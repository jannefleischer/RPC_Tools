import arcpy
#Diese Datei muss in der Toolbox als Validator für das Projekt löschen Skript eingefügt werden,
#damit die vorhandenen Projekte in der DropdownListe angezeigt werden
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


    list_uebergabepunkte = []

    i=-1

    #set project
    i+=1 ; self.params[i].filter.list = list_projects

    #set point
    i+=1 ; self.params[i].filter.list = list_uebergabepunkte

    heading = "Quellpotenziale"
    i+=1 ; self.params[i].category = heading
    i+=1 ; self.params[i].category = heading
    i+=1 ; self.params[i].category = heading

    heading = "Zielpotenziale"
    i+=1 ; self.params[i].category = heading
    i+=1 ; self.params[i].category = heading
    i+=1 ; self.params[i].category = heading

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

    if self.params[i].altered and not self.params[i].hasBeenValidated:

        projectname = self.params[i].value

        tablepath_uebergabepunkte = os.path.join(base_path,'3_Projekte',projectname,'FGDB_25_Verkehrserzeugung_'+projectname+'.gdb','L01_Uebergabepunkte')

        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_uebergabepunkte)

    	for row in rows_uebergabepunkte :
    		list_uebergabepunkte.append(row.Punkt_Name)
    	list_uebergabepunkte = list(set(list_uebergabepunkte ))


        i+=1 ; self.params[i].filter.list = list_uebergabepunkte


    i=1
    if self.params[i].altered and not self.params[i].hasBeenValidated:

        projectname = self.params[i-1].value
        punkt_name = self.params[i].value

        tablepath_uebergabepunkte = os.path.join(base_path,'3_Projekte',projectname,'FGDB_25_Verkehrserzeugung_'+projectname+'.gdb','L01_Uebergabepunkte')
        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_uebergabepunkte)

        for row in rows_uebergabepunkte:
            if row.Punkt_Name == punkt_name:
                qp_arbeit = row.qp_arbeit
                qp_versorgung = row.qp_versorgung
                qp_bildung = row.qp_bildung
                zp_arbeit = row.zp_arbeit
                zp_versorgung = row.zp_versorgung
                zp_bildung = row.zp_bildung
            else:
                qp_arbeit = 0.0
                qp_versorgung = 0.0
                qp_bildung = 0.0
                zp_arbeit =0.0
                zp_versorgung = 0.0
                zp_bildung = 0.0

        i+=1 ; self.params[i].value = qp_arbeit
        i+=1 ; self.params[i].value = qp_versorgung
        i+=1 ; self.params[i].value = qp_bildung
        i+=1 ; self.params[i].value = zp_arbeit
        i+=1 ; self.params[i].value = zp_versorgung
        i+=1 ; self.params[i].value = zp_bildung


    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return