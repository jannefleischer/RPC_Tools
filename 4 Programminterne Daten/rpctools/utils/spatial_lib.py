import arcpy
from rpctools.utils.params import Folders
from rpctools.utils.params import DummyTbx
from rpctools.utils.output import ArcpyEnv

import requests
import numpy as np
from os.path import join

def google_geocode(address, api_key=''):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address}
    if api_key:
        params['key'] = api_key
    r = requests.get(url, params=params)
    json = r.json()
    results = json['results']
    msg = json['status'] if json.has_key('status') else ''
    if not results:
        if json.has_key('error_message'):
            msg = json['error_message']
        return None, msg
    location = results[0]['geometry']['location']
    return (location['lat'], location['lng']), msg

def get_closest_point(point, points):
    """get the point out of given points that is closest to the given point,
    points are be passed as tuples of x, y (z optional) coordinates
    
    Parameters
    ----------
    point : tuple
        x, y (, z) coordinates of point
    points : list of tuples
        x, y (, z) coordinates of points to pick closest one to point from

    Returns
    -------
    index : int
        index of closest point in points
    point : tuple
        x, y of closest point
    """
    points = [np.array(p) for p in points]
    diff = np.array(points) - np.array(point)
    distances = np.apply_along_axis(np.linalg.norm, 1, diff)
    closest_idx = distances.argmin()
    return closest_idx, tuple(points[closest_idx])

def clip_raster(in_file, out_file, bbox):

    desc = arcpy.Describe(in_file)
    sr = desc.spatialReference
    srid = sr.factoryCode
    p1, p2 = bbox
    p1.transform(srid)
    p2.transform(srid)
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
    with ArcpyEnv(addOutputsToMap=False):
        folders = Folders()
        gemeinden = folders.get_base_table('FGDB_Basisdaten_deutschland.gdb',
                                           'bkg_gemeinden')
        tmp_table = join(arcpy.env.scratchGDB, 'tmp_join')
        if arcpy.Exists(tmp_table):
            arcpy.Delete_management(tmp_table)
    
        arcpy.SpatialJoin_analysis(features, gemeinden, tmp_table,
                                   match_option='HAVE_THEIR_CENTER_IN')
    
        cursor = arcpy.da.SearchCursor(tmp_table, [id_column, 'AGS_0', 'GEN'])
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

def assign_groessenklassen():
    '''assign the groessenklassen to the gemeinde table based on their
    number of inhabitants'''
    folders = Folders()
    tbx = DummyTbx()
    workspace = 'FGDB_Basisdaten_deutschland.gdb'
    gr_table = folders.get_base_table(workspace, 'Gemeindegroessenklassen')
    gr_df = tbx.table_to_dataframe('Gemeindegroessenklassen',
                                   workspace=workspace,
                                   is_base_table=True)
    # set nan values to max integer (for highest groessenklasse)
    gr_df.loc[np.isnan(gr_df['bis']), 'bis'] = sys.maxint
    gem_columns = ['Einwohner', 'groessenklasse']
    gem_table = folders.get_base_table(workspace, 'bkg_gemeinden')
    
    cursor = arcpy.da.UpdateCursor(gem_table, gem_columns)
    for ew, gr_klasse in cursor:
        higher = ew >= gr_df['von']
        lower = ew < gr_df['bis']
        # take the id where both borders match
        match = gr_df['groessenklasse'][np.logical_and(higher, lower)].values
        assert len(match) == 1
        gr_klasse = match[0]
        cursor.updateRow((ew, gr_klasse))

if __name__ == '__main__':
    assign_groessenklassen()