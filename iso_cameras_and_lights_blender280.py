# import bpy
'''
To run in Blender python console

filename = "C:/Users/Brandon/Desktop/blender_sprite_maker-master/iso_cameras_and_lights_blender280.py"

filename = "C:/Users/Brandon/Documents/Unity3D_Games/Frostgrave/Assets/Models/blender/iso_cameras_and_lights_blender280.py"

exec(compile(open(filename).read(), filename, 'exec'))

'''

#  delete Collection to fix importing into unity
# bpy.ops.outliner.collection_delete(hierarchy=False)

# x_locs = [-3, 0, 3]
# y_locs = [-3, 0, 3]
x_locs = [-3]
y_locs = [-3]
z = 3


bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))

# bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

bpy.context.scene.render.film_transparent = True

for x in x_locs:
    for y in y_locs:
        if (not (x==0 and y == 0)):
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))

            # bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            bpy.ops.object.constraint_add(type='TRACK_TO')
            bpy.context.object.constraints["Track To"].target = bpy.data.objects["Empty"]
            bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
            bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'

            # create lamp (looks better than sun)
            bpy.ops.object.light_add(type='POINT', location=(-2.8, -1.3, 5.9))


            # bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(x, y, z), rotation=(1.0247, 0.00937975, 0.717466), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x, y, z), rotation=(1.10871, 0.0132652, 1.14827))

            bpy.context.object.data.type = 'ORTHO'
            bpy.ops.object.constraint_add(type='TRACK_TO')
            bpy.context.object.constraints["Track To"].target = bpy.data.objects["Empty"]
            bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
            bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
            bpy.context.scene.render.resolution_x = 1080
            bpy.context.scene.render.resolution_y = 1080



# bpy.data.objects["Sun.005"].hide_render = False
