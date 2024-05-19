from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
import os, sys
import shutil
import subprocess

class UnrealCleaner:
    def __init__(self, unrealPrjDirFunc):
        self.unrealPrjDirFunction = unrealPrjDirFunc  
        
    def GetUnrealDeleteNames(self):
        return ['.vs', 'Binaries', 'DerivedDataCache', 'Intermediate', 'Saved', '.vsconfig']

    def GetAllPathsToDelete(self):
        filePaths = []
        for name in self.GetUnrealDeleteNames():
            filePath = os.path.join(self.unrealPrjDirFunction(), name)
            if os.path.exists(filePath):
                filePaths.append(os.path.normpath(filePath))

        slnPath = self.GetVisualStudioSolutionFilePath()
        if os.path.exists(slnPath):
            filePaths.append(os.path.normpath(slnPath))

        return filePaths

    def GetUnrealPrjFilePath(self):
        return self.GetFilePathWithExtention('.uproject')

    def GetVisualStudioSolutionFilePath(self):
        return self.GetFilePathWithExtention('.sln')

    def GetFilePathWithExtention(self, extention: str):
        for fileName in os.listdir(self.unrealPrjDirFunction()):
            filePath = os.path.join(self.unrealPrjDirFunction(), fileName)
            if os.path.isfile(filePath) and extention in fileName:
                return filePath
        return ""

    def RegenerateVisualStuidoProjFile(self):
        command = "\"C:\\Program Files (x86)\\Epic Games\\Launcher\\Engine\\Binaries\\Win64\\UnrealVersionSelector.exe\" /projectfiles " + self.GetUnrealPrjFilePath()        
    
        print("running: ")
        print(command)
        print("-----------------------------------")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Rebuilt Visual Studio Project with Return code: {result.returncode}\n Output: {result.stdout} \n")
        if result.stderr:
            print(f"Error: {result.stderr}")


    def CleanProject(self):
        for file in self.GetAllPathsToDelete():
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)

class UnrealCleanerGUI(QWidget):
    def __init__(self, unrealPrjDirFunc):
        super().__init__()
        self.unrealCleaner = UnrealCleaner(unrealPrjDirFunc) 
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.label = QLabel("Project Cleaner")
        self.masterLayout.addWidget(self.label)
        self.deleteFileDisplay = QListWidget()
        self.masterLayout.addWidget(self.deleteFileDisplay)
        self.analyzeBtn = QPushButton("Find")
        self.masterLayout.addWidget(self.analyzeBtn)
        self.analyzeBtn.clicked.connect(self.AnalyzeBtnClicked)
        self.cleanBtn = QPushButton("Clean")
        self.masterLayout.addWidget(self.cleanBtn)
        self.cleanBtn.clicked.connect(self.CleanBtnClicked)
        self.regenBtn = QPushButton("Regenerate")
        self.masterLayout.addWidget(self.regenBtn)
        self.regenBtn.clicked.connect(self.RegenBtnClicked)
        self.cleanAndRebuildBtn = QPushButton("Clean and Regenerate VS Project")
        self.masterLayout.addWidget(self.cleanAndRebuildBtn)
        self.cleanAndRebuildBtn.clicked.connect(self.CleanAndRebuild)

    def RegenBtnClicked(self):
        self.unrealCleaner.RegenerateVisualStuidoProjFile()

    def CleanAndRebuild(self):
        self.unrealCleaner.CleanProject()
        self.unrealCleaner.RegenerateVisualStuidoProjFile()

    def AnalyzeBtnClicked(self):
        self.UpdateDeleteItems()

    def UpdateDeleteItems(self):
        self.deleteFileDisplay.clear()
        self.deleteFileDisplay.addItems(self.unrealCleaner.GetAllPathsToDelete())

    def CleanBtnClicked(self):
        self.unrealCleaner.CleanProject()