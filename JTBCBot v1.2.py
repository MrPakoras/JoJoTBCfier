# Bot that edits video and adds To Be Continued to it

import moviepy, os
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
import time, re

## Choosing file to edit

flist = []
rootDir = './videos'
nth = 1
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        print('>> '+str(nth)+' - '+fname)
        flist.append(fname)
        nth += 1

while True:
    fileinp = int(input("Enter number of video clip you'd like to edit:   "))
    try:
        file = flist[(fileinp-1)]
        break
    except IndexError:
        print('Error 404. Please try again.')

print('>> File "'+file+'" chosen.')

start_time = time.time() # Timing Program

## Editing video

# ~ Video clip ~
v = mp.VideoFileClip('./videos/'+file)
final = v.duration-0.1 # Removes 0.1s from end of clip so that freeze frame doesnt loop to 1st frame


# ~ Roundabout song ~

# Calculating Lengh to play
'''
if final <= 4:
    song = './songs/roundabout_short.mp3' # Riff at 3.603s
    riff_time = 3.603
elif final >= 45:
    song = './songs/roundabout_long.mp3' # Riff at 44.944s
    riff_time = 44.944
else:
    song = './songs/roundabout_med.mp3' # Riff at 14.893s
    riff_time = 14.893
print('>> '+song)
'''
song = './songs/roundabout_long.mp3'
riff_time = 44.944

start_song = final-riff_time
audioclip = mp.AudioFileClip(song)
audioclip = audioclip.set_start(t=start_song)  # Time at which song should start so riff is at end

# ~ v1.2 edit - Adding Mute/No Audio function ~

#v = v.set_audio('')

try:
    fa = mp.CompositeAudioClip([audioclip, v.audio]) # If video contains audio, merge with song
except AttributeError:
    fa = mp.CompositeAudioClip([audioclip]) # Else skip

# ~ Video Freeze Frame ~

#vid_end = moviepy.video.fx.all.freeze(f, t=final, freeze_duration=(audioclip.duration-riff_time)) # FF duration from start of riff to end of song

# ~ Video yellow overlay ~
#f = f.fx( vfx.colorx, 120)

# Create Sepia image from last frame using PIL
#finalfr = f.to_ImageClip(t=final, duration=(audioclip.duration-riff_time)).set_start(final)
thumb = v.save_frame('thumbnail.jpg',t=final)
tg = Image.open('thumbnail.jpg').convert('L') # Convert image to grayscale
tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196') # Tintinng sepia tones
tinted.save('thumbnail.jpg')

finalfr = mp.ImageClip('thumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final) # Open tinted frame as freeze frame


# TBC arrow slide in
#tbcarrow = mp.ImageClip('tbcarrow.png').set_duration(10).resize(width=50).margin(left=10,bottom=10).set_pos(('left','bottom'))
tbcarrow = mp.ImageClip('tbcarrow.png')
vidwid = v.w
print('>>>> Width = '+str(vidwid))
#tbcarrow.resize()
#.resize(width=(f.size))

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
lf.write('\n\n'+dt+'\n>> File: '+file+'\n>> Location: ./JoJofication/jojofied_'+file+'\n>> Video Length: '+str(fva.duration)+'\n>> Time Taken: '+str(time.time()-start_time))
lf.close()
