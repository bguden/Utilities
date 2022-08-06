import bpy
'''
To run in Blender python console

scriptFilePath = "C:/Users/Brandon/Documents/Unity3D_Games/Frostgrave/Assets/Models/blender/blender_auto.py"

exec(compile(open(scriptFilePath).read(), scriptFilePath, 'exec'))

'''

import os
import numpy
from mathutils import Vector, Euler, Matrix
# from math import 

# startingDirectory = "C:/Users/Brandon/Documents/3D Printing/_Terrain/Castle_Walls_4.1/"

# startingDirectory = "C:\\Users\\Brandon\\Documents\\3D Printing\\_Terrain\\OpenLOCK_Tessellation_Templates_8-3"

# startingDirectory = "C:\\Users\\Brandon\\Documents\\3D Printing\\_Terrain\\__toUnity\\"
startingDirectory = "C:\\Users\\Brandon\\Documents\\3D Printing\\_Terrain\\ZoneMortalis\\"

# modelSaveFileStartingPath = "C:/Users/Brandon/Documents/Unity3D_Games/Frostgrave/Assets/Models/"

# saveFileStartingPath = "C:\\Users\\Brandon\\Documents\\Unity3D_Games\\Frostgrave\\Assets\\"
saveFileStartingPath = "C:\\Users\\Brandon\\Documents\\Unity3D_Games\\_Assets\\Photogrammetry\\"

modelSaveFileStartingPath = saveFileStartingPath + "Models\\Renders\\"
# "C:\\Users\\Brandon\\Documents\\Unity3D_Games\\Frostgrave\\Assets\\Models\\test\\"

# imageSaveFileStartingPath = saveFileStartingPath + "Images\\"

scaleFactor = 1/25.4 # convert mm to in
num_camera_angles = 25

def SetupLightsAndCameras():
    #  delete Collection to fix importing into unity
    # bpy.ops.outliner.collection_delete(hierarchy=False)

    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    # bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    # target = bpy.data.objects["Empty"]

    bpy.context.scene.render.film_transparent = True

    bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
    sun = bpy.data.objects["Sun"]
    sun.rotation_euler = Euler((numpy.deg2rad(30), 0, numpy.deg2rad(90)), 'XYZ') # set sunlight angle

    # create lamp (looks better than sun)
    # point_light = bpy.ops.object.light_add(type='POINT', location=(-2.8, -1.3, 5.9))

    # bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(x, y, z), rotation=(1.0247, 0.00937975, 0.717466), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    overhead_view_location = (7, 0, 7)
    overhead_view_rotation = (numpy.deg2rad(45), 0, numpy.deg2rad(90))
    
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW')
    camera = bpy.data.objects["Camera"]
    bpy.context.scene.camera = camera
    camera.location = overhead_view_location
    camera.rotation_euler = Euler(overhead_view_rotation, 'XYZ')

    pass

def DeleteNonPrimaryObjects():
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    # bpy.ops.object.select_by_type(type='EMPTY')
    # bpy.ops.object.delete()
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()

    pass

def RenderImage(target, angle, filePath):
    target.rotation_euler = Euler((0, 0, numpy.deg2rad(angle)), 'XYZ') # set object rotation

    filePath = filePath + "_" + str(angle) + ".png"

    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.object.select_by_type(type='CAMERA')

    bpy.context.scene.render.filepath = filePath
    bpy.context.scene.render.resolution_x = 1500 #perhaps set resolution in code
    bpy.context.scene.render.resolution_y = 1500
    bpy.ops.render.render(write_still = True)

    pass

def ApplyMaterial(mat, object_target):
    if mat is None:
        # create material
        print("material not found")
        mat = bpy.data.materials.new(name="concrete_wall_005")

    # Assign it to object
    if object_target.data.materials:
        # assign to 1st material slot
        object_target.data.materials[0] = mat
    else:
        # no slots
        object_target.data.materials.append(mat)

    pass

