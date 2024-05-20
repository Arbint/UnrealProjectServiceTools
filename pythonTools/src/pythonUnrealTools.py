
from UnrealCleanerGUI import UnrealCleanerGUI
from PySide6.QtWidgets import QApplication,QLabel ,QVBoxLayout, QWidget, QMainWindow, QPushButton, QLineEdit, QFileDialog, QHBoxLayout
from PySide6.QtGui import QIcon
import os, sys
import dirUtilities
from Unreal import UnrealBase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.unreal = UnrealBase()
        self.setWindowTitle("Python Unreal Tools")
        iconPath = os.path.join(dirUtilities.GetAssetDir(), "mainIcon.png")
        self.setWindowIcon(QIcon(iconPath))
        self.setCentralWidget(QWidget())
        self.centralLayout = QVBoxLayout()
        self.centralWidget().setLayout(self.centralLayout)
        self.SetupUnrealProjectLocatorGUI()
        self.SetupCleaner()

    def SetupUnrealProjectLocatorGUI(self):
        label = QLabel("Unreal Project Location:")
        self.centralLayout.addWidget(label)

        layout = QHBoxLayout()
        self.centralLayout.addLayout(layout)

        self.projectPath = QLineEdit(self.unreal.GetProjectDir())
        self.projectPath.setEnabled(False)
        layout.addWidget(self.projectPath)

        self.locationUnrealPrjBtn = QPushButton("...")
        self.locationUnrealPrjBtn.setFixedWidth(50)
        layout.addWidget(self.locationUnrealPrjBtn)
        self.locationUnrealPrjBtn.clicked.connect(self.LocateUnrealProject)

        openLayout = QHBoxLayout()
        self.centralLayout.addLayout(openLayout)

        openFolderBtn = QPushButton("Open Folder")
        openLayout.addWidget(openFolderBtn)
        openFolderBtn.clicked.connect(self.unreal.OpenUnrealProjectFolder)
        
        openEditorBtn = QPushButton("Open Editor")
        openLayout.addWidget(openEditorBtn)
        openEditorBtn.clicked.connect(self.unreal.OpenEditor)
        
        openSlnBtn = QPushButton("Open Visual Studio")
        openLayout.addWidget(openSlnBtn)
        openSlnBtn.clicked.connect(self.unreal.OpenVisualStudioSolution)

    def LocateUnrealProject(self):
        fileFilter = "Unreal Project File(*.uproject);;"
        unrealProj = QFileDialog().getOpenFileName(None, "Please Select The Unreal Project", self.unreal.unrealPrjDir, fileFilter)
        unrealProj = unrealProj[0] 
        if unrealProj:
            self.unreal.unrealPrjDir = os.path.dirname(unrealProj)
            self.projectPath.setText(unrealProj)
            
    def SetupCleaner(self):
        self.centralLayout.addWidget(UnrealCleanerGUI(self.unreal))

    def closeEvent(self, event):
        self.unreal.SaveConfig();

def StartUnrealTools():
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())