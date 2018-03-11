import bpy
from random import random, uniform,randint
import mathutils
from mathutils import Vector
import math
import time

def createKernel(name, origin,tuples):
    
    if(tuples==2):
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
    else:
        vert = [(0,0,0),(5,0,0),(2.5,5,0)]
        face = [(0,1,2)]
        edge = [(0,1),(1,2),(2,0)]
    
        my_mesh = bpy.data.meshes.new("Triangle")
        ob = bpy.data.objects.new("Triangle",my_mesh)
    
        ob.location = origin
        bpy.context.scene.objects.link(ob)
    
        my_mesh.from_pydata(vert,[],face)
        my_mesh.update(calc_edges=True)
    
    return ob

def createCulture(name, origin,tuples):
    
    if(tuples ==2):
        bpy.ops.mesh.primitive_plane_add(
            radius = 0.2,
            location=origin, 
            rotation=(0, 0, 0))
    else:
        bpy.ops.mesh.primitive_circle_add(
        radius = 0.2,
        location = (0,1,1),
        fill_type = "TRIFAN")

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

def createCamera(name,origin,tuples):  
    
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
    scene.objects.link(cam_ob)
    if(tuples==2):
        cam_ob.location = (0, 0, 3.5)  
    else:
        cam_ob.location = (2,2,3.5)
    
    cam_ob.rotation_euler = (0,0,0)  
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = 10
    
def get_slope(vertex1,vertex2):
    return (vertex2[1]-vertex1[1])/(vertex2[0]-vertex1[0])
    
def get_triangle_constraints(vertices):
    a = get_slope(vertices[0],vertices[2])
    b = get_slope(vertices[2],vertices[1])

    y = 100
    x = 1
    while y > a * x or y > (b*x)+ 10:
        y = uniform(0,5.0)
        x = uniform(0,5.0)
    
    print(x,y,0)
    return (x,y,0)

def create_text(tuples):
    if(tuples==2):
        bpy.ops.object.text_add(location=(-1,2.3,0))
        ob = bpy.context.object
        ob.data.body = "hot"
    
        bpy.ops.object.text_add(location=(-1,-3,0))
        ob = bpy.context.object
        ob.data.body = "cold"
    else:
        bpy.ops.object.text_add(location=(0,-1,0))
        ob = bpy.context.object
        ob.data.body = "cold"
        
        bpy.ops.object.text_add(location = (2.5,5,0))
        ob = bpy.context.object
        ob.data.body = "hot"
        
        bpy.ops.object.text_add(location = (5,-1,0))
        ob = bpy.context.object
        ob.data.body = "tbd"
    

if __name__ == "__main__":
    
    scene = bpy.context.scene
    tuples = 3
    kernel = createKernel("kernel", (0,0,0),tuples)
    culture1 = createCulture("culture1",(0,0.2,0),tuples)
    culture2 = createCulture("culture2",(0,-0.3,0),tuples)
    lamp = createLamp("Lampika",(1,0,4))
    cam = createCamera("Kamerka",(0,0,3.5),tuples)
    create_text(tuples)

    positions = []
    
    for i in range(200):
        if(tuples==2):
            y =uniform(-2.0,2.0)
            positions.append((0,y,0))
        else:
            positions.append(get_triangle_constraints(
                [(0,0,0),(5,0,0),(2.5,5,0)]))

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
        

#things to be done:
# add lines to two tuple
