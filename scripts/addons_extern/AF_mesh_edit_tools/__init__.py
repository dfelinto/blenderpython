# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# Contributed to by
# meta-androcto #

bl_info = {
    "name": "AF: Edit Tools",
    "author": "various",
    "version": (0, 1),
    "blender": (2, 76, 0),
    "location": "View3D > Toolshelf > Tools & Specials (W-key)",
    "description": "Add extra mesh edit tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Addon Factory"}



if "bpy" in locals():
    import importlib
    importlib.reload(face_inset_fillet)
    importlib.reload(mesh_filletplus)
    importlib.reload(mesh_vertex_chamfer)
    importlib.reload(mesh_mextrude_plus)
    importlib.reload(mesh_offset_edges)
    importlib.reload(pkhg_faces)
    importlib.reload(mesh_edge_roundifier)
    importlib.reload(mesh_cut_faces)
    importlib.reload(split_solidify)
    importlib.reload(mesh_to_wall)
    importlib.reload(mesh_edges_length)
    importlib.reload(random_vertices)
    importlib.reload(mesh_fastloop)

else:
    from . import face_inset_fillet
    from . import mesh_filletplus
    from . import mesh_vertex_chamfer
    from . import mesh_mextrude_plus
    from . import mesh_offset_edges
    from . import pkhg_faces
    from . import mesh_edge_roundifier
    from . import mesh_cut_faces
    from . import split_solidify
    from . import mesh_to_wall
    from . import mesh_edges_length
    from . import random_vertices
    from . import mesh_fastloop

import sys
import os
import shutil
import glob
import re
import bpy, blf, bgl
import bmesh
from bpy.props import StringProperty, FloatProperty, IntProperty, PointerProperty, BoolProperty
from bpy_extras.view3d_utils import region_2d_to_location_3d, location_3d_to_region_2d
from mathutils import Vector, Matrix
from math import degrees

### ------ PEN TOOL------ ###
def edit_mode_out():
    bpy.ops.object.mode_set(mode = 'OBJECT')

def edit_mode_in():
    bpy.ops.object.mode_set(mode = 'EDIT')

def get_direction_(bme, list_, ob_act):
    n = len(list_)
    for i in range(n):
        p = ob_act.matrix_world *(bme.verts[list_[i]].co).copy()
        p1 = ob_act.matrix_world *(bme.verts[list_[(i - 1) % n]].co).copy()
        p2 = ob_act.matrix_world *(bme.verts[list_[(i + 1) % n]].co).copy()
        ang = round(degrees((p - p1).angle((p - p2), any)))
        if ang == 0 or ang == 180:
            continue
        elif ang != 0 or ang != 180:
            return(((p - p1).cross((p - p2))).normalized())
            break

def align_view_to_face_(context, bme, f):
    ob_act = context.active_object
    list_e = [[v.index for v in e.verts] for e in f.edges][0]
    vec0 = -get_direction_(bme, [v.index for v in f.verts], ob_act)
    vec1 = ((ob_act.matrix_world * bme.verts[list_e[0]].co.copy()) - (ob_act.matrix_world * bme.verts[list_e[1]].co.copy())).normalized()
    vec2 = (vec0.cross(vec1)).normalized()
    context.space_data.region_3d.view_matrix = ((Matrix((vec1, vec2, vec0))).to_4x4()).inverted()
    context.space_data.region_3d.view_location = f.calc_center_median()

