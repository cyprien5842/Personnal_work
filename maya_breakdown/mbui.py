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
try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except ImportError:
    from PySide2 import QtWidgets, QtGui, QtCore

class MayaBreakdownUI(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.desktop()):
        super(MayaBreakdownUI, self).__init__(parent)
        self.setWindowTitle('Maya Breakdown Generator')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Validator for int value
        self.only_int = QtGui.QIntValidator()

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Selection Separator
        self.selection_separator_layout = hline.hline_layout("Selection")

        # Selection Layout
        self.selection_layout = QtWidgets.QHBoxLayout()

        # Selection Widget
        self.select_group_radio_btn = QtWidgets.QButtonGroup()
        self.select_all_radio_btn = QtWidgets.QRadioButton("All")
        self.select_group_radio_btn.addButton(self.select_all_radio_btn)
        self.select_current_radio_btn = QtWidgets.QRadioButton("Current selection")
        self.select_group_radio_btn.addButton(self.select_current_radio_btn)


        self.select_all_radio_btn.setChecked(True)

        self.selection_layout.addWidget(self.select_all_radio_btn)
        self.selection_layout.addWidget(self.select_current_radio_btn)

        # Mode Layout
        self.combo_box_layout = QtWidgets.QHBoxLayout()

        # Mode Separator
        self.mode_separator_layout = hline.hline_layout("Mode")

        # Combo Box Widgets
        self.mode_label = QtWidgets.QLabel("Mode :")

        self.cbox_mode = QtWidgets.QComboBox()
        self.cbox_mode.addItem("Bounding_box")
        self.cbox_mode.addItem("Top_to_bottom")
        self.cbox_mode.addItem("Depth")

        self.cbox_mode.currentTextChanged.connect(self.update_current_mode)

        self.combo_box_layout.addWidget(self.mode_label)
        self.combo_box_layout.addWidget(self.cbox_mode)

        # Option Separator
        self.option_separator_layout = hline.hline_layout("Options")

        # Option Layout
        self.option_layout = QtWidgets.QHBoxLayout()

        # Option Widgets
        self.option_group_radio_btn = QtWidgets.QButtonGroup()
        self.visible_radio_btn = QtWidgets.QRadioButton("Visible/Invisible effect")
        self.option_group_radio_btn.addButton(self.visible_radio_btn)
        self.translate_radio_btn = QtWidgets.QRadioButton("Translate effect")
        self.option_group_radio_btn.addButton(self.translate_radio_btn)

        self.translate_radio_btn.setChecked(True)
        self.translate_radio_btn.toggled.connect(self.update_current_option_mode)

        self.option_layout.addWidget(self.translate_radio_btn)
        self.option_layout.addWidget(self.visible_radio_btn)

        # Axis depth layout
        self.axis_depth_layout = QtWidgets.QHBoxLayout()

        # Axis depth widget
        self.axis_depth_label = QtWidgets.QLabel("Axis of depth :")
        self.axis_depth_cbox = QtWidgets.QComboBox()
        self.axis_depth_cbox.addItem("translateX")
        self.axis_depth_cbox.addItem("translateZ")
        self.axis_depth_label.setVisible(False)
        self.axis_depth_cbox.setVisible(False)

        self.axis_depth_layout.addWidget(self.axis_depth_label)
        self.axis_depth_layout.addWidget(self.axis_depth_cbox)


        # Reverse effect layout
        self.reverse_effect_layout = QtWidgets.QHBoxLayout()

        # Reverse effect widgets
        self.reverse_effect_checkbox = QtWidgets.QCheckBox("Reverse Effect")
  
        self.reverse_effect_layout.addWidget(self.reverse_effect_checkbox)

        # Transform offset layout
        self.transform_offset_layout = QtWidgets.QHBoxLayout()

        # Transform offset widgets
        self.offset_input_label = QtWidgets.QLabel("Transform offset :")

        self.offset_input = QtWidgets.QLineEdit()
        self.offset_input.setText("1000")
        self.offset_input.setValidator(self.only_int)

        self.transform_offset_layout.addWidget(self.offset_input_label)
        self.transform_offset_layout.addWidget(self.offset_input)

        # Transform direction layout
        self.transform_direction_layout = QtWidgets.QHBoxLayout()

        # Transform direction widgets
        self.translate_direction_label = QtWidgets.QLabel("Translate direction :")
        self.translate_direction_cbox = QtWidgets.QComboBox()
        self.translate_direction_cbox.addItem("translateX")
        self.translate_direction_cbox.addItem("translateY")
        self.translate_direction_cbox.addItem("translateZ")

        self.transform_direction_layout.addWidget(self.translate_direction_label)
        self.transform_direction_layout.addWidget(self.translate_direction_cbox)

        # Camera turn around layout
        self.camera_turn_around_layout = QtWidgets.QHBoxLayout()

        # Transform direction widgets
        self.camera_turn_around_check_box = QtWidgets.QCheckBox("Create turn around camera ")
        self.camera_turn_around_layout.addWidget(self.camera_turn_around_check_box)

        # Frame Range Separator
        self.frame_range_separator_layout = hline.hline_layout("Frame Range")

        # Current frame Range Layout
        self.current_frame_range_layout = QtWidgets.QHBoxLayout()

        # Current frame range Widget
        self.current_frame_checkbox = QtWidgets.QCheckBox("Use current frame range")
        self.current_frame_range_layout.addWidget(self.current_frame_checkbox)

        # Current frame range connection
        self.current_frame_checkbox.stateChanged.connect(self.update_frame_range_option)

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


        # Frame Range Connection
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
        self.main_layout.addLayout(self.selection_separator_layout)
        self.main_layout.addLayout(self.selection_layout)
        self.main_layout.addLayout(self.mode_separator_layout)
        self.main_layout.addLayout(self.combo_box_layout)
        self.main_layout.addLayout(self.option_separator_layout)
        self.main_layout.addLayout(self.option_layout)
        self.main_layout.addLayout(self.axis_depth_layout)
        self.main_layout.addLayout(self.reverse_effect_layout)
        self.main_layout.addLayout(self.transform_offset_layout)
        self.main_layout.addLayout(self.transform_direction_layout)
        #self.main_layout.addLayout(self.camera_turn_around_layout)
        self.main_layout.addLayout(self.frame_range_separator_layout)
        self.main_layout.addLayout(self.current_frame_range_layout)
        self.main_layout.addLayout(self.frame_range_layout)
        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.setFixedSize(self.main_layout.sizeHint())

    def apply(self):
        setting_dictionnary = {}
        setting_dictionnary['mode'] = self.cbox_mode.currentText()
        setting_dictionnary['selection'] = self.select_group_radio_btn.checkedButton().text()
        setting_dictionnary['axis_depth'] = self.axis_depth_cbox.currentText()
        setting_dictionnary['reverse_effect'] = self.reverse_effect_checkbox.isChecked()

        if self.current_frame_checkbox.isChecked():
            start_frame = int(pmc.playbackOptions(animationStartTime=True, query=True))
            end_frame = int(pmc.playbackOptions(animationEndTime=True, query=True))
            setting_dictionnary['time'] = (start_frame, end_frame)
        else:
            setting_dictionnary['time'] = int(self.frame_range_input.text())
        if self.visible_radio_btn.isChecked():
            setting_dictionnary['visible'] = True
            setting_dictionnary['attribute'] = "visibility"
            setting_dictionnary['offset'] = 0
        else:
            setting_dictionnary['visible'] = False
            setting_dictionnary['attribute'] = self.translate_direction_cbox.currentText()
            setting_dictionnary['offset'] = int(self.offset_input.text())

        if self.camera_turn_around_check_box.isChecked():
            setting_dictionnary['camera'] = True
        else:
            setting_dictionnary['camera'] = False
        self.action = mbcore.do_the_breakdown(setting_dictionnary, self.progress_bar)

    def undo(self):
        if self.action:
            mbcore.undo(self.action, self.progress_bar)
        else:
            pmc.warning("Please, do a breakdown !")


    def update_current_option_mode(self):
        if self.translate_radio_btn.isChecked():
            self.offset_input_label.setVisible(True)
            self.offset_input.setVisible(True)
            self.translate_direction_label.setVisible(True)
            self.translate_direction_cbox.setVisible(True)
        else:
            self.offset_input_label.setVisible(False)
            self.offset_input.setVisible(False)
            self.translate_direction_label.setVisible(False)
            self.translate_direction_cbox.setVisible(False)

    def update_current_mode(self):
        if self.cbox_mode.currentText() in ['Depth']:
            self.axis_depth_label.setVisible(True)
            self.axis_depth_cbox.setVisible(True)
        else:
            self.axis_depth_label.setVisible(False)
            self.axis_depth_cbox.setVisible(False)

    def update_frame_range_option(self):
        if self.current_frame_checkbox.isChecked():
            self.frame_range_label.setVisible(False)
            self.frame_range_input.setVisible(False)
            self.frame_range_slider.setVisible(False)
        else:
            self.frame_range_label.setVisible(True)
            self.frame_range_input.setVisible(True)
            self.frame_range_slider.setVisible(True)


def show_window():
    ui = MayaBreakdownUI()
    ui.show()
