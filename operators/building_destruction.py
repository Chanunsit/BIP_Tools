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
        bpy.context.space_data.shading.wireframe_color_type = 'OBJECT'
        bpy.context.space_data.shading.color_type = 'OBJECT'
        bpy.ops.object.select_all(action='DESELECT')
        

        utils.append_collection("resources", "bip_building_dst.blend", "BIP_BuildingDestruction")
        utils.select_object_by_name("BIP_BuildingDestruction_Locator")
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        # collection = bpy.data.collections.get("BIP_Bricks_Assets")
        # collection.hide_select = True
        bip_tools.info_text = "Select your Building and click Add Boolean"
        #utils.collection_collapse_all_by_name("BIP_BuildingDestruction")
        
        # ตรวจสอบว่าคอลเลคชัน "BIP_Bricks_Assets_LOD" มีอยู่ใน bpy.data.collections หรือไม่
        collection_name = "BIP_Bricks_Assets_LOD"
        collection = bpy.data.collections.get(collection_name)

        if collection:
            # ลบคอลเลคชันทั้งหมด รวมถึงวัตถุในคอลเลคชันและคอลเลคชันย่อย
            bpy.data.collections.remove(collection)
            print(f"Collection '{collection_name}' and its hierarchy have been deleted.")
        else:
            print(f"Collection '{collection_name}' not found.")

        # คำสั่ง Fake-User Mesh ทั้งหมด
        meshes = bpy.data.meshes
        for mesh in meshes:
            if "BIP_Brick" in mesh.name:
                print(mesh.name)
                mesh.use_fake_user = True
        
        return {'FINISHED'}
    
#คำสั่งลบ Assets
class BIP_OT_DelAssets(Operator):
    bl_idname = "bip_tools.del_assets_operator"
    bl_label = "Delete Assets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Delete Assets In Scene"

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_BuildingDestruction"
        return "BIP_BuildingDestruction" in bpy.data.collections

    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        
        # ตรวจสอบว่าคอลเลคชัน "BIP_BuildingDestruction" มีอยู่ใน bpy.data.collections หรือไม่
        collection_name = "BIP_BuildingDestruction"
        collection = bpy.data.collections.get(collection_name)

        if collection:
            # ลบคอลเลคชันทั้งหมด รวมถึงวัตถุในคอลเลคชันและคอลเลคชันย่อย
            bpy.data.collections.remove(collection)
            print(f"Collection '{collection_name}' and its hierarchy have been deleted.")
        else:
            print(f"Collection '{collection_name}' not found.")
        
        # คำสั่ง Fake-User Mesh ทั้งหมด
        meshes = bpy.data.meshes
        for mesh in meshes:
            if "BIP_Brick" in mesh.name:
                print(mesh.name)
                mesh.use_fake_user = False
        
        # ลบ Mesh Data ที่ไม่ได้ใช้งานออกจากหน่วยความจำ
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        bip_tools.info_text = "First! Import Assets to this Scene"
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
        scene = context.scene
        bip_tools = scene.bip_tools

        # ห้ามเลือกเกิน 2 0bj
        if len(context.selected_objects) > 1:
            self.report({"INFO"} ,"Please select only 1 object")
            return {'FINISHED'}
        
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
        collection = bpy.data.collections.get("BIP_Bricks")
        collection.hide_select = True
                
        # Add Boolean
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].name = "BIP_Brick_Cutters"
        bpy.context.object.modifiers["BIP_Brick_Cutters"].operand_type = 'COLLECTION'
        bpy.context.object.modifiers["BIP_Brick_Cutters"].collection = bpy.data.collections["BIP_Brick_Cutters"]
        bpy.context.object.modifiers["BIP_Brick_Cutters"].solver = 'FAST'
        bpy.context.object.modifiers["BIP_Brick_Cutters"].use_hole_tolerant = True
        bpy.context.object.modifiers["BIP_Brick_Cutters"].material_mode = 'TRANSFER'
        
        
        bip_tools.info_text = "Select a Cutter and click Duplicate and move it to your building"

        return {'FINISHED'}

