# -*- coding: utf-8 -*-


from collections import OrderedDict
import arcpy


class LayerGroup(OrderedDict):
    """"""
    def __init__(self, label='root'):
        """
        Parameters
        ----------
        label : str, optional(defaul='root')
            the label of the layer group

        Examples
        --------
        >>> lg = LayerGroup()
        >>> lg.label
        'root'
        """
        super(LayerGroup, self).__init__()
        self.label = label

    def __repr__(self, _repr_running={}):
        return self.label

    def __getitem__(self, key):
        value = self.get_value(key)
        if value is None:
            raise KeyError('{} not found'.format(key))
        return value

    def get_label(self, key):
        """
        return the label of the given key in self or a subgroup

        Parameters
        ----------
        key : str

        Returns
        -------
        label : str
        """
        return self[key].label

    def get_value(self, key):
        value = self.get(key)
        it = self.itervalues()
        while value is None:
            try:
                group = it.next()
                value = group.get_value(key)
            except StopIteration:
                break
        return value

    def add(self, key, label):
        """
        Parameters
        ----------
        key : str
            the key of the layer group
        label : str
            the label of the layer group

        Examples
        --------
        >>> lg = LayerGroup()
        >>> analysen = lg.add('analyse', 'Analysen')
        >>> definition = lg.add('definition', 'Definition')
        >>> einnahmen = analysen.add('einnahmen', 'Einnahmen')
        >>> steuern = einnahmen.add('steuern', 'Steuern')
        >>> ausgaben = analysen.add('ausgaben', 'Ausgaben')
        >>> nutzung = definition.add('nutzung', 'Nutzungsart')
        >>> analysen.label
        'Analysen'
        >>> nutzung.label
        'Nutzungsart'
        >>> lg['nutzung']
        Nutzungsart
        >>> lg['analyse']
        Analysen
        >>> len(lg['analyse'])
        2
        >>> len(lg['definition'])
        1
        >>> len(lg['ausgaben'])
        0
        >>> len(lg['einnahmen'])
        1
        >>> lg['steuern']
        Steuern
        >>> analysen['steuern']
        Steuern
        >>> einnahmen['steuern']
        Steuern
        >>> definition['steuern']
        Traceback (most recent call last):
            ...
        KeyError: 'steuern not found'
        """
        lg = LayerGroup(label)
        self[key] = lg
        return lg



