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
# Pontiac, Fourmadmen, varkenvarken, tuga3d, meta-androcto, metalliandy, dreampainter, cotejrp1 #
# liero, Kayo Phoenix, sugiany, dommetysk, Phymec, Anthony D'Agostino, Pablo Vazquez, Richard Wilks #
# xyz presets by elfnor

from .add_mesh_icicle_snowflake import add_mesh_icicle_gen
from .add_mesh_icicle_snowflake import add_mesh_snowflake
from .add_mesh_siding_wall import add_mesh_drystone
from .add_mesh_siding_wall import add_mesh_floor_planks
from .add_mesh_siding_wall import add_mesh_plancher
from .add_mesh_siding_wall import add_mesh_siding
from .add_ant_erosion import erode
from .add_ant_erosion import erosion
from .add_bound_box import bound_box
from .add_mesh_building_objects import build
from .add_mesh_rocks import rock_generator
from .bookGen import __init__
from .bookGen import utils
from .add_mesh_castle import __init__
from .add_mesh_castle import Castle

bl_info = {
    "name": "AF: Mesh Objects",
    "author": "Multiple Authors",
    "version": (0, 4, 9),
    "blender": (2, 7, 6),
    "location": "View3D > Add > Mesh",
    "description": "Add extra mesh object types",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Add_Extra",
    "category": "Addon Factory",
}

if "bpy" in locals():
    import importlib
    importlib.reload(add_mesh_star)
    importlib.reload(add_mesh_twisted_torus)
    importlib.reload(add_mesh_gemstones)
    importlib.reload(add_mesh_gears)
    importlib.reload(add_mesh_3d_function_surface)
    importlib.reload(add_mesh_round_cube)
    importlib.reload(add_mesh_supertoroid)
    importlib.reload(add_mesh_pyramid)
    importlib.reload(add_mesh_torusknot)
    importlib.reload(add_mesh_honeycomb)
    importlib.reload(add_mesh_teapot)
    importlib.reload(add_mesh_pipe_joint)
    importlib.reload(add_mesh_solid)
    importlib.reload(add_mesh_round_brilliant)
    importlib.reload(add_mesh_menger_sponge)
    importlib.reload(add_mesh_vertex)
    importlib.reload(add_empty_as_parent)
    importlib.reload(add_mesh_ant_landscape_modified)
    importlib.reload(add_mesh_cave_gen)
    importlib.reload(add_mesh_lowpoly_rock)
    importlib.reload(fractalDome)
    importlib.reload(Boltfactory)
    importlib.reload(terrain_gen)
    importlib.reload(add_dual_mesh)
    importlib.reload(add_mesh_grating)
    importlib.reload(add_mesh_propeller)
    importlib.reload(basket_arch)
    importlib.reload(add_mesh_curved_plane)
    importlib.reload(add_mesh_beam_builder)

else:
    from . import add_mesh_star
    from . import add_mesh_twisted_torus
    from . import add_mesh_gemstones
    from . import add_mesh_gears
    from . import add_mesh_3d_function_surface
    from . import add_mesh_round_cube
    from . import add_mesh_supertoroid
    from . import add_mesh_pyramid
    from . import add_mesh_torusknot
    from . import add_mesh_honeycomb
    from . import add_mesh_teapot
    from . import add_mesh_pipe_joint
    from . import add_mesh_solid
    from . import add_mesh_round_brilliant
    from . import add_mesh_menger_sponge
    from . import add_mesh_vertex
    from . import add_empty_as_parent
    from . import add_mesh_ant_landscape_modified
    from . import add_mesh_cave_gen
    from . import add_mesh_lowpoly_rock
    from . import fractalDome
    from . import Boltfactory
    from . import terrain_gen
    from . import add_dual_mesh
    from . import add_mesh_grating
    from . import add_mesh_propeller
    from . import basket_arch
    from . import add_mesh_curved_plane
    from . import add_mesh_beam_builder

import bpy

class INFO_MT_mesh_ant_add(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_ant_add"
    bl_label = "ANT Mod"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.landscape_modified_add",
            text="ANT Landscape")
        layout.label(text="Use Erode After ANT")
        layout.operator("mesh.erode",
            text="Erosion")
        layout.separator()
        layout.operator("mesh.primitive_terrain_add", text="Terrain")
        layout.operator("mesh.rocks", text="Rock Gen")
        layout.operator("mesh.primitive_cave_gen",
            text="Cave Gen")
        layout.operator("mesh.lowpoly_rock_add",
            text="Low Poly Rock")

class INFO_MT_mesh_vert_add(bpy.types.Menu):
    # Define the "Pipe Joints" menu
    bl_idname = "INFO_MT_mesh_vert_add"
    bl_label = "Single Vert"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_vert_add",
            text="Add Single Vert ")
        layout.operator("mesh.primitive_emptyvert_add",
            text="Object Origin Only")
        layout.operator("mesh.primitive_symmetrical_vert_add",
            text="Origin & Vert Mirrored")
        layout.operator("mesh.primitive_symmetrical_empty_add",
            text="Object Origin Mirrored")

