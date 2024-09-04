import bpy

from bpy.types import Scene
from bpy.types import (PropertyGroup)
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)



class MyProperties(PropertyGroup):
    tabs_menu : EnumProperty(
        name = "Tabs",
        items = [('destools', "Destruction", "Tools for Destruction", "MOD_BUILD", 1),
                 ('setting', "Setting", "Addon Setting", "PREFERENCES", 2)
                 ]
    )
    
    # ตัวแปร Info บน Panel
    info_text : StringProperty(name="Info", default="First! Import Assets to this Scene")

    #ตัวแปร LOD
    lod_num : IntProperty(name="LOD", default=0, min=0, max=3)


classes = [MyProperties]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Scene.bip_tools = PointerProperty(type= MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del Scene.bip_tools