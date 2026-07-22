
import bpy

# Adjust these two parameters to your liking:
VOXEL_SIZE = 0.5    # Target edge length (smaller = finer mesh)
SMOOTH_REPEAT = 15   # Edge rounding strength (higher = rounder edges)

# Ensure an object is active
obj = bpy.context.active_object
if obj and obj.type == 'MESH':
    # 1. Remesh to uniform grid
    obj.data.remesh_voxel_size = VOXEL_SIZE
    bpy.ops.object.voxel_remesh()
    
    # 2. Add Smooth Modifier
    mod = obj.modifiers.new(name="AutoSmooth", type='SMOOTH')
    mod.factor = 1.0
    mod.iterations = SMOOTH_REPEAT
    
    # 3. Apply Modifier
    bpy.ops.object.modifier_apply(modifier=mod.name)
    print("OpenSCAD mesh prepped and smoothed successfully!")
