from datetime import datetime
import MySQLdb
import Tkinter

top_window = Tkinter.Tk()
top_window.title("To Do Py")
items_list = Tkinter.Listbox(top_window)
date_now = datetime.now().strftime("%m/%d/%Y")

def addItem(item, dateAdded, window):
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "INSERT INTO todolist (item, datecreated) VALUES ('%s', '%s')" % (item, dateAdded)
  try:
    cursor.execute(sql)
    db.commit()
  except MySQLdb.Error, e:
    print(e)
  db.close()
  window.destroy()
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
    
def addButtonClicked():
  entry_window = Tkinter.Toplevel(top_window)
  entry_window.title("Add Item")
  itemField = Tkinter.Entry(entry_window)
  itemField.pack()
  submitButton = Tkinter.Button(entry_window, text = "Submit", command = lambda: addItem(itemField.get(), date_now, entry_window))
  submitButton.pack()
  
def deleteButtonClicked():
  try:  
    itemid = int(items_list.get(items_list.curselection()).split(" - ")[0])
    deleteItem(itemid)
    viewItems()
  except:
      print("Error!")
  
def exitButtonClicked():
  exit()
    
addButton = Tkinter.Button(top_window, text ="Add", command = addButtonClicked)
deleteButton = Tkinter.Button(top_window, text ="Delete", command = deleteButtonClicked)
exportButton = Tkinter.Button(top_window, text ="Export", command = exportTXT)
exitButton = Tkinter.Button(top_window, text ="Exit", command = exitButtonClicked)

items_list.pack()
viewItems()
addButton.pack()
deleteButton.pack()
exportButton.pack()
exitButton.pack()

top_window.mainloop()