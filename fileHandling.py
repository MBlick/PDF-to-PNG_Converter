
import os
import shutil
import myVariables

# remove the old file in the folder
def deleteFile(filePath):
    try:
        os.remove(filePath)
        print("File " + filePath + " removed successfully.")
    except OSError as error:
        print("Error removing file:", error)

# get the file name and the extension separatly
def getFileName(filePath):
    fileNameWithExtension = os.path.basename(filePath)
    fileName, extension = os.path.splitext(fileNameWithExtension)
    return fileName, extension

# check if the extionsion is part of the allowed extensions
def checkExtension(extension):
    # some of the most common text formats
    if extension == myVariables.ALLOWED_EXTENSION:
        return True
    else:
        return False

# move the file out of the folder if the extension was wrong
def moveFile(sourceFilePath, desitnationFilePath):
    try:
        shutil.move(sourceFilePath, desitnationFilePath)
    except OSError as error:
        print("Error moving file: " + str(error))
    