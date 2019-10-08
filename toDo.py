from datetime import datetime
import MySQLdb
import Tkinter
import tkMessageBox

top_window = Tkinter.Tk()
top_window.title("To Do Py")

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
  viewItems()

def viewItems():
  items_list.delete(0, "end")
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "SELECT * FROM todolist"
  try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for idx, row in enumerate(results):
      itemid = row[0]
      item = row[1]
      items_list.insert(idx, str(itemid) + " - " + item)
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
  outputFile = open("toDo.txt", "w")
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "SELECT * FROM todolist"
  try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      item = row[1]
      outputFile.write("%s\n" % (item))
  except MySQLdb.Error, e:
    print(e)
  db.close()
  outputFile.close()
  
def deleteButtonClicked():
  try:  
    itemid = int(items_list.get(items_list.curselection()).split(" - ")[0])
    deleteItem(itemid)
    viewItems()
  except:
      tkMessageBox.showinfo("Error", "Error: no item selected. Please try again")
  
def exitButtonClicked():
  exit()
  
itemField = Tkinter.Entry(top_window)
itemField.pack()
    
addButton = Tkinter.Button(top_window, text ="Add", command = lambda: addItem(itemField.get(), date_now))
addButton.pack()

deleteButton = Tkinter.Button(top_window, text ="Delete", command = deleteButtonClicked)
deleteButton.pack()

exportButton = Tkinter.Button(top_window, text ="Export", command = exportTXT)
exportButton.pack()

exitButton = Tkinter.Button(top_window, text ="Exit", command = exitButtonClicked)
exitButton.pack()

items_list = Tkinter.Listbox(top_window)
items_list.pack()

viewItems()

top_window.mainloop()