# v2.3 - Added date time to file name, fade final frame into sepia freeze frame

from tkinter import *
from tkinter import filedialog
import moviepy, os, time, re, mimetypes, threading
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
from moviepy.editor import ImageClip

print('>> Running...')

master = Tk()
master.iconbitmap('tbcarrowicon.ico')
master.title('JoJoTBCfier v2.0 GUI')
master.geometry('400x225')
master.resizable(False, False)
bkg = PhotoImage(file='bkg.png')
setb = Label(master, image=bkg)
setb.place(x=0, y=0, relwidth=1, relheight=1)

## Browse for file function
def browse():
	global filename
	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File")

	if len(filename) != 0:
		if len(filename) >= 45:
			avar = filename[:45]+'...'
		else:
			avar = filename
		addrvar.set(avar)

		if mimetypes.guess_type(filename)[0].startswith('video'):
			mvar = ':)'
			messvar.set(mvar)
			startbutton.config(state='normal')

		else:
			startbutton.config(state='disabled')
			mvar = 'Error. Please choose a video file.'
			messvar.set(mvar)

# def muteaudio():
# 	print(mute.get())

## Start program button
def start():
	browsebutton.config(state='disabled')
	mutebutton.config(state='disabled')
	mvar = 'JoJoTBCfying in progress. Please wait...'
	messvar.set(mvar)

	## JoJoTBCfier code:

	file = re.findall(r'.+(\/.+)$',filename)[0][1:]
	start_time = time.time()

	## Editing video

	# ~ Video clip ~
	
	v = mp.VideoFileClip(filename)
	final = v.duration-0.1 # Removes 0.1s from end of clip so that freeze frame doesnt loop to 1st frame



	# ~ Roundabout song ~	
	mvar = 'Adding roundabout.mp3...'
	messvar.set(mvar)
	
	song = 'roundabout.mp3'
	riff_time = 44.944

	start_song = final-riff_time
	audioclip = mp.AudioFileClip(song)
	audioclip = audioclip.set_start(t=start_song)  # Time at which song should start so riff is at end


	# ~ v1.2 edit - Adding Mute/No Audio function ~
	#v = v.set_audio('')
	global mute
	if mute.get() == 0: # If mute button not checked
		print('>> Not muting original audio')
		try:
		    fa = mp.CompositeAudioClip([audioclip, v.audio]) # If video contains audio, merge with song
		except AttributeError:
		    fa = mp.CompositeAudioClip([audioclip]) # Else just add audio
	elif mute.get() == 1: # If mute button checked
		print('>> Muting original audio')
		fa = mp.CompositeAudioClip([audioclip])



	# ~ Video Freeze Frame ~
	mvar = 'Creating freeze frame...'
	messvar.set(mvar)
	
	# Create Sepia image from last frame using PIL
	thumb = v.save_frame('thumbnail.jpg',t=final)
	tg = Image.open('thumbnail.jpg').convert('L') # Convert image to grayscale
	tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196') # Tinting sepia tones
	tinted.save('thumbnail.jpg')

	finalfr = mp.ImageClip('thumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final) # Open tinted frame as freeze frame
	
	# TBC arrow slide in	
	mvar = 'Adding To Be Continued arrow...'
	messvar.set(mvar)

	tbcarrow = mp.ImageClip('tbcarrow.png')
	vidwid, vidhei = v.w, v.h
	print('>> WidthxHeight = '+str(vidwid)+'x'+str(vidhei))

	tbcarrow = tbcarrow.resize(width=(vidwid*0.4)) # Resizing arrow to 40% of video width


	#  ~ Exporting video ~
	mvar = 'Exporting video...'
	messvar.set(mvar)

	fv = mp.CompositeVideoClip([v, finalfr, tbcarrow.set_pos(('left','bottom')).set_start(final).set_duration(audioclip.duration-riff_time)]) #add tbc arrow
	fva = fv.set_audio(fa).set_end(fv.duration-0.1)
	fva = fva.set_fps(fps=30)

	extindex = file.rfind('.') # finding final . for extension	
	dt = time.strftime('%d-%m-%y_%H-%M-%S')
	file = f'{file[0:extindex]}_{dt}.mp4' # replacing extension with .mp4
	fpath = f'./jojofied/jojofied_{file}'

	fva.write_videofile(fpath)


	# ~ Log File ~ 	
	mvar = 'Writing log file...'
	messvar.set(mvar)
	

	lf = open('log.txt','a+')
	lf.write(f'\n\n{dt}\n>> File: {file}\n>> Location: {fpath}\n>> Video Length: {fva.duration}\n>> Time Taken: {time.time()-start_time}')
	lf.close()

	if len({fpath}) >= 45:
		mvar = f'Done. Video output at {fpath[:35]}...'
	else:
		mvar = f'Done. Video output at {fpath}'
	messvar.set(mvar)


	# ~ Resetting GUI ~
	#startbutton.config(state='disabled')
	browsebutton.config(state='normal')
	mutebutton.config(state='normal')
	#mvar = ''
	#messvar.set(mvar)

	# ~ Opening file ~
	#os.startfile(fpath)



### GUI ###


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

## Mute audio check button
mute = IntVar()
mute.set(0)
mutebutton = Checkbutton(master, text='Mute original audio', variable=mute, bg='#1d1c2c', fg='#8d73ff', activebackground='#1d1c2c' , activeforeground='#8d73ff')
mutebutton.grid(row=3, column=0)
mutebutton.config(state='normal')

## JoJoTBCfy
startbutton = Button(master, text='JoJoTBCfy!', command=start, width=20, height=2, bg='#1d1c2c', fg='#8d73ff', activebackground='#1d1c2c' , activeforeground='#8d73ff')
# master.rowconfigure(3, weight=1)
master.rowconfigure(4, pad=10)
startbutton.grid(row=4, column=0)
startbutton.config(state='disabled')


## Messages
messvar = StringVar(master)
mvar = ''
messvar.set(mvar)

messlabel = Label(master, textvariable=messvar, anchor='center', width=58, bg='#1d1c2c', fg='#d7ceff')
messlabel.grid(row=5, column=0)


master.mainloop()
