import maya.cmds as cmds

def process_materials(selection, unique_materials, is_component=False):
    """
    Processes the given selection to find and add materials to the unique_materials set.
    
    :param selection: The selected object or component in Maya.
    :param unique_materials: A set to store unique material names.
    :param is_component: A boolean indicating if the selection is a component (e.g., face).
    """
    if is_component:
        shading_groups = cmds.listSets(type=1, object=selection) or []
    else:
        shapes = cmds.listRelatives(selection, children=True, shapes=True) or []
        shading_groups = []
        for shape in shapes:
            shading_groups.extend(cmds.listConnections(shape, type='shadingEngine') or [])
    
    for sg in shading_groups:
        materials = cmds.ls(cmds.listConnections(sg), materials=True)
        for mat in materials:
            unique_materials.add(mat)

def fetch_materials_selection():
    """
    Fetches materials from the current selection or component selection in Maya, ensuring uniqueness.
    :return: A list of unique material names.
    """
    selection = cmds.ls(selection=True, objectsOnly=True)
    component_selection = cmds.ls(selection=True, flatten=True, objectsOnly=False)
    if not selection and not component_selection:
        print("No objects or components selected.")
        return []
    
    unique_materials = set()
    
    for obj in selection:
        process_materials(obj, unique_materials)
    
    for comp in component_selection:
        if '.f[' in comp:
            process_materials(comp, unique_materials, is_component=True)

    unique_materials_list = list(unique_materials)
    
    if unique_materials_list:
        print(f"Unique Materials: {', '.join(unique_materials_list)}")
    else:
        print("No materials found.")
    
    return unique_materials_list

def assign_material_to_selection(self):
    selected_items = self.listWindow.selectedItems()
    if not selected_items:
        cmds.warning("No material selected in the list.")
        return

    material_name = selected_items[0].text()  # Assuming single selection for simplicity

    # Get Maya selection
    maya_selection = cmds.ls(selection=True)
    if not maya_selection:
        cmds.warning("No objects selected in Maya.")
        return

    # Find shading group associated with the material
    shading_groups = cmds.listConnections(f"{material_name}.outColor", type='shadingEngine')
    if not shading_groups:
        cmds.warning(f"No shading group found for material: {material_name}")
        return

    shading_group = shading_groups[0]  # Assuming the first shading group is the target

    # Assign the shading group to each selected object
    for obj in maya_selection:
        cmds.sets(obj, edit=True, forceElement=shading_group)

    cmds.inform(f"Assigned {material_name} to selected objects.")


# Example of executing the function
unique_materials = fetch_materials_selection()
print(unique_materials)
