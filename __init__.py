
bl_info = {
        "name": "BIP Tools",
        "description": "GOD Tools Of Blender3D",
        "author": "GrammaTeam",
        "version": (1, 0),
        "blender": (3, 5, 0),
        "location": "View3D",
        "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "",
        "tracker_url": "",
        "support": "COMMUNITY",
        "category": "Object"
        }

from . import properties
from . import ui
from . import icon_reg

from .operators import register as reg_operators
from .operators import unregister as unreg_operators

#Check patch version
addon_version = bl_info["version"]
addon_version_string = ".".join(map(str, addon_version))


def register():
     properties.register()
     ui.register()
     icon_reg.register()
     reg_operators()
     


def unregister():
     properties.unregister()
     ui.unregister()
     icon_reg.unregister()
     unreg_operators()
     

if __name__ == '__main__':
     register()