class INFO_MT_mesh_gears_add(bpy.types.Menu):
    # Define the "Gears" menu
    bl_idname = "INFO_MT_mesh_gears_add"
    bl_label = "Gears"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_gear",
            text="Gear")
        layout.operator("mesh.primitive_worm_gear",
            text="Worm")

class INFO_MT_mesh_diamonds_add(bpy.types.Menu):
    # Define the "Gears" menu
    bl_idname = "INFO_MT_mesh_diamonds_add"
    bl_label = "Diamonds"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_brilliant_add",
            text="Brilliant Diamond")
        layout.operator("mesh.primitive_diamond_add",
            text="Diamond")
        layout.operator("mesh.primitive_gem_add",
            text="Gem")

class INFO_MT_mesh_math_add(bpy.types.Menu):
    # Define the "Math Function" menu
    bl_idname = "INFO_MT_mesh_math_add"
    bl_label = "Math Functions"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("INFO_MT_mesh_torus_add", text="Torus Objects", icon="MESH_TORUS")
        layout.operator("mesh.primitive_z_function_surface",
            text="Z Math Surface")
        layout.operator("mesh.primitive_xyz_function_surface",
            text="XYZ Math Surface")
        self.layout.operator("mesh.primitive_solid_add", text="Regular Solid")
        self.layout.operator("object.dual_mesh_operator", text="Dual Mesh")

class INFO_MT_mesh_extras_add(bpy.types.Menu):
    # Define the "Simple Objects" menu
    bl_idname = "INFO_MT_mesh_extras_add"
    bl_label = "Extras"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.curved_plane",
            text="Curved Plane", icon="SMOOTHCURVE")
        layout.menu("INFO_MT_mesh_diamonds_add", text="Diamonds", icon="PMARKER_SEL")
        layout.menu("INFO_MT_mesh_ice_add", text="Ice & Snow", icon="FREEZE")
        layout.operator("mesh.primitive_star_add",
            text="Simple Star")
        layout.operator("mesh.primitive_steppyramid_add",
            text="Step Pyramid")
        layout.operator("mesh.honeycomb_add",
            text="Honeycomb")
        layout.operator("mesh.primitive_teapot_add",
            text="Teapot+")
        layout.operator("mesh.menger_sponge_add",
            text="Menger Sponge")
        layout.operator("mesh.fractal_dome",
            text="Fractal Dome")
        layout.operator("mesh.basketarch",
            text="Basket Arch")


class INFO_MT_mesh_torus_add(bpy.types.Menu):
    # Define the "Simple Objects" menu
    bl_idname = "INFO_MT_mesh_torus_add"
    bl_label = "Torus Objects"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_twisted_torus_add",
            text="Twisted Torus")
        layout.operator("mesh.primitive_supertoroid_add",
            text="Supertoroid")
        layout.operator("mesh.primitive_torusknot_add",
            text="Torus Knot")


class INFO_MT_mesh_pipe_joints_add(bpy.types.Menu):
    # Define the "Pipe Joints" menu
    bl_idname = "INFO_MT_mesh_pipe_joints_add"
    bl_label = "Pipe Joints"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_elbow_joint_add",
            text="Pipe Elbow")
        layout.operator("mesh.primitive_tee_joint_add",
            text="Pipe T-Joint")
        layout.operator("mesh.primitive_wye_joint_add",
            text="Pipe Y-Joint")
        layout.operator("mesh.primitive_cross_joint_add",
            text="Pipe Cross-Joint")
        layout.operator("mesh.primitive_n_joint_add",
            text="Pipe N-Joint")

class INFO_MT_mesh_icy_add(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_ice_add"
    bl_label = "Ice & Snow"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.icicle_gen",
            text="Icicle Generator")
        layout.operator("mesh.snowflake",
            text="Snowflake")

class INFO_MT_mesh_floorwall_add(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_floorwall_add"
    bl_label = "Floors & Walls"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_add_siding",
            text = "Siding")
        layout.operator("mesh.drystone",
            text="Drystone")
        layout.operator("mesh.floor_boards_add",
            text="Floor Boards")
        layout.operator("mesh.ajout_primitive",
            text="Plancher")

class INFO_MT_mesh_boundbox_add(bpy.types.Menu):
    # Define the "Bound Box" menu
    bl_idname = "INFO_MT_mesh_boundbox_add"
    bl_label = "Bound Box Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.boundbox_add",
            text = "Bound Box Add")
        layout.operator("object.min_bounds",
            text="Minimum Bounds")

class INFO_MT_mesh_mech_add(bpy.types.Menu):
    # Define the "Mech" menu
    bl_idname = "INFO_MT_mesh_mech_add"
    bl_label = "Mechanical"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("INFO_MT_mesh_pipe_joints_add", text="Pipe Joints", icon="SNAP_PEEL_OBJECT")
        layout.menu("INFO_MT_mesh_gears_add", text="Gears", icon="SCRIPTWIN")
        layout.operator("mesh.bolt_add", text="Add Bolt", icon="CURSOR")
        layout.operator("mesh.propeller_add", text="Propeller", icon="SCRIPTWIN")

