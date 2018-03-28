import PyQt4.QtCore as qc
import PyQt4.QtGui as qg
import functools

class InputLineEdit(qg.QLineEdit):
    def __init__(self, user, layout, scrollWidget, scroll):
        qg.QWidget.__init__(self)
        self.initMessage = qg.QLabel()
        self.initMessage.setText("Welcome {0} into Shower Messenger !".format(user.username))
        layout.addWidget(self.initMessage)
        scrollWidget.setLayout(layout)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setContentsMargins(5, 5, 5, 5)
        self.setFocus()

        self.returnPressed.connect(functools.partial(self.search_slot, user, layout, scroll))

    def search_slot(self, user, layout, scroll):
        message = qg.QLabel()
        if self.text():
            text = u"{0} : {1}".format(user.username, self.text())
            message.setText(text)
            layout.addWidget(message)
            self.setText("")
            scrollBar = scroll.verticalScrollBar()
            scrollBar.rangeChanged.connect(lambda: scrollBar.setValue(scrollBar.maximum()))

    def dragEnterEvent(self, eventQDragEnterEvent):
        print "Enter"

    def dropEvent(self, eventQDropEvent):
        print "Drop"