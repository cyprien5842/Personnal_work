import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from maya_breakdown.vendor.Qt import QtWidgets, QtCore, QtGui
from PySide2 import QtWidgets, QtGui, QtCore


def hline_widget():
    hline = QtWidgets.QFrame()
    hline.setFrameShape(QtWidgets.QFrame.HLine)
    hline.setFrameShadow(QtWidgets.QFrame.Sunken)
    return hline

def hline_layout(label):
    layout = QtWidgets.QHBoxLayout()
    separator_label = QtWidgets.QLabel(label)
    separator_label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(hline_widget())
    layout.addWidget(separator_label)
    layout.addWidget(hline_widget())
    return layout