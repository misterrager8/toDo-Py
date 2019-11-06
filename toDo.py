from java.awt import *
from javax.swing import *
import sys
from datetime import datetime
from taskModel import task

currentDate = datetime.now().strftime("%m/%d/%Y")
taskDB = []

class mainWindow(JFrame):
  
  def __init__(self):
    super(mainWindow, self).__init__()
    self.initComponents()
    
  def initComponents(self):

    bgPanel = JPanel()
    exitButton = JLabel(mouseClicked = self.exitButtonMouseClicked)
    addButton = JLabel(mouseClicked = self.addButtonMouseClicked)
    deleteButton = JLabel()
    clearButton = JLabel()
    jScrollPane1 = JScrollPane()
    taskTable = JTable()
    taskField = JTextField()
    notesField = JTextField()
    taskLabel = JLabel()
    notesLabel = JLabel()

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    bgPanel.setBackground(Color(51, 153, 255))

    exitButton.setText("X")
    exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    addButton.setBackground(Color(51, 204, 255))
    addButton.setHorizontalAlignment(SwingConstants.CENTER)
    addButton.setText("Add Task")
    addButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    addButton.setOpaque(True)

    deleteButton.setBackground(Color(51, 204, 255))
    deleteButton.setHorizontalAlignment(SwingConstants.CENTER)
    deleteButton.setText("Delete Task")
    deleteButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    deleteButton.setOpaque(True)

    clearButton.setBackground(Color(51, 204, 255))
    clearButton.setHorizontalAlignment(SwingConstants.CENTER)
    clearButton.setText("Delete All")
    clearButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    clearButton.setOpaque(True)

    taskTable.setModel(table.DefaultTableModel(
      [],
      ["Task", "Notes", "Date Created", "Done"]
    )
                      )
    jScrollPane1.setViewportView(taskTable)

    taskLabel.setText("Task")

    notesLabel.setText("Note(s)")

    bgPanelLayout = GroupLayout(bgPanel)
    bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGap(0, 0, sys.maxint)
            .addComponent(exitButton))
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
              .addComponent(addButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
              .addComponent(deleteButton, GroupLayout.DEFAULT_SIZE, 204, sys.maxint)
              .addComponent(clearButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
              .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, False)
                  .addComponent(taskLabel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
                  .addComponent(notesLabel, GroupLayout.DEFAULT_SIZE, 51, sys.maxint))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                  .addComponent(taskField)
                  .addComponent(notesField))))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(jScrollPane1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)))
        .addContainerGap())
    )
    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addComponent(exitButton)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
              .addComponent(taskField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
              .addComponent(taskLabel))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
              .addComponent(notesField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
              .addComponent(notesLabel))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(addButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 144, sys.maxint)
            .addComponent(deleteButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(clearButton, GroupLayout.PREFERRED_SIZE, 34, GroupLayout.PREFERRED_SIZE))
          .addComponent(jScrollPane1, GroupLayout.PREFERRED_SIZE, 0, sys.maxint))
        .addContainerGap())
    )

    layout = GroupLayout(self.getContentPane())
    self.getContentPane().setLayout(layout)
    layout.setHorizontalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
    )
    layout.setVerticalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
    )

    self.pack()
    self.setLocationRelativeTo(None)
    
  def exitButtonMouseClicked(self, event):
    sys.exit()
    
  def addButtonMouseClicked(self, event):
    JOptionPane.showMessageDialog(None, "Fn incomplete")
  
if __name__ == "__main__":
  mainWindow().setVisible(True)