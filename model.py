import bpy
from random import random, uniform,randint
import mathutils
from mathutils import Vector
import math
import time
        
class graphics_factory(object):
    
    # this method creates everything to be displayed
    # meant as abstraction layer between user and creation of objects
    @staticmethod
    def create(tuples):
        
        if(tuples == 2):
            shape = "Rectangle"   
        
        elif(tuples==3):
            shape = "Triangle"
        
        lamp = graphics_factory.create_lamp("Lampika",shape)
        cam = graphics_factory.create_camera("Kamerka",shape)
        kernel = graphics_factory.create_kernel("kernel",0.7,shape)
        culture1 = graphics_factory.create_culture("culture_1",(0,0.2,0),shape)
        culture2 = graphics_factory.create_culture("culture_2",(0,-0.3,0),shape)
        graphics_factory.create_text(shape)
        
        return lamp,cam,kernel,culture1,culture2
        
    #creates cultures
    @staticmethod
    def create_culture(name,origin,shape):
        
        if(shape=="Rectangle"):
            make_rectangle(0.2,origin)
        elif(shape=="Triangle"):
            make_circle(0.2,origin)
     
        culture = bpy.context.object
        culture.name = name
        culture.show_name = True
        data = culture.data
        data.name = name+'Mesh'
        mat = bpy.data.materials.new("some")
        #randomizes colors
        mat.diffuse_color = (random(),random(),random())
        

        culture.active_material = mat
        culture.scale = (1.2, 0.2, 0)
        
        return culture

    @staticmethod
    def create_camera(name,shape):
        
        cam_data = bpy.data.cameras.new(name="cam")  
        cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
        scene.objects.link(cam_ob)
        cam_ob.rotation_euler = (0,0,0)  
        cam = bpy.data.cameras[cam_data.name]  
        cam.lens = 10
        #camera changes depending on tuples, do we want more than one camera?
        if(shape=="Rectangle"):
            cam_ob.location = (0,0,3.5)
        elif(shape=="Triangle"):
            cam_ob.location = (2,3,4.5)

        return cam_ob
    @staticmethod
    def create_lamp(name,shape):
        data = bpy.data.lamps.new(name="lampa", type='POINT')  
        lamp = bpy.data.objects.new(name=name, object_data=data)  
        scene.objects.link(lamp)
        if(shape=="Rectangle"):
            lamp.location = (1,0,4.5)
        elif(shape=="Triangle"):
            lamp.location = (4,5,4.5)
        return lamp

    @staticmethod
    def create_kernel(name,radius,shape):
        origin = (0,0,0)
        if(shape=="Rectangle"):
            print("here")
            make_rectangle(radius,origin)
            kernel = bpy.context.object
            kernel.scale = (0.33, 3, 0)
        if(shape=="Triangle"):
            kernel = make_triangle(origin)
            

        kernel.name = name
        kernel.show_name = True
        data = kernel.data
        data.name = name+'Mesh'
        mat = bpy.data.materials.new("kernel_color")
        mat.diffuse_color = (1,1,1)
        kernel.active_material = mat

        
        return kernel
    
    @staticmethod
    def create_text(shape):
        if(shape=="Rectangle"):
            bpy.ops.object.text_add(location=(-1,2.3,0))
            ob = bpy.context.object
            ob.data.body = "hot"
        
            bpy.ops.object.text_add(location=(-1,-3,0))
            ob = bpy.context.object
            ob.data.body = "cold"
        elif(shape=="Triangle"):
            bpy.ops.object.text_add(location=(0,-1,0))
            ob = bpy.context.object
            ob.data.body = "cold"
            
            bpy.ops.object.text_add(location = (2.5,5,0))
            ob = bpy.context.object
            ob.data.body = "hot"
            
            bpy.ops.object.text_add(location = (5,-1,0))
            ob = bpy.context.object
            ob.data.body = "tbd"

def make_rectangle(radius,origin):
        bpy.ops.mesh.primitive_plane_add(
        radius = radius,
        location= origin, 
        rotation=(0, 0, 0))
        
def make_circle(radius,origin):
    bpy.ops.mesh.primitive_circle_add(
        radius = radius,
        location = (0,1,1),
        fill_type = "TRIFAN")

def make_triangle(origin):
                
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

    return (x,y,0)
        

if __name__=="__main__":
    
    scene = bpy.context.scene
    # change this to see 3 or 2 tuple demo
    tuples = 3
    lamp, cam, kernel, culture1, culture2 = graphics_factory.create(tuples)
    
    positions = []
    
    # random points for modeling purposes, this will change to data later
    for i in range(200):
        if(tuples==2):
            y = uniform(-2.0,2.0)
            positions.append((0,y,0))
        else:
            positions.append(get_triangle_constraints(
                [(0,0,0),(5,0,0),(2.5,5,0)]))

    number_of_frame = 0  
    t_end = time.time()+15
    # makes cultures move around
    while time.time() < t_end:
        
        scene.frame_set(number_of_frame)

        culture1.location = positions[randint(0,100)]
        culture2.location = positions[randint(0,100)]
        culture1.keyframe_insert(data_path="location")
        culture2.keyframe_insert(data_path="location")

        # move next 10 frames forward - Blender will figure out what to do between this time
        number_of_frame += 10
