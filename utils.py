import bpy
def select_object_by_name(name):
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        return True
    else:
        return False