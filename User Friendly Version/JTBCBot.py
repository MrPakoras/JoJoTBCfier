# Bot that edits video and adds To Be Continued to it
# ~ v1.5 - Resizing TBC Arrow ~
# ~ v1.55 - Cleaning up code ~

import moviepy, os, time, re, mimetypes
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
from moviepy.editor import ImageClip

## Choosing file to edit

flist = []
rootDir = './videos'
nth = 1
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        print('>> '+str(nth)+' - '+fname)
        flist.append(fname)
        nth += 1

if nth == 1:
    print('>> Error: There are no files. Place your videos in the "videos" folder!',end='')
    input()
    quit()

while True:
    fileinp = input("\n>> Enter number of video clip you'd like to edit:   ")

    if re.match(r'^[0-9]+$',fileinp):
        try:
            file = flist[(int(fileinp)-1)]
        except IndexError:
            print('>> Error 404. Please try again.')
            pass
        print(file)
        
        if mimetypes.guess_type('./videos/'+file)[0].startswith('video'):
            break

        else:
            print('>> Error. File must be a video!')

    else:
        print('>> Error 404. Please try again.')

print('>> File "'+file+'" chosen.')

start_time = time.time() # Timing Program

## Editing video

# ~ Video clip ~
v = mp.VideoFileClip('./videos/'+file)
final = v.duration-0.1 # Removes 0.1s from end of clip so that freeze frame doesnt loop to 1st frame


# ~ Roundabout song ~
song = 'roundabout.mp3'
riff_time = 44.944

start_song = final-riff_time
audioclip = mp.AudioFileClip(song)
audioclip = audioclip.set_start(t=start_song)  # Time at which song should start so riff is at end


# ~ v1.2 edit - Adding Mute/No Audio function ~
#v = v.set_audio('')

try:
    fa = mp.CompositeAudioClip([audioclip, v.audio]) # If video contains audio, merge with song
except AttributeError:
    fa = mp.CompositeAudioClip([audioclip]) # Else just add audio


# ~ Video Freeze Frame ~
# Create Sepia image from last frame using PIL
thumb = v.save_frame('thumbnail.jpg',t=final)
tg = Image.open('thumbnail.jpg').convert('L') # Convert image to grayscale
tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196') # Tinting sepia tones
tinted.save('thumbnail.jpg')

finalfr = mp.ImageClip('thumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final) # Open tinted frame as freeze frame


# TBC arrow slide in
tbcarrow = mp.ImageClip('tbcarrow.png')
vidwid, vidhei = v.w, v.h
print('>> WidthxHeight = '+str(vidwid)+'x'+str(vidhei))

tbcarrow = tbcarrow.resize(width=(vidwid*0.4)) # Resizing arrow to 40% of video width


# ~ Converting to .mp4 ~
extindex = file.rfind('.') # finding final . for extension
file = str(file[0:extindex])+'.mp4' # replacing extension with .mp4


#  ~ Exporting video ~
fv = mp.CompositeVideoClip([v, finalfr, tbcarrow.set_pos(('left','bottom')).set_start(final).set_duration(audioclip.duration-riff_time)]) #add tbc arrow
fva = fv.set_audio(fa).set_end(fv.duration-0.1)
fva = fva.set_fps(fps=30)
fva.write_videofile('./JoJofication/jojofied_'+file)


# ~ Log File ~ 
now = datetime.now()
dt = now.strftime('%a %d/%m/%y %I:%M:%S %p')

lf = open('log.txt','a+')
lf.write(f'\n\n{dt}\n>> File: {file}\n>> Location: ./JoJofication/jojofied_{file}\n>> Video Length: {fva.duration}\n>> Time Taken: {time.time()-start_time}')
lf.close()
