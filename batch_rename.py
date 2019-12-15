import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self, width=400, height=350):
        super().__init__()
        self.setWindowTitle('Batch Renamer')
        self.setFixedSize(width, height)

        self.sep_dict = {"underscore":"_", "hyphen":"-", "period":".", "space":" "}
        self.enum_dict = {"numbers":"1", "letters":"a"}

        self.createWidgets()
        self.arrangeWidgets()
        self.makeConnections()

    def createWidgets(self):
        self.selected_folder = QLabel()
        self.folder_dialog = QFileDialog(self)
        #self.folder_dialog.setDirectory(os.getenv('HOME'))
        self.folder_dialog.setDirectory(os.path.join(os.getenv('HOME'),"Desktop","Test"))
        self.folder_dialog.setFileMode(QFileDialog.Directory)
        self.folder_button = QPushButton("&Choose Folder")

        #file types
        self.images = QCheckBox("&Images")
        self.videos = QCheckBox("&Videos")

        self.new_name_label = QLabel("&Filename template")
        self.new_name = QLineEdit()
        self.new_name_label.setBuddy(self.new_name)

        self.l_unique_separator = QLabel("&Separator")
        self.unique_separator = QComboBox(self)
        self.unique_separator.addItems(list(self.sep_dict.keys()))
        self.l_unique_separator.setBuddy(self.unique_separator)

        self.l_unique_enum = QLabel("&Enumerator")
        self.unique_enumerator = QComboBox(self)
        self.unique_enumerator.addItems(list(self.enum_dict.keys()))
        self.l_unique_enum.setBuddy(self.unique_enumerator)

        self.paranthesize_enum = QCheckBox("&Paranthesize enumerator")

        self.example_name = QLabel()
        self.submit = QPushButton("Rename!")

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

        form = QFormLayout()
        form.addRow(self.new_name_label, self.new_name)
        form.addRow(self.l_unique_separator, self.unique_separator)
        form.addRow(self.l_unique_enum, self.unique_enumerator)
        form.addWidget(self.paranthesize_enum)
        main.addLayout(form)

        example_name_layout = QHBoxLayout()
        example_name_layout.addWidget(QLabel("Example filename: "))
        example_name_layout.addWidget(self.example_name)
        example_name_layout.addStretch(1)
        main.addLayout(example_name_layout)

        main.addStretch(1)
        main.addWidget(self.submit)
        self.setLayout(main)

    def update_example(self):
        name = self.new_name.text()
        sep = self.sep_dict[self.unique_separator.currentText()]
        enum = self.enum_dict[self.unique_enumerator.currentText()]
        if self.paranthesize_enum.checkState():
            enum = f"({enum})"
        self.example_name.setText(name+sep+enum)

    def makeConnections(self):
        self.folder_button.clicked.connect(self.folder_dialog.show)
        self.folder_dialog.currentChanged.connect(self.selected_folder.setText)

        self.new_name.textChanged.connect(self.update_example)
        self.unique_separator.currentIndexChanged.connect(self.update_example)
        self.unique_enumerator.currentIndexChanged.connect(self.update_example)
        self.paranthesize_enum.stateChanged.connect(self.update_example)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())