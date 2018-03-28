import PyQt4.QtCore as qc
import PyQt4.QtGui as qg


class inputMenuBar(qg.QMenuBar):
    def __init__(self):
        qg.QWidget.__init__(self)

        # Set Action
        self.exitAction = qg.QAction("&Exit", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qg.qApp.quit)

        #Set Menu
        self.fileMenu = self.addMenu("&File")
        self.fileMenu.addAction(self.exitAction)
        self.SettingsMenu = self.addMenu("&Settings")
        self.AboutMenu = self.addMenu("&About")

