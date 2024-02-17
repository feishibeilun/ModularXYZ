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

from PySide2.QtWidgets import QMainWindow, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPainter
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import grid_functions  # Ensure grid_functions.py is in the correct path

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
        self.setGeometry(100, 100, 400, 100)
        self.gridSpacingValue = 0.125  # Default starting value
        self.gridSizeMultiplier = 0  # Initialize multiplier
        self.initUI()

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

def create_custom_slider_window():
    try:
        cmds.deleteUI('customSliderWindow', wnd=True)
    except:
        pass
    custom_slider_window = CustomSliderWindow()
    custom_slider_window.setObjectName('customSliderWindow')
    custom_slider_window.show()

create_custom_slider_window()