for root, dirs, files in os.walk(startingDirectory):
    if 'Legacy' in dirs:
        dirs.remove('Legacy')  # don't visit Legacy directories
    for file in files:
        if file.endswith(".stl"):
            # print(os.path.join(root, file))
            # print(root)
            # print(file)
            # print(os.path.splitext(file)[0])

            # print(root.replace(startingDirectory,''))
            fileDirectory = root
            fileName = os.path.splitext(file)[0]
            print(fileName)
            fileType = ".stl"
            # print(os.path.join(fileDirectory, fileName + fileType))
            importFilePathComplete = os.path.join(fileDirectory, fileName + fileType)

            # saveFilePath = modelSaveFileStartingPath + fileDirectory.replace(startingDirectory,'') + fileName +".blend"
            fileDirectory = os.path.join(modelSaveFileStartingPath, fileDirectory.replace(startingDirectory,''))
            if (not os.path.exists(fileDirectory)):
                os.makedirs(fileDirectory)

            saveFilePath = os.path.join(fileDirectory, fileName + ".blend")

            # print(saveFilePath)
            ################ Setup Camera
            bpy.context.scene.render.film_transparent = True

            # individual lights are not needed when using HDRI https://www.youtube.com/watch?v=Pi4Ft7M8UOU
            # bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            # sun = bpy.data.objects["Sun"]
            # sun.rotation_euler = Euler((numpy.deg2rad(30), 0, numpy.deg2rad(90)), 'XYZ') # set sunlight angle

            # bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            # sun2 = bpy.data.objects["Sun.001"]
            # sun2.rotation_euler = Euler((numpy.deg2rad(30), 0, numpy.deg2rad(-45)), 'XYZ') # set sunlight angle

            overhead_view_location = (10, 0, 10)
            overhead_view_rotation = (numpy.deg2rad(45), 0, numpy.deg2rad(90))
            
            # bpy.ops.object.camera_add(enter_editmode=False, align='VIEW')
            camera = bpy.data.objects["Camera"]
            bpy.context.scene.camera = camera
            camera.location = overhead_view_location
            camera.rotation_euler = Euler(overhead_view_rotation, 'XYZ')    
            bpy.context.scene.render.resolution_x = 1500
            bpy.context.scene.render.resolution_y = 1500

            ################ import stl file
            bpy.ops.import_mesh.stl(filepath=importFilePathComplete)

            bpy.context.object.name = fileName
            target = bpy.data.objects[fileName]

            # scale to inches
            target.scale = (scaleFactor, scaleFactor, scaleFactor)
            
            bpy.ops.object.select_all(action='DESELECT')
            target.select_set(True)
            bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
            
            
            ################ Setup Scene to render isometric image
            # Render iso image to use on button
            imageSaveFilePath = saveFilePath.replace(".blend",".png")

            # bpy.ops.object.select_by_type(type='MESH')
            # set object center to 0,0,0 so it will be centered in camera view
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            target.location = (0, 0, 0)

            ################ Get materials
            # mat1 = bpy.data.materials.get("concrete_wall_005")
            matDamagedMetal = bpy.data.materials.get("ProceduralDamagedMetal")
            matAsphalt = bpy.data.materials.get("ProceduralAsphalt")
            matCracks = bpy.data.materials.get("ProceduralCracks")
            matConcrete = bpy.data.materials.get("ProceduralConcreteSmooth")
            matSylized = bpy.data.materials.get("ProceduralSylized")
            matTiles = bpy.data.materials.get("floor_tiles_06")
            mat2 = bpy.data.materials.get("rock_boulder_dry")
            mat3 = bpy.data.materials.get("rusty_metal_02")
            mat4 = bpy.data.materials.get("rocks_ground_04")
            ApplyMaterial(matConcrete, target)
            

            # sun.parent = target
            # sun2.parent = target

            ################ set up reference objects

            plane = bpy.data.objects["Plane"]
            plane.parent = target

            # bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(3.5, 1, 0), scale=(1, 1, 1))
            # cube1 = bpy.data.objects["Cube"]
            # cube1.parent = target
            # ApplyMaterial(matSylized, cube1)

            # bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(-4, 1.5, 0), scale=(1, 1, 1))
            # cube2 = bpy.data.objects["Cube.001"]
            # cube2.rotation_euler = Euler((0, 0, numpy.deg2rad(45)), 'XYZ')  
            # cube2.parent = target
            # ApplyMaterial(matAsphalt, cube2)

            # bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-4, -1, 0), scale=(1, 1, 1))
            # sphere1 = bpy.data.objects["Sphere"]
            # sphere1.parent = target
            # ApplyMaterial(matAsphalt, sphere1)

            # bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-5, -1, 0), scale=(1, 1, 1))
            # sphere2 = bpy.data.objects["Sphere.001"]
            # sphere2.parent = target
            # ApplyMaterial(matCracks, sphere2)

            # bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-4.5, -1.25, 0), scale=(1, 1, 1))
            # sphere3 = bpy.data.objects["Sphere.002"]
            # sphere3.parent = target
            # ApplyMaterial(mat4, sphere3)
            

            ################ get overhead angles

            camera.location = overhead_view_location
            camera.rotation_euler = Euler(overhead_view_rotation, 'XYZ')  

            angles = numpy.linspace(0, 360, num_camera_angles, endpoint=False)
            pathNameBase = os.path.join(fileDirectory, fileName)
            pathNameBase += "_overhead"
            for angle in angles:
                RenderImage(target, angle, pathNameBase)

            ################# get sideview angles
            side_view_location = (16, 0, 8)
            side_view_rotation = (numpy.arctan(side_view_location[0]/side_view_location[2]), 0, numpy.deg2rad(90))

            camera.location = side_view_location
            camera.rotation_euler = Euler(side_view_rotation, 'XYZ')

            initial_angle = angles[1]/2
            angles = numpy.linspace(initial_angle, 360 + initial_angle, num_camera_angles, endpoint=False)
            pathNameBase = os.path.join(fileDirectory, fileName)
            pathNameBase += "_side"
            for angle in angles:
                RenderImage(target, angle, pathNameBase)

            #################### Deselect items in blend file
            # bpy.ops.object.select_all(action='DESELECT')

            # bpy.ops.object.select_by_type(type='CAMERA')

            # bpy.context.scene.render.filepath = imageSaveFilePath
            # bpy.context.scene.render.resolution_x = 1080 #perhaps set resolution in code
            # bpy.context.scene.render.resolution_y = 1080
            # bpy.ops.render.render(write_still = True)

            
            # ## Setup Scene to export to Unity
            # # bpy.ops.object.select_by_type(type='MESH')
            # # center bottom of object at origin
            # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            # bpy.context.object.location[0] = 0
            # bpy.context.object.location[1] = 0
            # bpy.context.object.location[2] = 0

            # new_cursor_z = -bpy.context.object.dimensions.z/2.0
            # # print(new_cursor_z)
            # # bpy.context.scene.cursor_location = Vector((0.0, 0.0, new_cursor_z))
            # bpy.context.scene.cursor.location = Vector((0.0,0.0,new_cursor_z))
            # bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
            # bpy.context.object.location[0] = 0
            # bpy.context.object.location[1] = 0
            # bpy.context.object.location[2] = 0

            # DeleteNonPrimaryObjects()

            # # Save the blend file in the Unity asset directory
            # bpy.ops.wm.save_as_mainfile(filepath=saveFilePath)

            # ## Clear Scene for next model
            # bpy.data.objects.remove(target, do_unlink=True)
            # bpy.data.objects.remove(cube, do_unlink=True)


