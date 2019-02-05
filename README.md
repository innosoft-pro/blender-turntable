# Blender Turntable Script

## Description
Use this to create 360 mask pictures of your model from various distances and heights.

Supported extensions: .3ds, .fbx, .ply, .obj, .stl. 

## Usage
Make sure you have Blender installed and run:

`./turntable <path to model> [<output folder> [<steps>]]`

Example:

`./turntable models/truck_1.dae`

`./turntable models/truck_1.dae output`

`./turntable models/truck_1.dae output 1`

Output folder will be created if it does not exist.
