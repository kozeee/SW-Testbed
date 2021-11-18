from tkinter import *
from exportmessagestoexcel import exportmessagestoxl
from exportmessagestoexcel import getnums

def messagestoexcel():
    csvorxlsx = filetype.get()
    filename = fileform.get()
    phonenum = phonenumtype.get()
    exportmessagestoxl(csvorxlsx, filename, phonenum)

root = Tk()

fileformlable = Label(root, text="Enter the name of your file")
fileformlable.pack()
fileform = Entry(root)
fileform.pack()

filetype = StringVar()
filetype.set("csv")

phonenumtype = StringVar()
phonenumtype.set(getnums()[0])

fileoptions = ["csv" , "xlsx"]
exdropmenu = OptionMenu(root, filetype, *fileoptions)
dropmenulabel = Label(root, text="choose between csv or xlsx format")
dropmenulabel.pack()
exdropmenu.pack()

getnumsdrop = OptionMenu(root, phonenumtype, *getnums())
phonemenulabel = Label(root, text="choose a phone number")
phonemenulabel.pack()
getnumsdrop.pack()

exportButton = Button(root, text="Export", command=messagestoexcel)
exportbuttonlable=Label(root,text="Press export to save your file with the desired settings")
exportbuttonlable.pack()
exportButton.pack()


root.mainloop()


