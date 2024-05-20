
import pickle
import os
import dirUtilities
import shutil
import CLIUtilities

class SaveUnrealConfig:
    def __init__(self, unrealDir):
        self.unrealProjectDir = unrealDir 

class UnrealBase:
    def __init__(self):
        self.unrealPrjDir = ""
        self.ReadConfig()

    def ReadConfig(self):
        if os.path.exists(self.GetConfigFilePath()):
            with open(self.GetConfigFilePath(), 'rb') as file:
                loadedConfing = pickle.load(file)
                self.unrealPrjDir = loadedConfing.unrealProjectDir
                return True

        return False

    def SaveConfig(self):
        config = SaveUnrealConfig(self.unrealPrjDir)
        with open(self.GetConfigFilePath(), 'wb') as file:
            pickle.dump(config, file) 

    def GetConfigFilePath(self):
        return os.path.join(dirUtilities.GetSrcDir(), "config.uptl")

    def GetProjectDir(self):
        return self.unrealPrjDir

    def OpenEditor(self):
        command = f"{self.GetUnrealPrjFilePath()}"
        os.startfile(self.GetUnrealPrjFilePath())

    def OpenVisualStudioSolution(self):
        command = f"{self.GetVisualStudioSolutionFilePath()}"
        os.startfile(self.GetVisualStudioSolutionFilePath())

    def OpenUnrealProjectFolder(self):
        if self.unrealPrjDir and os.path.exists(self.unrealPrjDir):
            os.startfile(self.unrealPrjDir)

    def GetUnrealPrjFilePath(self):
        return dirUtilities.GetFilePathWithExtention(self.unrealPrjDir, '.uproject')
    def GetEngineSelectorCmd(self):

        return f"\"{self.GetEngineSelectorPath()}\""

    def GetVisualStudioSolutionFilePath(self):
        return dirUtilities.GetFilePathWithExtention(self.unrealPrjDir, '.sln')

    def GetEngineSelectorPath(self):
        return "C:\\Program Files (x86)\\Epic Games\\Launcher\\Engine\\Binaries\\Win64\\UnrealVersionSelector.exe"

    def RegenerateVisualStuidoProjFile(self):
        command = f"{self.GetEngineSelectorCmd()} /projectfiles " + self.GetUnrealPrjFilePath()        
        CLIUtilities.RunCommand(command) 

class UnrealCleaner:
    def __init__(self, unreal:UnrealBase):
        self.unreal = unreal  
        
    def GetUnrealDeleteNames(self):
        return ['.vs', 'Binaries', 'DerivedDataCache', 'Intermediate', 'Saved', '.vsconfig']

    def GetAllPathsToDelete(self):
        filePaths = []
        for name in self.GetUnrealDeleteNames():
            filePath = os.path.join(self.unreal.GetProjectDir(), name)
            if os.path.exists(filePath):
                filePaths.append(os.path.normpath(filePath))

        slnPath = self.unreal.GetVisualStudioSolutionFilePath()
        if os.path.exists(slnPath):
            filePaths.append(os.path.normpath(slnPath))

        return filePaths

    def CleanProject(self):
        for file in self.GetAllPathsToDelete():
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)