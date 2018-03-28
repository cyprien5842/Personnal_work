# Standart import
import os
import sys

# Custom import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import maya_breakdown.mbcore as mbcore
from maya_breakdown.vendor.Qt import QtWidgets, QtCore, QtGui


class MayaBreakdownUI(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.desktop()):
        super(MayaBreakdownUI, self).__init__(parent)
        self.setWindowTitle('Maya Breakdown Generator')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(60)
        self.setFixedWidth(300)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Combo Box Layout
        self.combo_box_layout = QtWidgets.QHBoxLayout()

        # Combo Box widgets
        self.cbox_mode = QtWidgets.QComboBox()
        self.cbox_mode.addItem("Bounding_box")
        self.cbox_mode.addItem("Top_to_the_bottom")
        self.cbox_mode.addItem("Bottom_to_the_top")

        self.mode_label = QtWidgets.QLabel("Mode :")

        self.combo_box_layout.addWidget(self.mode_label)
        self.combo_box_layout.addWidget(self.cbox_mode)

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
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

    def apply(self):
        mbcore.do_the_breakdown(self.cbox_mode.currentText())


def show_window():
    ui = MayaBreakdownUI()
    ui.show()
