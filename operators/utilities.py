import bpy
import bmesh
from bpy.types import (Operator)
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)



class BIP_OT_ToggleProp(Operator):
    bl_idname = "bip_tools.toggle_prop_operator"
    bl_label = "Toggle"
    bl_description = "Show/Hide"

    prop_name: bpy.props.StringProperty(name="Property Name") 

    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        current_value = getattr(bip_tools, self.prop_name)
        setattr(bip_tools, self.prop_name, not current_value)
        print(f"{self.prop_name}: {getattr(bip_tools, self.prop_name)}")
               
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(BIP_OT_ToggleProp)


           
def unregister():
    bpy.utils.unregister_class(BIP_OT_ToggleProp)

