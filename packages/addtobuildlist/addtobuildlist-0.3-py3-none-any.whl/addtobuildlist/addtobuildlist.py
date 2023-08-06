import sys
import os
import hglib
import subprocess
import printandlog

def main(argv):
  printandlog.init("C:\Log\AddToBuildList.log")
  repoPath = argv[0]
  try:
    repo = hglib.open(repoPath)
  except:
    printandlog.printAndLog("Not a valid Mercurial repo",printandlog.MessageType.errorMessage)
  numberOfArguments = len(argv)
  if (numberOfArguments > 1):
    revisionList=[]
    for argvIndex in range (1,numberOfArguments):
      revisionList.append(argv[argvIndex])
    statusList = repo.status(revisionList)
  else:
    statusList = repo.status()


  printandlog.printAndLog("Following files were modified:", list = statusList)

  linkSet = createLinkList(statusList)
  for link in linkSet:
    modulePath = os.path.dirname(link)
    subsystem = os.path.basename(link)
    linkSourceFolder = os.path.join(b'w:\\TestLab\\Cada-NT\\',modulePath).decode()
    if not os.path.isdir(linkSourceFolder):
      printandlog.printAndLog("Creating folder: " + linkSourceFolder)
      os.makedirs(linkSourceFolder)
      printandlog.printAndLog("Folder was created.\n")

    assert(os.path.isdir(linkSourceFolder))
    
    linkSource = os.path.join(linkSourceFolder, subsystem.decode())

    linkTarget = os.path.join(repoPath,'Cada-NT', modulePath.decode(), subsystem.decode())
    assert(os.path.exists(linkTarget))
    localSubsystemsFileName = "W:\\local_subsystems.txt"
    try:
      localSubsystemsFile = open(localSubsystemsFileName, 'a')
    except:
      printandlog.printAndLog("File: " + localSubsystemsFileName +  " does not exists", printandlog.MessageType.errorMessage)

    if not os.path.exists(linkSource):
      printandlog.printAndLog("Creating link in " + linkSource + " for " + linkTarget)
      command = "mklink /D " + linkSource + " " + linkTarget
      subprocess.call(command, shell = True)
      printandlog.printAndLog("Link was created.\n")
      
      printandlog.printAndLog("Subsystem: " + link.decode() + " was added to localSubsystems file")
      localSubsystemsFile.write(link.decode() + "\n")
    localSubsystemsFile.close()

def createLinkList(statusList):
  linkSet = set()
  for status in statusList:
    filePath = status[1]
    linkSet.add(createLink(filePath))
  return linkSet

def createLink(filePath):
  directories = filePath.rsplit(b'\\')
  #                           LmsHq           Module          Subsystem
  relativePath = os.path.join(directories[1], directories[2], directories[3])
  return relativePath

if __name__ == '__main__':
    main(sys.argv[1:])