# ------ ------
def draw_callback_px(self, context):

    font_id = 0
    alpha = context.scene.pt_custom_props.a
    font_size = context.scene.pt_custom_props.fs

    bgl.glColor4f(0.0, 0.6, 1.0, alpha)
    bgl.glPointSize(4.0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(pt_buf.x, pt_buf.y)
    bgl.glEnd()
    bgl.glDisable(bgl.GL_BLEND)

    # -- -- -- -- location 3d
    if context.scene.pt_custom_props.b2 == True:
        mloc3d = region_2d_to_location_3d(context.region, context.space_data.region_3d, Vector((pt_buf.x, pt_buf.y)), pt_buf.depth_location)
        blf.position(font_id, pt_buf.x + 15, pt_buf.y - 15, 0)
        blf.size(font_id, font_size, context.user_preferences.system.dpi)
        blf.draw(font_id, '(' + str(round(mloc3d[0], 4)) + ', ' + str(round(mloc3d[1], 4)) + ', ' + str(round(mloc3d[2], 4)) + ')')

    n = len(pt_buf.list_m_loc_3d)
    if n != 0:

        # -- -- -- -- add points
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glPointSize(4.0)
        bgl.glBegin(bgl.GL_POINTS)
        for i in pt_buf.list_m_loc_3d:
            loc_0 = location_3d_to_region_2d(context.region, context.space_data.region_3d, i)
            bgl.glVertex2f(loc_0[0], loc_0[1])
        bgl.glEnd()
        bgl.glDisable(bgl.GL_BLEND)

        # -- -- -- -- text next to the mouse
        m_loc_3d = region_2d_to_location_3d(context.region, context.space_data.region_3d, Vector((pt_buf.x, pt_buf.y)), pt_buf.depth_location)
        vec0 = pt_buf.list_m_loc_3d[-1] - m_loc_3d
        blf.position(font_id, pt_buf.x + 15, pt_buf.y + 15, 0)
        blf.size(font_id, font_size, context.user_preferences.system.dpi)
        blf.draw(font_id, str(round(vec0.length, 4)))

        # -- -- -- -- angle first after mouse
        if n >= 2:
            vec1 = pt_buf.list_m_loc_3d[-2] - pt_buf.list_m_loc_3d[-1]
            if vec0.length == 0.0 or vec1.length == 0.0:
                pass
            else:
                ang = vec0.angle(vec1)

                if round(degrees(ang), 2) == 180.0:
                    text_0 = '0.0'
                elif round(degrees(ang), 2) == 0.0:
                    text_0 = '180.0'
                else:
                    text_0 = str(round(degrees(ang), 2))

                loc_4 = location_3d_to_region_2d(context.region, context.space_data.region_3d, pt_buf.list_m_loc_3d[-1])
                bgl.glColor4f(0.0, 1.0, 0.525, alpha)
                blf.position(font_id, loc_4[0] + 10, loc_4[1] + 10, 0)
                blf.size(font_id, font_size, context.user_preferences.system.dpi)
                blf.draw(font_id, text_0 + '')

        bgl.glLineStipple(4, 0x5555)
        bgl.glEnable(bgl.GL_LINE_STIPPLE)      # enable line stipple

        bgl.glColor4f(0.0, 0.6, 1.0, alpha)
        # -- -- -- -- draw line between last point and mouse
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_LINES)
        loc_1 = location_3d_to_region_2d(context.region, context.space_data.region_3d, pt_buf.list_m_loc_3d[-1])
        bgl.glVertex2f(loc_1[0], loc_1[1])
        bgl.glVertex2f(pt_buf.x, pt_buf.y)
        bgl.glEnd()
        bgl.glDisable(bgl.GL_BLEND)

        # -- -- -- -- draw lines between points
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for j in pt_buf.list_m_loc_3d:
            loc_2 = location_3d_to_region_2d(context.region, context.space_data.region_3d, j)
            bgl.glVertex2f(loc_2[0], loc_2[1])
        bgl.glEnd()
        bgl.glDisable(bgl.GL_BLEND)

        bgl.glDisable(bgl.GL_LINE_STIPPLE)      # disable line stipple

        # -- -- -- -- draw line length between points
        if context.scene.pt_custom_props.b1 == True:
            for k in range(n - 1):
                loc_3 = location_3d_to_region_2d(context.region, context.space_data.region_3d, (pt_buf.list_m_loc_3d[k] + pt_buf.list_m_loc_3d[(k + 1) % n]) * 0.5)
                blf.position(font_id, loc_3[0] + 10, loc_3[1] + 10, 0)
                blf.size(font_id, font_size, context.user_preferences.system.dpi)
                blf.draw(font_id, str(round((pt_buf.list_m_loc_3d[k] - pt_buf.list_m_loc_3d[(k + 1) % n]).length, 4)))

        # -- -- -- -- draw all angles
        if context.scene.pt_custom_props.b0 == True:
            for h in range(n - 1):
                if n >= 2:
                    if h == 0:
                        pass
                    else:
                        vec_ = pt_buf.list_m_loc_3d[h] - pt_buf.list_m_loc_3d[(h - 1) % n]
                        if vec_.length == 0.0:
                            pass
                        else:
                            ang = vec_.angle(pt_buf.list_m_loc_3d[h] - pt_buf.list_m_loc_3d[(h + 1) % n])
                            if round(degrees(ang)) == 0.0:
                                pass
                            else:
                                loc_4 = location_3d_to_region_2d(context.region, context.space_data.region_3d, pt_buf.list_m_loc_3d[h])
                                bgl.glColor4f(0.0, 1.0, 0.525, alpha)
                                blf.position(font_id, loc_4[0] + 10, loc_4[1] + 10, 0)
                                blf.size(font_id, font_size, context.user_preferences.system.dpi)
                                blf.draw(font_id, str(round(degrees(ang), 2)) + '')

    # -- -- -- -- tool on / off
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    blf.position(font_id, 150, 10, 0)
    blf.size(font_id, 20, context.user_preferences.system.dpi)
    blf.draw(font_id, 'Draw On')

