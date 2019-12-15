import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self, width=400, height=250):
        super().__init__()
        self.setWindowTitle('Batch Renamer')
        self.setFixedSize(width, height)
        self.createWidgets()
        self.arrangeWidgets()
        self.makeConnections()

    def createWidgets(self):
        pass

    def arrangeWidgets(self):
        pass

    def makeConnections(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())