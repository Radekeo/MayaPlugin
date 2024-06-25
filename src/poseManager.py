import maya.cmds as cmds
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

import json
import os 
import sys

HOME_DIR = os.path.expanduser('~')
PROJECT_FOLDER = cmds.file(q=True, sn=True).split('/')[-1].split('.')[0]
DEFAULT_PROJECT_DIR = os.path.join(HOME_DIR, PROJECT_FOLDER)

def mayaMainWindow() :
    # note api1 code here
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window),QtWidgets.QDialog)

class PoseManager:
    def __init__(self) -> None:
        # Get rig controllers in the scene
        self.nurbs = [nurb[:-5] for nurb in cmds.ls(type=['nurbsCurve'])]
        
        self.default_pose_data_path = os.path.join(DEFAULT_PROJECT_DIR, 'DEFAULT.json')
        
        self.startPlugin()

    def capturePose(self,pose_name):
        self.addJSONToDir(pose_name+'.json')
        self.addSnapshotToDir(pose_name+'.jpg')

    def getPoseData(self, ctrl):
        translation = cmds.xform(ctrl, q=True, translation=True, worldSpace=False)
        rotation = cmds.xform(ctrl, q=True, rotation=True, worldSpace=False)
        scale = cmds.xform(ctrl, q=True, scale=True, worldSpace=False)
        return [translation, rotation, scale]
    
    def writeToJSON(self,file_dir, data):
        with open(file_dir, 'w') as file:
            try:
                json.dump(data, file)
                print('done')
            except:
                print('not done')
    
    ####### Get data for each nurbsCurve and write to a JSON file
    def addJSONToDir(self, file_name):
        self.pose_data = {}
        file_path = os.path.join(DEFAULT_PROJECT_DIR, file_name)
        for nurb in self.nurbs:
            try:
                data = self.getPoseData(nurb)
                self.pose_data[nurb] = {'translation': data[0], 'rotation': data[1], 'scale': data[2]}
            except:
                continue

        if os.path.exists(DEFAULT_PROJECT_DIR):
            with open(self.default_pose_data_path, 'r') as file:
                default_pose = json.load(file)

            for controller in default_pose:
                if self.pose_data[controller]:
                    if default_pose[controller] == self.pose_data[controller]:
                        del self.pose_data[controller]   
        else:
            os.makedirs(DEFAULT_PROJECT_DIR)
        
        self.writeToJSON(file_path, self.pose_data)

    def addSnapshotToDir(self, pose_name):
        # Capture viewport
        snapshot_path = os.path.join(DEFAULT_PROJECT_DIR, pose_name)
        cmds.viewFit()
        cmds.refresh(cv=True, f=False, fe="jpg", fn=snapshot_path)
    
    def updatePose(self,selected_poses):
        # get Data from json
        pose_data = {}
        for pose in selected_poses:
            file_name = f"{pose[:-4]}.json"
            file_path = os.path.join(DEFAULT_PROJECT_DIR, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                pose_data.update(json_data)

        # set controller (translation, rotation and scale) values
        for controller, values in pose_data.items():
            try:
                # Translation Values
                cmds.setAttr(controller + '.translateX', values['translation'][0])
                cmds.setAttr(controller + '.translateY', values['translation'][1])
                cmds.setAttr(controller + '.translateZ', values['translation'][2])

                # Rotation Values
                cmds.setAttr(controller + '.rotateX', values['rotation'][0])
                cmds.setAttr(controller + '.rotateY', values['rotation'][1])
                cmds.setAttr(controller + '.rotateZ', values['rotation'][2])

                # Scale Values
                cmds.setAttr(controller + '.scaleX', values['scale'][0])
                cmds.setAttr(controller + '.scaleY', values['scale'][1])
                cmds.setAttr(controller + '.scaleZ', values['scale'][2])
            except:
                continue

    '''
    Capture default pose data first time plugin is loaded.
    This would help keep track of changes made to the rig data
    '''
    def startPlugin(self):
        if not os.path.exists(self.default_pose_data_path): 
            self.addJSONToDir('DEFAULT.json')
        ui = PoseManagerUI(self)
        ui.show(dockable=True)
        

class PoseCaptureUI(QtWidgets.QDialog):
    def __init__(self, program, parent=None):
            super().__init__(parent)
            self.program = program
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
            self.program.capturePose(pose_name)
            QtWidgets.QMessageBox.information(self, "Pose Captured", f"Pose '{pose_name}' Captured")

        else:
            QtWidgets.QMessageBox.warning(self, "Empty Name", "Please enter a pose name")

    def closeEvent(self, event):
        event.accept()

class PoseManagerUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, program, parent=mayaMainWindow()):
        super(PoseManagerUI, self).__init__(parent)
        self.setWindowTitle("Manage Poses")
        self.selected_files_label = QtWidgets.QLabel("No poses selected.")
        self.program = program

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

        capture_button = QtWidgets.QPushButton("Capture Pose")
        capture_button.clicked.connect(self.captureAction)
        layout.addWidget(capture_button)

        self.loader_button = QtWidgets.QPushButton("Update Pose")
        self.loader_button.clicked.connect(self.updatePose)
        layout.addWidget(self.loader_button)
        
        self.reset_button = QtWidgets.QPushButton("Reset to Default Pose")
        self.reset_button.clicked.connect(self.resetPose)
        layout.addWidget(self.reset_button)

        self.image_labels = {}
        self.selected_files = []
        self.folder_path = DEFAULT_PROJECT_DIR

        self.load_files(scroll_layout)

    def captureAction(self):
        print("User chose to capture")
        capture_action = PoseCaptureUI(self.program)
        capture_action.exec_()

    def resetPose(self):
        self.updatePose(['DEFAULT.jpg'])

    def load_files(self, layout):
        max_dialog_width = 450
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
                filename_label.setAlignment(QtCore.Qt.AlignCenter)
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

    def updatePose(self, file_list=None):
        # print(self.selected_files)
        fl = file_list
        if fl:
            message = "Pose reset to default"
        else:
            fl = self.selected_files
            message = f"{len(fl)} updated poses:\n{[f[:-4] for f in fl]}"
            
            
        self.program.updatePose(fl)
        cmds.refresh(cv=True)

        QtWidgets.QMessageBox.information(self, "Poses", f"{message}")

class PoseManagerShelf(object):
    def __init__(self):
        self.shelf_name = "PoseManager"
        self.button_label = "PoseManager"
        self.icon_path = "MayaPoseManagerPlugin/icon.png"  # Replace with your icon path

    def create_shelf(self):
        if not cmds.shelfLayout(self.shelf_name, exists=True):
            cmds.shelfLayout(self.shelf_name, parent="ShelfLayout")

        # Add a button to the shelf
        cmds.shelfButton(parent=self.shelf_name,
                         label="Pose Manager",
                         image=self.icon_path,
                         command=self.run_plugin_command,
                         annotation="Start Plugin")

    def run_plugin_command(self, *args):
        if cmds.pluginInfo("PoseManagerPlugin", q=True, loaded=True):
            cmds.unloadPlugin("PoseManagerPlugin")

        try:
            del sys.modules['PoseManager']
        except KeyError:
            pass

        cmds.loadPlugin("PoseManagerPlugin")
        cmds.PoseManagerImporter()