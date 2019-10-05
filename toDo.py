import time
from datetime import datetime
import MySQLdb
import Tkinter

top = Tkinter.Tk()
top.title("To Do Py")
list = Tkinter.Listbox(top)
date_now = datetime.now().strftime("%m/%d/%Y")

def addItem(item, dateAdded):
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "INSERT INTO todolist (item, datecreated) VALUES ('%s', '%s')" % (item, dateAdded)
  try:
    cursor.execute(sql)
    db.commit()
  except MySQLdb.Error, e:
    print(e)
  db.close()

def viewItems():
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "SELECT * FROM todolist"
  try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for idx, row in enumerate(results):
      itemid = row[0]
      item = row[1]
      list.insert(idx, str(itemid) + " - " + item)
#      print "%d\t%s" % (itemid, item)
  except MySQLdb.Error, e:
    print(e)
  db.close()

def deleteItem(itemid):
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "DELETE FROM todolist WHERE id = '%d'" % (itemid)
  try:
    cursor.execute(sql)
    db.commit()
  except MySQLdb.Error, e:
    print(e)
  db.close()

def exportTXT():
  fo = open("toDo.txt", "w")
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "SELECT * FROM todolist"
  try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      item = row[1]
      fo.write("%s\n" % (item))
  except MySQLdb.Error, e:
    print(e)
  db.close()
  fo.close()

#while True:
#  print("-TO-DO LIST-\n[ID]\t[ITEM]")
#  viewItems()
#  answer = raw_input("\n(A) Add Item\n(B) Delete Item\n(C) Export To TXT\n(D) Exit\n")
#  if answer == "a":
#    itemName = raw_input("Item Name: ")
#    addItem(itemName, date_now)
#    print("Item Added.")
#  elif answer == "b":
#    itemID = raw_input("Item ID: ")
#    deleteItem(int(itemID))
#    print("Item Deleted.")
#    time.sleep(1)
#  elif answer == "c":
#    exportTXT()
#    print("Exported to .txt")
#    time.sleep(1)
#  elif answer == "d":
#    exit()
    
def buttonA():
  print("A")
def buttonB():
  print("B")
def buttonD():
  exit()
    
addButton = Tkinter.Button(top, text ="Add", command = buttonA)
deleteButton = Tkinter.Button(top, text ="Delete", command = buttonB)
exportButton = Tkinter.Button(top, text ="Export", command = exportTXT)
exitButton = Tkinter.Button(top, text ="Exit", command = buttonD)

list.pack()
viewItems()
addButton.pack()
deleteButton.pack()
exportButton.pack()
exitButton.pack()

top.mainloop()