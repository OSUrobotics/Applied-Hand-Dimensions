
from bpy import data, context
import bpy
import mathutils
from mathutils import Matrix, Vector
import bmesh
import numpy as np
import os
from pathlib import Path
import sys
import json
from math import sin, cos, tan, pi


def create_material(mat_name, diffuse_color=(1,1,1,1)): 

    # from https://blender.stackexchange.com/questions/240866/how-to-assign-a-material-to-a-single-face-of-a-mesh-using-python-api
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = diffuse_color
    return mat


def delete_all():
    """Delete all objects in the blender enviroment."""
    bpy.ops.object.select_all(action='SELECT')  #deletes everything
    bpy.ops.object.delete(use_global=False)


def blender_make_mesh(verts, faces, mesh_name):
    """Create the meshs using blenders tools.

    Args:
        verts (list): list of tuples, each tuple represents a vertex(x,y,z). 
        faces (list): list of tuples, each tuple represents a face and contains the index of the vertices used for a face. Follows right hand rule to get face normal.
        mesh_name (str): The name of the new mesh, make sure it is unique else blender will add .001 to the end if the name already exists.
    """
    edges = [] # Only need edges or faces, we are using faces
    mesh_data = data.meshes.new(mesh_name)
    mesh_data.from_pydata(verts,edges,faces)
    bm = bmesh.new()
    bm.from_mesh(mesh_data)
    bm.to_mesh(mesh_data)
    bm.free()
    mesh_obj = data.objects.new(mesh_data.name, mesh_data)
    context.collection.objects.link(mesh_obj)


if __name__ == '__main__':
    
    number = 9

    delete_all()

    

    verts = [Vector((1, 1, 1)), #0
             Vector((0, 1, 1)), #1
             Vector((0, 0, 1)), #2
             Vector((1, 0, 1)), #3
             Vector((1, 1, 0)), #4
             Vector((1, 0, 0)), #5
             Vector((0, 0, 0)), #6
             Vector((0, 1, 0))] #7

    faces = [(0, 1, 2, 3),
             (4, 5, 6, 7),
             (0, 4, 7, 1),
             (0, 3, 5, 4),
             (6, 5, 3, 2),
             (6, 2, 1, 7)]
    

    mesh_name = f"test_cube{number}"
    edges = [] # Only need edges or faces, we are using faces
    mesh_data = data.meshes.new(mesh_name)
    mesh_data.from_pydata(verts,edges,faces)
    
    bm = bmesh.new()
    bm.from_mesh(mesh_data)
    bm.to_mesh(mesh_data)


    bm.free()
    mesh_obj = data.objects.new(mesh_data.name, mesh_data)
    context.collection.objects.link(mesh_obj)
    
    mat_red = create_material("Red", (1,0,0,1))
    mat_green = create_material("Green", (0,1,0,1))
    mat_blue = create_material("Blue", (0,0,1,1))
    mat_white = create_material("White", (1,1,1,1))
    mat_black = create_material("Black", (0,0,0,1))
    mat_yellow = create_material("yellow", (1,1,0,1))
    
    
    cube_mesh = data.objects[f"test_cube{number}"]
    
#    cube_mesh = bpy.context.object
    
    cube_mesh.data.materials.append(mat_red)
    cube_mesh.data.materials.append(mat_green)
    cube_mesh.data.materials.append(mat_blue)
    cube_mesh.data.materials.append(mat_white)
    cube_mesh.data.materials.append(mat_black)
    cube_mesh.data.materials.append(mat_yellow)
    
    for face in range(len(cube_mesh.data.polygons)):
        cube_mesh.data.polygons[face].material_index = face