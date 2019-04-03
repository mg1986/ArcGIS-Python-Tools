# Author: Matthew Gray
# Copyright (C) 2017 Matthew Gray
# Last Modified: 03/01/2018
# split_by_values.py - Splits a layer into multiple layers based of the values in a integer or string field

# Module imports
import re
import arcpy

# Set overwrites to True
arcpy.env.overwriteOutput = True

# Script tool input variables
input_layer = arcpy.GetParameterAsText(0)
output_workspace = arcpy.GetParameterAsText(1)
output_name = arcpy.GetParameterAsText(2)
split_field = arcpy.GetParameterAsText(3)
split_values_list  = arcpy.GetParameterAsText(4).split(";")
where_clause = ""

# Determines data type of split_field
field_type = [f.type for f in arcpy.ListFields(input_layer) if f.name == split_field][0]

# Iterate through all the items in split_values_list and save out an individul layer for each one
for value in split_values_list:
    arcpy.AddMessage(value)
    #arcpy.AddMessage(value[0])
    # Generate where clause based on field_type
    if field_type == "String":
        if value not in ["", " "]:
            counter = 0
            value_list = []
            for item in value:
                if counter == 0 or counter == len(value)-1:
                    if item == "'":
                        item =''
                    value_list.append(item)
                elif counter != 0 or counter != len(value)-1:
                    value_list.append(item.replace("'", "''").replace('"', '""'))
                counter += 1
                
            value = ''.join(value_list)
        where_clause = '"' + split_field + '"' + " = " + "'" + value + "'"
    else:
        where_clause = '"' + split_field + '"' + " = " + str(value)
        
    # Use regular expression to remove special characters from each output layer name
    value = re.sub(r'[^\w]', '_', value.replace("'", ""))
    output_layer_name = output_name + "_" + value

    # Save each final layer to disk
    arcpy.FeatureClassToFeatureClass_conversion (input_layer, output_workspace, output_layer_name, where_clause)
