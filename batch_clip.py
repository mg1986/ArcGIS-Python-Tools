# Author: Matthew Gray
# Copyright (C) 2018 Matthew Gray
# Last Modified: 03/15/2018
# batch_clip.py - Clips multiple input layers on one clipping layer.

# Module imports
import os
import arcpy

# Set overwrites to True
arcpy.env.overwriteOutput = True
            
# Script tool input variables
input_layers = arcpy.GetParameterAsText(0).split(";")
clip_layer = arcpy.GetParameterAsText(1)
output_workspace = arcpy.GetParameterAsText(2)

for layer in input_layers:
    arcpy.Clip_analysis (layer, clip_layer, os.path.join(output_workspace, layer + "_CLIP"))
