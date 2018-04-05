# Standart import
import os
import sys
import pymel.core as pmc

# Custom import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import maya_breakdown.mbcore as mbcore
import maya_breakdown.hline as hline
reload(hline)
reload(mbcore)
from maya_breakdown.vendor.Qt import QtWidgets, QtCore, QtGui
from PySide2 import QtWidgets, QtGui, QtCore


class MayaBreakdownUI(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.desktop()):
        super(MayaBreakdownUI, self).__init__(parent)
        self.setWindowTitle('Maya Breakdown Generator')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedHeight(190)
        self.setFixedWidth(300)

        # Validator for int value
        self.only_int = QtGui.QIntValidator()

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Combo Box Layout
        self.combo_box_layout = QtWidgets.QHBoxLayout()

        # Mode Separator
        self.mode_separator_layout = hline.hline_layout("Mode")

        # Combo Box Widgets
        self.mode_label = QtWidgets.QLabel("Mode :")

        self.cbox_mode = QtWidgets.QComboBox()
        self.cbox_mode.addItem("Bounding_box")
        self.cbox_mode.addItem("Top_to_the_bottom")
        self.cbox_mode.addItem("Bottom_to_the_top")

        self.combo_box_layout.addWidget(self.mode_label)
        self.combo_box_layout.addWidget(self.cbox_mode)

        # Option Separator
        self.option_separator_layout = hline.hline_layout("Options")

        # Option Layout
        self.option_layout = QtWidgets.QHBoxLayout()

        # Option Widgets
        self.visible_check_box = QtWidgets.QCheckBox("Visible/Invisible effect")
        self.visible_check_box.stateChanged.connect(self.update_current_option_mode)
        self.offset_input_label = QtWidgets.QLabel("Transform offset :")
        self.offset_input = QtWidgets.QLineEdit()
        self.offset_input.setText("1000")
        self.offset_input.setValidator(self.only_int)

        self.option_layout.addWidget(self.visible_check_box)
        self.option_layout.addWidget(self.offset_input_label)
        self.option_layout.addWidget(self.offset_input)

        # Frame Range Separator
        self.frame_range_separator_layout = hline.hline_layout("Frame Range")

        # Frame Range Layout
        self.frame_range_layout = QtWidgets.QHBoxLayout()

        # Frame Range Widgets
        self.frame_range_label = QtWidgets.QLabel("Time (seconds) :")
        self.frame_range_input = QtWidgets.QLineEdit()
        self.frame_range_input.setText("0")
        self.frame_range_input.setFixedWidth(30)

        self.frame_range_input.setValidator(self.only_int)
        self.frame_range_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.frame_range_slider.setMaximum(50)

        # Connection
        self.frame_range_slider.valueChanged.connect(lambda value: self.frame_range_input.setText(str(value)))
        self.frame_range_input.textChanged.connect(lambda value: self.frame_range_slider.setValue(int(value)))

        self.frame_range_layout.addWidget(self.frame_range_label)
        self.frame_range_layout.addWidget(self.frame_range_input)
        self.frame_range_layout.addWidget(self.frame_range_slider)

        # Progress Bar Layout
        self.progress_layout = QtWidgets.QHBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_layout.addWidget(self.progress_bar)

        # Button Layout
        self.button_layout = QtWidgets.QHBoxLayout()

        # Buttons widgets
        self.button_validate = QtWidgets.QPushButton("Validate")
        self.button_undo = QtWidgets.QPushButton("Undo")
        self.button_close = QtWidgets.QPushButton("Close")

        self.button_validate.clicked.connect(self.apply)
        self.button_undo.clicked.connect(self.undo)
        self.button_close.clicked.connect(self.close)

        self.button_layout.addWidget(self.button_validate)
        self.button_layout.addWidget(self.button_undo)
        self.button_layout.addWidget(self.button_close)
        self.button_layout.setAlignment(QtCore.Qt.AlignBottom)

        # Creation of the main layout
        self.main_layout.addLayout(self.mode_separator_layout)
        self.main_layout.addLayout(self.combo_box_layout)
        self.main_layout.addLayout(self.option_separator_layout)
        self.main_layout.addLayout(self.option_layout)
        self.main_layout.addLayout(self.frame_range_separator_layout)
        self.main_layout.addLayout(self.frame_range_layout)
        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

    def apply(self):
        setting_dictionnary = {}
        setting_dictionnary['mode'] = self.cbox_mode.currentText()
        setting_dictionnary['time'] = int(self.frame_range_input.text())
        if self.visible_check_box.isChecked():
            setting_dictionnary['visible'] = True
            setting_dictionnary['attribute'] = "visibility"
            setting_dictionnary['offset'] = 0
        else:
            setting_dictionnary['visible'] = False
            setting_dictionnary['attribute'] = "translateY"
            setting_dictionnary['offset'] = int(self.offset_input.text())
        self.action = mbcore.do_the_breakdown(setting_dictionnary, self.progress_bar)

    def undo(self):
        if self.action:
            mbcore.undo(self.action, self.progress_bar)
        else:
            pmc.warning("Please, do a breakdown !")

    def update_current_option_mode(self):
        if self.visible_check_box.isChecked():
            self.offset_input_label.setVisible(False)
            self.offset_input.setVisible(False)
        else:
            self.offset_input_label.setVisible(True)
            self.offset_input.setVisible(True)


def show_window():
    ui = MayaBreakdownUI()
    ui.show()
