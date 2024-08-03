from tkinter import *
from tkinter import filedialog
import moviepy, os, time, re, mimetypes, threading
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
from moviepy.editor import ImageClip
from customtkinter import *
from customtkinter import filedialog
from proglog import ProgressBarLogger

print('>> Running...')

## Message box update and create new line
def message(text):
	message_label.insert(END, f'>> {text}\n')
	print(f'>> {text}')

# Please wait...
n = 1
def waiting():
	global n
	e = ['>> Please wait.', '>> Please wait..', '>> Please wait...']
	if n%3 == 0:
		print(e[2])
		n = 1
	if n%2 == 0:
		print(e[1])
	else:
		print(e[0])
	n += 1

## Browse for file function
def browse():
	global filename
	filename = filedialog.askopenfilename(initialdir = "./", title = "Select a File")

	if len(filename) != 0:
		if len(filename) >= 45:
			avar = filename[:45]+'...'
		else:
			avar = filename
		file_label.configure(text=avar)

		if mimetypes.guess_type(filename)[0].startswith('video'):
			message(':)')
			
			run_button.configure(state='normal')

		else:
			run_button.configure(state='disabled')
			message('Error. Please choose a video file.')
			


## Progress Bar - https://stackoverflow.com/questions/69423410/moviepy-getting-progress-bar-values
class MyBarLogger(ProgressBarLogger):

	def callback(self, **changes):
		pass
		# Every time the logger message is updated, this function is called with
		# the `changes` dictionary of the form `parameter: new value`.
		# for (parameter, value) in changes.items():
		#	message ('Parameter %s is now %s' % (parameter, value))
    
	def bars_callback(self, bar, attr, value,old_value=None):
		# Every time the logger progress is updated, this function is called        
		percentage = (value / self.bars[bar]['total']) * 100
		progbar.set(percentage/100)
		# message(bar,attr,percentage)

global logger
logger = MyBarLogger()


