import bpy
import os


from . import icon_reg
from . import utils


from bpy.types import Panel
from bpy.types import Menu
from bpy.types import Scene
from bpy.types import Header



class VIEW3D_PT_BIP_MainPanel(Panel):
    bl_idname = "VIEW3D_PT_BIP_Main_panel"
    bl_label = " Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "❘❙❚✖❚❙❘"
    #bl_width = 1000

    def draw_header(self, context):

        layout = self.layout
        row = layout.row(align=True)
        row.scale_x = 0.85
        row.label(text="", icon_value=icon_reg.iconLib("logo_B"))
        row.label(text="", icon_value=icon_reg.iconLib("logo_I"))
        row.label(text="", icon_value=icon_reg.iconLib("logo_P"))
        #layout.label(text="Tools")
        

    def draw(self, context):
        scene = context.scene
        bip_tools = scene.bip_tools
        layout = self.layout

        row = layout.row()
        row.alignment = "CENTER"
        row.prop(bip_tools, "tabs_menu", text="", expand=True) # Tabs, no expand
        row.scale_x = 2
        
        #Mesh Tab
        if bip_tools.tabs_menu == "destools":
            layout = self.layout
            row = layout.row()
            row.label(text="Destruction Tools :")
            box = layout.box()
            row = box.row()
            row.alignment = "LEFT"
            row.label(text="Wall :")
            row.label(text="", icon_value=icon_reg.iconLib("wall_dst_01"))
            row.label(text="", icon_value=icon_reg.iconLib("wall_dst_02"))
            row.label(text="", icon_value=icon_reg.iconLib("wall_dst_03"))
            row.label(text="", icon_value=icon_reg.iconLib("wall_dst_04"))
            row.label(text="", icon_value=icon_reg.iconLib("wall_dst_05"))
            utils.text_wrap(context, bip_tools.info_text, box, 0.5, 7)
            row = box.row()
            row = box.row(align=True)
            row.operator("bip_tools.import_assets_operator", icon="IMPORT")
            row.operator("bip_tools.del_assets_operator", text="", icon="TRASH")
            col = box.column()
            row = col.row(align=True)
            row.operator("bip_tools.add_boolean_operator", icon="MOD_BOOLEAN")
            row.operator("bip_tools.del_boolean_operator", text="", icon="TRASH")
            #row = box.row(align=True)
            #row.alignment = "CENTER"
            row = col.row(align=True)
            obj = context.active_object
        
            # วนลูปผ่าน modifiers เพื่อหา "BIP_Brick_Cutters"
            if not obj:
                row.label(text="No object selected")
                return

            # ค้นหา modifier ที่ชื่อ "BIP_Brick_Cutters"
            modifier = next((mod for mod in obj.modifiers if mod.name == "BIP_Brick_Cutters"), None)
            if modifier:
                # ตรวจสอบว่า modifier มี property "solver" หรือไม่
                if hasattr(modifier, "solver"):
                    # แสดง property "solver" บน Panel โดยใช้ปุ่มแบบขยายได้
                    row.prop(modifier, "solver", text="Solver", expand=True)
                else:
                    row.label(text="No Solver property found.")

            row = box.row(align=True)
            row.scale_y = 2
            row.operator("bip_tools.dup_cutter_operator", icon="UV_ISLANDSEL")
            if bip_tools.dup_to_cursor:
                row.operator("bip_tools.toggle_prop_operator", text="", icon="PIVOT_CURSOR").prop_name = "dup_to_cursor"
            else:
                row.operator("bip_tools.toggle_prop_operator", text="", icon="CURSOR").prop_name = "dup_to_cursor"
            row = box.row(align=True)
            row.alignment = "CENTER"
            row.scale_x = 5
            row.operator("bip_tools.del_cutter_operator", text="", icon="TRASH")
            row.operator("bip_tools.replace_cutter_operator", text="", icon="EYEDROPPER")
            row = box.row()
            col = box.column()
            col.label(text="Show and Hide :")
            row = col.row()
            row.operator("bip_tools.show_brick_operator", text="All").action = "collection:>BIP_BuildingDestruction"
            row.operator("bip_tools.show_brick_operator", text="Cutters").action = "collection:>BIP_Brick_Cutters"
            row.operator("bip_tools.show_brick_operator", text="Bricks").action = "collection:>BIP_Bricks"
            row = box.row()
            col = box.column()
            col.label(text="Entity :")
            row = col.row(align=True)
            row.prop(bip_tools, "lod_num", text="")
            row.operator("bip_tools.lod_tools_operator", text="LOD")
            col.operator("bip_tools.create_entity_operator", text="Create Entity To Collection")
            row = box.row(align=True)
            row.scale_y = 0.5
            row.alignment = "LEFT"
            row.active = False
            row.label(text="", icon="INFO")
            row.label(text="Select LOD and click create Entity")
            row = box.row()
            row.scale_y = 0.5
            row.active = False
            row.label(text="When you have finished the design")
            row = box.row()

classes = [VIEW3D_PT_BIP_MainPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
