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

	if len(filename) > 55:
		avar = filename[:55]+'...'
	else:
		avar = filename

	if len(filename) != 0:
		addrvar.set(avar)
		startbutton.config(state='normal')

## Start program button
def start():
	browsebutton.config(state='disabled')


## Text
infolab = Label(master, width=58, justify='left', anchor='center', text="Please select a file and click the 'JoJoTBCfy!' button", bg='#1d1c2c', fg='#d7ceff')
master.rowconfigure(0, pad=20)
infolab.grid(row=0)



## Address bar and browse button
addrframe = Frame(master, width=400, bg='#1d1c2c')
addrframe.pack_propagate(0)
addrframe.grid(row=2, column=0)

addrvar = StringVar(addrframe)
avar = 'Please choose a file'
addrvar.set(avar)

addrlab = Label(addrframe, textvariable=addrvar, anchor='w', width=40, bg='#1d1c2c', fg='#d7ceff')
addrlab.grid(row=0, column=0, sticky='we')

browsebutton = Button(addrframe, text='Browse', command=browse, width=9, bg='#1d1c2c', fg='#8d73ff', activebackground='#1d1c2c' , activeforeground='#8d73ff')
browsebutton.config(state='normal')
browsebutton.grid(row=0, column=1, pady=4)



## JoJoTBCfy
startbutton = Button(master, text='JoJoTBCfy!', command=start, width=20, height=2, bg='#1d1c2c', fg='#8d73ff', activebackground='#1d1c2c' , activeforeground='#8d73ff')
# master.rowconfigure(3, weight=1)
master.rowconfigure(3, pad=20)
startbutton.grid(row=3, column=0, pady=4)
startbutton.config(state='disabled')


## Messages
messvar = StringVar(master)
mvar = ''
messvar.set(mvar)

messlabel = Label(master, textvariable=messvar, anchor='center', width=58, bg='#1d1c2c', fg='#d7ceff')
messlabel.grid(row=4, column=0)


master.mainloop()