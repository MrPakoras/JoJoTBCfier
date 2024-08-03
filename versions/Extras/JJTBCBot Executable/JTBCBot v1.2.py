import moviepy, os
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
import time, re

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

start_time = time.time()

v = mp.VideoFileClip('./videos/'+file)
final = v.duration-0.1 

song = './songs/roundabout_long.mp3'
riff_time = 44.944

start_song = final-riff_time
audioclip = mp.AudioFileClip(song)
audioclip = audioclip.set_start(t=start_song)

try:
    fa = mp.CompositeAudioClip([audioclip, v.audio])
except AttributeError:
    fa = mp.CompositeAudioClip([audioclip]) 

thumb = v.save_frame('thumbnail.jpg',t=final)
tg = Image.open('thumbnail.jpg').convert('L')
tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196')
tinted.save('thumbnail.jpg')

finalfr = mp.ImageClip('thumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final)

tbcarrow = mp.ImageClip('tbcarrow.png')
vidwid = v.w
print('>>>> Width = '+str(vidwid))

extindex = file.rfind('.')
file = str(file[0:extindex])+'.mp4'

fv = mp.CompositeVideoClip([v, finalfr, tbcarrow.set_pos(('left','bottom')).set_start(final).set_duration(audioclip.duration-riff_time)])
fva = fv.set_audio(fa).set_end(fv.duration-0.1)
fva = fva.set_fps(fps=30)
fva.write_videofile('./JoJofication/jojofied_'+file)

now = datetime.now()
dt = now.strftime('%a %d/%m/%y %I:%M:%S %p')

lf = open('log.txt','a+')
lf.write('\n\n'+dt+'\n>> File: '+file+'\n>> Location: ./JoJofication/jojofied_'+file+'\n>> Video Length: '+str(fva.duration)+'\n>> Time Taken: '+str(time.time()-start_time))
lf.close()
