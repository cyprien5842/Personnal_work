from PySide2 import QtWidgets, QtCore, QtGui
import sys
import json
import re
import os.path

class simpleUI(QtWidgets.QDialog):
    """
    That is a little script which saves and stores data user information in JSON with PyQt interface.
    These informations can be used in Maya/Nuke and other software.
    """
    def __init__(self, parent=QtWidgets.QApplication.desktop()):
        super(simpleUI, self).__init__(parent)
        self.setWindowTitle('Configuration')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        
        myLayout = QtWidgets.QVBoxLayout()
        self.setLayout(myLayout)
        myLayout.setContentsMargins(10, 10, 10, 5)
        myLayout.setSpacing(15)
        
        myformLayout = QtWidgets.QFormLayout()
        
        self.name_le = QtWidgets.QLineEdit()
        self.phone_number_le = QtWidgets.QLineEdit()
        self.email_le = QtWidgets.QLineEdit()
        
        reg_ex_phone_number = QtCore.QRegExp("^0[6-7]([ .-]?[0-9]{2}){4}$")
        phone_number_validator = QtGui.QRegExpValidator(reg_ex_phone_number, self.phone_number_le)
        self.phone_number_le.setValidator(phone_number_validator)
        
        myformLayout.addRow("Username :", self.name_le)
        myformLayout.addRow("Phone Number :", self.phone_number_le)
        myformLayout.addRow("Email :", self.email_le)
        
        myLabelLayout = QtWidgets.QHBoxLayout()
        
        self.message_label = QtWidgets.QLabel('')
        self.style_sheet =""
        self.message_label.setStyleSheet(self.style_sheet)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setVisible(False)
        
        myLabelLayout.addWidget(self.message_label)
                
        myButtonLayout = QtWidgets.QHBoxLayout()
        
        bttn_close = QtWidgets.QPushButton('Close')
        bttn_val = QtWidgets.QPushButton('Apply')
        
        myButtonLayout.addWidget(bttn_close)
        myButtonLayout.addWidget(bttn_val)
        
        myLayout.addLayout(myformLayout)
        myLayout.addLayout(myLabelLayout)
        myLayout.addLayout(myButtonLayout)
        
        bttn_close.clicked.connect(self.close)
        bttn_val.clicked.connect(self.saveConfiguration)
        
        self.loadConfiguration()
        
    #----------------------------------------------------------------------#

    def jsonEmplacement(self):
        return os.environ["TMP"]
        
    def saveConfiguration(self):
        name = str(self.name_le.text())
        number = str(self.phone_number_le.text())
        mail = str(self.email_le.text())

        if not (name and number and mail) or "@" not in mail or not re.match("^0[6-7]([ .-]?[0-9]{2}){4}$", number):
            error = " "
            self.style_sheet = "color: rgb(170, 0, 0); \
                      font-size: 10pt; \
                      font-weight: bold;"
            self.message_label.setStyleSheet(self.style_sheet)
            
            if "@" not in mail:
                error = "(Wrong mail)"
            
            if not re.match("^0[6-7]([ .-]?[0-9]{2}){4}$", number):
                error += "(Wrong number)"
            self.message_label.setText('Houston, we have a problem !%s' %(error))
            self.message_label.setVisible(True)
            return
        
        data = {}
        data['name'] = name
        data['number'] = number
        data['mail'] = mail
        
        with open("{0}\{1}".format(self.jsonEmplacement(), "data.json"), 'w') as outfile:
            json.dump(data, outfile)
        
        self.message_label.setText('Your data have been saved with success !')
        self.style_sheet = "color: rgb(0, 170, 0); \
                      font-size: 10pt; \
                      font-weight: bold;"
        self.message_label.setStyleSheet(self.style_sheet)
        self.message_label.setVisible(True)
                
    #----------------------------------------------------------------------#
    
    def loadConfiguration(self):
        if os.path.isfile("{0}\{1}".format(self.jsonEmplacement(), "data.json")):
            with open("{0}\{1}".format(self.jsonEmplacement(), "data.json")) as json_data:
                data = json.load(json_data)
                
            self.name_le.setText(data['name'])
            self.phone_number_le.setText(data['number'])
            self.email_le.setText(data['mail'])
        
    #----------------------------------------------------------------------#

def main():
    main_window = simpleUI()
    main_window.show()