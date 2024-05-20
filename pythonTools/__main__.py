import os
import sys

def AddDirToSys(pathToAdd):
    if pathToAdd not in sys.path:
        sys.path.append(pathToAdd)

def main():
    toolPath = os.path.abspath(__file__)
    toolDir = os.path.dirname(toolPath)
    srcDir = os.path.join(toolDir, "src")
    parentDir = os.path.dirname(toolDir)

    AddDirToSys(toolDir)
    AddDirToSys(srcDir)
    AddDirToSys(parentDir)

    from pythonUnrealTools import StartUnrealTools
    StartUnrealTools()

if __name__ == "__main__":
    main()