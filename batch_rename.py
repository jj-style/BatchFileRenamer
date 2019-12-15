import sys, os, string, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

IMG_EXT = set(["png","jpg","jpeg","tiff","gif","bmp"])
VID_EXT = set(["mp4","mov","avi","mkv","flv","m4v","mpg","mpeg","wmv"])
AUD_EXT = set(["mp3","ogg","wav","wma","m4a"])

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
        self.folder_dialog.setDirectory(os.getenv('HOME'))
        self.folder_dialog.setFileMode(QFileDialog.Directory)
        self.folder_button = QPushButton("&Choose Folder")

        #file types
        self.images = QCheckBox("&Images")
        self.videos = QCheckBox("&Videos")
        self.audio = QCheckBox("&Audio")

        self.custom = QCheckBox("&Other extensions")
        self.custom_extensions = QLineEdit(self)
        self.custom_extensions.setEnabled(False)
        self.custom_extensions.setToolTip("Comma delimited extensions")

        self.new_name = QLineEdit(self)
        self.new_name.setToolTip("General name for all files")

        self.unique_separator = QComboBox(self)
        self.unique_separator.addItems(list(self.sep_dict.keys()))

        self.unique_enumerator = QComboBox(self)
        self.unique_enumerator.addItems(list(self.enum_dict.keys()))

        self.paranthesize_enum = QCheckBox("&Paranthesize enumerator")

        self.example_name = QLabel()
        self.submit = QPushButton("&Rename!")

        self.completed_dialog = QMessageBox()

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
        filetype_layout.addWidget(self.audio)
        filetype_layout.addStretch(1)
        main.addLayout(filetype_layout)

        form = QFormLayout()
        form.addRow(self.custom, self.custom_extensions)
        form.addRow("&Filename template", self.new_name)
        form.addRow("&Separator", self.unique_separator)
        form.addRow("&Enumerator", self.unique_enumerator)
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

    def makeConnections(self):
        self.folder_button.clicked.connect(self.folder_dialog.show)
        self.folder_dialog.directoryEntered.connect(self.selected_folder.setText)

        self.custom.stateChanged.connect(self.custom_extensions.setEnabled)

        self.new_name.textChanged.connect(self.update_example)
        self.unique_separator.currentIndexChanged.connect(self.update_example)
        self.unique_enumerator.currentIndexChanged.connect(self.update_example)
        self.paranthesize_enum.stateChanged.connect(self.update_example)

        self.submit.clicked.connect(self.rename)

    def update_example(self):
        name = self.new_name.text()
        sep = self.sep_dict[self.unique_separator.currentText()]
        enum = self.enum_dict[self.unique_enumerator.currentText()]
        if self.paranthesize_enum.checkState():
            enum = f"({enum})"
        self.example_name.setText(name+sep+enum+".ext")

    def rename(self):
        name = self.new_name.text()
        sep = self.sep_dict[self.unique_separator.currentText()]
        enum = self.unique_enumerator.currentText()
        exts = []
        exts += (x for x in IMG_EXT if self.images.checkState())
        exts += (x for x in VID_EXT if self.videos.checkState())
        exts += (x for x in AUD_EXT if self.audio.checkState())
        if self.custom.checkState():
            custom_extensions = self.custom_extensions.text().split(",")
            custom_extensions = [x for x in custom_extensions if x]
            custom_extensions = [re.sub("[^a-z]","", x.lower()) for x in custom_extensions]
            exts += custom_extensions
            exts = set(exts)
        try:
            count = 0
            for file in os.listdir(self.selected_folder.text()):
                extension = file.rpartition(".")[-1].lower()
                if extension in exts:
                    if enum == "numbers":
                        next_enum = count + 1
                    elif enum == "letters":
                        next_enum = string.ascii_lowercase[count%26]
                        if count // 26 > 0:
                            next_enum += string.ascii_lowercase[count//26]
                    if self.paranthesize_enum.checkState():
                        next_enum = f"({next_enum})"
                    old_file = os.path.join(self.selected_folder.text(), file)
                    new_file = os.path.join(self.selected_folder.text(), name+sep+str(next_enum)+f".{extension}")
                    os.rename(old_file, new_file)
                    count += 1
            
            self.show_finished_dialog(count)

        except FileNotFoundError as error:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error!")
            error_dialog.setText(error.args[1])
            error_dialog.show()

    def show_finished_dialog(self, count):
        if count > 0:
            self.completed_dialog.setIcon(QMessageBox.Information)
        else:
            self.completed_dialog.setIcon(QMessageBox.Warning)
        self.completed_dialog.setWindowTitle("Renaming finished")
        self.completed_dialog.setText(f"{count} files renamed.")
        self.completed_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())