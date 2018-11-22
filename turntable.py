import os
import sys

import bpy


def close():
    if not background:
        bpy.ops.wm.quit_blender()


def render():
    if background:
        bpy.ops.render.render(animation=True)
    else:
        bpy.ops.render.opengl(animation=True, view_context=False)


# Evaluate arguments
input_arg = "--turntable-model"
output_arg = "--turntable-output"

argv = sys.argv
background = any(arg in argv for arg in ["-b", "--background"])

if input_arg not in argv:
    print(input_arg, "argument missing")
    close()
    exit(1)

for arg in [input_arg, output_arg]:
    if arg in argv and argv.index(arg) + 1 == len(argv):
        print(arg, "argument value missing")
        close()
        exit(1)

input_file = argv[argv.index(input_arg) + 1]
output_dir = argv[argv.index(output_arg) + 1] if output_arg in argv else bpy.data.scenes["Scene"].render.filepath

if not os.path.isfile(input_file):
    print("File not found:", input_file)
    close()
    exit(1)

import_functions = {
    "dae": bpy.ops.wm.collada_import,
    "3ds": bpy.ops.import_scene.autodesk_3ds,
    "fbx": bpy.ops.import_scene.fbx,
    "ply": bpy.ops.import_mesh.ply,
    "obj": bpy.ops.import_scene.obj,
    "stl": bpy.ops.import_mesh.stl
}

extension = input_file.rsplit('.', 1)[1].lower() if '.' in input_file else None
if not extension or extension not in import_functions:
    print("Unsupported input file extension")
    close()
    exit(1)

# Import the file and get objects ready
import_functions[extension](filepath=input_file)
for o in bpy.data.objects:
    if o.select:
        o.pass_index = 1

# Align camera view to imported objects
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'WINDOW':
                override = {'area': area, 'region': region}
                bpy.ops.view3d.camera_to_view_selected(override)
bpy.data.objects["MainCamera"].location[0] = bpy.data.objects["MainCamera"].location[0] * 1.2
bpy.data.objects["MainCamera"].parent = bpy.data.objects["CameraRoot"]

# Render the turntable
distance = bpy.data.objects["MainCamera"].location[0]
height = bpy.data.objects["MainCamera"].location[2]

for i in range(6):
    for j in range(6):
        bpy.data.objects["MainCamera"].location[0] = distance + distance * i
        bpy.data.objects["MainCamera"].location[2] = height + abs(distance * j)
        bpy.data.scenes["Scene"].render.filepath = os.path.join(output_dir, f"distance {i} height {j}", "")
        render()

close()
