
import os
import sys

def AddDirToSys(pathToAdd):
    if pathToAdd not in sys.path:
        sys.path.append(pathToAdd)

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow, QPushButton, QLineEdit
from PySide6.QtGui import QIcon

def main():
    toolPath = os.path.abspath(__file__)
    toolDir = os.path.dirname(toolPath)
    srcDir = os.path.join(toolDir, "src")
    unrealPrjDir = os.path.dirname(toolDir)

    AddDirToSys(toolDir)
    AddDirToSys(srcDir)
    AddDirToSys(unrealPrjDir)

    from cleanup import UnrealCleanerGUI
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Python Unreal Tools")
            iconPath = os.path.join(toolDir, "assets", "mainIcon.png")
            self.setWindowIcon(QIcon(iconPath))
            self.setCentralWidget(QWidget())
            self.centralLayout = QVBoxLayout()
            self.centralWidget().setLayout(self.centralLayout)
            self.centralLayout.addWidget(UnrealCleanerGUI(unrealPrjDir))

    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()