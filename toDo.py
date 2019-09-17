import MySQLdb
from datetime import datetime
import os

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
    for row in results:
      itemid = row[0]
      item = row[1]
      print "%d\t%s" % (itemid, item)
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
  
def writeToFile(itemid, item):
  fo = open(os.getcwd() + "todo.txt", "a")
  fo.write("%d\t%s\n" % (itemid, item))
  fo.close()
  
def exportTXT():
  db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
  cursor = db.cursor()
  sql = "SELECT * FROM todolist"
  try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      itemid = row[0]
      item = row[1]
      writeToFile(itemid, item)
  except MySQLdb.Error, e:
    print(e)
  db.close()
  
while True:
  print("\t____TO-DO LIST____")
  viewItems()
  answer = raw_input("\n(A)Add Item\n(B)Delete Item\n(C)Export To TXT\n(D)Exit")
  if answer == "a":
    itemName = raw_input("Item Name: ")
    addItem(itemName, date_now)
    print("Item Added.")
  elif answer == "b":
    itemID = raw_input("Item ID: ")
    deleteItem(int(itemID))
    print("Item Deleted.")
  elif answer == "c":
    exportTXT()
  elif answer == "d":
    exit()