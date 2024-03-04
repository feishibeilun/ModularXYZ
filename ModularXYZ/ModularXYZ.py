#--------------------------------------------------------------------------------#
#             only for maya 2022+
#
#
#             ModularXYZ.py 
#             version alpha, last modified 17/02/2024
#             Copyright (C) 2024 XiaoyueZhang
#             Email: xiaoyuezhangart@gmail.com
#             Website: https://www.artstation.com/xiaoyuezhang
#
# This program is free software: you can redistribute it and/or modify. More function are still need to be added, you can follow up through my page.
#--------------------------------------------------------------------------------#
#                    I N S T A L L A T I O N:
#
# Copy the "ModularXYZ.py" together with "grid_functions.py", Icon folder and curves folder to your Maya scriptsdirectory:
#     MyDocuments\Maya\scripts\
#         use this text as a python script within Maya:
'''
import ModularXYZ
ModularXYZ.create_custom_slider_window()
'''
# this text can be entered from the script editor and can be made into a button
#
# note: PyQt and sip or pyside  libraries are necessary to run this file

from PySide2.QtWidgets import QMainWindow, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QFrame, QListWidget, QAbstractItemView, QListWidgetItem
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPainter
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import grid_functions
import UVboxmap
import customboxmapuv
import grid_slice
import material_functions as MF
import grid_sample 
import math

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is not None:
        return wrapInstance(int(main_window_ptr), QWidget)

class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super(CustomSlider, self).__init__(orientation, parent)
        self.setMinimum(0)
        self.setMaximum(7)  # Represents 8 positions
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSingleStep(1)

    def paintEvent(self, event):
        super(CustomSlider, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.white)
        stepSize = self.width() / self.maximum()
        for i in range(self.maximum() + 1):
            x = stepSize * i
            markHeight = 5
            startPoint = QPoint(x, self.height() / 2 - markHeight / 2)
            endPoint = QPoint(x, self.height() / 2 + markHeight / 2)
            painter.drawLine(startPoint, endPoint)

