# Author: Matthew Gray
# Copyright (C) 2017 Matthew Gray
# Last Modified: 09/18/2017
# kmz_with_labels.py - Creates a point, line, or polygon kmz with each feature labeled

# Module imports
import os
import shutil

import arcpy

# Set overwrites to True
arcpy.env.overwriteOutput = True

# Set cwd
cwd = os.path.dirname(__file__)  

# Set Scratch GDB
scratch_gdb = arcpy.env.scratchGDB

# WGS84
wgs_1984 = arcpy.SpatialReference(4326)

# Script tool input variables      
input_layer = arcpy.GetParameterAsText(0)
label_field = arcpy.GetParameterAsText(1)
output_kmz_folder = arcpy.GetParameterAsText(2)
output_kmz_name = arcpy.GetParameterAsText(3)

# Reproject input to WGS84
arcpy.Project_management(input_layer, os.path.join(scratch_gdb, "INPUT_LAYER_WGS84"), wgs_1984)
wgs84_fc = os.path.join(scratch_gdb, "INPUT_LAYER_WGS84")

# Input Layer
input_lyr = arcpy.mapping.Layer(wgs84_fc)    
input_lyr.name = output_kmz_name
arcpy.ApplySymbologyFromLayer_management (input_lyr, input_layer)

# Create Input Labels
arcpy.AddField_management(wgs84_fc, "XCENTROID", "DOUBLE")
arcpy.CalculateField_management(wgs84_fc, "XCENTROID", "!SHAPE.CENTROID.X!","PYTHON_9.3")

arcpy.AddField_management(wgs84_fc, "YCENTROID", "DOUBLE")
arcpy.CalculateField_management(wgs84_fc, "YCENTROID", "!SHAPE.CENTROID.Y!","PYTHON_9.3")

arcpy.MakeXYEventLayer_management (wgs84_fc, "XCENTROID", "YCENTROID", "KMZ_LABELS", wgs_1984)
arcpy.CopyFeatures_management("KMZ_LABELS", os.path.join(scratch_gdb, "KMZ_LABELS"))
input_labels = os.path.join(scratch_gdb, "KMZ_LABELS")

arcpy.DeleteField_management(input_labels, ["XCENTROID", "YCENTROID"])

# Input Labels File
mxd = arcpy.mapping.MapDocument(os.path.join(cwd, "KMZ_WITH_LABELS.mxd"))
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

input_labels_lyr = arcpy.mapping.ListLayers(mxd, "", df)[1]
input_labels_lyr.replaceDataSource (scratch_gdb, "FILEGDB_WORKSPACE", "KMZ_LABELS")
input_labels_lyr.labelClasses[0].expression = "[" + label_field + "]"

kmz_group_lyr = arcpy.mapping.ListLayers(mxd, "", df)[0]
arcpy.mapping.AddLayerToGroup(df, kmz_group_lyr, input_lyr, "TOP")

kmz_group_lyr.name = output_kmz_name

arcpy.RefreshTOC()
arcpy.RefreshActiveView()

# Export to KMZ
arcpy.LayerToKML_conversion (kmz_group_lyr, os.path.join(output_kmz_folder, output_kmz_name + ".kmz"))

# Delete intermediary data and clean up scratch workspace
arcpy.env.workspace = scratch_gdb
fc_list = arcpy.ListFeatureClasses()
while "INPUT_LAYER_WGS84" in fc_list or "KMZ_LABELS" in fc_list:
    for fc in fc_list:
        if fc in ["INPUT_LAYER_WGS84", "KMZ_LABELS"]:
            arcpy.Delete_management (fc)
    fc_list = arcpy.ListFeatureClasses()
    arcpy.Compact_management(scratch_gdb)

