import arcpy
from rpctools.utils.params import Folders
from rpctools.utils.params import DummyTbx

def clip_raster(in_file, out_file, bbox):
    
    desc = arcpy.Describe(in_file)
    sr = desc.spatialReference
    srid = sr.factoryCode
    p1, p2 = bbox
    p1 = p1.transform(srid)
    p2 = p2.transform(srid)
    arcpy.Clip_management(
        in_file,
        "{x_min} {y_min} {x_max} {y_max}".format(
            x_min=p1.x, y_min=p1.y,
            x_max=p2.x, y_max=p2.y),
        out_file)
    return srid

def get_project_centroid(projectname):
    """get the centroid of the defined areas of the given project
    (projection is defined by project)"""
    tbx = DummyTbx()
    tbx.set_active_project(projectname)
    flaechen_df = tbx.table_to_dataframe(
        'Teilflaechen_Plangebiet',
        columns=['INSIDE_X', 'INSIDE_Y'], 
        workspace='FGDB_Definition_Projekt.gdb')
    x = flaechen_df['INSIDE_X'].mean()
    y = flaechen_df['INSIDE_Y'].mean()
    return x, y

def get_ags(features, id_column):
    """
    get the ags and names of the areas the centroids of all polygons in given
    feature table or layer lie in, the bkg_gemeinden table is taken as a source
    for ags and names

    Parameters
    ----------
    features : str
        a feature table
    id_column : str
        the name of the column containing the unique ids of the features

    Returns
    -------
    ags_res : dict
        keys are the ids of the features with tuples of (ags, gen) as values
    """
    folders = Folders()
    gemeinden = folders.get_base_table('FGDB_Basisdaten_deutschland.gdb',
                                       'bkg_gemeinden')
    tmp_table = join(arcpy.env.scratchGDB, 'tmp_join')
    if arcpy.Exists(tmp_table):
        arcpy.Delete_management(tmp_table)

    arcpy.SpatialJoin_analysis(features, gemeinden, tmp_table,
                               match_option='HAVE_THEIR_CENTER_IN')

    cursor = arcpy.da.SearchCursor(tmp_table, [id_column, 'AGS', 'GEN'])
    ags_res = {}
    for row in cursor:
        ags_res[row[0]] = row[1], row[2]

    arcpy.Delete_management(tmp_table)
    return ags_res

def get_gemeindetyp(ags):
    """get the gemeindetyp referenced by ags"""
    folders = Folders()
    table = folders.get_base_table('FGDB_Basisdaten_deutschland.gdb',
                                   'bkg_gemeinden')
    columns = ['Gemeindetyp', 'AGS']
    cursor = arcpy.da.SearchCursor(table, columns, 
                                   where_clause="AGS='{}'".format(ags))
    return cursor.next()[0]

if __name__ == '__main__':
    folders = Folders()
    project = folders.get_projects()[0]
    teilflaechen_table = folders.get_table(
        'Teilflaechen_Plangebiet',
        workspace='FGDB_Definition_Projekt.gdb',
        project=project)
    ags = get_ags(teilflaechen_table, 'id_teilflaeche')
    typ = get_gemeindetyp(ags.values()[0][0])
    print(ags)