'''
fileDirectoryName = "C:/Users/Brandon/Documents/3D Printing/_Terrain/Castle_Walls_4.1/"
fileName = "A-TRP-BrickWall-v4.0"
fileType = ".stl"
filePathComplete = fileDirectoryName + fileName + fileType
scaleFactor = 1/25.4 # convert mm to in

# bpy.ops.import_mesh.stl(filepath="/home/sam/KAPPA.stl", filter_glob="*.stl", files=[{"name":"KAPPA.stl", "name":"KAPPA.stl"}], directory="/home/sam/")

# import stl
bpy.ops.import_mesh.stl(filepath=filePathComplete)

# scale to inches
bpy.context.object.scale[0] = scaleFactor
bpy.context.object.scale[1] = scaleFactor
bpy.context.object.scale[2] = scaleFactor



# Save as blend file
saveFilePath = "C:/Users/Brandon/Documents/Unity3D_Games/Frostgrave/Assets/Models/" + fileName +".blend"
#bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=saveFilePath)

# delete object
bpy.ops.object.delete(use_global=False, confirm=False)
'''

# C:\Users\Brandon\Documents\3D Printing\_Terrain\Castle_Walls_4.1
# For python C:/Users/Brandon/Documents/3D Printing/_Terrain/Castle_Walls_4.1
