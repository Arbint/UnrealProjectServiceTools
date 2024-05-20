import os

def GetSrcDir():
    filePath = os.path.abspath(__file__)
    return os.path.normpath(os.path.dirname(filePath))

def GetAssetDir():
    srcDir = GetSrcDir()
    parent = os.path.dirname(srcDir)
    return os.path.normpath(os.path.join(parent, "assets"))

def GetFilePathWithExtention(dir, extention: str):
    for fileName in os.listdir(dir):
        filePath = os.path.join(dir, fileName)
        if os.path.isfile(filePath) and extention in fileName:
            return os.path.normpath(filePath)
    return ""