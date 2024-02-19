import maya.cmds as cmds

def boxmap1X1():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return

    for obj in selected_objects:
        # Apply Automatic Box Mapping with a fixed scale of 4x4 units for each projection plane
        cmds.polyAutoProjection(obj,lm=0,cm=0,l=0,sc=1,o=1,p=6,ps=0.2,ws=1,sx=1,sy=1,sz=1,ch=False) 

        print(f"4x4 box map UV applied to {obj}. UVs may extend beyond 0-1 space.")

boxmap1X1()


def boxmap2X2():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return

    for obj in selected_objects:
        # Apply Automatic Box Mapping with a fixed scale of 4x4 units for each projection plane
        cmds.polyAutoProjection(obj,lm=0,cm=0,l=0,sc=1,o=1,p=6,ps=0.2,ws=1,sx=2,sy=2,sz=2,ch=False) 

        print(f"4x4 box map UV applied to {obj}. UVs may extend beyond 0-1 space.")

boxmap2X2()


def boxmap4X4():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return

    for obj in selected_objects:
        # Apply Automatic Box Mapping with a fixed scale of 4x4 units for each projection plane
        cmds.polyAutoProjection(obj,lm=0,cm=0,l=0,sc=1,o=1,p=6,ps=0.2,ws=1,sx=4,sy=4,sz=4,ch=False) 

        print(f"4x4 box map UV applied to {obj}. UVs may extend beyond 0-1 space.")

boxmap4X4()

def boxmap8X8():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return

    for obj in selected_objects:
        # Apply Automatic Box Mapping with a fixed scale of 4x4 units for each projection plane
        cmds.polyAutoProjection(obj,lm=0,cm=0,l=0,sc=1,o=1,p=6,ps=0.2,ws=1,sx=8,sy=8,sz=8,ch=False) 

        print(f"4x4 box map UV applied to {obj}. UVs may extend beyond 0-1 space.")

boxmap8X8()

def boxmap16X16():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select at least one object.")
        return

    for obj in selected_objects:
        # Apply Automatic Box Mapping with a fixed scale of 4x4 units for each projection plane
        cmds.polyAutoProjection(obj,lm=0,cm=0,l=0,sc=1,o=1,p=6,ps=0.2,ws=1,sx=16,sy=16,sz=16,ch=False) 

        print(f"4x4 box map UV applied to {obj}. UVs may extend beyond 0-1 space.")

boxmap16X16()

def OverlapClean():
    selected_objects = cmds.ls(selection=True, type='transform')
    
    if not selected_objects:
        cmds.error("Please select at least one object with UVs.")
        return
    
    # Store the current selection to reselect after operation
    original_selection = cmds.ls(sl=True)
    
    for obj in selected_objects:
        # Get all shapes of the current object
        shapes = cmds.listRelatives(obj, children=True, shapes=True) or []
        
        for shape in shapes:
            # Check if the shape has UVs
            if cmds.polyEvaluate(shape, uv=True) > 0:
                # Layout UVs without scaling
                cmds.polyLayoutUV(shape, scale=0, layout=2)  # scale 0 turns off scaling, layout 2 for no overlap

    # Reselect originally selected objects
    cmds.select(original_selection, replace=True)

    print("UV layout applied to selected objects without scaling.")

OverlapClean()
