
import pickle
import os
import dirUtilities
import shutil
import subprocess

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

        slnPath = self.GetVisualStudioSolutionFilePath()
        if os.path.exists(slnPath):
            filePaths.append(os.path.normpath(slnPath))

        return filePaths

    def GetUnrealPrjFilePath(self):
        return self.GetFilePathWithExtention('.uproject')

    def GetVisualStudioSolutionFilePath(self):
        return self.GetFilePathWithExtention('.sln')

    def GetFilePathWithExtention(self, extention: str):
        for fileName in os.listdir(self.unreal.GetProjectDir()):
            filePath = os.path.join(self.unreal.GetProjectDir(), fileName)
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