class INFO_MT_mesh_building_add(bpy.types.Menu):
    # Define the "Building" menu
    bl_idname = "INFO_MT_mesh_building_add"
    bl_label = "Building"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("INFO_MT_mesh_floorwall_add", text="Floors & Walls", icon = "UV_ISLANDSEL")
        layout.operator("mesh.add_beam",
            text="Beam")
        layout.operator("mesh.add_say3d_balcony",
            text="Balcony")
        layout.operator("mesh.add_say3d_sove",
            text="Sove")
        layout.operator("mesh.add_say3d_pencere2",
            text="Window")
        layout.operator("mesh.wall_add",
            text="Wall Factory")
        layout.operator("mesh.stairs",
            text="Stair Builder")
        layout.operator("mesh.primitive_add_grating",
            text="Grating")
        layout.operator("object.book_gen",
            text="Book Gen")
        layout.operator("mesh.add_castle",
            text="Castle")
        layout.operator("window.run_action", text="Window (editable)", icon="MOD_LATTICE")

# Define "Extras" menu
def menu(self, context):
	layout = self.layout
	col = layout.column()
	self.layout.separator()
	self.layout.operator("object.parent_to_empty", text="Parent To Empty", icon="LINK_AREA")
	self.layout.separator()
	layout.label(text="AF: Mesh Objects", icon="OBJECT_DATAMODE")
	self.layout.menu("INFO_MT_mesh_vert_add", text="Single Vert", icon="LAYER_ACTIVE")
	self.layout.operator("mesh.primitive_round_cube_add", text="Round Cube", icon="WIRE")
	self.layout.menu("INFO_MT_mesh_ant_add", text="Landscape", icon="RNDCURVE")
	self.layout.menu("INFO_MT_mesh_math_add", text="Math Function", icon="PACKAGE")
	self.layout.menu("INFO_MT_mesh_mech_add", text="Mechanical", icon="SCRIPTWIN")
	self.layout.menu("INFO_MT_mesh_building_add", text="Building", icon="UV_ISLANDSEL")
	self.layout.menu("INFO_MT_mesh_extras_add", text="Extras", icon="MESH_DATA")
	self.layout.menu("INFO_MT_mesh_boundbox_add", text="Bound Box", icon="LATTICE_DATA")

# Addons Preferences
class MeshObjectPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "Enable_Tab_01", text="info", icon="INFO")   
        if context.scene.Enable_Tab_01:
            row = layout.row()
            layout.label(text="----Add Mesh Objects----")
            layout.label(text="Merges most Mesh Object Addons into One")
            layout.label(text="New sub menu's & organization")

        layout.prop(context.scene, "Enable_Tab_02", text="Mesh Objects", icon="INFO")  
        if context.scene.Enable_Tab_02:
            row = layout.row()
            layout.label(text="Add Mesh Vert: Adds single Vert with options")
            layout.label(text="Add Mesh Round Cube: Adds base sulpting objects")
            layout.label(text="Add Bound Box: Adds bounding box with options")
            layout.label(text="ANT Landscape: Create Landscape Mesh")
            layout.label(text="Erode: Add erosion To ANT Landscape mesh")
            layout.label(text="Terrain: create large Terrain mesh")
            layout.label(text="Rock Gen: Create displacement Rocks")
            layout.label(text="Cave Gen: Create Caves with lights")
            layout.label(text="Low Poly Rock: Create Low Poly Rock Shapes")
            layout.label(text="Torus Objects: Twisted, Super & Knot")
            layout.label(text="Z math & XYZ surface functions")
            layout.label(text="Regular Solid: Library of Solid Math Shapes")
            layout.label(text="Duel Mesh: Create duel copy of mesh")
            layout.label(text="Pipe Joints: Create various pipes")
            layout.label(text="Gears: Create Gears")
            layout.label(text="Bolt: Add several types of Bolt")
            layout.label(text="Propeller: Add Aerodynamic propeller")
            layout.label(text="Beam Builder: Create various Beams")
            layout.label(text="Floors & Walls: Siding, Drystone, Floorboards, Plancher")
            layout.label(text="Balcony, Sove, Window")
            layout.label(text="Wall Factory: Add Castle Wall")
            layout.label(text="Stair Builder: Add Stairs")
            layout.label(text="Grating: Add mesh Grating")
            layout.label(text="Book Gen: Create rows of books")
            layout.label(text="Castle: Create Castles (wip)")
            layout.label(text="Diamonds, Icicle & Snowflake")
            layout.label(text="Simple Star, Step Pyramid, Honeycomb")
            layout.label(text="Teapot+, Menger Sponge, Fractal Dome")
            layout.label(text="Basket Arch")

def register():
    bpy.utils.register_module(__name__)

    # Add "AF:" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu)

def unregister():
    # Remove "AF:" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
