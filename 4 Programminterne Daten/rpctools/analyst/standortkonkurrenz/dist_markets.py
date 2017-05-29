# -*- coding: utf-8 -*-

import arcpy
import os.path

import shutil
from pyproj import Proj, transform
from rpctools.utils.params import Tool
from rpctools.utils.config import Folders


class DistMarkets(Tool):
    _param_projectname = 'project'

    def run(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            for lyr in arcpy.mapping.ListLayers(mxd, "", df):
                if lyr.name == "AusschnittZensusGrid.tif":
                    arcpy.mapping.RemoveLayer(df, lyr)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        del mxd
        toolbox = self.parent_tbx
        folders = Folders(self.par)
        xy_inside = toolbox.query_table("Teilflaechen_Plangebiet",
                                        columns=['INSIDE_X', 'INSIDE_Y'],
                                        workspace='FGDB_Definition_Projekt.gdb')
        num_areas = len(xy_inside)

        # Gauß Krueger:
        x_mid = sum([tuple[0] for tuple in xy_inside]) / num_areas
        y_mid = sum([tuple[1] for tuple in xy_inside]) / num_areas
        square_size = self.par.square_size.value * 1000 / 2  # in meters
        x_min = x_mid - square_size
        x_max = x_mid + square_size
        y_min = y_mid - square_size
        y_max = y_mid + square_size

        # lat lon:
        target_srs = Proj(init='epsg:{}'.format(4326))
        srid_proj = Proj(init='epsg:{}'.format(toolbox.config.epsg))
        x_min, y_min = transform(srid_proj, target_srs, x_min, y_min)
        x_max, y_max = transform(srid_proj, target_srs, x_max, y_max)

        # clip a square out of ZensusGrid and save it to the projcet folder
        # in path
        in_path = os.path.join(folders.INTERN, r"workspaces\ZensusGrid",
                               "Zensus2011GridWGS84_int.tif")
        # out path
        projectfolder = folders.get_projectpath(project=self.par.project.value)
        new_folder = os.path.join(projectfolder, "AusschnittZensusGrid")
        if os.path.exists(new_folder):
            shutil.rmtree(new_folder)
        os.makedirs(new_folder)
        out_path = os.path.join(new_folder, "AusschnittZensusGrid.tif")
        arcpy.Clip_management(in_path,"{} {} {} {}".format(x_min, y_min,
                                                           x_max, y_max),
                              out_path, "#", "#", "None", "NO_MAINTAIN_EXTENT")
        # add layer
        addLayer = arcpy.mapping.Layer(out_path)
        arcpy.mapping.AddLayer(df, addLayer)

        # create numpy array of tiff file
        #in_raster = arcpy.Raster(out_path)
        #population_array = arcpy.RasterToNumPyArray(in_raster)
        #in_raster.spatialReference()
        #arcpy.RasterToPoint_conversion(in_raster="f:/projekte sh/rpc tools/3 Benutzerdefinierte Projekte/2405/AusschnittZensusGrid/AusschnittZensusGrid.tif",
                                       #out_point_features="F:/Projekte SH/RPC Tools/3 Benutzerdefinierte Projekte/2405/FGDB_Standortkonkurrenz_Supermaerkte.gdb/Einwohner",
                                       #raster_field="Value")

        # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
        # The following inputs are layers or table views: "Einwohner"
        #arcpy.env.extent  = raster
        #arcpy.env.snapRaster = raster

        #arcpy.FeatureToRaster_conversion(in_features="Einwohner",
                                         #field="grid_code",
                                         #out_raster="F:/Projekte SH/RPC Tools/3 Benutzerdefinierte Projekte/2405/FGDB_Standortkonkurrenz_Supermaerkte.gdb/test",
                                         #cell_size="1,20516709876898E-03")