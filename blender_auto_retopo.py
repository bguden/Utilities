import bpy
import os
import numpy
from mathutils import Vector, Euler, Matrix
# from math import 

def SelectAndActivate(obj):
    # bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    pass

def Scale_mm_to_in(obj):
    scaleFactor = 1/25.4 # convert mm to in

    obj.scale = (scaleFactor, scaleFactor, scaleFactor)
            
    SelectAndActivate(obj)
    bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)

    pass

def Center_obj(obj, bottom=False):
    SelectAndActivate(obj)

    ################# set object center to 0,0,0
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location = (0, 0, 0)

    if (bottom):
        ################# center bottom of object at 0, 0, 0
        new_cursor_z = -bpy.context.object.dimensions.z/2.0
        bpy.context.scene.cursor.location = Vector((0.0, 0.0, new_cursor_z))
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
        obj.location = (0, 0, 0)

    pass

def ApplyMaterial(object_target, mat):
    if mat is None:
        # create material
        print("material not found")
        mat = bpy.data.materials.new(name="new_mat")
        mat.use_nodes = True
        node_tree = mat.node_tree
        nodes = node_tree.nodes
        bsdf = nodes.get("Principled BSDF") 

    # Assign it to object
    if object_target.data.materials:
        # assign to 1st material slot
        object_target.data.materials[0] = mat
    else:
        # no slots
        object_target.data.materials.append(mat)

    pass

def Retopo(obj):
    # filePath = "//..\\..\\..\\Python Scripts\\blender\\low poly\\"
    filePath = '/'
    fileName = obj.name + "_low"
    
    ############### Create duplicate object
    # obj_low = obj.copy()
    # obj_low.data = obj.data.copy()
    # bpy.data.scenes[0].collection.objects.link(obj_low)
    bpy.ops.object.duplicate(linked=False)
    obj_low = bpy.context.active_object
    obj_low.name = fileName
    
    ############### apply modifier to reduce polygons
    remesh_mod = obj_low.modifiers.new("Remesh", 'REMESH')
    remesh_mod.voxel_size = 0.03 # gives around 15k faces (30k tris) for 2 length wall...
    remesh_mod.use_smooth_shade = True

    SelectAndActivate(obj_low)
    bpy.ops.object.modifier_apply(modifier="Remesh")

    ############### add a new material
    ApplyMaterial(obj_low, None)

    ############### create the uv
    new_uv = bpy.context.active_object.data.uv_layers.new(name='NewUV')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()

    ############### bake the high poly normal map to the low poly model
    bpy.context.scene.low_poly = obj_low
    bpy.context.scene.high_poly = obj

    bpy.ops.object.bake_op()

    ############### save the new normal map
    mat = obj_low.data.materials[0]
    image = mat.node_tree.nodes.get('Image Texture').image

    fileType = ".png"
    # totalPath = filePath + fileName + "_normal" + fileType
    fileDirectory = "C:\\Users\\Brandon\\Documents\\Python Scripts\\blender\\low poly\\"
    totalPath = os.path.join(fileDirectory, fileName + "_normal" + fileType)
    # totalPath = filePath + image.name + fileType
    # image = bpy.data.images["2-length-fan-wall.004_normal.002"]
    # image = bpy.data.images[fileName + "_normal"]
    image.file_format = 'PNG'
    image.filepath_raw = totalPath
    image.save()
    # bpy.ops.image.save_as(save_as_render=False, filepath=totalPath, show_multiview=False, use_multiview=False)

    ############### hide the high poly model
    obj.hide_set(True)

    ############### export the low poly model as fbx
    fileType = ".fbx"
    totalPath = os.path.join(fileDirectory, fileName + fileType)
    # totalPath = filePath + fileName + ".fbx"
    bpy.ops.export_scene.fbx(filepath=totalPath, use_selection=False, use_visible=True, object_types={'MESH'})

    pass

targetName = bpy.context.active_object.name
target = bpy.data.objects[targetName]
Scale_mm_to_in(target)
Center_obj(target, bottom=True)
Retopo(target)
