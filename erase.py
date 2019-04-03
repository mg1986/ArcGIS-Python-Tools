# Author: Matthew Gray
# Copyright (C) 2017 Matthew Gray
# Last Modified: 09/18/2017
# erase.py - Mimics the functionality of the ArcGIS Erase tool (available only with an Advanced License)

# Module imports
import os
import arcpy

# Set overwrites to True
arcpy.env.overwriteOutput = True

# Script tool input variables
input_layer = arcpy.GetParameterAsText(0)
erase_layer = arcpy.GetParameterAsText(1)
output_layer = arcpy.GetParameterAsText(2)

# Create temporary copies of inputs and Union them
input_temp = arcpy.FeatureClassToFeatureClass_conversion (input_layer, "in_memory", "input")
erase_temp = arcpy.FeatureClassToFeatureClass_conversion (erase_layer, "in_memory", "erase")
union_temp = arcpy.Union_analysis ([input_temp, erase_temp], os.path.join("in_memory", "union"))

# Iterate through Union output and delete all rows with FID_erase value of -1
rows = arcpy.da.UpdateCursor(union_temp, ["FID_erase"])
for row in rows:
    if row[0] != -1:
        rows.deleteRow()

# Create empty copy of input_layer and truncate and append Union_temp rows into it, preserving
# original table schema with erased features
temp_fc = arcpy.FeatureClassToFeatureClass_conversion (input_layer, "in_memory", "temp")
arcpy.DeleteRows_management(temp_fc)
arcpy.Append_management (union_temp, temp_fc, "NO_TEST")

# Save output layer to disk
arcpy.CopyFeatures_management (temp_fc, output_layer)

