import bpy


from . import icon_reg


from bpy.types import Panel
from bpy.types import Menu
from bpy.types import Scene
from bpy.types import Header


\
class VIEW3D_PT_BIP_MainPanel(Panel):
    bl_idname = "VIEW3D_PT_BIP_Main_panel"
    bl_label = " Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "∩"
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
            row.label(text="Destruction Tools:")
            box = layout.box()
            row = box.row()
            row.label(text="Building")
            row = box.row()
            row.operator("bip_tools.import_assets_operator", icon="IMPORT")
            row = box.row()
            row.operator("bip_tools.dup_cutter_operator", icon="UV_ISLANDSEL")

classes = [VIEW3D_PT_BIP_MainPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
