import logging
import os
from datetime import datetime
from enum import Enum

class MessageType(Enum):
  normalMessage = 0
  succededMessage = 1
  warningMessage = 2
  errorMessage = 3

messageString = {}
messageString[MessageType.normalMessage] = " "
messageString[MessageType.succededMessage] = " Succeeded: "
messageString[MessageType.warningMessage] = " Warning: "
messageString[MessageType.errorMessage] = " Error: "

def makeUniqueFileName(logFilePath):
  dirName = os.path.dirname(logFilePath)
  if dirName == "":
    dirName = defaultFolder()

  fileFullName = os.path.basename(logFilePath)
  fileName = fileFullName.split(".")[0]
  fileExtension = fileFullName.split(".")[1]
  if not os.path.exists(dirName):
    os.makedirs(dirName)

  time = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
  fileNewName = str(fileName) + "_" + time
  if fileExtension != "":
    fileNewName = fileNewName + "." + fileExtension
  logFileNewPath = os.path.join(dirName, fileNewName)
  return logFileNewPath

def init(logFilePath):
  logFileNewPath = makeUniqueFileName(logFilePath)
  logging.basicConfig(filename=logFileNewPath, level=logging.INFO, format='%(asctime)s %(message)s')

def printAndLog(string, messageType = MessageType.normalMessage):
  messageTypeString = messageString(messageType)
  message = messageTypeString + string
  logging.info(message)
  print(datetime.now().strftime('%H:%M:%S')+ " " + message)

def defaultFolder():
  return "D:\Log"



