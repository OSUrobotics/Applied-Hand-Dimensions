

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


class GraspRegion():

    def __init__(self, json_file) -> None:
        
        self.material_list = [self.new_material("Red", (1,0,0,0.5)),
                     self.new_material("Green", (0,1,0,0.5)),
                     self.new_material("Blue", (0,0,1,0.5)),
                     self.new_material("White", (1,1,1,0.5)),
                     self.new_material("Black", (0,0,0,0.5)),
                     self.new_material("yellow", (1,1,0,0.5))]

        # self.material_list = []
        # for i in range(6):
        #     self.material_list.append(self.new_material(materials[i][0], materials[i][1]))

        print(f"\n\n\n {self.material_list} \n\n\n")
        self.delete_all()
        self.current_loc = os.getcwd()
        json_file_loc = f'{self.current_loc}/{json_file}'
        grasp_region_dict = self.read_json(json_file=json_file_loc)
        gripper_name = grasp_region_dict["gripper_name"]
        self.mesh_loc = f'{self.current_loc}/{gripper_name}'
        self.directory_maker(self.mesh_loc)

        self.main(grasp_region_dict)

    def new_material(self, name, color=(1,1,1,1)):

        material = bpy.data.materials.new(name=name)
        material.diffuse_color = color
        return material


    def main(self, grasp_region_dict):
        
        if grasp_region_dict["grasp_style"] == "cylindrical":
            self.cylindrical_grasp(grasp_region_dict=grasp_region_dict)
        elif grasp_region_dict["grasp_style"] == "spherical":
            pass
        else:
            raise ValueError("incorrect grasp_style enter either cylindrical or spherical")
    
    def cylindrical_grasp(self, grasp_region_dict):
        
        power_keys = grasp_region_dict["power"].keys()
        power_keys -= ["width"]

        for key in power_keys:
            verts, faces, face_number = self.cylindrical_power(grasp_region_dict["power"][key], grasp_region_dict["power"]["width"][1])
            print("making mesh")
            self.blender_make_mesh(verts, faces, f'{grasp_region_dict["gripper_name"]}_power_{key}')
            self.blender_color_mesh(face_number=face_number, mesh_name=f'{grasp_region_dict["gripper_name"]}_power_{key}')
            self.export_part(f'{grasp_region_dict["gripper_name"]}_power_{key}', self.mesh_loc)
            self.delete_all()
        precision_keys = grasp_region_dict["precision"].keys()
        precision_keys -= ["width", "abs_max"]
        for prec_key in precision_keys:
            verts, faces, face_number = self.cylindrical_power(grasp_region_dict["precision"][prec_key], grasp_region_dict["precision"]["width"][1])
            self.blender_make_mesh(verts, faces, f'{grasp_region_dict["gripper_name"]}_precision_{prec_key}')

            self.blender_color_mesh(face_number, mesh_name=f'{grasp_region_dict["gripper_name"]}_precision_{prec_key}')

            self.export_part(f'{grasp_region_dict["gripper_name"]}_precision_{prec_key}', self.mesh_loc)
            self.delete_all()

    def blender_color_mesh(self, face_number, mesh_name):
        
        mesh = data.objects[mesh_name]
        for material in self.material_list:
            mesh.data.materials.append(material)
        
        mesh.data.polygons[face_number["top"]].material_index = 3
        mesh.data.polygons[face_number["bottom"]].material_index = 3
        mesh.data.polygons[face_number["back"]].material_index = 3

        side_faces = len(face_number["sides"]) // 2
        for side_number in range(3, 3+side_faces):
            mesh.data.polygons[side_number].material_index = 0
        
        if len(face_number["sides"]) % 2 == 0:
            for side_number in range(3+side_faces, 3 + side_faces*2):
                mesh.data.polygons[side_number].material_index = 2
        else:
            mesh.data.polygons[3+side_faces].material_index = 3
            for side_number in range(3+side_faces + 1, 3+side_faces*2 + 1):
                mesh.data.polygons[side_number].material_index = 2


    def cylindrical_power(self, point_list, height):
        top_pos = []
        top_neg = []
        bottom_pos = []
        bottom_neg = []
        verts = []
        face_number = {}
        for point in point_list:
            if point[0] == 0.0:
                span = point[0]
                bottom_pos.append((span, point[1], 0))
                top_pos.append((span, point[1], height))
            else:
                span = point[0] / 2
                bottom_pos.append((span, point[1], 0))
                bottom_neg.insert(0,(-1*span, point[1], 0))
                top_pos.append((span, point[1], height))
                top_neg.insert(0, (-1*span, point[1], height))
        verts += bottom_pos
        verts += bottom_neg
        top_position = len(verts)
        verts += top_pos
        verts += top_neg

        # faces = []
        # print(f'top_position: {top_position}, len of verts: {len(verts)}')
        faces = [(range(top_position-1, -1, -1))]
        face_number["top"] = 0
        faces.append((range(top_position, len(verts))))
        face_number["bottom"] = 1
        faces.append((0, top_position, len(verts)-1, top_position-1))
        face_number["back"] = 2
        for i in range(top_position - 1):
            faces.append((i, i + 1, i + 1 + top_position, i + top_position))
        
        face_number["sides"] =  list(range(3,len(faces)))
        
        return verts, faces, face_number

    def delete_all(self):
        """Delete all objects in the blender enviroment."""
        bpy.ops.object.select_all(action='SELECT')  #deletes everything
        bpy.ops.object.delete(use_global=False)

    def blender_make_mesh(self, verts, faces, mesh_name):
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

    def export_part(self, name, export_directory):
        """Export the object as an obj file.

        Arg: 
            name (str): The absolute path including the name of file object you wish to export.
        """
        name += '.obj'
        target_file = os.path.join(export_directory, name)
        bpy.ops.export_scene.obj(filepath=target_file, use_triangles=True, use_materials=True, path_mode='COPY', axis_forward="Y", axis_up='Z')

    def directory_maker(self, location):
        """Create a new directory.

        Args:
            location (str): path to new directory that needs to be made.
        """
        if not os.path.isdir(location):
            Path(location).mkdir(parents=True, exist_ok=True)

    def read_json(self, json_file) -> dict:
        """Read a given json file in as a dictionary.

        Args:
            json_loc (str): path to the json file to be read in

        Returns:
            (dictionary): A dictionary of the json that was read in
        """
        with open(json_file, "r") as read_file:
            dictionary = json.load(read_file)
        return dictionary


if __name__ == '__main__':

    json_file_name = sys.argv[-1]

    GraspRegion(json_file=json_file_name)