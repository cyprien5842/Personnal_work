# Standart import
import os
import sys

# Custom import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import maya_breakdown.mbcore as mbcore
from maya_breakdown.vendor.Qt import QtWidgets, QtCore, QtGui
#from PyQt5 import QtWidgets, QtGui, QtCore

class MayaBreakdownUI(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.desktop()):
        super(MayaBreakdownUI, self).__init__(parent)
        self.setWindowTitle('Maya Breakdown Generator')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(100)
        self.setFixedWidth(300)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Combo Box Layout
        self.combo_box_layout = QtWidgets.QHBoxLayout()

        # Combo Box Widgets
        self.mode_label = QtWidgets.QLabel("Mode :")

        self.cbox_mode = QtWidgets.QComboBox()
        self.cbox_mode.addItem("Bounding_box")
        self.cbox_mode.addItem("Top_to_the_bottom")
        self.cbox_mode.addItem("Bottom_to_the_top")

        self.combo_box_layout.addWidget(self.mode_label)
        self.combo_box_layout.addWidget(self.cbox_mode)

        # Check Box Layout
        self.check_box_layout = QtWidgets.QHBoxLayout()

        # Check Box Widgets
        self.visible_check_box = QtWidgets.QCheckBox("Visible/Invisible effect")
        self.check_box_layout.addWidget(self.visible_check_box)

        # Frame Range Layout
        self.frame_range_layout = QtWidgets.QHBoxLayout()

        # Frame Range Widgets
        self.frame_range_label = QtWidgets.QLabel("Time (seconds) :")
        self.frame_range_input = QtWidgets.QLineEdit()
        self.frame_range_input.setText("0")
        self.frame_range_input.setFixedWidth(30)

        # Validator for int value
        self.only_int = QtGui.QIntValidator()
        self.frame_range_input.setValidator(self.only_int)
        self.frame_range_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.frame_range_slider.setMaximum(50)

        # Connection
        self.frame_range_slider.valueChanged.connect(lambda value: self.frame_range_input.setText(str(value)))
        self.frame_range_input.textChanged.connect(lambda value: self.frame_range_slider.setValue(int(value)))

        self.frame_range_layout.addWidget(self.frame_range_label)
        self.frame_range_layout.addWidget(self.frame_range_input)
        self.frame_range_layout.addWidget(self.frame_range_slider)

        # Button Layout
        self.button_layout = QtWidgets.QHBoxLayout()

        # Buttons widgets
        self.button_validate = QtWidgets.QPushButton("Validate")
        self.button_close = QtWidgets.QPushButton("Close")

        self.button_validate.clicked.connect(self.apply)
        self.button_close.clicked.connect(self.close)

        self.button_layout.addWidget(self.button_validate)
        self.button_layout.addWidget(self.button_close)
        self.button_layout.setAlignment(QtCore.Qt.AlignBottom)

        # Creation of the main layout
        self.main_layout.addLayout(self.combo_box_layout)
        self.main_layout.addLayout(self.check_box_layout)
        self.main_layout.addLayout(self.frame_range_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

    def apply(self):
        mode_value = self.cbox_mode.currentText()
        if self.visible_check_box.isChecked():
            visible_value = True
        else:
            visible_value = False
        time_value = int(self.frame_range_input.text())
        mbcore.do_the_breakdown(mode=mode_value, visible=visible_value, time=time_value)


def show_window():
    ui = MayaBreakdownUI()
    ui.show()
