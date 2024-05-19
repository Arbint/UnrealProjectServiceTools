
import os
import sys

def AddDirToSys(pathToAdd):
    if pathToAdd not in sys.path:
        sys.path.append(pathToAdd)

from PySide6.QtWidgets import QApplication,QLabel ,QVBoxLayout, QWidget, QMainWindow, QPushButton, QLineEdit, QFileDialog, QHBoxLayout
from PySide6.QtGui import QIcon

def main():
    toolPath = os.path.abspath(__file__)
    toolDir = os.path.dirname(toolPath)
    srcDir = os.path.join(toolDir, "src")
    parentDir = os.path.dirname(toolDir)

    AddDirToSys(toolDir)
    AddDirToSys(srcDir)
    AddDirToSys(parentDir)

    from cleanup import UnrealCleanerGUI
    class Unreal:
        def __init__(self):
            self.unrealPrjDir = self.AutoFindProject()

        def AutoFindProject(self):
            for file in os.listdir(parentDir):
                if ".uproject" in file:
                    return parentDir

            return ""

        def GetProjectDir(self):
            return self.unrealPrjDir

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.unreal = Unreal()
            self.setWindowTitle("Python Unreal Tools")
            iconPath = os.path.join(toolDir, "assets", "mainIcon.png")
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

            self.projectPath = QLineEdit(self.unreal.unrealPrjDir)
            self.projectPath.setEnabled(False)
            layout.addWidget(self.projectPath)

            self.locationUnrealPrjBtn = QPushButton("...")
            layout.addWidget(self.locationUnrealPrjBtn)
            self.locationUnrealPrjBtn.clicked.connect(self.LocateUnrealProject)

        def LocateUnrealProject(self):
            fileFilter = "Unreal Project File(*.uproject);;"
            unrealProj = QFileDialog().getOpenFileName(None, "Please Select The Unreal Project", self.unreal.unrealPrjDir, fileFilter)
            unrealProj = unrealProj[0] 
            if unrealProj:
                self.unreal.unrealPrjDir = os.path.dirname(unrealProj)
                self.projectPath.setText(unrealProj)
                
        def SetupCleaner(self):
            self.centralLayout.addWidget(UnrealCleanerGUI(self.unreal.GetProjectDir))

    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()