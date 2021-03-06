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

__bpydoc__ = """\
The KeepTrans addon works when you want to remove a ChildOf constraint, but keep
constraineed object in place globally.


Documentation

First go to User Preferences->Addons and enable the KeepTrans addon in the Object category.
Select the parent object of your choice and invoke the addon (button in the Object Tools panel).

If you wish to hotkey DeCouple:
In the Input section of User Preferences at the bottom of the 3D View > Object Mode section click 'Add New' button.
In the Operator Identifier box put 'object.keeptrans'.
Assign a hotkey.
Save as Default (Optional).
"""


bl_info = {
	"name": "KeepTrans",
	"author": "Gert De Roost",
	"version": (0, 3, 0),
	"blender": (2, 6, 5),
	"location": "View3D > Tools",
	"description": "Remove ChildOf constraint and keep transforms",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"}

if "bpy" in locals():
    import imp


import bpy
from mathutils import * 

class DeCouple(bpy.types.Operator):
	bl_idname = "object.keeptrans"
	bl_label = "KeepTrans"
	bl_description = "Remove ChildOf constraint and keep transforms"
	bl_options = {"REGISTER", "UNDO"}
	
	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return (obj and context.mode == 'OBJECT')

	def invoke(self, context, event):
		self.save_global_undo = bpy.context.user_preferences.edit.use_global_undo
		bpy.context.user_preferences.edit.use_global_undo = False
		
		do_keeptrans(self)
		
		bpy.context.user_preferences.edit.use_global_undo = self.save_global_undo
		return {'FINISHED'}


def panel_func(self, context):
	self.layout.label(text="KeepTrans:")
	self.layout.operator("object.keeptrans", text="KeepTrans")


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_PT_tools_objectmode.append(panel_func)


def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VIEW3D_PT_tools_objectmode.remove(panel_func)


if __name__ == "__main__":
	register()





def do_keeptrans(self):

	scn = bpy.context.scene
	ob = bpy.context.active_object
	parent = ob.parent
	childof = None
	for c in ob.constraints:
		if c.type == "CHILD_OF":
			childof = c
			break
	if childof == None:
		return
	tar = childof.target
	if parent:
		bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
		ob.constraints.remove(childof)
		parent.select = 1
		scn.objects.active = parent
		bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
		parent.select = 0
		ob.select = 1
		scn.objects.active = ob
	else:
		ob.constraints.remove(childof)
		ob.parent = tar
		bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
