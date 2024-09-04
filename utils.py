import bpy
import os
import textwrap

# ตัดบรรทัดบน Panel
def text_wrap(context, text, parent, line_height, char_width:int = 7):
    texts = text.split("$/n")
    for text in texts:
        chars = int(context.region.width / char_width)   # 7 pix on 1 character
        wrapper = textwrap.TextWrapper(width=chars)
        text_lines = wrapper.wrap(text=text)
        if "$/h" in text_lines[0]:
            text_lines[0] = text_lines[0].replace("$/h","")
            for i in range(len(text_lines)):
                text_lines[i] = "$/h" + text_lines[i]
        if "$/s" in text_lines[0]:
            text_lines[0] = text_lines[0].replace("$/s","")
            for i in range(len(text_lines)):
                text_lines[i] = "$/s" + text_lines[i]
        for i, text_line in enumerate(text_lines):
            row = parent.row(align=True)
            if i == 0:
                row.label(text="", icon="INFO")
            if "$/h" in text_line:
                row.alert = True
                text_line = text_line.replace("$/h","")
            if "$/s" in text_line:
                row.enabled = False
                text_line = text_line.replace("$/s","") 
            row.label(text=text_line)
            row.scale_y = line_height

# เลือก OBJ ผ่านชื่อ
def select_object_by_name(name):
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        return True
    else:
        return False
    
# Append Collection ผ่านไฟล์ในโฟลเดอร์
def append_collection(path: str, filename: str, collection: str):
    # กำหนด path ของไฟล์ .blend
    resources_path = os.path.join(os.path.dirname(__file__), path)
    blend_file_path = os.path.join(resources_path, filename)

    # กำหนดชื่อของคอลเลคชันที่ต้องการ Append
    collection_name = collection

    # เตรียม path ไปยังคอลเลคชันในไฟล์ .blend
    collection_path = os.path.join(blend_file_path, "Collection", collection_name)
    print(collection_path)

    # Append คอลเลคชันจากไฟล์ .blend
    with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
        if collection_name in data_from.collections:
            data_to.collections.append(collection_name)
    
    # นำคอลเลคชันที่ Append ไปใส่ใน Scene Collection
    appended_collection = bpy.data.collections.get(collection_name)
    if appended_collection:
        bpy.context.scene.collection.children.link(appended_collection)
        print(f"Appended collection '{collection_name}' to the Scene Collection.")
    else:
        print(f"Failed to append collection '{collection_name}' from '{blend_file_path}'.")

# Append Node ผ่านไฟล์ในโฟลเดอร์
def append_geometry_node(path: str, filename: str, node_group_name: str):
    # ตรวจสอบว่า Geometry Node Group มีอยู่แล้วหรือไม่
    if node_group_name in bpy.data.node_groups:
        print(f"'{node_group_name}' already exists in the current file. Skipping append.")
        return
    
    # กำหนด path ของไฟล์ .blend
    resources_path = os.path.join(os.path.dirname(__file__), path)
    blend_file_path = os.path.join(resources_path, filename)

    # กำหนดชื่อของ Geometry Node Group ที่ต้องการ Append
    geometry_node_name = node_group_name

    # เตรียม path ไปยัง Geometry Node Group ในไฟล์ .blend
    node_group_path = os.path.join(blend_file_path, "NodeTree", geometry_node_name)
    print(node_group_path)

    # Append Geometry Node Group จากไฟล์ .blend
    bpy.ops.wm.append(
        filepath=node_group_path, 
        directory=os.path.join(blend_file_path, "NodeTree"), 
        filename=geometry_node_name
    )

    print(f"Appended Geometry Node Group '{geometry_node_name}' from '{blend_file_path}'.")


# Focus outliner
def focus_object_in_outliner():
    try:
        for area in [a for a in bpy.context.screen.areas if a.type == 'OUTLINER']:
            for region in [r for r in area.regions if r.type == 'WINDOW']:
                override = {'area':area, 'region': region}
                bpy.ops.outliner.show_active(override)
    except:
        for area in [a for a in bpy.context.screen.areas if a.type == 'OUTLINER']:
            for region in [r for r in area.regions if r.type == 'WINDOW']:
                try:
                    with bpy.context.temp_override(area=area, region=region):
                        bpy.ops.outliner.show_active()
                except:
                    pass
                
def collection_collapse_all_by_name(name: str):
    for area in bpy.context.screen.areas:
        if area.type == 'OUTLINER':
            for region in area.regions:
                if region.type == 'WINDOW':
                    # ลองใช้ temp_override เพื่อจัดการบริบท
                    with bpy.context.temp_override(area=area, region=region, space_data=area.spaces.active):
                        try:
                            bpy.ops.outliner.show_one_level(open=False)
                        except Exception as e:
                            print(f"Error collapsing Outliner: {e}")
                            
                            
