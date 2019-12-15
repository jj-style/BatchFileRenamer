import sys, os
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
        self.selected_folder = QLabel()
        self.folder_dialog = QFileDialog(self)
        self.folder_dialog.setFileMode(QFileDialog.Directory)
        self.folder_button = QPushButton("&Choose Folder")

        #file types
        self.images = QCheckBox("&Images")
        self.videos = QCheckBox("&Videos")

        self.new_name_label = QLabel("&Filename template")
        self.new_name = QLineEdit()
        self.new_name_label.setBuddy(self.new_name)

    def arrangeWidgets(self):
        main = QVBoxLayout()

        selected = QHBoxLayout()
        selected.addWidget(QLabel("Selected folder: "))
        selected.addWidget(self.selected_folder)
        selected.addStretch(1)
        main.addLayout(selected)

        main.addWidget(self.folder_button)
        filetype_layout = QHBoxLayout()
        filetype_layout.addStretch(1)
        filetype_layout.addWidget(self.images)
        filetype_layout.addWidget(self.videos)
        filetype_layout.addStretch(1)
        main.addLayout(filetype_layout)

        new_name_layout = QHBoxLayout()
        new_name_layout.addWidget(self.new_name_label)
        new_name_layout.addWidget(self.new_name)

        main.addLayout(new_name_layout)
        main.addWidget(self.new_name)
        main.addStretch(1)
        self.setLayout(main)

    def makeConnections(self):
        self.folder_button.clicked.connect(self.folder_dialog.show)
        self.folder_dialog.currentChanged.connect(self.selected)
        self.folder_dialog.currentChanged.connect(self.selected_folder.setText)

    def selected(self, path):
        print("selected: {}".format(path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())