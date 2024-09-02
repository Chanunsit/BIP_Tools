import bpy
from .. import utils


from bpy.types import (Operator )
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)

#คำสั่ง Duplicate Cutter
class BIP_OT_DupCutter(Operator):
    bl_idname = "bip_tools.dup_cutter_operator"
    bl_label = "Duplicate Cutter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "UV_ISLANDSEL"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Duplicate Cutter with constraints and move to Boolean collection"

    action : StringProperty(name="action")

    @classmethod
    def poll(cls, context):
        return context.selected_objects
    
    def execute(self, context):
        scene = context.scene
        
        # สร้าง BIP_Brick_Cutters Collection
        main_collection_name = "BIP_BuildingDestruction"
        main_parent_collection = bpy.data.collections.get(main_collection_name)
        
        if main_parent_collection is None:
            print(f"Collection '{main_collection_name}' not found!")
            self.report({"INFO"} ,"BIP_BuildingDestruction not found")
        else:
            # สร้าง BIP_Brick_Cutters Collection เมื่อไม่มีอยู่ใน Scene"
            cutter_collection_name = "BIP_Brick_Cutters"
            cutter_collection = bpy.data.collections.get(cutter_collection_name)
            if cutter_collection is None:
                new_cutter_collection = bpy.data.collections.new(cutter_collection_name)
                # ย้าย BIP_Brick_Cutters Collection ไปที่ BIP_BuildingDestruction
                main_parent_collection.children.link(new_cutter_collection)
                print(f"Collection '{cutter_collection_name}' created inside '{main_collection_name}'.")
            brick_collection_name = "BIP_Bricks"
            brick_collection = bpy.data.collections.get(brick_collection_name)
            if brick_collection is None:
                new_brick_collection = bpy.data.collections.new(brick_collection_name)
                # ย้าย BIP_Brick Collection ไปที่ BIP_BuildingDestruction
                main_parent_collection.children.link(new_brick_collection)
                print(f"Collection '{brick_collection_name}' created inside '{main_collection_name}'.")
            
            # คำสั่ง Duplicate และย้ายไปที่ Collection
            bpy.ops.object.duplicate_move()
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
            # Unlink the object from its current collection(s)
                for collection in obj.users_collection:
                    collection.objects.unlink(obj)
                # Link the object to the target collection
                cutter_collection = bpy.data.collections.get(cutter_collection_name)
                cutter_collection.objects.link(obj)
            cutter_name = bpy.context.active_object.name
            brick_name = cutter_name
            brick_name = brick_name.rpartition('_Cutter')[0]
            print(brick_name)
            bpy.ops.object.select_all(action='DESELECT')
            utils.select_object_by_name(brick_name)
            bpy.ops.object.duplicate_move()
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
            # Unlink the object from its current collection(s)
                for collection in obj.users_collection:
                    collection.objects.unlink(obj)
                # Link the object to the target collection
                brick_collection = bpy.data.collections.get(brick_collection_name)
                brick_collection.objects.link(obj)
            bpy.context.active_object.name = cutter_name.replace("_Cutter", "")
            selected_object = bpy.context.active_object
            while selected_object.constraints:
                selected_object.constraints.remove(selected_object.constraints[0])
            bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
            bpy.context.object.constraints["Copy Transforms"].target = bpy.data.objects[cutter_name]
            utils.select_object_by_name(cutter_name)

        return {'FINISHED'}

    
def register():
    bpy.utils.register_class(BIP_OT_DupCutter)

           
def unregister():
    bpy.utils.unregister_class(BIP_OT_DupCutter)

        
