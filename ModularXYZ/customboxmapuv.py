from maya import cmds

def customboxmapuv(x_sides, y_sides, z_sides):
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return
    
    for obj in selected_objects:
        cmds.polyAutoProjection(obj, lm=0, cm=0, l=0, sc=1, o=1, p=6, ps=0.2, ws=1, ch=False, sx=x_sides, sy=y_sides, sz=z_sides)
        print(f"Auto Project UV applied to {obj} with X: {x_sides}, Y: {y_sides}, Z: {z_sides} sides.")
