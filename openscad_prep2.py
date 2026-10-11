import os
import sys
import bpy

# Adjust these two parameters to your liking:
VOXEL_SIZE = 0.3    # Target edge length (smaller = finer mesh)
SMOOTH_REPEAT = 15   # Edge rounding strength (higher = rounder edges)


def import_stl(filepath):
    """Import STL file across Blender versions (4.0+/5.x vs older)."""
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=filepath)
    elif hasattr(bpy.ops, "import_mesh") and hasattr(bpy.ops.import_mesh, "stl"):
        bpy.ops.import_mesh.stl(filepath=filepath)
    else:
        raise RuntimeError("No STL import operator found in Blender.")


def export_stl(filepath):
    """Export STL file across Blender versions (4.0+/5.x vs older)."""
    try:    bpy.ops.wm.stl_export(filepath=filepath)
    except:   bpy.ops.export_mesh.stl(filepath=filepath)

def smooth_mesh(obj):
    """Apply voxel remesh and smooth modifier to the given mesh object."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # 1. Remesh to uniform grid
    obj.data.remesh_voxel_size = VOXEL_SIZE
    bpy.ops.object.voxel_remesh()

    # 2. Add Smooth Modifier
    mod = obj.modifiers.new(name="AutoSmooth", type='SMOOTH')
    mod.factor = 1.0
    mod.iterations = SMOOTH_REPEAT

    # 3. Apply Modifier
    bpy.ops.object.modifier_apply(modifier=mod.name)
    print(f"OpenSCAD mesh prepped and smoothed successfully! ({len(obj.data.polygons)} polygons)")


def process_stl_file(input_file, output_file):
    input_path = os.path.abspath(input_file)
    output_path = os.path.abspath(output_file)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input STL file not found: {input_path}")

    print(f"Importing: {input_path}")

    # Remove all existing objects and meshes from the scene (removes default Cube, Camera, Light)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh, do_unlink=True)

    # Import STL
    import_stl(input_path)

    # Locate imported mesh
    mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not mesh_objs:
        raise RuntimeError(f"No mesh objects found after importing {input_path}")

    target_obj = mesh_objs[0]

    # Remesh & Smooth
    smooth_mesh(target_obj)

    # Export smoothed mesh to STL
    print(f"Exporting: {output_path}")
    export_stl(output_path)
    print("Export complete!")


def main():
    # Parse CLI arguments passed after '--'
    cli_args = []
    if "--" in sys.argv:
        cli_args = sys.argv[sys.argv.index("--") + 1:]

    if cli_args:
        input_file = cli_args[0]
        output_file = cli_args[1] if len(cli_args) > 1 else "parturi_smoothed.stl"
        process_stl_file(input_file, output_file)
    elif bpy.app.background:
        # Running headless without explicit arguments
        process_stl_file("parturi.stl", "parturi_smoothed.stl")
    else:
        # Running inside Blender GUI on the currently active object
        obj = bpy.context.active_object
        if obj and obj.type == 'MESH':
            smooth_mesh(obj)
        else:
            print("No active mesh object selected.")


if __name__ == "__main__":
    main()
