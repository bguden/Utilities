# import bpy
'''
To run in Blender 2.8 python console copy and run the following two lines:

scriptFilePath = "C:/Users/Brandon/Documents/3D Printing/_Terrain/WarLayer-4-Files-Delivery/_mods/double_side_roofs.py"

exec(compile(open(scriptFilePath).read(), scriptFilePath, 'exec'))

# scriptFilePath is the complete directory path to this script file (on Windows this usually starts with C:/Users/[username]/ where [username] is replaced with your username on your computer)
# If copying the directory path from Windows File Explorer, '\' characters will need to be changed to '/' characters
'''

import os

# The complete directory path to the folder where the files are (on Windows this usually starts with C:/Users/[username]/ where [username] is replaced with your username on your computer)
# If copying the directory path from Windows File Explorer, '\' characters will need to be changed to '/' characters
startingDirectory = "C:/Users/Brandon/Documents/3D Printing/_Terrain/WarLayer-4-Files-Delivery/"

import_subfolder = "Floors and roofs/"

# file name of the first file (excluding the extension)
model_name_1 = "3x2-roof-style-B"
# file name of the first file (excluding the extension)
model_name_2 = "3x2-roof-style-D"

# file extenion type (for 3D printing files this is usually .stl)
fileType = ".stl"

# optional output directory an file name for automatically exporting and saving the final part
saveFilePath = startingDirectory + "_mods/"
saveFileName = model_name_1 + "_&_" + model_name_2



import_path_1 = os.path.abspath(startingDirectory + import_subfolder + model_name_1 + fileType)
import_path_2 = os.path.abspath(startingDirectory + import_subfolder + model_name_2 + fileType)

# delete any existing objects in the scene
objects = bpy.context.scene.objects
for obj in objects:
    obj.select_set(True)
    bpy.ops.object.delete()

# import and center the first file
bpy.ops.import_mesh.stl(filepath=import_path_1)
model_1 = bpy.context.object
model_1.name = model_name_1
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
model_1.location[0] = 0
model_1.location[1] = 0
model_1.location[2] = 0

# rotate the first model 180 degrees
model_1.rotation_euler[2] = 3.14159

# import and center the second file
bpy.ops.import_mesh.stl(filepath=import_path_2)
model_2 = bpy.context.object
model_2.name = model_name_2
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
model_2.location[0] = 0
model_2.location[1] = 0
model_2.location[2] = 0

# sclae and move the object slightly so faces and edges are not perfectly coplaner so the boolean modier will work more consistently
scale = 1.01
model_2.scale[0] = scale
model_2.scale[1] = scale
model_2.scale[2] = scale
model_2.location[0] = 0.1

# add the boolean modier
# bpy.data.objects[model_name_1].select_set(True)
model_1.select_set(True)
bpy.context.view_layer.objects.active = model_1
bpy.ops.object.modifier_add(type='BOOLEAN')
model_1.modifiers["Boolean"].operation = 'INTERSECT'
model_1.modifiers["Boolean"].object = bpy.data.objects[model_name_2]
# apply the boolean modifier
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

# delete the unnecessary second object
model_1.select_set(False)
model_2.select_set(True)
bpy.ops.object.delete()

# optional code to automatically export and save the completed model
