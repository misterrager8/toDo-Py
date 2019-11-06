from java.awt import *
from javax.swing import *
import sys
from datetime import datetime
from taskModel import task
import csv

currentDate = datetime.now().strftime("%m/%d/%Y")
taskDB = []

class mainWindow(JFrame):
  
  def __init__(self):
    super(mainWindow, self).__init__()
    self.initComponents()
    
  def initComponents(self):

    self.bgPanel = JPanel()
    self.exitButton = JLabel(mouseClicked = self.exitButtonMouseClicked)
    self.addButton = JLabel(mouseClicked = self.addButtonMouseClicked,
                            mouseEntered = self.addButtonMouseEntered,
                            mouseExited = self.addButtonMouseExited)
    self.deleteButton = JLabel(mouseEntered = self.deleteButtonMouseEntered,
                               mouseExited = self.deleteButtonMouseExited)
    self.clearButton = JLabel(mouseClicked = self.clearButtonMouseClicked,
                              mouseEntered = self.clearButtonMouseEntered,
                              mouseExited = self.clearButtonMouseExited)
    self.jScrollPane1 = JScrollPane()
    self.taskTable = JTable()
    self.taskField = JTextField(focusGained = self.taskFieldFocusGained)
    self.notesField = JTextField(focusGained = self.notesFieldFocusGained)
    self.taskLabel = JLabel()
    self.notesLabel = JLabel()

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    self.bgPanel.setBackground(Color(51, 153, 255))

    self.exitButton.setText("X")
    self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    self.addButton.setBackground(Color(51, 204, 255))
    self.addButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.addButton.setText("Add Task")
    self.addButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.addButton.setOpaque(True)

    self.deleteButton.setBackground(Color(51, 204, 255))
    self.deleteButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.deleteButton.setText("Delete Task")
    self.deleteButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.deleteButton.setOpaque(True)

    self.clearButton.setBackground(Color(51, 204, 255))
    self.clearButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.clearButton.setText("Delete All")
    self.clearButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.clearButton.setOpaque(True)

    self.taskTable.setModel(table.DefaultTableModel(
      [],
      ["Task", "Notes", "Date Created", "Done"]
    ))
    
    self.jScrollPane1.setViewportView(self.taskTable)

    self.taskLabel.setText("Task")

    self.notesLabel.setText("Note(s)")

    bgPanelLayout = GroupLayout(self.bgPanel)
    self.bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGap(0, 0, sys.maxint)
            .addComponent(self.exitButton))
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
              .addComponent(self.addButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
              .addComponent(self.deleteButton, GroupLayout.DEFAULT_SIZE, 204, sys.maxint)
              .addComponent(self.clearButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
              .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, False)
                  .addComponent(self.taskLabel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
                  .addComponent(self.notesLabel, GroupLayout.DEFAULT_SIZE, 51, sys.maxint))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                  .addComponent(self.taskField)
                  .addComponent(self.notesField))))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.jScrollPane1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)))
        .addContainerGap())
    )
    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addComponent(self.exitButton)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
              .addComponent(self.taskField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
              .addComponent(self.taskLabel))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
              .addComponent(self.notesField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
              .addComponent(self.notesLabel))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.addButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 144, sys.maxint)
            .addComponent(self.deleteButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.clearButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE))
          .addComponent(self.jScrollPane1, GroupLayout.PREFERRED_SIZE, 0, sys.maxint))
        .addContainerGap())
    )

    layout = GroupLayout(self.getContentPane())
    self.getContentPane().setLayout(layout)
    layout.setHorizontalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(self.bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
    )
    layout.setVerticalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(self.bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
    )

    self.pack()
    self.setLocationRelativeTo(None)
    
    with open("toDoList.csv", "r") as f:
      reader = csv.reader(f)
      for row in reader:
        taskDB.append(task(row[0], row[1], row[2], bool(int(row[3]))))
        
    for i in taskDB:
      self.taskTable.getModel().addRow([i.taskName, i.notes, i.dateCreated, str(i.done)])
    
  def addButtonMouseEntered(self, event):
    self.addButton.setBorder(border.LineBorder(Color.black))
    
  def addButtonMouseExited(self, event):
    self.addButton.setBorder(None)
    
  def deleteButtonMouseEntered(self, event):
    self.deleteButton.setBorder(border.LineBorder(Color.black))
    
  def deleteButtonMouseExited(self, event):
    self.deleteButton.setBorder(None)
    
  def clearButtonMouseEntered(self, event):
    self.clearButton.setBorder(border.LineBorder(Color.black))
    
  def clearButtonMouseExited(self, event):
    self.clearButton.setBorder(None)
    
  def taskFieldFocusGained(self, event):
    self.taskField.selectAll()
    
  def notesFieldFocusGained(self, event):
    self.notesField.selectAll()
    
  def exitButtonMouseClicked(self, event):
    csvData = []
    for i in taskDB:
      csvData.append([i.taskName,
                      i.notes,
                      i.dateCreated,
                      int(i.done)])
      
    with open("toDoList.csv", "wb") as f:
      writer = csv.writer(f)
      writer.writerows(csvData)

    sys.exit()

  def addButtonMouseClicked(self, event):
    taskName = self.taskField.getText()
    notes = self.notesField.getText()
    
    self.taskField.setText("")
    self.notesField.setText("")
    
    if taskName == "":
      JOptionPane.showMessageDialog(None, "Empty field")
    else:
      x = task(taskName, notes, currentDate, False)
      taskDB.append(x)
      self.taskTable.getModel().addRow([taskName, notes, currentDate, str(False)])
    
  def clearButtonMouseClicked(self, event):
    del taskDB[:]
    self.taskTable.getModel().setRowCount(0)
  
if __name__ == "__main__":
  mainWindow().setVisible(True)