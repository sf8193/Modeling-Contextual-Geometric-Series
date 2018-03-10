import bpy
from random import random, uniform,randint
import mathutils
from mathutils import Vector
import math
import time

def createKernel(name, origin):
    bpy.ops.mesh.primitive_plane_add(
        radius = 0.7,
        location=origin, 
        rotation=(0, 0, 0))
            
    ob = bpy.context.object
    ob.name = name
    ob.show_name = True
    me = ob.data
    me.name = name+'Mesh'
    mat = bpy.data.materials.new("background")
    mat.diffuse_color = (1,1,1)

    ob.active_material = mat
    ob.scale = (0.33, 3, 0)
    
    return ob

def createCulture(name, origin):
    bpy.ops.mesh.primitive_plane_add(
        radius = 0.2,
        location=origin, 
        rotation=(0, 0, 0))
 
    ob = bpy.context.object
    ob.name = name
    ob.show_name = True
    me = ob.data
    me.name = name+'Mesh'
    mat = bpy.data.materials.new("some")
    mat.diffuse_color = (random(),random(),random())
    


    ob.active_material = mat
    ob.scale = (1.2, 0.2, 0)
    
    return ob
def createLamp(name,origin):
        
    lamp_data = bpy.data.lamps.new(name="lampa", type='POINT')  
    lamp_object = bpy.data.objects.new(name=name, object_data=lamp_data)  
    scene.objects.link(lamp_object)  
    lamp_object.location = origin
    return lamp_object

if __name__ == "__main__":
    scene = bpy.context.scene
    kernel = createKernel("kernel", (0,0,0))
    culture1 = createCulture("culture1",(0,0.2,0))
    culture2 = createCulture("culture2",(0,-0.3,0))
    lamp = createLamp("Lampika",(1,0,4))
    
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
    scene.objects.link(cam_ob)
    cam_ob.location = (0, 0, 3.5)  
    cam_ob.rotation_euler = (0,0,0)  
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = 10
    
    positions = []
    for i in range(500):
        y =uniform(-2.0,2.0)
        positions.append((0,y,0))

    number_of_frame = 0  
    t_end = time.time()+15
    while time.time() < t_end:
        
        scene.frame_set(number_of_frame)

        culture1.location = positions[randint(0,100)]
        culture2.location = positions[randint(0,100)]
        culture1.keyframe_insert(data_path="location")
        culture2.keyframe_insert(data_path="location")

        # move next 10 frames forward - Blender will figure out what to do between this time
        number_of_frame += 10
        
    bpy.context.space_data.font_size = 14
    bpy.ops.object.text_add(location=(-1,2.3,0))
    ob = bpy.context.object
    ob.data.body = "hot"
    
    bpy.ops.object.text_add(location=(-1,-3,0))
    ob = bpy.context.object
    ob.data.body = "cold"

#things to be done:
#add lines to 2 tuple
#create 3 tuple kernel
#re-structure into classes
