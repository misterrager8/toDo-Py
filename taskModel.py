class task:
  
  def __init__(self, taskName, notes, dateCreated):
    self.taskName = taskName
    self.notes = notes
    self.dateCreated = dateCreated
    self.done = False
    
  def getTaskName(self):
    return self.taskName
  
  def setTaskName(self, x):
    self.taskName = x
    
  def getNotes(self):
    return self.notes
  
  def setNotes(self, x):
    self.notes = x
    
  def getDateCreated(self):
    return self.dateCreated
  
  def setDateCreated(self, x):
    self.dateCreated = x
    
  def getDone(self):
    return self.done
  
  def setDone(self, x):
    self.done = x
    
  def printTask(self):
    print(self.taskName + "\n" + 
          self.notes + "\n" + 
          self.dateCreated + "\n" + 
          str(self.done)
         )