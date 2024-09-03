import bpy
from .. import utils


from bpy.types import (Operator )
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)


#คำสั่ง Import Assets
class BIP_OT_ImportAssets(Operator):
    bl_idname = "bip_tools.import_assets_operator"
    bl_label = "Import Assets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Import Assets"

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_BuildingDestruction"
        return not "BIP_BuildingDestruction" in bpy.data.collections

    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        utils.append_collection("resources", "bip_building_dst.blend", "BIP_BuildingDestruction")
        utils.select_object_by_name("BIP_BuildingDestruction_Locator")
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        collection = bpy.data.collections.get("BIP_Bricks_Assets")
        collection.hide_select = True
        bip_tools.info_text = "Select your Building and click Add Boolean"
        #utils.collection_collapse_all_by_name("BIP_BuildingDestruction")

        return {'FINISHED'}
    
    
#คำสั่ง Add Boolean
class BIP_OT_AddBoolean(Operator):
    bl_idname = "bip_tools.add_boolean_operator"
    bl_label = "Add Boolean"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Add Boolean To Object"

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_BuildingDestruction" และมี active object
        if "BIP_BuildingDestruction" in bpy.data.collections and context.active_object:
            if not "BIP_Brick_" in context.active_object.name:
                # ตรวจสอบว่า active object เป็นวัตถุชนิด Mesh และมีการเลือกวัตถุ Mesh
                if context.active_object.type == 'MESH':
                    # ตรวจสอบว่ามี Boolean แล้วหรือยัง
                    for modifier in context.active_object.modifiers:
                        if modifier.name == "BIP_Brick_Cutters":
                            return False
                    # ตรวจสอบว่ามีวัตถุ Mesh ที่ถูกเลือก
                    if any(obj.type == 'MESH' for obj in context.selected_objects):
                        return True
        return False

    def execute(self, context):
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
                
        # Add Boolean
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].name = "BIP_Brick_Cutters"
        bpy.context.object.modifiers["BIP_Brick_Cutters"].operand_type = 'COLLECTION'
        bpy.context.object.modifiers["BIP_Brick_Cutters"].collection = bpy.data.collections["BIP_Brick_Cutters"]
        bpy.context.object.modifiers["BIP_Brick_Cutters"].use_hole_tolerant = True
        bpy.context.object.modifiers["BIP_Brick_Cutters"].material_mode = 'TRANSFER'

        return {'FINISHED'}
    
    
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
        # ตรวจสอบว่ามีวัตถุที่ถูกเลือกและ active object ไม่เป็น None
        if context.selected_objects and context.active_object:
            # ตรวจสอบว่าชื่อของ active object มี "BIP_Brick_" อยู่หรือไม่
            return "BIP_Brick_" in context.active_object.name and "BIP_BuildingDestruction" in bpy.data.collections
        return False
    
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
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            
            bpy.context.object.lock_location[0] = False
            bpy.context.object.lock_location[1] = False
            bpy.context.object.lock_location[2] = False
            bpy.context.object.lock_rotation[0] = False
            bpy.context.object.lock_rotation[1] = False
            bpy.context.object.lock_rotation[2] = False
            bpy.context.object.lock_scale[0] = False
            bpy.context.object.lock_scale[1] = False
            bpy.context.object.lock_scale[1] = False

            
            bpy.ops.wm.tool_set_by_id(name="builtin.move")


        return {'FINISHED'}

    
def register():
    bpy.utils.register_class(BIP_OT_ImportAssets)
    bpy.utils.register_class(BIP_OT_AddBoolean)
    bpy.utils.register_class(BIP_OT_DupCutter)

           
def unregister():
    bpy.utils.unregister_class(BIP_OT_ImportAssets)
    bpy.utils.unregister_class(BIP_OT_AddBoolean)
    bpy.utils.unregister_class(BIP_OT_DupCutter)

        
