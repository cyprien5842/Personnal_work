import PyQt4.QtCore as qc
import PyQt4.QtGui as qg
import shower_messenger.core.userClass as userData
import customLineEdit
import customMenuBar
import sys


class MainMessageUI(qg.QWidget):
    def __init__(self, user):
        qg.QWidget.__init__(self)
        self.setWindowTitle('Shower Messenger')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setAcceptDrops(False)
        self.setMinimumSize(300, 200)

        # Init Status Bar Layout
        self.statusBarLayout = qg.QVBoxLayout()
        self.statusBarLayout.setAlignment(qc.Qt.AlignTop)

        # Init main Layout
        self.mainLayout = qg.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 5)

        # Init message Layout
        self.messageLayout = qg.QVBoxLayout()
        self.messageLayout.setAlignment(qc.Qt.AlignTop)


        # Init scroll Layout
        self.scrollLayout = qg.QVBoxLayout()

        # Init input Layout
        self.inputLayout = qg.QVBoxLayout()
        self.inputLayout.setAlignment(qc.Qt.AlignBottom)

        # Init status Bar
        self.menuBar = customMenuBar.inputMenuBar()
        self.mainLayout.addWidget(self.menuBar)

        # Init ScrollAreaWidget
        self.scrollWidget = qg.QWidget()
        self.scroll = qg.QScrollArea()

        self.scroll.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scrollLayout.addWidget(self.scroll)
        self.scrollLayout.setContentsMargins(5, 0, 5, 0)

        # Init Input Text
        self.inputMessage = customLineEdit.InputLineEdit(user, self.messageLayout, self.scrollWidget, self.scroll)
        self.scroll.setWidget(self.scrollWidget)
        self.scroll.setFocus()

        # Init Input message
        self.inputLayout.addWidget(self.inputMessage)

        # Set Layout
        self.mainLayout.addLayout(self.scrollLayout)
        self.mainLayout.addLayout(self.inputLayout)
        self.mainLayout.setSpacing(5)
        self.setLayout(self.mainLayout)


if __name__ == "__main__":
    user = userData.UserPref("Cyprien")
    app = qg.QApplication(sys.argv)
    main_window = MainMessageUI(user)
    main_window.show()
    sys.exit(app.exec_())