# ------ ------
class pt_p_group0(bpy.types.PropertyGroup):
        a = FloatProperty( name = '', default = 1.0, min = 0.1, max = 1.0, step = 10, precision = 1 )
        fs = IntProperty( name = '', default = 14, min = 12, max = 40, step = 1 )
        b0 = BoolProperty( name = '', default = False )
        b1 = BoolProperty( name = '', default = False )
        b2 = BoolProperty( name = '', default = False )

# ------ ------
class pt_buf():
    list_m_loc_2d = []
    list_m_loc_3d = []
    x = 0
    y = 0
    sws = 'off'
    depth_location = Vector((0.0, 0.0, 0.0))
    alt = False
    shift = False

# ------ panel 0 ------
class pt_p0(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Pen Tool'
    bl_context = 'mesh_edit'
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        
        if pt_buf.sws == 'on':
            layout.active = False
            layout.label('Pen Tool On')
        else:
            layout.label('Font:')
            row = layout.split(0.50, align = True)
            row.prop(context.scene.pt_custom_props, 'fs', text = 'Size', slider = True)
            row.prop(context.scene.pt_custom_props, 'a', text = 'Alpha', slider = True)
            layout.prop(context.scene.pt_custom_props, 'b0', text = 'Angles')
            layout.prop(context.scene.pt_custom_props, 'b1', text = 'Edge Length')
            layout.prop(context.scene.pt_custom_props, 'b2', text = 'Mouse Location 3d')
            row1 = layout.split(0.80, align = True)
            row1.operator('pt.op0_id', text = 'Draw')
            row1.operator('pt.op1_id', text = '?')

# ------ operator 0 ------
class pt_op0(bpy.types.Operator):
    bl_idname = 'pt.op0_id'
    bl_label = 'Pen Tool'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod      # do not run in object mode
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def draw(self, context):
        layout = self.layout

    def execute(self, context):

        edit_mode_out()
        ob_act = context.active_object
        bme = bmesh.new()
        bme.from_mesh(ob_act.data)

        mtrx = ob_act.matrix_world.inverted()      # ob_act matrix world inverted

        # -- -- -- -- add vertices
        list_ = []
        for i in pt_buf.list_m_loc_3d:
            bme.verts.new(mtrx * i)
            bme.verts.index_update()
            bme.verts.ensure_lookup_table()
            list_.append(bme.verts[-1])

        # -- -- -- -- add edges
        n = len(list_)
        for j in range(n - 1):
            bme.edges.new((list_[j], list_[(j + 1) % n]))
            bme.edges.index_update()

        bme.to_mesh(ob_act.data)
        edit_mode_in()

        pt_buf.list_m_loc_2d[:] = []
        pt_buf.list_m_loc_3d[:] = []
        pt_buf.depth_location = Vector((0.0, 0.0, 0.0))
        return {'FINISHED'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type =='LEFT_ALT' or event.type == 'RIGHT_ALT':
            if event.value == 'PRESS': pt_buf.alt = True
            if event.value == 'RELEASE': pt_buf.alt = False
            return {'RUNNING_MODAL'}

        elif event.type =='LEFT_SHIFT' or event.type == 'RIGHT_SHIFT':
            if event.value == 'PRESS': pt_buf.shift = True
            if event.value == 'RELEASE': pt_buf.shift = False
            return {'RUNNING_MODAL'}

        elif event.type == 'MOUSEMOVE':
            if pt_buf.list_m_loc_2d != []:
                pt_buf_list_m_loc_3d_last_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, pt_buf.list_m_loc_3d[-1])

                if pt_buf.alt == True:
                    pt_buf.x = pt_buf_list_m_loc_3d_last_2d[0]
                    pt_buf.y = event.mouse_region_y
                elif pt_buf.shift == True:
                    pt_buf.x = event.mouse_region_x
                    pt_buf.y = pt_buf_list_m_loc_3d_last_2d[1]
                else:
                    pt_buf.x = event.mouse_region_x
                    pt_buf.y = event.mouse_region_y
            else:
                pt_buf.x = event.mouse_region_x
                pt_buf.y = event.mouse_region_y

        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                mouse_loc_2d = Vector((pt_buf.x, pt_buf.y))
                pt_buf.list_m_loc_2d.append(mouse_loc_2d)

                mouse_loc_3d = region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_loc_2d, pt_buf.depth_location)
                pt_buf.list_m_loc_3d.append(mouse_loc_3d)

                pt_buf.depth_location = pt_buf.list_m_loc_3d[-1]      # <----- depth location
            elif event.value == 'RELEASE':
                pass
        elif event.type == 'RIGHTMOUSE':
            context.space_data.draw_handler_remove(self._handle_px, 'WINDOW')
            self.execute(context)
            pt_buf.sws = 'off'
            return {'FINISHED'}
        elif event.type == 'ESC':
            context.space_data.draw_handler_remove(self._handle_px, 'WINDOW')
            pt_buf.list_m_loc_2d[:] = []
            pt_buf.list_m_loc_3d[:] = []
            pt_buf.depth_location = Vector((0.0, 0.0, 0.0))
            pt_buf.sws = 'off'
            return {'CANCELLED'}
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        bme = bmesh.from_edit_mesh(context.active_object.data)
        list_f = [f for f in bme.faces if f.select]

        if len(list_f) != 0:
            f = list_f[0]
            pt_buf.depth_location = f.calc_center_median()
            align_view_to_face_(context, bme, f)

        if context.area.type == 'VIEW_3D':
            if pt_buf.sws == 'on':
                return {'RUNNING_MODAL'}
            elif pt_buf.sws != 'on':
                context.window_manager.modal_handler_add(self)
                self._handle_px = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')
                pt_buf.sws = 'on'
                return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

