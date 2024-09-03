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
def append_collection(path:str, filename:str, collection:str):
    # กำหนด path ของไฟล์ .blend
    blend_file_path = os.path.join(path, filename)

    # กำหนดชื่อของคอลเลคชันที่ต้องการ Append
    collection_name = collection

    # เตรียม path ไปยังคอลเลคชันในไฟล์ .blend
    collection_path = os.path.join(blend_file_path, "Collection", collection_name)
    print(collection_path)

    # Append คอลเลคชันจากไฟล์ .blend
    bpy.ops.wm.append(
        filepath=collection_path, 
        directory=os.path.join(blend_file_path, "Collection"), 
        filename=collection_name
    )

    print(f"Appended collection '{collection_name}' from '{blend_file_path}'.")


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