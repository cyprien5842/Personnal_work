from ui import mainWindow
from core import userClass
import sys
import PyQt4.QtGui as qg

if __name__ == "__main__":
    user = userClass.UserPref("Cyprien")
    app = qg.QApplication(sys.argv)
    main_window = mainWindow.MainMessageUI(user)
    main_window.show()
    sys.exit(app.exec_())