#คำสั่งลบ Boolean
class BIP_OT_DelBoolean(Operator):
    bl_idname = "bip_tools.del_boolean_operator"
    bl_label = "Delete Boolean"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Delete Boolean In Object"

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_BuildingDestruction" และมี active object
        if "BIP_BuildingDestruction" in bpy.data.collections and context.selected_objects:
            if not "BIP_Brick_" in context.active_object.name:
                # ตรวจสอบว่า active object เป็นวัตถุชนิด Mesh และมีการเลือกวัตถุ Mesh
                if context.active_object.type == 'MESH':
                    # ตรวจสอบว่ามี Boolean แล้วหรือยัง
                    for modifier in context.active_object.modifiers:
                        if modifier.name == "BIP_Brick_Cutters":
                            return True
                    # # ตรวจสอบว่ามีวัตถุ Mesh ที่ถูกเลือก
                    # if any(obj.type == 'MESH' for obj in context.selected_objects):
                    #     return True
        return False

    def execute(self, context):
        bpy.ops.object.modifier_remove(modifier="BIP_Brick_Cutters")
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

    

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีวัตถุที่ถูกเลือกและ active object ไม่เป็น None
        if context.selected_objects and context.active_object:
            # ตรวจสอบว่าชื่อของ active object มี "BIP_Brick_" อยู่หรือไม่
            return "BIP_Brick_" in context.active_object.name and "BIP_BuildingDestruction" in bpy.data.collections
        return False
    
    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        
        # ห้ามเลือกเกิน 1 0bj
        if len(context.selected_objects) > 1:
            self.report({"INFO"} ,"Please select only 1 object, Multiple select work in progress")
            return {'FINISHED'}
        
        #Show Collection
        if "BIP_Brick_Cutters" in bpy.data.collections and "BIP_Bricks" in bpy.data.collections:
            collection = bpy.data.collections.get("BIP_Brick_Cutters")
            collection.hide_viewport = False
            collection = bpy.data.collections.get("BIP_Bricks")
            collection.hide_viewport = False
        
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
                collection = bpy.data.collections.get("BIP_Bricks")
                collection.hide_select = True
            
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
            bpy.ops.object.duplicate_move_linked()
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
            bpy.ops.object.select_all(action='DESELECT')
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
            
            if bip_tools.dup_to_cursor:
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)

        return {'FINISHED'}

#คำสั่งลบ Cutter
class BIP_OT_DelCutter(Operator):
    bl_idname = "bip_tools.del_cutter_operator"
    bl_label = "Delete Cutter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Delete Selected Cutters"

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีวัตถุที่ถูกเลือกและ active object ไม่เป็น None
        if context.selected_objects and context.active_object:
            # ตรวจสอบว่าชื่อของ active object มี "_Cutter." อยู่หรือไม่
            return "_Cutter." in context.active_object.name and "BIP_BuildingDestruction" in bpy.data.collections
        return False

    def execute(self, context):
        collection = bpy.data.collections.get("BIP_Bricks")
        collection.hide_select = False
        selected_object_names = [obj.name for obj in bpy.context.selected_objects]
        for name in selected_object_names:
            utils.select_object_by_name(name.replace("_Cutter", ""))
            utils.select_object_by_name(name)
            bpy.ops.object.delete()
        collection.hide_select = True
        # ลบ Mesh Data ที่ไม่ได้ใช้งานออกจากหน่วยความจำ
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=False, do_recursive=False)
        return {'FINISHED'}
    
