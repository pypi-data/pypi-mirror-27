import logging
import os
from datetime import datetime
from enum import Enum
import traceback
import sys


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
  if not (os.path.exists(dirName) and os.path.isdir(dirName)) :
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

def printAndLog(string,  messageType = MessageType.normalMessage, list = []):
  messageTypeString = messageString[messageType]
  message = messageTypeString + string
  logging.info(message)
  print(datetime.now().strftime('%H:%M:%S')+ " " + message)
  for element in list:
    message = "\t" + str(element)
    logging.info(message)
    print(message)

def printException():
  print ('-'*177)
  traceback.print_exc(file=sys.stdout)
  print ('-'*177)
  logging.exception("\n \n" + '-'*77 + "Error" + '-'*77)

def defaultFolder():
  return "D:\Log"
