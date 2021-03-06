#
# Copyright 2011-2013 Blender Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# XML exporter for generating test files, not intended for end users

__license__ = "GPL"

bl_info = {
    "name": "Cycles exporter",
    'blender': (2, 7, 4),
    "description": "export scenes as cycles (xml)",
    "category": "Import-Export",
    "location": "File > Export" }

import os
import xml.etree.ElementTree as etree
import xml.dom.minidom as dom

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import PointerProperty, StringProperty
import math
from mathutils import Matrix

def strip(root):
    root.text = None
    root.tail = None

    for elem in root:
        strip(elem)

def write(node, fname):
    strip(node)

    s = etree.tostring(node)
    s = dom.parseString(s).toprettyxml()

    f = open(fname, "w")
    f.write(s)
    
class CyclesXMLSettings(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.cycles_xml = PointerProperty(
                                        type=cls,
                                        name="Cycles XML export Settings",
                                        description="Cycles XML export settings")
        cls.filepath = StringProperty(
                        name='Filepath',
                        description='Filepath for the .xml file',
                        maxlen=256,
                        default='',
                        subtype='FILE_PATH')
                        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.cycles_xml
        
# User Interface Drawing Code
class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(self, context):
        rd = context.scene.render
        return rd.engine == 'CYCLES'


class PHYSICS_PT_fluid_export(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Cycles XML Exporter"

    def draw(self, context):
        layout = self.layout
        
        cycles = context.scene.cycles_xml
        
        #layout.prop(cycles, "filepath")
        layout.operator("export_mesh.cycles_xml")

def matrix_to_str(m):
    m = m.transposed()
    return " ".join([str(i) for v in m for i in v])

def output_camera(scene, node):
    x_res = (scene.render.resolution_x * scene.render.resolution_percentage) / 100
    y_res = (scene.render.resolution_y * scene.render.resolution_percentage) / 100

    etree.SubElement(node, 'camera', attrib={
        'width': str(int(x_res)),
        'height': str(int(y_res))})

    cam_matrix = scene.camera.matrix_world  * Matrix.Scale(-1, 4, (0,0,1))

    trans = etree.SubElement(node, 'transform', attrib={
        'matrix': matrix_to_str(cam_matrix) })
    etree.SubElement(trans, 'camera', attrib={
        'type': 'perspective',
        'fov': str((bpy.context.scene.camera.data.angle ) / math.pi * 180) })

def output_background(world, node):
    if not world.node_tree == None:
        print("FIX ME We do not support node trees for world and will continue like nothing happened")

    bg = etree.SubElement(node, 'background')
    etree.SubElement(bg, 'background', attrib={
    'name': 'bg', 'strength': '1.0', 'color': " ".join([str(x) for x in world.horizon_color])})
    etree.SubElement(bg, 'connect', attrib={
    'from': "bg background", 'to': "output surface" })


# Export Operator
class ExportCyclesXML(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.cycles_xml"
    bl_label = "Export Cycles XML"

    filename_ext = ".xml"


    def execute(self, context):
        filepath = bpy.path.ensure_ext(self.filepath, ".xml")

        cycles_node = etree.Element('cycles')

        # get mesh
        scene = context.scene

        output_camera(scene, cycles_node)
        output_background(scene.world, cycles_node)

        shader = etree.SubElement(cycles_node, 'shader', attrib={
            'name': 'diff'})

        etree.SubElement(shader, 'diffuse_bsdf', attrib={
            'name': 'cube_closure',
            'roughness': "0.2"})
        etree.SubElement(shader, 'connect', attrib={
            'from': "cube_closure bsdf",
            'to': "output surface"
        })

        for object in (ob for ob in scene.objects if ob.is_visible(scene)):
            if object.type == 'LAMP':

                shader = etree.SubElement(cycles_node, 'shader', attrib={
                    'name': 'point_shader'})

                etree.SubElement(shader, 'emission', attrib={
                    'name': 'emission',
                    'color': '1.0 1.0 1.0',
                    'strength': '100.0'})

                etree.SubElement(shader, 'connect', attrib={
                    'from': 'emission emission',
                    'to': 'output surface'
                })

                trans = etree.SubElement(cycles_node, 'transform', attrib={
            'matrix':  matrix_to_str(object.matrix_world )})

                shader_state = etree.SubElement(trans, "state", attrib={
                    'shader': 'point_shader'})




                etree.SubElement(shader_state, 'light', attrib={
                    'type': '0',
                    'cast_shadow': 'true',
                    'size': '0.01'})

            try:
                mesh = object.to_mesh(scene, True, 'PREVIEW')
            except RuntimeError as e:
                continue

            if not mesh:
                continue
            print("exporting ", object.name)
            # generate mesh node
            nverts = ""
            verts = ""
            uvs = ""
            P = ""


            for v in mesh.vertices:
                P += "%f %f %f  " % (v.co[0], v.co[1], v.co[2])

            if mesh.tessface_uv_textures.active_index > -1:
                verts_and_uvs = zip(mesh.tessfaces, mesh.tessface_uv_textures.active.data)

                for f, uvf in verts_and_uvs:
                    vcount = len(f.vertices)
                    nverts += str(vcount) + " "

                    for v in f.vertices:
                        verts += str(v) + " "

                    uvs += str(uvf.uv1[0]) + " " + str(uvf.uv1[1]) + " "
                    uvs += str(uvf.uv2[0]) + " " + str(uvf.uv2[1]) + " "
                    uvs += str(uvf.uv3[0]) + " " + str(uvf.uv3[1]) + " "
                    if vcount==4:
                        uvs += " " + str(uvf.uv4[0]) + " " + str(uvf.uv4[1]) + " "

                trans = etree.SubElement(cycles_node, 'transform', attrib={
                        'matrix': matrix_to_str(object.matrix_world) })
                state = etree.SubElement(trans, 'state', attrib={"shader": "diff"})
                etree.SubElement(state, 'mesh', attrib={'nverts': nverts.strip(),
                                                     'name': object.name,
                                                     'verts': verts.strip(),
                                                     'P': P,
                                                     'UV' : uvs.strip()})

            else:
                for f in mesh.tessfaces:
                    vcount = len(f.vertices)
                    nverts += str(vcount) + " "

                    for v in f.vertices:
                        verts += str(v) + " "

                trans = etree.SubElement(cycles_node, 'transform', attrib={
                        'matrix': matrix_to_str(object.matrix_world) })
                state = etree.SubElement(trans, 'state', attrib={"shader": "diff"})
                etree.SubElement(state, 'mesh', attrib={'nverts': nverts.strip(),
                                                     'name': object.name,
                                                     'verts': verts.strip(),
                                                     'P': P})

        # write to file
        write(cycles_node, filepath)
        print(etree.dump(cycles_node))

        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportCyclesXML.bl_idname, text="Export Cycles Scene(.xml)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()