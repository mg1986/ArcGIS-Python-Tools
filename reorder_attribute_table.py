# Author: Matthew Gray
# Copyright (C) 2017 Matthew Gray
# Last Modified: 09/18/2017
# rearrange_attribute_table.py - Allows for the field order of a layers attribute table to be permaneantly reordered

# Module imports
import os
import arcpy

# Set overwrites to True
arcpy.env.overwriteOutput = True
            
# Script tool input variables
input_layer = arcpy.GetParameterAsText(0)
output_workspace = arcpy.GetParameterAsText(1)
output_layer_name = arcpy.GetParameterAsText(2)
field_order_list = arcpy.GetParameterAsText(4).split(";")
arcpy.AddMessage(field_order_list)

# Create a Field Mappings and add all fields in the field_order_list to it
fms = arcpy.FieldMappings()

for field in field_order_list:
    field_map = arcpy.FieldMap()
    field_map.addInputField(input_layer, field)
    fms.addFieldMap(field_map)

# Save output layer to disk
arcpy.FeatureClassToFeatureClass_conversion (input_layer, output_workspace, output_layer_name, field_mapping=fms)
