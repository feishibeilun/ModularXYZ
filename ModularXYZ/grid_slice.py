import maya.cmds as cmds
import math  # Import math library for ceiling function

def grid_slice(grid_size=1.0):
    selected_objects = cmds.ls(selection=True, long=True, type='transform')

    for object_name in selected_objects:
        shapes = cmds.listRelatives(object_name, shapes=True)
        if shapes and cmds.objectType(shapes[0], isType='mesh'):
            slice_mesh_by_grid(object_name, grid_size)

def slice_mesh_by_grid(object_name, grid_size=1.0):
    bbox = cmds.exactWorldBoundingBox(object_name)
    min_x, min_y, min_z, max_x, max_y, max_z = bbox

    # Function to align min values with the grid
    align_with_grid = lambda min_val: math.ceil(min_val / grid_size) * grid_size

    # Adjusted min values to be grid-aligned
    min_x_aligned, min_y_aligned, min_z_aligned = map(align_with_grid, (min_x, min_y, min_z))
    max_x_aligned, max_y_aligned, max_z_aligned = map(align_with_grid, (max_x, max_y, max_z))
    # Iterate over each axis and perform slicing
    for axis, (min_val, max_val) in enumerate([(min_x_aligned, max_x_aligned), (min_y_aligned, max_y_aligned), (min_z_aligned, max_z_aligned)]):
        num_cuts = int((max_val - min_val) / grid_size)
        for i in range(num_cuts):
            cut_position = min_val + i * grid_size
            # Define cut plane rotation for each axis
            if axis == 0:  # X-axis
                cut_plane_rotate = [0, 90, 0]
                cut_plane_center = [cut_position, 0, 0]
            elif axis == 1:  # Y-axis
                cut_plane_rotate = [90, 0, 0]
                cut_plane_center = [0, cut_position, 0]
            else:  # Z-axis
                cut_plane_rotate = [0, 0, 0]  # No rotation needed for Z-axis cuts
                cut_plane_center = [0, 0, cut_position]
            
            # Perform the cut with updated rotation and center
            cmds.polyCut(object_name, cutPlaneCenter=cut_plane_center, cutPlaneRotate=cut_plane_rotate)

    print(f"Mesh '{object_name}' sliced by grid of size {grid_size}.")

# Example usage
grid_slice(1)
