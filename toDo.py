import MySQLdb
from datetime import datetime

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
      dateadded = row[2]
      print "%d\t%s\t%s" % (itemid, item, dateadded)
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

while True:
  answer = raw_input("(A)View Items\t(B)Add Item\t(C)Delete Item\t(D)Exit\n")
  if answer == "a":
    viewItems()
  elif answer == "b":
    itemName = raw_input("Item Name: ")
    addItem(itemName, date_now)
    print("Item Added.")
    viewItems()
  elif answer == "c":
    itemID = raw_input("Item ID: ")
    deleteItem(int(itemID))
    print("Item Deleted.")
    viewItems()
  elif answer == "d":
    exit()