# ------ operator 1 ------
class pt_op1(bpy.types.Operator):
    bl_idname = 'pt.op1_id'
    bl_label = '....'
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def draw(self, context):
        layout = self.layout
        layout.label('To use:')
        layout.label('Press D key or click Draw button.')
        layout.label('To draw along x use SHIFT + MOUSEMOVE')
        layout.label('To draw along y use ALT + MOUSEMOVE')
    
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width = 260)

# ------ operator 2 ------
class pt_op2(bpy.types.Operator):
    bl_idname = 'pt.op2_id'
    bl_label = '....'
    bl_options = {'INTERNAL'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.va.op1_id('INVOKE_DEFAULT')
        return {'FINISHED'}

# ------ ------
class_list = [ pt_p0, pt_op0, pt_op1, pt_op2, pt_p_group0 ]

### ------ MENUS ====== ###

class VIEW3D_MT_edit_mesh_extras(bpy.types.Menu):
    # Define the "Extras" menu
    bl_idname = "VIEW3D_MT_edit_mesh_extras"
    bl_label = "Edit Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        mode = context.tool_settings.mesh_select_mode
        if mode[0]: 	
            split = layout.split()		
            col = split.column()
            col.label(text="Vert")
            col.operator("mesh.vertex_chamfer",
                text="Vertex Chamfer")
            col.operator("mesh.random_vertices",
                text="Random Vertices")
            col.operator("pt.op0_id",
                text="Pen Tool")

            row = split.row(align=True)		
            col = split.column()
            col.label(text="Utilities")
            col.operator("object_ot.fastloop",
                text="Fast loop")
            col.operator('mesh.flip_normals', text = 'Normals Flip')
            col.operator('mesh.remove_doubles', text = 'Remove Doubles')

        elif mode[1]: 	
            split = layout.split()		
            col = split.column()
            col.label(text="Edge")
            col.operator("fillet.op0_id",
                text="Edge Fillet Plus")
            col.operator("mesh.offset_edges",
                text="Offset Edges")
            col.operator("mesh.edge_roundifier",
                text="Edge Roundify")
            col.operator("object.mesh_edge_length_set",
                text="Set Edge Length")
            col.operator("bpt.mesh_to_wall",
                text="Edge(s) to Wall")
				
            row = split.row(align=True)		
            col = split.column()
            col.label(text="Utilities")
            col.operator("object_ot.fastloop",
                text="Fast loop")
            col.operator('mesh.flip_normals', text = 'Normals Flip')
            col.operator('mesh.remove_doubles', text = 'Remove Doubles')

        elif mode[2]: 			
            split = layout.split()		
            col = split.column()
            col.label(text="Face")
            col.operator("object.mextrude",
                text="Multi Extrude")
            col.operator("faceinfillet.op0_id",
                text="Face Inset Fillet")
            col.operator("mesh.add_faces_to_object",
                text="PKHG Faces")
            col.operator("mesh.ext_cut_faces",
                text="Cut Faces")
            col.operator("sp_sol.op0_id",
                text="Split Solidify")

            row = split.row(align=True)		
            col = split.column()
            col.label(text="Utilities")
            col.operator("object_ot.fastloop",
                text="Fast loop")
            col.operator('mesh.flip_normals', text = 'Normals Flip')
            col.operator('mesh.remove_doubles', text = 'Remove Doubles')


class EditToolsSettings(bpy.types.PropertyGroup):


    vert_settings = BoolProperty(
        name="Vert",
        default=False)

    edge_settings = BoolProperty(
        name="Edge",
        default=False)

    face_settings = BoolProperty(
        name="Face",
        default=False)

    utils_settings = BoolProperty(
        name="Utils",
        default=False)


class EditToolsPanel(bpy.types.Panel):
    bl_label = 'Mesh Edit Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'mesh_edit'
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        wm = bpy.context.window_manager

        # Vert options
        box = layout.box()
        col = box.column(align=False)
        if wm.edit_tools_settings.vert_settings:
            file_icon = 'TRIA_DOWN'
        else:
            file_icon = 'TRIA_RIGHT'
        col.prop(wm.edit_tools_settings, "vert_settings",
                 icon=file_icon, toggle=True)
        if wm.edit_tools_settings.vert_settings:
            layout = self.layout
            row = layout.row()
            row.label(text="Vert Tools:", icon="VERTEXSEL")
            row = layout.split(0.70)
            row.operator('mesh.vertex_chamfer', text = 'Chamfer')
            row.operator('help.vertexchamfer', text = '?')
            row = layout.split(0.70)
            row.operator('mesh.random_vertices', text = 'Random Vertices')
            row.operator('help.random_vert', text = '?')
            row = layout.row()

        # Edge options
        box = layout.box()
        col = box.column(align=True)
        if wm.edit_tools_settings.edge_settings:
            modifier_icon = 'TRIA_DOWN'
        else:
            modifier_icon = 'TRIA_RIGHT'
        col.prop(wm.edit_tools_settings, "edge_settings",
                 icon=modifier_icon, toggle=True)
        if wm.edit_tools_settings.edge_settings:
            layout = self.layout
            row = layout.row()
            row.label(text="Edge Tools:", icon="EDGESEL")
            row = layout.split(0.70)
            row.operator('fillet.op0_id', text = 'Fillet plus')
            row.operator('help.edge_fillet', text = '?')
            row = layout.split(0.70)
            row.operator('mesh.offset_edges', text = 'Offset Edges')
            row.operator('help.offset_edges', text = '?')
            row = layout.split(0.70)
            row.operator('mesh.edge_roundifier', text = 'Roundify')
            row.operator('help.roundify', text = '?')
            row = layout.split(0.70)
            row.operator('object.mesh_edge_length_set', text = 'Set Edge Length')
            row.operator('help.roundify', text = '?')
            row = layout.split(0.70)
            row.operator('bpt.mesh_to_wall', text = 'Mesh to wall')
            row.operator('help.wall', text = '?')
            row = layout.row()

        # Face options
        box = layout.box()
        col = box.column(align=True)
        if wm.edit_tools_settings.face_settings:
            object_icon = 'TRIA_DOWN'
        else:
            object_icon = 'TRIA_RIGHT'
        col.prop(wm.edit_tools_settings, "face_settings",
                 icon=object_icon, toggle=True)
        if wm.edit_tools_settings.face_settings:
            layout = self.layout
            row = layout.row()
            row.label(text="Face Tools:", icon="FACESEL")
            row = layout.split(0.70)
            row.operator('object.mextrude', text = 'Multi Extrude')
            row.operator('help.mextrude', text = '?')
            row = layout.split(0.70)
            row.operator('faceinfillet.op0_id', text = 'Inset Fillet')
            row.operator('help.face_inset', text = '?')
            row = layout.split(0.70)
            row.operator('mesh.add_faces_to_object', text = 'Face Extrude')
            row.operator('help.pkhg', text = '?')
            row = layout.split(0.70)
            row.operator('mesh.ext_cut_faces', text = 'Cut Faces')
            row.operator('help.cut_faces', text = '?')
            row = layout.split(0.70)
            row.operator('sp_sol.op0_id', text = 'Split Solidify')
            row.operator('help.solidify', text = '?')
            row = layout.row()

        # Utils options
        box = layout.box()
        col = box.column(align=True)
        if wm.edit_tools_settings.utils_settings:
            rename_icon = 'TRIA_DOWN'
        else:
            rename_icon = 'TRIA_RIGHT'
        col.prop(wm.edit_tools_settings, "utils_settings",
                 icon=rename_icon, toggle=True)
        if wm.edit_tools_settings.utils_settings:
            layout = self.layout
            row = layout.row()
            row.label(text="Utilities:")
            row = layout.row()
            row = layout.split(0.70)
            row.operator('object_ot.fastloop', text = 'Fast Loop')
            row.operator('help.random_vert', text = '?')
            row = layout.row()
            row.operator('mesh.flip_normals', text = 'Normals Flip')
            row = layout.row()
            row.operator('mesh.remove_doubles', text = 'Remove Doubles')

# Addons Preferences
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	def draw(self, context):
		layout = self.layout
		layout.label(text="----Mesh Edit Tools----")
		layout.label(text="Collection of extra Mesh Edit Functions")
		layout.label(text="Edit Mode toolshelf or W key specials")

# Define "Extras" menu
def menu_func(self, context):
    self.layout.menu('VIEW3D_MT_edit_mesh_extras', icon='PLUGIN')

def register():


    for c in class_list:
        bpy.utils.register_class(c)
    bpy.utils.register_module(__name__)
    wm = bpy.context.window_manager
    bpy.types.WindowManager.edit_tools_settings = bpy.props.PointerProperty(type=EditToolsSettings)
    bpy.types.Scene.pt_custom_props = PointerProperty(type = pt_p_group0)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('pt.op0_id', 'D', 'PRESS')


    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)


def unregister():
    for c in class_list:
        bpy.utils.unregister_class(c)

    if 'pt_custom_props' in bpy.context.scene:
        del bpy.context.scene['pt_custom_props']

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['3D View']
    for kmi in km.keymap_items:
        if kmi.idname == 'pt.op0_id':
            km.keymap_items.remove(kmi)
            break

    bpy.utils.unregister_module(__name__)

    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)

    del bpy.types.WindowManager.edit_tools_settings

if __name__ == "__main__":
    register()