#คำสั่งสลับ Cutter
class BIP_OT_ReplaceCutter(Operator):
    bl_idname = "bip_tools.replace_cutter_operator"
    bl_label = "Replace Cutter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Replace Cutters From Active"

    @classmethod
    def poll(cls, context):
        if "BIP_BuildingDestruction" in bpy.data.collections:
            # ตรวจสอบว่า Active Object มีอยู่และไม่มีชื่อ "_Cutter."
            if len(context.selected_objects) <= 1:
                return False
            active_obj = context.active_object
            if "_Cutter" in active_obj.name:
                return True
        return False

    def execute(self, context):
        selected_object_names = [obj.name for obj in bpy.context.selected_objects]
        active_object_name = context.active_object.name
        
        for i, name in enumerate(selected_object_names):
            bpy.ops.object.select_all(action='DESELECT')
            if "BIP_Brick_" in name:
                print(name)
                utils.select_object_by_name(name)
                obj = context.active_object
                if not obj.name == active_object_name:
                    if obj.type == "MESH":
                        # เก็บตำแหน่งและการหมุนของ Object ที่เลือก
                        loc = obj.location.copy()
                        roc = obj.rotation_euler.copy()

                        # ลบ Object เดิม
                        print(f"Old Object : {name}")
                        utils.select_object_by_name(name)
                        bpy.ops.bip_tools.del_cutter_operator()
                        bpy.ops.object.select_all(action='DESELECT')

                        # คัดลอก Object ต้นแบบและวางที่ตำแหน่งเดิม
                        print(f"active_object_name : {active_object_name} : to {loc}, {roc}")
                        utils.select_object_by_name(active_object_name)
                        bpy.ops.bip_tools.dup_cutter_operator()

                        # บังคับให้เลือกวัตถุใหม่หลังการคัดลอก
                        new_object = context.active_object
                        new_object.select_set(True)
                        bpy.context.view_layer.objects.active = new_object

                        # กำหนดตำแหน่งและการหมุน
                        new_object.location = loc
                        new_object.rotation_euler = roc
                        bpy.ops.object.select_all(action='DESELECT')
            print("---------------------------------------")
        return {'FINISHED'}

#คำสั่ง Show/Hide Collection
class BIP_OT_ShowBrick(Operator):
    bl_idname = "bip_tools.show_brick_operator"
    bl_label = "Show and Hide Brick"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Show and Hide Brick"

    action : StringProperty(name="action")

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_BuildingDestruction"
        if "BIP_BuildingDestruction" in bpy.data.collections:
                return True
        return False

    def execute(self, context):
        action = self.action
        command = action.split(":>")[0]
        name = action.split(":>")[1]
        if command == "collection":
            utils.hide_viewport_collection(name, True)
            # try:
            #     collection = bpy.data.collections.get(name)
            #     collection.hide_viewport = not collection.hide_viewport
            # except:
            #     print("Not Found Collection")
        elif command == "entity":
            print("Ennnnnnnnnnnnnnnn")
            
        return {'FINISHED'}
    
#คำสั่งสร้าง Entity
class BIP_OT_CreateEntity(Operator):
    bl_idname = "bip_tools.create_entity_operator"
    bl_label = "Create Entity"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Create Entity To Active Collection"

    action : StringProperty(name="action")

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีคอลเลคชันชื่อ "BIP_Bricks"
        if "BIP_Bricks" in bpy.data.collections:
                return True
        return False

    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools

        # Apply
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == "MESH":
                for mod in obj.modifiers:
                    if mod.name == "BIP_Brick_Cutters":
                        # ตรวจสอบว่ามี Solver property
                        if hasattr(mod, "solver"):
                            mod.solver = 'EXACT'
                            print(f"Changed solver to Exact for object: {obj.name}")
                        # Apply modifier หลังจากแก้ไขค่า solver
                        bpy.context.view_layer.objects.active = obj  # ตั้งค่า object ที่จะ Apply เป็น Active
                        bpy.ops.object.modifier_apply(modifier=mod.name)  # Apply modifier
                        print(f"Applied modifier {mod.name} for object: {obj.name}")
                        break

        
        utils.append_geometry_node("resources", "bip_node_lib.blend", "BIP_Collection_Join")
        bpy.ops.mesh.primitive_cube_add(size=2)
        bpy.context.object.name = "BIP_Entity_Brick_LOD"+str(bip_tools.lod_num)
        bpy.context.object.data.uv_layers["UVMap"].name = "UVMap0"
        # เพิ่ม Geometry Nodes modifier ให้กับวัตถุที่เลือก
        bpy.ops.object.modifier_add(type='NODES')

        # กำหนดชื่อของ Node Group ที่จะใช้
        node_group_name = "BIP_Collection_Join"
        collection_name = "BIP_Bricks"

        # ตรวจสอบว่ามี Node Group ที่ต้องการใน bpy.data.node_groups หรือไม่
        if node_group_name in bpy.data.node_groups:
            # Assign Node Group ให้กับ modifier
            modifier = bpy.context.object.modifiers[-1]
            modifier.node_group = bpy.data.node_groups[node_group_name]

            # เชื่อมต่อคอลเลคชันกับ input socket ของ Node Group
            if collection_name in bpy.data.collections:
                modifier["Socket_2"] = bpy.data.collections[collection_name]
            else:
                print(f"Collection '{collection_name}' not found.")
        else:
            print(f"Node Group '{node_group_name}' not found.")
        
        bpy.ops.object.modifier_apply(modifier="GeometryNodes")

        
            
        return {'FINISHED'}
    
