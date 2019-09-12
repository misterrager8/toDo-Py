import os

folderPath = os.getcwd() + "/toDoList"

if not os.path.exists(folderPath):
  os.mkdir(folderPath)

def formatList(fileList):
  for index, item in enumerate(fileList):
    print(str(index) + " - " + item)
  
def listFiles():
  return os.listdir(folderPath)
  
def addItem(answer):
  if answer == "y":
    return True
  elif answer == "n":
    return False
    
def changeItem(item):
  fileItem = os.listdir(folderPath)[item]
  newFile = open(folderPath + "/" + fileItem, "a+")
  fileText = input("Content of the file:\n")
  newFile.write(fileText)
  newFile.close()
    
def handleInput(answer):
  if answer == "a":
    item = input("Item name: ") + ".txt"
    newFile = open(folderPath + "/" + item, "a+")
    newFile.close()
  elif answer == "b":
    formatList(listFiles())
    itemSelected = input("Which item do you want to edit? ")
    changeItem(int(itemSelected))
  elif answer == "c":
    print("na")
  elif answer == "d":
    exit()

# print("There are " + str(len(listFiles())) + " items on the list")

while True:
  # formatList(listFiles())
  answer = input(
  """
  A: Add To List
  B: Edit Item
  C: Delete Item
  D: Quit Program

  Please select
  """
  )
  handleInput(answer)
  # if (addItem(answer)):
    # item = input("Item name: ") + ".txt"
    # newFile = open(folderPath + "/" + item, "a+")
    # newFile.close()
    # formatList(listFiles())
  # elif (not addItem(answer)):
    # formatList(listFiles())
    # break
    
    
