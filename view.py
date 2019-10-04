import Tkinter

top = Tkinter.Tk()

def helloCallBack():
  print("Pressed")

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()