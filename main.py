
import os
import time
import fitz
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import fileHandling
import myVariables

# get the user's desktop path and define the folder to monitor
desktopPathUser = os.path.expanduser('~') + "\\Desktop"
nameOfFolderToMonitor = "Convert PDF to PNG"
folderToMonitor = desktopPathUser + "\\" + nameOfFolderToMonitor

# create the folder "Convert PDF to PNG", if it does not exist yet
try:
  os.makedirs(folderToMonitor, exist_ok=True)
except OSError as error:
  print("Error creating folder on desktop: " + error)

class pdfToPngConverter(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # get the path of the new file or URL
            filePath = event.src_path
            
            fileName, oldExtension = fileHandling.getFileName(filePath)
            if (not fileHandling.checkExtension(oldExtension)):
                print("Wrong filetype!")
                fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
            else:
                try:
                    doc = fitz.open(filePath)
                    zoomX = myVariables.RESOLUTION / 72 # zoom with the right resolution
                    zoomY = myVariables.RESOLUTION / 72
                    matrix = fitz.Matrix(zoomX, zoomY)

                    # loop through each page
                    for pageNumber in range(len(doc)):
                        page = doc.load_page(pageNumber)
                        # get the pixmap with desired resolution
                        pixmap = page.get_pixmap(matrix=matrix)
                        # save the pixmap as PNG with highest quality
                        outputFilenameSingular = desktopPathUser + "\\" + fileName
                        if len(doc) > 1:
                            outputFilenamePlurar = outputFilenameSingular + "_page " + str(pageNumber + 1) + myVariables.NEW_EXTENSION
                            pixmap.save(outputFilenamePlurar)
                        else:
                            outputFilenameSingular = outputFilenameSingular + myVariables.NEW_EXTENSION
                            pixmap.save(outputFilenameSingular)

                    # print out result to the console
                    if len(doc) > 1:
                        print("PNG picture's generated for " + filePath + " and saved on desktop.")
                    else:
                        print("PNG picture generated for " + filePath + " and saved on desktop.")
                    
                    # delete the old file after the qr code got generated
                    doc.close()
                    fileHandling.deleteFile(filePath)
                    
                # exception handling
                except FileNotFoundError as error:
                    print("Error: File not found - " + str(error)) # catch error if the file has been removed unintentionally (very unlikely due to the speed of processing)
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except OSError as error:
                    print("Error reading file: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except UnicodeDecodeError as error:
                    print("Error decoding file: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except fitz.FileDataError as e:
                    print("An error occurred:", e)
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except:
                    print("General error: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)

# create and start the observer
eventHandler = pdfToPngConverter()
observer = Observer()
observer.schedule(eventHandler, folderToMonitor, recursive=True)
observer.start()

try:
    while True:
        time.sleep(.5)
except KeyboardInterrupt:
    observer.stop()

observer.join()