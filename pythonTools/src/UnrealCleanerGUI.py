from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
from Unreal import UnrealBase, UnrealCleaner

class UnrealCleanerGUI(QWidget):
    def __init__(self, unreal : UnrealBase):
        super().__init__()
        self.unrealCleaner = UnrealCleaner(unreal) 
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.label = QLabel("Project Cleaner")
        self.masterLayout.addWidget(self.label)
        self.deleteFileDisplay = QListWidget()
        self.masterLayout.addWidget(self.deleteFileDisplay)

        cleanStepsLayout= QHBoxLayout()
        self.masterLayout.addLayout(cleanStepsLayout)
        self.analyzeBtn = QPushButton("Find Regeneratable Binaries")
        cleanStepsLayout.addWidget(self.analyzeBtn)
        self.analyzeBtn.clicked.connect(self.UpdateDeleteItems)
        self.cleanBtn = QPushButton("Clean")
        cleanStepsLayout.addWidget(self.cleanBtn)
        self.cleanBtn.clicked.connect(self.CleanBtnClicked)
        self.regenBtn = QPushButton("Regenerate")
        cleanStepsLayout.addWidget(self.regenBtn)

        self.regenBtn.clicked.connect(self.RegenBtnClicked)
        self.cleanAndRebuildBtn = QPushButton("Clean and Regenerate VS Project")
        self.masterLayout.addWidget(self.cleanAndRebuildBtn)
        self.cleanAndRebuildBtn.clicked.connect(self.CleanAndRebuild)

        self.UpdateDeleteItems()        

    def RegenBtnClicked(self):
        self.unrealCleaner.unreal.RegenerateVisualStuidoProjFile()
        self.UpdateDeleteItems()

    def CleanAndRebuild(self):
        self.unrealCleaner.CleanProject()
        self.unrealCleaner.unreal.RegenerateVisualStuidoProjFile()
        self.UpdateDeleteItems()

    def UpdateDeleteItems(self):
        self.deleteFileDisplay.clear()
        self.deleteFileDisplay.addItems(self.unrealCleaner.GetAllPathsToDelete())

    def CleanBtnClicked(self):
        self.unrealCleaner.CleanProject()
        self.UpdateDeleteItems()