#คำสั่งเกี่ยวกับ LOD
class BIP_OT_LODTools(Operator):
    bl_idname = "bip_tools.lod_tools_operator"
    bl_label = "LOD Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "IMPORT"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Edit LOD For Bricks"

    action : StringProperty(name="action")

    @classmethod
    def poll(cls, context):
        # ตรวจสอบว่ามีวัตถุที่ถูกเลือกและ active object ไม่เป็น None
        if context.selected_objects:
            # ตรวจสอบว่าชื่อของ active object มี "BIP_Brick_" อยู่หรือไม่
            return "BIP_Brick_" in context.active_object.name and "BIP_BuildingDestruction" in bpy.data.collections
        return False

    def execute(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        
        selected_objects = context.selected_objects
        bricks_name = []
        for obj in selected_objects:
            bricks_name.append(obj.name.replace("_Cutter", ""))
        print(bricks_name)
        
        bpy.ops.object.select_all(action='DESELECT')
        for name in bricks_name:
            utils.select_object_by_name(name)
            obj = context.active_object
            data_name = obj.data.name
            data_name = data_name[:-1]
            print("Replace Data : " + data_name+str(bip_tools.lod_num))
            new_mesh_data = bpy.data.meshes.get(data_name+str(bip_tools.lod_num))
            print(obj.data.name)
            obj.data = new_mesh_data
        
        # สำสั่งเลือก Object
        bpy.ops.object.select_all(action='DESELECT')
        for name in bricks_name:
            utils.select_object_by_name(name.replace(".", "_Cutter."))
        return {'FINISHED'}

    
def register():
    bpy.utils.register_class(BIP_OT_ImportAssets)
    bpy.utils.register_class(BIP_OT_AddBoolean)
    bpy.utils.register_class(BIP_OT_DupCutter)
    bpy.utils.register_class(BIP_OT_ShowBrick)
    bpy.utils.register_class(BIP_OT_DelCutter)
    bpy.utils.register_class(BIP_OT_ReplaceCutter)
    bpy.utils.register_class(BIP_OT_CreateEntity)
    bpy.utils.register_class(BIP_OT_LODTools)
    bpy.utils.register_class(BIP_OT_DelBoolean)
    bpy.utils.register_class(BIP_OT_DelAssets)

           
def unregister():
    bpy.utils.unregister_class(BIP_OT_ImportAssets)
    bpy.utils.unregister_class(BIP_OT_AddBoolean)
    bpy.utils.unregister_class(BIP_OT_DupCutter)
    bpy.utils.unregister_class(BIP_OT_ShowBrick)
    bpy.utils.unregister_class(BIP_OT_DelCutter)
    bpy.utils.unregister_class(BIP_OT_ReplaceCutter)
    bpy.utils.unregister_class(BIP_OT_CreateEntity)
    bpy.utils.unregister_class(BIP_OT_LODTools)
    bpy.utils.unregister_class(BIP_OT_DelBoolean)
    bpy.utils.unregister_class(BIP_OT_DelAssets)

        