## Start program button
def start():
	openfile_button.configure(state='disabled')
	mute_button.configure(state='disabled')
	open_button.configure(state='disabled')
	message('JoJoTBCfying in progress. Please wait...')
	

	## JoJoTBCfier code:
	global file
	file = re.findall(r'.+(\/.+)$',filename)[0][1:]
	start_time = time.time()

	## Editing video

	# ~ Video clip ~
	
	v = mp.VideoFileClip(filename)
	final = v.duration-0.1 # Removes 0.1s from end of clip so that freeze frame doesnt loop to 1st frame



	# ~ Roundabout song ~	
	message('Adding roundabout.mp3...')
	
	
	song = './assets/roundabout.mp3'
	riff_time = 44.944

	start_song = final-riff_time
	audioclip = mp.AudioFileClip(song)
	audioclip = audioclip.set_start(t=start_song)  # Time at which song should start so riff is at end


	# ~ v1.2 edit - Adding Mute/No Audio function ~
	#v = v.set_audio('')
	global mute
	if mute.get() == 0: # If mute button not checked
		message('>> Not muting original audio')
		try:
		    fa = mp.CompositeAudioClip([audioclip, v.audio]) # If video contains audio, merge with song
		except AttributeError:
		    fa = mp.CompositeAudioClip([audioclip]) # Else just add audio
	elif mute.get() == 1: # If mute button checked
		message('Muting original audio')
		fa = mp.CompositeAudioClip([audioclip])



	# ~ Video Freeze Frame ~
	message('Creating freeze frame...')
	
	
	# Create Sepia image from last frame using PIL
	thumb = v.save_frame('./assets/thumbnail.jpg',t=final)
	tg = Image.open('./assets/thumbnail.jpg').convert('L') # Convert image to grayscale
	tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196') # Tinting sepia tones
	tinted.save('./assets/thumbnail.jpg')

	finalfr = mp.ImageClip('./assets/thumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final) # Open tinted frame as freeze frame
	
	# TBC arrow slide in	
	message('Adding To Be Continued arrow...')
	

	# tbcarrow = mp.ImageClip('./assets/tbcarrow.png')
	vidwid, vidhei = v.w, v.h
	message('WidthxHeight = '+str(vidwid)+'x'+str(vidhei))

	# tbcarrow = tbcarrow.resize(width=(vidwid*0.4)) # Resizing arrow to 40% of video width

	##  ~ Arrow slide animation ~
	arrow = Image.open('./assets/tbcarrow.png')
	arrow_ratio = arrow.size[0]/arrow.size[1] # Aspect ratio of arrow 

	arrow_sizex = int(round(v.w*0.4)) # Arrow width to 40% of video width
	arrow_sizey = int(round((v.h*0.4)/arrow_ratio)) # Scale arrow height to preserve aspect ratio
	arrow = arrow.resize((arrow_sizex, arrow_sizey))

	arrow_posx, arrow_posy = int(round(v.w*0.1)), int(round(v.h*0.7)) # Pastes arrow 10% across x axis, and 50% down y axis of video

	# Arrow Frame (transparent layer)
	arrow_frame = Image.new('RGBA', (v.w, v.h), (0,0,0,0)) # Blank image with dimensions of video

	#https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
	arrow_frame.paste(arrow, (arrow_posx, arrow_posy), arrow) # need to specify arrow as mask (after position tuple), so that it removes the alpha part and only pastes the visible part of image
	arrow_frame.save('./assets/arrow_frame.png', 'PNG')

	arrow_frame = mp.ImageClip('./assets/arrow_frame.png')

	slide = mp.CompositeVideoClip([arrow_frame.fx(mp.transfx.slide_in, 0.3, 'right').set_duration(audioclip.duration-riff_time)]) # Slides in from set position (width of image)


	#  ~ Exporting video ~
	message('Creating video...')
	

	# fv = mp.CompositeVideoClip([v, finalfr, tbcarrow.set_pos(('left','bottom')).set_start(final).set_duration(audioclip.duration-riff_time)]) #add tbc arrow
	fv = mp.CompositeVideoClip([v, finalfr, slide.set_start(final).set_duration(audioclip.duration-riff_time)]) #add tbc arrow
	fva = fv.set_audio(fa).set_end(fv.duration-0.1)
	fva = fva.set_fps(fps=30)

	extindex = file.rfind('.') # finding final . for extension	
	dt = time.strftime('%d-%m-%y_%H-%M-%S')

	global fpath
	file = f'{file[0:extindex]}_{dt}.mp4' # replacing extension with .mp4
	fpath = os.path.realpath(f'./jojofied/jojofied_{file}')

	message('Exporting video...')
	fva.write_videofile(fpath, logger=logger)

	v.close()
	audioclip.close()

	if len(fpath) > 40:
		message(f'Done. Video output at {fpath[:40]}...')
	else:
		message(f'Done. Video output at {fpath}')

	print(os.path.realpath(fpath))
	


	# ~ Resetting GUI ~
	#run_button.configure(state='disabled')
	openfile_button.configure(state='normal')
	mute_button.configure(state='normal')
	open_button.configure(state='normal')


## ~ Opening file ~
def openvideo():
	os.startfile(fpath)


### GUI ###

colourmain = '#e23f9f'
colourdark = '#901d61'

master = CTk()
master.iconbitmap('./assets/tbcarrowicon.ico')
master.title('JoJoTBCfier v2.4.3 GUI')
master.geometry('800x600')
master.resizable(False, False)


mainframe = CTkFrame(master) # Split window in half for image on left side
mainframe.grid(row=0, column=0)

leftframe = CTkFrame(mainframe, width=310, height=600) # Left side - for image
leftframe.grid(row=0, column=0, padx=0, ipadx=0)

bkg = PhotoImage(file='./assets/bkg.png')
setb = CTkLabel(leftframe, text='', image=bkg)
setb.place(x=0, y=0, relwidth=1, relheight=1)

rightframe = CTkFrame(mainframe, height=600) # Right side - for GUI elements
rightframe.grid(row=0, column=1)

rows = ['title', 'fileselect', 'mute', 'message', 'progbar', 'start']


## Title
title_label = CTkLabel(rightframe, text='JoJo TBC Meme Creator', font=('Calibri', 30), text_color=colourmain)
title_label.grid(row=rows.index('title'), column=0)


## File select
file_frame = CTkFrame(rightframe)
file_frame.grid(row=rows.index('fileselect'),column=0,padx=10,pady=10)
file_frame.pack_propagate(0)

file_label = CTkLabel(file_frame, text='Choose video file', width=300, anchor='w', wraplength=0)
file_label.grid(row=0,column=0,padx=10)

openfile_button = CTkButton(file_frame, text='Open File', command=browse, fg_color=colourmain, hover_color=colourdark, text_color='black')
openfile_button.grid(row=0,column=1)


## Mute audio check button
mute = IntVar()
mute.set(0)
mute_button = CTkCheckBox(rightframe, text='Mute original audio', variable=mute, fg_color=colourdark, text_color=colourmain, hover_color=colourmain)
mute_button.grid(row=rows.index('mute'), column=0)
mute_button.configure(state='normal')

# ## JoJoTBCfy
# run_button = CTkButton(master, text='JoJoTBCfy!', command=lambda:threading.Thread(target=start).start(), width=20, height=2, fg_color='#1d1c2c', text_color='#8d73ff')
# # master.rowconfigure(3, weight=1)
# # master.rowconfigure(4, pad=10)
# run_button.grid(row=4, column=0)
# run_button.configure(state='disabled')


## Messages
message_frame = CTkFrame(rightframe, width=300, height=400)
message_frame.grid(row=rows.index('message'),column=0, padx=10, pady=10)
message_frame.pack_propagate(0)

message_label = CTkTextbox(message_frame, text_color='#fff', width=400, height=350)
message_label.grid(row=0, column=0)

## Progress bar
global progvar
progvar = IntVar()
progvar.set(0)
progbar = CTkProgressBar(rightframe, orientation='horizontal', width=300, height=10, mode='determinate', fg_color='black', progress_color=colourmain, variable=progvar)
# progbar.set(0.6)
progbar.grid(row=rows.index('progbar'),column=0, pady=10)

## Run button
run_frame = CTkFrame(rightframe)
run_frame.grid(row=rows.index('start'),column=0, padx=10)

run_button = CTkButton(run_frame, text='JoJoTBC-fy!', command=lambda:threading.Thread(target=start).start(), fg_color=colourmain, hover_color=colourdark, text_color='black', state='disabled', text_color_disabled=colourdark)
run_button.grid(row=0,column=0, padx=10, pady=10)

open_button = CTkButton(run_frame, text='Open Video', command=openvideo, fg_color=colourmain, hover_color=colourdark, text_color='black', state='disabled', text_color_disabled=colourdark)
open_button.grid(row=0,column=1, padx=10)
open_button.configure(state='disabled')



master.mainloop()
