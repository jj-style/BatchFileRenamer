import sys, os, string, re, itertools
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
        # creates all the widgets used in the application

        # widgets to popup folder browser dialog
        self.selected_folder = QLabel(self)
        self.folder_dialog = QFileDialog(self)
        self.folder_dialog.setDirectory(os.getenv('HOME'))
        self.folder_dialog.setFileMode(QFileDialog.Directory)
        self.folder_button = QPushButton("&Choose Folder")

        # file types
        self.images = QCheckBox("&Images")
        self.videos = QCheckBox("&Videos")
        self.audio = QCheckBox("&Audio")

        # input for custom file extensions
        self.custom = QCheckBox("&Other extensions")
        self.custom_extensions = QLineEdit(self)
        self.custom_extensions.setEnabled(False)
        self.custom_extensions.setToolTip("Comma delimited extensions")

        # new name for files
        self.new_name = QLineEdit(self)
        self.new_name.setToolTip("General name for all files")

        # separator between filename and enumerator
        self.unique_separator = QComboBox(self)
        self.unique_separator.addItems(list(self.sep_dict.keys()))

        # enumerator for files (i.e. increasing number)
        self.unique_enumerator = QComboBox(self)
        self.unique_enumerator.addItems(list(self.enum_dict.keys()))

        # whether or not to put () around the enumerator
        self.paranthesize_enum = QCheckBox("&Paranthesize enumerator")

        # example label of new filename
        self.example_name = QLabel(self)
        # press to rename
        self.submit = QPushButton("&Rename!")

        # success dialog to popup after completion
        self.completed_dialog = QMessageBox()
        self.completed_dialog.setWindowTitle("Renaming finished")

        # error dialog to popup if error occurs
        self.error_dialog = QMessageBox()
        self.error_dialog.setIcon(QMessageBox.Critical)
        self.error_dialog.setWindowTitle("Error!")

    def arrangeWidgets(self):
        # arranges widgets in the window
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
        # create Qt connections between widgets

        # open folder browser when click button
        self.folder_button.clicked.connect(self.folder_dialog.show)
        # update selected folder text when new folder selected 
        self.folder_dialog.directoryEntered.connect(self.selected_folder.setText)

        # toggle custom extension input box enabled with the checkbox
        self.custom.stateChanged.connect(self.custom_extensions.setEnabled)

        # if any widget effecting the filename is changed, update the example filename
        self.new_name.textChanged.connect(self.update_example)
        self.unique_separator.currentIndexChanged.connect(self.update_example)
        self.unique_enumerator.currentIndexChanged.connect(self.update_example)
        self.paranthesize_enum.stateChanged.connect(self.update_example)

        # rename files when click rename
        self.submit.clicked.connect(self.rename)

    def update_example(self):
        # update the label of what renamed files will look like
        name = self.new_name.text()
        sep = self.sep_dict[self.unique_separator.currentText()]
        enum = self.enum_dict[self.unique_enumerator.currentText()]
        if self.paranthesize_enum.checkState():
            enum = f"({enum})"
        self.example_name.setText(name+sep+enum+".ext")

    def rename(self):
        # renames files in the selected directory with matching extensions to format specified
        name = self.new_name.text()
        sep = self.sep_dict[self.unique_separator.currentText()]
        enum = self.unique_enumerator.currentText()
        exts = []
        exts += (x for x in IMG_EXT if self.images.checkState())
        exts += (x for x in VID_EXT if self.videos.checkState())
        exts += (x for x in AUD_EXT if self.audio.checkState())
        if self.custom.checkState():
            # split custom extensions on ,
            custom_extensions = self.custom_extensions.text().split(",")
            # remove empty strings
            custom_extensions = [x for x in custom_extensions if x]
            # lowercase and remove anything except lowercase characters
            custom_extensions = [re.sub("[^a-z]","", x.lower()) for x in custom_extensions]
            exts += custom_extensions
            exts = set(exts) # make set incase custom extension is same as defaults
        try:
            count = 0
            if enum == "letters":
                iterator = itertools.combinations_with_replacement(string.ascii_lowercase, count//26 + 1)
            for file in os.listdir(self.selected_folder.text()):
                extension = file.rpartition(".")[-1].lower()
                if extension in exts:
                    if enum == "numbers":
                        next_enum = count + 1
                    elif enum == "letters":
                        # a-z then aa,ab,...,az then ba,bb,...bz ...
                        try:
                            next_enum = "".join(next(iterator))
                        except:
                            # increase length when iterator runs out
                            iterator = itertools.combinations_with_replacement(string.ascii_lowercase, count//26 + 1)
                            next_enum = "".join(next(iterator))
                    if self.paranthesize_enum.checkState():
                        # add () around the next_enum if specified
                        next_enum = f"({next_enum})"
                    
                    # rename the file
                    old_file = os.path.join(self.selected_folder.text(), file)
                    new_file = os.path.join(self.selected_folder.text(), name+sep+str(next_enum)+f".{extension}")
                    os.rename(old_file, new_file)
                    count += 1
            
            self.show_finished_dialog(count)

        except FileNotFoundError as error:
            self.error_dialog.setText(error.args[1])
            self.error_dialog.show()

    def show_finished_dialog(self, count):
        # shows dialog on success of file renaming
        if count > 0:
            self.completed_dialog.setIcon(QMessageBox.Information)
        else:
            self.completed_dialog.setIcon(QMessageBox.Warning)
        self.completed_dialog.setText(f"{count} files renamed.")
        self.completed_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())