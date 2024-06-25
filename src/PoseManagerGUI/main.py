import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt

PROJECT_PATH = '/home/s5636764/Downloads'

class PoseManagerDialogUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Manage Poses')
        self.resize(100,100)
        layout = QtWidgets.QVBoxLayout()
        label= QtWidgets.QLabel("Please select an option")
        layout.addWidget(label)

        capture_button = QtWidgets.QPushButton("Capture")
        capture_button.clicked.connect(self.captureAction)
        layout.addWidget(capture_button)

        loader_button = QtWidgets.QPushButton("Load")
        loader_button.clicked.connect(self.loadAction)
        layout.addWidget(loader_button)

        self.setLayout(layout)

    def captureAction(self):
        print("User chose to capture")
        self.accept()
        capture_action = PoseCaptureUI()
        capture_action.exec_()

    def loadAction(self):
        self.accept()
        print("User chose to load")
        pose_loader = PoseLoaderUI(folder_path=PROJECT_PATH)
        pose_loader.exec_()

class PoseCaptureUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle('Capture Pose')
            layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel("Please enter the pose name")
            layout.addWidget(label)

            self.pose_name_edit = QtWidgets.QLineEdit()
            layout.addWidget(self.pose_name_edit)

            capture_button = QtWidgets.QPushButton("Capture")
            capture_button.clicked.connect(self.capturePose)
            layout.addWidget(capture_button)

            self.setLayout(layout)

    def capturePose(self):
        pose_name = self.pose_name_edit.text()
        if pose_name:
            self.accept()
            QtWidgets.QMessageBox.information(self, "Pose Captured", f"Pose '{pose_name}' Captured")
            pose_reloader = PoseLoaderUI(folder_path=PROJECT_PATH)
            pose_reloader.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "Empty Name", "Please enter a pose name")

    def closeEvent(self, event):
        event.accept()

class PoseLoaderUI(QtWidgets.QDialog):
    def __init__(self, parent=None, folder_path=''):
        super().__init__(parent)
        self.setWindowTitle("Select Poses")
        self.selected_files_label = QtWidgets.QLabel("No poses selected.")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.selected_files_label)

        scroll_area = QtWidgets.QScrollArea()
        layout.addWidget(scroll_area)

        scroll_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)

        self.folder_path = folder_path
        self.image_labels = {}
        self.selected_files = []

        self.loader_button = QtWidgets.QPushButton("Update")
        self.loader_button.clicked.connect(self.getFileNames)
        layout.addWidget(self.loader_button)

        self.folder_path = folder_path
        self.load_files(scroll_layout)

    def load_files(self, layout):
        max_dialog_width = 600
        max_dialog_height = 150

        files = os.listdir(self.folder_path)
        row, col = 0, 0
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                filepath = os.path.join(self.folder_path, filename)
                pixmap = QtGui.QPixmap(filepath)
                pixmap = pixmap.scaled(max_dialog_width // 3, max_dialog_height // 3, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

                label = QtWidgets.QLabel()
                label.setPixmap(pixmap)
                label.setStyleSheet("")
                label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Set cursor to hand pointer
                label.mousePressEvent = lambda event, file=filename: self.imageClicked(file)  # Connect click event

                layout.addWidget(label)
                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                # Add QLabel below the image to display filename
                filename_label = QtWidgets.QLabel(os.path.basename(filename)[:-4])  # Show only the filename without the full path
                filename_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(filename_label)
                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                self.image_labels[label] = (filename, filename_label)

    def imageClicked(self, filename):
        # Find the QLabel corresponding to the clicked image
        for label in self.findChildren(QtWidgets.QLabel):
            if label.pixmap() and self.image_labels[label][0] == filename:
                # Toggle selection state
                if filename in self.selected_files:
                    self.selected_files.remove(filename)
                    label.setStyleSheet("")  # Reset style sheet
                    self.image_labels[label][1].setStyleSheet("")
                else:
                    self.selected_files.append(filename)
                    label.setStyleSheet("border: 2px solid blue;")  # Add border to highlight selection
                    self.image_labels[label][1].setStyleSheet("border-bottom: 1px solid blue; border-radius: 0.5px") # Border highlight for text

        self.selected_files_label.setText(f"Selected poses: {len(self.selected_files)}")

    def getFileNames(self):
        self.accept()
        print(self.selected_files)
        QtWidgets.QMessageBox.information(self, "Poses", f"{len(self.selected_files)} updated poses:\n{self.selected_files[0][:-4]}")
        start_ui = PoseManagerDialogUI()
        start_ui.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog=PoseManagerDialogUI()
    dialog.exec()
    sys.exit(app.exec_())