class Output(object):
    """
    Add and update layers to the current ArcMap file.
    """
    def __init__(self, folders, params, parent_tbx):
        self.folders = folders
        self.params = params
        self.module = LayerGroup()
        self.add_layer_groups()
        self.parent_tbx = parent_tbx

    def add_layer_groups(self):
        root = self.module
        analysen = root.add("analysen", "Analysen")
        pd = root.add("projektdefinition", "Projektdefinition")
        background = root.add('hintergrundkarten', 'Hintergrundkarten Projekt-Check')

        analysen.add("bevoelkerung",
                     "Wirkungsbereich 1 - Bewohner und Arbeitsplaetze")
        analysen.add("erreichbarkeit",
                     "Wirkungsbereich 2 - Erreichbarkeit")
        analysen.add("verkehr", "Wirkungsbereich 3 - Verkehr im Umfeld")
        analysen.add("oekologie", "Wirkungsbereich 4 - Fläche und Ökologie")
        analysen.add("infrastruktur",
                     "Wirkungsbereich 5 - Infrastrukturfolgekosten")
        analysen.add("einnahmen",
                     "Wirkungsbereich 6 - Kommunale Steuereinnahmen")
        analysen.add("standortkonkurrenz",
                     "Wirkungsbereich 7 - Standortkonkurrenz Lebensmitteleinzelhandel")

    def set_projectlayer(self, projektname=None):
        """
        Check and add project layer
        """
        projektname = projektname or self.params._get_projectname()

        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame

        layer_exists = arcpy.mapping.ListLayers(
            current_mxd,
            projektname,
            current_dataframe)
        if layer_exists:
            is_grouplayer = layer_exists[0].isGroupLayer
        else:
            is_grouplayer = False

        if not layer_exists or not is_grouplayer:
            group_layer_template = self.folders.get_layer(
                layername="__Projektname__", folder='toc', enhance=True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            addLayer.name = projektname
            arcpy.mapping.AddLayer(current_dataframe, addLayer, "TOP")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

    def get_projectlayer(self, projectname=None):
        """
        Returns project layer in table of contents

        Parameters
        ----------
        projectname : str, optional
        """
        projectname = projectname or self.params._get_projectname()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        layers = arcpy.mapping.ListLayers(current_mxd, projectname,
                                          current_dataframe)
        projectlayer = []
        for layer in layers:
            if layer.isGroupLayer:
                projectlayer = layer

        return projectlayer

    def set_headgrouplayer(self, project_layer=None, dataframe=None):
        """
        Check and add headgroup layer groups
        """
        project_layer = project_layer or self.get_projectlayer()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        dataframe = dataframe or current_mxd.activeDataFrame

        projektdef = self.module.get_label("projektdefinition")
        if not arcpy.mapping.ListLayers(project_layer,
                                        projektdef,
                                        dataframe):
            group_layer_template = self.folders.get_layer(
                layername=projektdef,  folder='toc', enhance=True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayerToGroup(dataframe, project_layer,
                                          addLayer, "BOTTOM")

        analysen = self.module.get_label("analysen")
        if not arcpy.mapping.ListLayers(project_layer,
                                        analysen,
                                        dataframe):
            group_layer_template = self.folders.get_layer(
                layername=analysen, folder='toc', enhance=True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayerToGroup(dataframe, project_layer,
                                          addLayer, "BOTTOM")

    def set_backgroundgrouplayer(self, dataframe=None):
        """
        Check and add Background layer group
        """
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        dataframe = dataframe or current_mxd.activeDataFrame
        hintergrund = self.module.get_label("hintergrundkarten")
        if not arcpy.mapping.ListLayers( current_mxd,
                                         hintergrund,
                                         dataframe):
            group_layer_template = self.folders.get_layer(
                layername=hintergrund, folder='toc', enhance=True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            arcpy.mapping.AddLayer(dataframe, addLayer, "BOTTOM")

    def set_grouplayer(self, group,
                       project_layer=None,
                       dataframe=None,
                       headgroup=""):
        """
        Check and add subgroup layer
        """
        project_layer = project_layer or self.get_projectlayer()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        dataframe = dataframe or current_mxd.activeDataFrame

        if not arcpy.mapping.ListLayers(project_layer, group, dataframe):
            group_layer_template = self.folders.get_layer(layername=group,
                folder='toc', enhance=True)
            addLayer = arcpy.mapping.Layer(group_layer_template)
            if headgroup == "":
                target_headgroup = self.module["analysen"]
            target_headgrouplayer = arcpy.mapping.ListLayers(
                project_layer, target_headgroup, dataframe)[0]
            arcpy.mapping.AddLayerToGroup(
                dataframe, target_headgrouplayer, addLayer, "BOTTOM")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

    def set_subgrouplayer(self,
                          group,
                          subgroup,
                          project_layer=None,
                          dataframe=None):
        """
        Check and add subgroup layer
        """
        project_layer = project_layer or self.get_projectlayer()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        dataframe = dataframe or current_mxd.activeDataFrame

        group_layer = arcpy.mapping.ListLayers(
            project_layer, group, dataframe)[0]
        if not arcpy.mapping.ListLayers(group_layer, subgroup, dataframe):
            subgroup_layer_template = self.folders.get_layer(
                layername=subgroup,
                folder='toc',
                enhance=True)
            addLayer = arcpy.mapping.Layer(subgroup_layer_template)
            target_grouplayer = arcpy.mapping.ListLayers(
                project_layer, group, dataframe)[0]
            arcpy.mapping.AddLayerToGroup(
                dataframe, target_grouplayer, addLayer, "BOTTOM")
            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

    def add_output(self,
                   groupname,
                   template_layer,
                   featureclass='',
                   disable_other=False,
                   subgroup="",
                   in_project=True,
                   zoom=True):
        """
        Add output layer to group

        Parameters
        ----------
        groupname : str
            the layer group

        template_layer : str
            full path of the template layer

        featureclass : str, optional
            the full path of the feature class,
            which should be linked to the layer

        disable_other : boolean, optional(Default=False)
            if true, then all other layers will be turned off

        subgroup : str, optional
            the subgroup of the layergroup

        in_project : bool, optional(Default = True)
            if False, layer will be created outside the project layers

        zoom : bool, optional(Default = True)
            if True, zoom to layer extent
        """

        projektname = self.params._get_projectname()
        group = self.module.get_label(groupname)
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame

        # Layer-Gruppen hinuzfuegen, falls nicht vorhanden
        self.set_backgroundgrouplayer(current_dataframe)

        # Template Layer laden
        source_layer = arcpy.mapping.Layer(template_layer)
        arcpy.AddMessage(source_layer)

        # Datasource des Layers auf die gewünschte FeatureClass setzen
        if featureclass:
            arcpy.AddMessage(featureclass)
            source_ws = source_layer.workspacePath
            target_ws = arcpy.Describe(featureclass).path
            source_layer.findAndReplaceWorkspacePath(source_ws, target_ws)

        # Untergruppen hinzufügen
        if in_project:
            self.set_projectlayer(projektname)
            project_layer = self.get_projectlayer(projektname)
            self.set_headgrouplayer(project_layer, current_dataframe)
            self.set_grouplayer(group, project_layer, current_dataframe)
            if subgroup != "":
                self.set_subgrouplayer(group, subgroup,
                                       project_layer, current_dataframe)

            # Neuen Layer hinzufuegen
            target_grouplayer = arcpy.mapping.ListLayers(
                project_layer, group, current_dataframe)[0]
        else:
            target_grouplayer = arcpy.mapping.ListLayers(
                current_mxd, group, current_dataframe)[0]

        # Layer zur Group oder Subgroup hinzufügen
        if not subgroup:
            self.add_or_replace_layer(target_grouplayer,
                                      current_dataframe,
                                      source_layer)
        else:
            target_subgrouplayer = arcpy.mapping.ListLayers(
                target_grouplayer, subgroup, current_dataframe)[0]

            self.add_or_replace_layer(target_subgrouplayer,
                                      current_dataframe,
                                      source_layer)

        # neuer Layer
        new_layer = arcpy.mapping.ListLayers(target_grouplayer,
                                             source_layer.name,
                                             current_dataframe)[0]
        # Auf Layer zentrieren
        if zoom:
            ext = new_layer.getExtent()
            current_dataframe.extent = ext
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

        if disable_other == True:
            for lyr in arcpy.mapping.ListLayers(project_layer):
                lyr.visible = False
        new_layer.visible = True
        if subgroup != "":
            target_subgrouplayer.visible = True
        target_grouplayer.visible = True
        if in_project:
            project_layer.visible = True
            analysen = self.module["analysen"]
            if groupname in analysen:
                arcpy.mapping.ListLayers(project_layer,
                                         analysen,
                                         current_dataframe)[0].visible = True
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

    def add_or_replace_layer(self,
                             target_grouplayer,
                             current_dataframe,
                             source_layer):
        """
        Add source_layer to target_grouplayer
        in the current_dataframe and remove existing layer
        in the target_grouplayer if exists"""
        existing_layers = arcpy.mapping.ListLayers(
            target_grouplayer,
            source_layer.name,
            current_dataframe)
        if existing_layers:
            for layer in existing_layers:
                arcpy.mapping.RemoveLayer(current_dataframe, layer)

        arcpy.mapping.AddLayerToGroup(current_dataframe,
                                      target_grouplayer,
                                      source_layer, "BOTTOM")

    def delete_output(self, layer):

        projektname = self.params._get_projectname()
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        project_layer = self.get_projectlayer(projektname)

        if project_layer:
            layer_exists = arcpy.mapping.ListLayers(project_layer,
                                                    layer, current_dataframe)
            if layer_exists:
                arcpy.mapping.RemoveLayer(current_dataframe, layer_exists[0])

        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

    def update_output(self, group, layername):
        """ToDo - oder ist das was replace_output tun soll?"""
        projektname = self.params._get_projectname()


    def replace_output(self,
                       groupname,
                       fc,
                       layername,
                       folder,
                       subgroup='',
                       disable_other=False):
        """
        delete output layer if exists and create a new layer in groupname

        Parameters
        ----------
        groupname : str
            the groupname where the layer should be created
        fc : str
            the featur-class to show
        layername : str
            the layername
        folder : str
            the folder, where the template layer resides
        subgroup : str, optional
            the subgroup below the group
        disable_other : bool, optional(default=False)
            if true, disable other layers
        """
        self.delete_output(layername)
        template_lyr = self.folders.get_layer(layername=layername,
                                              enhance=True,
                                              folder=folder)
        self.add_output(groupname=groupname,
                        template_layer=template_lyr,
                        featureclass=fc,
                        disable_other=disable_other,
                        subgroup=subgroup,
                        )

    @staticmethod
    def reclassify_layer(mxd, lyrname):
        """
        Reclassify the first layer in the mxd that matches lyrname

        Parameters
        ----------
        mxd : map-instance
        lyrname : str
            the layername
        """
        matched_layers = arcpy.mapping.ListLayers(mxd, lyrname)
        if matched_layers:
            lyr = matched_layers[0]
            lyr.symbology.reclassify()

    def change_layers_workspace(self, source_ws, target_ws):
        """
        change the workspace in the current map that reference source_ws
        to target_ws

        Parameters
        ----------
        source_ws : str
        target_ws : str
        """
        mxd = arcpy.mapping.MapDocument('CURRENT')
        mxd.findAndReplaceWorkspacePaths(source_ws, target_ws)
        arcpy.RefreshActiveView()

    def define_projection(self):
        """Define the projection of the current dataframe from the config"""
        config = self.parent_tbx.config
        mxd = arcpy.mapping.MapDocument('CURRENT')
        df = mxd.activeDataFrame
        sr = arcpy.SpatialReference(config.epsg)
        df.spatialReference = sr
        df.geographicTransformations = [config.transformation]
        arcpy.RefreshActiveView()

    def add_graph(self, input_template, graph, out_graph_name):
        """
        Add a graph to the output.
        If a graph with the same name already exists,
        replace it with the new one

        Parameters
        ----------
        input_template : a graph template
        graph : arcpy.Graph-instance
        out_graph_name : str
            the name of the graph to create
        """
        arcpy.env.addOutputsToMap = True
        old_overwrite = arcpy.env.overwriteOutput
        arcpy.env.overwriteOutput = True
        arcpy.MakeGraph_management(input_template, graph, out_graph_name)
        arcpy.env.addOutputsToMap = False
        arcpy.env.overwriteOutput = old_overwrite
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
