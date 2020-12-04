from tkinter import *
from tkinter import filedialog

master = Tk()
master.title('JoJoTBCfier v2.0 GUI')
master.geometry('400x225')
master.resizable(False, False)
bkg = PhotoImage(file='bkg.png')
setb = Label(master, image=bkg)
setb.place(x=0, y=0, relwidth=1, relheight=1)

## Browse for file function
def browse():
	filename = filedialog.askopenfilename(initialdir = "/", 
										  title = "Select a File", 
										  filetypes = (("Text files", 
														"*.txt*"), 
													   ("all files", 
														"*.*")))

	if len(filename) > 60:
		var = filename[:60]+'...'
	else:
		var = filename

	addrvar.set(var)

## Address bar
def clr1(event):
  event.widget.delete(0, 'end')
  return None

## Text
l1 = Label(master, text="Please select a file and click the 'JoJoTBCfy!' button").grid(row=0)

## Address bar and browse button

addrframe = Frame(master, width=400)
addrframe.pack_propagate(0)
addrframe.grid(row=2, column=0)

addrvar = StringVar(addrframe)
var = 'Please choose a file'
addrvar.set(var)

l2 = Label(addrframe, textvariable=addrvar).grid(row=0, column=0, sticky='we')

b1 = Button(addrframe, text='Browse', command=browse, width=9).grid(row=0, column=1, sticky=W, pady=4)

## JoJoTBCfy

b2 = Button(master, text='JoJoTBCfy!', command=browse, width=9).grid(row=4, column=0, sticky=W, pady=4)






master.mainloop()