class CustomSliderWindow(QMainWindow):
    def __init__(self, parent=get_maya_main_window()):
        super(CustomSliderWindow, self).__init__(parent)
        self.setWindowTitle('ModularXYZ')  # Update the window title here
        self.setGeometry(100, 100, 100, 100)
        self.gridSpacingValue = 0.125  # Default starting value
        self.gridSizeMultiplier = 0  # Initialize multiplier
        self.initUI()
        self.listWindow.focusOutEvent = self.deselectAllItems

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)

        # Slider 1 setup for grid lines control
        self.slider1Layout = QHBoxLayout()
        self.valueDisplay1 = QLabel('GridUnit:0.125 cm', self)
        self.valueDisplay1.setFixedWidth(100)  # Set a fixed width for the display label
        self.slider1Layout.addWidget(self.valueDisplay1)
        self.slider1 = CustomSlider(Qt.Horizontal, self)
        self.slider1.valueChanged.connect(self.slider1_changed)
        self.slider1Layout.addWidget(self.slider1)
        self.mainLayout.addLayout(self.slider1Layout)

        # Slider 2 setup for grid size control
        self.slider2Layout = QHBoxLayout()
        self.valueDisplay2 = QLabel('GridSize:0 unit', self)
        self.valueDisplay2.setFixedWidth(100)  # Set a fixed width for the display label
        self.slider2Layout.addWidget(self.valueDisplay2)
        self.slider2 = CustomSlider(Qt.Horizontal, self)
        self.slider2.valueChanged.connect(self.slider2_changed)
        self.slider2Layout.addWidget(self.slider2)
        self.mainLayout.addLayout(self.slider2Layout)

        # Buttons for adjusting grid lines spacing
        self.buttonsLayout = QHBoxLayout()
        self.button1 = QPushButton("GridDown", self)
        self.button2 = QPushButton("GridUp", self)
        self.button1.clicked.connect(self.grid_down_clicked)
        self.button2.clicked.connect(self.grid_up_clicked)
        self.buttonsLayout.addWidget(self.button1)
        self.buttonsLayout.addWidget(self.button2)
        self.mainLayout.addLayout(self.buttonsLayout)
        
        self.setupDivider()
        
        self.row1Layout = QHBoxLayout()
        self.buttonBoxMap1X1 = QPushButton("BoxMap1X1", self)
        self.buttonBoxMap2X2 = QPushButton("BoxMap2X2", self)
        self.buttonBoxMap1X1.clicked.connect(self.BoxMap1X1_clicked)
        self.buttonBoxMap2X2.clicked.connect(self.BoxMap2X2_clicked)
        self.row1Layout.addWidget(self.buttonBoxMap1X1)
        self.row1Layout.addWidget(self.buttonBoxMap2X2)
        self.mainLayout.addLayout(self.row1Layout)

        # Row 2
        self.row2Layout = QHBoxLayout()
        self.buttonBoxMap4X4 = QPushButton("BoxMap4X4", self)
        self.buttonBoxMap8X8 = QPushButton("BoxMap8X8", self)
        self.buttonBoxMap4X4.clicked.connect(self.BoxMap4X4_clicked)
        self.buttonBoxMap8X8.clicked.connect(self.BoxMap8X8_clicked)
        self.row2Layout.addWidget(self.buttonBoxMap4X4)
        self.row2Layout.addWidget(self.buttonBoxMap8X8)
        self.mainLayout.addLayout(self.row2Layout)

        # Row 3
        self.row3Layout = QHBoxLayout()
        self.buttonBoxMap16X16 = QPushButton("BoxMap16X16", self)
        self.buttonOverlapClean = QPushButton("OverlapClean", self)
        self.buttonBoxMap16X16.clicked.connect(self.BoxMap16X16_clicked)
        self.buttonOverlapClean.clicked.connect(self.OverlapClean_clicked)
        self.row3Layout.addWidget(self.buttonBoxMap16X16)
        self.row3Layout.addWidget(self.buttonOverlapClean)
        self.mainLayout.addLayout(self.row3Layout)
        
        self.setupCustomScaleRow()
        
        self.setupModelingToolkitDivider()
        
        self.setupVoxelSliceRow()
        
        self.setupSectionWithDividerAndColumns()
        
    def deselectAllItems(self, event):
        self.listWindow.clearSelection()
        event.ignore() 

    # The rest of your class methods remain unchanged...


    def slider1_changed(self, value):
        mapping = [0.125, 0.25, 0.5, 1, 2, 4, 8, 16]
        self.gridSpacingValue = mapping[value]
        grid_functions.grid_lines_control(self.gridSpacingValue)
        self.valueDisplay1.setText(f"GridUnit:{self.gridSpacingValue} cm")
        self.update_grid_size()

    def slider2_changed(self, value):
        self.gridSizeMultiplier = value
        self.update_grid_size()

    def grid_down_clicked(self):
        grid_functions.grid_down()
        self.update_grid_spacing_display()
        self.update_grid_size()

    def grid_up_clicked(self):
        grid_functions.grid_up()
        self.update_grid_spacing_display()
        self.update_grid_size()

    def setupDivider(self):
        # Left line
        leftLine = QFrame()
        leftLine.setFrameShape(QFrame.HLine)
        leftLine.setFrameShadow(QFrame.Sunken)

        # Right line
        rightLine = QFrame()
        rightLine.setFrameShape(QFrame.HLine)
        rightLine.setFrameShadow(QFrame.Sunken)

        # Label for 'UV ToolKit'
        label = QLabel('UV ToolKit')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(" margin-left: 5px; margin-right: 5px; font-size: 10pt;")

        # Layout for line and label
        dividerLayout = QHBoxLayout()
        dividerLayout.addWidget(leftLine, 1)  # Line stretches to fill space on the left
        dividerLayout.addWidget(label)        # Label stays in the middle
        dividerLayout.addWidget(rightLine, 1)  # Line stretches to fill space on the right

        # Add the divider layout to the main layout
        self.mainLayout.addLayout(dividerLayout)

    def setupModelingToolkitDivider(self):
        # Divider Title
        dividerLabel = QLabel('Modeling Toolkit')
        dividerLabel.setAlignment(Qt.AlignCenter)
        
        # Divider Lines
        line1 = QFrame(); line1.setFrameShape(QFrame.HLine); line1.setFrameShadow(QFrame.Sunken)
        line2 = QFrame(); line2.setFrameShape(QFrame.HLine); line2.setFrameShadow(QFrame.Sunken)
        
        # Divider Layout
        dividerLayout = QHBoxLayout()
        dividerLayout.addWidget(line1, 1)
        dividerLayout.addWidget(dividerLabel)
        dividerLayout.addWidget(line2, 1)
        
        # Add Divider to Main Layout
        self.mainLayout.addLayout(dividerLayout)
        
    def BoxMap1X1_clicked(self):
        UVboxmap.boxmap1X1()

    def BoxMap2X2_clicked(self):
        UVboxmap.boxmap2X2()
    
    def BoxMap4X4_clicked(self):
        UVboxmap.boxmap4X4()
    
    def BoxMap8X8_clicked(self):
        UVboxmap.boxmap8X8()
    
    def BoxMap16X16_clicked(self):
        UVboxmap.boxmap16X16()

    def OverlapClean_clicked(self):
        UVboxmap.OverlapClean()

    def setupCustomScaleRow(self):
        # Row layout
        customScaleLayout = QHBoxLayout()

        # 'Custom Scale' button instead of a label
        self.customScaleBtn = QPushButton("Custom Scale")
        self.customScaleBtn.clicked.connect(self.onCustomScaleClicked)
        customScaleLayout.addWidget(self.customScaleBtn)

        # Input fields for X, Y, Z with placeholders
        self.xInput = QLineEdit()
        self.xInput.setPlaceholderText("X")
        customScaleLayout.addWidget(self.xInput)

        self.yInput = QLineEdit()
        self.yInput.setPlaceholderText("Y")
        customScaleLayout.addWidget(self.yInput)

        self.zInput = QLineEdit()
        self.zInput.setPlaceholderText("Z")
        customScaleLayout.addWidget(self.zInput)

        # Add the row to the main layout
        self.mainLayout.addLayout(customScaleLayout)

    def onCustomScaleClicked(self):
        # Example action when 'Custom Scale' button is clicked
        # Here, you might gather the X, Y, Z values and do something with them
        x_val = float(self.xInput.text())
        y_val = float(self.yInput.text())
        z_val = float(self.zInput.text())
        
        customboxmapuv.customboxmapuv(x_val, y_val, z_val)
        print(f"Custom Scale button clicked with X: {x_val}, Y: {y_val}, Z: {z_val}")

        # Implement the desired functionality for when the button is clicked
        # This could involve reading the X, Y, Z values and applying them as needed

    def setupVoxelSliceRow(self):
        # Row Layout for Voxel Slice
        voxelSliceLayout = QHBoxLayout()
        
        # Voxel Slice Button
        voxelSliceBtn = QPushButton('Voxel Slice')
        voxelSliceBtn.clicked.connect(self.onVoxelSliceClicked)
        voxelSliceLayout.addWidget(voxelSliceBtn)
        
        # Input Slot for Voxel Slice Value
        self.voxelSliceValueInput = QLineEdit()
        voxelSliceLayout.addWidget(self.voxelSliceValueInput)
        
        # Add Row to Main Layout
        self.mainLayout.addLayout(voxelSliceLayout)

    def onVoxelSliceClicked(self):
        # Retrieve the grid size value from the input slot
        gridSizeValue = float(self.voxelSliceValueInput.text())
        # Call the grid_slice function with the retrieved value
        grid_slice.grid_slice(gridSizeValue)  # Ensure grid_slice is defined in grid_functions module


    
    def update_grid_size(self):
        if self.gridSizeMultiplier is not None:
            mapping = [0, 1, 5, 10, 15, 20, 25, 30]
            gridSizeValue = mapping[self.gridSizeMultiplier] * self.gridSpacingValue
            grid_functions.grid_size_control(gridSizeValue, gridSizeValue)
            self.valueDisplay2.setText(f"GridSize:{gridSizeValue} units")

    def update_grid_spacing_display(self):
        current_spacing = cmds.grid(query=True, spacing=True)
        self.valueDisplay1.setText(f"{current_spacing} cm")
        mapping = [0.125, 0.25, 0.5, 1, 2, 4, 8, 16]
        closest_index = mapping.index(min(mapping, key=lambda x: abs(x - current_spacing)))
        self.slider1.setValue(closest_index)


    def setupSectionWithDividerAndColumns(self):
        self.setupAdditionalDivider()
        self.setupTwoColumns()

    def setupAdditionalDivider(self):
        # Additional divider similar to setupDivider
        dividerLabel = QLabel('Shader Toolkit')
        dividerLabel.setAlignment(Qt.AlignCenter)
        
        # Divider Lines
        line1 = QFrame(); line1.setFrameShape(QFrame.HLine); line1.setFrameShadow(QFrame.Sunken)
        line2 = QFrame(); line2.setFrameShape(QFrame.HLine); line2.setFrameShadow(QFrame.Sunken)
        
        # Divider Layout
        dividerLayout = QHBoxLayout()
        dividerLayout.addWidget(line1, 1)
        dividerLayout.addWidget(dividerLabel)
        dividerLayout.addWidget(line2, 1)
        
        # Add Divider to Main Layout
        self.mainLayout.addLayout(dividerLayout)

    def setupTwoColumns(self):
        # Layout for two columns
        twoColumnsLayout = QHBoxLayout()

        # First Column with Buttons
        self.column1Layout = QVBoxLayout()
        self.getMTLButton = QPushButton("GetMTL")
        self.assignMTLButton = QPushButton("AssignMTL")
        self.allMTLButton = QPushButton("AllMTL")
        self.onIMG2MTLButton = QPushButton("IMG2MTL")
        self.boxsampleButton = QPushButton("BoxSample")
        self.ballsampleButton = QPushButton("BallSample")
        self.getMTLButton.clicked.connect(self.onGetMTLClicked)
        self.assignMTLButton.clicked.connect(self.onAssignMTLClicked)
        self.allMTLButton.clicked.connect(self.onallMTLClicked)
        self.onIMG2MTLButton.clicked.connect(self.onIMG2MTLClicked)
        self.boxsampleButton.clicked.connect(self.onboxsampleClicked)
        # Add buttons to the column layout
        self.column1Layout.addWidget(self.getMTLButton)
        self.column1Layout.addWidget(self.assignMTLButton)
        self.column1Layout.addWidget(self.allMTLButton)
        self.column1Layout.addWidget(self.onIMG2MTLButton)
        self.column1Layout.addWidget(self.boxsampleButton)
        self.column1Layout.addWidget(self.ballsampleButton)

        # Second Column with List Window
        self.listWindow = QListWidget()
        self.listWindow.setSelectionMode(QAbstractItemView.MultiSelection)
        # Allow editing of items
        self.listWindow.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.listWindow.itemDoubleClicked.connect(self.onItemDoubleClicked)  # Connect to handle double click
        self.listWindow.itemChanged.connect(self.onMaterialRenamed)  # Connect to handle item renaming(self.onItemDoubleClicked)

        # Add both columns to the layout
        twoColumnsLayout.addLayout(self.column1Layout)
        twoColumnsLayout.addWidget(self.listWindow)

        # Add the two columns layout to the main layout
        self.mainLayout.addLayout(twoColumnsLayout)

    # You can call this method to update the list dynamically
    def updateListWindow(self, itemsList):
        self.listWindow.clear()  # Clear existing items
        for itemText in itemsList:
            self.listWindow.addItem(itemText)
            
    def onGetMTLClicked(self):
        # Fetch unique materials
        unique_materials = MF.fetch_materials_selection()

        # Clear the list window
        self.listWindow.clear()

        # Iterate over unique materials
        for item_text in unique_materials:
            # Create a QListWidgetItem with the material name
            item = QListWidgetItem(item_text)
            print("Flags before setting:", item.flags())

            # Add the Qt.ItemIsEditable flag
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            print("Flags after setting:", item.flags())
            # Add the item to the list window
            self.listWindow.addItem(item)

        # Update the list window
        self.updateListWindow(unique_materials)

    
    def onAssignMTLClicked(self):
        selected_items = self.listWindow.selectedItems()
        material_name = selected_items[0].text()
        maya_selection = cmds.ls(selection=True)
        shading_groups = cmds.listConnections(f"{material_name}.outColor", type='shadingEngine')
        shading_group = shading_groups[0]
        for obj in maya_selection:
            cmds.sets(obj, edit=True, forceElement=shading_group)
            
            
    def onallMTLClicked(self):
        unique_materials_list = MF.list_all_materials()
        for item in unique_materials_list:
            self.listWindow.addItem(item)
        self.updateListWindow(unique_materials_list)
    
    def onIMG2MTLClicked(self):
        MF.convert_images_to_shaders()
    
    def onMaterialRenamed(self, item):
        new_name = item.text()
        old_name = item.data(Qt.UserRole)  # Retrieve the original material name
        # Perform the renaming operation using the MF module
        MF.rename_material(old_name, new_name)
    
    def onItemDoubleClicked(self, item):
        self.listWindow.editItem(item)
        print("Item double-clicked:", item.text())  # Print the text of the double-clicked item
        print("Item flags:", item.flags())  # Print the flags of the double-clicked item
        print("Item is editable:", bool(item.flags() & Qt.ItemIsEditable))  # Print if the item is editable
        
    def onboxsampleClicked(self):
        # Get selected items from the list window
        selected_items = self.listWindow.selectedItems()
        selected_items = list(selected_items)
        # Count the total number of selected items
        num_cubes = len(selected_items)
        grid_size = math.ceil(math.sqrt(num_cubes))
        actual_num_cubes = grid_size ** 2
        n = 0
        #grid_sample.create_cube_grid(total_selected)
        for index, item in enumerate(selected_items):
            material_name = item.text()
            print(material_name)
            xpos = n * 2
            zpos = 0
            cube = cmds.polyCube()[0]
            cmds.move(xpos, 0, zpos, cube)
            shading_groups = cmds.listConnections(f"{material_name}.outColor", type='shadingEngine')
            shading_group = shading_groups[0]
            cmds.sets(cube, edit=True, forceElement=shading_group)
            num_cubes -= 1
            n = n + 1

    
    def updateListWindow(self, itemsList):
        self.listWindow.clear()  # Clear existing items
        for itemText in itemsList:
            item = QListWidgetItem(itemText)
            item.setData(Qt.UserRole, itemText)  # Set the original material name as data
            self.listWindow.addItem(item)

               


def create_custom_slider_window():
    try:
        cmds.deleteUI('customSliderWindow', wnd=True)
    except:
        pass
    custom_slider_window = CustomSliderWindow()
    custom_slider_window.setObjectName('customSliderWindow')
    custom_slider_window.show()

create_custom_slider_window()
