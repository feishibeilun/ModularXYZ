import maya.cmds as cmds

def grid_lines_control(value):
    """Adjusts the spacing of the grid lines."""
    cmds.grid(spacing=value)

def grid_size_control(length, width):
    """Adjusts the length and width of the grid."""
    cmds.grid(size=length)
    # In Maya, the grid size command sets both the length and width to the same value.

def grid_down():
    """Divides the 'grid lines every' value by 2, making the grid lines closer."""
    current_spacing = cmds.grid(query=True, spacing=True)
    new_spacing = max(current_spacing / 2, 0.001)  # Prevents the spacing from becoming 0
    cmds.grid(spacing=new_spacing)

def grid_up():
    """Doubles the 'grid lines every' value, making the grid lines further apart."""
    current_spacing = cmds.grid(query=True, spacing=True)
    cmds.grid(spacing=current_spacing * 2)